# agent1 ノート

## サイクル1（2026-10-03）全体像と先行研究の一次スキャン

注意: この環境では arxiv.org への WebFetch がプロキシで遮断される。arXiv 論文の内容は検索結果の要約経由で取得しており、本文を直接確認できていない（→ agent4 に検証依頼）。anthropic.com は本文取得できた。

### A. 実運用事例（エンジニアリング記事）
1. **Anthropic: マルチエージェント研究システム**（本文確認済） https://www.anthropic.com/engineering/multi-agent-research-system
   - orchestrator-worker 型（リード1＋並列サブエージェント）。Opus 4 リード＋Sonnet 4 サブで単一 Opus 4 比 +90.2%（社内評価）。
   - BrowseComp で性能分散の80%はトークン使用量だけで説明、ツール呼び出し数・モデル選択を加えて95%。→ 「マルチエージェントの利得の多くは単に多くトークンを使えること」示唆。
   - トークン消費: エージェントはチャットの約4倍、マルチエージェントは約15倍。
   - 努力量スケーリング規則をプロンプトに明記（単純:1エージェント3〜10ツール呼び出し／比較:2〜4サブ／複雑:10+）。
   - 失敗例: 単純な問いに過剰なサブエージェント、タスク記述が曖昧で重複作業、SEOコンテンツファームを優先。
   - サブへの指示には「目的・出力形式・ツール/情報源の指針・明確な境界」が必要。
   - 長時間タスクでは完了フェーズを要約し外部メモリに保存。
   - 向かない用途: 全員が同じ文脈を要する／相互依存が強い／リアルタイム協調。
2. **Anthropic: 16並列 Claude で C コンパイラ構築**（本文確認済） https://www.anthropic.com/engineering/building-c-compiler
   - 16エージェント並列、git ベース同期。`current_tasks/` にテキストファイルを書いてタスクをロック→push。マージ衝突は Claude が自力解決。
   - 役割分化あり: 重複コード統合役、性能改善役、ドキュメント役、コード品質批評役。
   - 約2,000セッション/2週間、入力20億・出力1.4億トークン、約$20,000。
   - 「極めて質の高いテスト」が自律運用の鍵（客観的な検証器）。
   - 失敗: 巨大な一枚岩タスク（Linuxカーネル）では全員が同じバグに当たり互いの修正を上書き → GCC をオラクルとした比較テストで分割して解決。
3. **Anthropic: Effective harnesses for long-running agents** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents （検索要約経由、本文未確認）
   - 初期化エージェントが init.sh・進捗ファイル（claude-progress.txt）・初回コミットを用意、以後のセッションは進捗ファイル＋git履歴で状態復元し少しずつ進める。

### B. 役割分化・構造化（問い1・2関連）
4. **MetaGPT**（ICLR 2024）https://arxiv.org/abs/2308.00352 — SOP（標準作業手順）で役割（PM/Architect/Engineer/QA）を固定、自由会話ではなく構造化ドキュメントを受け渡し。共有メッセージプール＋publish-subscribe で各役割が必要な情報だけ購読。「カスケード幻覚」を抑制すると主張。
5. **ChatDev** https://arxiv.org/abs/2307.07924 — instructor-assistant の2者対話をチェーン化。（本文未確認）
6. **Blackboard 型**: https://arxiv.org/abs/2510.01285 — 中央エージェントが黒板に依頼を掲示し、能力ある下位エージェントが自発的に応答。ベースライン比 13〜57% 相対改善（データサイエンス情報探索）。→ 本プロジェクトの BOARD.md はこの型に近い。

### C. 議論・批判役の効果（問い1・3関連）— 賛否が割れている
7. **Du et al. 2023 Multiagent Debate** https://arxiv.org/abs/2305.14325 — 複数インスタンスが複数ラウンド議論すると事実性・推論が向上。不確かな事実は意見が割れて最終回答から落ちやすい。
8. **反証側**: 同一トークン予算では CoT self-consistency が debate や Reflexion を上回ることが多い。debate は前ラウンドに条件付けるため多様性が減り誤答にトンネルしやすい。https://aclanthology.org/2024.emnlp-main.1112.pdf
9. **"If Multi-Agent Debate is the Answer, What is the Question?"** https://arxiv.org/abs/2502.08788 — 既存MAD手法は CoT/SC を安定して上回れない。モデルの異質性（heterogeneity）を推奨。（要約経由）
10. **同調・追従（sycophancy）**: debate では正→誤の変化の方が誤→正より多い、ラウンドを重ねると全員一致の誤答が増える。https://arxiv.org/abs/2509.05396 , https://arxiv.org/abs/2509.23055 （要約経由、数値は未確認）
11. **反論の反論**: プロトコル設計次第で同予算でも SC を上回る（ColMAD）https://arxiv.org/html/2510.20963v2 （要約経由）

### D. 失敗分析（問い3）
12. **MAST: Why Do Multi-Agent LLM Systems Fail?** https://arxiv.org/abs/2503.13657 — 1,642トレースから14の失敗モード、3分類: 仕様・システム設計（41.8%）、エージェント間の不整合（36.9%）、タスク検証（21.3%）。基盤モデルの限界より設計・協調の問題が主因と主張。（割合は二次要約経由、要確認）
13. **Sakana AI Scientist の独立評価**（Beel ら） https://arxiv.org/abs/2502.14297 , https://isg.beel.org/blog/2025/02/21/sakana-ai-scientist-evaluation/ — 文献レビューが弱い、実験の約半数（12中5）が失敗、原稿の一部に幻覚された数値、既知アイデアを新規と誤認、引用中央値5件で古い。→ 自律研究の典型的品質リスク。

### 論点（洗い出し）
- P1: マルチエージェントの利得は「トークン量」でほぼ説明できるのでは（A1, C8）。同予算の単一エージェントと比べないと役割分化の効果は言えない。
- P2: 批判役は有効か。同質モデル同士の議論は同調で劣化しうる（C10）→ 批判役には「出典の実在確認」など客観的タスクを与える方が良い（推測）。
- P3: 共有方式は「ファイル＋git」が実績あり（A2,A3）。タスクロック用ファイル（current_tasks/）の導入は重複防止に直接効く。本 PROTOCOL には着手宣言の仕組みが BOARD 頼みで粒度が粗い。
- P4: 検証器の有無が決定的（A2 のテスト、A1 の LLM-as-judge）。研究タスクには自動テストがないので「引用URLの到達性・引用文の一致チェック」が代替検証器になりうる（推測）。
- P5: 失敗の大半は設計（仕様・終了条件）由来（D12）→ PROTOCOL に終了条件・出力フォーマットの明示が重要。
- P6: 環境制約（arxiv 遮断など）が情報源の質を下げ、二次要約依存による幻覚リスクを生む。
