#!/usr/bin/env python3
"""8社の直近4回の決算への株価反応（agent3, R4）。REPORT §5.2 #6「上振れ常連が決算日に下落」の検証用。

使い方: python3 scripts/earnings_reaction.py → data/earnings_reaction.md, data/earnings_reaction.csv

反応日の決め方:
- 米国: GLW は寄り前発表 → 発表当日。FN・LITE・COHR・AAOI は引け後発表 → 翌営業日（8-K の受付時刻 [一次]）
- 日本: 東証の取引終了 15:30 より前の開示（フジクラ 14:00、住友電工 15:00）→ 当日、16:00 以降（精工技研）→ 翌営業日
  （開示時刻は stocks/5803.md・5802.md・6834.md の TDnet [一次]）
指標: 米国株 SMH、日本株 日経平均。2日 = 反応日とその翌営業日の累計。
"""
import csv
import collections
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# 反応日（すでに上のルールで決めた日付）
EVENTS = {
    "GLW": ["2025-10-28", "2026-01-28", "2026-04-28", "2026-07-28"],
    "FN": ["2025-11-04", "2026-02-03", "2026-05-05", "2026-08-18"],
    "LITE": ["2025-11-05", "2026-02-04", "2026-05-06", "2026-08-12"],
    "COHR": ["2025-11-06", "2026-02-05", "2026-05-07", "2026-08-13"],
    "AAOI": ["2025-11-07", "2026-02-27", "2026-05-08", "2026-08-07"],
    "5803.T": ["2025-11-07", "2026-02-09", "2026-05-14", "2026-08-07"],
    "5802.T": ["2025-10-31", "2026-02-03", "2026-05-12", "2026-07-31"],
    "6834.T": ["2025-11-14", "2026-02-16", "2026-05-15", "2026-08-12"]  # 08-11 は祝日,
}
# 会社の数字が直前のガイダンス/会社予想を上回ったか（各 stocks/ の B [一次]）。日本は「同時に上方修正したか」
BEAT = {
    "GLW": ["上限", "上限", "上限超え", "上限超え"],
    "FN": ["上限超え"] * 4,
    "5803.T": ["上方修正", "上方修正", "期初予想(+11.8%)・中計", "上方修正(+39%)"],
    "5802.T": ["上方修正・増配", "上方修正", "期初予想・中計", "上方修正(+6%)"],
    "6834.T": ["上方修正", "上方修正", "期初予想(+7%)", "上方修正"],
}
JP = {"5803.T", "5802.T", "6834.T"}


def main():
    px = collections.defaultdict(dict)
    with open(os.path.join(DATA, "prices.csv")) as f:
        for r in csv.DictReader(f):
            if r["adjclose"]:
                px[r["symbol"]][r["date"]] = float(r["adjclose"])

    def ret(s, d, n):
        ds = sorted(px[s])
        if d not in px[s]:
            return None
        i = ds.index(d)
        if i + n - 1 >= len(ds):
            return None
        return px[s][ds[i + n - 1]] / px[s][ds[i - 1]] - 1

    rows = []
    for s, ds in EVENTS.items():
        b = "^N225" if s in JP else "SMH"
        for k, d in enumerate(ds):
            r1, r2 = ret(s, d, 1), ret(s, d, 2)
            b1, b2 = ret(b, d, 1), ret(b, d, 2)
            rows.append(dict(symbol=s, date=d, bench=b, ret1=r1, exc1=None if None in (r1, b1) else r1 - b1,
                             ret2=r2, exc2=None if None in (r2, b2) else r2 - b2,
                             note=BEAT.get(s, [""] * 4)[k]))
    with open(os.path.join(DATA, "earnings_reaction.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})

    p = lambda v: "—" if v is None else f"{v*100:+.1f}%"
    L = ["# 決算への株価反応（8社 × 直近4回、基準日 2026-10-02）", "",
         "再現: `python3 scripts/earnings_reaction.py`。反応日の決め方と出典はスクリプト冒頭。株価は data/prices.csv [一次: 計算]。",
         "超過 = 銘柄 − 指標（米国 SMH、日本 日経平均）。2日 = 反応日＋翌営業日。", "",
         "| 銘柄 | 2025年10〜11月 | 2026年1〜2月 | 2026年4〜5月 | 2026年7〜8月 | 超過がマイナスの回 | 超過の平均 |",
         "|---|---|---|---|---|---|---|"]
    by = collections.defaultdict(list)
    for r in rows:
        by[r["symbol"]].append(r)
    for s, rs in by.items():
        cells = [f"{p(r['exc1'])}（{r['date'][5:]}）" for r in rs]
        neg = sum(1 for r in rs if r["exc1"] is not None and r["exc1"] < 0)
        v = [r["exc1"] for r in rs if r["exc1"] is not None]; avg = sum(v) / len(v)
        L.append(f"| {s} | " + " | ".join(cells) + f" | {neg}/4 | {p(avg)} |")
    L += ["", "## 明細（反応日の騰落・超過、2日累計、会社の数字）", "",
          "| 銘柄 | 反応日 | 騰落 | 超過 | 2日 騰落 | 2日 超過 | 会社の数字（直前のガイダンス/予想に対して）|", "|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['symbol']} | {r['date']} | {p(r['ret1'])} | {p(r['exc1'])} | {p(r['ret2'])} | {p(r['exc2'])} | {r['note']} |")
    us = [r["exc1"] for r in rows if r["symbol"] not in JP and r["exc1"] is not None]
    jp = [r["exc1"] for r in rows if r["symbol"] in JP and r["exc1"] is not None]
    jp_up = [r["exc1"] for r in rows if r["symbol"] in JP and r["exc1"] is not None and "上方修正" in r["note"]]
    L += ["", "## 集計", "",
          f"- 米国5社（20回）: 超過がマイナス {sum(1 for x in us if x < 0)}/{len(us)} 回、平均 {p(sum(us)/len(us))}",
          f"- 日本3社（12回）: 超過がマイナス {sum(1 for x in jp if x < 0)}/{len(jp)} 回、平均 {p(sum(jp)/len(jp))}",
          f"- 日本3社のうち上方修正を伴った回（{len(jp_up)}回）: 平均 {p(sum(jp_up)/len(jp_up))}、マイナス {sum(1 for x in jp_up if x < 0)} 回"]
    with open(os.path.join(DATA, "earnings_reaction.md"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
