#!/usr/bin/env python3
"""1年日足の取得と「大きく動いた日」の抽出（agent3, R1）。標準ライブラリのみ。

使い方:
    python3 scripts/fetch_prices.py            # 取得 → data/ に出力
    python3 scripts/fetch_prices.py --offline  # data/raw/*.json を再利用（再取得しない）

出典: Yahoo Finance chart API v8（https://query1.finance.yahoo.com/v8/finance/chart/<sym>?range=1y&interval=1d）
出力:
    data/raw/<sym>.json  API 応答そのまま（再現用）
    data/prices.csv      long 形式: date,symbol,open,high,low,close,adjclose,volume
    data/summary.md      期間リターン・最大下落・指標との相関/β
    data/big_moves.md    銘柄ごとの「大きく動いた日」（全員がイベント年表に使う）
    data/big_moves.csv   閾値超えの全件

方針:
- リターンは adjclose（配当・分割調整後）で計算
- 取得時点で取引時間中の当日バーは「未確定」として除外（基準日 = 全銘柄で確定している最新日）
- 大きな動き: 指標比の超過リターン（米国株は SMH、日本株は日経平均）の大きさ順に上位を出す。
  全件（|日次| >= 7% または |超過| >= 6%）は data/big_moves.csv。
  日本株は東京の取引時間が米国より先なので、「前の米国営業日の SMH」も併記する
"""
import csv
import datetime as dt
import json
import math
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RAW = os.path.join(DATA, "raw")

STOCKS = {
    "5803.T": "フジクラ", "6834.T": "精工技研", "5802.T": "住友電工",
    "LITE": "Lumentum", "COHR": "Coherent", "AAOI": "Applied Optoelectronics",
    "GLW": "Corning", "FN": "Fabrinet",
}
BENCH = {
    "SMH": "VanEck 半導体ETF", "^SOX": "フィラデルフィア半導体指数", "NVDA": "NVIDIA",
    "^GSPC": "S&P500", "QQQ": "Nasdaq100 ETF", "^N225": "日経平均", "1306.T": "TOPIX連動ETF",
    "JPY=X": "USD/JPY",
}
JP = {"5803.T", "6834.T", "5802.T"}
ABS_TH = 0.07
EXC_TH = 0.06
TOP_N = 15
TOP_W = 6
UA = "Mozilla/5.0 (research-bot admin@example.com)"


def fetch(sym, offline=False):
    path = os.path.join(RAW, sym.replace("^", "_") + ".json")
    if not offline:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?range=1y&interval=1d"
        for i in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=30) as r:
                    body = r.read()
                break
            except Exception as e:  # noqa: BLE001
                print(f"retry {sym}: {e}", file=sys.stderr)
                time.sleep(2 ** (i + 1))
        else:
            raise SystemExit(f"failed: {sym}")
        os.makedirs(RAW, exist_ok=True)
        with open(path, "wb") as f:
            f.write(body)
        time.sleep(0.5)
    with open(path) as f:
        return json.load(f)["chart"]["result"][0]


