# agent2 ノート

## サイクル1（2026-10-03）

担当: 問い1（役割分担）・問い2（同期・共有）。
**注意（検証度）**: この環境では arxiv.org / huggingface.co / research.google への直接取得がプロキシで遮断されていた。以下の論文の数値は Web 検索結果の要約経由で、原文PDF未確認のものに `[要約経由]` を付ける。原文を確認できたのは Anthropic のブログのみ `[原文確認]`。@agent4 の検証対象として優先度高。

### 問い1: 役割分担（人数・同質並列 vs 役割分化・批判役）

**1-a. 「人数を増やせば良い」は条件付き**
- 同一モデルの単純サンプリング＋多数決でも、エージェント数を増やすと性能はスケールする。ただし利得はタスク難度に対して山型で、一定の難度を超えると頭打ち。`[要約経由]` Li et al. "More Agents Is All You Need" https://arxiv.org/abs/2402.05120
- 180構成の比較実験（単一 / Independent / Centralized / Decentralized / Hybrid × 3モデル系列）で、並列化可能なタスクでは Centralized が +80.8%、一方で逐次的な推論タスクでは全マルチエージェント構成が 39〜70% 劣化。`[要約経由]` Kim et al. "Towards a Science of Scaling Agent Systems" https://arxiv.org/abs/2512.08296 / https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
- 同論文: 相互チェックのない Independent 構成はエラーを 17.2倍に増幅、Centralized（オーケストレータが検証のボトルネックになる）は 4.4倍に抑制。`[要約経由]` 同上
- Anthropic の Research 機能: リード（Opus 4）＋サブエージェント（Sonnet 4）構成が単一エージェント比 +90.2%。ただしトークンはチャットの約15倍、性能分散の80%はトークン使用量だけで説明される。人数目安は「単純な事実確認は1体・3〜10ツール呼出、比較は2〜4体、複雑な調査は10体超で責任を明確に分割」。`[原文確認]` https://www.anthropic.com/engineering/multi-agent-research-system

**1-b. 同質並列 vs 役割分化**
- 同じ役割を複製しても利得はほぼない（<0.5%）、異なる補完的役割が多様性を保つ、という報告。異種モデル混成（X-MAS）は同質構成より最大 +47%（AIME-2024）。`[要約経由]` https://arxiv.org/html/2606.20629 , https://pith.science/paper/2505.16997
- MetaGPT は SOP（標準作業手順）に沿って役割を固定し、各役割に構造化成果物（PRD・設計書など）を出させることで成功率が上がったとする。`[要約経由]` https://arxiv.org/abs/2308.00352

**1-c. 批判役（debate / critic）の効果は「やり方次第」**
- 原実装のままの Multi-Agent Debate は self-consistency 等のアンサンブルを上回らない。ただし「同意の強さ（agreement intensity）」をプロンプトで調整すると最下位→最上位に変わった。→批判役は存在より**どれだけ反対させるか**が効く。`[要約経由]` Smit et al. "Should we be going MAD?" https://arxiv.org/abs/2311.17371
- 議論を続けると迎合（sycophancy）が伝播し、3ラウンド目には当初意見が割れた問題の 23.9% が「全員一致で誤答」に収束。`[要約経由]` https://arxiv.org/html/2604.02668
- 失敗分解: 多数派への迎合（最大85.5%）、他者の根拠で正答が崩れる脆弱性（最大70%）、多数決が正答を捨てる（最大32.3pt）。`[要約経由]` https://arxiv.org/pdf/2509.23055 （※この数値の出典論文が 2509.23055 か 2605.00914 か検索要約では曖昧。要確認）
- 対策例: 矛盾が出たら、元の推論を見せずに「主張と根拠だけ」を新しい検証役に渡して独立評価させる（迎合回避）。`[要約経由・実践記事]` https://github.com/liatrio-labs/claude-code-gauntlet/blob/main/docs/research/artifacts/14-inter-agent-debate-and-challenge-rounds.md

**1-d. 失敗の大半は設計・仕様由来**
- MAST（150トレース, κ=0.88, 14失敗モード, 3カテゴリ）: 仕様/システム設計 約42%、エージェント間の不整合 約37%、検証・終了 約21%。役割の曖昧さ、重複役割、終了条件の欠落が典型。`[要約経由]` Cemri et al. "Why Do Multi-Agent LLM Systems Fail?" https://arxiv.org/abs/2503.13657

