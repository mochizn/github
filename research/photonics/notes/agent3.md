# agent3 ノート（米国株＋台湾・中国参考）

## 最新の要点（R6 終了時, 2026-10-05）
- R6: **REPORT §2 米国株部分の完成文素材**を下の「§2 用の完成文（米国株）」に用意（agent5 へ）。訂正の伝播を grep → REPORT §2.2 の COHR 予想PER が ⚠ のまま（正: 約35倍）等を board/requests/agent3-6-1.md で agent5 に依頼。他は訂正済みの値が使われている
- CIEN 確定: 1億4,190万株 → **時価 $53.8B**、長期借入 $3.23B・現金 $2.8B → 純負債 約$0.4B、**EV $54.2B**、EV/ガイド年率売上 7.7倍
- stocks/MRVL.md 新規: $273.04・時価 $238.9B、FQ2'27 売上 $2.74B（+37%）・GM 58.9%、FY28 売上見通し $18B、FY28 EPS $6.75 → PER 約40倍（光関連の中で割高）、光 DSP は売上の約8%（agent1）
- 新規出典 約8 / 新規主張 約25 / 次ラウンド: agent4 の照合結果の反映、REPORT §2 素材の修正対応、最終ラウンドに向けた全カードの数値の最終確認（✔/⚠ タグの付け直し）

## §2 用の完成文（米国株）— agent5 が REPORT §2 にそのまま使える素材（R6, 2026-10-05）
（数値はすべて [二次]、基準日 2026-10-02 終値。倍率は agent3 の計算 [推測]。詳細は stocks/_US_COMPARE.md と各カード）

### 2.x 米国株: 光チップを持つ会社に利益が集まり、株価もそれを織り込んでいる
米国の光関連銘柄は、バリューチェーンの位置によって3つに分けられる。

**(1) 光チップ（InP レーザー）を自社で作る会社 — Lumentum（LITE）、Coherent（COHR）**
AI データセンター向けの EML・CW レーザーは供給が需要に追いつかず、Lumentum は「200G EML は完売、価格は旧世代の約2倍」と報じられている。この希少性は利益率に表れ、Lumentum の調整後粗利率は 50.4%（FY26 Q4）と初めて 50% を超え、売上は前年比 +109% だった。Coherent は同じ InP レーザーを持つが、トランシーバの組立と産業用レーザーの比重が高く、粗利率は 40.2%、売上の伸びは +34%（売却事業を除くと +42%）にとどまる。
株価の織り込みは Lumentum が突出している。希薄化後の企業価値（EV）約 $1,069億は、次四半期ガイダンスを年率にした売上の約21倍、営業利益の約53倍で、Coherent（7倍、33倍）の約1.6倍のプレミアムがつく。2026年3月には NVIDIA が両社に $20億ずつ出資し、複数年の購入を約束した。需要の下支えになる一方、両社とも上位顧客への依存は大きい（Lumentum は上位2社で売上の 42%）。

**(2) 組立・受託製造 — AAOI、Fabrinet（FN）**
組立の層は売上倍率が低い（EV/年率売上 3〜9倍）が、利益率も低い（AAOI の粗利率 約30%、Fabrinet 約12%）。AAOI は自社レーザーを持つ米国内生産のトランシーバメーカーで、2026年の売上を約 $11億（前年の約2.4倍）と見込むが、足元の利益はほぼゼロで、2026年だけで3回の株式売出し（ATM、計 $17億枠）を行っている。株価は 2027年の利益が急増するという予想（PER 約25倍）にかかっており、上位2社で売上の 8割超を占める顧客集中と、2017年に大口顧客の発注減で株価が −63% となった前例がある。Fabrinet は黒字・無借金（純現金 $8.8億）で顧客も分散しており（上位4社で 57%）、組立層の中では質が高い。CPO（光電融合パッケージ）への移行では、プラガブル・モジュールの組立は付加価値を失う側になりうる。

