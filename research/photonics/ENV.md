# ENV（到達可否、1行1ドメイン）
- www.fujikura.co.jp: ✘ WebFetch EGRESS_BLOCKED (agent2, 2026-10-05)
- finance-frontend-pc-dist.west.edge.storage-yahoo.jp (Yahoo開示PDF): ✘ WebFetch blocked (agent2, 2026-10-05)
- kabutan.jp: ✘ WebFetch/curl blocked (agent2, 2026-10-05)
- dempa-digital.com: ✘ WebFetch blocked (agent2, 2026-10-05)
- stockexpress.jp: ✘ WebFetch blocked (agent2, 2026-10-05)
- www.release.tdnet.info / disclosure2.edinet-fsa.go.jp / irbank.net / minkabu.jp / finance.yahoo.co.jp / www.jpx.co.jp / stooq.com / query1.finance.yahoo.com: ✘ curl CONNECT 403 (agent2, 2026-10-05)
- 迂回: WebSearch は動作（検索結果スニペットのみ。[二次]扱い）(agent2, 2026-10-05)
- fred.stlouisfed.org / www.ecb.europa.eu / www.federalreserve.gov / www.sec.gov / www.boj.or.jp: ✘ curl CONNECT 403・WebFetch EGRESS_BLOCKED (agent5, 2026-10-05)
- www.tradingkey.com: ✘ WebFetch blocked (agent5, 2026-10-05)
- www.sec.gov / efts.sec.gov / data.sec.gov: ✘ WebFetch EGRESS_BLOCKED・curl失敗 (agent3, 2026-10-05)
- investor.lumentum.com / ir.ao-inc.com / investors.coherent.com: ✘ blocked (agent3, 2026-10-05)
- nasdaq.com / barchart.com / businesswire.com / globenewswire.com / prnewswire.com / stockanalysis.com / finance.yahoo.com / investing.com / seekingalpha.com / reuters.com / macrotrends.net / companiesmarketcap.com / marketbeat.com / fool.com / en.wikipedia.org: ✘ curl失敗（WebFetchも nasdaq/barchart は EGRESS_BLOCKED） (agent3, 2026-10-05)
- 結論(agent3): 米国株の一次資料は直接取得不可。WebSearch のスニペット（SEC 8-K の URL が検索結果に出る場合も本文は未読）→ すべて [二次] 扱い (agent3, 2026-10-05)
<!-- agent1 R1 作成 2026-10-05（UTC 03:50頃）。検証方法: curl（HTTPS_PROXY経由）、WebFetch、WebSearch -->
## 結論（最重要）
- **直接取得（curl / WebFetch）は github.com・api.github.com・pypi.org・registry.npmjs.org 以外ほぼ全滅**（egress proxy が CONNECT に 403 = 組織ポリシーで拒否。リトライ・迂回は禁止）
- **使えるのは WebSearch のみ**: 検索結果のタイトル/URL＋検索エンジン側の要約（数値含む）が返る。`allowed_domains=["sec.gov"]` 等の絞り込みも有効で、10-K/8-K の該当数値が要約に出る
- したがって原典を「自分で開いた」[一次] は事実上取得不能。**WebSearch 要約経由は [二次] とし、要約が依拠した原典URL（sec.gov 等）を併記**することを提案（DECISIONS.md 参照）
- WebSearch の要約は誤り・古い値の混入あり（例: AAOI の52週レンジ要約が不自然）。重要数値は**異なるクエリ/ソースで2回以上一致**を確認すること
- 人間側の対処: 環境設定の Network access で許可ドメインを追加すれば解消（https://code.claude.com/docs/en/cloud-environments#network-access）。本研究中は不可として進める

## ドメイン別（1行1ドメイン｜curl｜WebFetch｜WebSearch経由の可否・備考）
- www.google.com / www.bing.com / duckduckgo.com | ✘403 | - | 検索は WebSearch ツールで代替可
- www.sec.gov / data.sec.gov / efts.sec.gov (EDGAR) | ✘403 | ✘ | ◯ allowed_domains=["sec.gov"] で10-K/8-K(EX-99.1)の数値要約が取れる
- disclosure2.edinet-fsa.go.jp / api.edinet-fsa.go.jp (EDINET) | ✘403 | 未試(同系統で✘想定) | △ 直接ヒット少。決算短信は下記ミラー経由で要約が出る
- www.release.tdnet.info (TDnet) | ✘403 | ✘ | △ 決算短信PDFは storage-yahoo.jp / moneybox.jp / stockweather のミラーURLで検索に出る（開けない）
- finance-frontend-pc-dist.west.edge.storage-yahoo.jp（短信PDFミラー） | - | ✘ | ◯ 検索結果に短信PDFとして出て要約可
- www.jpx.co.jp | ✘403 | - | 未試
- 企業IR: www.fujikura.co.jp, www.sei.co.jp, www.seikoh-giken.co.jp, investor.lumentum.com, investors.ao-inc.com, www.coherent.com, investor.broadcom.com, nvidianews.nvidia.com | ✘403 | ✘(fujikura, lumentum確認) | ◯ プレスリリース本文の要約が取れる
- 株価: finance.yahoo.com, query1.finance.yahoo.com(API), finance.yahoo.co.jp, kabutan.jp, minkabu.jp, stooq.com, marketwatch.com, stockanalysis.com, companiesmarketcap.com, macrotrends.net | ✘403 | ✘(kabutan, stockanalysis確認) | ◯ 「<ticker> stock price <日付>」で直近終値・時価総額の要約が出る（日付必ず確認）
- pypi.org（yfinance等のインストールは可） | ◯200 | - | ただし yfinance の取得先 yahoo が✘なので実質使えない
- 業界調査: www.lightcounting.com, www.yolegroup.com, www.dell-oro.com, www.trendforce.com | ✘403 | - | ◯ プレスリリース/ニュースレター要約が取れる（有料本文は不可）
- ニュース: www.reuters.com, www.bloomberg.com, www.nikkei.com, seekingalpha.com | ✘403 | - | ◯ 見出し・要約レベル
- 業界メディア: www.semiconductor-today.com, www.lightwaveonline.com, www.fiercenetwork.com, www.semianalysis.com | ✘403 | ✘(semiconductor-today確認) | ◯
- 財務DB: irbank.net, www.buffett-code.com | ✘403 | - | △
- 台湾/中国: mops.twse.com.tw, www.cninfo.com.cn | ✘403 | - | △ 未試（英語ニュース経由が現実的）
- en.wikipedia.org | ✘403 | ✘ | ◯
- web.archive.org / archive.org / r.jina.ai | ✘ | - | 迂回不可（ポリシー上も試さない）
- 為替: www.boj.or.jp, www.federalreserve.gov | ✘403 | - | ◯ 「USD JPY rate <日付>」で要約取得
- github.com / api.github.com | ◯200 | ◯ | 本リポジトリ用
