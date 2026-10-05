# agent3 ノート（米国株＋台湾・中国参考）

## 最新の要点（R1 終了時, 2026-10-05）
- 米国一次資料（SEC/IR/主要金融サイト）は全滅 → 全数値 [二次]（検索スニペット）。agent4 の照合も同条件になる点に注意（ENV.md 追記済み）
- 米国ユニバース 22銘柄＋台中参考 8銘柄を作成（下表）。光エクスポージャ高: LITE/AAOI/COHR/CIEN/FN/POET/AXTI
- LITE: FY26 売上 $3.01B(+83%)、Q4 $1.01B(+109%)、Non-GAAP GM 50.4%、Q1FY27 ガイド $1.25B 中央値。株価 $1,085(10/02)、FY27予想PER 約50倍・EV/年率売上 約19倍。上位2顧客 42%
- 新規出典 約20 / 新規主張 約35 / 次ラウンド: AAOI カード、LITE の未確認項目（地域別・転換社債残高・逆算DCF）、COHR カード着手
- 依頼: board/requests/agent3-1-1.md（@agent4 LITE 主要主張の照合）

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
| AAOI | Applied Optoelectronics | 垂直統合トランシーバ（自社レーザー）、CATV | H | Q2'26 $191.9M(+86%)、DC $107.7M、CATV $80.6M。2026年売上 約$1.1B 見通し、Q4 1.6T $70M超 | $9.8B（日付不明⚠） | ◎ R2 |
| COHR | Coherent | トランシーバ最大手級、InP/VCSEL/SiPh、6インチInP | H(DC&Comm 79%) | FY26 $7.12B +23%、Q4 $2.05B、Q1FY27 ガイド $2.2〜2.4B、PhotonLink 発表 | $56.7B（日付曖昧⚠）、株価$315(10/01) | ◎ R2-3 |
| FN | Fabrinet | 光モジュールEMS（NVIDIA/Cisco 等） | H | FY26 $4.6B +36%、Q4 $1.316B。顧客 Cisco20%/NVIDIA16%/Nokia11%/Amazon11% | $16.6B（10/04, 5月は$24.6B ⚠） | ○ |
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

台湾・中国（参考、競合として）:
| コード | 社名 | 位置 | メモ [二次] |
|---|---|---|---|
| 300308.SZ | Zhongji Innolight（中際旭創） | 800G/1.6T トランシーバ世界首位級 | 1H26 売上 417.8億元(+182%)、純利益 136.5億元(+242%) https://finance.biggo.com/news/2b25909c-bd1d-49fd-8c51-a9c7996700d5 |
| 300502.SZ | Eoptolink（新易盛） | トランシーバ（LPO/SiPh 強い） | 1H26 売上 104.4億元(+283%)、純利益 39.4億元(+356%) 同上系 |
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
