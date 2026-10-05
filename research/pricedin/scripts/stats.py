#!/usr/bin/env python3
"""回帰・相関・日本株の時差反応（agent3, R2）。data/prices.csv から計算。標準ライブラリのみ。

使い方: python3 scripts/stats.py  → data/stats.md、data/corr.csv

1. 8社の日次リターンを ^SOX・NVDA それぞれで単回帰（β・R²）。1年・前半・後半
   日本株は「前の米国営業日」の SOX/NVDA と、同日の日経平均で回帰（時差補正）
2. 相関行列（8社＋指標、同日。日本株の対米国は時差のため過小評価）
3. 米国5社の決算反応日の翌東京営業日に、日本3社がどう動いたか（簡易イベントスタディ）
"""
import csv
import collections
import datetime as dt
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
STOCKS = ["5803.T", "6834.T", "5802.T", "LITE", "COHR", "AAOI", "GLW", "FN"]
JP = {"5803.T", "6834.T", "5802.T"}
BENCH = ["SMH", "^SOX", "NVDA", "^GSPC", "^N225", "1306.T", "JPY=X"]
BASE = "2026-10-02"
SPLIT = "2026-04-01"  # 前半/後半の境目

# 米国5社の決算反応日（米国時間）。GLW は寄り前発表で当日、他4社は引け後発表で翌営業日。
# 出典: SEC 8-K（Item 2.02）の提出日・受付時刻 [一次]
EARN = {
    "GLW": ["2025-10-28", "2026-01-28", "2026-04-28", "2026-07-28"],
    "FN": ["2025-11-04", "2026-02-03", "2026-05-05", "2026-08-18"],
    "LITE": ["2025-11-05", "2026-02-04", "2026-05-06", "2026-08-12"],
    "COHR": ["2025-11-06", "2026-02-05", "2026-05-07", "2026-08-13"],
    "AAOI": ["2025-11-07", "2026-02-27", "2026-05-08", "2026-08-07"],
}


def load():
    px = collections.defaultdict(dict)
    with open(os.path.join(DATA, "prices.csv")) as f:
        for r in csv.DictReader(f):
            if r["date"] <= BASE and r["adjclose"]:
                px[r["symbol"]][r["date"]] = float(r["adjclose"])
    R = {}
    for s, p in px.items():
        ds = sorted(p)
        R[s] = {ds[i]: p[ds[i]] / p[ds[i - 1]] - 1 for i in range(1, len(ds))}
    return R


def reg(y, x):
    ks = sorted(set(y) & set(x))
    n = len(ks)
    if n < 20:
        return None
    xs = [x[k] for k in ks]; ys = [y[k] for k in ks]
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs); syy = sum((b - my) ** 2 for b in ys)
    return sxy / sxx, sxy * sxy / (sxx * syy), n


def lagged(Rjp, Rus):
    """日本株の t 日に、米国の t より前の直近営業日のリターンを対応させる。"""
    us = sorted(Rus)
    out, j = {}, 0
    for d in sorted(Rjp):
        while j < len(us) and us[j] < d:
            j += 1
        if j:
            out[d] = Rus[us[j - 1]]
    return out


