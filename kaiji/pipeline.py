"""収集 -> 抽出 -> (要約) -> 通知 -> アーカイブ のパイプライン。"""

from __future__ import annotations

import datetime as dt
import gzip
import io
import json
import logging
import os
from collections import defaultdict
from pathlib import Path

from . import llm, notify
from .classify import classify
from .db import ARCHIVE_FIELDS, Store, now_iso
from .extract import extract
from .pdftext import is_readable, pdf_to_text
from .tdnet import TdnetClient
from .textutil import truncate

log = logging.getLogger(__name__)
JST = dt.timezone(dt.timedelta(hours=9))


def today_jst() -> dt.date:
    return dt.datetime.now(JST).date()


def collect(store: Store, client: TdnetClient, dates: list[dt.date]) -> dict:
    """一覧を取得してメタ情報を登録する。"""
    res = {"days": 0, "seen": 0, "new": 0, "deep": 0}
    for d in dates:
        items = client.list_day(d)
        res["days"] += 1
        res["seen"] += len(items)
        for it in items:
            c = classify(it.title, it.name)
            if store.upsert_meta(it.to_dict(), c.primary, c.tags, c.importance, c.is_correction, c.deep):
                res["new"] += 1
                res["deep"] += int(c.deep)
        store.commit()
        log.info("collect %s: %d items", d, len(items))
    return res


def body_limit(tags: list[str]) -> int:
    # 決算短信の本文は大半が財務諸表なので定性情報のみで十分
    return 0 if "earnings" in tags else 12000


def _fetch_pdf(client: TdnetClient, row: dict) -> bytes | None:
    """PDFを取得。KAIJI_PDF_CACHE が設定されていればディスクにキャッシュする(再抽出用)。"""
    cache = os.environ.get("KAIJI_PDF_CACHE")
    path = Path(cache) / row["date"][:7] / f"{row['id']}.pdf" if cache else None
    if path and path.exists():
        return path.read_bytes()
    data = client.download(row["pdf_url"])
    if data and path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return data


def process(store: Store, client: TdnetClient, limit: int = 200) -> dict:
    """未処理の開示のPDFを取得し、抽出結果を保存する。"""
    res = {"done": 0, "error": 0}
    for row in store.pending(limit=limit):
        try:
            data = _fetch_pdf(client, row)
            if not data:
                raise RuntimeError("PDF not found")
            # 決算短信は定性情報が冒頭数ページにあるため全ページは読まない
            text = pdf_to_text(data, max_pages=8 if "earnings" in row["tag_list"] else 20)
            if not is_readable(text):
                # 画像PDF・文字コード表の無いPDF: タイトル等のメタ情報のみ保持
                store.update(row["id"], status="done", processed_at=now_iso(), error="no_text",
                             summary="(本文テキストを抽出できないPDFです。原文PDFを参照してください)")
                res["no_text"] = res.get("no_text", 0) + 1
                store.commit()
                continue
            ex = extract(text, row["title"], row["tag_list"])
            store.update(
                row["id"],
                status="done",
                processed_at=now_iso(),
                error=None,
                summary=ex.summary,
                lead=ex.lead,
                outlook=ex.outlook,
                reason=ex.reason,
                qualitative=ex.qualitative,
                body=truncate(ex.body, body_limit(row["tag_list"])) if body_limit(row["tag_list"]) else "",
                kv_json=ex.kv or None,
                order_json=ex.order or None,
                order_mentions_json=ex.order_mentions or None,
                signals_json=ex.signals or None,
                direction=ex.direction,
                amount_yen=ex.amount_yen,
            )
            res["done"] += 1
        except Exception as e:  # noqa: BLE001 - 1件の失敗で全体を止めない
            log.warning("process %s failed: %s", row["id"], e)
            store.update(row["id"], status="error", error=str(e)[:500], attempts=row["attempts"] + 1)
            res["error"] += 1
        store.commit()
    return res


