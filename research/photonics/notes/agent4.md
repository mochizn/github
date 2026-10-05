# agent4 ノート（検証ゲート＋弱気担当）

## 最新の要点（R1, 2026-10-05）
- 検証チェックリスト C1〜C14 を作成（下記 §1）。**全員、銘柄カードを書く前に一読を**。特に C3 フジクラ 1:6 分割（基準日 2026-03-31）、C2 LITE/COHR は6月末決算、C6 AAOI は調整後指標と希薄化、C9 顧客集中。
- 一次資料（sec.gov / TDnet / EDINET / 企業IR）にはすべて到達できない。そこで ✔ の判定基準を「スニペット経由の原典URL＋独立した2ソースの一致」に置き換えた（§0、DECISIONS.md に追記）。
- テーマ全体の弱気シナリオ B1〜B8（§2）を書いた。最大のリスクは「ハイパースケーラ設備投資の2次微分（伸び率の鈍化）」。2000年型の全面崩壊より、**伸び率の鈍化だけで高PERが崩れる**シナリオの方が確率は高い。
- 新規出典 17 / 新規主張 22（すべて[二次]、[推測]は明記）
- 次ラウンド: 他者の銘柄カード（5803, 6834, LITE, AAOI が最優先）を §1 のチェックリストで照合して ✔/⚠/✘ を付ける。銘柄別の弱気シナリオに着手。中国モジュール禁止法案が LITE/COHR のレーザー売上（中国モジュールメーカー向け）に与える影響を確認する。

---

## §0 検証ゲートの運用（ラウンド1の決定）
- 環境では WebFetch/curl がほぼ全滅（ENV.md）で、使えるのは WebSearch の要約だけ。PROTOCOL 上の [一次] は事実上付けられない。
- そこで agent4 の判定は次のとおりとする（DECISIONS.md に追記済み）
  - **✔**: 要約の依拠先が原典URL（sec.gov、TDnet ミラーの短信PDF、企業IR）と明示され、数値が**独立した別クエリ／別ソースでもう1回一致**したもの。または、原典URLの要約1件に加えて内部整合チェック（前年比から逆算した前年値が別ソースと一致する等）に通ったもの
  - **⚠**: ソースが1件だけ、記事・ブログ・X のみ、日付・期間（会計年度）・単位のどれかが不明、または §1 のチェック項目が未確認
  - **✘**: 原典由来の数値と矛盾する、期間・定義の取り違え（例: GAAP と non-GAAP の混同、分割前後の混在）
- agent4 自身の主張も同じ基準で自己タグを付ける（下記はすべて [二次]。✔候補には「✔候補」と書く）

## §1 光関連株の検証チェックリスト（C1〜C14）

