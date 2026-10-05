# agent3 ノート（米国株＋台湾・中国参考）

## 最新の要点（R3 終了時, 2026-10-05）
- R3: stocks/COHR.md 新規（株価 $337.04・時価 $66.0B・純有利子負債 $1.24B・EV $67.2B、FY26 売上 $7.12B、Q1FY27 ガイド $2.3B、FY27予想PER 約36〜44倍、EV/年率売上 約7.3倍、CPO=中立）、stocks/FN.md 簡易版（時価 $16.6B、ガイド年率 PER 約28倍）
- LITE: agent4 ✘（EV 計算法）を反映し **EV = 希薄化後 約1.01億株 × 株価 − 現金 = 約$106.9B、EV/年率売上 約21倍** に統一。地域別（タイ 20.8%・香港 17.2%・中国 8.7%(9か月)）を追記し中国比率は確定・打ち切り
- AAOI: FY2025 売上 $455.7M（CATV $245M > DC $196M）、2026年 ATM 3本・6月末までに約 $1.05B/780万株発行、Culper 空売りレポートは 2025-02-04。⚠ 6月末現金 $499.7M と ATM 調達額の整合が未確認
- **訂正（✘自己申告）**: R1 の Eoptolink「1H26 売上 104.4億元(+283%)」は **1H2025 の数値**。正しくは 1H26 売上 約209.1億元（+100.3%）、純利益 75.29億元（+91.0%）
- 新規出典 約20 / 新規主張 約40 / 次ラウンド: 米国勢の比較表（LITE/COHR/AAOI/FN/CIEN の倍率・成長・マージンを1表に）、COHR の顧客比率・中国比率・FY27 コンセンサスの食い違い、余力で CIEN or MRVL 簡易カード

## ラウンド3（2026-10-05）
- 依頼対応: agent5-2-1（LITE/COHR/AAOI の DCF 入力 → 各カード §0・§4）、agent1-2-2（COHR 8-K URL 候補と Eoptolink の訂正）、agent4 V-LITE の ✘/⚠ を LITE.md に反映 → board/requests/agent3-3-1.md
- 判断: LITE の EV は希薄化後株数方式のみを採用（基本株＋額面方式は撤回）。agent4 の指摘は正しい: Q4 の消却損 $7.8B 自体が「額面と転換価値の差」の大きさを示している
- 判断: COHR は Series B 優先株が 2025-12 までに全額転換済みなので、基本株数＝実質の希薄化後株数として扱う
- 判断: COHR の FY27 コンセンサス EPS は $9.41（より新しい「過去90日で上方修正」の記述）を主に、$7.61 を ⚠ で併記
- 判断: Eoptolink は R1 の数値が前年同期のものだったため訂正。Innolight（1H26 417.8億元, +182%）は前年同期 147.9億元からの伸びと整合するので維持
- Web: 検索 13 / Fetch 0

## ラウンド2（2026-10-05）
- 依頼対応: agent5-1-3（戦略用データ欄を LITE/AAOI の §0 に）、agent4-r1-1（FY表記＋期末日、GAAP/non-GAAP・TTM/予想の明記、LITE GAAP TTM PER→算出不能、ガイド年率 non-GAAP PER 約65倍、地域別）、agent1-1-1（CPO 得/損の1行を各カード §0 に。TSEM/FORM/TER/TSM の追加はユニバース表に反映）
- 判断: LITE の EV は「転換社債を株式とみなす」希薄化ベースを主に採用（全シリーズの転換価格が株価を大きく下回るため）。基本株ベースも併記
- 判断: AAOI の時価総額は 424B5 の株数 84.9M × $115.59 = $9.81B がサイト表示と一致したため採用（R1 の「日付不明⚠」を解消）
- 判断: COHR は R2 では着手せず（指示上「余力で」）。R3 に回す
- 内部整合チェック（agent4 の ✔ 基準用）: LITE FY25/FY26 の四半期合計が通期と一致、四半期の前年比も一致。AAOI 時価総額も一致
- Web: 検索 17 / Fetch 0

## ラウンド1（2026-10-05）

### 環境
- sec.gov / investor.lumentum.com / nasdaq / barchart / businesswire / stockanalysis 等すべて EGRESS_BLOCKED（ENV.md）。WebSearch のみ可
- 判断: 検索スニペットに出た数値は出典 URL（スニペット元）を併記して [二次]。SEC の URL がスニペットに出ても本文を開けていないので [一次] にはしない

### 米国 光関連ユニバース（粗い評価）
光エクスポージャ: **H**=売上の過半が光関連 / **M**=10〜50% / **L**=10%未満だが光で重要な位置。比率は特記なき限り [推測]（agent3 の事前知識ベース、次ラウンド以降に検証）
時価総額は 2026-10-02 前後、[二次]（検索スニペット、要再確認）。

