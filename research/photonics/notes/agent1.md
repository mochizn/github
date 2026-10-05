# agent1 ノート（業界・技術）

## 最新の要点（R3, 2026-10-05）
- **設備投資（§R3-1）**: 米4社の四半期設備投資は 2026Q2 に**1,712億ドル（前年比+79%）**、2025年計4,126億ドル（報道値約4,100億ドルと一致 ✔内部整合）。2026年ガイダンス中央値 合計約7,475億ドル → 2026年下期は四半期約2,220億ドルへ加速が必要。**2027年コンセンサス約9,345億ドルは前年比+25%で、伸び率は+70%台から急減速**＝光株にとっての「2次微分」リスクの時期は2027年
- **過去サイクル（§R3-2）**: 業界売上の落ち込みは 2019年 -18%（イーサネット光トランシーバ、史上最大）、2023年 約-1%（Ethernetは-10%）と意外に小さいが、**利益は大きく崩れる**（LITE 営業利益率 FY22 30.8% → FY24 2.8%）。2001-02年は桁違い（JDSU 売上 -66%）
- **供給追いつき時期（§R3-3, agent5-2-2回答）**: EML/CWレーザー・ファイバとも「2028年に新能力が立ち上がる」が各社計画の共通項。**2028年は「供給増」と「設備投資の伸び率鈍化」が重なる最大の警戒期**。平常期マージン: LITE 粗利40〜45%/営業15〜20%、COHR 粗利36〜40%、Corning光通信 純利益率10〜14%（現在21%）
- **R採点案（§R3-4）**: 5点＝AVGO, TSM, GLW, santec(6777)。2点＝AAOI, CRDO, MRVL, エンプラス(6961)。DSP/SerDes勢は「2026-28年の勝者、2029年以降に侵食リスク」。CRDO（銅AEC）は**光の普及が遅れた場合のヘッジ**になる
- 新規出典 約25 / 新規主張 約40（[二次]、計算・採点は[推測]）/ 次ラウンド: トランシーバBOM（DSP・レーザー比率）の出典付き数値、フジクラ情報通信の過去マージン（agent2 に依頼）、2027年設備投資コンセンサスの別ソース確認

## R2 要点（アーカイブ）
- **利益プール（§R2-1）**: 直近四半期の粗利率は TSMC 67.7% > Arista 63.4% > Marvell 58.9% > Lumentum 50.4% > Eoptolink 48.5% ≈ Innolight 46% ≈ Ciena 46.4% > Coherent 40.2% > AAOI 29.8% > Fabrinet 12.2%。**中国2強の純利益率(33〜36%)は Coherent の営業利益率(21.8%)を上回る** → 「モジュール組立＝低収益」は現時点では誤り。利益は「規模＋1.6T先行＋内製SiPh」を持つ組立大手にも溜まっている
- **CPOの侵食試算（§R2-3）**[推測]: CPOはまずスイッチ側だけを置き換えるため、トランシーバ数量の減少は「CPO比率×約50%」が上限。2028年にスケールアウトのCPO比率10〜30%なら数量減は5〜15%程度で、スケールアップ光化の新規需要が相殺し得る。本当の侵食はNIC/GPU側もCPO化する2029年以降。最も確実に失うのはDSP（スイッチ側で100%不要）
- **中国・関税（§R2-4）**: FCCの最終規則（2026-09-11官報）は光モジュールを個別指定せず、Innolight/Eoptolink/TFCは対象外 → 「全面禁止」シナリオは一旦後退。残るリスク: 上院の連邦調達禁止法案（5年猶予）、国防総省1260HリストへのInnolight追加（2026/6）、中国のInP輸出規制（6インチウエハ価格+250%）
- ロードマップ時期表を agent5 向けに作成（§R2-2）。agent5-1-1 の1・2は回答済み（board/requests/agent1-2-1.md）。依頼3（四半期設備投資表）・5（過去サイクル）・6（R採点）は R3
- 新規出典 約25 / 新規主張 約30（[二次]、試算は[推測]）/ 次ラウンド: ハイパースケーラ四半期設備投資表、過去サイクル比較、ロードマップ耐性 R の採点案

## R1 要点（アーカイブ）
- 環境: 直接取得は全滅、WebSearch 要約のみ → 数値は原則 [二次]（✔基準は DECISIONS.md の agent4 基準をリーダーが正式採用。R1要点で触れた board/issues/agent1-1-1.md は作成していない＝agent4 基準と重複のため取り下げ）
- 利益の溜まり場（R1仮説）: InPレーザー・DSP・CPO光エンジン＋先端パッケージ・ファイバ/コネクタ
- ロードマップ: 2026=1.6T元年＆CPO量産初期、本格拡大2027-28、スケールアップ光化2028（Feynman）
- 需要起点: 米4社設備投資 2026年 約7,600億ドル

---

## R1 作業ログ
- 2026-10-05 ENV.md 作成（curl 48ドメイン、WebFetch 13ドメイン、WebSearch 多数で確認）。詳細は ENV.md
- 判断: [一次] が取得不能なため、WebSearch 要約で原典（sec.gov / 会社IR / 決算短信PDF）のURLが示され数値が要約されたものは「[二次]（原典URL=…）」と書く。agent4 の照合も同じ手段になるので、別クエリ・別ソースでの再現を ✔ の条件にするのが現実的
- WebSearch 要約の品質注意: 業者ブログ（c-light, 100gmodules, ascentoptics 等）の数値は出所不明が多く、価格データは特に信頼度低（[二次・低]と付記）

---

## バリューチェーン全体マップ（R1版）

### 0. 需要起点: ハイパースケーラ設備投資
| 項目 | 値 | タグ/出典 |
|---|---|---|
| 米4社(AMZN, MSFT, GOOGL, META) 2026年設備投資合計 | 約7,600億ドル（Q2決算後）。Q2前の集計は約7,250億ドル | [二次] https://www.statista.com/chart/35046/capital-expenditure-of-meta-alphabet-amazon-and-microsoft/ , https://aiweekly.co/alerts/amazon-microsoft-alphabet-meta-plan-725b-ai-capex-in-2026 |
| 同 2025年実績 | 約4,100〜4,130億ドル | [二次] 同上 |
| Alphabet 2026年ガイダンス | 1,950〜2,050億ドル（Q2で1,800〜1,900億ドルから上方修正、Q2単体449億ドル） | [二次] https://www.cnbc.com/2026/07/22/google-earnings-q2-goog-live-updates.html |
| Amazon 2026年 | 約2,200億ドル見通し（メモリ価格上昇も要因） | [二次] https://www.cnbc.com/2026/07/30/amazon-amzn-q2-earnings-report-2026.html |
| Meta 2026年 | 1,300〜1,450億ドル（下限を引上げ） | [二次] https://valueaddvc.com/blog/meta-145b-ai-capex-2026-why-zuckerberg-raised-guidance-twice |
| Microsoft | 4月以降ガイダンス据え置き（※会計年度6月末。暦年換算に注意） | [二次] cnbc 同上 |
| 2027年 4社合計 | コンセンサス 約9,300億ドル、Evercore/BofA は1兆ドル超を想定 | [二次] https://valueaddvc.com/blog/big-tech-ai-capex-in-2025-microsoft-google-meta-amazon-and-the-spending-race |
- 示唆[推測]: 光部品は設備投資のうちネットワーク比率（一般に数%〜1割程度と言われるが未確認）に連動。GPU/ASIC1基当たりの光トランシーバ本数（アタッチレート）が上昇しているため、設備投資成長率以上に光が伸びる局面。逆に設備投資の「伸び率鈍化」は光銘柄に先行的に効く（R2で過去サイクル=2001年・2018-19年と比較）