**(3) システム・電気側の半導体・ファイバ — Ciena（CIEN）、Marvell（MRVL）、Broadcom（AVGO）、Corning（GLW）**
この層は光の比率が低いか、データセンター内の CPO と別の領域にいる。Ciena はデータセンター間の光伝送装置で、受注残 $85億（年間売上の約1.3倍）が業績の見通しを支える。Marvell と Broadcom は光トランシーバの DSP を2社で寡占するが、光は全社売上の 2〜8% にすぎず、株価は AI 向けカスタム半導体で決まる。Corning は光ファイバ・ケーブルで、光通信部門が売上の約44%を占める。2028年度のコンセンサス利益で見ると、Broadcom の PER は約14倍と最も低く、Coherent 約24倍、Lumentum 約31倍、Corning 28〜35倍、Marvell 約40倍が続く。

**米国株の共通リスク**: 7銘柄すべてのベータが 1 を超え（AAOI 3.8、Marvell 2.3、Coherent 2.1、Lumentum 1.5 など）、2026年の下落は同じ時期に起きた（5〜7月に Lumentum −34%、8〜9月に Coherent −36%）。銘柄を分けても、ハイパースケーラの設備投資という共通の要因は消えない。

（表は stocks/_US_COMPARE.md §1〜§2 を REPORT §2.2 に転記してよい）

## ラウンド6（2026-10-05）
- 訂正の伝播チェック（grep: $7.61 / $95B / 19倍 / $56.7B / 104.4億元 / PhotonLink 10-01 / $71.5B 等）: stocks・REPORT の本文には残っていない。REPORT §2.2 の COHR「予想PER ⚠」は空欄の扱いなので値の記入を依頼。agent5 ノートの R1 採点メモ（COHR 時価 約$57B・LITE 約19倍・AAOI 日付不明）は履歴なので依頼のみ
- 判断: CIEN の時価総額は 10-Q の発行済株数（2026-08-01）× 株価で確定。$55.5B 系は希薄化後平均株数と判断
- 判断: MRVL は FY29 のコンセンサスが取れないため、FY28 EPS を中立の基準にした（2年後としては1年短い点を明記）
- 判断: REPORT §2 の素材は「位置で3分類」の構成にした（agent1 の利益プール表と整合）
- Web: 検索 6 / Fetch 0

## ラウンド5（2026-10-05）
- 依頼対応: agent4-4-1（COHR EPS 訂正、NVIDIA 出資は R4 で反映済み＋LITE 優先株の転換条件、PhotonLink 日付）、agent5-4-1（COHR FY28 EPS、FN FY28 EPS・純現金、GLW/AVGO のシナリオ値）、agent1-4-1（比較表に GLW/AVGO の EV を反映）→ board/requests/agent3-5-1.md
- 判断: シナリオの倍率（強気 25〜35倍 / 中立 20〜28倍 / 弱気 15〜20倍）は agent3 の仮置きと明記し、agent5 に置き換えを委ねる
- 判断: COHR の 10% 顧客比率は R4・R5 の2ラウンドで取れず → ⚠未確認で確定（PROTOCOL）
- 判断: CIEN の時価総額は表示が2種類（$50.61B / $55.50B）あり、どちらも採らず幅で記載
- Web: 検索 11 / Fetch 0

## ラウンド4（2026-10-05）
- 依頼対応: agent5-3-1（ボラ・ベータ、GLW/AVGO のデータ → 比較表の行で回答。カードは agent1 担当なので作らない）、agent4-3-1（NVIDIA 出資の確認 → LITE.md §2a・COHR.md §4b・比較表 §4、AAOI の A5/A6/A10/A12 を反映）→ board/requests/agent3-4-1.md
- 判断: 90日ボラは検索スニペットで取れないため、ベータ（対S&P）＋52週レンジ＋2026年最大下落で代用。ベータは対 SOX ではない点を明記
- 判断: GLW のコンセンサス EPS（$3.18 / $2.95）は Q3 ガイド年率 $3.48 と矛盾するため不採用、ガイド年率で PER を計算
- 判断: 「COHR が $2B の普通株を発行して需給悪化」という 247wallst の説明は、3月の NVIDIA 私募を指すと判断（新規公募は確認できず）
- 判断: AAOI の空売り比率は取得日不明のため比率決定には使わない（agent4 A12）
- Web: 検索 12 / Fetch 0

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
