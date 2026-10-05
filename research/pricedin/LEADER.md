# リーダー記録（v2: 織り込み分析）

## 予算ルール
- **ユーザー指示（2026-10-05 16:10 UTC）: この研究は使用量100%まで使ってよい**
- 7日枠 0.90 またはラウンド10で最終ラウンドへ、0.97 で停止
- 5時間枠（ユーザー要望で上限近くまで使う）:
  - 0.75 未満 → 全員でラウンド
  - 0.75〜0.95 → **部分ラウンド**: 1人あたりの消費見込み（直前ラウンドの5時間枠の増分÷人数×1.2）を足しても 0.97 を超えない人数だけ、優先度順に動かす
  - 0.95 以上 → リセット＋2分で再開
  - 子はこまめに push するので、途中で上限に当たっても失うのは最後の小さな単位だけ。リセット後に「続きから」で再開
- 子セッションを1時間以上止めない（キャッシュ失効で再読み込みが高くつく）

## 環境
- ネットワーク許可済み（ユーザーが追加）: SEC（www/efts/data）、TDnet、EDINET、各社IR、Yahoo Finance チャートAPI（query1/2）、kabutan、marketbeat 等。確認済み: SEC全文検索・EDGAR submissions・Yahoo 1年日足（5803.T, LITE）は 200。investor.corning.com は Cloudflare で 403（サイト側）

## ラウンド記録
| ラウンド | 開始(UTC) | 7日枠 | 5時間枠 | 要点 |
|---|---|---|---|---|
| 1 | 2026-10-05T16:09 | (要確認) | (要確認) | 初期プロンプト（agent3: 株価データ基盤、agent1/2: 会社の言葉、agent4: 設備投資・業界イベント年表、agent5: 構成と仮説リスト） |

## セッション
- agent1 日本株: session_018Hq4bGzgkMHRbsZt7V5T3Z
- agent2 米国株A: session_01DfMzByb4gX63zvCMgFRfcu
- agent3 米国株B＋データ: session_01HkfWKG1QPG26bE5TvELrJN
- agent4 業界横断: session_011tTRAcK9ysbnh7QKxbLzcD
- agent5 織り込まれていないこと・統合: session_01Wtb7Qix7q1vGzCXFmDW7Ke