### 1. バリューチェーン（上流→下流）
```
[材料]           InP基板・GaAs基板 / 光ファイバ用プリフォーム / シリコンウエハ(SOI)
   ↓
[光チップ]       EML・DML・CWレーザー(InP) / VCSEL(GaAs) / PD / シリコンフォトニクスPIC(変調器・導波路)
   ↓            ＋ 電気IC: PAM4 DSP / ドライバ / TIA （LPOではDSP省略）
[光サブアセンブリ/光エンジン]  TOSA/ROSA、CPO用光エンジン（PIC+EIC 3D積層）、外部レーザー光源(ELS/ELSFP)
   ↓
[モジュール/システム] プラガブル光トランシーバ(800G/1.6T/3.2T) / AEC(銅) / CPOスイッチ / OCS(光回線スイッチ) / DCI・コヒーレント
   ↓
[配線]           光ファイバ・ケーブル、MPO/MTコネクタ・フェルール、シャッフル/パネル
   ↓
[顧客]           NVIDIA・Broadcom(スイッチ/GPUシステム) → ハイパースケーラ / ネオクラウド
横断: 製造装置・検査（研磨機、アライメント、ウエハプローバ、光測定器）、受託製造(EMS: Fabrinet等)、先端パッケージ(TSMC, ASE/SPIL)
```

### 2. レイヤー別の主要プレイヤーと構造
| レイヤー | 主要企業（日=日本, 米, 中, 台 他） | 構造・ボトルネック | タグ/出典 |
|---|---|---|---|
| InP基板 | 住友電工(日), AXT(米), IQE(英) | 寡占 | [二次] Lumentum ELS関連の検索要約 https://semiengineering.com/lasers-are-the-heartbeat-of-the-optical-ai-data-center/ |
| EML/レーザー | Lumentum, Broadcom, 三菱電機(日) で EML 約72%。Lumentum単独50〜60%で200G/laneを量産出荷している唯一の供給者とされる | **需給ギャップ30%超**（Lumentum発言）。Lumentumは2025/12→2026/12でEML出力+50%超、Coherentは社内InP出力を2026末までに倍増・2027末にさらに倍増。TrendForce: EML+CW-DFB月産能力は2026年に約5,070万個へ倍増 | [二次] https://mlq.ai/news/lumentum-says-ai-laser-demand-exceeds-supply-by-more-than-30-as-inp-capacity-lags/ , https://xenospectrum.com/en/lumentum-inp-ai-optics-shortage/ |
| CW/外部レーザー(CPO用) | Lumentum(NVIDIA Spectrum-X Photonicsの主要レーザー供給者)、Coherent(400mW CWサンプル)、住友電工 ほか | CPOでもレーザーは外付け(ELS)で残る → **CPO移行でレーザー需要は消えない**。NVIDIA新世代は「レーザー数4分の1」との報道あり（1個当たり高出力化）→個数減・単価増 | [二次] https://www.storagereview.com/news/nvidia-spectrum-x-ethernet-photonics-enters-full-production-with-4x-fewer-lasers-and-a-five-vendor-cpo-supply-chain |
| PAM4 DSP | Marvell 約60%、Broadcom 30%超（合計9割超） | 2社寡占。1.6T向け3nm DSP。LPO/CPOはDSPを省くため長期的な侵食リスク | [二次] https://www.digitimes.com/news/a20260427PD210/broadcom-marvell-production-chips-cpo.html （要約経由、数値の原典は不明確→⚠） |
| シリコンフォトニクス製造 | TSMC(COUPE, 65nm EIC/PIC, SoIC-X 3D積層), Tower, GlobalFoundries, UMC(2026/7に12インチSiPh量産出荷) | 能力立上げに時間。先端パッケージはAIチップと奪い合い | [二次] https://www.trendforce.com/presscenter/news/20260727-13151.html , https://www.trendforce.com/news/2026/07/14/news-umc-announces-first-delivery-of-mass-produced-silicon-photonics-wafers-from-singapore-12-inch-fab/ |
| 光トランシーバ(モジュール) | 2025年出荷シェア: Innolight(中) 23.4%で1位、Coherent 約16%、Eoptolink(中)が2位浮上との報道。上位10社中7社が中国系。上位5社で約56% | 中国勢が組立で優位。Innolight 2026年1-6月 売上417.8億元(+182%)、純利益136.5億元(+242%)、Q1粗利率46%。Eoptolink Q1粗利率約49% | [二次] https://www.lightcounting.com/newsletter/en/may-2026-optical-vendor-landscape-376 , https://photoncap.net/p/chinese-optical-modules-own-7-of , https://finance.biggo.com/news/2b25909c-bd1d-49fd-8c51-a9c7996700d5 |
| 米国系部品/モジュール | Lumentum: FY26 Q4(2026/6期)売上10.1億ドル(+109% YoY)、非GAAP粗利率50.4%、営業利益率36.6%、FY27 Q1ガイド12.25〜12.75億ドル。Coherent: Datacenter & Communications セグメント FY26売上52.75億ドル(+40%) | 部品(レーザー)を内製する垂直統合型が高マージン | [二次] 原典URL=https://www.sec.gov/Archives/edgar/data/0001633978/000162828026055726/lite_ex991xq4fy26.htm , https://www.sec.gov/Archives/edgar/data/0000820318/000082031826000020/iivi-20260630.htm （WebSearch要約経由。詳細は agent3 のカードへ） |
| CPOスイッチ | NVIDIA(Spectrum-X/Quantum-X Photonics), Broadcom(TH5 Bailly 51.2T 限定出荷 → TH6-Davisson 102.4T、Meta/HPE/Nexthopにサンプル、広範供給は2026Q3前後), NTT(PEC-2, Broadcom+Accton協業) | NVIDIAのCPOサプライチェーン: TSMC(SiPh製造)、SPIL(パッケージ/テスト)、Lumentum(レーザーチップ)、TFC(中, レーザーモジュール組立)、Foxconn(最終組立)、Coherent/Corning も協業。ボトルネック=光エンジン歩留まり・SiPh能力・先端パッケージ | [二次] https://www.trendforce.com/presscenter/news/20260727-13151.html , https://www.servethehome.com/broadcom-tomahawk-6-davisson-102-4t-switch-with-co-packaged-optics-shipping/ , https://optics.org/news/nvidia-reveals-plan-to-scale-ai-factories-with-co-packaged-optics |
| OCS(光回線スイッチ) | Lumentum(R64 MEMS、2026年末に四半期約1億ドルを目標と報道), Coherent(LCoS、Google/Oracleから3億ドル超受注、2026年に約3,000台), Huber+Suhner。Googleは内製から外部調達へ | Cignal AI: OCS市場 2030年に80億ドル超へ上方修正（2025/12時点は2029年25億ドル超） | [二次] https://cignal.ai/2026/07/ocs-market-to-top-8-billion-by-2030/ |
| 光ファイバ・ケーブル | Corning(米), フジクラ(日), 住友電工(日), 古河電工(日), Prysmian, YOFC(中) | **供給制約**: プリフォーム増設は18〜24ヶ月、フジクラの有意な増設は2028年との報道。Blackwell 72GPUノードは従来クラウドラック比16倍のファイバ | [二次] https://www.fierce-network.com/broadband/major-fiber-vendors-strategize-huge-demand-ai-2026 , https://techblog.comsoc.org/2025/12/23/how-will-fiber-and-equipment-vendors-meet-the-increased-demand-for-fiber-in-2026-due-to-ai-data-center-buildouts/ |
| 同 業績 | Corning 光通信 2026Q2 売上20.7億ドル(+32%)、うちEnterprise +65%。フジクラ 2026/3期 売上1兆1,824億円(+20.7%)、営業利益1,887億円(+39.2%)、情報通信事業部門 売上6,530億円・営業利益1,527億円 | | [二次] 原典URL=https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000253/glw-20260728xex99xq22026.htm , フジクラ決算短信ミラー https://finance-frontend-pc-dist.west.edge.storage-yahoo.jp/disclosure/20260514/20260514532598.pdf （詳細は agent2） |
| コネクタ/MPO・研磨 | Corning(MPO 2025年13.2億ドル・シェア15.4%と業者レポート), 精工技研(日, 光コネクタ＋研磨機・測定器), フジクラ, Senko, US Conec | 高密度化で多心MPO/MTフェルール需要増 | [二次・低] https://www.reportprime.com/optical-fiber-data-connector-r5267/company |
| 検査・装置 | Advantest(V93000), Teradyne, FormFactor(TRITON), MPI(台), Keysight, santec(日, 光測定器), ficonTEC(撤退報道) | **CPO量産の最大ボトルネックはテスト**との見方。ウエハレベル光電同時テストは自動化の量産解が未確立、Advantest陣営は2026上期PoC→下期共同開発 | [二次] https://www.trendforce.com/insights/cpo-testing-market-opportunities , https://www.formfactor.com/blog/2026/triton-scaling-silicon-photonics-wafer-test-for-high-volume-manufacturing/ |
| 日本の光電融合 | NTT(IOWN, PEC-2: 2026Q2光エンジンサンプル→Q4 CPOスイッチ商用サンプル、102.4T、スイッチ単体で電力50%削減、5,000個/ライン/月を目標), 浜松ホトニクス, 三菱電機(EML) | 日本勢は「完成品ではなく部品・材料・装置」で取る構図 | [二次] https://cloud.watch.impress.co.jp/docs/event/2065773.html , https://internet.watch.impress.co.jp/docs/news/2053692.html |