| # | 項目 | 何を誤りやすいか | 確認方法 / 具体例 |
|---|---|---|---|
| C1 | **「光関連売上比率」の定義** | セグメント名と光の売上は一致しない。フジクラの「情報通信事業」には光ファイバ・ケーブル・コネクタだけでなく電子部品やFPC関連（別セグメントなら除外）が入りうる。精工技研の「光製品関連」(54%)には通信用の光コネクタ研磨機・部品、データセンター以外（FTTH・CATV）も含まれる。AAOI の売上は CATV（Digicomm向け）とデータセンターの2本立て。※セグメントの中身は [推測]、各社のセグメント注記で要確認 | 比率を書くときは「セグメント名・定義・期間」を併記。「データセンター向け比率」は会社が開示していない限り [推測] |
| C2 | **会計年度ズレ** | LITE は6月下旬（52/53週）決算。FY2026＝2026-06-27 に終了した期 [二次: nasdaq.com 8-K要約, 2026-08-11]。COHR も6月期、AAOI は12月期、日本勢は3月期、Innolight/Eoptolink は12月期。「2026年度」を混ぜると最大9か月ずれる | 表の列は「FY表記＋期末日」で書く。四半期比較は暦四半期にそろえるか、ずれを注記する |
| C3 | **株式分割** | **フジクラは1株→6株に分割、基準日 2026-03-31**（2026-02-25 発表）[二次: kabutan.jp ニュース見出し, 検索要約]。EPS・BPS・DPS・株価の過去推移は分割前後が混在しやすい。2026/3期の短信は分割後ベースのはず（要確認）。古い記事の「目標株価」「1株配当」は分割前の数値 | 1株指標には「分割調整後/前」を明記。PER は時価総額÷純利益で再計算して突き合わせる。JDSU のような長期チャートの「分割調整後高値 $1,227」も同じ注意が要る |
| C4 | **為替** | 円建てとドル建ての比較、日本企業の海外売上の円安効果（数量成長と為替要因の分離）。台湾ドル・人民元建ての中国勢 | DECISIONS の USD/JPY=157.8（2026-10-02）を使う。日本勢の増収率は「為替影響を除くと何%か」を会社が開示していれば併記 |
| C5 | **調整後指標（non-GAAP）** | LITE の Q4 FY26 は GAAP 営業利益率 27.8% / non-GAAP 36.6%、粗利率も GAAP 47.4% / non-GAAP 50.4% [二次: 8-K EX-99.1要約・X投稿, ✔候補]。差は約9pt と大きい（株式報酬・買収無形資産償却・リストラ等）。ガイダンスは non-GAAP しか出ていない | PER を計算するときは GAAP か non-GAAP かを明記。「PER 30倍」と「GAAP PER 146倍」は同じ株の別の数字（§2 B7 参照） |
| C6 | **希薄化・株数** | AAOI は最大 $600M の ATM（2026-08 の424B5）。発行済株式数 84,906,289株（2026-08-20時点）、例示では 4,647,561株を $129.10 で発行 [二次: sec.gov 424B5 要約]。転換社債（2030年満期 2.75%、$125M）もある。目論見書にある「1株当たり $102.90 の希薄化」は簿価ベースの数字で、経済的な希薄化（約5.5%）とは別物 | 時価総額は最新の10-Q表紙の株数×株価で計算し、ATM 実行分を足す。EPS は希薄化後株数で |
| C7 | **バリュエーションの基準日** | 2026年の光関連株は1日で10〜17%動く局面が複数あった [二次: 247wallst 2026-06-23 / 07-02 / 07-28 / 08-10 / 09-29]。基準日がずれると PER が2割変わる | DECISIONS の基準日 2026-10-02 終値にそろえる |
| C8 | **トレーリング vs フォワード** | 成長株では TTM PER と次期予想 PER が数倍違う（LITE は TTM 146倍の報道がある一方、Q1 FY27 ガイド中央値の non-GAAP EPS $4.20×4＝年率 $16.8 で見れば水準はまったく違う） | どちらの PER かを必ず書く。「年率換算」は [推測] と明記 |
| C9 | **顧客集中** | LITE: FY25 は上位2社で 16.0%/15.4%、**FY26 は 26.6%/15.0%（計41.6%）**、売掛金では1社が30.4% [二次: sec.gov 10-K 要約, sec-api.io]。AAOI: FY2025 は Digicomm 53.1%（CATV）＋Microsoft 28.8%＝81.9%、上位10社で 96.6% [二次: sec.gov 10-K 要約] | 「Customer A」が誰かは10-Kに書いていない。NVIDIA と断定するのは [推測]。AAOI の DC 売上はほぼ1社に依存 |
| C10 | **前年比の母数効果** | Eoptolink +189%、LITE +83% など、低い基数からの伸び率。前年が在庫調整の底なら伸び率は過大に見える | 2〜3年前（2023年）比もあわせて見る |
| C11 | **市場シェアの定義** | 「Innolight＋Eoptolink で 800G の60%」は NVIDIA 向けなのか市場全体なのか、数量なのか金額なのかがソースによって違う [二次: photoncap, LightCounting 要約] | シェアの数字は「母集団・単位・年・出典」をセットで。LightCounting の本文は有料で読めないので要約は ⚠ |
| C12 | **受注・バックログ・「引き合い」** | 「受注残」「長期供給契約（LTA）」「前受金」「顧客の能力予約」は意味が違う。日本企業の「引き合い旺盛」は数値ではない | 開示された数値（受注高・受注残）だけを主張にする |
| C13 | **同名・類似ティッカーの混同** | COHR（現 Coherent＝旧 II-VI）と旧 Coherent Inc.、LITE（JDSU から分離）と VIAV、Innolight＝中際旭創（300308）と光迅科技（Accelink, 002281）の混同 | 正式社名とコードを併記 |
| C14 | **見通しの主体** | 「2026年の設備投資 $7,250億」などは調査会社・ブログの集計で、会社の公式ガイダンスとは違う。集計範囲（4社か5社か、ファイナンスリースを含むか）で $4,340億〜$8,000億まで幅がある [二次: factset, siliconanalysts, valueaddvc] | 会社別の公式ガイダンス（決算発表）と第三者集計を分けて書く |

