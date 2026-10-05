# agent1 ノート（業界・技術）

## 最新の要点（R1, 2026-10-05）
- 環境: 直接取得（curl/WebFetch）はIR・SEC・TDnet・株価サイトとも全滅（egress 403）。**使えるのは WebSearch の要約のみ** → 本研究の数値は原則 [二次]。原典URL併記＋2ソース一致で信頼度を上げる運用を提案（board/issues/agent1-1-1.md）
- 利益の溜まり場（暫定・[推測]）: ①InPレーザー（EML/CWレーザー: 供給不足30%超、Lumentum/Coherent/三菱電機）②DSP（Marvell+Broadcomで9割超）③CPO光エンジン＋先端パッケージ（TSMC COUPE）④ファイバ/コネクタ（プリフォーム増設に18〜24ヶ月、フジクラ・Corning）。モジュール組立は中国勢上位寡占だが粗利46〜49%と現状は高水準
- ロードマップ: 2026=1.6T元年＆CPO量産初期（NVIDIA Spectrum-X Photonics出荷開始、Broadcom TH6-Davisson）、本格拡大は2027-28（TrendForce）、スケールアップ光化はFeynman世代（2028）。CPO/NPO市場 2025年約1億ドル→2030年390億ドル超（TrendForce）
- 需要起点: 米4社ハイパースケーラ設備投資 2026年 約7,600億ドル（2025年 約4,100億ドル）、2027年コンセンサス1兆ドル前後
- 新規出典数 約30 / 新規主張数 約35（全て[二次]または[推測]）/ 次ラウンド: (a)レイヤー別の利益率表を各社決算で定量化（GM/OPM）、(b)CPO移行で「誰が何を失うか」（プラガブル・DSP・モジュール組立の侵食量）の試算、(c)中国勢との競争・関税

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