### 3. 市場規模（R1時点の収集値）
| 指標 | 値 | タグ/出典 |
|---|---|---|
| 光モジュール市場 2026年成長率 | 約+60%、2031年に約600億ドル近く（2025-31 CAGR 20%超） | [二次] LightCounting 2026/3 予測の要約 https://www.lightcounting.com/report/march-2026-ethernet-optics-382 （要約元が c-light 等の可能性→⚠） |
| 800G+1.6T の2026年売上 | 約146億ドル（光モジュール売上の約64%） | [二次・低] 同上要約 |
| 1.6T 出荷 | 2025年 約270万個 → 2026年 500万個超 | [二次・低] 同上要約（出典にばらつき: 860万〜2,000万個の幅も） |
| CPO/NPO市場 | 2025年 約1億ドル → 2030年 390億ドル超、2028-29年に急加速（スケールアップの光化） | [二次] https://www.trendforce.com/presscenter/news/20260615-13098.html |
| OCS市場 | 2030年 80億ドル超（Cignal AI） | [二次] 上記 |
| 800G 価格 | 2023年 約1,200ドル → 2026年 約400ドル前後（-60%超） | [二次・低] https://ascentoptics.com/blog/800g-optical-module-price/ （業者ブログ。要検証） |

### 4. 技術ロードマップと勝者・敗者（R1版の仮説、全て[推測]）
| 時期 | 主流 | 恩恵 | 逆風 |
|---|---|---|---|
| 2025-26 | 800G→1.6T プラガブル（200G/lane EML、3nm DSP） | 200G EML供給者(Lumentum, 三菱電機, Coherent)、DSP(Marvell, Broadcom)、大手モジュール(Innolight, Eoptolink, Coherent)、ファイバ(フジクラ, Corning) | 100G/lane世代しか持たない二番手モジュール（価格下落に晒される） |
| 2026-27 | LPO/LRO（DSP省略・省電力）の部分採用、CPOスケールアウト量産初期、OCS拡大 | OCS(Lumentum, Coherent)、SiPh製造(TSMC)、高出力CWレーザー | DSP（LPO比率次第。R1時点で1.6T LPOは限定的） |
| 2027-28 | CPOスケールアウト本格化（TH6-Davisson, Spectrum-X Photonics）、Rubin Ultra NVL576のラック間光接続 | 光エンジン/先端パッケージ(TSMC, ASE/SPIL)、ELSレーザー、ファイバ・高密度コネクタ（CPOはファイバ本数が増える）、検査装置 | プラガブル・モジュール組立（スイッチ側のトランシーバ需要が減る）、DSP |
| 2028以降 | スケールアップの光化（Feynman世代 NVLink CPO、銅と併存）、3.2T、IOWN系 | 同上＋スケールアップ向けで市場自体が数倍化（TrendForce: 2028-29に急加速） | 銅ケーブル/AEC（Credo等）の中長期的な天井 |

- キー仮説1[推測]: **CPOは「モジュール組立の付加価値」を「SiPh製造＋先端パッケージ＋スイッチベンダー」に移す**。一方レーザーとファイバ/コネクタは移行後も残る（むしろ本数増）→ 日本勢（フジクラ・精工技研・住友電工・三菱電機・santec）はCPO移行の被害が相対的に小さい側
- キー仮説2[推測]: 現在の超過利潤は「InPレーザー不足」と「ファイバ・プリフォーム不足」という**供給制約**に由来。供給が2027-28年に追いつくと（Coherent InP 2倍→さらに2倍、プリフォーム18〜24ヶ月）、価格下落・マージン正常化のリスク。参考: 「Shortage Today, Oversupply Tomorrow?」論点 https://cruxcapitalgroup.substack.com/p/the-ai-optics-trade-shortage-today （agent4 の弱気シナリオ材料）
- キー仮説3[推測]: NVIDIA は「スケールアップは可能な限り銅」で、光化はFeynman(2028)まで限定的。スケールアップ光化のタイミングがCPO市場の最大の変数

### 5. REPORT §1.1 形式の層別表（R1暫定版、agent5 依頼 requests/agent5-1-1.md の1・2への回答）
粗利率は R1 で取れた代表値のみ。空欄は R2 で各社決算から埋める。「26→28」は2026→2028年に層の利益が増えるか（↑/→/↓）の見立て [推測]。