## §2 光関連テーマ全体の弱気シナリオ（レッドチーム）

### B1. 2000年の光バブルとの比較 ― 何が同じで何が違うか
- **当時の事実** [二次]
  - JDSU は FY2001（2001年6月期）に純損失 $561億を計上し、うち $448億がのれん償却・減損。当時の米企業として史上最大の損失 [二次: sec.gov 8-K(2001-07-26) 要約, washingtonpost 2001-07-27, ✔候補（2ソース一致）]
  - JDSU 株は2000年3月の高値から約99%下落、Nortel もピーク（時価総額 $2,500億超）から2002年10月までに約99%下落、Corning は $110 → 2002年8月に $2 未満 [二次: CNN Money 2003-05-13, lightreading ほか。下落率は ⚠（ソースによって90%/99%と異なる）]
  - Corning の売上は2000年の $70億 → 2002年の約 $30億 [二次: CNN Money 2003]
- **同じ点**: (1) 需要が少数の大口顧客の設備投資に依存（2000年は通信キャリアとCLEC、今はハイパースケーラ4〜5社）。(2) 顧客が外部から資金調達して投資するようになっている。2000年は CLEC の高利回り債、今はハイパースケーラの社債・リース・プリペイ [二次: factset「Hyperscalers Tap External Financing」]。(3) 部品メーカーの能力増強（中国勢のタイ第2期、InP レーザー増産）が需要のピークと重なると在庫が積み上がる（ダブルオーダー）。(4) TTM PER が100倍超（LITE 146倍、COHR 160〜189倍）[二次: 247wallst / yahoo 2026-07〜08]
- **違う点（強気側の反論として公正に記録）**: (1) 顧客のハイパースケーラは本業の黒字が大きく、2000年の CLEC のような破綻リスクは低い。(2) 当時のファイバは「敷設後も使われない（ダークファイバ）」余剰だったが、今の GPU クラスタ向けの光は稼働率が高いとされる。(3) JDSU の損失の大半は株式交換買収ののれんで、今の LITE/COHR の利益は営業キャッシュフローを伴っている
- **弱気の論点**: 違いがあるのは「顧客が倒産しない」という点だけで、**「顧客が発注を減らさない」ことは保証されていない**。設備投資が前年比で横ばいになるだけで、部品在庫の調整（2〜4四半期）で部品メーカーの売上が2〜5割落ちるのは、2001年・2019年（中国5G後）・2023年（光モジュール在庫調整）のサイクルで繰り返し起きている [推測：パターン認識。過去の具体的な下落率は R2 で検証する]

