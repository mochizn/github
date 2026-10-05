# リーダー記録（v2: 織り込み分析）

## 予算ルール
- 7日枠 0.50 で最終ラウンドへ、0.55 で停止（ユーザーの別指示があればそれに従う）
- 5時間枠 0.70 以上では新ラウンドを開始しない（リセット後すぐ再開）
- 子セッションを1時間以上止めない（キャッシュ失効で再読み込みが高くつく）

## 環境
- ネットワーク許可済み（ユーザーが追加）: SEC（www/efts/data）、TDnet、EDINET、各社IR、Yahoo Finance チャートAPI（query1/2）、kabutan、marketbeat 等。確認済み: SEC全文検索・EDGAR submissions・Yahoo 1年日足（5803.T, LITE）は 200。investor.corning.com は Cloudflare で 403（サイト側）

## ラウンド記録
| ラウンド | 開始(UTC) | 7日枠 | 5時間枠 | 要点 |
|---|---|---|---|---|
