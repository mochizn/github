# レポート: 無人・長時間のマルチエージェント共同研究の設計パターン

> 更新: agent5（まとめ役）／ 現在 **サイクル1（骨組み）**。各章の「暫定」は次サイクル以降に他エージェントの成果で置き換える。
> 凡例: [aN] は notes/agentN.md 由来。出典のない主張には **推測** と書く。⚠ は数値・内容が未検証（arxiv.org はこの環境から取得できず、二次要約経由）。

## 結論の要約
（最終サイクルで記入）

---

## 1. 役割分担: 何人で、どう分けると質が上がるか
**担当: agent2 ／ 状態: 暫定（agent1 のスキャン結果を反映）**

- **課題が分けられるなら orchestrator-worker 型が強い**: リード（Opus 4）＋並列サブエージェント（Sonnet 4）が、単一の Opus 4 を社内評価で +90.2% 上回った。ただし、相互依存が強い課題や全員が同じ文脈を要する課題には向かない。[a1][a5] https://www.anthropic.com/engineering/multi-agent-research-system
- **人数は課題の複雑さで変える**: 単純な課題は1エージェント（3〜10ツール呼び出し）、比較は2〜4、複雑な課題は10以上。単純な問いにサブエージェントを付けすぎるのは失敗例として挙がっている。[a1][a5] 同上
- **役割分化の実例**: 16並列で C コンパイラを作った事例では、重複コードの統合役・性能改善役・ドキュメント役・コード品質の批評役を置いた。[a1] https://www.anthropic.com/engineering/building-c-compiler
  MetaGPT は SOP で役割（PM/Architect/Engineer/QA）を固定し、構造化文書を受け渡すことで「カスケード幻覚」を抑えると主張している。[a1] https://arxiv.org/abs/2308.00352 ⚠
- **批判役・討論の効果は賛否が割れている**
  - 肯定: 複数インスタンスの討論で事実性と推論が向上した（Du et al.）。[a1][a5] https://proceedings.mlr.press/v235/du24e.html
  - 否定: トークン予算をそろえると CoT self-consistency が討論を上回ることが多い。https://aclanthology.org/2024.emnlp-main.1112.pdf ／ 既存の MAD 手法は CoT/SC を安定して上回れず、モデルの異質性が重要。https://arxiv.org/abs/2502.08788 ⚠ ／ 同調（sycophancy）でラウンドを重ねるほど全員一致の誤答が増える。https://arxiv.org/abs/2509.05396 ⚠ [a1]
  - 再反論: プロトコル設計次第では同じ予算でも SC を上回る（ColMAD）。https://arxiv.org/html/2510.20963v2 ⚠ [a1]
- **暫定の解釈（推測）**: マルチエージェントの利得の多くはトークン量で説明できる（§4）。そのため、役割分化の効果を主張するには同じ予算の単一エージェントとの比較が必要。批判役には「意見を述べる」よりも「出典の実在確認」のような客観的な検証タスクを与える方が同調に強いと考えられる。[a1 P1,P2]
- 未解決: 同質並列と役割分化を同じ予算で直接比較した研究／最適な人数

## 2. 同期・共有: 知見の共有方法と衝突・重複の防止
**担当: agent2 ／ 状態: 暫定**

- **ファイルと git による共有には実績がある**: C コンパイラの事例では、エージェントが `current_tasks/` にテキストファイルを書いてタスクをロックしてから push した。マージ衝突は Claude が自力で解決した。[a1] https://www.anthropic.com/engineering/building-c-compiler
- **成果はファイルに書き出し、受け渡しは参照だけにする**: 「伝言ゲーム」とトークンの浪費を避けるため。[a5] https://www.anthropic.com/engineering/multi-agent-research-system
- **委任の指示には目的・出力形式・ツール/情報源・境界を含める**: 曖昧だと重複作業や漏れが起きた。[a1][a5] 同上
- **Blackboard 型**: 中央が黒板に依頼を掲示し、能力のある下位エージェントが自発的に応答する方式で、ベースライン比 13〜57% の相対改善が報告されている。本プロジェクトの BOARD.md はこの型に近い。[a1] https://arxiv.org/abs/2510.01285 ⚠
  MetaGPT の publish-subscribe（必要な情報だけを購読）も同系統。[a1] https://arxiv.org/abs/2308.00352 ⚠
- **セッション間の記憶**: 進捗ファイル（claude-progress.txt）と git log を最初に読み、状態を復元する。[a1][a5] https://anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **一枚岩の課題では並列化が崩れる**: Linux カーネルのビルドでは全員が同じバグに当たり、互いの修正を上書きした。GCC をオラクルとする比較テストで課題を分割して解決した。[a1] https://www.anthropic.com/engineering/building-c-compiler
- 未解決: 掲示板・共有ファイル・直接メッセージの比較

## 3. 品質管理: 幻覚・薄い根拠・堂々巡りの検出と抑制
**担当: agent3（＋agent4 の検証） ／ 状態: 暫定**

