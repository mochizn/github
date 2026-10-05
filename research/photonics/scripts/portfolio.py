#!/usr/bin/env python3
"""6軸採点 → 3パターンの目標比率と「今日の投入比率」（agent5, R4 暫定版）。

使い方: python3 scripts/portfolio.py

ルール（notes/agent5.md「評価軸の定義」、R3・R4 の決定）
- 確信度 = 0.20E + 0.20R + 0.15M + 0.25V + 0.20K
- 補正（R3）: ✔ の無い軸は 3 点超なら 3 点に下げ、3 点未満はそのまま
  （R4）R は agent1 の判断による採点なので、agent1 が採点した銘柄は ✔ 扱い。K は agent4 の採点を ✔ 扱い
- 組み入れ: 補正後確信度 ≥ 3.0。積極パターンだけ、群A（純度の高い群）で 2.5 以上 3.0 未満の銘柄を投機枠（1銘柄 3%、合計 5% 以内）
- 目標比率: 素の比率 = 上限 × (確信度−2.5)/(最高確信度−2.5)。これに共通の倍率 k を掛け、
  上限で切りながら銘柄合計がパターンの銘柄枠（保守70/標準87.5/積極90%）に届くまで k を上げる（R4）。
  各銘柄の天井は 上限 × clip((確信度−2.5)/(最高−2.5), 0.5, 1)。確信度の低い銘柄が上限まで膨らまないようにするため
  上限ですべて頭打ちになったら残りは現金
  × 下値リスク調整（R4）: 対象群の弱気下落率の中央値 ÷ その銘柄の弱気下落率（0.7〜1.2 に制限）
  90日ボラが揃うまでの代用。弱気下落率が無い銘柄は 1.0
- 上限: 1銘柄（保守10/標準12/積極15%）、小型株 L≤2（3/5/8%）、K≤2 は保守・標準で上限の半分
- 同一ファクター上限（R4）: 「AI-DC 光の純度が高い群」(E≥4) の合計を 保守25/標準40/積極60% に制限。
  超えたら群内を比例で縮める。どの銘柄も米ハイパースケーラの設備投資で動くため
- 今日の投入（R4）: 価格の位置で目標比率のどれだけを持つかを決める（REPORT §4.3 のシナリオ値）
    株価 > 中立値                     → 0
    確率加重値 < 株価 ≤ 中立値         → 1/3
    確率加重値×0.85 < 株価 ≤ 確率加重値 → 2/3
    株価 ≤ 確率加重値×0.85            → 全部
  シナリオ値が未計算の銘柄は 0（計算するまで買わない）
"""

W = {"E": 0.20, "R": 0.20, "M": 0.15, "V": 0.25, "K": 0.20}

# 素点, ✔ の軸, 弱気下落率(正の%、agent4 §4/§6 の中央値。無ければ None), 群A(E≥4 の純度が高い群)か
# 素点の理由は notes/agent5.md「R4: 採点 v3」
SCORES = {
    "5803": ({"E": 4, "R": 4, "M": 5, "V": 4, "K": 3, "L": 5}, {"E", "R", "M", "V", "K", "L"}, 55, True),
    "LITE": ({"E": 5, "R": 4, "M": 5, "V": 2, "K": 2, "L": 5}, {"E", "R", "M", "V", "K", "L"}, 67, True),
    "6834": ({"E": 4, "R": 4, "M": 5, "V": 3, "K": 2, "L": 2}, {"E", "R", "M", "V", "K", "L"}, 59, True),
    "COHR": ({"E": 4, "R": 3, "M": 4, "V": 3, "K": 3, "L": 5}, {"R", "L"}, None, True),
    "FN":   ({"E": 4, "R": 3, "M": 5, "V": 4, "K": 3, "L": 3}, {"R"}, None, True),
    "6777": ({"E": 4, "R": 5, "M": 3, "V": 3, "K": 3, "L": 2}, {"R"}, None, True),
    "GLW":  ({"E": 3, "R": 5, "M": 4, "V": 3, "K": 4, "L": 5}, {"R"}, None, False),
    "AVGO": ({"E": 2, "R": 5, "M": 3, "V": 3, "K": 4, "L": 5}, {"R"}, None, False),
    "5802": ({"E": 2, "R": 4, "M": 4, "V": 3, "K": 4, "L": 5}, {"R"}, None, False),
    "AAOI": ({"E": 4, "R": 2, "M": 4, "V": 3, "K": 1, "L": 3}, {"E", "R", "M", "K"}, 60, True),
    "5801": ({"E": 2, "R": 4, "M": 3, "V": 2, "K": 3, "L": 5}, {"R", "K"}, 55, False),
    "MRVL": ({"E": 3, "R": 2, "M": 3, "V": 3, "K": 3, "L": 5}, {"R"}, None, False),
    "CRDO": ({"E": 2, "R": 2, "M": 5, "V": 3, "K": 3, "L": 5}, {"R"}, None, False),
}

# 株価（2026-10-02）と REPORT §4.3 のシナリオ値（約2年後, 割引なし）: (株価, 中立値, 確率加重値)
PRICES = {
    "5803": (5598, 5230, 4890),
    "LITE": (1085.42, 863, 818),
    "6834": (6850, 6220, 6010),
    "COHR": (337.04, 308, 281),
    "FN": (463.69, 500, 448),
    "AAOI": (115.59, 110, 110),  # 加重値(117)が中立値を上回るため中立値で代用（二極的な分布）
}

