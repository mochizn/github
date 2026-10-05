#!/usr/bin/env python3
"""GLW・FN の逆算（agent3, R3）。research/photonics/scripts/reverse_dcf.py と同じモデル。

使い方: python3 scripts/reverse_dcf_glw_fn.py  → data/reverse_dcf_glw_fn.md

モデル（年次、t=0 は基準日 2026-10-02）
- DCF: 売上 R_t = R_0(1+g)^t、FCF マージンは m_0 → m_T へ N 年で直線的に移る。
  終端価値 TV = FCF_N(1+g_T)/(WACC−g_T)。EV と一致する g を二分法で解く（＝株価が要求する売上 CAGR）
- 出口PER: 時価総額 ×(1+株主資本コスト)^N = 純利益_N × 出口PER → 必要な N 年後純利益と CAGR
入力の出典はコメント。確度: 株価・株数・純負債・実績は [一次]、予想は [二次]、マージン・WACC・倍率は [推測]
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "reverse_dcf_glw_fn.md")

INPUTS = {
    "GLW": dict(
        name="Corning（百万ドル、暦年）",
        # $164.19 × 希薄化後 8.644億株（8.614億株 10-Q 表紙 2026-07-24 ＋ NVIDIA プレファンド300万株）[一次]
        market_cap=164.19 * 864.4,
        # 長期債務 7,756 ＋ 1年内 668 − 現金 2,504（2026-06-30, Q2 10-Q）[一次]
        net_debt=7756 + 668 - 2504,
        # R0: 2026年コンセンサス コア売上 $19.28B [二次 StockAnalysis]／Q3'26 ガイダンス中央値 $4.95B×4 [一次＋推測]
        revenue0={"2026年コンセンサス": 19280.0, "Q3'26ガイド年率": 19800.0},
        # FCF マージン: 2025年 調整後FCF $1.72B ÷ コア売上 $16.41B = 10.5% [一次]。2026年は設備投資 $2.0B で 約10% [推測]
        fcf_margin0=0.10,
        # 終端: 10%=現状維持、14%=会社の「FCF は大幅に増える」、18%=光の高収益が恒久化 [推測]
        fcf_margin_T=[0.10, 0.14, 0.18],
        wacc=[0.08, 0.09, 0.10],
        g_T=0.03, years=5,
        # 出口PER: 2026年コンセンサス EPS $3.28 × 8.644億株 = $2,835M [二次]
        cost_of_equity=0.09, exit_pe=[20, 25, 30],
        ni0={"2026年コンセンサス": 3.28 * 864.4},
        # 比較対象
        refs=[
            ("会社 Springboard（社内計画）", "年率売上 2026年末 $20B → 2028年末 $30B → 2030年末 $40B（Q4'26→Q4'30 CAGR 19%）", "[一次] 2026-07-28 8-K"),
            ("アナリスト", "2026年 売上 $19.28B・EPS $3.28、2027年 EPS $4.31〜4.36、BofA 2028年 EPS $6.50", "[二次]"),
        ],
    ),
    "FN": dict(
        name="Fabrinet（百万ドル、6月決算）",
        # $463.69 × 希薄化後 3,630万株（Q1 FY27 ガイダンスの前提）[一次]
        market_cap=463.69 * 36.3,
        # 現金 347 ＋ 短期投資 528（2026-06-26, 10-K）− THB 25億タームローン 約75（2026-08）[一次]
        net_debt=-(347 + 528 - 75),
        # R0: FY26 実績 $4,641M [一次]／FY27 コンセンサス $6,100M [二次 StockAnalysis]
        revenue0={"FY26実績": 4641.0, "FY27コンセンサス": 6100.0},
        # FCF マージン: FY25 6.1%（$207M）、FY26 0.1%（$4M）[一次] → 足元 3% [推測]
        fcf_margin0=0.03,
        # 終端: 4%=設備投資が続く、6%=FY25 並み、8%=EMS の好調期 [推測]
        fcf_margin_T=[0.04, 0.06, 0.08],
        wacc=[0.09, 0.10, 0.11],
        g_T=0.03, years=5,
        # 出口PER: FY27 コンセンサス EPS $18.20 × 3,630万株 = $661M [二次]。Pillar Two（$1.60/株）を費用とみると $603M [推測]
        cost_of_equity=0.10, exit_pe=[15, 20, 25],
        ni0={"FY27コンセンサス": 18.20 * 36.3, "FY27 Pillar Two 控除後": 16.60 * 36.3},
        refs=[
            ("会社", "四半期ガイダンスのみ（Q1 FY27 売上 $1.375〜1.425B、非GAAP EPS $4.10〜4.25）。中期計画なし", "[一次] 2026-08-17 8-K"),
            ("アナリスト", "FY27 売上 $6.10B（+31.5%）・EPS $18.20（+29%）、目標株価 平均 $650〜734", "[二次]"),
        ],
    ),
}


def ev_at(g, R0, m0, mT, wacc, gT, N):
    ev, fcf = 0.0, 0.0
    for t in range(1, N + 1):
        m = m0 + (mT - m0) * t / N
        fcf = R0 * (1 + g) ** t * m
        ev += fcf / (1 + wacc) ** t
    return ev + fcf * (1 + gT) / (wacc - gT) / (1 + wacc) ** N


def solve(target, *a):
    lo, hi = -0.5, 1.5
    for _ in range(200):
        mid = (lo + hi) / 2
        if ev_at(mid, *a) < target:
            lo = mid
        else:
            hi = mid
    return mid


def main():
    L = ["# 逆算DCF・出口PER（GLW・FN、基準日 2026-10-02）", "",
         "再現: `python3 scripts/reverse_dcf_glw_fn.py`。モデルは research/photonics/scripts/reverse_dcf.py と同じ。入力の出典はスクリプトのコメント。",
         "結果は [推測]（入力の株価・株数・純負債は [一次]、予想は [二次]、マージン・WACC・倍率は仮定）。", ""]
    for t, p in INPUTS.items():
        ev = p["market_cap"] + p["net_debt"]
        L += [f"## {t} {p['name']}", "",
              f"時価総額 ${p['market_cap']:,.0f}M、純負債 ${p['net_debt']:,.0f}M、EV ${ev:,.0f}M。期間 {p['years']}年、終端成長 {p['g_T']:.0%}、足元 FCF マージン {p['fcf_margin0']:.0%}。", ""]
        for lbl, R0 in p["revenue0"].items():
            L += [f"### DCF: 基準売上 = {lbl} ${R0:,.0f}M → 株価が要求する売上 CAGR（{p['years']}年）と {p['years']}年後の売上", "",
                  "| 終端FCFマージン ＼ WACC | " + " | ".join(f"{w:.0%}" for w in p["wacc"]) + " |", "|---|" + "---|" * len(p["wacc"])]
            for mT in p["fcf_margin_T"]:
                cells = []
                for w in p["wacc"]:
                    g = solve(ev, R0, p["fcf_margin0"], mT, w, p["g_T"], p["years"])
                    cells.append(f"{g:+.1%}（${R0*(1+g)**p['years']/1000:,.1f}B）")
                L.append(f"| {mT:.0%} | " + " | ".join(cells) + " |")
            L.append("")
        N, ke = p["years"], p["cost_of_equity"]
        need = p["market_cap"] * (1 + ke) ** N
        L += [f"### 出口PER: {N}年後に必要な純利益（株主資本コスト {ke:.0%}）", "",
              "| 出口PER | 必要な純利益 | " + " | ".join(f"{k} からの CAGR" for k in p["ni0"]) + " |", "|---|---|" + "---|" * len(p["ni0"])]
        for pe in p["exit_pe"]:
            ni = need / pe
            L.append(f"| {pe}倍 | ${ni:,.0f}M | " + " | ".join(f"{(ni/v)**(1/N)-1:+.1%}" for v in p["ni0"].values()) + " |")
        L += ["", "比較: " + "；".join(f"{a}: {b} {c}" for a, b, c in p["refs"]), ""]
    with open(OUT, "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