| 層 | 主要プレイヤー（日/米/台中） | 粗利率の目安 | 参入障壁 / 価格決定力 | 26→28 | 出典・確度 |
|---|---|---|---|---|---|
| L1 ファイバ・ケーブル・コネクタ | 日: フジクラ, 住友電工, 古河電工, 精工技研 / 米: Corning / 中: YOFC / 欧: Prysmian | R2で取得（フジクラ情報通信の営業利益率 約23%=1,527/6,530億円） | 高: プリフォーム増設18〜24ヶ月で供給制約。価格決定力 中〜高（不足局面） | ↑（CPO・スケールアップ光化でファイバ本数増） | [二次] fierce-network, フジクラ短信要約 |
| L2 レーザー・受光（EML/CW/VCSEL, InP） | 米: Lumentum, Coherent, Broadcom / 日: 三菱電機, 住友電工(InP基板も) / 中: 源杰 ほか | Lumentum 全社 非GAAP 50.4%（FY26Q4） | 非常に高: InPの歩留まり・200G/lane。EMLは3社で約72%、需給ギャップ30%超 → 価格決定力 高 | ↑→（2027-28に供給追いつけば正常化リスク） | [二次] mlq.ai, sec.gov EX-99.1要約 |
| L3 DSP・ドライバ・TIA | 米: Marvell(約60%), Broadcom(30%超) / 他: Credo(AEC) | R2で取得（両社とも全社GMは高水準） | 非常に高: 3nm設計・2社寡占 | →↓（LPO/CPOでDSP省略の侵食。ただし2028までは1.6T/3.2Tプラガブルで量は伸びる） | [二次] digitimes要約（⚠） |
| L4 トランシーバ組立 | 中: Innolight(23.4%), Eoptolink, Huawei, Accelink, Hisense / 米: Coherent, AAOI / 台: 多数 | Innolight 46%(Q1'26), Eoptolink 約49%(Q1'26) | 中: 量産・認定・顧客関係。国内10社超が量産 → 長期的に価格下落圧力（800Gは年率大幅下落） | →↓（スイッチ側はCPOが代替。ただしGPU/NIC側・スケールアップ向けは残る） | [二次] lightcounting newsletter, biggo |
| L5 SiPh / CPO / 光エンジン | 台: TSMC(COUPE), ASE/SPIL, UMC / 米: NVIDIA, Broadcom, GlobalFoundries, Tower / 日: NTT(PEC-2) | 未取得 | 非常に高: SiPh製造・3D積層・歩留まり。量産できる供給者は少数 | ↑↑（市場 2025年約1億ドル→2030年390億ドル超） | [二次] trendforce 2026/6, 2026/7 |
| L6 スイッチ・システム | 米: NVIDIA, Broadcom(チップ), Arista, Cisco / 台: Accton, Foxconn / 光: OCS=Lumentum, Coherent | 未取得 | 高: スイッチASIC・NVIDIA統合システム。CPOで価値を取り込む側 | ↑ | [二次] |
| L7 装置・検査・受託製造 | 日: 精工技研(研磨機), santec(光測定), Advantest / 米: Keysight, FormFactor, Teradyne, Fabrinet(EMS) / 台: MPI | 未取得 | 中〜高: CPOのウエハレベル光電テストは量産解が未確立＝ボトルネックかつ機会 | ↑（CPO量産でテスト需要が新規発生） | [二次] trendforce insights, formfactor |
| L8 IOWN・次世代網 | 日: NTT, NTTイノベーティブデバイス / 協業: Broadcom, Accton | — | 長期オプション。PEC-2は2026Q4にCPOスイッチ商用サンプル | →（業績寄与は2027年以降） | [二次] impress |

**1.2 どこに利益が溜まるか（R1仮説）[推測]**: ①供給制約を握る L2（InPレーザー）と L1（ファイバ）が2026-27年の超過利潤の源泉、②寡占の L3 と、CPOで価値を取り込む L5/L6 が2027-28年の勝者候補、③L4 はシェア上位の中国勢が当面高マージンだが、CPO移行と価格下落の両面で最も構造的に不利。④L7 検査は「CPO量産のボトルネック」として小型株の機会（santec・精工技研は agent2 に要調査依頼済み）。

### 6. 次ラウンドの課題
1. レイヤー別の利益率表（GM/OPM、直近4四半期）: Lumentum, Coherent, Marvell(光部門), Broadcom, Innolight, Eoptolink, Fabrinet, Corning, フジクラ, TSMC → 「どこに利益が溜まるか」を定量化
2. CPO移行の侵食試算: スイッチ1台当たりのトランシーバ/DSP/レーザー/ファイバ金額の比較（プラガブル vs CPO）
3. 中国勢との競争・関税・輸出規制（Innolightのペンタゴン1260Hリスト報道 https://hellochinatech.com/p/zhongji-innolight-optical-transceiver を確認）
4. 過去サイクル（2000-01年光バブル、2018-19年400G調整）との比較材料（agent5依頼5）
5. agent5依頼3: ハイパースケーラ四半期設備投資 2024Q1〜最新の表（+Oracle）
6. agent5依頼6: 銘柄別ロードマップ耐性 R=1〜5 の採点案


---

## R2（2026-10-05）

### R2-1. 層別の利益プール表（各社GM/OPMの定量化）— agent5-1-1 依頼1への回答
期は各社の直近開示四半期。会計年度に注意（LITE/COHR/FN=6月末、MRVL=1月末、AVGO=10月末）。粗利率は特記なき限り non-GAAP。

| 層 | 企業 | 期 | 売上 | 粗利率 | 営業利益率（または純利益率） | タグ/出典 |
|---|---|---|---|---|---|---|
| L1 | Corning 光通信セグメント | 2026Q2 | 20.7億ドル(+32%) | — | セグメント純利益 4.38億ドル＝**21.2%**（内部整合: 438/2,070 ✔） | [二次] 原典URL=https://www.sec.gov/Archives/edgar/data/24741/000002474126000253/glw-20260728xex99xq22026.htm |
| L1 | フジクラ 情報通信事業部門 | 2026/3期通期 | 6,530億円 | — | 営業利益 1,527億円＝**23.4%** | [二次] R1と同じ（短信ミラー）。詳細は stocks/5803.md |
| L2/L4/L6 | Lumentum（全社） | FY26Q4（2026/6期末） | 10.1億ドル(+109%) | **50.4%** | 営業 **36.6%**（non-GAAP） | [二次] 原典URL=https://www.sec.gov/Archives/edgar/data/0001633978/000162828026055726/lite_ex991xq4fy26.htm |
| L2/L4 | Coherent（全社、DC&Cは売上の59%） | FY26Q4 | 20.5億ドル(+34%) | **40.2%**（FY26通期39.4%） | 営業 **21.8%**（FY26通期20.5%） | [二次] https://ir.coherent.com/news-releases/news-release-details/coherent-corp-reports-fourth-quarter-and-full-year-fiscal-2026（sec.gov上のどの8-Kが該当かは未特定） |
| L3 | Marvell（全社、DC比率79%） | FY27Q2（2026/8） | 27.39億ドル(+37%) | **58.9%** | 営業 **36.6%**、Q4に38〜40%目標 | [二次] https://convergedigest.com/marvell-q2-fy2027-data-center-ai-revenue/ |
| L3 | Credo（AEC/DSP） | FY26Q3（2026/1期、やや古い） | — | **68.6%** | — | [二次] 要約経由、⚠期が古い |
| L3/L5/L6 | Broadcom（全社） | FY26Q3（2026/8/2期末） | AI半導体 167億ドル(+221%) | GAAP 69%（non-GAAP 75%との要約もあり⚠） | — | [二次] 原典URL=https://www.sec.gov/Archives/edgar/data/0001730168/000173016826000080/avgo-20260802.htm |
| L4 | Innolight（中際旭創, 300308） | 2026年1-6月 | 417.8億元(+182%) | Q1 **46.1%**（H1は未取得） | 純利益 136.5億元＝**32.7%** | [二次] https://www.thestandard.com.hk/finance/article/340637/ |
| L4 | Eoptolink（新易盛, 300502） | 2026年1-6月 | 209.1億元(+100%) | **48.5%** | 純利益 75.3億元＝**36.0%** | [二次] 要約経由。⚠ marketscreener見出しは「売上+283%」で不一致→要確認 |
| L4 | AAOI | 2026Q2 | 1.919億ドル(+86%) | **29.8%**（GAAP 27.7%） | 純利益 0.055億ドル≈3% | [二次] https://investors.ao-inc.com/news-releases/news-release-details/applied-optoelectronics-reports-second-quarter-2026-results |
| L5 | TSMC（全社） | 2026Q2 | — | **67.7%** | — | [二次] 原典URL=https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000451/a2q26e_withguidancexfinal.htm |
| L6 | Arista | 2026Q2 | — | **63.4%** | — | [二次] 要約経由 |
| L6 | Ciena | FY26Q3（2026/7） | 16.7億ドル | **46.4%** | — | [二次] https://www.tradingview.com/news/tradingview:b7163ae57abaa:0-ciena-posts-q3-fy2026-revenue-1-67b-adjusted-diluted-eps-2-11-raises-fy26-revenue-guide/ |
| L7 | Fabrinet（EMS） | FY26Q4（2026/6期末） | 13.16億ドル(+45%) | **12.2%** | 営業 **10.9%** | [二次] 原典URL=https://www.sec.gov/Archives/edgar/data/0001408710/000140871026000026/fn-2026811xex991q426.htm |

