# agent4 ノート

## サイクル1（2026-10-03）

### 状況
他エージェントのノートはまだ空（サイクル0）。そのため指示どおり (A) 検証観点の整理、(B) BRIEF の暗黙の前提に対する反証的文献探し、を行った。

**検証レベルの表記**（以後このノートで使う）:
- [一次確認] 原典ページを自分で取得して数値・文言を確認
- [二次] 検索結果の要約・二次サイトでの確認のみ（原典未取得）
- 注: この環境では arxiv.org が egress proxy でブロックされ WebFetch できない。arxiv 論文は現状 [二次] 止まり。他エージェントも同条件のはずなので、arxiv 由来の数値は特に要注意。

### (A) 検証チェックリスト（他者ノートを見るときの観点）
1. **出典の実在**: URL が実在し、主張がその URL に本当に書いてあるか。LLM の引用URLは 3〜13% が実在しない／5〜18% が解決不能という報告あり [二次] — https://arxiv.org/html/2604.03173v1 。Deep research 型エージェントのほうがむしろ幻覚URL率が高いとの指摘も同論文 [二次]。
2. **数値の出所の取り違え**: ブログ・まとめ記事の数値を論文の数値として書いていないか。例: 「マルチエージェントは本番で41〜86%失敗する」はまとめ記事（orq.ai, futureagi 等）で流通しているが、MAST 論文の何の数値かを要確認（下記）。
3. **条件の脱落**: 「マルチエージェントは90.2%良い」のような数値が、どのタスク・どの比較対象・どのトークン予算での話かが落ちていないか。
4. **コスト非統制の比較**: マルチエージェント優位の主張が、単一エージェントに同じトークン予算（self-consistency 等）を与えた比較になっているか。
5. **版の違い**: arXiv 論文が改訂で結論を反転させている例がある（下記 persona 論文）。版番号を確認。
6. **一般化の飛躍**: 数学/QA ベンチの結果を「一晩の共同研究」という本テーマに直接当てはめていないか。本テーマに近い実証（長時間・ファイル共有・非同期）は少ないはず（推測）。
7. **出典の利害**: 自社製品ブログ（Anthropic, Cognition, LangChain 等）の主張は利害関係ありとして扱う。

### (B) BRIEF の前提への反証的文献

| # | 疑われる前提 | 反証・留保となる文献 | 要点 | 検証 |
|---|---|---|---|---|
| R1 | 役割を分けた複数エージェントは単一より良い（問い1） | Tran & Kiela "Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets" https://pith.science/paper/2604.02460 （arXiv:2604.02460） | 思考トークン予算を揃えると単一エージェントがsequential/debate/role-based/ensembleと同等以上（FRAMES, MuSiQue, Qwen3/DeepSeek-R1-Distill/Gemini 2.5）。handoff＝情報圧縮という説明 | [二次] |
| R2 | 同上 | Google Research "Towards a science of scaling agent systems" https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/ （arXiv:2512.08296） | 並列化可能タスクでは中央集権型が大幅改善(+80.8%)だが、逐次推論タスクでは全マルチエージェント構成が39〜70%劣化 | [二次]（ブログ未取得） |
| R3 | 討論・批判役で品質が上がる（問い1・3） | "Stop Overvaluing Multi-Agent Debate" https://arxiv.org/abs/2502.08788 | 5種のMAD手法がCoTに対し36条件で勝率20%超なし。トークン当たり効率はself-consistencyに劣る。モデル異質性(heterogeneity)を推奨 | [二次] |
| R4 | 批判役の指摘で誤りが直る（問い3） | Huang et al. "Large Language Models Cannot Self-Correct Reasoning Yet" https://arxiv.org/abs/2310.01798 | 外部フィードバックなしの内省的自己修正は精度を上げず、時に下げる。先行研究の効果はoracle（正解ラベル）依存。**同一モデルの批判役＝外部フィードバックではない可能性**が本プロジェクトへの含意（推測） | [二次] |
| R5 | 合意＝正しさ（問い3） | "Too Polite to Disagree: Sycophancy Propagation in Multi-Agent Systems" https://arxiv.org/html/2604.02668v2 ほか | 討論でエージェントが誤答に同調して収束する（conformity）。誤答時にも議論中に正答が出ていたケースがあるのに無視される | [二次] |
| R6 | 役割（ペルソナ）付与自体に効果がある（問い1） | Zheng et al. "When 'A Helpful Assistant' Is Not Really Helpful" (Findings of EMNLP 2024) https://arxiv.org/abs/2311.10054v2 | 162ロール×2,410事実問題で、システムプロンプトのペルソナは性能を改善せず。**初版は逆の結論（"consistently improves"）で、改訂で反転**——版確認の重要性を示す好例 | [二次] |
| R7 | 並列サブエージェントは有効 | Cognition "Don't Build Multi-Agents" https://cognition.ai/blog/dont-build-multi-agents | 文脈分断で並列サブエージェントが矛盾した決定をする（Flappy Bird例）。文脈共有・意思決定を分割しない単線エージェントを推奨。※後に同社は "Multi-Agents: What's Actually Working" https://cognition.com/blog/multi-agents-working を出しており立場が更新された可能性→要確認 | [二次] |
| R8 | マルチエージェントの失敗は主にモデル能力の問題 | Cemri et al. "Why Do Multi-Agent LLM Systems Fail?" (MAST) https://arxiv.org/abs/2503.13657 | 14の失敗モード×3分類（仕様・設計 / エージェント間不整合 / 検証）、7フレームワーク・1600超のトレース。設計・調整の問題が主因。**疑義**: 「41〜86%失敗」はまとめ記事経由の数値で、原典での定義（どのベンチの失敗率か）未確認 | [二次] |
| R9 | 自律研究エージェントの出力は信頼できる | Beel et al. "Evaluating Sakana's AI Scientist" https://isg.beel.org/blog/2025/02/21/sakana-ai-scientist-evaluation/ （arXiv:2502.14297） | 生成論文7本中4本(57%)に誤り・幻覚の数値、実験12件中5件がコーディングエラーで失敗、引用は中央値5本で古い | [二次] |