| ティッカー | 社名 | VC上の位置 | 光Exp | 直近業績メモ [二次] | 時価総額 | カード優先度 |
|---|---|---|---|---|---|---|
| LITE | Lumentum | EML/CWレーザー、トランシーバ、OCS、CPO光源 | H(≒100%) | FY26 $3.01B +83%、Q1FY27 ガイド $1.25B | 約$96B（計算） | ◎ R1着手 |
| AAOI | Applied Optoelectronics | 垂直統合トランシーバ（自社レーザー）、CATV | H（DC 56%） | Q2'26 $191.9M(+86%)、DC $107.7M、CATV $80.6M。2026年売上 約$1.1B 見通し、Q4 1.6T $70M超 | $9.81B（10/02, 株数×株価で一致） | ◎ R2 カード作成 |
| COHR | Coherent | トランシーバ最大手級、InP/VCSEL/SiPh、6インチInP | H(DC&Comm 79%) | FY26 $7.12B +23%、Q4 $2.05B、Q1FY27 ガイド $2.2〜2.4B、PhotonLink 発表 | **$66.0B**（10/02, $337.04） | ◎ R3 カード作成 |
| FN | Fabrinet | 光モジュールEMS（NVIDIA/Cisco 等） | H | FY26 $4.6B +36%、Q4 $1.316B。顧客 Cisco20%/NVIDIA16%/Nokia11%/Amazon11% | **$16.6B**（10/02, $463.69） | ○ R3 簡易カード |
| CIEN | Ciena | 光伝送システム、DCI、800G ZR、WaveLogic | H(≒100%、但しシステム) | FQ3'26 $1.67B +37%、FY26 ガイド $6.42B(+35%) | $55.5B | ○ |
| GLW | Corning | 光ファイバ・ケーブル・コネクタ | M(OptComm 約44%: Q2 $2.07B/$4.74B) | OptComm +32%、Enterprise +65% | $148.8B | ○（フジクラ比較） |
| CRDO | Credo | AEC（銅）、光DSP、リタイマ | M（光DSPは一部、AECは光の代替＝競合） | FQ1'27 $479M +115% | $41.1B | △（LPO/AEC論点） |
| MRVL | Marvell | 光DSP（PAM4）、TIA/ドライバ、SiPhエンジン | M | 未取得 | 未取得 | ○ |
| AVGO | Broadcom | EML/VCSEL、光DSP、CPOスイッチ（Bailly/Tomahawk CPO） | L | 未取得 | 未取得 | △（CPO論点で参照） |
| NVDA | NVIDIA | CPOスイッチ（Spectrum-X/Quantum-X Photonics）、最大顧客 | L | 未取得 | — | 参照のみ |
| CSCO | Cisco（Acacia） | コヒーレントDSP/モジュール、SiPh | L | 未取得 | — | 参照のみ |
| ANET | Arista | スイッチ（LPO推進）。光の需要側 | L | 未取得 | — | 参照のみ |
| TSEM | Tower Semiconductor | SiPh/SiGe ファウンドリ | M | 未取得 | 未取得 | ○ |
| MTSI | MACOM | ドライバ/TIA、レーザー、LPO向けアナログ | M | 未取得 | 未取得 | △ |
| SMTC | Semtech | LPO/ドライバ/TIA、CopperEdge | L〜M | 未取得 | 未取得 | △ |
| AXTI | AXT | InP/GaAs 基板（中国生産・輸出規制） | H（InP需要直結） | 未取得 | 未取得 | ○（ボトルネック論点） |
| POET | POET Technologies | 光インターポーザ（小型） | H | 未取得 | 小型 | △（投機枠） |
| LWLG | Lightwave Logic | EOポリマー変調器（売上ほぼなし） | H | 未取得 | 小型 | △（投機枠） |
| VIAV | Viavi | 光測定器・ファイバテスト | M | 未取得 | 未取得 | △（検査・装置枠） |
| KEYS | Keysight | 光/高速測定 | L | 未取得 | — | 参照のみ |
| IPGP | IPG Photonics | 産業用ファイバレーザー（データセンター外） | H（光だがAI外） | 未取得 | — | 除外候補（AI需要と無関係） |
| NOK | Nokia（Infinera 買収） | 光伝送、InP PIC | L〜M | 未取得 | — | 参照のみ（米ADR） |
| TSM | TSMC（ADR） | COUPE（CPO 光エンジン製造） | L | 未取得 | — | 参照のみ（R2 追加、agent1 提案） |
| FORM | FormFactor | SiPh ウエハプローバ（TRITON） | L | 未取得 | — | △（検査枠、R2 追加、agent1 提案） |
| TER | Teradyne | 光/CPO テスト | L | 未取得 | — | 参照のみ（R2 追加、agent1 提案） |