市場全体: Cignal AI によるとデータコム光部品市場は 1Q26 に **77億ドル（前年比2倍超）**、うち Innolight 26億ドル＝34%（内部整合 ✔）。2025年通年は190億ドル超。[二次] https://cignal.ai/2026/06/datacom-optical-component-revenue-doubles-to-7-7-billion-in-1q26/ , https://cignal.ai/2026/08/fcc-ban-on-new-chinese-optical-modules/

**読み取り [推測]**
1. 粗利率の階層は「電気側シリコン（TSMC/Broadcom/Marvell/Credo 59〜75%）＞ 光チップ内製型（Lumentum 50%）≈ 中国組立大手（46〜49%）＞ 部品外部調達の組立（Coherent 40%、AAOI 30%）＞ EMS（Fabrinet 12%）」。
2. 意外な点: 中国2強の**純利益率33〜36%**は Lumentum の営業利益率36.6%と同水準で、Coherent を上回る。現局面では組立大手も超過利潤を得ている。理由の仮説は、(a) 1.6T・800Gでの量と認定の先行、(b) SiPh/レーザーの一部内製、(c) 供給制約下の価格維持。→ **供給制約が緩むと最初に剥落するのは(c)**。L4 は「現在の利益は大きいが、持続性は最も低い」層。
3. Fabrinet の12%は受託製造の構造的上限。量の恩恵は受けるがマージンは伸びない（L7のうちEMSは「量のベータ」）。
4. L1 は Corning・フジクラとも営業ベースで**20%台前半**と、ケーブル事業としては歴史的高水準。供給制約（プリフォーム18〜24ヶ月）が続く限り維持されやすい。

### R2-2. ロードマップ時期表 — agent5-1-1 依頼2への回答
| 技術 | 量産開始（想定） | 根拠 | 得をする層 | 損をする層 | 確度 |
|---|---|---|---|---|---|
| 800G プラガブル（100G/lane） | 2024〜（主力、2026年に出荷倍増見込み） | LightCounting要約 | L4, L3, L2(EML/VCSEL) | — | [二次] |
| 1.6T プラガブル（200G/lane, 3nm DSP） | 2025後半〜**2026が元年**（1Q26に急増、2Q26に量産出荷） | Cignal AI 1Q26/2Q26 | L2（200G EML: Lumentum先行）, L3（Marvell Ara）, L4大手 | 100G/laneしか持たない二番手 | [二次] |
| LPO（DSPなし）/ LRO（送信側DSPのみ） | 800G LPOは限定的。1.6Tは熱の問題（>30W）でLROが現実解。「2026-28年の800G/1.6Tポートの30%超がLPO/CPO」との予測あり | IEEE EPS資料・業者ブログの要約 | L2, ドライバ/TIA（中国ローカル化） | L3（DSP） | [二次・低] |
| CPO スケールアウト（スイッチ） | 2026年に量産出荷開始（NVIDIA Spectrum-X Photonics、Broadcom TH6-Davisson 102.4T は2026Q3前後に広範供給）、**本格拡大2027-28** | TrendForce 2026/7、ServeTheHome | L5（TSMC/SPIL/ASE）, L6（NVIDIA/Broadcom）, L2（ELSレーザー）, L1（シャッフル/高密度コネクタ）, L7（SiPhテスト） | L4（スイッチ側モジュール）, L3（DSP） | [二次] |
| OCS（光回線スイッチ） | 2026年に外部調達で量産（Google→Lumentum/Coherent/Huber+Suhner） | Cignal AI | L6/L2（Lumentum, Coherent） | 電気スパイン・スイッチの一部 | [二次] |
| 3.2T プラガブル | 2028年 | deepfundamental要約（Innolight先行との見方） | L4大手, L2 | — | [二次・低] |
| スケールアップ光化（NVLink CPO） | Rubin Ultra NVL576（2027後半）でラック間に光。**Feynman（2028）でNVLink CPOスイッチ**（銅と併存） | GTC 2026 発言の報道 | L5, L2, L1。市場規模は2028-29年に急加速（CPO/NPO 2030年390億ドル超） | 銅AEC（L3のCredo等）の長期天井 | [二次] |
| IOWN / NTT PEC-2 | 2026Q2光エンジンサンプル→**2026Q4 CPOスイッチ商用サンプル**（102.4T、Broadcom+Accton） | NTT/impress | L8, 日本の部品 | — | [二次] |

### R2-3. CPO 移行の得失試算（[推測]、前提を明示）
**モデル**: 102.4T スイッチ1台＝1.6T×64ポート。
- プラガブルの場合: スイッチ側に1.6Tトランシーバ64本。単価は2026年末に1,500〜2,000ドルとの見方（[二次・低] vitextech ほか業者ブログ）→ **スイッチ側の光の金額 約10〜13万ドル/台**。
- CPOの場合（TH6-Davisson）: 6.4T光エンジン×16＋外部レーザー（ELS）。光インターコネクト電力は約70%減（Broadcom）。
- **金額の行き先**: 失う＝モジュール組立の付加価値（L4）、DSP（L3: スイッチ側で100%不要）、ケージ/コネクタの一部。得る＝光エンジン（L5: Broadcom/NVIDIA＋TSMC/SPIL）、ELSレーザー（L2: 個数は減るが高出力で単価上昇）、内部ファイバ・シャッフル・高密度コネクタ（L1）、ウエハレベル光電テスト（L7）。

