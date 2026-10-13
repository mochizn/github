# kaiji — 適時開示 受注・定性情報ボット

TDnet(適時開示情報閲覧サービス)の開示を毎日収集し、**受注・契約獲得**や**業績修正の理由**、
**決算短信の定性情報(経営成績の概況・見通し・受注高への言及)** を抽出してSQLiteに蓄積します。
後から**全文検索**で振り返れます。

```
TDnet一覧 ──▶ タイトル分類 ──▶ PDF本文抽出 ──▶ ルール抽出(受注金額/相手先/納期/理由/定性情報/シグナル)
                                                    │            └─▶ (任意) Claude で要約
                                                    ▼
                              SQLite + FTS5(trigram) ──▶ CLI検索 / Web UI / 単一HTML / Discord・Slack通知
```

## できること

| 機能 | 内容 |
|---|---|
| 収集 | TDnetの一覧を日付指定で取得(TDnetで閲覧できるのは直近約1か月) |
| 分類 | 受注・契約獲得 / 業績予想修正 / 決算短信 / 提携 / 新製品・新事業 / 採択・補助金 / 中計 / M&A / 特別損益 / 月次 など16分類 |
| 受注抽出 | 受注先・内容・**金額(円換算。外貨は注記の円換算額を優先)**・納期・売上計上時期・「売上高の10%以上」等・業績影響 |
| 業績修正 | 修正理由の本文、上方/下方の判定 |
| 決算短信 | 経営成績の概況(定性情報)、業績予想・見通し、**受注高・受注残高の数値と前年比**、受注への言及文 |
| シグナル | 「過去最高」「上方修正」「需要拡大」「価格改定」/「下回る」「遅延」「減損」等を含む文をポジ/ネガで抽出 |
| 検索 | 全文検索(2文字語もOK、`-語`で除外、`"…"`でフレーズ)、銘柄・カテゴリ・期間・金額・上方/下方で絞り込み |
| 振り返り | 銘柄ごとの開示タイムライン(受注高・受注残の推移表つき)、受注一覧(金額順ソート可) |
| スクリーニング | 決算短信の受注高・受注残高を前年比でランキング(例: 受注高 前年比+30%以上) |
| 通知 | 重要度の高い開示とウォッチリスト銘柄を Discord / Slack へ |
| AI要約(任意) | `KAIJI_LLM=1` で Claude による要約・要点・業績影響・キーワード付与 |

## セットアップ

```bash
pip install -e .            # AI要約も使うなら: pip install -e ".[llm]"
python -m kaiji collect --days 30     # 過去1か月分を収集(PDF処理込みで数十分)
python -m kaiji serve                 # http://127.0.0.1:8765
```

以後は1日数回 `python -m kaiji run` を実行すれば、直近2日分の新着を取り込み、通知し、`data/archive/` に月別アーカイブを書き出します。

## 使い方(CLI)

```bash
# 全文検索
python -m kaiji search 受注 半導体
python -m kaiji search データセンター -c earnings --since 2026-10-01
python -m kaiji search '"過去最高"' --code 6227
python -m kaiji search 値上げ -c forecast --direction up

# 受注一覧(金額10億円以上、金額順)
python -m kaiji orders --min 10億 --sort amount

# 決算短信の受注高・受注残高を前年比順に(+30%以上)
python -m kaiji metrics --min-yoy 30
python -m kaiji metrics --code 6432

# 銘柄の開示タイムライン / 詳細
python -m kaiji company 6227
python -m kaiji show 140120260928541186 --full

# ウォッチリスト(この銘柄の開示は重要度に関係なく通知)
python -m kaiji watch add 6227 3776 --note 半導体
python -m kaiji search --watch -n 50

# 単一HTMLを生成(ブラウザで開くだけで検索できる。スマホに送っても使える)
python -m kaiji site --out site && open site/index.html

# その他
python -m kaiji stats
python -m kaiji notify --dry-run --since 2026-10-01   # 通知内容の確認
python -m kaiji reprocess --since 2026-10-01          # 抽出ロジック改善後の再抽出
python -m kaiji export / import                       # アーカイブ(月別gzip JSONL) ⇔ DB
```

カテゴリキー: `order` 受注 / `forecast` 業績修正 / `earnings` 決算短信 / `alliance` 提携 / `new_biz` 新製品・新事業 /
`subsidy` 採択・補助金 / `mtp` 中計 / `ma` M&A / `extraordinary` 特別損益 / `monthly` 月次 / `shareholder` 還元 /
`capital` 資本政策 / `presentation` 説明資料 / `governance` 人事 / `fund` ETF・REIT / `other`

