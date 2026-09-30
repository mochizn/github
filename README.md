# US 大型株 値動きレポート

時価総額100億ドル以上の米国株のうち、当日 ±5% 以上動いた銘柄を抽出し、値動きの理由を日本語でまとめます。

## 仕組み
1. **抽出**: Yahoo Finance のスクリーナー（`yfinance.screen`）で「米国取引所・時価総額 ≥ $10B・騰落率 ≥ +5% または ≤ -5%」の銘柄を取得
2. **材料収集**: 各銘柄の直近ニュース見出しを取得
3. **要約**: Claude API（Web検索つき）に見出しを渡し、理由を表形式で要約。見出しで分からない銘柄は Claude が Web 検索で確認

## セットアップ
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # 要約に使用（--no-ai なら不要）
```

## 使い方
```bash
python us_movers.py                  # レポートを標準出力へ
python us_movers.py -o report.md     # ファイルに保存
python us_movers.py --no-ai          # AI要約なし（ニュース見出しの列挙のみ）
python us_movers.py --min-cap 5e10 --threshold 3   # 条件変更
```

## 注意
- 取引時間中に実行すると途中経過の騰落率になります。終値ベースにしたい場合は米国市場の引け後（日本時間の早朝）に実行してください。
- Yahoo Finance の非公式APIを使っているため、仕様変更で動かなくなることがあります。
- 投資判断は自己責任で。AIの要約は誤りを含む可能性があります（情報源URLを併記します）。