**数量への効き方（重要）**: CPOは当面**スイッチ側だけ**。リンクの反対側（NIC/GPU側、または相手スイッチ側がプラガブルのまま）にはトランシーバが残る（TH6-Davissonでも「フロントパネルのトランシーバは消え、リンクの遠端のモジュールに置き換わる」）。したがって
- トランシーバ数量の減少率 ≈ CPO採用率（スケールアウトのスイッチポート比）× 約50%
- 2028年の CPO 採用率 10〜30% と置くと、数量減は **約5〜15%**（[推測]。採用率の根拠は TrendForce「2027-28年に本格拡大」と「LPO/CPOで30%超」予測の幅）
- 同時期にスケールアップの光化（Rubin Ultra NVL576 のラック間、Feynman の NVLink CPO）が**新規の光需要**を生むため、L4 全体の需要は2028年までは純増の可能性が高い
- **L4 の本当の侵食は NIC/GPU 側も CPO/NPO 化する2029年以降**（Meta/Microsoft は OCI-MSA で NPO 推進、TrendForce）

**層別の結論（2026→2030）[推測]**
| 層 | CPO移行の影響 | 理由 |
|---|---|---|
| L1 ファイバ・コネクタ | 得 | CPOでもファイバは必要。シャッフル・高密度化で本数・付加価値が増える |
| L2 レーザー | 中立〜得 | ELSで残る。個数↓・出力と単価↑。InP能力を持つ者（Lumentum/Coherent/三菱電機/住友電工）が有利 |
| L3 DSP | 損 | スイッチ側DSPが不要。LPO/LROも逆風。ただし2028年まではプラガブルの量で伸びる |
| L4 組立 | 2028まで中立、以後損 | スイッチ側が先に消える。光エンジンを内製できる大手（Innolight等）は一部を取り返す |
| L5 SiPh/光エンジン | 大きく得 | 2025年約1億ドル→2030年390億ドル超（TrendForce） |
| L6 スイッチ | 得 | 光の価値をスイッチ価格に取り込む（Broadcom/NVIDIA） |
| L7 検査 | 得 | ウエハレベル光電テストは新規需要。EMS(Fabrinet)は光エンジン組立を取れるか次第 |

R3 で精緻化: トランシーバ BOM の内訳（DSP・レーザー・その他）の出典付き数値、CPO 1台当たりの光エンジン価格。

### R2-4. 中国勢との競争・関税・輸出規制
| 論点 | 事実 | タグ/出典 |
|---|---|---|
| 中国勢のシェア | 2025年トランシーバ出荷: Innolight 23.4%（1位）、上位10社中7社が中国系。1Q26データコム光部品市場77億ドルのうち Innolight が34% | [二次] lightcounting newsletter, cignal.ai |
| FCC の動き | 2026/8/4 ロイター「FCCが中国製の新型光トランシーバの輸入禁止を起草」→ LITE/COHR/MRVL株が8〜10%上昇。しかし**最終規則（FCC 26-50、7/23公表・8/7官報・30日後発効、さらに9/11に機器認証プログラムの規則を官報掲載）は、光モジュールを独立の対象カテゴリにせず、Innolight/Eoptolink/TFC はカバードリスト外**。対象は「カバードリスト掲載企業製のロジック部品を含む機器」に限定 | [二次] https://cignal.ai/2026/08/fcc-ban-on-new-chinese-optical-modules/ , https://finance.biggo.com/news/527f426d-2faa-4536-8c71-3772272ffdf4 （⚠ 9/11 と 8/7 の2つの日付が混在。同一規則か別規則か R3 で確認） |
| 議会 | 上院超党派法案（McCormick/Gallego/Cornyn/Fetterman, 2026/9）「Securing National Security Systems from Chinese Optical Transceivers Act」: 国家安全保障システム向けの連邦調達から中国製トランシーバを排除。**5年の移行期間**。対象に Innolight・Eoptolink | [二次] https://www.mccormick.senate.gov/news/press-releases/senators-mccormick-gallego-cornyn-fetterman-introduce-bill-to-keep-chinese-transceivers-out-of-u-s-national-security-systems/ |
| 国防総省 | 2026/6 に Innolight を「中国軍事企業」リスト（1260H）に追加 | [二次] executivegov 等の要約 |
| 原産地 | 中国2強は米国向けの大半を中国国外（タイ等）で生産 → 実際の影響は原産地規則次第 | [二次] 同上 |
| 中国のInP輸出規制 | 2025/2 に導入。ライセンス遅延で6インチInPウエハ価格が**+250%（5,000ドル）**、AXT・Coherent・Lumentum・台湾VPEC/LandMarkに影響。中国は世界のインジウム生産の約70% | [二次] https://www.mining.com/web/chinas-control-over-indium-phosphide-exports-threatens-ai-data-centre-rollout/ |
| ハイパースケーラへの影響 | 禁止されれば Amazon/Microsoft 等のコスト増・GPU稼働率低下（Counterpoint）。非中国勢（Coherent/Lumentum）には代替できる能力がまだない | [二次] https://thenextweb.com/news/fcc-optical-transceiver-ban-china-us-hyperscalers |

**投資上の含意 [推測]**
- 米規制は「起草→後退」の往復で、**ヘッドラインで米国光株が±10%動くイベントリスク**（監視指標: FCC・上院法案・1260H・原産地判断）。agent5 のイベントカレンダーに入れる価値あり
- 本当に禁止されれば最大の受益は Lumentum/Coherent/AAOI/Fabrinet（米国・非中国の生産能力）だが、能力不足で短期は「ハイパースケーラのコスト増＝設備投資の効率低下」という逆風も
- 中国の InP 輸出規制は、**中国外のInP基板供給者（住友電工、AXTの中国外拠点、IQE）**とInPを内製するレーザー大手の交渉力を高める。日本株では住友電工(5802)の論点（agent2 へ）
- 中国勢は米国規制リスクを抱える一方、米国外の需要（中国国内AI、他地域）と東南アジア生産で逃げ道がある。中国勢の価格攻勢は「800Gの価格下落」の主因であり、規制で米国市場から締め出されるほど米国内の価格は維持されやすい（米国勢に有利）


---

## R3（2026-10-05）

### R3-1. ハイパースケーラ四半期設備投資表（暦年四半期、単位: 10億ドル）
定義: MSFT・META はファイナンスリースを含む（各社が開示する「capital expenditures including finance leases」）。GOOGL・AMZN は有形固定資産の取得（現金ベース）。MSFT は6月決算なので暦年に読み替え（FY25Q1＝2024Q3）。

| 社 | 24Q3 | 24Q4 | 25Q1 | 25Q2 | 25Q3 | 25Q4 | 26Q1 | 26Q2 | 2026年ガイダンス | 出典・確度 |
|---|---|---|---|---|---|---|---|---|---|---|
| MSFT | 20.0 | 22.6 | 21.4 | 24.2 | 34.9⚠ | 37.5 | 31.9 | 41.0 | 暦年2026 約190（4月時点、7月据え置き） | [二次] cnbc 2026/4/29・2026/7/29、microsoft.com IR。26Q1=31.9は「前年比+49%」で25Q1=21.4と整合 ✔。FY25各四半期と25Q3=34.9は検索要約がクエリを反映した可能性あり ⚠ |
| GOOGL | 13.1 | 14.2 | 17.2 | 22.4 | 24.0 | 27.8 | 35.7 | 44.9 | 195〜205（Q2で180〜190から上方修正） | [二次] 原典URL=sec.gov 10-Q/10-K（goog-20260630 等）の累計値からの差分。2025年計91.4 ✔ |
| AMZN | 22.6 | 27.8 | 25.0 | 32.2 | 35.1 | 39.5 | 44.2 | 54.2 | 約220（当初200、メモリ価格上昇で上方修正） | [二次] cnbc 2024/10/31・2026/7/30。2025年計131.8 ✔ |
| META | 9.2 | 14.8 | 12.9 | 17.0 | 19.4 | 22.1 | 19.8 | 31.1 | 130〜145（下限引上げ） | [二次] 原典URL=sec.gov 8-K EX-99.1（meta-xxxxxxxexhibit991）。2025年計は要約で72.2だが四半期合計は71.4 ⚠（差0.8） |
| **4社合計** | **64.9** | **79.4** | **76.5** | **95.8** | **113.4** | **126.9** | **131.6** | **171.2** | **約747.5（中央値）** | 計算 |
| 前年比 | | | | | +75% | +60% | +72% | +79% | | 計算 |

