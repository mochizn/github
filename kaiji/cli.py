"""コマンドラインインターフェース。

    python -m kaiji run                 # 直近2日分を収集・抽出・通知・アーカイブ
    python -m kaiji collect --days 30   # 過去30日分を収集(TDnetは約1か月分のみ閲覧可)
    python -m kaiji process             # 未処理PDFの抽出
    python -m kaiji search 受注 半導体  # 全文検索
    python -m kaiji orders --min 1e9    # 受注一覧(10億円以上)
    python -m kaiji company 6227        # 銘柄の開示タイムライン
    python -m kaiji show <id>           # 詳細
    python -m kaiji serve               # Web UI (http://127.0.0.1:8765)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import os
import sys
import textwrap

from . import pipeline
from .classify import LABELS
from .db import SearchQuery, Store
from .extract import format_yen
from .tdnet import TdnetClient
from .textutil import truncate

DEFAULT_DB = os.environ.get("KAIJI_DB", "data/kaiji.db")
DEFAULT_ARCHIVE = os.environ.get("KAIJI_ARCHIVE", "data/archive")


def _date(s: str) -> dt.date:
    return dt.date.fromisoformat(s.replace("/", "-")) if "-" in s or "/" in s else dt.datetime.strptime(s, "%Y%m%d").date()


def parse_amount(s: str | None) -> float | None:
    """'1e9' '10億' '500百万' '3000万' などを円に。"""
    if not s:
        return None
    s = s.strip().replace(",", "")
    for unit, mul in (("兆", 1e12), ("億", 1e8), ("百万", 1e6), ("万", 1e4)):
        if s.endswith(unit):
            return float(s[: -len(unit)]) * mul
    return float(s)


def _print_rows(rows: list[dict], as_json: bool, show_snippet: bool = True) -> None:
    if as_json:
        keep = ("id", "date", "time", "code", "name", "title", "category", "tags", "summary", "amount_yen",
                "direction", "order", "llm", "pdf_url", "snippet")
        print(json.dumps([{k: r.get(k) for k in keep} for r in rows], ensure_ascii=False, indent=1))
        return
    if not rows:
        print("該当なし")
        return
    for r in rows:
        badge = LABELS.get(r["category"], r["category"])
        amt = f"  {format_yen(r['amount_yen'])}" if r.get("amount_yen") else ""
        dirn = {"up": "  ↑上方", "down": "  ↓下方", "mixed": "  ↕"}.get(r.get("direction") or "", "")
        print(f"{r['date']} {r['time']}  {r['code']:<5} {truncate(r['name'], 14):<14} [{badge}]{amt}{dirn}")
        print(f"    {r['title']}")
        llm = r.get("llm") or {}
        text = llm.get("summary") or r.get("summary")
        if show_snippet and r.get("snippet") and r.get("snippet") != text:
            print("    > " + truncate(r["snippet"], 160))
        elif text:
            print("    = " + truncate(text, 160))
        print(f"    id={r['id']}")


def cmd_collect(store: Store, a: argparse.Namespace) -> None:
    client = TdnetClient(interval=a.interval)
    if a.date:
        dates = [_date(a.date)]
    else:
        end = _date(a.to) if a.to else pipeline.today_jst()
        start = _date(a.since) if a.since else end - dt.timedelta(days=a.days - 1)
        dates = [start + dt.timedelta(days=i) for i in range((end - start).days + 1)]
    res = pipeline.collect(store, client, dates)
    print(json.dumps(res, ensure_ascii=False))
    if not a.no_process:
        print(json.dumps(pipeline.process(store, client, limit=a.limit), ensure_ascii=False))


def cmd_process(store: Store, a: argparse.Namespace) -> None:
    client = TdnetClient(interval=a.interval)
    print(json.dumps(pipeline.process(store, client, limit=a.limit), ensure_ascii=False))


def cmd_run(store: Store, a: argparse.Namespace) -> None:
    client = TdnetClient(interval=a.interval)
    res = pipeline.run(store, client, days=a.days, archive_dir=None if a.no_archive else a.archive,
                       min_importance=a.min_importance, notify_since=a.notify_since)
    print(json.dumps(res, ensure_ascii=False, indent=1))


def cmd_summarize(store: Store, a: argparse.Namespace) -> None:
    if not pipeline.llm.enabled():
        print("LLM要約は無効です。KAIJI_LLM=1 と ANTHROPIC_API_KEY を設定してください。", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(pipeline.summarize(store, max_items=a.max), ensure_ascii=False))


def _query_from_args(a: argparse.Namespace, **over) -> SearchQuery:
    q = SearchQuery(
        text=" ".join(getattr(a, "query", []) or []),
        code=getattr(a, "code", None),
        category=getattr(a, "category", None),
        date_from=getattr(a, "since", None),
        date_to=getattr(a, "to", None),
        min_amount=parse_amount(getattr(a, "min", None)),
        min_importance=getattr(a, "importance", None),
        direction=getattr(a, "direction", None),
        title_only=getattr(a, "title_only", False),
        watch_only=getattr(a, "watch", False),
        sort=getattr(a, "sort", "date"),
        limit=getattr(a, "limit", 30),
    )
    for k, v in over.items():
        setattr(q, k, v)
    return q


def cmd_search(store: Store, a: argparse.Namespace) -> None:
    _print_rows(store.search(_query_from_args(a)), a.json)


def cmd_orders(store: Store, a: argparse.Namespace) -> None:
    rows = store.search(_query_from_args(a, category="order"))
    if a.json:
        _print_rows(rows, True)
        return
    if not rows:
        print("該当なし")
        return
    for r in rows:
        o = r.get("order") or {}
        amt = format_yen(r.get("amount_yen")) or ("非開示" if o.get("amount_undisclosed") else "-")
        print(f"{r['date']}  {r['code']:<5} {truncate(r['name'], 14):<14} {amt:>10}  {truncate(r['title'], 50)}")
        detail = " / ".join(x for x in (o.get("item"), o.get("counterparty"), o.get("period") or o.get("revenue_timing")) if x)
        if detail:
            print(f"      {truncate(detail, 150)}")


def cmd_metrics(store: Store, a: argparse.Namespace) -> None:
    items = store.order_metrics(metric=a.metric, min_yoy=a.min_yoy, since=a.since, code=a.code, limit=a.limit)
    if a.json:
        print(json.dumps([{"id": r["id"], "date": r["date"], "code": r["code"], "name": r["name"], **m} for r, m in items],
                         ensure_ascii=False, indent=1))
        return
    if not items:
        print("該当なし")
    for r, m in items:
        yoy = "   -   " if m.get("yoy_pct") is None else f"{m['yoy_pct']:+6.1f}%"
        print(f"{r['date']}  {r['code']:<5} {truncate(r['name'], 14):<14} {m['metric']:<4} {format_yen(m['value_yen']):>10} {yoy}")


def cmd_company(store: Store, a: argparse.Namespace) -> None:
    q = SearchQuery(code=a.code, category=a.category, limit=a.limit, date_from=a.since)
    _print_rows(store.search(q), a.json, show_snippet=False)


def cmd_show(store: Store, a: argparse.Namespace) -> None:
    r = store.get(a.id)
    if not r:
        print("not found", file=sys.stderr)
        sys.exit(1)
    if a.json:
        r.pop("body", None) if not a.body else None
        print(json.dumps(r, ensure_ascii=False, indent=1, default=str))
        return
    w = lambda s: textwrap.fill(s, width=90, initial_indent="  ", subsequent_indent="  ")  # noqa: E731
    print(f"{r['name']} ({r['code']})  {r['date']} {r['time']}")
    print(f"{r['title']}")
    print(f"分類: {', '.join(LABELS.get(t, t) for t in r['tag_list'])}  重要度: {r['importance']}  状態: {r['status']}")
    print(f"PDF: {r['pdf_url']}")
    if r.get("llm"):
        print("\n[AI要約]")
        print(w(r["llm"].get("summary", "")))
        for p in r["llm"].get("key_points", []):
            print("  ・" + p)
        if r["llm"].get("earnings_impact"):
            print("  業績影響: " + r["llm"]["earnings_impact"])
    if r.get("summary"):
        print("\n[要約]")
        print(w(r["summary"]))
    if r.get("order"):
        print("\n[受注情報]")
        for k, lab in (("item", "内容"), ("counterparty", "相手先"), ("amount_text", "金額(原文)"), ("period", "納期/期間"),
                       ("revenue_timing", "売上計上"), ("sales_ratio", "規模"), ("contract_date", "日付")):
            if r["order"].get(k):
                print(f"  {lab}: {r['order'][k]}")
        if r.get("amount_yen"):
            print(f"  金額(円換算): {format_yen(r['amount_yen'])}")
    for key, lab in (("reason", "理由"), ("outlook", "見通し/業績影響"), ("qualitative", "経営成績の概況(定性情報)")):
        if r.get(key):
            print(f"\n[{lab}]")
            txt = r[key] if a.full else truncate(r[key], 1200)
            for para in txt.splitlines():
                print(w(para))
    if r.get("metrics"):
        print("\n[受注高・受注残高]")
        for m in r["metrics"]:
            yoy = "" if m.get("yoy_pct") is None else f" (前年比 {m['yoy_pct']:+.1f}%)"
            print(f"  {m['metric']}: {format_yen(m['value_yen'])}{yoy}")
    if r.get("order_mentions"):
        print("\n[受注への言及]")
        for s in r["order_mentions"]:
            print("  ・" + s)
    if r.get("signals"):
        print("\n[シグナル]")
        for s in r["signals"]:
            mark = {"pos": "+", "neg": "-", "mixed": "±"}[s["polarity"]]
            print(f"  {mark} {s['text']}")
    if a.body and r.get("body"):
        print("\n[本文]")
        print(r["body"])


def cmd_stats(store: Store, a: argparse.Namespace) -> None:
    s = store.stats()
    s["by_category"] = {LABELS.get(k, k): v for k, v in s["by_category"].items()}
    s["last_run"] = store.get_meta("last_run")
    print(json.dumps(s, ensure_ascii=False, indent=1))


def cmd_watch(store: Store, a: argparse.Namespace) -> None:
    if a.action == "add":
        for c in a.codes:
            store.watch_add(c, a.note or "")
    elif a.action == "rm":
        for c in a.codes:
            store.watch_remove(c)
    for w in store.watchlist():
        print(f"{w['code']}\t{w['note']}")


def cmd_export(store: Store, a: argparse.Namespace) -> None:
    for p in pipeline.export_archive(store, a.archive):
        print(p)


def cmd_import(store: Store, a: argparse.Namespace) -> None:
    print(f"imported {pipeline.import_archive(store, a.archive)} rows")


def cmd_reprocess(store: Store, a: argparse.Namespace) -> None:
    """抽出ロジック改善後に再抽出する(status を new に戻す)。"""
    where = ["status IN ('done','error')"]
    params: list = []
    if a.since:
        where.append("date >= ?")
        params.append(a.since)
    if a.category:
        where.append("(',' || tags || ',') LIKE ?")
        params.append(f"%,{a.category},%")
    n = store.conn.execute(f"UPDATE disclosures SET status='new', attempts=0 WHERE {' AND '.join(where)}", params).rowcount
    store.commit()
    print(f"{n} rows reset")
    if not a.no_process:
        cmd_process(store, a)


def cmd_reclassify(store: Store, a: argparse.Namespace) -> None:
    """分類ルール変更後に既存データへ再適用する。新たに詳細抽出対象になったものは未処理に戻す。"""
    from .classify import classify

    changed = queued = 0
    for r in list(store.iter_all()):
        c = classify(r["title"], r["name"])
        tags = ",".join(c.tags)
        if tags == r["tags"] and c.importance == r["importance"]:
            continue
        fields = {"category": c.primary, "tags": tags, "importance": c.importance, "is_correction": int(c.is_correction)}
        if c.deep and r["status"] == "meta":
            fields["status"] = "new"
            queued += 1
        store.update(r["id"], **fields)
        changed += 1
    store.commit()
    print(f"{changed} rows reclassified, {queued} queued for extraction")


def cmd_notify(store: Store, a: argparse.Namespace) -> None:
    cats = set(a.category.split(",")) if a.category else None
    res = pipeline.notify_new(store, since=a.since or pipeline.today_jst().isoformat(), min_importance=a.min_importance,
                              categories=cats, dry_run=a.dry_run)
    print(json.dumps(res, ensure_ascii=False))


def cmd_serve(store: Store, a: argparse.Namespace) -> None:
    from .web import serve

    serve(store, host=a.host, port=a.port)


def cmd_site(store: Store, a: argparse.Namespace) -> None:
    from .site import build_site

    print(build_site(store, a.out, months=a.months))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="kaiji", description="適時開示から受注・定性情報を蓄積して検索するボット")
    p.add_argument("--db", default=DEFAULT_DB, help=f"SQLiteファイル (既定: {DEFAULT_DB})")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_filters(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--code", help="証券コード(カンマ区切りで複数可)")
        sp.add_argument("--category", "-c", help="カテゴリ: " + ",".join(k for k in LABELS))
        sp.add_argument("--since", help="開始日 YYYY-MM-DD")
        sp.add_argument("--to", help="終了日 YYYY-MM-DD")
        sp.add_argument("--min", help="最低金額 例: 1e9 / 10億 / 500百万")
        sp.add_argument("--importance", type=int, help="重要度の下限(0-3)")
        sp.add_argument("--direction", choices=["up", "down", "mixed"], help="業績修正の方向")
        sp.add_argument("--title-only", action="store_true", help="タイトルと社名のみ検索")
        sp.add_argument("--watch", action="store_true", help="ウォッチリスト銘柄のみ")
        sp.add_argument("--sort", choices=["date", "amount", "relevance"], default="date")
        sp.add_argument("--limit", "-n", type=int, default=30)
        sp.add_argument("--json", action="store_true")

    sp = sub.add_parser("collect", help="TDnetから一覧を取得(+PDF処理)")
    sp.add_argument("--date", help="特定日 YYYY-MM-DD")
    sp.add_argument("--days", type=int, default=1, help="今日から遡る日数")
    sp.add_argument("--since")
    sp.add_argument("--to")
    sp.add_argument("--limit", type=int, default=1000, help="処理するPDFの上限")
    sp.add_argument("--interval", type=float, default=1.0, help="リクエスト間隔(秒)")
    sp.add_argument("--no-process", action="store_true")
    sp.set_defaults(func=cmd_collect)

    sp = sub.add_parser("process", help="未処理PDFを抽出")
    sp.add_argument("--limit", type=int, default=500)
    sp.add_argument("--interval", type=float, default=1.0)
    sp.set_defaults(func=cmd_process)

    sp = sub.add_parser("reprocess", help="抽出をやり直す")
    sp.add_argument("--since")
    sp.add_argument("--category", "-c")
    sp.add_argument("--limit", type=int, default=5000)
    sp.add_argument("--interval", type=float, default=1.0)
    sp.add_argument("--no-process", action="store_true")
    sp.set_defaults(func=cmd_reprocess)

    sp = sub.add_parser("run", help="定期実行(収集→抽出→要約→通知→アーカイブ)")
    sp.add_argument("--days", type=int, default=2)
    sp.add_argument("--archive", default=DEFAULT_ARCHIVE)
    sp.add_argument("--no-archive", action="store_true")
    sp.add_argument("--min-importance", type=int, default=2)
    sp.add_argument("--notify-since", help="この日付以降の開示のみ通知(既定: 今日)")
    sp.add_argument("--interval", type=float, default=1.0)
    sp.set_defaults(func=cmd_run)

    sp = sub.add_parser("summarize", help="Claude APIで要約を付与")
    sp.add_argument("--max", type=int, default=30)
    sp.set_defaults(func=cmd_summarize)

    sp = sub.add_parser("search", help="全文検索")
    sp.add_argument("query", nargs="*", help='検索語(スペースでAND、-語で除外、"..."でフレーズ)')
    add_filters(sp)
    sp.set_defaults(func=cmd_search)

    sp = sub.add_parser("orders", help="受注・契約獲得の一覧")
    sp.add_argument("query", nargs="*")
    add_filters(sp)
    sp.set_defaults(func=cmd_orders)

    sp = sub.add_parser("metrics", help="決算短信の受注高・受注残高(前年比で絞り込み)")
    sp.add_argument("--metric", choices=["受注高", "受注残高"])
    sp.add_argument("--min-yoy", type=float, help="前年同期比の下限(%%)")
    sp.add_argument("--since")
    sp.add_argument("--code")
    sp.add_argument("--limit", "-n", type=int, default=50)
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_metrics)

    sp = sub.add_parser("company", help="銘柄の開示タイムライン")
    sp.add_argument("code")
    sp.add_argument("--category", "-c")
    sp.add_argument("--since")
    sp.add_argument("--limit", "-n", type=int, default=50)
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_company)

    sp = sub.add_parser("show", help="開示の詳細")
    sp.add_argument("id")
    sp.add_argument("--full", action="store_true", help="定性情報を省略せず表示")
    sp.add_argument("--body", action="store_true", help="本文も表示")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_show)

    sp = sub.add_parser("stats", help="件数など")
    sp.set_defaults(func=cmd_stats)

    sp = sub.add_parser("watch", help="ウォッチリスト(通知対象)")
    sp.add_argument("action", choices=["add", "rm", "ls"])
    sp.add_argument("codes", nargs="*")
    sp.add_argument("--note")
    sp.set_defaults(func=cmd_watch)

    sp = sub.add_parser("reclassify", help="分類ルールを既存データに再適用")
    sp.set_defaults(func=cmd_reclassify)

    sp = sub.add_parser("notify", help="未通知の重要開示を通知")
    sp.add_argument("--since")
    sp.add_argument("--min-importance", type=int, default=2)
    sp.add_argument("--category")
    sp.add_argument("--dry-run", action="store_true")
    sp.set_defaults(func=cmd_notify)

    sp = sub.add_parser("export", help="アーカイブ(月別gzip JSONL)へ書き出し")
    sp.add_argument("--archive", default=DEFAULT_ARCHIVE)
    sp.set_defaults(func=cmd_export)

    sp = sub.add_parser("import", help="アーカイブからDBを復元")
    sp.add_argument("--archive", default=DEFAULT_ARCHIVE)
    sp.set_defaults(func=cmd_import)

    sp = sub.add_parser("serve", help="Web UIを起動")
    sp.add_argument("--host", default="127.0.0.1")
    sp.add_argument("--port", type=int, default=8765)
    sp.set_defaults(func=cmd_serve)

    sp = sub.add_parser("site", help="静的サイト(GitHub Pages用)を生成")
    sp.add_argument("--out", default="site")
    sp.add_argument("--months", type=int, default=12, help="含める月数")
    sp.set_defaults(func=cmd_site)
    return p


def main(argv: list[str] | None = None) -> None:
    a = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO if a.verbose else logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    logging.getLogger("pdfminer").setLevel(logging.ERROR)
    store = Store(a.db)
    try:
        a.func(store, a)
    finally:
        store.close()


if __name__ == "__main__":
    main()
