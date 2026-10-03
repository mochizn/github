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
9. **"If Multi-Agent Debate is the Answer, What is the Question?"**（**[訂正 C2]** 同じ論文の初版タイトル。改訂版は "Stop Overvaluing Multi-Agent Debate"。agent4 の V5 による） https://arxiv.org/abs/2502.08788 — 既存MAD手法は CoT/SC を安定して上回れない。モデルの異質性（heterogeneity）を推奨。（要約経由）
10. **同調・追従（sycophancy）**: debate では正→誤の変化の方が誤→正より多い、ラウンドを重ねると全員一致の誤答が増える。https://arxiv.org/abs/2509.05396 , https://arxiv.org/abs/2509.23055 （要約経由、数値は未確認）
11. **反論の反論**: プロトコル設計次第で同予算でも SC を上回る（ColMAD）https://arxiv.org/html/2510.20963v2 （要約経由）

### D. 失敗分析（問い3）
12. **MAST: Why Do Multi-Agent LLM Systems Fail?** https://arxiv.org/abs/2503.13657 — 1,642トレースから14の失敗モード、3分類: 仕様・システム設計（41.8%）、エージェント間の不整合（36.9%）、タスク検証（21.3%）。基盤モデルの限界より設計・協調の問題が主因と主張。（割合は二次要約経由、要確認）**[訂正 C2] 割合は版によって異なる。サイクル2 の E1 を参照**
13. **Sakana AI Scientist の独立評価**（Beel ら） https://arxiv.org/abs/2502.14297 , https://isg.beel.org/blog/2025/02/21/sakana-ai-scientist-evaluation/ — 文献レビューが弱い、実験の約半数（12中5）が失敗、原稿の一部に幻覚された数値、既知アイデアを新規と誤認、引用中央値5件で古い。→ 自律研究の典型的品質リスク。

### 論点（洗い出し）
- P1: マルチエージェントの利得は「トークン量」でほぼ説明できるのでは（A1, C8）。同予算の単一エージェントと比べないと役割分化の効果は言えない。
- P2: 批判役は有効か。同質モデル同士の議論は同調で劣化しうる（C10）→ 批判役には「出典の実在確認」など客観的タスクを与える方が良い（推測）。
- P3: 共有方式は「ファイル＋git」が実績あり（A2,A3）。タスクロック用ファイル（current_tasks/）の導入は重複防止に直接効く。本 PROTOCOL には着手宣言の仕組みが BOARD 頼みで粒度が粗い。
- P4: 検証器の有無が決定的（A2 のテスト、A1 の LLM-as-judge）。研究タスクには自動テストがないので「引用URLの到達性・引用文の一致チェック」が代替検証器になりうる（推測）。
- P5: 失敗の大半は設計（仕様・終了条件）由来（D12）→ PROTOCOL に終了条件・出力フォーマットの明示が重要。
- P6: 環境制約（arxiv 遮断など）が情報源の質を下げ、二次要約依存による幻覚リスクを生む。

## サイクル2（2026-10-03 02:3x UTC）依頼対応＋未カバー領域

### 依頼への対応
- **@agent4 V1（MAST の割合が食い違う件）→ 一次資料で確認し、第3の値が見つかった。**
  公式リポジトリの README（raw.githubusercontent.com 経由で取得、[原文確認]）https://raw.githubusercontent.com/multi-agent-systems-failure-taxonomy/MAST/main/README.md に載っている分類図 `assets/taxonomy_v11_cropped-1.png`（https://raw.githubusercontent.com/multi-agent-systems-failure-taxonomy/MAST/main/assets/taxonomy_v11_cropped-1.png ）を画像として目視確認した。図の値は次のとおり。
  - Poor Specification **37.17%**（1.1 タスク仕様違反 15.2 / 1.2 役割仕様違反 1.57 / 1.3 手順の繰り返し 11.5 / 1.4 会話履歴の喪失 2.36 / 1.5 終了条件を認識しない 6.54）
  - Inter-Agent Misalignment **31.41%**（2.1 会話リセット 5.50 / 2.2 確認質問をしない 2.09 / 2.3 タスク脱線 5.50 / 2.4 情報の出し惜しみ 6.02 / 2.5 他エージェントの入力を無視 4.71 / 2.6 推論と行動の不一致 7.59）
  - Task Verification **31.41%**（3.1 早すぎる終了 8.64 / 3.2 検証なし・不十分 9.16 / 3.3 誤った検証 13.61）
  - → 少なくとも3つの版がある（41.8/36.9/21.3、44.2/32.3/23.5、37.17/31.41/31.41）。図のファイル名は v11 だが、どの論文版に対応するかは不明（推測不可）。**提案: REPORT では一つの数値に寄せず、「版によって 37〜44 / 31〜37 / 21〜31%」と幅で示し、順位（仕様 ≥ 協調 ≳ 検証）だけを結論に使う。** 3分類がほぼ均等である以上、「検証の失敗は少数派」と言い切るのは危険（MAST の版次第）。
  - 本研究に直接関係する FM: 1.3 手順の繰り返し（堂々巡り、11.5%）、1.5 終了条件を認識しない（6.54%）、3.1 早すぎる終了（8.64%）、3.3 誤った検証（13.61%）。
- **@agent4 C9 のタイトル** → 2502.08788 の初版タイトルと改訂版タイトルであることを確認し、ノートを訂正した。
- **@agent2 の境界の質問** → 合意する。agent1 は「広く一覧化し、論点・出典を投げる」まで。深掘り（数値の裏取り、比較）は agent2/3 が担う。agent1 はサイクル2以降、(a) 誰も見ていない領域の発掘、(b) 一次資料に到達できる経路の探索（後述 E5）に集中し、深掘り領域には入らない。

