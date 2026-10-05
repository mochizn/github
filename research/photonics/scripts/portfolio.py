#!/usr/bin/env python3
"""6軸採点 → 3パターンの比率（agent5, R3 暫定版）。

使い方: python3 scripts/portfolio.py

ルール（notes/agent5.md「評価軸の定義」と R3 の決定）
- 確信度 = 0.20E + 0.20R + 0.15M + 0.25V + 0.20K
- 補正: agent4 の ✔ が無い軸は、3 点超なら 3 点に下げる（良い材料は確認されるまで使わない）。
  3 点未満は下げたまま（悪い材料は未確認でも使う）。R3 で非対称に変更
- 組み入れ: 補正後の確信度 ≥ 3.0。積極パターンだけ 2.25 以上を「投機枠」（合計 5% 以内）で扱う
- 比率: 確信度が最も高い銘柄に上限いっぱいを置き、他は 上限 × (確信度 − 2.5) / (最高確信度 − 2.5)。
  銘柄数が少なく上限で頭打ちになるため、単純な按分ではなく確信度の順位が比率に出るこの方式にした（R3）。
  銘柄枠の余りは「未採点候補枠」（採点が済むまで現金）
- 上限: 1銘柄（保守10/標準12/積極15%）、小型株（3/5/8%）、K ≤ 2 の銘柄は保守・標準で1銘柄上限の半分
- ボラ調整（90日ボラ）は全銘柄 ⚠未取得のため R3 では未適用
"""

W = {"E": 0.20, "R": 0.20, "M": 0.15, "V": 0.25, "K": 0.20}

# (素点, ✔ が付いた軸) 。素点の理由は notes/agent5.md「R3: 6軸採点 v2」
SCORES = {
    "5803": ({"E": 4, "R": 4, "M": 5, "V": 4, "K": 3, "L": 5}, {"E", "M", "V", "K", "L"}),
    "LITE": ({"E": 5, "R": 4, "M": 5, "V": 2, "K": 2, "L": 5}, {"E", "M", "V", "K", "L"}),
    "COHR": ({"E": 4, "R": 3, "M": 4, "V": 3, "K": 3, "L": 5}, set()),
    "6834": ({"E": 4, "R": 4, "M": 5, "V": 3, "K": 3, "L": 2}, set()),
    "AAOI": ({"E": 4, "R": 2, "M": 4, "V": 3, "K": 1, "L": 3}, set()),
}

PATTERNS = {
    # 名前: (銘柄枠%, 1銘柄上限, 小型株上限, K≤2を半分にするか, 投機枠%)
    "保守": (70, 10, 3, True, 0),
    "標準": (87.5, 12, 5, True, 0),
    "積極": (95, 15, 8, False, 5),
}


def conviction(s, verified=None):
    tot = 0.0
    for k, w in W.items():
        v = s[k]
        if verified is not None and k not in verified and v > 3:
            v = 3
        tot += w * v
    return tot


def allocate(name):
    budget, cap, small_cap, halve_lowk, spec = PATTERNS[name]
    rows = {}
    for tk, (s, ver) in SCORES.items():
        c = conviction(s, ver)
        if c >= 3.0:
            lim = small_cap if s["L"] <= 2 else cap
            if halve_lowk and s["K"] <= 2:
                lim = min(lim, cap / 2)
            rows[tk] = [c, lim]
    ex = {tk: r[0] - 2.5 for tk, r in rows.items()}
    top = max(ex.values())
    w = {}
    for tk in rows:
        base = small_cap if SCORES[tk][0]["L"] <= 2 else cap
        w[tk] = min(base * ex[tk] / top, rows[tk][1])
    out = dict(w)
    if spec:
        for tk, (s, ver) in SCORES.items():
            c = conviction(s, ver)
            if 2.25 <= c < 3.0:
                out[tk + "（投機枠）"] = min(3, spec)
    used = sum(out.values())
    reserve = budget + spec - used
    return out, reserve, 100 - budget - spec


if __name__ == "__main__":
    print("| 銘柄 | 素点 | 補正後 |")
    print("|---|---|---|")
    for tk, (s, ver) in SCORES.items():
        print(f"| {tk} | {conviction(s):.2f} | {conviction(s, ver):.2f} |")
    print()
    for name in PATTERNS:
        out, reserve, cash = allocate(name)
        parts = ", ".join(f"{tk} {v:.1f}%" for tk, v in out.items())
        print(f"- {name}: {parts}, 未採点候補枠 {reserve:.1f}%, 現金・ヘッジ {cash:.1f}%")