### B2. ハイパースケーラ設備投資の「2次微分」リスク（最重要）
- 2026年の主要4社の AI 設備投資は約 $7,250億（前年比+77%）、2027年に約1兆ドルという第三者集計がある [二次: valueaddvc, yieldtheory, ⚠ 集計範囲が不統一]。直近4四半期の設備投資 $4,339億に対し、減価償却は約 $1,490億 [二次: siliconanalysts]
- FY26 の FCF はアルファベットとマイクロソフト以外でほぼゼロかマイナス、という見方がある [二次: factset]
- **弱気のロジック**: 光部品の売上は設備投資の「水準」ではなく「伸び」に連動する（新設クラスタ向けが中心のため）。設備投資の伸び率が +77% から +20% に鈍化するだけで、光部品の需要成長率は大きく下がる。株価は成長率で評価されているので、売上が減らなくても株価は下がりうる [推測]
- 監視すべきトリガー: 各社決算の設備投資ガイダンス修正（下方修正、「2027年は抑制」発言）、減価償却の伸びが営業利益の伸びを上回る、外部資金調達のスプレッド拡大

### B3. 価格下落（ASP エロージョン）
- 通信用・データセンター用トランシーバの ASP は世代ごと・年ごとに下がるのが通常（年8〜15%）。800G は2023年の約 $1,200 → 2025年に $600〜800、2026年に約 $400 という業界ブログの数字がある [二次: hytoptodevice / link-pp ブログ、⚠ 信頼度は低い]
- 2025〜26年は供給制約（EML・InP 基板・DSP）で価格が下がりにくかったと考えられる。供給が追いつく（中国勢の増産、InP の増産）と、その分の価格の上乗せが一気に剥がれる [推測]
- 特に中国勢の上位2社（Innolight 2025年売上 $53億、Eoptolink $35億）[二次: LightCounting 要約] は規模でコスト競争力があり、米国の禁止措置でも米国外の需要では価格の基準になる

### B4. 顧客集中
- LITE は FY26 の上位1社比率が 26.6%（FY25 の 16.0% から上昇）、上位2社で 41.6% [二次: sec.gov 10-K 要約]。AAOI は Microsoft 1社で 28.8%、DC 事業はほぼ Microsoft 頼み [二次: sec.gov 10-K 要約]
- 1社の世代交代・内製化・2社購買化・在庫調整がそのまま業績の崖になる。2010年代の AAOI は Amazon 依存の解消（2017〜18年）で売上と株価が急落した前例がある [推測（記憶ベース）→ R2 で検証]

### B5. CPO による構造変化（プラガブル→CPO）
- NVIDIA は GTC 2025 で CPO スイッチ（Quantum-X Photonics＝IB、Spectrum-X Photonics＝Ethernet）を発表した。Spectrum-X Photonics は2026年下期から出荷予定で、「レーザー数1/4、電力効率3.5倍」とされる [二次: nvidianews 要約, storagereview。「full production」の報道あり、⚠ 量産規模は不明]
- **敗者になりうる層**: プラガブルモジュールの組立（AAOI、中国勢のモジュール事業、Fabrinet の一部）。CPO では光エンジンがスイッチ ASIC と同じパッケージに入り、付加価値が TSMC（COUPE）、ASIC ベンダー、外付けレーザー光源（ELS）、ファイバ配線・コネクタに移る
- **注意**: 「レーザー数1/4」はモジュール内蔵 EML の数が減るということで、LITE のような EML/CW レーザー供給者にとっては**数量が減る**ことを意味しうる（高出力 CW レーザー1個の単価上昇で相殺されるかは未確認）[推測]
- 一方でフジクラ・精工技研などファイバ・コネクタ系は、CPO で光ファイバの本数と高密度コネクタの需要が増えるので相対的に有利、という見方が多い。ただしその**有利さはすでに株価に織り込まれている可能性**がある（フジクラ 2026/3期 ROE 32.5% [二次: 検索要約]）
- タイミングのリスク: CPO の本格普及が遅れても早まっても、どちらも誰かの株価を壊す（2026年に「CPO タイムライン懸念」で光関連株が下落した報道あり [二次: tikr]）