def main():
    R = load()
    L = [f"# 回帰・相関・時差反応（基準日 {BASE}、data/prices.csv の adjclose から計算 [一次: 計算]）", "",
         "再現: `python3 scripts/stats.py`。agent4 の要因分解（data/agent4_factor.md）と補完関係: こちらは単回帰で指標ごとの β・R² を並べる。", "",
         f"## 1. β と R²（1年 / 前半 〜{SPLIT} / 後半 {SPLIT}〜）", "",
         "日本株の SOX・NVDA は**前の米国営業日**のリターン（時差補正）。日経は同日。", "",
         "| 銘柄 | 説明変数 | β 1年 | R² 1年 | β 前半 | R² 前半 | β 後半 | R² 後半 |", "|---|---|---|---|---|---|---|---|"]
    for s in STOCKS:
        xs = [("^SOX", "SOX"), ("NVDA", "NVDA")] + ([("^N225", "日経(同日)")] if s in JP else [])
        for b, name in xs:
            x = lagged(R[s], R[b]) if (s in JP and b != "^N225") else R[b]
            cells = []
            for lo, hi in (("0", "9"), ("0", SPLIT), (SPLIT, "9")):
                y = {d: v for d, v in R[s].items() if lo <= d < hi}
                r = reg(y, x)
                cells += [f"{r[0]:.2f}", f"{r[1]:.2f}"] if r else ["—", "—"]
            L.append(f"| {s} | {name} | " + " | ".join(cells) + " |")
    L += ["", "読み方: R² は日次の値動きのうち、その指標1つで説明できる割合。NVDA の R² が SOX より低い銘柄は「NVIDIA 個社より半導体全体に連動」。"]

    # 相関行列
    syms = STOCKS + ["SMH", "^SOX", "NVDA", "^GSPC", "^N225", "JPY=X"]
    M = [[None] * len(syms) for _ in syms]
    for i, a in enumerate(syms):
        for j, b in enumerate(syms):
            r = reg(R[a], R[b])
            M[i][j] = math.copysign(math.sqrt(r[1]), r[0]) if r else float("nan")
    with open(os.path.join(DATA, "corr.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([""] + syms)
        for a, row in zip(syms, M):
            w.writerow([a] + [f"{v:.3f}" for v in row])
    L += ["", "## 2. 相関行列（1年、同日の日次リターン。全体は data/corr.csv）", "",
          "| | " + " | ".join(syms) + " |", "|---|" + "---|" * len(syms)]
    for a, row in zip(syms, M):
        L.append(f"| {a} | " + " | ".join(f"{v:.2f}" for v in row) + " |")
    # 日本株×米国株の時差補正相関
    L += ["", "日本株 × 前の米国営業日の米国株（時差補正後の相関）", "",
          "| | " + " | ".join(s for s in STOCKS if s not in JP) + " | SOX | NVDA |", "|---|" + "---|" * 7]
    for s in sorted(JP):
        cells = []
        for b in [x for x in STOCKS if x not in JP] + ["^SOX", "NVDA"]:
            r = reg(R[s], lagged(R[s], R[b]))
            cells.append(f"{math.copysign(math.sqrt(r[1]), r[0]):.2f}")
        L.append(f"| {s} | " + " | ".join(cells) + " |")

    # 時差のイベントスタディ
    jp_days = sorted(R["5803.T"])

    def next_jp(d):
        n = [x for x in jp_days if x > d]
        return n[0] if n else None

    L += ["", "## 3. 米国の光株の決算反応日 → 翌東京営業日の日本3社（簡易イベントスタディ）", "",
          "米国の反応日（GLW は発表当日、他は発表翌日）の米国株リターンと、その次の東京営業日の日本株リターン（日経比の超過も）。出典: 8-K 提出日 [一次]。", "",
          "| 米国の反応日 | 銘柄 | 米国株 | SOX | 東京の日付 | 5803 | 6834 | 5802 | 3社平均の日経比 |", "|---|---|---|---|---|---|---|---|---|"]
    rows = []
    for t, ds in EARN.items():
        for d in ds:
            j = next_jp(d)
            jr = [R[s].get(j) for s in ["5803.T", "6834.T", "5802.T"]]
            n = R["^N225"].get(j)
            exc = sum(x - n for x in jr) / 3 if None not in jr and n is not None else None
            rows.append((d, t, R[t].get(d), R["^SOX"].get(d), j, jr, exc))
    rows.sort()
    f = lambda v: "—" if v is None else f"{v*100:+.1f}%"
    for d, t, ur, sr, j, jr, exc in rows:
        L.append(f"| {d} | {t} | {f(ur)} | {f(sr)} | {j} | " + " | ".join(f(x) for x in jr) + f" | {f(exc)} |")
    # 要約: 米国株の超過（対SOX）と日本株の超過の相関
    pairs = [(ur - sr, exc) for _, _, ur, sr, _, _, exc in rows if None not in (ur, sr, exc)]
    if pairs:
        xs = {i: p[0] for i, p in enumerate(pairs)}; ys = {i: p[1] for i, p in enumerate(pairs)}
        n = len(pairs); mx = sum(xs.values()) / n; my = sum(ys.values()) / n
        sxy = sum((xs[i] - mx) * (ys[i] - my) for i in xs); sxx = sum((xs[i] - mx) ** 2 for i in xs); syy = sum((ys[i] - my) ** 2 for i in ys)
        same = sum(1 for a, b in pairs if a * b > 0)
        L += ["", f"要約: 米国株の対SOX超過と、翌日の日本3社の対日経超過の相関 {sxy/math.sqrt(sxx*syy):.2f}、傾き {sxy/sxx:.2f}（n={n}）。符号が一致した回 {same}/{n}。",
              "（n が小さく、同じ日に業界ニュースが重なる回もあるので参考値）"]
    with open(os.path.join(DATA, "stats.md"), "w") as fo:
        fo.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