def summarize(store: Store, max_items: int | None = None) -> dict:
    """Claude API で要約を付与(KAIJI_LLM=1 のときのみ)。"""
    res = {"summarized": 0}
    if not llm.enabled():
        return res
    max_items = max_items or int(os.environ.get("KAIJI_LLM_MAX_PER_RUN", "30"))
    cats = llm.target_categories()
    rows = [r for r in store.iter_all("status='done' AND llm_json IS NULL AND is_correction=0") if set(r["tag_list"]) & cats]
    rows.sort(key=lambda r: (r["importance"], r["date"], r["time"]), reverse=True)
    s = llm.Summarizer()
    for r in rows[:max_items]:
        try:
            out = s.summarize(r)
        except Exception as e:  # noqa: BLE001 - レート制限等は次回に回す
            log.warning("summarize stopped: %s", e)
            break
        if out:
            store.update(r["id"], llm_json=out, llm_model=s.model)
            store.commit()
            res["summarized"] += 1
    return res


def notify_new(store: Store, since: str, min_importance: int = 2, categories: set[str] | None = None,
               dry_run: bool = False) -> dict:
    """未通知の重要開示を通知する。ウォッチリスト銘柄は重要度に関係なく通知。"""
    res = {"notified": 0, "candidates": 0}
    watch = {w["code"] for w in store.watchlist()}
    rows = list(store.iter_all("notified_at IS NULL AND date >= ? AND status IN ('done','meta')", (since,)))
    for r in rows:
        hit = (r["importance"] >= min_importance and (not categories or set(r["tag_list"]) & categories)) or r["code"] in watch
        if not hit or r["category"] == "fund":
            continue
        res["candidates"] += 1
        if dry_run:
            print(notify.format_message(r), "\n")
            continue
        if notify.configured() and not notify.send(r):
            continue
        store.update(r["id"], notified_at=now_iso())
        res["notified"] += 1
    store.commit()
    return res


# ---------------------------------------------------------------------- archive

def _archive_path(root: Path, month: str) -> Path:
    return root / month[:4] / f"{month}.jsonl.gz"


def export_archive(store: Store, root: str | Path, months: list[str] | None = None) -> list[Path]:
    """月別 gzip JSONL へ書き出す(gitで履歴管理しやすいよう mtime=0 / id順)。"""
    root = Path(root)
    by_month: dict[str, list[dict]] = defaultdict(list)
    where, params = "1=1", ()
    if months:
        where = "substr(date,1,7) IN (%s)" % ",".join("?" * len(months))
        params = tuple(months)
    for r in store.iter_all(where, params):
        rec = {k: r.get(k) for k in ARCHIVE_FIELDS}
        for k in ("kv_json", "order_json", "order_mentions_json", "signals_json", "llm_json"):
            rec[k] = r.get(k[:-5])
        by_month[r["date"][:7]].append(rec)
    written = []
    for month, recs in sorted(by_month.items()):
        recs.sort(key=lambda x: (x["date"], x["time"], x["id"]))
        path = _archive_path(root, month)
        path.parent.mkdir(parents=True, exist_ok=True)
        buf = io.BytesIO()
        with gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0) as gz:
            for rec in recs:
                gz.write((json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))
        data = buf.getvalue()
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
            written.append(path)
    return written


def import_archive(store: Store, root: str | Path) -> int:
    n = 0
    for path in sorted(Path(root).glob("*/*.jsonl.gz")):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            n += store.import_rows(json.loads(line) for line in f if line.strip())
    return n


def run(store: Store, client: TdnetClient, days: int = 2, archive_dir: str | Path | None = None,
        notify_since: str | None = None, min_importance: int = 2, process_limit: int = 400) -> dict:
    """定期実行用: 直近 days 日分を収集 -> 処理 -> 要約 -> 通知 -> アーカイブ。"""
    today = today_jst()
    dates = [today - dt.timedelta(days=i) for i in range(days)]
    out = {"collect": collect(store, client, dates)}
    out["process"] = process(store, client, limit=process_limit)
    out["summarize"] = summarize(store)
    out["notify"] = notify_new(store, since=notify_since or today.isoformat(), min_importance=min_importance)
    if archive_dir:
        # 変更のあった月だけ書き換わる(内容が同じならファイルは更新されない)
        out["archive"] = [str(p) for p in export_archive(store, archive_dir)]
    store.set_meta("last_run", now_iso())
    store.commit()
    return out