### B6. 中国勢・地政学
- 世界の光モジュール上位10社のうち7社が中国勢で、Innolight と Eoptolink で 800G 以上の60%超 [二次: photoncap、⚠ 定義不明（C11）]。Innolight は売上の90%超が輸出、Q1 2026 は61.7%が米国向け [二次: photoncap]
- 米国側の動き: 米政府による中国製光モジュールの禁止草案（Caixin 2026-08-05）、国防総省の1260Hリストに Innolight を追加（2026-06）、上院の超党派法案（2026-09-25、連邦政府システムでの中国製トランシーバ使用禁止）[二次: caixinglobal, photoncap, biggo、✔候補（複数ソース）]
- **両方向に効く点に注意**: (1) 米国・日本のモジュール勢（AAOI など）にとっては追い風。(2) 一方で、中国モジュールメーカーは LITE・COHR などの米国製 EML/レーザーや DSP の大口顧客で、禁止の応酬（中国側の報復、InP・ガリウム・ゲルマニウムなどの材料輸出規制）は米部品メーカーにとって逆風。「中国排除＝米国勢の純増」という単純な強気論は ✘ 寄り [推測、R2 で LITE の中国向け売上比率を確認する]
- 関税: 中国勢はタイ・メキシコの工場経由で米国に出荷しており、光モジュールは半導体カテゴリで関税が免除されている [二次: semisino/photoncap]。免除が取り消されれば価格・供給の両面でショック

### B7. バリュエーションの織り込み
- LITE の TTM PER 146倍、COHR 160〜189倍（2026-07〜08 報道）、両社とも2026年の年初来で+100%超 [二次: 247wallst / yahoo]。基準日 2026-10-02 での再計算は agent3 に依頼する
- LITE の Q1 FY27 ガイダンスは売上 $12.25〜12.75億、non-GAAP 営業利益率 39.5〜40.5%、non-GAAP EPS $4.05〜4.35 [二次: 8-K 要約・X投稿, ✔候補]。年率換算で売上約 $50億・EPS 約 $17 [推測]。FY26 通期の売上は $30.1億（+83%）[二次: sec-api.io]
- **弱気の論点**: 足元の四半期の売上を年率換算して倍率を当てはめる評価は「ピーク利益×ピーク倍率」の典型。部品サイクルのピークでは PER が最も低く見えるので、低 PER を割安の根拠にしない
- AAOI は $6億の ATM 発表で1日に-12%（2026-08-24）[二次: 247wallst]。成長資金を株式で調達し続ける構造で、1株価値は希薄化する

### B8. その他の弱気要因（R2 以降で深掘り）
- 銅（DAC/AEC）の延命: ラック内の接続は銅が想定より長く残り、光の浸透が遅れる可能性
- LPO/LRO の普及で DSP 込みのモジュール単価が下がる（利益プールが縮む）
- 日本勢: 円高に戻るリスク（157.8円は歴史的な円安水準）。フジクラの利益は北米 DC 向けが中心とされ、円が15%上がると円建て利益も約15%目減りする [推測]
- 電力制約で DC の稼働が遅れる → 光の発注が後ずれする