def parse(res):
    """date -> dict。取引時間中の未確定バーは除外。"""
    meta = res["meta"]
    tz = dt.timezone(dt.timedelta(seconds=meta["gmtoffset"]))
    q = res["indicators"]["quote"][0]
    adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose") or q["close"]
    reg = meta.get("currentTradingPeriod", {}).get("regular", {})
    rows = {}
    for i, ts in enumerate(res["timestamp"]):
        if q["close"][i] is None:
            continue
        d = dt.datetime.fromtimestamp(ts, tz).date()
        rows[d] = dict(open=q["open"][i], high=q["high"][i], low=q["low"][i],
                       close=q["close"][i], adjclose=adj[i], volume=q["volume"][i] or 0)
    # 異常値除去: 前後±5営業日の終値の中央値から ±50% 以上離れた日は配信側の誤り（例: 1306.T 2026-03-30/31 が 1/10 表示）
    ds = sorted(rows)
    bad = []
    for i, d in enumerate(ds):
        win = sorted(rows[x]["close"] for x in ds[max(0, i - 5):i + 6] if x != d)
        if win and abs(rows[d]["close"] / win[len(win) // 2] - 1) > 0.5:
            bad.append(d)
    for d in bad:
        print(f"drop glitch {meta['symbol']} {d}", file=sys.stderr)
        rows.pop(d)
    # 当日バーが取引時間中（regularMarketTime < 終了時刻）なら未確定として落とす
    if reg and rows:
        last = max(rows)
        end = dt.datetime.fromtimestamp(reg["end"], tz)
        if last == end.date() and meta.get("regularMarketTime", 0) < reg["end"] - 60:
            rows.pop(last)
    return rows


def rets(rows):
    ds = sorted(rows)
    return {ds[i]: rows[ds[i]]["adjclose"] / rows[ds[i - 1]]["adjclose"] - 1 for i in range(1, len(ds))}


def pct(x):
    return "—" if x is None else f"{x*100:+.1f}%"


def corr_beta(a, b):
    ks = sorted(set(a) & set(b))
    x = [b[k] for k in ks]; y = [a[k] for k in ks]
    n = len(ks)
    mx, my = sum(x) / n, sum(y) / n
    cxy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    vx = sum((xi - mx) ** 2 for xi in x); vy = sum((yi - my) ** 2 for yi in y)
    return cxy / math.sqrt(vx * vy), cxy / vx


def period_ret(rows, base, days):
    ds = [d for d in sorted(rows) if d <= base]
    start = base - dt.timedelta(days=days)
    prev = [d for d in ds if d <= start]
    s = prev[-1] if prev else ds[0]
    return rows[ds[-1]]["adjclose"] / rows[s]["adjclose"] - 1


def max_dd(rows, base):
    peak, mdd, pk_d, dd_rng = -1, 0, None, ("", "")
    for d in sorted(rows):
        if d > base:
            break
        p = rows[d]["adjclose"]
        if p > peak:
            peak, pk_d = p, d
        dd = p / peak - 1
        if dd < mdd:
            mdd, dd_rng = dd, (pk_d, d)
    return mdd, dd_rng


def main():
    offline = "--offline" in sys.argv
    allsyms = list(STOCKS) + list(BENCH)
    data, metas = {}, {}
    for s in allsyms:
        res = fetch(s, offline)
        data[s] = parse(res)
        metas[s] = res["meta"]
        print(f"{s}: {len(data[s])} bars, last {max(data[s])}", file=sys.stderr)

    # 基準日: 8社すべてで確定している最新日のうち最も早いもの（米国・日本の双方が確定）
    base = min(max(data[s]) for s in STOCKS)
    fetched = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    with open(os.path.join(DATA, "prices.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "symbol", "open", "high", "low", "close", "adjclose", "volume"])
        for s in allsyms:
            for d in sorted(data[s]):
                r = data[s][d]
                w.writerow([d, s] + [("" if r[k] is None else round(r[k], 4)) for k in ("open", "high", "low", "close", "adjclose")] + [r["volume"]])

    R = {s: rets(data[s]) for s in allsyms}

    # ---- summary.md
    L = [f"# 株価サマリー（基準日 {base}、取得 {fetched}、出典 Yahoo Finance chart API v8 [一次: 取引所データの再配信]）", "",
         "リターンは配当・分割調整後終値（adjclose）。通貨は現地通貨。1年 = 基準日から365日前以前の直近終値比。", "",
         "| 銘柄 | 名称 | 終値 | 1か月 | 3か月 | 6か月 | 1年 | 52週高値(日付) | 52週安値(日付) | 高値から | 最大下落(期間) | 相関/β vs SMH | 相関/β vs N225 |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in allsyms:
        rows = {d: v for d, v in data[s].items() if d <= base}
        last = rows[max(rows)]
        hi_d = max(rows, key=lambda d: rows[d]["high"] or 0); lo_d = min(rows, key=lambda d: rows[d]["low"] or 1e18)
        mdd, (a, b) = max_dd(rows, base)
        cs = corr_beta(R[s], R["SMH"]) if s != "SMH" else (1, 1)
        cn = corr_beta(R[s], R["^N225"]) if s != "^N225" else (1, 1)
        name = STOCKS.get(s) or BENCH.get(s)
        L.append(f"| {s} | {name} | {last['close']:,.2f} | {pct(period_ret(rows, base, 30))} | {pct(period_ret(rows, base, 91))} | "
                 f"{pct(period_ret(rows, base, 182))} | {pct(period_ret(rows, base, 365))} | {rows[hi_d]['high']:,.2f} ({hi_d}) | "
                 f"{rows[lo_d]['low']:,.2f} ({lo_d}) | {pct(last['close']/rows[hi_d]['high']-1)} | {pct(mdd)} ({a}→{b}) | "
                 f"{cs[0]:.2f}/{cs[1]:.2f} | {cn[0]:.2f}/{cn[1]:.2f} |")
    L += ["", "注: 日本株と SMH の相関は同日比較（時差のため過小評価になりうる）。big_moves.md では日本株に前の米国営業日の SMH を併記。",
          "注: 高値・安値はザラ場（high/low）、高値からの下落率は終値ベース。"]
    # 日本株: 前の米国営業日の SMH との相関/β（時差を補正）
    usd = sorted(R["SMH"])
    L += ["", "日本株 vs **前の米国営業日**の SMH（時差補正）: " + "、".join(
        f"{s} {c:.2f}/{b:.2f}" for s in sorted(JP) for c, b in [corr_beta(
            {d: v for d, v in R[s].items() if [x for x in usd if x < d]},
            {d: R["SMH"][[x for x in usd if x < d][-1]] for d in R[s] if [x for x in usd if x < d]})]) + "（相関/β）"]
    # 月次リターン表
    months = sorted({(d.year, d.month) for d in data["GLW"] if d <= base})
    L += ["", "## 月次リターン（月末終値比、adjclose）", "", "最初の月は前月末データがないため空欄、最後の月は基準日までの途中経過。", "", "| 銘柄 | " + " | ".join(f"{y%100:02d}/{m:02d}" for y, m in months) + " |",
          "|---|" + "---|" * len(months)]
    for s in allsyms:
        rows = {d: v for d, v in data[s].items() if d <= base}
        ends = {}
        for d in sorted(rows):
            ends[(d.year, d.month)] = rows[d]["adjclose"]
        cells, prev = [], None
        for ym in months:
            v = ends.get(ym)
            cells.append("" if prev is None or v is None else f"{(v/prev-1)*100:+.0f}%")
            prev = v if v is not None else prev
        L.append(f"| {s} | " + " | ".join(cells) + " |")
    with open(os.path.join(DATA, "summary.md"), "w") as f:
        f.write("\n".join(L) + "\n")

    # ---- big_moves.md / big_moves.csv
    us_days = sorted(R["SMH"])

    def prev_us(d):
        p = [x for x in us_days if x < d]
        return p[-1] if p else None

    B = [f"# 大きく動いた日（基準日 {base}、取得 {fetched}）", "",
         "この1年は値動きが非常に大きく、固定閾値（±7%）では AAOI だけで100日超になるため、**指標比の超過リターンの大きさ順**に並べる。",
         f"- 単日: 各銘柄の超過リターン |超過| の上位 {TOP_N} 日（σ = その銘柄の超過リターンの標準偏差。3σ 以上は ★）",
         f"- 5営業日: 重ならない5営業日窓の累積超過リターン上位 {TOP_W} 区間（ニュースが数日かけて織り込まれた局面を拾う）",
         f"- 全件（|日次| >= {ABS_TH:.0%} または |超過| >= {EXC_TH:.0%}）は data/big_moves.csv",
         "- 指標: 米国株 = SMH（同日）、日本株 = 日経平均（同日）。日本株には「前の米国営業日の SMH」も併記（米国の夜間の動きを東京が翌日に映すため）",
         "- 出来高倍率 = 当日出来高 ÷ 直前20営業日平均。ギャップ = 始値 ÷ 前日終値 − 1（寄り前/前日引け後のニュースなら大きい）",
         "- 「何に反応したか」はここには入れない。各担当が stocks/ の年表で出典付きで埋める", ""]
    body, allrows = [], []
    for s in STOCKS:
        rows = data[s]; ds = sorted(d for d in rows if d <= base)
        jp = s in JP
        bench = "^N225" if jp else "SMH"
        recs = []
        for i, d in enumerate(ds[1:], 1):
            r = R[s][d]; br = R[bench].get(d)
            if br is None:
                continue
            vols = [rows[x]["volume"] for x in ds[max(0, i - 20):i]]
            vr = rows[d]["volume"] / (sum(vols) / len(vols)) if vols and sum(vols) else None
            gap = rows[d]["open"] / rows[ds[i - 1]]["close"] - 1 if rows[d]["open"] else None
            pu = prev_us(d) if jp else None
            recs.append(dict(d=d, r=r, br=br, exc=r - br, psmh=R["SMH"].get(pu) if pu else None, pu=pu,
                             nvda=R["NVDA"].get(d), vr=vr, gap=gap, c=rows[d]["close"]))
        sd = math.sqrt(sum(x["exc"] ** 2 for x in recs) / len(recs))
        for x in recs:
            if abs(x["r"]) >= ABS_TH or abs(x["exc"]) >= EXC_TH:
                allrows.append([x["d"], s, round(x["r"], 4), bench, round(x["br"], 4), round(x["exc"], 4), round(x["exc"] / sd, 2),
                                "" if x["vr"] is None else round(x["vr"], 2), "" if x["gap"] is None else round(x["gap"], 4)])
        top = sorted(recs, key=lambda x: -abs(x["exc"]))[:TOP_N]
        top.sort(key=lambda x: x["d"])
        body += ["", f"## {s} {STOCKS[s]}（超過リターンσ = {sd*100:.1f}%/日）", ""]
        if jp:
            body += ["| 日付 | 日次 | 日経 | 超過 | σ | 前の米国日のSMH(日付) | 出来高倍率 | ギャップ | 終値 |", "|---|---|---|---|---|---|---|---|---|"]
        else:
            body += ["| 日付 | 日次 | SMH | 超過 | σ | NVDA | 出来高倍率 | ギャップ | 終値 |", "|---|---|---|---|---|---|---|---|---|"]
        for x in top:
            z = x["exc"] / sd
            zs = f"{z:+.1f}{' ★' if abs(z) >= 3 else ''}"
            vr = "—" if x["vr"] is None else f"{x['vr']:.1f}x"
            mid = f"{pct(x['psmh'])} ({x['pu']})" if jp else pct(x["nvda"])
            body.append(f"| {x['d']} | {pct(x['r'])} | {pct(x['br'])} | {pct(x['exc'])} | {zs} | {mid} | {vr} | {pct(x['gap'])} | {x['c']:,.2f} |")
        # 重ならない5営業日窓（累積超過 = 銘柄の5日リターン − 指標の5日リターン）
        adj = {d: rows[d]["adjclose"] for d in ds}
        badj = data[bench]
        wins = []
        for i in range(5, len(ds)):
            a, b = ds[i - 5], ds[i]
            if a in badj and b in badj:
                sr = adj[b] / adj[a] - 1; br5 = badj[b]["adjclose"] / badj[a]["adjclose"] - 1
                wins.append((abs(sr - br5), i, sr, br5))
        wins.sort(reverse=True)
        used, pick = set(), []
        for _, i, sr, br5 in wins:
            if any(j in used for j in range(i - 4, i + 1)):
                continue
            used.update(range(i - 4, i + 1))
            pick.append((ds[i - 4], ds[i], sr, br5))
            if len(pick) >= TOP_W:
                break
        pick.sort()
        body += ["", f"5営業日の大きな動き（{bench} 比）", "", "| 期間 | 銘柄 | 指標 | 超過 |", "|---|---|---|---|"]
        for a, b, sr, br5 in pick:
            body.append(f"| {a}→{b} | {pct(sr)} | {pct(br5)} | {pct(sr-br5)} |")
    # セクター全体の大きな日（SMH ±4%）
    body += ["", "## セクター全体が大きく動いた日（|SMH| >= 4%）", "",
             "同日の各銘柄の動き。日本株の列は**翌東京営業日**のリターン（米国の動きを映すのは翌日のため。東京の休日をはさむと2つの米国日が同じ東京日を指す）。", "",
             "| 日付 | SMH | NVDA | " + " | ".join(STOCKS) + " |", "|---|---|---|" + "---|" * len(STOCKS)]

    def next_jp(s, d):
        n = [x for x in sorted(R[s]) if x > d]
        return R[s][n[0]] if n else None

    for d in us_days:
        if d <= base and abs(R["SMH"][d]) >= 0.04:
            cells = [pct(next_jp(s, d) if s in JP else R[s].get(d)) for s in STOCKS]
            body.append(f"| {d} | {pct(R['SMH'][d])} | {pct(R['NVDA'].get(d))} | " + " | ".join(cells) + " |")
    with open(os.path.join(DATA, "big_moves.md"), "w") as f:
        f.write("\n".join(B + body) + "\n")
    allrows.sort(key=lambda x: (x[1], x[0]))
    with open(os.path.join(DATA, "big_moves.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "symbol", "ret", "bench", "bench_ret", "excess", "excess_sigma", "vol_ratio", "gap"])
        w.writerows(allrows)
    print(f"base={base}", file=sys.stderr)


if __name__ == "__main__":
    import urllib.parse  # noqa: E402
    main()
