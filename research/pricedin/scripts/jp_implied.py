#!/usr/bin/env python3
"""日本3社の「株価が要求する水準」（agent1, R3）

3つの見方で、基準日 2026-10-02 の株価が何を前提にしているかを出す。単位: 億円。
 (1) 逆算DCF: research/photonics/scripts/reverse_dcf.py の関数を流用。EV を正当化する5年の売上CAGR
 (2) 出口PER法: 5年後（FY32 = 2032/3期）に必要な純利益 = 時価総額 × (1+ke)^5 ÷ 出口PER
 (3) 永続成長率: 今期予想純益が全額配分可能で永続的に g で伸びるとき 時価総額 = NI×(1+g)/(ke−g) を満たす g。
     「今期の利益がそのまま永続」（g=0）での価値も併記（持続年数法は 3社とも g=0 永続でも届かず不採用）
 (4) EV/営業利益と、住友電工の SOTP（光以外に倍率を当てた残りが光事業の評価）
入力の出典は stocks/<code>.md の B（[一次]）と C（[二次]）。前提の値（WACC・マージン・PER）は [推測]。

使い方: python3 research/pricedin/scripts/jp_implied.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "photonics", "scripts"))
from reverse_dcf import implied_growth  # noqa: E402

INPUTS = {
    "5803 フジクラ": {
        # 5,598円 × 16.557億株（FY26末 発行済−自己株）[一次: 短信]
        "mcap": 5598 * 16.557,
        # FY27 1Q末: 有利子負債(短借457+CP200+社債200+長借303) − 現預金1,923 = −763（純現金）[一次]
        "net_debt": -763,
        "rev0": 17550, "ni_peak": 3260,              # FY27 会社予想 08-07 [一次]
        "fcf_m0": 0.12, "fcf_mT": [0.10, 0.15, 0.20],  # FY26 FCF/売上 7.9% [一次]、純益率 18.6% − 増強投資 [推測]
        "wacc": [0.08, 0.09, 0.10], "gT": 0.02, "ke": 0.09,
        # 正常水準の候補（純益は FY27 予想の 純益/営業 = 0.755 で換算 [推測]）
        "norms": {
            "28中計 FY29 営業3,150": 3150 * 0.755,
            "中計参考値 FY31 営業3,800": 3800 * 0.755,
            "FY26 実績 純益1,572": 1572,
        },
        "pe_norm": [15, 20],
        "exit_pe": [15, 20, 25],
        "ops": {"FY27 会社予想 営業": 4320, "28中計 FY29 営業": 3150, "中計参考値 FY31 営業": 3800},
        "refs": {"FY27 会社予想": 3260, "中計 FY29（換算）": 2378, "中計参考値 FY36 営業5,800（換算）": 5800 * 0.755},
    },
    "6834 精工技研": {
        "mcap": 6850 * 0.44696,        # 自己株除く 8,939,271×5 株 [一次]
        "net_debt": -180,              # FY26末 現預金 180億、有利子負債ほぼなし [一次: 説明資料]
        "rev0": 410, "ni_peak": 92,    # FY27 会社予想 08-10 [一次]
        "fcf_m0": 0.15, "fcf_mT": [0.10, 0.15, 0.20],  # FY26 FCF/売上 15% [一次]
        "wacc": [0.08, 0.09, 0.10], "gT": 0.015, "ke": 0.09,
        "norms": {
            "FY26 実績 純益62": 62,
            "FY25 実績 純益22（ブーム前）": 22,
            "FY27 期初予想 純益64": 64,
        },
        "pe_norm": [15, 20],
        "exit_pe": [15, 20, 25],
        "ops": {"FY27 会社予想 営業": 120, "FY26 実績 営業": 77.3},
        "refs": {"FY27 会社予想": 92, "コンセンサス FY27": 96},
    },
    "5802 住友電工": {
        "mcap": 2452 * 31.1968,        # 自己株除く 3,119.68百万株 [一次: 1Q 短信]
        # 1Q末 有利子負債 7,376（短借3,284+CP639+1年内社債450+社債1,299+長借1,704）− 現預金2,647 ＋ 非支配持分 927 [一次]
        "net_debt": 7376 - 2647 + 927,
        "rev0": 54000, "ni_peak": 3400,  # FY27 会社予想 07-31 [一次]
        "fcf_m0": 0.04, "fcf_mT": [0.03, 0.04, 0.05],  # FY26 FCF 2,030/51,102 = 4.0% [一次]
        "wacc": [0.07, 0.08, 0.09], "gT": 0.015, "ke": 0.08,
        "norms": {
            "FY25 実績 純益1,938": 1938,
            "FY26 実績（売却益除く 約2,995）": 3695 - 700,
        },
        "pe_norm": [12, 15],
        "exit_pe": [12, 15, 18],
        "ops": {"FY27 会社予想 営業": 4500, "中計 FY29 営業": 6000},
        # 情報通信の FY27 営業利益は 1Q 272.5×4 ≈ 1,090 [推測: 年率換算]、FY29 は中計の約2,400 [二次]
        "sotp": {"non_op": 4500 - 1090, "mults": [8, 10, 12, 14],
                 "opt_ops": {"FY27 1Q年率 1,090": 1090, "FY29 中計 約2,400": 2400}},
        "refs": {"FY27 会社予想": 3400, "コンセンサス FY27": 3619, "中計 FY29 営業6,000（純益換算 ×0.756）": 6000 * 0.756},
    },
}


def years_needed(mcap, ni_peak, ni_norm, pe_norm, ke, kmax=60):
    """持続年数法の k（連続値を線形補間）"""
    def val(k):
        pv = sum(ni_peak / (1 + ke) ** t for t in range(1, k + 1))
        return pv + ni_norm * pe_norm / (1 + ke) ** k
    if val(0) >= mcap:
        return 0.0
    prev = val(0)
    for k in range(1, kmax + 1):
        v = val(k)
        if v >= mcap:
            return k - 1 + (mcap - prev) / (v - prev)
        if v <= prev:   # 頭打ち（peak 永続でも届かない）
            return float("inf")
        prev = v
    return float("inf")


def run(name, p):
    ev = p["mcap"] + p["net_debt"]
    print(f"## {name}")
    print(f"- 時価総額 {p['mcap']:,.0f} / 純負債(+非支配) {p['net_debt']:,.0f} / EV {ev:,.0f}"
          f" / PER(会社予想) {p['mcap']/p['ni_peak']:.1f}倍\n")
    print(f"### (1) 逆算DCF: 必要な5年売上CAGR（基準 FY27 予想売上 {p['rev0']:,}、FCFマージン {p['fcf_m0']:.0%}→終端、g_T {p['gT']:.1%}）")
    print("| WACC \\ 終端FCFマージン | " + " | ".join(f"{m:.0%}" for m in p["fcf_mT"]) + " |")
    print("|---" * (len(p["fcf_mT"]) + 1) + "|")
    for w in p["wacc"]:
        cells = []
        for mT in p["fcf_mT"]:
            g = implied_growth(ev, p["rev0"], p["fcf_m0"], mT, w, p["gT"], 5)
            cells.append(f"{g:+.1%}（FY32 売上 {p['rev0']*(1+g)**5:,.0f}）")
        print(f"| {w:.0%} | " + " | ".join(cells) + " |")
    print(f"\n### (2) 出口PER法（ke {p['ke']:.0%}、FY32 に必要な純利益）")
    print("| 出口PER | 必要な純利益 | " + " | ".join(f"{k} {v:,.0f} 比" for k, v in p["refs"].items()) + " |")
    print("|---" * (len(p["refs"]) + 2) + "|")
    for pe in p["exit_pe"]:
        ni = p["mcap"] * (1 + p["ke"]) ** 5 / pe
        print(f"| {pe}倍 | {ni:,.0f} | " + " | ".join(f"{ni/v:.2f}倍" for v in p["refs"].values()) + " |")
    g = (p["ke"] * p["mcap"] - p["ni_peak"]) / (p["mcap"] + p["ni_peak"])
    print(f"\n### (3) 永続成長率: 今期予想純益 {p['ni_peak']:,} から永続的に年 **{g:.1%}** 伸びる前提（ke {p['ke']:.0%}）。"
          f"g=0 で永続した場合の価値は {p['ni_peak']/p['ke']:,.0f}（時価総額の {p['ni_peak']/p['ke']/p['mcap']:.0%}）")
    print(f"\n### (4) EV/営業利益")
    for lab, op in p["ops"].items():
        print(f"- {lab} {op:,.0f} → {ev/op:.1f}倍")
    if "sotp" in p:
        s = p["sotp"]
        print(f"\n#### SOTP: 光以外の営業利益 {s['non_op']:,.0f} に EV/営業利益 m を当て、残りを光（情報通信）の評価とみなす")
        print("| 光以外の倍率 m | 光以外の価値 | 光の含意EV | 光の含意EV ÷ " + " | ÷ ".join(s["opt_ops"]) + " |")
        print("|---" * (len(s["opt_ops"]) + 3) + "|")
        for m in s["mults"]:
            nv = s["non_op"] * m
            ov = ev - nv
            print(f"| {m}倍 | {nv:,.0f} | {ov:,.0f} | " + " | ".join(f"{ov/v:.1f}倍" for v in s["opt_ops"].values()) + " |")
    print()


if __name__ == "__main__":
    for name, p in INPUTS.items():
        run(name, p)