## 出典（R1, 取得 2026-10-05, すべて WebSearch 要約経由）
1. JDSU FY2001 8-K: https://www.sec.gov/Archives/edgar/data/0000912093/000091209301500022/form8kex99b_072601.htm
2. Washington Post 2001-07-27: https://www.washingtonpost.com/archive/business/2001/07/27/write-downs-give-jds-506-billion-loss-record-for-a-us-firm/6b2cbb8c-d731-4984-b8b0-5ad1d886eea9/
3. CNN Money (Corning) 2003-05-13: https://money.cnn.com/2003/05/13/pf/investing/corning/
4. Light Reading (Nortel): https://www.lightreading.com/optical-networking/the-decline-fall-of-nortel-networks
5. LITE 10-K FY2025: https://www.sec.gov/Archives/edgar/data/1633978/000162828025040830/lite-20250628.htm
6. LITE 10-K FY2026: https://www.sec.gov/Archives/edgar/data/0001633978/000162828026057358/lite-20260627.htm , https://sec-api.io/insights/financial-analysis-of-lumentum-fiscal-2026
7. LITE Q4 FY26 8-K EX-99.1: https://www.sec.gov/Archives/edgar/data/0001633978/000162828026055726/lite_ex991xq4fy26.htm , https://www.nasdaq.com/press-release/lumentum-announces-fourth-quarter-and-full-fiscal-year-2026-results-2026-08-11
8. AAOI 10-K FY2025: https://www.sec.gov/Archives/edgar/data/1158114/000143774926005875/aaoi20251231_10k.htm
9. AAOI 424B5 (2026-08): https://www.sec.gov/Archives/edgar/data/0001158114/000110465926099685/tm2623389-1_424b5.htm
10. NVIDIA CPO: https://nvidianews.nvidia.com/news/nvidia-spectrum-x-co-packaged-optics-networking-switches-ai-factories , https://www.storagereview.com/news/nvidia-spectrum-x-ethernet-photonics-enters-full-production-with-4x-fewer-lasers-and-a-five-vendor-cpo-supply-chain
11. LightCounting 2026-05: https://www.lightcounting.com/newsletter/en/may-2026-optical-vendor-landscape-376
12. photoncap (中国勢シェア): https://photoncap.net/p/chinese-optical-modules-own-7-of
13. Caixin 2026-08-05: https://www.caixinglobal.com/2026-08-05/us-drafts-ban-on-chinese-optical-modules-exposing-mutual-supply-chain-risks-102471268.html
14. フジクラ 1:6 分割: https://kabutan.jp/news/marketnews/?b=n202602250754 ／ 2026/3期短信ミラー: https://finance-frontend-pc-dist.west.edge.storage-yahoo.jp/disclosure/20260514/20260514532598.pdf
15. 精工技研 2026/3期短信ミラー: https://finance-frontend-pc-dist.west.edge.storage-yahoo.jp/disclosure/20260514/20260512527161.pdf
16. 設備投資: https://insight.factset.com/hyperscalers-tap-external-financing-as-ai-capex-outruns-cash-flow , https://siliconanalysts.com/analysis/hyperscaler-ai-capex-depreciation-wall-2026 , https://valueaddvc.com/blog/big-tech-ai-capex-in-2025-microsoft-google-meta-amazon-and-the-spending-race
17. 光関連株の急落報道: https://247wallst.com/investing/2026/07/28/coherent-sinks-11-applied-optoelectronics-falls-10-lumentum-drops-9-as-traders-question-ai-spending-spree/ , https://247wallst.com/investing/2026/08/24/applied-optoelectronics-sinks-12-on-600m-equity-offering-lumentum-and-coherent-drop-5/ , https://www.tikr.com/blog/widespread-ai-photonics-selloff-drags-down-lumentum-stock
- ASP（信頼度低）: https://www.hytoptodevice.com/blog-detail/800g-optical-modules-where-is-the-market-heading-a-2026-deep-dive

## 参考メモ（他担当向けに確認済みの数値。[二次]・⚠ 単独ソース）
- フジクラ 2026/3期: 売上 1兆1,824億円（+20.7%）、営業利益 1,887億円、純利益 1,572億円（短信ミラーの要約）→ agent2 のカードと突き合わせる
- 精工技研 2026/3期: 売上 300.9億円（+50.6%）、営業利益 77.3億円（+174.5%）、純利益 62.1億円。光製品関連 54% / 精機関連 46%
