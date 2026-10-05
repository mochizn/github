# ENV（到達可否、1行1ドメイン）
- www.sec.gov / efts.sec.gov / data.sec.gov: ◯（UA必須）(leader, 2026-10-05)
- query1/query2.finance.yahoo.com v8 chart API: ◯ 1年日足が取れる（LITE, 5803.T 確認）(leader)
- www.release.tdnet.info / disclosure2.edinet-fsa.go.jp / www.fujikura.co.jp / kabutan.jp / www.marketbeat.com: ◯ トップページ200 (leader)
- investor.corning.com: ✘ Cloudflare 403（サイト側の防御）。SEC の 8-K/10-Q で代替 (leader)
- stooq.com CSV: ✘ タイムアウト（Yahoo で代替）(leader)
- Yahoo chart API: 1306.T（TOPIX ETF）の 2026-03-30/31 に 1/10 の誤値あり → fetch_prices.py で自動除外。^N225・JPY=X も取得可 (agent3, R1)
