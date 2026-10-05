"""agent4 R3: 大きな値動きの日（data/big_moves.csv の全行）を「業界要因 / 個別要因」に判定する。
モデルは agent4_sector.py と同じ（1年の日次で推定）:
  米国株 r = a + b1*SMH + b2*光バスケット残差(自分除く) + e
  日本株 r = a + b1*日経 + b2*SMH(前の米国営業日) + b3*日本光残差(自分除く) + b4*米光残差(前の米国営業日) + e
判定（その日のリターン r に対する各成分の寄与）:
  全体 = 指標成分, 光 = 光セクター成分, 個別 = r - 全体 - 光 - a
  ・業界(全体)  : 全体成分が r と同符号で |全体| >= 0.5|r|
  ・業界(光)    : 上に当たらず、全体+光 が同符号で |全体+光| >= 0.5|r|
  ・個別        : 個別成分が同符号で |個別| >= 0.5|r|
  ・混合        : どれにも当たらない
出力: data/agent4_daylabels.csv（全行）、data/agent4_factor.md の末尾に銘柄別の表を追記
"""
import csv, collections, os
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, '..', 'data')
px = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(D, 'prices.csv'))):
    if r['adjclose']: px[r['symbol']][r['date']] = float(r['adjclose'])
def rets(s):
    ds = sorted(px[s]); return {ds[i]: px[s][ds[i]] / px[s][ds[i-1]] - 1 for i in range(1, len(ds))}
R = {s: rets(s) for s in px}
US = ['LITE', 'COHR', 'AAOI', 'GLW', 'FN']; JP = ['5803.T', '6834.T', '5802.T']
usd = sorted(set.intersection(*[set(R[s]) for s in US + ['SMH']]))
jpd = sorted(set.intersection(*[set(R[s]) for s in JP + ['^N225']]))
def prev_us(d):
    i = np.searchsorted(usd, d) - 1; return usd[i] if i >= 0 else None
def ols(y, X, const=True):
    A = np.column_stack(([np.ones(len(y))] if const else []) + X); b, *_ = np.linalg.lstsq(A, y, rcond=None); return b, y - A @ b
EV = collections.defaultdict(list)
for l in open(os.path.join(H, 'agent4_events.txt')):
    if l.strip() and not l.startswith('#'):
        ed, rd, name = [x.strip() for x in l.split('|')]; EV[rd].append(name)
model = {}
for s in US + JP:
    if s in US:
        ds = usd; peers = [p for p in US if p != s]
        mk = [np.array([R['SMH'][d] for d in ds])]
        bk = np.array([np.mean([R[p][d] for p in peers]) for d in ds]); _, o = ols(bk, mk, False); sec = [o]
    else:
        ds = [d for d in jpd if prev_us(d)]; peers = [p for p in JP if p != s]
        mk = [np.array([R['^N225'][d] for d in ds]), np.array([R['SMH'][prev_us(d)] for d in ds])]
        bk = np.array([np.mean([R[p][d] for p in peers]) for d in ds]); _, o = ols(bk, mk, False)
        ub = np.array([np.mean([R[p][prev_us(d)] for p in US]) for d in ds]); _, ou = ols(ub, mk, False); sec = [o, ou]
    y = np.array([R[s][d] for d in ds]); b, e = ols(y, mk + sec)
    k = len(mk)
    model[s] = {d: (y[i], sum(b[1+j]*mk[j][i] for j in range(k)), sum(b[1+k+j]*sec[j][i] for j in range(len(sec))), b[0]) for i, d in enumerate(ds)}
def label(r, m, o, a):
    idio = r - m - o - a
    if np.sign(m) == np.sign(r) and abs(m) >= 0.5 * abs(r): return '業界(全体)', idio
    if np.sign(m + o) == np.sign(r) and abs(m + o) >= 0.5 * abs(r): return '業界(光)', idio
    if np.sign(idio) == np.sign(r) and abs(idio) >= 0.5 * abs(r): return '個別', idio
    return '混合', idio
def events_for(s, d):
    if s in US: return EV.get(d, [])
    pu = prev_us(d); out = list(EV.get(d, []))  # 東京の当日イベント（日本固有）＋前の米国営業日のイベント
    if pu: out += [f'(前の米国日 {pu}) ' + x for x in EV.get(pu, [])]
    return out
rows = []
for r in csv.DictReader(open(os.path.join(D, 'big_moves.csv'))):
    s, d = r['symbol'], r['date']
    if s not in model or d not in model[s]: continue
    ret, m, o, a = model[s][d]; lab, idio = label(ret, m, o, a)
    rows.append([d, s, ret, m, o, idio, lab, ' / '.join(events_for(s, d))])
w = csv.writer(open(os.path.join(D, 'agent4_daylabels.csv'), 'w'))
w.writerow(['date', 'symbol', 'ret', 'index_part', 'optics_sector_part', 'idio_part', 'label', 'events_agent4'])
for x in rows: w.writerow([x[0], x[1], f'{x[2]:.4f}', f'{x[3]:.4f}', f'{x[4]:.4f}', f'{x[5]:.4f}', x[6], x[7]])
out = ['\n---\n', '## R3: 大きな値動きの日の「業界要因 / 個別要因」判定（scripts/agent4_classify.py）\n',
       '対象は data/big_moves.csv の全行（|日次| ≥ 7% または |超過| ≥ 6%）。成分は上の分解と同じモデルで、その日の「指標成分」「光セクター成分」「個別成分」。判定: 指標成分が同符号でリターンの半分以上 → **業界(全体)**、指標＋光で半分以上 → **業界(光)**、個別成分が半分以上 → **個別**、それ以外 → 混合。全行は data/agent4_daylabels.csv。[一次: 計算]。イベント名は scripts/agent4_events.txt（[二次] 含む、出典は notes/agent4.md §5・§10）。**注意: 「業界(光)」は同業他社の個別ニュースの波及を含む**（例: NVIDIA の LITE・COHR 出資の日、他の光株も上がる）。判定は「市場がその日、セクターとして動いたか」であり、ニュースの出所ではない\n',
       '### 銘柄別の集計（大きな値動きの日数）\n', '| 銘柄 | 日数 | 業界(全体) | 業界(光) | 個別 | 混合 | 個別の比率 |', '|---|---|---|---|---|---|---|']
for s in US + JP:
    c = collections.Counter(x[6] for x in rows if x[1] == s); n = sum(c.values())
    out.append(f"| {s} | {n} | {c['業界(全体)']} | {c['業界(光)']} | {c['個別']} | {c['混合']} | {c['個別']/n:.0%} |")
for s in US + JP:
    sel = sorted([x for x in rows if x[1] == s], key=lambda x: -abs(x[2]))[:15]
    out.append(f'\n### {s}（|日次| の大きい順に15日）\n')
    out.append('| 日付 | 日次 | 指標成分 | 光セクター成分 | 個別成分 | 判定 | 同日の業界・全体イベント（agent4） |')
    out.append('|---|---|---|---|---|---|---|')
    for x in sorted(sel):
        out.append(f'| {x[0]} | {x[2]:+.1%} | {x[3]:+.1%} | {x[4]:+.1%} | {x[5]:+.1%} | {x[6]} | {x[7] or "—（業界イベントなし → 個別ニュースを各カードで確認）"} |')
p = os.path.join(D, 'agent4_factor.md'); txt = open(p).read().split('\n---\n')[0].rstrip('\n')
open(p, 'w').write(txt + '\n' + '\n'.join(out) + '\n')
print('\n'.join(out[:20]))
