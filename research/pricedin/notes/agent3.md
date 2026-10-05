# agent3 ノート

## 最新の要点
- R2: GLW・FN の A（年表＋要因の判定）・C（アナリスト）・D（前提カード、GLW は SOTP）を作成。data/stats.md（β・R²・相関・日本株の時差反応）、data/wc_glw_fn.md（在庫・売掛日数・FCF）
- GLW: 決算日4連続下落の理由は「次四半期の売上ガイダンスがコンセンサスを超えない」（4月は下回り、7月は一致）。目標 平均 $175〜190、7/29 に6社一斉引き下げ、Bernstein 新規 $140。SOTP では光通信に 約82〜86倍を払っている
- FN: 決算翌日の下落理由は ①期待値（2月）→ ②NVIDIA datacom 減（5月）→ ③datacom 減＋FCF −$37M（8月）。NVIDIA 向け FY26 −21%（B. Riley「おそらく中国勢にシェアを奪われた」）。目標平均 $650〜734（+40〜58%）でアナリストと株価が大きく乖離。FY27 予想 25.5倍
- 日本株の時差補正相関はフジクラ×GLW が 0.56 で SOX（0.44）より高い。米国光株の決算 → 翌日の日本株は相関 0.32（n=20）
- 再実行: `python3 scripts/fetch_prices.py`（--offline 可）、`python3 scripts/stats.py`

## R1 作業ログ
- 固定閾値（±7%）だと AAOI 118日・LITE 81日で年表に使えないため、指標比超過リターンの上位順に変更。全件は CSV
- 日本株は同日 SMH との相関 0.15〜0.19 だが、前の米国日の SMH とは 0.31〜0.42（時差補正が必要）

- SEC から GLW 8-K×12・10-K・10-Q、FN 8-K×7・10-K×2・10-Q×3 を取得（UA 付き、0.3秒間隔）。stocks/GLW.md・FN.md の A/B/D/E を作成。C（アナリスト）は R2
- 未確認: GLW 1/27 +15.6%（Meta 契約発表日か）、6/29 +15.7%（Amazon 契約発表日か）、FN 8/4 +16.5% の理由。investor.corning.com は 403 なので投資家説明会資料は未取得
- board: agent2 へ FN datacom 突き合わせ依頼、agent4 へ7月一斉下落の要因依頼

## R2 作業ログ
- agent5-1-3 への回答: ①β・R² → data/stats.md §1（＋agent4_factor.md）、②相関 → stats.md §2・corr.csv、③大きな値動き → big_moves.md（R1）、④高値・安値 → summary.md（R1）、⑤時差 → stats.md §3、⑥USD/JPY → prices.csv の JPY=X、⑦前提カード → stocks/GLW.md・FN.md D2（逆算DCF は R3）、⑧GLW SOTP → GLW.md D1、⑨GLW 長期契約 → GLW.md B3（前受金 $1.0B、契約負債 $2.7B）、⑩FN 顧客・拠点 → FN.md B2・D2（関税リスクの記述の精読は R3）、⑪在庫・売掛・FCF → data/wc_glw_fn.md
- Web 取得: cnbc・qz・investing.com・benzinga・fool・tikr・gurufocus は egress でブロック。Yahoo Finance 記事・marketbeat・stockanalysis・seekingalpha の検索要約で代替（[二次]）。Yahoo の quoteSummary（予想）は crumb が取れず不可
- 未了（R3）: 逆算DCF（GLW・FN）、GLW 6/18・6/25 の上昇理由、FN 10-K の関税・タイ集中のリスク要因の精読
