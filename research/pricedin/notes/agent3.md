# agent3 ノート

## 最新の要点
- データ基盤 push 済み: data/prices.csv（8社＋SMH/^SOX/NVDA/^GSPC/QQQ/^N225/1306.T/USDJPY、1年日足）、data/summary.md（期間リターン・最大下落・β）、data/big_moves.md（超過リターン上位15日＋5日窓）、big_moves.csv（全件）
- 基準日 2026-10-02。1年: GLW +94%（高値 6/30 から −40%）、FN +25%（高値 5/14 から −38%）、SMH +84%
- 全銘柄共通: 2026-06下旬〜07-29 に高値から −40〜−65% の同時下落 → 7/30・8/4 に一斉反発（セクター要因の候補、agent4 へ）
- 再実行: `python3 scripts/fetch_prices.py`（--offline で data/raw を再利用）

## R1 作業ログ
- 固定閾値（±7%）だと AAOI 118日・LITE 81日で年表に使えないため、指標比超過リターンの上位順に変更。全件は CSV
- 日本株は同日 SMH との相関 0.15〜0.19 だが、前の米国日の SMH とは 0.31〜0.42（時差補正が必要）
