"""agent4: セクター要因の分解とイベント日の反応表。
入力: data/prices.csv（agent3, adjclose）。出力: data/agent4_factor.md, data/agent4_events.csv
- 米国光バスケット = LITE, COHR, AAOI, GLW, FN の等ウェイト（日次リバランス）
- 日本光バスケット = 5803, 6834, 5802
- 分解: r_i = a + b1*SMH + b2*OPT_resid(ex-self) + e  （OPT_resid は ex-self バスケットを SMH に回帰した残差）
  日本株は SMH を「前の米国営業日」にずらし、日経平均も加える
"""
import csv, math, collections, os, sys
import numpy as np
D = os.path.join(os.path.dirname(__file__), '..', 'data')
px = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(D, 'prices.csv'))):
    if r['adjclose']:
        px[r['symbol']][r['date']] = float(r['adjclose'])
def rets(sym):
    ds = sorted(px[sym]); return {ds[i]: px[sym][ds[i]] / px[sym][ds[i-1]] - 1 for i in range(1, len(ds))}
R = {s: rets(s) for s in px}
US = ['LITE', 'COHR', 'AAOI', 'GLW', 'FN']; JP = ['5803.T', '6834.T', '5802.T']
usd = sorted(set.intersection(*[set(R[s]) for s in US + ['SMH']]))
jpd = sorted(set.intersection(*[set(R[s]) for s in JP + ['^N225']]))
def prev_us(d):
    i = np.searchsorted(usd, d) - 1  # 東京の d より前の最後の米国営業日
    return usd[i] if i >= 0 else None
def ols(y, X, const=True):
    X = np.column_stack(([np.ones(len(y))] if const else []) + X); b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b; return b, 1 - e.var() / y.var(), e
out = []
out.append('# セクター要因の分解（agent4, 基準日 2026-10-02, data/prices.csv の adjclose から計算）\n')
out.append('分散の分解は逐次: ①指標（米国株=SMH 同日、日本株=日経平均 同日＋前の米国営業日の SMH）→ ②光バスケット（自分を除く、①で説明できない部分）→ ③残り＝個別要因。累積寄与は「1年の対数リターン」を、係数×各要因の日次リターン合計で近似配分（残り＝個別要因、α を含む）。光バスケットは指標に切片なしで回帰した残差（バスケットの指標超過分はセクター要因側に残す）。[一次: 計算]\n')
out.append('| 銘柄 | ①指標で説明(R²) | ②光セクターで追加説明 | ③個別(残り) | β_指標 | β_光 | 1年 対数リターン | うち指標 | うち光セクター | うち個別 | うち変動の目減り |')
out.append('|---|---|---|---|---|---|---|---|---|---|---|')
for grp, names in (('US', US), ('JP', JP)):
    for s in names:
        peers = [p for p in names if p != s]
        if grp == 'US':
            ds = usd; mk = [np.array([R['SMH'][d] for d in ds])]
        else:
            ds = [d for d in jpd if prev_us(d) and prev_us(d) in R['SMH']]
            mk = [np.array([R['^N225'][d] for d in ds]), np.array([R['SMH'][prev_us(d)] for d in ds])]
        y = np.array([R[s][d] for d in ds])
        bk = np.array([np.mean([R[p][d] for p in peers]) for d in ds])
        # 日本株の光要因には米国光バスケット（前の米国営業日）も入れる
        if grp == 'JP':
            usb = np.array([np.mean([R[p][prev_us(d)] for p in US]) for d in ds])
            _, _, ou = ols(usb, mk, const=False); oth = [ou]
        else:
            oth = []
        _, _, o = ols(bk, mk, const=False)  # 切片なし: バスケットの指標超過分はセクター要因に残す
        b1, r1, _ = ols(y, mk); b2, r2, e = ols(y, mk + [o] + oth)
        ly = np.log1p(y); n = len(ds)
        cm = sum(b2[1 + k] * mk[k].sum() for k in range(len(mk)))  # 日次リターンの単純和で近似
        co = sum(b2[1 + len(mk) + k] * f.sum() for k, f in enumerate([o] + oth))
        tot = ly.sum(); dr = ly.sum() - y.sum(); ci = tot - cm - co - dr  # dr: 変動による目減り（対数と単純和の差）
        bo = ', '.join(f'{x:.2f}' for x in b2[1 + len(mk):])
        out.append(f'| {s} | {r1:.0%} | {r2 - r1:.0%} | {1 - r2:.0%} | {", ".join(f"{x:.2f}" for x in b2[1:1+len(mk)])} | {bo} | {tot:+.2f} | {cm:+.2f} | {co:+.2f} | {ci:+.2f} | {dr:+.2f} |')
out.append('\n注: 日本株の②は「日本光バスケット（自分除く）」と「米国光バスケット（前の米国営業日）」の2つ（β_光 はこの順）。日本株の①の β は 日経, SMH(前日) の順。対数リターンなので単純リターンとは違う（例: +1.0 ≒ 2.7倍）')
open(os.path.join(D, 'agent4_factor.md'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))

# イベント日の反応表
EV = [l.split('|') for l in open(os.path.join(os.path.dirname(__file__), 'agent4_events.txt')).read().strip().splitlines() if l and not l.startswith('#')]
w = csv.writer(open(os.path.join(D, 'agent4_events.csv'), 'w'))
cols = ['SMH', 'NVDA'] + US + JP
w.writerow(['event_date', 'reaction_date_us', 'event', 'US_optics_basket', 'excess_vs_SMH'] + cols)
print('\n| 反応日(米) | イベント | 米光バスケット | 対SMH超過 | SMH | NVDA | LITE | COHR | AAOI | GLW | FN | 5803 | 6834 | 5802 |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for ed, rd, name in EV:
    rd = rd.strip()
    b = np.mean([R[s].get(rd, np.nan) for s in US])
    vals = []
    for c in cols:
        if c in JP:  # 米国反応日の翌東京営業日
            nx = [d for d in jpd if d > rd][:1]; vals.append(R[c].get(nx[0], np.nan) if nx else np.nan)
        else:
            vals.append(R[c].get(rd, np.nan))
    w.writerow([ed.strip(), rd, name.strip(), f'{b:.4f}', f'{b - R["SMH"].get(rd, np.nan):.4f}'] + [f'{v:.4f}' for v in vals])
    print(f'| {rd} | {name.strip()} | {b:+.1%} | {b - R["SMH"].get(rd, np.nan):+.1%} | ' + ' | '.join(f'{v:+.1%}' for v in vals) + ' |')