PATTERNS = {
    # 名前: (1銘柄上限, 小型株上限, K≤2を半分にするか, 投機枠%, 群A上限%, 銘柄枠%)
    "保守": (10, 3, True, 0, 25, 70),
    "標準": (12, 5, True, 0, 40, 87.5),
    "積極": (15, 8, False, 5, 60, 90),
}

# 感応度（R4）: 中立シナリオの倍率を 1.2 倍、確率を 25/50/25 にした場合の (中立値, 確率加重値)
# 弱気値・強気値は REPORT §4.3 のまま。弱気値: 5803 2510, LITE 355, 6834 2780, COHR 120, FN 180, AAOI 46.5
# 強気値: 5803 7600, LITE 1400, 6834 10330, COHR 455, FN 720, AAOI 240
BEAR = {"5803": 2510, "LITE": 355, "6834": 2780, "COHR": 120, "FN": 180, "AAOI": 46.5}
BULL = {"5803": 7600, "LITE": 1400, "6834": 10330, "COHR": 455, "FN": 720, "AAOI": 240}


def conviction(s, verified=None):
    tot = 0.0
    for k, w in W.items():
        v = s[k]
        if verified is not None and k not in verified and v > 3:
            v = 3
        tot += w * v
    return tot


def downside_factor(tk):
    dd = [d for _, _, d, _ in SCORES.values() if d]
    med = sorted(dd)[len(dd) // 2]
    d = SCORES[tk][2]
    if not d:
        return 1.0
    return max(0.7, min(1.2, med / d))


def alt_prices(tk):
    p, neutral, _ = PRICES[tk]
    n2 = neutral * 1.2
    return p, n2, min(n2, 0.25 * BEAR[tk] + 0.5 * n2 + 0.25 * BULL[tk])


def deploy_fraction(tk, alt=False):
    if tk not in PRICES:
        return 0.0
    p, neutral, weighted = alt_prices(tk) if alt else PRICES[tk]
    if p > neutral:
        return 0.0
    if p > weighted:
        return 1 / 3
    if p > weighted * 0.85:
        return 2 / 3
    return 1.0


def allocate(name):
    cap, small_cap, halve_lowk, spec, cap_a, budget = PATTERNS[name]
    rows = {}
    for tk, (s, ver, _, _) in SCORES.items():
        c = conviction(s, ver)
        if c >= 3.0:
            base = small_cap if s["L"] <= 2 else cap
            lim = base
            if halve_lowk and s["K"] <= 2:
                lim = min(lim, cap / 2)
            rows[tk] = (c, base, lim)
    top = max(c for c, _, _ in rows.values()) - 2.5
    # 確信度に応じた天井（R4）: 上限 × clip((確信度−2.5)/(最高−2.5), 0.5, 1)
    rows = {tk: (c, base, lim * max(0.5, min(1.0, (c - 2.5) / top))) for tk, (c, base, lim) in rows.items()}
    raw = {tk: base * (c - 2.5) / top * downside_factor(tk) for tk, (c, base, lim) in rows.items()}

    def build(k):
        w = {tk: min(k * raw[tk], rows[tk][2]) for tk in rows}
        a = sum(v for tk, v in w.items() if SCORES[tk][3])
        if a > cap_a:
            for tk in w:
                if SCORES[tk][3]:
                    w[tk] *= cap_a / a
        return w

    lo, hi = 1.0, 50.0
    if sum(build(lo).values()) < budget:
        for _ in range(100):
            mid = (lo + hi) / 2
            if sum(build(mid).values()) < budget:
                lo = mid
            else:
                hi = mid
    w = build(lo)
    if spec:
        left = spec
        for tk, (s, ver, _, grp) in sorted(SCORES.items(), key=lambda x: -conviction(x[1][0], x[1][1])):
            if grp and 2.5 <= conviction(s, ver) < 3.0 and left >= 3.0:
                w[tk + "（投機）"] = 3.0
                left -= 3.0
    return w


def fmt(d):
    return ", ".join(f"{k} {v:.1f}%" for k, v in d.items())


if __name__ == "__main__":
    print("| 銘柄 | 素点 | 補正後 | 下値調整 | 今日の投入割合 | 同（感応度: 中立倍率×1.2・確率25/50/25） |")
    print("|---|---|---|---|---|---|")
    for tk, (s, ver, _, _) in sorted(SCORES.items(), key=lambda x: -conviction(x[1][0], x[1][1])):
        print(f"| {tk} | {conviction(s):.2f} | {conviction(s, ver):.2f} | {downside_factor(tk):.2f} | "
              f"{deploy_fraction(tk):.2f} | {deploy_fraction(tk, alt=True):.2f} |")
    print()
    for name in PATTERNS:
        w = allocate(name)
        tot = sum(w.values())
        a = sum(v for tk, v in w.items() if tk in SCORES and SCORES[tk][3])
        today = {tk: v * deploy_fraction(tk.replace("（投機）", "")) for tk, v in w.items()}
        today = {k: v for k, v in today.items() if v > 0}
        print(f"### {name}")
        print(f"- 目標比率: {fmt(w)} / 銘柄合計 {tot:.1f}%（うち群A {a:.1f}%）/ 現金 {100 - tot:.1f}%")
        print(f"- 今日の投入: {fmt(today) or 'なし'} / 合計 {sum(today.values()):.1f}% / 現金 {100 - sum(today.values()):.1f}%")
        alt = {tk: v * deploy_fraction(tk.replace("（投機）", ""), alt=True) for tk, v in w.items()}
        alt = {k: v for k, v in alt.items() if v > 0}
        print(f"- 感応度ケースの今日の投入: {fmt(alt) or 'なし'} / 合計 {sum(alt.values()):.1f}%")
        print()