- 2025年合計 **412.6**（報道の約410〜413と一致 ✔）。2026年上期 302.8 → ガイダンス中央値達成には**下期に四半期約222**（上期平均151の1.5倍）が必要。下期の各社必要額: MSFT 58.5、GOOGL 59.7、AMZN 60.8、META 43.3／四半期
- Oracle（参考）: FY26（2026/5期）55.7、FY27Q1（2026/8期）28.0、FY27 ガイダンス 900〜950（ネット現金ベースは700以下）[二次] 原典URL=https://www.sec.gov/Archives/edgar/data/0001341439/000119312526389274/orcl-20260831.htm
- 2027年: コンセンサス 約934.5（GOOGL 284.8 / AMZN 256.5 / MSFT 207.6 / META 185.6）[二次] valueaddvc。**2026年中央値747.5比 +25%**。Evercore/BofA は1兆ドル超（+34%）
- **示唆 [推測]**: 金額は2027年も増えるが、**伸び率は+70%台から+25〜35%へ急減速**。光部品の発注は設備投資の「伸び」に連動しやすい（新規クラスタ分の発注が先行するため）。2027年の各社ガイダンス初出（2027年1〜2月の10-12月期決算）が最重要イベント。agent4 B1（2次微分リスク）と整合

### R3-2. 過去サイクル比較（業界売上・設備投資側。株価下落率は agent4 B1 担当）
| サイクル | 需要側の引き金 | 業界売上の落ち込み | 企業業績の落ち込み | 期間 | 出典・確度 |
|---|---|---|---|---|---|
| 2001-02年 通信バブル崩壊 | 通信キャリアの設備投資の急減、ネットワークの過剰能力、資本市場の閉鎖、顧客の在庫圧縮 | ⚠業界合計は未取得 | JDSU 売上 FY01 32.3億ドル → FY02 11.0億ドル（**-66%**）。買収のれん等 448億ドルを減損 | 2001〜2003年（回復は数年） | [二次] 原典URL=https://www.sec.gov/Archives/edgar/data/0000912093/000089161802004336/f84311e10vk.htm |
| 2018後半-19年 クラウド消化 | クラウドの光への支出鈍化（設備投資の消化期）、100G価格下落 | イーサネット光トランシーバ **-18%**（LightCounting「記録上最大の下落」） | （LITE はこの時期3Dセンシングの比重が大きく比較困難 ⚠） | 約1年、2020年に回復 | [二次] https://www.cablinginstall.com/data-center/article/14068853/ethernet-transceiver-sales-dip-18-in-2019-after-nearly-a-decade-of-growth-report |
| 2023年 在庫調整 | 供給不安時の過剰発注→在庫の正常化、クラウド設備投資 2Q23 **-2%**（Dell'Oro）、無線フロントホール -30% | 光トランシーバ全体 110億→109億ドル（**約-1%**）、イーサネット -10% | LITE 非GAAP 粗利 FY23 43.2% → FY24 33.0%、営業利益率 FY22 30.8% → FY23 19.2% → **FY24 2.8%**。Corning 光通信 純利益率 2023Q3-Q4 約10%（91/918、88/903） | 2023〜2024年前半 | [二次] https://www.delloro.com/news/ai-investments-not-enough-to-offset-hyperscale-digestion-cycle-cloud-capex-down-2-percent-in-2q-2023/ , https://techblog.comsoc.org/2023/04/28/lightcounting-sales-of-optical-transceivers-will-decline-in-2023/ , LITE 8-K（sec.gov lite_ex991xq4fy24） |

**読み取り [推測]**
1. 2001年型（売上が2/3消える）は「顧客＝通信キャリアの設備投資がゼロ近くまで縮む＋顧客自身の資金繰り破綻」の組合せ。現在の顧客はキャッシュフローの厚いハイパースケーラで、2001年型の再現確率は低い（ただし Oracle やネオクラウドは負債調達の比重が高く、ここが弱い環）
2. 2019年・2023年型は**業界売上 -1〜-18%でも、営業レバレッジで利益は半減〜消滅**。現在の利益率が過去最高水準（LITE 36.6%、Corning光通信 21%）なので、同じ規模の調整でも株価への影響は大きい
3. 現在との違い: 2019・2023年は「設備投資の伸び率がマイナス近辺」で起きた。2027年は伸び率+25%前後の見込みで、**マイナス成長ではなく「伸びの鈍化＋供給増」の組合せ**。これは過去に前例がないため、価格（ASP）の下落率が鍵になる

### R3-3. 供給が需要に追いつく時期と平常マージン — agent5-2-2 回答
**(1) 供給追いつき時期**
| ボトルネック | 増産計画（各社） | 追いつく時期の見立て | 出典・確度 |
|---|---|---|---|
| EML/CW レーザー（InP） | Lumentum: 2027年まで完売、2028年分も2四半期以内に完売の可能性。能力追加は2026〜2028年に段階的、新規取得ファブで**2028年初に生産開始（年50億ドル分の売上能力）**、EML出力を8倍超へ。Coherent: 社内InP出力を2026年末までに倍増、2027年末までにさらに倍増。TrendForce: EML+CW-DFB 月産能力は2026年に倍増。欧州で6インチInPファブが2028年に本格稼働 | **2028年後半〜2029年** [推測] | [二次] https://www.semiconductor-today.com/news_items/2026/aug/lumentum-190826.shtml , https://mlq.ai/research/lumentum-ai-optical-laser-supercycle/ , trendforce 2026/3/18 |
| 光ファイバ・プリフォーム | 増設は18〜24ヶ月。フジクラは国内・米国の各拠点で最大約3倍、総額最大3,000億円を段階投資（佐倉の新工場建設中）、有意な新能力は2028年。Corning は Meta と最大60億ドルの複数年供給契約・ノースカロライナ増設。YOFC 等の中国勢は2030年に20億芯km/年を目指す。需要は2027年に8.8億芯km（2025年比+35%、CRU） | **2028年**（UBS「需給逼迫は2027〜28年まで」）[二次]。中国勢の増設次第で2028年に供給過剰へ転じるリスク | [二次] https://www.datacenterdynamics.com/en/news/fujikura-to-triple-optical-fiber-production-as-part-of-2bn-investment/ , https://allweatherfinance.com/after-a-37-correction-in-the-fiber-optic-sector-ubs-remains-bullish-the-market-may-be-overestimating-the-risk-of-overcapacity-in-2027/ |
| SiPh・先端パッケージ（CPO） | TSMC COUPE 2026年量産、UMC 12インチSiPh 2026/7出荷開始。テストの量産解は未確立 | 2027-28年もボトルネック継続 [推測] | R1 §2 |