### 一次確認できたもの
- Anthropic "How we built our multi-agent research system" https://www.anthropic.com/engineering/multi-agent-research-system [一次確認]
  - 「Opus 4リード＋Sonnet 4サブがOpus 4単体を**内部research eval**で90.2%上回る」——例示タスクはS&P500 IT企業の取締役列挙という**幅優先・並列化しやすい**タスク。一般化注意。
  - 「エージェントはチャットの約4倍、マルチエージェントは約15倍のトークン」
  - 「BrowseCompで3要因が分散の95%を説明、トークン使用量単独で80%」→ **性能差の大半はトークンを多く使ったことで説明される**。R1/R3（予算を揃えると優位が消える）と整合的。マルチエージェント＝「トークンを並列に多く使う手段」と読むべき。
  - 不向きな領域を自ら明記: 全員が文脈共有を要するタスク、依存関係の強いタスク、多くのコーディング。
  - 初期の失敗: 単純なクエリにサブエージェント50体以上、タスク記述不十分で重複作業、存在しない情報を延々検索、SEO記事を権威ある情報源より優先。→ 問い2・3・4に直結する実例。

### 暫定的な批判的見解（推測を含む）
- 本プロジェクト構成（同一モデル5体・役割固定・共有ファイル）への含意:
  1. 同一モデルの批判役は R4/R5 の理由で「外部検証」になりにくい（推測）。**批判役の価値は"意見"ではなく"ツールによる外部検証"（URL取得・原典照合）に置くべき**。私（agent4）は以後この方針で動く。
  2. 「何人が良いか」の問いは、トークン予算を揃えない限り答えが出ない（R1, Anthropic の80%）。REPORT で人数の推奨を書く場合はコスト統制の有無を明記すべき。
  3. 本テーマのような「一晩・非同期・ファイル共有」の設定での直接的実証は見当たらない（探した範囲で。推測）。ベンチマーク結果の外挿であることを明記すべき。
- 環境制約: arxiv.org 取得不可のため、論文数値の一次確認は代替（ACL Anthology, OpenReview, 著者サイト, Semantic Scholar）経由で試みる。

### 次サイクルでやること
- agent1〜3 のノートが入っていれば、主張を抽出し出典を照合（優先: 数値主張、arxiv 由来）。
- MAST の「41〜86%」の原典での意味を代替経路で確認。
- Cognition の立場更新（"Multi-Agents: What's Actually Working"）を確認。

### サイクル1 追補: 他者ノート（push 中に agent1/2/3/5 のノートが着いた）の初回照合

試した一次確認経路: arxiv.org / export.arxiv.org / openreview.net / aclanthology.org / proceedings.neurips.cc / huggingface.co / alphaxiv / emergentmind / research.google / sites.google.com — **すべて egress ポリシーで 403**（`curl $HTTPS_PROXY/__agentproxy/status` の recentRelayFailures で確認）。github.com / anthropic.com / isg.beel.org は取得可。→ 論文数値の一次確認は事実上不可能。以下は「複数の独立した検索スニペットの突き合わせ」による照合で、[二次] 止まり。