## 設定(環境変数)

| 変数 | 説明 |
|---|---|
| `KAIJI_DB` | DBファイル(既定 `data/kaiji.db`) |
| `KAIJI_ARCHIVE` | アーカイブ出力先(既定 `data/archive`) |
| `KAIJI_PDF_CACHE` | 指定するとPDFをキャッシュ(再抽出が高速) |
| `KAIJI_DISCORD_WEBHOOK` / `KAIJI_SLACK_WEBHOOK` | 通知先 |
| `KAIJI_LLM=1` | Claude 要約を有効化(`ANTHROPIC_API_KEY` 等の認証が必要) |
| `KAIJI_LLM_MODEL` | 既定 `claude-opus-5-5`。コストを抑えたい場合は `claude-haiku-5-5` 等 |
| `KAIJI_LLM_MAX_PER_RUN` | 1回の要約件数上限(既定30) |
| `KAIJI_LLM_CATEGORIES` | 要約対象カテゴリ(既定 order,forecast,earnings,mtp,alliance,new_biz,subsidy) |

通知は既定で重要度2以上(受注・業績修正=3、決算短信・提携・新事業・採択・中計・M&A・特別損益=2)。`run --min-importance 3` で受注と業績修正だけに絞れます。

## GitHub Actions で自動運用

`.github/workflows/collect.yml` が平日 JST 12:10 / 15:40 / 17:10 / 19:10 / 22:10 に `kaiji run` を実行します。
DBはActionsキャッシュで引き継ぎ、通知済みフラグも保持されます。

1. Settings → Secrets and variables → Actions
   - Variable `KAIJI_ENABLED=true`(スケジュール実行の有効化)
   - Secret `KAIJI_DISCORD_WEBHOOK` または `KAIJI_SLACK_WEBHOOK`(通知)
   - (任意) Variable `KAIJI_LLM=1` と Secret `ANTHROPIC_API_KEY`
2. 長期保存したい場合は**非公開**のデータ用リポジトリを作り、
   Variable `KAIJI_DATA_REPO=owner/repo` と Secret `KAIJI_DATA_TOKEN`(そのリポジトリへの contents 書き込み権限のある Fine-grained PAT)を設定。
   月別アーカイブが `kaiji-data` ブランチに蓄積され、キャッシュが消えても自動復元されます。
3. 初回は Actions → collect → Run workflow で `days=30` を指定すると過去1か月分をバックフィルします。

> **注意:** このリポジトリは公開リポジトリです。TDnetの掲載情報(を加工したもの)を公開の場に保存・配布すると
> 利用規約上問題になり得るため、ワークフローは公開リポジトリ自身へのデータ保存や成果物のアップロードを行いません
> (`KAIJI_ALLOW_PUBLIC_DATA=true` で明示的に許可しない限り)。個人利用の範囲で、データは非公開の場所に置いてください。
> また、TDnetへのアクセスは1秒間隔に抑えています。

## 仕組みのメモ

- **検索**: SQLite FTS5 の trigram トークナイザ(日本語の分かち書き不要)。trigram では2文字語(例:「受注」)が引けないため、3文字未満の語は `instr` で補完しています。
- **金額**: `約45億円` `20.4百万USドル(3,212百万円)` `1億2,000万円` `147,000,000円` などを円に正規化。外貨のみの場合は注記の「円換算」額を採用。非開示の場合は「売上高の10%以上」等の規模表記を保持。
- **PDF**: pypdfium2 で抽出(失敗時は pdfplumber → pypdf)。画像のみのPDFや文字コード表の無いPDF(全体の1%未満)は本文なしとして記録します。
- **決算短信**: 冒頭8ページから目次・ページ番号・ランニングヘッダを除去し、「経営成績の概況」「将来予測情報」等の見出し単位で切り出し。財務諸表本文は保存しません。
- **アーカイブ**: `data/archive/YYYY/YYYY-MM.jsonl.gz`(id順・mtime固定でgit差分が最小)。`kaiji import` でDBを再構築できます。
- ルールで拾いきれない書式もあるため、詳細画面から必ず原文PDFを確認してください。投資判断は自己責任で。

## 開発

```bash
pip install -e ".[dev,llm]"
pytest -q
```