**問い1 暫定結論（推測を含む）**
- 本テーマ（Web調査＝並列化しやすい）では役割分化＋中央集約型が有利という根拠は比較的強い（Anthropic, Kim et al.）。
- ただし「批判役を置けば品質が上がる」は無条件ではない。批判役は (i) 他者の推論ではなく**主張と出典**を検証する、(ii) 合意圧から独立させる、ことが条件（推測：上記 MAD/迎合研究からの外挿）。
- 本プロトコルの5人構成は、掘り下げ役2人が問いで分割されているので「同役割の複製」問題は避けられている。一方、まとめ役が唯一の集約点で、Centralized の「検証ボトルネック」役を agent4 と agent5 のどちらが担うかが曖昧（推測）。

### 問い2: 同期・共有

**2-a. 共有方法の3類型**
- (A) 中央経由（リードが全結果を受け取る）: Anthropic の基本形。ただし付録で「サブエージェントは成果をファイル等に永続化し、コーディネータには軽量な参照だけ返す」ことを推奨（会話履歴経由のコピーでトークン浪費・劣化を防ぐ）。`[原文確認]` https://www.anthropic.com/engineering/multi-agent-research-system
- (B) 黒板（blackboard）型: 全員が読み書きする共有ボードに要求を掲示し、能力のあるエージェントが自発的に応答。データサイエンスの情報探索でベースライン比 13〜57% 相対改善。`[要約経由]` https://arxiv.org/abs/2510.01285 , https://arxiv.org/abs/2507.01701
- (C) Publish-Subscribe: MetaGPT は共有メッセージプールに構造化メッセージを発行し、各役割は自分に関係する型だけ購読（情報過多を防ぐ）。前提メッセージが揃うまで役割は動かない。`[要約経由]` https://arxiv.org/abs/2308.00352
- 本プロトコル（BOARD.md + notes/）は (B) 黒板型＋ファイル永続化で、Anthropic 推奨の「成果は永続化、参照だけ共有」に近い。

**2-b. 重複作業の防ぎ方**
- Anthropic: 初期はサブエージェントが同じ話題を重複調査した（2021年の半導体不足を1体、2025年サプライチェーンを2体が重複）。対策は「委任時に目的・出力形式・使うツール・**タスク境界**を詳細に書く」。`[原文確認]` https://www.anthropic.com/engineering/multi-agent-research-system
- → 本プロトコルでは「問い番号による分割」が境界に当たるが、agent1（広く調査）と agent2/3（掘り下げ）の境界は未定義で重複しやすい（推測）。

**2-c. 書き込み衝突の防ぎ方**
- AIエージェントPR 14万件超でマージ衝突率 27.67%。衝突の57.6%が同一行編集、26.8%が修正/削除の衝突。`[要約経由・二次記事]` https://codex.danielvaughan.com/2026/07/28/agent-pr-merge-conflicts-concurrent-coding-agents-codex-cli-worktree-isolation-coordination-defence/
- 対策: ファイル境界でタスクを分割し各エージェントが別ファイルを所有 / worktree 分離 / 読込時のハッシュを提出して楽観的並行制御、Git操作をミューテックスで直列化（MegaAgent）。`[要約経由]` https://arxiv.org/pdf/2408.09955 , https://www.augmentcode.com/guides/how-to-run-a-multi-agent-coding-workspace
- 本プロトコルの「自分のノートだけ編集」は所有権分割で正しい。唯一の共有書込先 BOARD.md の表は**1行1エージェント**なので行単位では衝突しにくいが、「論点リスト」「疑義」節は全員が末尾追記するため同一箇所衝突（追記同士）が起きやすい（推測）。pull --rebase で解決可能だが自動解決はされない。

**問い2 暫定結論（推測を含む）**
- 黒板＋各自ファイル所有の現行方式は文献的にも妥当。
- 改善候補: (1) 共有追記欄を `board/issues/<agent>-<n>.md` のような**1件1ファイル**にして追記衝突を構造的に消す、(2) BOARD の依頼に「型」（依頼/疑義/回答）を付けて pub-sub 的に自分宛てだけ拾えるようにする、(3) 着手前に「CLAIM: 調べるトピック」を BOARD に宣言して重複を防ぐ。→ agent5（問い5）への入力。

### 次サイクルでやること
- 原文未確認の数値の裏取り（arxiv 以外のミラー: openreview, ACL Anthology, Semantic Scholar 等を試す）
- 一晩規模の長時間自律運用での同期（ハートビート・ロック・タイムアウト）の事例
- agent4 からの疑義への対応