| ID | 対象主張 | 判定 | 根拠 |
|---|---|---|---|
| V1 | MAST 3分類の割合: agent1/agent2 = 41.8/36.9/21.3%、agent5 = 44.2/32.3/23.5% | **⚠ 不一致（版の違いの可能性大）** | "44.2/32.3/23.5" で検索すると NeurIPS 2025 Datasets & Benchmarks 版PDF（1642トレース記述と同居）がヒット https://proceedings.neurips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf 。"41.8/36.9/21.3" は substack まとめ記事・「200超タスク/150トレース」の記述と同居 https://futureagi.substack.com/p/why-do-multi-agent-llm-systems-fail 。→ 41.8% 系は初期版(v1/v2)、44.2% 系は最終版（推測、本文未取得）。**REPORT では最終版(NeurIPS 2025)の 44.2/32.3/23.5 を採用し版を明記すべき**。agent3 の FM別割合（FM-1.3 15.7% 等）もどの版か要明記 |
| V2 | MAST「本番で41〜86%失敗」（まとめ記事で流通） | ⚠ 未確認・引用非推奨 | 原典での定義（各フレームワークのベンチ失敗率か）が取れない。現状どのノートにも入っていないので予防的注意のみ |
| V3 | agent2「迎合最大85.5%・脆弱性70%・多数決が正答を捨てる32.3pt」の出典 = 2509.23055? | **✘ 出典取り違えの疑い** | これら3数値は "The Cost of Consensus: Isolated Self-Correction Prevails Over…" https://arxiv.org/pdf/2605.00914 の要約に一致（sycophantic conformity up to 85.5%, contextual fragility up to 70.0%, oracle gap up to 32.3pt）。2509.23055 は別論文 "Peacemaker or Troublemaker: How Sycophancy Shapes Multi-Agent Debate" https://awesomepapers.io/ai-agents/papers/2509.23055 。また 85.5% は「多数派回答の採用率（modal adoption）」で、"迎合率" と書くと意味がずれる。agent2 自身が曖昧と注記済みだったので、**2605.00914 に修正**を推奨 |
| V4 | agent2「3ラウンド目に意見の割れた問題の23.9%が全員一致誤答」の出典 = 2604.02668 (Too Polite to Disagree)? | **⚠ 出典取り違えの疑い** | 検索要約では 23.9% は "From Debate to Decision: Conformal Social Choice for Safe Multi-Agent Deliberation" https://arxiv.org/pdf/2604.07667 由来とされる。"Too Polite to Disagree" は SIGDIAL 2026 https://aclanthology.org/2026.sigdial-1.56/ で、ピアの迎合度ランキングを与える実験の論文。要再確認（検索要約の一致は弱い証拠） |
| V5 | agent5「"Stop Overvaluing MAD" の主張は（推測）討論の効果は評価方法次第・異質性が重要」 | ✔ 概ね妥当 [二次] | 5手法×9ベンチ×4モデル、36条件でCoTに勝率20%超の手法なし、SCよりトークン効率が悪い、モデル異質性で改善。https://arxiv.org/abs/2502.08788 。なお初版タイトルは "If Multi-Agent Debate is the Answer, What is the Question?"（agent1 C9 は旧題で引用、同一論文 2502.08788 の別版） |
| V6 | Anthropic 90.2% / 4×・15× / 分散80%（agent1,2,3,5 全員が引用） | ✔ 一次確認 | https://www.anthropic.com/engineering/multi-agent-research-system 。ただし全員が同一ソースに依存しており、**問い1・4の根拠が1社1記事に集中**している点は弱み（利害関係あり、内部eval） |
| V7 | agent2「Kim et al.: Independent はエラー17.2倍、Centralized 4.4倍」 | 未確認 | research.google ブログも遮断。次サイクルで別経路を試す |
| V8 | agent3「CoVe FActScore 55.9→71.4」「ChatDev 検証追加で+15.6pt」 | 未確認 | 次サイクル |

#### 構造的な所見（チーム全体への批判）
- **単一ソース依存**: 4人全員が Anthropic 記事を主要根拠にしている。独立した二つ目の実証がない主張（例: 「10体超で責任分割」の人数目安）は REPORT で「1社の経験則」と明記すべき。
- **全員が同じ検索要約に依存**: arxiv 遮断下では、全員が同じ検索エンジン要約を読んでいるため、要約の誤りが5人に同時に伝播しうる（V3/V4 はその実例の可能性）。「5人が同じ数値を書いている」ことは独立な裏付けにならない。→ 問い3（品質管理）・問い5（改善提案）の材料。提案: 環境で一次資料が取れない場合、数値は「[二次] 出典URL＋参照した要約サイトURL」の2点を書く規約。
- agent3 の「批判役は主張だけ抜き出して出典を開き直す（factored）」提案に同意。ただし本環境では "開き直す" 対象の大半が遮断されている。**検証器が環境に依存する**ことを PROTOCOL 改善に反映すべき（例: 起動時に主要ドメインの到達性を確認し BOARD に記録する）。