- **結論 [推測]**: 2028年に「レーザーとファイバの新能力の立ち上がり」と「設備投資の伸び率鈍化（R3-1）」が重なる。**終端マージンの弱気シナリオは2028〜29年に平常期へ回帰する前提**が妥当。なお光ファイバ株は「2027年の過剰能力」懸念ですでに一度37%調整した（UBS記事）→市場は部分的に織り込み始めている

**(2) 前回サイクルの平常期マージン（2019〜2024年）**
| 企業 | 平常期（目安） | 谷 | 現在（参考） | 出典・確度 |
|---|---|---|---|---|
| Lumentum | 非GAAP 粗利 **40〜45%**、営業 **15〜20%**（FY23: 43.2% / 19.2%）。FY20-21は粗利約50〜53%だが3Dセンシング（民生）の比重が大きく構成が違う ⚠ | FY24: 粗利 33.0%、営業 2.8% | FY26Q4: 50.4% / 36.6% | [二次] LITE 8-K（sec.gov lite_ex991xq4fy22, xq4fy24, q2fy21） |
| Coherent（II-VI） | 非GAAP 粗利 **36〜40%**（FY21 39.8%、FY22 39.8%、FY24 36.0%）、営業 約18%（FY25 17.8%） | FY24 36.0% | FY26: 39.4% / 20.5% | [二次] coherent.com 決算資料 |
| Corning 光通信 | セグメント純利益率 **10〜14%**（2023Q3 9.9%、2023Q4 9.7%、2024Q2 12.8%、2024Q3 14.1%） | 2023年 約10% | 2026Q2: 21.2% | [二次] sec.gov 8-K 要約・yahoo |
| フジクラ 情報通信 | ⚠未取得（agent2 に依頼） | | 2026/3期 23.4% | |

- **agent5 への提案 [推測]**: 終端（平常期）FCF マージンの置き方 — 弱気＝2023-24年の谷（LITE 営業 約3〜10%）、中立＝平常期（LITE 営業 15〜20% → FCF 12〜17%）、強気＝現在水準の一部維持（LITE 営業 25〜30%）。**Coherent は現在のマージンが平常期と大差ない**（粗利40% vs 36〜40%）ので、終端マージンの下振れ余地は LITE より小さい → V/K の比較で COHR に有利な論点

### R3-4. R（ロードマップ耐性）採点案 — agent5-1-1 依頼6
基準は agent5 の定義（5＝CPO/LPO に移るほど売上が増える、3＝中立、1＝置き換えられる）。**R は方向だけを見る**（光の売上比率の大小は E で評価）。根拠は §R2-3 の層別結論。全て [推測]。

| 銘柄 | R | 理由（1行） |
|---|---|---|
| AVGO | 5 | CPOスイッチ（TH6-Davisson）・EML・DSPを全部持つ。どの技術が勝っても取る側 |
| TSM | 5 | COUPE で CPO 光エンジンを製造。CPO 比率が上がるほど増える |
| GLW | 5 | ファイバ・コネクタは CPO で本数増。NVIDIA CPO 協業先 |
| 6777 santec | 5 | SiPh/CPO の光検査は CPO 量産で新規発生する需要 |
| 5803 フジクラ | 4 | ファイバ・高密度ケーブル・MPO は CPO でも増える。ただしコネクタ形状変化への対応が条件 |
| 5801 古河電工 | 4 | ファイバ（＋励起LD）。CPO で減る製品が少ない |
| 5802 住友電工 | 4 | InP基板・ファイバ・レーザー。CPO の外部光源・InP 不足の受益 |
| 4063 信越化学 | 4 | プリフォームと SOI ウエハ（SiPh 基板） |
| 6834 精工技研 | 4 | 高密度コネクタ・研磨機は増える側。プラガブル用部品比率が高いなら3へ（製品転換が条件、agent2 と同見解） |
| LITE | 4 | EML はプラガブル向けだが、ELS（CPO 光源）・OCS で残る。レーザー個数1/4化の単価相殺は未確認 |
| TSEM | 4 | SiPh ファウンドリ。CPO で増える |
| AXTI | 4 | InP 基板は CPO でも必要（K で中国リスクを評価） |
| FORM | 4 | SiPh ウエハプローバ（TRITON）は CPO で新規需要。全社に占める比率は小（E で評価） |
| 6857 アドバンテスト | 4 | CPO 光電同時テスト（V93000）。同上 |
| 6613 QDレーザ | 4 | SiPh/CPO 向け光源。ただし事業化前 |
| POET | 4 | 光インターポーザ（光エンジン部品）。事業化前 |
| NVDA（参照） | 5 | CPO スイッチの価値を取り込む側 |
| COHR | 3 | トランシーバ組立は侵食されるが、InP・OCS・CW レーザー・CPO 協業で相殺 |
| FN | 3 | EMS。プラガブルが減っても光エンジン・CPO スイッチ組立を取れれば中立（NVIDIA が顧客の16%） |
| CIEN | 3 | DCI/コヒーレントは CPO の対象外。スケールアクロス需要は別軸 |
| ANET | 3 | スイッチ側だが LPO 推進派。CPO の主導権は Broadcom/NVIDIA |
| MTSI / SMTC | 3 | LPO ではドライバ/TIA が増え DSP を置き換える側、CPO では統合されて減る側。差し引き中立 |
| 6965 浜松ホト / 6503 三菱電機 / 9432 NTT / 4062 イビデン / 5232 住友大阪セメント / 6524 湖北工業 / LWLG / VIAV | 3 | 移行の影響が中立、または光通信の比率が小さく方向が定まらない |
| MRVL | 2 | PAM4 DSP 約60%シェアは LPO/LRO/CPO で侵食される側。SiPh 光エンジン・カスタムXPUで一部相殺 |
| CRDO | 2 | 光DSP は LPO/CPO で侵食、AEC（銅）はスケールアップ光化で長期的に天井。ただし2027-28年は銅継続の受益 |
| AAOI | 2 | プラガブル組立が中心。自社レーザーはあるが CPO 光源の実績なし |
| 6961 エンプラス | 2 | トランシーバ用レンズ・光学部品はプラガブル依存 [推測] |

**DSP/SerDes 勢（AVGO, MRVL, CRDO）を「光の勝者」に含めるべきか（リーダー余力課題）[推測]**
- **AVGO: 含める（ただし E は低い）**。光は全社の一部だが、CPO・EML・DSP・スイッチ ASIC を全部持ち、技術ロードマップのどの分岐でも取り分がある。ポートフォリオでは「ロードマップ不確実性に強い大型コア」
- **MRVL: 2026-28年は勝者、2029年以降は条件付き**。1.6T/3.2T プラガブルの量で DSP が伸びる期間は勝者。CPO 本格化とともに DSP の取り分は縮む。株価はカスタム XPU の比重が大きく、光テーマの純度は中程度
- **CRDO: 「光の勝者」ではなく、光普及が遅れる場合のヘッジ**。NVIDIA は2027-28年までラック内を銅で引っ張る方針（R1 キー仮説3）→ CPO/スケールアップ光化が遅れるほど CRDO（AEC）が勝つ。光株ポートフォリオに少量組み込むと、ロードマップ遅延リスクに対する逆相関の役割を期待できる（相関の実測は未確認）
