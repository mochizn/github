import datetime as dt
import gzip
import json
from pathlib import Path

import pytest

from kaiji import pipeline
from kaiji.classify import classify
from kaiji.db import SearchQuery, Store, parse_terms
from kaiji.tdnet import normalize_code, parse_list_html

FIX = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    "title,primary",
    [
        ("大口受注に関するお知らせ", "order"),
        ("大型案件の受注に関するお知らせ", "order"),
        ("英国連結子会社における新規防衛案件の契約獲得に関するお知らせ", "order"),
        ("2026年９月度 受注速報", "monthly"),
        ("財務上の特約が付された金銭消費貸借契約の締結に関するお知らせ", "capital"),
        ("シンジケートローン契約締結に関するお知らせ", "capital"),
        ("主要取引先との供給契約の解除に伴う損失等の計上、および2027年3月期通期連結業績予想の修正に関するお知らせ", "forecast"),
        ("TOPIX（東証株価指数）構成銘柄への新規採用に関するお知らせ", "other"),
        ("2027年２月期 第２四半期（中間期）決算短信〔日本基準〕（連結）", "earnings"),
        ("通期連結業績予想の修正に関するお知らせ", "forecast"),
        ("株式会社FCEとの資本業務提携に関するお知らせ", "alliance"),
        ("「中小企業成長加速化補助金」採択に関するお知らせ", "subsidy"),
        ("子会社設立に関するお知らせ", "other"),
        ("自己株式の取得状況に関するお知らせ", "shareholder"),
        ("第３期中期経営計画（2027年度～2030年度）の策定に関するお知らせ", "mtp"),
    ],
)
def test_classify(title, primary):
    assert classify(title).primary == primary


def test_classify_correction_lowers_importance():
    c = classify("（訂正）「大口受注に関するお知らせ」の一部訂正について")
    assert c.is_correction and c.importance <= 1


def test_normalize_code():
    assert normalize_code("72030") == "7203"
    assert normalize_code("130A0") == "130A"
    assert normalize_code("７２０３０") == "7203"


def test_parse_list_html():
    html = (FIX / "tdnet_list.html").read_text(encoding="utf-8")
    items, total = parse_list_html(html, dt.date(2026, 10, 9))
    assert total == 265
    assert len(items) == 3
    a, b = items[:2]
    assert a.code == "7603" and a.time == "19:30" and a.id == "140120261009549010"
    assert a.pdf_url.endswith("/inbs/140120261009549010.pdf")
    assert b.xbrl_url and b.xbrl_url.endswith(".zip")
    assert a.date == "2026-10-09"


def meta(id_, title, code="1234", name="テスト", date="2026-10-01", time="15:00"):
    return {"id": id_, "date": date, "time": time, "code": code, "name": name, "title": title,
            "pdf_url": f"https://example/{id_}.pdf", "xbrl_url": None, "exchange": "東", "history": ""}


@pytest.fixture
def store():
    s = Store(":memory:")
    for i, (title, code, date) in enumerate([
        ("大口受注に関するお知らせ", "6227", "2026-09-28"),
        ("通期連結業績予想の修正に関するお知らせ", "7203", "2026-10-01"),
        ("自己株式の取得状況に関するお知らせ", "7203", "2026-10-02"),
    ]):
        c = classify(title)
        s.upsert_meta(meta(f"id{i}", title, code=code, date=date), c.primary, c.tags, c.importance, c.is_correction, c.deep)
    s.update("id0", status="done", summary="内容: ウエハレベルパッケージ向けシステム / 金額: 約45.0億円",
             body="海外の大手半導体関連メーカー2社より受注", amount_yen=4.5e9, order_json={"item": "装置"})
    s.update("id1", status="done", reason="データセンター向け需要が堅調に推移し上方修正", direction="up")
    s.commit()
    return s


def test_search_fts_and_short_terms(store):
    assert [r["id"] for r in store.search(SearchQuery(text="半導体関連"))] == ["id0"]
    # 2文字語(trigramでは引けない)もヒットする
    assert [r["id"] for r in store.search(SearchQuery(text="受注"))] == ["id0"]
    assert {r["id"] for r in store.search(SearchQuery(text="お知らせ -受注"))} == {"id1", "id2"}
    r = store.search(SearchQuery(text="データセンター"))[0]
    assert "データセンター" in r["snippet"]


