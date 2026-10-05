#!/usr/bin/env python3
"""逆算DCF（agent5, R2）: 現在の EV を正当化するのに必要な売上 CAGR を求める。

使い方:
    python3 scripts/reverse_dcf.py            # 全銘柄の基本ケースと感応度表
    python3 scripts/reverse_dcf.py LITE       # 1銘柄だけ

モデル（年次、評価時点 t=0）
- 売上 R_t = R_0 * (1+g)^t  (t=1..N)
- FCF マージン m_t は m_0 から m_T へ N 年で直線的に移る
- 終端価値 TV_N = FCF_N * (1+g_T) / (WACC - g_T)
- EV = Σ FCF_t/(1+WACC)^t + TV_N/(1+WACC)^N を満たす g を二分法で解く
もう1つの見方として「出口PER法」も出す:
- 時価総額 * (1+株主資本コスト)^N = 純利益_N * 出口PER  → 必要な N 年後純利益と、その CAGR

入力値はすべて INPUTS に置き、各値の出典・確度タグをコメントに書く。
入力の確度が [二次]⚠ の場合、結果も ⚠ として扱う（REPORT では補助指標）。
"""
import sys

# ---------------------------------------------------------------------------
# 入力（基準日 2026-10-02 終値、USD/JPY 157.8 は使わず各社の現地通貨で計算）
# ---------------------------------------------------------------------------
INPUTS = {
    "LITE": {
        "name": "Lumentum (USD, 百万ドル)",
        # 株価 $1,085.42 [二次] companiesmarketcap（stocks/LITE.md §4）
        # 基本株式数 88.6M [二次] 10-K 表紙要約。転換社債は株数に入れず負債側で扱う
        "market_cap": 1085.42 * 88.6,
        # 現金 $2.7B [二次]、残存転換社債 約$2.0B [推測: 交換前約$3.2B の 65%]（LITE.md §4）
        "net_debt": 2000.0 - 2700.0,
        # 基準売上: FY26 実績 $3,010M [二次]。もう1案は Q1 FY27 ガイダンス中央値の年率 $5,000M [推測]
        "revenue0": {"FY26実績": 3010.0, "Q1FY27ガイド年率": 5000.0},
        # FCF マージン: 足元 ≒ non-GAAP 営業利益率 36.6〜40% × (1-税15%) − 設備投資等 ≒ 25% [推測]
        "fcf_margin0": 0.25,
        # 終端 FCF マージン: 15%=部品サイクル平均（過去の LITE は 10〜20% 程度 [推測]）、25%=現状維持、35%=供給制約が恒久化
        "fcf_margin_T": [0.15, 0.25, 0.35],
        "wacc": [0.09, 0.10, 0.11],
        "g_T": 0.03,
        "years": 5,
        # 出口PER法: 株主資本コスト 10%、出口PER 20/25/30倍
        # 参照純利益: FY26 non-GAAP $782M [二次]、Q1 FY27 ガイド EPS 中央値 $4.20×4×希薄化後約1.01億株 ≒ $1,700M [推測]
        "cost_of_equity": 0.10,
        "exit_pe": [20, 25, 30],
        "ni0": {"FY26 non-GAAP": 782.3, "Q1FY27ガイド年率": 1700.0},
        # 比較する業界成長率: 光モジュール市場 2025-31 CAGR 20%超 [二次]⚠ LightCounting 要約（notes/agent1.md §3）
        "industry_cagr": 0.20,
    },
    "5803": {
        "name": "フジクラ (JPY, 億円)",
        # 株価 5,598円 [二次]。株数は 27/3期予想純利益 3,260億円 ÷ EPS 196.88円 ≒ 16.56億株 [推測: 逆算]
        # （カードの「9.9兆円」は発行済約17.7億株ベースと推測。自己株の扱いが未確認 ⚠）
        "market_cap": 5598 * 3260 / 196.88,
        # 純有利子負債 ⚠未取得 → 0 と置く [推測]
        "net_debt": 0.0,
        # 基準売上: 26/3期実績 11,824億円 [二次]。もう1案は 27/3期 1Q 4,020億円×4 [推測]
        "revenue0": {"26/3期実績": 11824.0, "27/3期1Q年率": 16080.0},
        # FCF マージン: 27/3期予想 営業利益率 ≒ 4,320/16,080 = 27% [推測] → 税後 19%、増産投資（最大3,000億円/数年）で ≒ 12% [推測]
        "fcf_margin0": 0.12,
        # 終端 FCF マージン: 電線・ケーブル業界の平常時は 5〜8% 程度 [推測]。光の構造変化で上振れケースも置く
        "fcf_margin_T": [0.08, 0.12, 0.16],
        "wacc": [0.07, 0.08, 0.09],
        "g_T": 0.015,
        "years": 5,
        # 出口PER法: 株主資本コスト 8%、出口PER 15/20/25倍。参照純利益 27/3期会社予想 3,260億円 [二次]
        "cost_of_equity": 0.08,
        "exit_pe": [15, 20, 25],
        "ni0": {"27/3期会社予想": 3260.0},
        # 比較: 中計 FY2028(28/3期) 売上 1.6兆円 → 26/3期比 CAGR 約16.3%（2年） [二次]⚠ 中計要約
        "industry_cagr": (16000 / 11824) ** 0.5 - 1,
    },
}


