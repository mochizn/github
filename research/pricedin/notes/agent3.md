# agent3 ノート

STATUS: DONE（R7）

## 最新の要点
- R6: GLW・FN の E カレンダー（E 末尾）。次の山場は GLW Q3 決算 10/27〜28 頃・10-Q 10/30 頃（ATM 実績・前受金）、FN Q1 FY27 決算 11/2 引け後頃・10-Q（Amazon ワラント確定株数）。日付は前年パターンからの推定
- R6: REPORT §5.6「日米の市場全体の PER 差」→ 日経平均 17.4倍・TOPIX 17倍台 vs S&P500 予想 19.0倍（[二次]）。差は1割強で、必要成長率の日米差の大半は銘柄ごとの期待の差（data/common_yardstick.md 末尾）
- R6: §5.6 の U2（スケールアップ光化がコンセンサスに入っているか）は GLW・FN とも確認不能（コンセンサスの内訳は有料。BofA が GLW のガラス基板・CPO を「オプション」と言及するのみ [二次]）
- R6: agent2 の doubts 3件に「対応」を追記済み
- R5: agent1 カードの相互チェック。原典（FY27 1Q 短信3本）で予想・株数・純有利子負債を抜き取り → すべて一致。指摘4件（board/doubts/agent3-5-1〜4）: 住友電工だけ ke 8%・出口15倍で比較不能（共通前提では +11.6%）、EV の非支配持分の扱い、住友電工の起点が減益年、5803 E4 の GLW 前受金との対比は弱めるべき
- R5: data/common_yardstick.md（8社を ke 9/10%・出口PER 15/20/25・5年でそろえた必要純利益 CAGR）。共通前提で日本3社 +12〜21%、米国は FN（+16%）を除き +27〜64%
- R5: agent2 の指摘で自カードを訂正: GLW の前受金は NVIDIA $10億だけでなく 2025末 約$15億（ディスプレイ＋光通信）＋2025年新規 $4.9億（10-K Note 4）。FN の FY27 起点の CAGR は約4年で +20%（R3 の +15.5% は5年割りで過小）
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

## R5 作業ログ
- 相互チェック（agent1 の 5803・6834・5802）: 前提比較、TDnet 1Q 短信で抜き取り、E の織り込み証拠を earnings_reaction で補足 → board/doubts/agent3-5-1〜4
- scripts/common_yardstick.py → data/common_yardstick.md
- 自カードへの指摘（agent2-5-1〜3）に回答・訂正: GLW B3・E3・D3 注記、FN D3・前提カード・E1

## R6 作業ログ
- doubts agent2-5-1〜3 に対応場所を追記
- GLW・FN の E カレンダー（日付の確度タグ付き）
- data/common_yardstick.md に日米の市場 PER 比較を追加

## R7 訂正一覧
- data/post_base_moves.md 追加（基準日→10-08 終値、8社＋SOX・日経平均。米国株と日経平均は 10-08 日足が空のため60分足の引け値で代用）、REPORT §0.1 直下に「基準日以降の動き（参考）」として1表
- REPORT §0.1 GLW 行: 「2030年計画を達成しても PER 約25倍が必要」→「2031年に出口 PER 25〜30倍と純利益率の改善が必要」（stocks/GLW.md D3・E1 の R4 以降の値に合わせた）
- REPORT の自分由来の数字（FN +16.4%/+19%、FN の FCF ベース $181〜243億、GLW 光部分 PER 82〜86倍、GLW 前受金の R5 訂正、決算反応表）をカードの最新値と照合 → 一致
- stocks/FN.md C3: 「8社で最も安い部類」→「予想 PER が8社で最も低い部類（強気派の論拠の要約）」（評価に読める表現を中立化）
- stocks/FN.md D3: 「利益が現金にならない限り、株価は高くない」→「FCF ベースで見ると株価の要求水準は高い」（同上）