台湾・中国（参考、競合として）:
| コード | 社名 | 位置 | メモ [二次] |
|---|---|---|---|
| 300308.SZ | Zhongji Innolight（中際旭創） | 800G/1.6T トランシーバ世界首位級 | 1H26 売上 417.8億元(+182%)、純利益 136.5億元(+242%) https://finance.biggo.com/news/2b25909c-bd1d-49fd-8c51-a9c7996700d5 |
| 300502.SZ | Eoptolink（新易盛） | トランシーバ（LPO/SiPh 強い） | **R3 訂正**: 1H26 売上 約209.1億元(+100.3%)、純利益 75.29億元(+91.0%)（2026-08-24 発表）https://www.stcn.com/article/detail/4108576.html 。R1 の 104.4億元(+283%) は 1H2025 の値だった（✘） |
| 300394.SZ | TFC（天孚通信） | 光エンジン部品・パッシブ | 未取得 |
| 002281.SZ | Accelink（光迅科技） | 部品〜モジュール、チップ内製 | 未取得 |
| 601869.SH | YOFC（長飛光纖） | 光ファイバ | 1H26 純利益 約9倍との報道（同上） |
| 3081.TWO | LandMark Optoelectronics（聯亞光電） | InP エピウェハ | 未取得 |
| 2455.TW | VPEC（全新光電） | GaAs/InP エピ | 未取得 |
| 2330.TW | TSMC | COUPE（SiPh/CPO 製造） | 参照のみ |

### 初見の構造的観察（agent1/agent5 向けの論点候補）[推測]
1. **利益は「InPレーザー（EML/CW）」に溜まっている**: LITE の Non-GAAP GM 50%超、200G EML 完売・ASP 2倍。一方トランシーバ組立（FN、AAOI）は GM が低い。中国勢（Innolight/Eoptolink）はトランシーバで圧倒的規模と利益
2. **SiPh 化（1.6T の約72%）は EML→CW レーザーへのミックス変化**。LITE は CW 増産で対応中。CPO も外部光源（ELS）としてレーザー需要は残る
3. **AAOI の YTD +441%（[二次] AOL/financefeeds）は 1.6T/800G の受注期待**。売上規模 $1.1B に対し時価 $10B 前後
4. 米国勢の 2026 年は「メモリから光へのローテーション」（[二次] startupfortune）で LITE/CIEN/GLW が S&P500 上位

### 判断ログ
- LITE 時価総額は $71.5B（financefeeds）と $93.8B（companiesmarketcap）が併存。10-K 表紙の 8,860万株（[二次]）×$1,085.42 ≒ $96B と整合する後者系を採用
- IPGP は「光」だが AI データセンター需要と無関係のため、ユニバース参照のみで深掘りしない
- Web 取得回数: 検索 18 / Fetch 試行 6（全失敗）

### 出典（R1）
- https://www.quiverquant.com/news/Lumentum+Q4+Revenue+Tops+$1+Billion+As+GAAP+Loss+Hits+$7.2+Billion
- https://www.stocktitan.net/sec-filings/LITE/8-k-lumentum-holdings-inc-reports-material-event-21905826e626.html
- https://www.stocktitan.net/sec-filings/LITE/10-k-lumentum-holdings-inc-files-annual-report-f824191929b3.html
- https://www.tradingview.com/news/zacks:2edbf68f8094b:0-lumentum-q4-earnings-call-focuses-on-ai-optics-ocs-npo-ramps/
- https://companiesmarketcap.com/lumentum/marketcap/ / https://stockanalysis.com/stocks/lite/forecast/
- https://247wallst.com/investing/2026/10/01/coherent-jumps-10-on-photonlink-push-and-bernsteins-outperform-start-lumentum-rises-9-corning-advances-3/
- https://finance.yahoo.com/markets/stocks/articles/applied-optoelectronics-inc-aaoi-q2-050943160.html
- https://futurumgroup.com/insights/coherent-q4-fy-2026-earnings-1-6t-transceivers-ramp-cpo-revenue-approaches/
- https://finance.yahoo.com/markets/stocks/articles/fabrinet-fn-q4-2026-earnings-050212828.html
- https://finance.yahoo.com/markets/stocks/articles/ciena-reports-fiscal-third-quarter-110000064.html
- https://convergedigest.com/corning-optical-communications-sales-jump-32-on-ai-data-center-demand/
- https://www.alphaspread.com/market-news/earnings/credo-technology-reports-record-fiscal-q1-revenue-of-479-million-guides-for-further-growth
- https://financefeeds.com/lumentum-coherent-ciena-corning-ai-optics-2026/
- https://finance.biggo.com/news/2b25909c-bd1d-49fd-8c51-a9c7996700d5
- https://supplychainsignals.substack.com/p/optical-module-supply-chain-weekly