def ev_from_growth(g, r0, m0, mT, wacc, gT, n):
    pv = 0.0
    rev = r0
    fcf = 0.0
    for t in range(1, n + 1):
        rev *= 1 + g
        m = m0 + (mT - m0) * t / n
        fcf = rev * m
        pv += fcf / (1 + wacc) ** t
    tv = fcf * (1 + gT) / (wacc - gT)
    return pv + tv / (1 + wacc) ** n


def implied_growth(ev, r0, m0, mT, wacc, gT, n, lo=-0.5, hi=5.0):
    f = lambda g: ev_from_growth(g, r0, m0, mT, wacc, gT, n) - ev
    if f(lo) > 0:
        return lo
    if f(hi) < 0:
        return float("inf")
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def exit_pe_required(mcap, ke, n, pe, ni0):
    ni_n = mcap * (1 + ke) ** n / pe
    return ni_n, (ni_n / ni0) ** (1 / n) - 1


def run(tk):
    p = INPUTS[tk]
    ev = p["market_cap"] + p["net_debt"]
    n = p["years"]
    print(f"## {tk} {p['name']}")
    print(f"- 時価総額 {p['market_cap']:,.0f} / 純負債 {p['net_debt']:,.0f} / EV {ev:,.0f}")
    print(f"- 比較する成長率（業界・会社目標） {p['industry_cagr']:.1%}")
    for label, r0 in p["revenue0"].items():
        print(f"\n### 基準売上 {label} = {r0:,.0f}（{n}年、FCFマージン {p['fcf_margin0']:.0%}→終端、g_T {p['g_T']:.1%}）")
        print("| WACC \\ 終端FCFマージン | " + " | ".join(f"{m:.0%}" for m in p["fcf_margin_T"]) + " |")
        print("|---" * (len(p["fcf_margin_T"]) + 1) + "|")
        for w in p["wacc"]:
            cells = []
            for mT in p["fcf_margin_T"]:
                g = implied_growth(ev, r0, p["fcf_margin0"], mT, w, p["g_T"], n)
                rn = r0 * (1 + g) ** n
                cells.append(f"{g:.1%}（{n}年後売上 {rn:,.0f}）")
            print(f"| {w:.0%} | " + " | ".join(cells) + " |")
    labels = list(p["ni0"])
    print(f"\n### 出口PER法（株主資本コスト {p['cost_of_equity']:.0%}、{n}年後）")
    print("| 出口PER | 必要な純利益 | " + " | ".join(f"必要CAGR（基準 {k} {v:,.0f}）" for k, v in p["ni0"].items()) + " |")
    print("|---" * (len(labels) + 2) + "|")
    for pe in p["exit_pe"]:
        cells = []
        for k in labels:
            ni_n, c = exit_pe_required(p["market_cap"], p["cost_of_equity"], n, pe, p["ni0"][k])
            cells.append(f"{c:.1%}")
        print(f"| {pe}倍 | {ni_n:,.0f} | " + " | ".join(cells) + " |")
    print()


if __name__ == "__main__":
    for tk in sys.argv[1:] or INPUTS:
        run(tk)
