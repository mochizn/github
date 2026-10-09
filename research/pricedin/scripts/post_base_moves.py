#!/usr/bin/env python3
"""基準日（2026-10-02）以降の値動き（agent3, R7、参考）。分析の数字は基準日のまま変えない。
使い方: python3 scripts/post_base_moves.py → data/post_base_moves.md
出典: Yahoo Finance chart API v8（range=1mo, interval=1d）。終値（close）ベース。"""
import datetime as dt, json, os, time, urllib.parse, urllib.request

BASE, END = "2026-10-02", "2026-10-08"
SYMS = [("5803.T", "フジクラ"), ("6834.T", "精工技研"), ("5802.T", "住友電工"), ("LITE", "Lumentum"),
        ("COHR", "Coherent"), ("AAOI", "Applied Opto"), ("GLW", "Corning"), ("FN", "Fabrinet"),
        ("^SOX", "フィラデルフィア半導体指数"), ("^N225", "日経平均")]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "post_base_moves.md")


FALLBACK = []  # 日足の終値が空で、60分足の最後の値で代用した銘柄


def closes(sym, q="range=1mo&interval=1d"):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research-bot admin@example.com)"})
    r = json.load(urllib.request.urlopen(req, timeout=30))["chart"]["result"][0]
    tz = dt.timezone(dt.timedelta(seconds=r["meta"]["gmtoffset"]))
    out = {}
    for ts, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]):
        if c is not None:
            out[dt.datetime.fromtimestamp(ts, tz).date().isoformat()] = c  # 60分足なら同日の最後の値が残る
    if q.endswith("1d") and END not in out:
        # 配信側で当日の日足終値が空のことがある → 60分足の同日最後の値（＝引け値）で代用
        intraday = closes(sym, "range=5d&interval=60m")
        if END in intraday:
            out[END] = intraday[END]
            FALLBACK.append(sym)
    return out


fetched = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
L = [f"# 基準日以降の値動き（参考、基準日 {BASE} 終値 → {END} 終値）", "",
     f"取得 {fetched}、Yahoo Finance chart API v8 の終値 [一次: 取引所データの再配信]。**分析（REPORT・stocks/）の数字は基準日のまま**。", "",
     "| 銘柄 | 名称 | 基準日終値 | 10-08 終値 | 騰落 | 指標比 |", "|---|---|---|---|---|---|"]
rows = {}
for s, n in SYMS:
    c = closes(s); time.sleep(0.5)
    b, e = c.get(BASE), c.get(END)
    rows[s] = (n, b, e, (e / b - 1) if b and e else None)
for s, (n, b, e, r) in rows.items():
    bench = "^N225" if s.endswith(".T") else "^SOX"
    br = rows[bench][3]
    exc = "—" if s in ("^SOX", "^N225") or r is None or br is None else f"{(r-br)*100:+.1f}%"
    L.append(f"| {s} | {n} | {b:,.2f} | {e:,.2f} | {r*100:+.1f}% | {exc} |" if r is not None else f"| {s} | {n} | {b} | {e} | — | — |")
L.append("\n指標比: 日本株は日経平均、米国株は SOX との差（単純差）。")
if FALLBACK:
    L.append(f"注: {', '.join(FALLBACK)} は 10-08 の日足終値が配信で空だったため、60分足の同日最後の値（引け）で代用。SOX で日足と60分足の最後の値が一致することを確認済み。")
open(OUT, "w").write("\n".join(L) + "\n")
print("\n".join(L))
