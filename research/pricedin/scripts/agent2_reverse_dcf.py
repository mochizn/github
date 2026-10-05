#!/usr/bin/env python3
"""逆算DCF（agent2, R3）: LITE・COHR・AAOI の株価が要求する売上・利益の水準を求める。

モデルは research/photonics/scripts/reverse_dcf.py と同じ考え方を簡略化したもの。
- 売上 R_t = R_0 (1+g)^t（t=1..N, N=5）
- FCF マージンは m0 から mT へ N 年で直線的に移る
- 終端価値 TV_N = FCF_N (1+gT) / (WACC − gT)
- EV = Σ FCF_t/(1+WACC)^t + TV_N/(1+WACC)^N を満たす g を二分法で解く
出口PER法: 時価総額 × (1+ke)^N = 純利益_N × 出口PER → 必要な N 年後の純利益・EPS

入力の出典（基準日 2026-10-02 終値、data/prices.csv [一次]）:
- 株数・現金・負債: SEC XBRL companyfacts（10-K/10-Q）[一次]。希薄化は stocks/<ticker>.md B 節
- 基準売上: 直近四半期ガイダンス中央値 ×4（8-K EX-99.1 [一次]、年率化は [推測]）
- コンセンサス: 報道・集計サイト [二次]（stocks/<ticker>.md D 節に URL）
使い方: python3 scripts/agent2_reverse_dcf.py > data/agent2_reverse_dcf.md
"""

INPUTS = {
    "LITE": dict(
        price=1085.42,
        # 希薄化後 1.01億株: FY26 Q4 non-GAAP NI $326.3M ÷ EPS $3.23（EX-99.1 [一次]、計算）。
        # 10-K 表紙の普通株 8,970万株（2026-08-14）＋ NVIDIA 優先株 288万株 ＋ 転換社債（イン・ザ・マネー、株式扱い）
        shares=101.0,
        # 現金 $2,043.5M ＋ 短期投資 $694.9M（2026-06-27, 10-K）。転換社債（流動負債 $1,596.9M）は株式扱いで負債に含めない。非流動の借入 $40.5M
        net_debt=40.5 - (2043.5 + 694.9),
        rev0=1250.0 * 4,           # FY27 Q1 ガイド中央値の年率
        m0=0.20,                   # OPM 40% × 税後 0.85 − 設備投資 15% ≒ 19%（FY26 実績 FCF マージン 10%）[推測]
        mT=[0.15, 0.25, 0.35],     # 部品サイクル平均 / 高マージン維持 / 不足が恒久化
        wacc=[0.09, 0.10, 0.11],
        ke=0.10, exit_pe=[20, 25, 30],
        unit="FY（6月期）", base_label="FY27 Q1 ガイド年率 $5.0B",
    ),
    "COHR": dict(
        price=337.04,
        shares=202.2,              # FY26 Q4 希薄化後（EX-99.2 [一次]）。基本 1億9,583万株（2026-08-10, 10-K 表紙）
        # 負債 $3,222.2M − 現金 $1,162.0M − 短期投資 $825.0M（2026-06-30, 10-K [一次]）
        net_debt=3222.2 - 1162.0 - 825.0,
        rev0=2300.0 * 4,           # FY27 Q1 ガイド中央値の年率 $9.2B
        m0=0.00,                   # FY26 FCF は −$1.02B（営業CF $80M − 設備投資 $1,103M）。足元 0 と置く [推測]
        mT=[0.08, 0.12, 0.16],     # 産業向けを含む総合フォトニクス。FY25 の FCF マージン約3%、営業 non-GAAP 22% [推測]
        wacc=[0.09, 0.10, 0.11],
        ke=0.10, exit_pe=[20, 25, 30],
        unit="FY（6月期）", base_label="FY27 Q1 ガイド年率 $9.2B",
    ),
    "AAOI": dict(
        price=115.59,
        shares=92.8,               # 2026 Q3 ガイダンスの想定株数（EX-99.1 [一次]）。基本 8,457万株（2026-08-03）。8/21 の $600M ATM の実行分は未反映 ⚠
        # 転換社債 $129.1M ＋ 借入 $58.9M − 現金 $499.7M（2026-06-30, 10-Q [一次]）
        net_debt=129.1 + 58.9 - 499.7,
        rev0=272.5 * 4,            # 2026 Q3 ガイド中央値の年率 $1.09B
        m0=-0.10,                  # 1H26 FCF −$409M（営業CF −$73.8M − 設備投資 $335.1M）÷ 売上 $343M ≒ −119%。立ち上げ期で −10% と置く [推測]
        mT=[0.05, 0.08, 0.12],     # 粗利 30% の組立事業（FN の FCF マージン 0〜6% を参照）[推測]
        wacc=[0.11, 0.12, 0.13],
        ke=0.12, exit_pe=[15, 20, 25],
        unit="暦年", base_label="2026 Q3 ガイド年率 $1.09B",
    ),
}
N, GT = 5, 0.03


def ev_of(g, rev0, m0, mT, wacc):
    pv, fcf = 0.0, 0.0
    for t in range(1, N + 1):
        m = m0 + (mT - m0) * t / N
        fcf = rev0 * (1 + g) ** t * m
        pv += fcf / (1 + wacc) ** t
    return pv + fcf * (1 + GT) / (wacc - GT) / (1 + wacc) ** N


def solve(target, **kw):
    lo, hi = -0.5, 3.0
    if ev_of(hi, **kw) < target:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if ev_of(mid, **kw) < target:
            lo = mid
        else:
            hi = mid
    return mid


for tk, p in INPUTS.items():
    mcap = p["price"] * p["shares"]
    ev = mcap + p["net_debt"]
    print(f"## {tk}（{p['unit']}、百万ドル）")
    print(f"- 株価 ${p['price']:,.2f} × 希薄化後 {p['shares']:.1f}M株 = 時価総額 ${mcap:,.0f}M、純負債 ${p['net_debt']:,.0f}M → EV ${ev:,.0f}M")
    print(f"- 基準売上: {p['base_label']}、FCF マージン {p['m0']:.0%} → 5年目 mT、終端成長 {GT:.0%}")
    print()
    print("| 5年目の FCF マージン ＼ WACC | " + " | ".join(f"{w:.0%}" for w in p["wacc"]) + " |")
    print("|---|" + "---|" * len(p["wacc"]))
    for mT in p["mT"]:
        cells = []
        for w in p["wacc"]:
            g = solve(ev, rev0=p["rev0"], m0=p["m0"], mT=mT, wacc=w)
            cells.append("—" if g is None else f"CAGR {g:+.0%} → 5年目 ${p['rev0'] * (1 + g) ** N / 1000:,.1f}B")
        print(f"| {mT:.0%} | " + " | ".join(cells) + " |")
    print()
    print("出口PER法（N=5年、株主資本コスト {:.0%}）: 必要な5年後の純利益・EPS".format(p["ke"]))
    print()
    print("| 出口PER | 必要な純利益 | 必要な EPS |")
    print("|---|---|---|")
    for pe in p["exit_pe"]:
        ni = mcap * (1 + p["ke"]) ** N / pe
        print(f"| {pe}倍 | ${ni:,.0f}M | ${ni / p['shares']:,.2f} |")
    print()
