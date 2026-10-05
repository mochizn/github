#!/usr/bin/env python3
"""R5 相互チェック（agent2）: 米国5社の出口PER法を同じ前提で再計算する。

agent2（LITE・COHR・AAOI）と agent3（GLW・FN）は、株主資本コスト（9〜12%）・中心の出口PER（20倍/25倍）・
基準とする純利益（ガイド年率/コンセンサス）がそろっていない。ここでは全社を
  株主資本コスト 10%、期間 5年（2026-10 → 2031）、出口PER 20倍と25倍、
  基準 = 次の会計年度のコンセンサス純利益（EPS × 希薄化後株数）
にそろえ、「基準年から 4年間に必要な純利益 CAGR」を出す。
入力: 時価総額は data/agent2_reverse_dcf.md と data/reverse_dcf_glw_fn.md の値（株数は SEC [一次]、株価は prices.csv [一次]）、
コンセンサス EPS は各カード [二次]。
使い方: python3 scripts/agent2_crosscheck_r5.py > data/agent2_crosscheck_r5.md
"""
KE, N, YEARS_AFTER_BASE = 0.10, 5, 4
ROWS = [
    # ticker, 時価総額 $M, 基準年, コンセンサス EPS, 希薄化後株数 M, 元の担当の前提
    ("LITE", 1085.42 * 101.0, "FY27(6月)", 21.67, 101.0, "agent2: ke 10%・中心 25倍・基準 Q1 ガイド年率"),
    ("COHR", 337.04 * 202.2, "FY27(6月)", 9.56, 202.2, "agent2: ke 10%・中心 25倍・基準 Q4 年率"),
    ("AAOI", 115.59 * 92.8, "2027", 4.60, 92.8, "agent2: ke 12%・中心 20倍・基準 2027 コンセンサス"),
    ("GLW", 164.19 * 864.4, "2027", 4.335, 864.4, "agent3: ke 9%・中心 25倍・基準 2026 コンセンサス"),
    ("FN", 463.69 * 36.3, "FY27(6月)", 18.20, 36.3, "agent3: ke 10%・中心 20倍・基準 FY27 コンセンサス"),
]
print("# 出口PER法の前提をそろえた再計算（agent2, R5 相互チェック）\n")
print(f"共通の前提: 株主資本コスト {KE:.0%}、期間 {N}年、基準 = 次の会計年度のコンセンサス純利益、CAGR は基準年から {YEARS_AFTER_BASE}年。[計算]（コンセンサスは [二次]）\n")
print("| 銘柄 | 時価総額 | 基準年のコンセンサス純利益（PER） | 必要な5年後純利益: 20倍 / 25倍 | 必要な CAGR: 20倍 / 25倍 | 元の担当の前提 |")
print("|---|---|---|---|---|---|")
for tk, mcap, by, eps, sh, note in ROWS:
    ni0 = eps * sh
    req = {pe: mcap * (1 + KE) ** N / pe for pe in (20, 25)}
    cg = {pe: (req[pe] / ni0) ** (1 / YEARS_AFTER_BASE) - 1 for pe in req}
    print(f"| {tk} | ${mcap/1000:,.1f}B | {by} ${ni0/1000:,.2f}B（{mcap/ni0:.0f}倍） | ${req[20]/1000:,.2f}B / ${req[25]/1000:,.2f}B | {cg[20]:+.0%} / {cg[25]:+.0%} | {note} |")
