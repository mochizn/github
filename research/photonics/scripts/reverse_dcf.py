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
        # R3: agent4 ✘(L11) を反映。イン・ザ・マネーの転換社債は株式とみなし、希薄化後 約1.01億株で時価を計算
        # 株価 $1,085.42 ✔（agent4 L6）。希薄化後株数 1.01億 [推測: non-GAAP NI $326.3M ÷ EPS $3.23]
        "market_cap": 1085.42 * 101.0,
        # 転換社債を株式扱いにしたので、純負債 = −現金 $2.7B [二次]（stocks/LITE.md §0）
        "net_debt": -2700.0,
        # 基準売上: FY26 実績 $3,014M ✔（agent4 L2）。Q1 FY27 ガイダンス中央値 $1,250M ✔(L3) ×4 [推測: 年率換算]
        "revenue0": {"FY26実績": 3014.0, "Q1FY27ガイド年率": 5000.0},
        # FCF マージン: FY26 実績 10%（FCF $300M / 売上 $3.0B [二次]）。ガイドの営業利益率 40% × 税後 0.85 − 設備投資 15% ≒ 19% [推測] → 20%
        "fcf_margin0": 0.20,
        # 終端 FCF マージン: 15%=部品サイクル平均 [推測]、25%=高マージン維持、35%=供給制約が恒久化
        "fcf_margin_T": [0.15, 0.25, 0.35],
        "wacc": [0.09, 0.10, 0.11],
        "g_T": 0.03,
        "years": 5,
        "mid_ni": "Q1FY27ガイド年率",
        "mid": ("Q1FY27ガイド年率", 0.10, 0.25),
        # 出口PER法: 参照純利益 FY26 non-GAAP $782M ✔(L2)、Q1 ガイド年率 $4.20×4×1.01億株 ≒ $1,700M [推測]
        "cost_of_equity": 0.10,
        "exit_pe": [20, 25, 30],
        "ni0": {"FY26 non-GAAP": 782.3, "Q1FY27ガイド年率": 1700.0},
        # 比較: 光モジュール市場 2025-31 CAGR 20%超 [二次]⚠ LightCounting 要約（notes/agent1.md §3）
        "industry_cagr": 0.20,
        "industry_label": "光モジュール市場 2025-31",
    },
    "COHR": {
        "name": "Coherent (USD, 百万ドル)",
        # 株価 $315（2026-10-01 終値、基準日の前日 ⚠）[二次] notes/agent3.md。株数 1.95億（2026-06-30）[二次]⚠ macrotrends 要約
        "market_cap": 315.0 * 195.0,
        # 総債務 $3,222M − 現金 $1,162M − 短期投資 $825M（2026-06-30）[二次] 8-K EX-99.1 要約（WebSearch, 2026-10-05）
        "net_debt": 3222.0 - 1162.0 - 825.0,
        # 基準売上: FY26 実績 $7,120M [二次]（notes/agent3.md）。Q1 FY27 ガイド $2.2〜2.4B の中央値 ×4 [推測]
        "revenue0": {"FY26実績": 7120.0, "Q1FY27ガイド年率": 9200.0},
        # FCF マージン: 足元は設備投資 $1.1B でマイナス [二次]⚠ 単一ソース。non-GAAP GM 40.2% → 営業 20% 前後 [推測] → 足元 5%
        "fcf_margin0": 0.05,
        "fcf_margin_T": [0.08, 0.12, 0.16],
        "wacc": [0.09, 0.10, 0.11],
        "g_T": 0.03,
        "years": 5,
        "mid_ni": "Q4FY26 non-GAAP年率",
        "mid": ("Q1FY27ガイド年率", 0.10, 0.12),
        # 参照純利益: Q4 FY26 non-GAAP EPS $1.74 ×4 ×1.95億株 ≒ $1,360M [推測]
        "cost_of_equity": 0.10,
        "exit_pe": [20, 25, 30],
        "ni0": {"Q4FY26 non-GAAP年率": 1360.0},
        "industry_cagr": 0.20,
        "industry_label": "光モジュール市場 2025-31",
    },
    "AAOI": {
        "name": "Applied Optoelectronics (USD, 百万ドル)",
        # 株価 $115.59（2026-10-02）[二次]、株数 84.9M（2026-08-20, 424B5）→ 時価 $9.81B ✔（内部整合, stocks/AAOI.md §0）。ATM 実行分は未反映 ⚠
        "market_cap": 115.59 * 84.906,
        # 純現金 約$375M（現金 $499.7M − 転換社債 $124.9M）[二次]。転換社債はイン・ザ・マネーだが小さいので負債扱いのまま
        "net_debt": -375.0,
        # 基準売上: 2026年会社見通し 約$1.1B [二次]⚠、2027年コンセンサス $2.66B [二次]
        "revenue0": {"2026年見通し": 1100.0, "2027年コンセンサス": 2660.0},
        # FCF マージン: 足元マイナス（設備投資先行・ATM 調達）[推測] → 0%。non-GAAP GM 29〜30.5% の組立事業
        "fcf_margin0": 0.0,
        "fcf_margin_T": [0.05, 0.08, 0.12],
        "wacc": [0.11, 0.12, 0.13],
        "g_T": 0.03,
        "years": 5,
        "mid_ni": "2027年コンセンサス",
        "mid": ("2026年見通し", 0.12, 0.08),
        # 参照純利益: 2027年コンセンサス EPS $4.60 × 約0.88億株 ≒ $400M [推測]
        "cost_of_equity": 0.12,
        "exit_pe": [15, 20, 25],
        "ni0": {"2027年コンセンサス": 400.0},
        "industry_cagr": 0.20,
        "industry_label": "光モジュール市場 2025-31",
    },
    "5803": {
        "name": "フジクラ (JPY, 億円)",
        # 株価 5,598円 ✔。株数は自己株除く 16.588億株 ✔（agent4 V8・V13: 発行済 1,775,180,526 − 自己株 116,394,761）
        "market_cap": 5598 * 16.588,
        # ネットキャッシュ 約+1,160億円 [二次]（stocks/5803.md §8-2）
        "net_debt": -1160.0,
        # 基準売上: 26/3期実績 11,824億円 ✔(V1)、27/3期 会社予想 17,550億円（agent4 V7 追加情報）
        "revenue0": {"26/3期実績": 11824.0, "27/3期会社予想": 17550.0},
        # FCF マージン: 26/3期の単純FCF 967億円 / 売上 = 8.2% [二次]。27/3期は営業 4,320/17,550 = 24.6% → 税後 17%、増産投資で ≒ 12% [推測]
        "fcf_margin0": 0.12,
        # 終端: 8%=電線業の平常 [推測]、12%=足元維持、16%=光の構造変化で上振れ
        "fcf_margin_T": [0.08, 0.12, 0.16],
        "wacc": [0.07, 0.08, 0.09],
        "g_T": 0.015,
        "years": 5,
        "mid_ni": "27/3期会社予想",
        "mid": ("27/3期会社予想", 0.08, 0.12),
        "cost_of_equity": 0.08,
        "exit_pe": [15, 20, 25],
        "ni0": {"27/3期会社予想": 3260.0},
        # 比較: 中計 FY2028(28/3期) 売上 1.6兆円 ✔(V10) → 26/3期比 CAGR 16.3%（2年）
        "industry_cagr": (16000 / 11824) ** 0.5 - 1,
        "industry_label": "中計 28/3期 売上1.6兆円",
    },
    "6834": {
        "name": "精工技研 (JPY, 億円)",
        # 株価 6,850円（2026-10-02）[二次]、自己株除く 約4,470万株 [二次]（stocks/6834.md §3）→ 約3,062億円
        "market_cap": 6850 * 0.4470,
        # 純現金 ⚠未取得 → 0 と置く [推測]（無借金に近いと推測されるが未確認）
        "net_debt": 0.0,
        # 基準売上: 26/3期実績 300.9億円 [二次]（agent4 参考メモ）、27/3期会社予想 410億円 [二次]
        "revenue0": {"26/3期実績": 300.9, "27/3期会社予想": 410.0},
        # FCF マージン: 27/3期予想 純利益 92/410 = 22% [推測] → 設備投資を引いて 15%
        "fcf_margin0": 0.15,
        # 終端: 8%=過去の平常期 [推測]、12%、16%=高付加価値品への転換が続く
        "fcf_margin_T": [0.08, 0.12, 0.16],
        "wacc": [0.08, 0.09, 0.10],
        "g_T": 0.015,
        "years": 5,
        "mid_ni": "27/3期会社予想",
        "mid": ("27/3期会社予想", 0.09, 0.12),
        "cost_of_equity": 0.09,
        "exit_pe": [15, 20, 25],
        "ni0": {"27/3期会社予想": 92.0},
        # 比較: 個別の市場予測が無いので光モジュール市場 20% で代用 [推測]⚠
        "industry_cagr": 0.20,
        "industry_label": "光モジュール市場で代用",
    },
}