### 未カバー領域の調査
- **E2. Anthropic「マルチエージェントをいつ使うか」**（本文確認済）https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them
  - マルチエージェントが割に合うのは3場面だけ: 文脈の保護（無関係な情報の隔離）、並列探索、専門化（ツールが20を超える場合など）。
  - 「マルチエージェントは、単一エージェントのほうが良い場面に適用されがち」「単一エージェントのプロンプトを改善したら同等の結果が出た」。
  - トークンは単一エージェント比で**3〜10倍**（文脈の重複、調整メッセージ、受け渡し時の要約）。※研究システム記事の「チャット比15倍」とは比較対象が違う点に注意。
  - **分解の原則: 問題の種類別（計画／実装／テスト／レビュー）で分けると、受け渡しのたびに情報が失われ逆効果。文脈の共有単位で分けるべき。** → 本プロトコルの役割（調査／深掘り／批判／まとめ）は「問題の種類別」分割に近く、この指摘がそのまま当てはまる（推測。agent2・agent5 へ）。
  - 検証サブエージェントは安定して成功しているが、強いオーケストレーターは別の検証段を挟まず直接評価する傾向。
- **E3. Anthropic「Effective context engineering」**（本文確認済）https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - 長時間タスクの3手法: compaction（要約して続行）、構造化ノート（文脈外に記録し後で読み戻す）、サブエージェント（詳細は隔離し、要約だけ返す）。往復が多い作業は compaction、マイルストーンが明確な反復作業はノート、並列探索はマルチエージェントが向く。→ 本プロジェクトの notes/ は「構造化ノート」型にあたる。
- **E4. 反対の立場: Cognition「Don't Build Multi-Agents」** https://cognition.com/blog/dont-build-multi-agents （cognition.ai / cognition.com とも遮断されており、検索要約経由）
  - 原則: (1) 文脈を共有せよ（エージェントの全トレースを渡す）、(2) 行動には暗黙の決定が含まれ、並列エージェント間で衝突する（Flappy Bird の例: 背景担当と鳥担当で様式がバラバラになる）。並列サブエージェントの結果を後で結合する構成は「とても脆い」。
  - 問い1への含意: 並列の書き手が多いほど暗黙の決定が衝突する。共有ファイルに「決定事項」欄を設けて暗黙の決定を明示化する、という対策が考えられる（推測）。
  - agent4 が BOARD に書いた「Cognition 立場の更新」は自分では確認できていない（遮断のため）。
- **E5. AutoGen の終了条件**（ソースコードで確認、[原文確認]）https://raw.githubusercontent.com/microsoft/autogen/main/python/packages/autogen-agentchat/src/autogen_agentchat/conditions/__init__.py
  - 用意されている終了条件: MaxMessage, TextMention, StopMessage, TokenUsage, Handoff, Timeout, External, SourceMatch, TextMessage, FunctionCall, Functional。ドキュメント（遮断のため検索要約経由）によれば `|`（OR）と `&`（AND）で組み合わせられる https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/termination.html
  - → 問い4: 実用フレームワークは「回数・トークン・時間・明示的な完了宣言・外部停止」を OR で併用するのが標準。本プロトコルは「3サイクル」という回数制限だけで、トークン上限や「成果なしで停止」の条件がない。
- **E6. CAMEL の失敗モード** https://arxiv.org/abs/2303.17760 （NeurIPS 2023、検索要約経由）
  - ロールプレイでの4つの失敗: 役割の入れ替わり、指示のオウム返し、「やります」とだけ言って実行しない空返事、終わらないループ（お礼や挨拶を繰り返す）。終了は `<CAMEL_TASK_DONE>` トークンで行う。
  - → 本プロジェクトで起こりうる対応物（推測）: BOARD 上の依頼の応酬だけで中身が増えない「空返事」。検出指標として agent3 の「新規出典数/サイクル」が有効そう。
- **E6b. MemGPT／エージェント記憶のサーベイ** https://github.com/Shichun-Liu/Agent-Memory-Paper-List （検索要約経由）: 文脈内のコアメモリと外部のアーカイブ記憶を階層化する。本プロジェクトの規模では、git のノートで十分と判断（推測）。

### 一次資料にアクセスできる経路（全員向け）
- 使える: anthropic.com、claude.com、**raw.githubusercontent.com**（論文の公式リポジトリの README・図・コードが読める。MAST はこれで確認できた）
- 遮断されている: arxiv（export. を含む）、semanticscholar（API を含む）、r.jina.ai、cognition.ai/.com、langchain.com、microsoft.github.io、api.github.com（スコープ外）
- → 数値を検証するときは、論文の公式 GitHub リポジトリの README・図を raw で取りに行くのが現実的。

### 論点の追加
- P7: 役割を「問題の種類別」に分ける（調査→深掘り→批判→まとめ）と、受け渡しで情報が失われる（E2）。代替案として、問いごとに「調査＋深掘り＋自己検証」を1人が受け持つ「文脈単位」の分割がある。批判役は外部ツールで検証する専任として残す（推測）。
- P8: 暗黙の決定の衝突（E4）。共有ファイルに「決定事項ログ」を置くべきでは。
- P9: 終了条件を複合にする（回数 OR トークン OR 新規成果ゼロ）（E5, E6）。
- P10: 「MAST は検証失敗が少数派」という主張は版依存で不安定（E1）。
