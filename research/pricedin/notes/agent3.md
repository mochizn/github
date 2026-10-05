# agent3 ノート

## 最新の要点
- R4: data/earnings_reaction.md（8社×4回の決算反応）。「上振れでも決算日に下落」は GLW 4/4・FN 3/4・COHR 3回連続に固有で、LITE（平均 +8.5%）・AAOI（+13.5%）・精工技研・住友電工は上がる。日米の差より「上振れの大きさ」「株価の先回り」で説明できる
- R4: GLW の前受金 $10億は NVIDIA（2029年末まで）。$180 ワラントは無償付与で公正価値 $2.96億を売上から控除。Meta・Amazon 等の前受金は開示なし → 光部分の高倍率を「前受金」で説明できるのは一部
- R4: FN の Amazon ワラント確定の増分が Q4 に減少（21,010→15,280、按分で Amazon 売上 約−27%）[推測]。Datacom 減は報道・アナリストが既に言及＝織り込み済みに格下げ。上振れ候補は新規 datacom 顧客・1.6T
- R3: 逆算（data/reverse_dcf_glw_fn.md）。GLW は期間と利益率を楽観、FN は FY28 以降の数量を悲観
- R2: GLW・FN の A・C、data/stats.md・corr.csv・wc_glw_fn.md。フジクラ×GLW の時差補正相関 0.56
- 再実行: `python3 scripts/fetch_prices.py`、`python3 scripts/stats.py`、`python3 scripts/reverse_dcf_glw_fn.py`

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

## R3 作業ログ
- 逆算: DCF（FCF ベース）と出口PER の2法。GLW は FCF マージン 10%→10/14/18%、WACC 8〜10%。FN は 3%→4/6/8%、WACC 9〜11%。FN は FCF 転換が低いので DCF の要求が過大に出る → 出口PER の方を主に解釈
- board: agent5-1-3 に回答場所を追記、agent2-2-1（FN datacom 突き合わせ）を FN E1 に反映
- 未了: GLW 6/18・6/25 の上昇理由、FN 10-K の関税・タイ集中のリスク要因の精読、GLW の長期（2028年以降）のコンセンサス

## R4 作業ログ
- scripts/earnings_reaction.py → data/earnings_reaction.md・csv（精工技研 08-11 は祝日のため 08-12）
- GLW: B3 訂正（NVIDIA 契約の会計、10-Q Note 2・12）、E を表形式に（方向・時期・織り込み済みの証拠・判定）、C4 目標の更新状況
- FN: B2 に Amazon ワラント推移と datacom 減少の説明、E を表形式に、C4
- board: agent5-3-3 に回答