def v_score(gap):
    """V 軸の採点（notes/agent5.md R2 で決定）: 含意CAGR − 比較成長率 の差（pt）"""
    if gap <= 0:
        return 5
    if gap <= 0.05:
        return 4
    if gap <= 0.15:
        return 3
    if gap <= 0.25:
        return 2
    return 1


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


def summary(tks):
    print("## まとめ（中央ケース）")
    print("V = (DCF法の点 + 出口PER法の点) / 2 を切り上げ。出口PER法は中央の出口PER・参照純利益から必要な純利益CAGRを出し、同じ比較成長率との差で採点")
    print("| 銘柄 | EV | 基準売上 | WACC | 終端FCFマージン | 含意売上CAGR | 比較成長率 | 差 | V(DCF) | 必要純利益CAGR（出口PER） | 差 | V(PER) | V |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for tk in tks:
        p = INPUTS[tk]
        ev = p["market_cap"] + p["net_debt"]
        label, w, mT = p["mid"]
        g = implied_growth(ev, p["revenue0"][label], p["fcf_margin0"], mT, w, p["g_T"], p["years"])
        gap = g - p["industry_cagr"]
        pe = p["exit_pe"][len(p["exit_pe"]) // 2]
        _, c = exit_pe_required(p["market_cap"], p["cost_of_equity"], p["years"], pe, p["ni0"][p["mid_ni"]])
        gap2 = c - p["industry_cagr"]
        v1, v2 = v_score(gap), v_score(gap2)
        v = -(-(v1 + v2) // 2)
        print(f"| {tk} | {ev:,.0f} | {label} {p['revenue0'][label]:,.0f} | {w:.0%} | {mT:.0%} | {g:.1%} | "
              f"{p['industry_cagr']:.1%}（{p['industry_label']}） | {gap*100:+.1f}pt | {v1} | "
              f"{c:.1%}（{pe}倍, {p['mid_ni']}） | {gap2*100:+.1f}pt | {v2} | **{v}** |")
    print()


if __name__ == "__main__":
    tks = sys.argv[1:] or list(INPUTS)
    summary(tks)
    for tk in tks:
        run(tk)