def test_search_filters(store):
    assert [r["id"] for r in store.search(SearchQuery(category="order"))] == ["id0"]
    assert [r["id"] for r in store.search(SearchQuery(min_amount=1e9))] == ["id0"]
    assert [r["id"] for r in store.search(SearchQuery(code="7203", date_from="2026-10-02"))] == ["id2"]
    assert [r["id"] for r in store.search(SearchQuery(direction="up"))] == ["id1"]
    store.watch_add("6227")
    assert [r["id"] for r in store.search(SearchQuery(watch_only=True))] == ["id0"]


def test_fts_follows_updates(store):
    store.update("id2", summary="自社株買いの進捗")
    store.commit()
    assert [r["id"] for r in store.search(SearchQuery(text="自社株買い"))] == ["id2"]


def test_parse_terms():
    assert parse_terms('受注 "過去 最高" -訂正') == (["受注", "過去 最高"], ["訂正"])


def test_archive_roundtrip(store, tmp_path):
    written = pipeline.export_archive(store, tmp_path)
    assert {p.name for p in written} == {"2026-09.jsonl.gz", "2026-10.jsonl.gz"}
    # 内容が同じなら再書き込みしない
    assert pipeline.export_archive(store, tmp_path) == []
    with gzip.open(tmp_path / "2026" / "2026-09.jsonl.gz", "rt", encoding="utf-8") as f:
        rec = json.loads(f.readline())
    assert rec["order_json"] == {"item": "装置"}
    s2 = Store(":memory:")
    assert pipeline.import_archive(s2, tmp_path) == 3
    r = s2.get("id0")
    assert r["order"] == {"item": "装置"} and r["amount_yen"] == 4.5e9
    assert [x["id"] for x in s2.search(SearchQuery(text="半導体関連"))] == ["id0"]


def test_notify_dry_run_marks_nothing(store, capsys):
    res = pipeline.notify_new(store, since="2026-09-01", dry_run=True)
    assert res["candidates"] == 2  # 受注 + 業績修正(自己株式は重要度1)
    assert "大口受注" in capsys.readouterr().out
    assert store.get("id0")["notified_at"] is None


def test_notify_marks_when_no_webhook(store, monkeypatch):
    monkeypatch.delenv("KAIJI_DISCORD_WEBHOOK", raising=False)
    monkeypatch.delenv("KAIJI_SLACK_WEBHOOK", raising=False)
    res = pipeline.notify_new(store, since="2026-09-01")
    assert res["notified"] == 2
    assert pipeline.notify_new(store, since="2026-09-01")["notified"] == 0


def test_order_metrics_query(store):
    store.update("id1", metrics_json=[{"metric": "受注高", "value_yen": 1e9, "yoy_pct": 52.2, "text": "a"},
                                      {"metric": "受注残高", "value_yen": 2e9, "yoy_pct": -3.0, "text": "b"}])
    store.commit()
    items = store.order_metrics(min_yoy=10)
    assert [(r["id"], m["metric"]) for r, m in items] == [("id1", "受注高")]
    assert len(store.order_metrics()) == 2


def test_migrate_adds_column(tmp_path):
    import sqlite3

    path = tmp_path / "old.db"
    c = sqlite3.connect(path)
    c.execute("CREATE TABLE disclosures (id TEXT PRIMARY KEY, date TEXT NOT NULL, time TEXT, code TEXT, name TEXT, title TEXT,"
              " category TEXT, tags TEXT, importance INTEGER, is_correction INTEGER, pdf_url TEXT, xbrl_url TEXT, exchange TEXT,"
              " history TEXT, status TEXT, attempts INTEGER, error TEXT, fetched_at TEXT, processed_at TEXT, summary TEXT, lead TEXT,"
              " outlook TEXT, reason TEXT, qualitative TEXT, body TEXT, kv_json TEXT, order_json TEXT, order_mentions_json TEXT,"
              " signals_json TEXT, direction TEXT, amount_yen REAL, llm_json TEXT, llm_model TEXT, notified_at TEXT)")
    c.commit()
    c.close()
    s = Store(path)
    assert "metrics_json" in {r[1] for r in s.conn.execute("PRAGMA table_info(disclosures)")}