- **失敗の主因は設計と協調で、基盤モデルの限界ではない**: MAST は14の失敗モードを3分類に整理した（仕様・システム設計／エージェント間の不整合／タスク検証）。[a1][a5] https://arxiv.org/abs/2503.13657
  ⚠ **割合は出典間で食い違っている**: 41.8/36.9/21.3%（a1、二次要約）と 44.2/32.3/23.5%（a5、検索要約）。論文の版の違いの可能性がある（推測）。→ agent4 に確認を依頼済み。
- **検証器の有無が決定的**: 自律運用の鍵は「極めて質の高いテスト」だった（C コンパイラの事例）。[a1] https://www.anthropic.com/engineering/building-c-compiler
  研究タスクでは、LLM-as-judge（事実・引用の正確さ、網羅性、情報源の質）＋人間レビュー、専用の citation エージェントが使われる。[a5] https://www.anthropic.com/engineering/multi-agent-research-system
  自動テストのない研究では「引用 URL に到達できるか・引用文と一致するか」の確認が代替の検証器になりうる（推測）[a1 P4]
- **早すぎる完了宣言と、半端なまま次に渡す失敗**: 対策は、項目ごとの合否リスト（`passes:false`）、テストの削除・改変の禁止、1セッション1項目。[a5] https://anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **自律研究で典型的な品質リスク**（AI Scientist の独立評価）: 文献レビューが弱い、実験の約半数が失敗、幻覚された数値、既知のアイデアを新規と誤認、引用が少なく古い。[a1] https://arxiv.org/abs/2502.14297 ⚠ , https://isg.beel.org/blog/2025/02/21/sakana-ai-scientist-evaluation/
- **情報源の制約が幻覚リスクを生む**: 本試運転では arxiv.org を取得できず、二次要約に頼らざるを得ない。実際に MAST の割合が食い違った（上記）。[a1 P6][a5]
- 未解決: 堂々巡り（同じ論点の繰り返し）の検出法

## 4. コスト: トークンあたりの成果を最大化する運用
**担当: agent3 ／ 状態: 暫定**

- **トークン量が性能をほぼ決める**: BrowseComp では性能分散の80%をトークン使用量だけで説明でき、ツール呼び出し数とモデル選択を加えると95%になる。マルチエージェントのトークン消費はチャットの約15倍（エージェント単体で約4倍）。→ 課題の価値がコストに見合う場合にだけ使う。[a1][a5] https://www.anthropic.com/engineering/multi-agent-research-system
- **実規模の例**: C コンパイラは約2,000セッション／2週間、入力20億・出力1.4億トークン、約 $20,000。[a1] https://www.anthropic.com/engineering/building-c-compiler
- **モデルの使い分け**: リードに上位モデル、ワーカーに下位モデル（Opus＋Sonnet）。[a1] 同上 multi-agent-research-system
- 未解決: サイクル間隔、打ち切り条件、同じ予算での単一エージェントとの比較

## 5. 結論: 本 PROTOCOL.md の改善提案
**担当: agent5 ／ 状態: 候補を収集中**

| # | 観察 | 提案 | 根拠 |
|---|---|---|---|
| P1 | 同時に起動すると、まとめ役にはサイクル1で統合する材料がほとんどない（agent1 の push は agent5 の作業中に届いた） | まとめ役の起動を他より遅らせる。または初回の役割を「骨組みのみ」と明記する | 本試運転の観察 [a5] |
| P2 | 着手宣言が BOARD の自由記述頼みで粒度が粗い | `tasks/` に1ファイル1タスクのロックファイルを置き、着手時に push する | C コンパイラ事例 https://www.anthropic.com/engineering/building-c-compiler [a1 P3] |
| P3 | 問いごとの進捗状態が機械的に読めない | BRIEF の各問いに状態表（回答済み/根拠数/未解決の疑義）を置く | 要件 JSON 方式 https://anthropic.com/engineering/effective-harnesses-for-long-running-agents |
| P4 | 失敗の多くは仕様・終了条件の設計に由来する | 依頼のテンプレート（目的・出力形式・情報源・境界・終了条件）を PROTOCOL に入れる | MAST https://arxiv.org/abs/2503.13657 ⚠／Anthropic [a1 P5] |
| P5 | 一次情報源（arxiv）を取得できず、二次要約の数値が食い違う | 情報源の取得可否を事前に確認する。二次情報由来の数値には ⚠ を付ける規則を設ける | 本試運転の観察 [a1 P6][a5] |
| P6 | 同質モデルの批判役は同調しやすい（⚠） | 批判役の仕事を「出典 URL の到達と引用一致の確認」など客観的なチェックリストに寄せる | https://arxiv.org/abs/2509.05396 ⚠ [a1 P2]（推測を含む） |
| P7 | BOARD の衝突 | 観察: サイクル1では agent1 と agent5 が BOARD を同時に編集したが、rebase は自動で成功した（行が離れていたため）。隣接行での衝突は未観測なので、この提案は保留 | 本試運転の観察 [a5] |

---

## 付録: 未解決の疑義
- MAST の3分類の割合が出典間で不一致（§3）→ @agent4
- arXiv 2502.08788 の題名が検索結果によって異なる（"If Multi-Agent Debate is the Answer, What is the Question?" と "Stop Overvaluing Multi-Agent Debate"）。改題の可能性がある（推測）→ @agent4
