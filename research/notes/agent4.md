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

## サイクル2（2026-10-03 02:3x UTC）

### 前回からの変化
- 他エージェント（agent1/2/3）はまだサイクル2未着。agent5 がサイクル1で REPORT を作成し、MAST 不一致と 2502.08788 の題名問題を私に依頼。→ 今回は (1) 自分宛て依頼への回答、(2) 前回積み残し V7/V8、(3) **REPORT に入った主張**の照合を優先した（REPORT に入る＝結論に効くため）。
- 一次確認可能ドメインは前回と同じ（anthropic.com, github.com は可。cognition.com も今回遮断を確認）。

### 依頼への回答
- **@agent5 MAST 割合**: V1 の結論を維持。44.2/32.3/23.5% は NeurIPS 2025 D&B 版（1642トレースの記述と同じ文書）、41.8/36.9/21.3% は「200タスク/150トレース」記述の初期版とまとめ記事に出る。REPORT は 44.2/32.3/23.5（NeurIPS 2025 版）を採用し、旧版値は脚注に、が妥当。[二次・複数スニペット一致]
- **@agent5 2502.08788 の題名**: 同一論文の改題。初版 "If Multi-Agent Debate is the Answer, What is the Question?" → 現行 "Stop Overvaluing Multi-Agent Debate — We Must Rethink Evaluation and Embrace Model Heterogeneity"。alphaxiv の v1 ページが旧題、abs ページと v3 overview が新題 https://www.alphaxiv.org/abs/2502.08788v1 , https://arxiv.org/abs/2502.08788 [二次]。引用は新題＋arXiv番号で統一を。

### 照合結果（V7〜V16）

| ID | 対象 | 判定 | 根拠・コメント |
|---|---|---|---|
| V7 | agent2: Kim et al. Independent エラー17.2倍 / Centralized 4.4倍 | ✔ 数値一致 [二次] | 複数の要約で "Independent agents amplify errors 17.2x, centralized contains to 4.4x" https://arxiv.org/pdf/2512.08296 。+80.8%（並列タスク）, 逐次推論で39〜70%劣化も一致。※「エラー増幅」の定義（何に対する倍率か）は未確認なので、REPORT では文言を要約どおりに留めること |
| V8a | agent3: CoVe「**factored 版が最良**で FActScore 55.9→71.4」 | **✘ 一部誤り** | 55.9→71.4 は **factor+revise** 版。factored 版は 63.7。しかも factored は1回答あたり事実数が 16.6→11.7 に減る（精度↑・網羅性↓のトレードオフ）https://arxiv.org/pdf/2309.11495 [二次: 検索要約に表の値] 。→ 「独立検証で幻覚が減る」結論自体は維持できるが、**"言うことを減らして正確に見せる"効果が混ざる**点を明記すべき。本プロジェクトへの含意: 批判役の検証で主張を削ると見かけの正確さが上がるが網羅性が落ちる（推測） |
| V8b | agent3: MAST の ChatDev 介入 +15.6 | ✔ 概ね一致 [二次] | 「高レベルの目的検証ステップ追加で ProgramDev のタスク成功 +15.6%」、別に「CEO に最終決定権を与える役割仕様の修正で +9.4%」https://arxiv.org/html/2503.13657 。単位（%かpt）は要約では "%"。agent3 の "pt" 表記は未確認 |
| V9 | REPORT §1 / agent1: EMNLP 2024 aclanthology 1112 =「同予算では CoT-SC が debate を上回る」 | ✔ 一致 [二次] | 論文名 "Reasoning in Token Economies: Budget-Aware Evaluation of LLM Reasoning Strategies" https://aclanthology.org/2024.emnlp-main.1112/ 。追加の要点: **MAD や Reflexion は予算を増やすと逆に悪化しうる**（SC は単調）。→ 問い4（コスト）にも効く。REPORT には論文名を書くべき（現状URLのみ） |
| V10 | REPORT §1 / agent1: 2509.05396 =「同調で全員一致の誤答が増える」 | ✔ 概ね一致＋**重要な留保** [二次] | 論文名 "Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate"（Wynn, Satija, Hadfield; ICML 2025 関連ワークショップ）https://arxiv.org/abs/2509.05396 , https://icml.cc/virtual/2025/49332 。正→誤の変化、議論が長いほど劣化。**さらに: 能力の低いモデルを混ぜると強いモデルの性能も下がる／モデル多様性では失敗モードが解消しない**との記述。→ agent3・REPORT の「異質性（別モデル）を入れれば良い」（2502.08788 の推奨）と**衝突**。異質性は"能力が同等以上の別モデル"に限るなど条件付きで書くべき |
| V11 | REPORT §2 / agent1: Blackboard 2510.01285 で 13〜57% 改善 | ✔ 数値一致 [二次] | "LLM-Based Multi-Agent Blackboard System for Information Discovery in Data Science"（Salemi et al., Google 共著）https://arxiv.org/abs/2510.01285 。end-to-end 成功率で13–57%相対改善、データ発見F1は最大9%。**ただし**「BOARD.md はこの型に近い」は類推が緩い: 原論文はサブエージェントが**能力に応じて自発的に依頼を引き受ける**方式で、本プロトコルは役割固定（推測） |
| V12 | REPORT §2 / agent1: C コンパイラ事例 | ✔ 一次確認 | https://www.anthropic.com/engineering/building-c-compiler 16エージェント、`current_tasks/` ロック（同じタスクを取ろうとすると git の同期で後者が別タスクへ）、約2,000セッション/2週間、入力20億・出力1.4億トークン、$20,000弱、GCC をオラクルにして分割。役割は「重複コード統合」「性能改善」「効率的なコード出力」「**Rust 開発者視点での設計批評**」「ドキュメント」。"task verifier is nearly perfect" が必要と明記。→ agent1 の「コード品質批評役」は大意OK。**注意: 検証器は自動テスト**であり、本プロジェクトのような研究タスクには同等の検証器がない＝そのまま外挿不可 |
| V13 | REPORT §2/§3 / agent5: Effective harnesses 記事 | ✔ 一次確認＋**留保** | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents init.sh、claude-progress.txt、`"passes": false` の機能リストJSON、"It is unacceptable to remove or edit tests" を確認。**ただし記事自身が「別エージェントと呼ぶのはプロンプトが違うだけ。システムプロンプト・ツール・ハーネスは同一」と明言＝逐次の単一エージェント構成**。REPORT §2 で「マルチエージェントの同期手法」として引く場合は「逐次セッション間の引き継ぎ」の根拠に限定すべき |
| V14 | agent2: エージェントPR 14万件超でマージ衝突率 27.67%、内訳57.6%/26.8% | ⚠ 数値は概ね一致、**解釈に疑義** | 一次出典は AgenticFlict（arXiv:2604.03551）https://github.com/unlv-evol/AgenticFlict 。AIDev の 932,791 PR → 未マージ/オープンの 142,652 件 → **107,026 件の模擬マージ**で 27.67% が衝突 [二次]。分母は14万件ではなく模擬マージ10.7万件。対象は**未マージPRに偏ったサンプル**で、上流の進行との衝突。**本プロジェクトの「同時に共有ファイルへ追記」状況とは別物**。内訳57.6%/26.8%は別の二次記事（33,596PR の研究？）由来で未確認。agent2 が引用した danielvaughan.com は個人ブログ（遮断で未取得） |
| V15 | Cognition の立場（R7 の更新） | 更新あり [二次] | 2026-04-22 "Multi-Agents: What's Actually Working"（Walden Yan）https://cognition.com/blog/multi-agents-working : 「**書き込みは単一スレッドに保ち、追加エージェントは行動でなく知性（レビュー・調査）を提供する**」形は機能する。manager が分割→子が実行→manager が統合（map-reduce-and-manage）。無構造なスウォームは"mostly a distraction"。文脈（同じ情報源・todo・plan ファイル）を最大限共有。→ 本プロトコルは各自のノートに書き込みを分離しており「single writer per file」は満たすが、**REPORT への書き込みを agent5 に一本化している点はこの原則と整合**。逆に BOARD は多重書き込み |
| V16 | REPORT §5 P7（agent5）「BOARD 衝突は未観測なので保留」 | **✘ 反例あり（私の実体験）** | サイクル1で私（agent4）の push 時に `CONFLICT (content): Merge conflict in research/BOARD.md` が発生。原因: 私の行の更新と「論点リスト」末尾追記が、agent1/2/3/5 の同時更新と同じ hunk に入った。手動解決に約2回の rebase を要し、一度は rebase 途中状態で push に失敗。→ **P7 は「保留」ではなく「観測済み・要対策」**。agent2 の「1件1ファイル化」提案、agent5 O2 の `board/agentN.md` 分割案を支持する根拠 |

### 横断的な批判（REPORT への提言）
1. **"異質性を入れれば討論は効く" は未確立**: 2502.08788（異質性で改善）vs 2509.05396（弱いモデル混入で劣化・多様性では失敗が解消しない）。REPORT §1・§3 で一方だけを書かないこと。
2. **検証器の外挿問題**: 成功事例（C コンパイラ、long-running harness）はいずれも**自動テストという強い検証器**がある。研究タスクにはそれがないので、本プロトコルの成功見込みを過大評価しないこと。研究タスクで代替になりうるのは URL 到達性・引用一致チェック（推測）だが、本環境ではその到達性自体が大きく制限されている。
3. **数値の圧縮で条件が落ちる例が今回も2件**（V8a の factored/factor+revise 取り違え、V14 の分母）。いずれも「検索要約→ノート」の1ホップで起きた。→ 問い3の具体例として REPORT に入れる価値あり。

### 判断の記録
- 他者のサイクル2が未着のため、既に REPORT に入った主張を優先的に検証した（結論への影響が大きい順）。
- V8a は検索要約2件の数値が整合（55.9/63.7/71.4、事実数16.6/11.7）していたため ✘ 判定とした。原文未取得なので確度は中。

### 次サイクル（最終）でやること
- agent1〜3 のサイクル2の新規主張を照合（特に REPORT に入りそうなもの）
- 自分の指摘（V3/V4/V8a/V14/V16）が各ノート・REPORT に反映されたか確認
- 批判役としての総括: 本試運転で観測された誤りの型（版違い・出典取り違え・条件の脱落・単一ソース依存）を agent5 の問い5向けにまとめる

### サイクル2 追補（push 前に agent1/2/3 のサイクル2が着いたため照合）

| ID | 対象 | 判定 | コメント |
|---|---|---|---|
| V17 | agent1 E1: MAST 公式リポジトリの図（taxonomy_v11）で第3の値 37.17/31.41/31.41% | ✔ 受け入れ・**私の V1 推奨を撤回** | 私はサイクル1・2で「NeurIPS 版 44.2/32.3/23.5 を採用」と推奨したが、根拠は検索スニペットのみ。agent1 は公式リポジトリの図を原文確認しており、証拠の質が上。agent1 の「幅で示す」案に賛成。**ただし agent1 の「順位（仕様 ≥ 協調 ≳ 検証）は安定」も言い過ぎ**: 3版のうち v11 図では協調＝検証（31.41＝31.41）で、旧版では検証が最小(21.3)。**全版で安定なのは「仕様・設計が最大」だけ**。REPORT に書けるのはそこまで |
| V18 | agent2: C コンパイラ事例は「オーケストレータなし」 | ✔ 一次確認 | 原文 "I don't use an orchestration agent. Instead, I leave it up to each Claude agent to decide how to act." 通信はロックのみ（"haven't yet implemented any other method for communication between agents"）https://www.anthropic.com/engineering/building-c-compiler 。agent2 の「中央集約の本質は検証点の集中で、テストが肩代わりできる」解釈は筋が通るが推測（agent2 も推測と明記済み） |
| V19 | agent1 E2: claude.com「いつマルチエージェントを使うか」 | ✔ 一次確認（大部分） | 2026-01-23 公開。「同等タスクで単一比3〜10倍のトークン」「文脈保護・並列化・専門化の3場面」「単一エージェントのプロンプト改善で同等の結果」「作業の種類別に分けるな、文脈境界で分けよ」「検証サブエージェントは文脈の受け渡しが最小なので安定して成功」を確認 https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them 。agent1 の「強いオーケストレーターは検証段を挟まず直接評価する傾向」は私の取得では確認できず（未確認）。**含意**: 批判役(検証役)は「文脈の受け渡しが最小で済む」唯一安定な分割として記事に支持されている一方、調査→深掘り→まとめの流れは「作業の種類別」分割に当たり記事の警告対象（agent1 P7 に同意） |
| V20 | agent3: CoVe/ChatDev は [二次情報] のまま | 補足 | 私の V8a（55.9→71.4 は factor+revise 版、factored は63.7で事実数も減る）を参照して REPORT 用文言を直してほしい |
| — | agent2 V3/V4 の修正 | ✔ 反映確認 | 取り消し線で履歴を残す方式は良い（検証可能性が上がる） |
| — | agent3: BOARD 衝突の実例 | ✔ 私の V16 と独立に同じ観測 | 2件の独立な観測で、P7「未観測」は誤りと確定。衝突したのはいずれも「誰でも追記可」の共有末尾（私の場合は行更新も同じ hunk）。本サイクル2の push でも私は再び BOARD で衝突した（3件目） |

**自己批判**: V1 で検索スニペットだけを根拠に「最終版を採用せよ」と断定的に推奨したのは、批判役として自分のチェックリスト（項目2・5）に反していた。一次資料に近い証拠（公式リポジトリの図）が出た時点で撤回する。→ 問い3への教訓: **批判役の指摘も同じ確度タグで扱い、批判役自身も検証対象にする**べき。

## サイクル3（最終, 2026-10-03 03:3x UTC）

### 前回からの変化
- 起動時点で他エージェントのサイクル3は未着。REPORT は agent5 のサイクル2版（私のサイクル2の V8a〜V20 は**未反映**）。→ 最終サイクルの方針: (1) REPORT サイクル2版の本文を照合し、**最終版で直すべき箇所を優先度順のリスト**にして agent5 に渡す、(2) 未検証だった REPORT 記載の一次資料・数値を追加照合、(3) 批判役として「本試運転で観測された誤りの型」を総括（問い3・5の材料）。

### 追加照合（V21〜V25）

| ID | 対象（REPORT サイクル2版） | 判定 | 根拠・コメント |
|---|---|---|---|
| V21 | §1-2/§2/§3/§4: Claude Code agent teams の引用（3〜5人、"Three focused teammates often outperform five scattered ones"、5〜6タスク/人、ファイルロック、同一ファイル編集で上書き、TaskCompleted フック、リードの早期停止） | ✔ 一次確認・全て原文どおり | https://code.claude.com/docs/en/agent-teams 。**REPORT に未記載の重要点**: (a) 機能自体が "experimental" と明記。(b) "For sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective"。(c) **"Letting a team run unattended for too long increases the risk of wasted effort"**（"Monitor and steer" 節）——BRIEF の前提「人間の監督なしに一晩」に対し、公式ドキュメント自体が逆方向の推奨をしている。REPORT の結論で触れるべき |
| V22 | §4: プロンプトキャッシュ 5分=1.25×、1時間=2×、読み込み≈0.1× | ✔ 一次確認 | https://platform.claude.com/docs/en/build-with-claude/prompt-caching 。読み込みはモデル別に 0.05×/0.025× の例外あり。**重要: キャッシュはヒットのたびに無料で TTL が更新され、寿命は「そのキャッシュを読み書きしたリクエストの開始時刻」から測る** |
| V23 | §4/P8: 「サイクル間隔が1時間を超えると再書込が起きうるので55分が安全」（agent3, agent2） | **⚠ 推論の前提が不正確** | V22 より、キャッシュの起点は「前サイクルの開始」ではなく「前サイクル最後のリクエストの開始」。各サイクルは30〜40分作業するので、次サイクル起動までの空白は**約20〜30分**で、1時間 TTL には十分収まる（推測: CCR 内部のキャッシュ挙動は未確認）。トリガー間隔を55分に詰める根拠としては弱い。むしろ効くのは「作業時間＋空白 < 1h」ではなく「**空白 < 1h**」。P8 は「間隔は作業終了から60分未満なら可」に書き換えるのが正確 |
| V24 | §1-3: 異種モデル混成で「最大+47%」（X-MAS, 2505.16997） | ⚠ 数値一致・**条件が脱落** [二次] | +47% は AIME で **chatbot と reasoner（推論特化モデル）を混ぜた**場合。chatbot 同士の異種混成では MATH で最大 +8.4%。https://arxiv.org/pdf/2505.16997 。+47% には「より強い推論モデルを足した効果」が混ざっている可能性（推測）。2509.05396（V10: 弱いモデルの混入で劣化）と合わせ、「異質性」は**能力が同等以上のモデルを足す場合**に限って書くべき |
| V25 | §3-1: 「個別の失敗モードでは『ステップの反復』が最多 15.7%」 | **✘ 公式図と矛盾** | agent1 が原文確認した公式リポジトリの図（taxonomy_v11）では FM-1.3 Step Repetition は **11.5%**、最多は FM-1.1 タスク仕様違反 15.2%、次いで FM-3.3 13.61%。15.7% は版不明の二次情報（agent3 自身がサイクル2で格下げ済み）。→「最多」の主張ごと削除を推奨 |

### REPORT 最終版への修正依頼（@agent5、優先度順）
1. **§2-3「衝突0件」と P10「変更不要」は誤り**（V16）。BOARD.md の push 衝突は agent4（サイクル1・2の2回）と agent3（サイクル1）で独立に3回観測。いずれも「誰でも追記可」の共有末尾が絡む。→ P10 は「観測済み・要対策（追記欄の1件1ファイル化 or `board/agentN.md` 分割）」に。agent5 自身の push で衝突しなかったのは事実だが、それは5人中の一部の経験にすぎない（生存者バイアス）。
2. **§3-1 MAST 割合**: 「最終版44.2/32.3/23.5%を採用」は私の V1 推奨に基づくが、**V17 で撤回済み**。版は少なくとも3つ（41.8/36.9/21.3、44.2/32.3/23.5、公式図 37.17/31.41/31.41）。**結論に使えるのは「仕様・設計が最大」だけ**。付録 V1 の状態「解決」も「撤回・幅で記載」に。
3. **§3-1「ステップの反復が最多 15.7%」を削除**（V25）。
4. **§1-4/§1-3 異質性**: 「モデルの異質性を入れると改善」に、反証 2509.05396（弱いモデル混入で強いモデルも劣化、多様性で失敗が解消しない）と X-MAS の条件（+47% は推論モデル混成時）を併記（V10, V24）。
5. **§2-4 long-running harness** は記事自身が「プロンプトが違うだけの単一エージェント」と明言（V13）。「逐次セッション間の引き継ぎ」の根拠として限定。
6. **§2-3 マージ衝突率 約28%** は AgenticFlict（arXiv 2604.03551）の**未マージPRの模擬マージ10.7万件**での値。同時編集とは状況が違う（V14）。引用するなら出典を一次の AgenticFlict に差し替え、文脈を明記。
7. **§3-2 CoVe**: 55.9→71.4 は factor+revise 版。factored は 63.7 で事実数が 16.6→11.7 に減る（V8a）。「独立検証は正確さを上げるが、主張を減らす効果も含む」と書く。
8. **§4 P8（55分）** は V23 の理由で根拠が弱い。
9. **付録 V3/V4「未解決」→解決済み**（agent2 がサイクル2で出典を 2605.00914 / 2604.07667 に修正）。V7 は「二次3ソースで一致（独立とは限らない）」。
10. **結論の要約に V21(c) を追加**: 公式ドキュメントは「長時間の無人運用は無駄な作業のリスクを高める」と明記しており、BRIEF の前提（人間の監督なしに一晩）は外部根拠と緊張関係にある。

### 総括: 本試運転で観測された誤りの型（問い3・問い5向け）

全3サイクルで私が出した照合 25 件（V1〜V25）の内訳（自己集計）:
- ✔ 一致・確認: 13件（うち一次確認 7件: V6, V12, V13, V18, V19, V21, V22）
- ⚠ 数値は合うが条件・解釈に問題: 7件（V1/V17, V2, V4, V10, V14, V23, V24）
- ✘ 誤り: 4件（V3, V8a, V16, V25）
- 未確認のまま: 1件（V2 の定義）※V1 は私自身の誤推奨を V17 で撤回

**誤りの型（実例つき）**
| 型 | 実例 | 発生箇所 | 効く対策（提案） |
|---|---|---|---|
| T1 版の取り違え | MAST 割合が3版混在（V1/V17）、persona 論文の結論反転（R6）、2502.08788 改題（V5） | 検索要約→ノート | 数値には版（arXiv vN / 会議版 / 公式リポジトリ）を必須記載 |
| T2 出典の取り違え | 85.5%/23.9% を隣接論文に帰属（V3, V4） | 検索要約が複数論文を混ぜる | [二次] には「参照した要約URL」も書く（追跡可能にする） |
| T3 条件の脱落 | CoVe の版（V8a）、X-MAS の推論モデル混成（V24）、マージ衝突の分母と母集団（V14）、Anthropic 90.2% の課題・予算（V6） | 要約→ノート→REPORT の各ホップ | 数値は「何の・何に対する・どの条件で」の3点セットで書く |
| T4 単一ソース依存 | 問い1・4の主要根拠が Anthropic の1〜2記事（V6）、人数目安も同社のみ（REPORT 自身が注記） | 全員 | 結論に使う主張は独立2出典を目標、1出典なら明記 |
| T5 自己観測の過剰一般化 | 「BOARD 衝突0件」（V16）——一人の push 経験を全体に一般化 | まとめ役 | 自己観測は「誰が・何回」を書き、BOARD に観測ログ欄を設ける |
| T6 批判役自身の誤り | 私が検索スニペットだけで「NeurIPS版を採用せよ」と推奨→撤回（V17） | 批判役 | 批判役の指摘にも確度タグを付け、批判役も検証対象にする |
| T7 推論の前提ミス | キャッシュ TTL の起点の誤解（V23） | 問い4の推論 | 推論の前提となる仕様を一次ドキュメントで確認してから提案に入れる |

**批判役の役割についての結論（問い1・3への寄与、推測を含む）**
- 本試運転で批判役が実際に価値を出したのは、**意見ではなく照合**（URL を開く・数値を突き合わせる・版を比べる）の場面だけだった。これは R4（外部フィードバックなしの自己修正は効かない）、claude.com 記事の「検証サブエージェントは文脈の受け渡しが最小なので安定」（V19）と整合する。
- ただし本環境では一次資料の大半が遮断され、照合の多くが「検索要約どうしの突き合わせ」に留まった。検索要約は互いに引き写している可能性があり、**批判役の照合力は環境の到達性に上限を決められる**。→ PROTOCOL 改善 P1（起動時の到達性確認・ENV.md）は批判役の有効性の前提条件。
- 依頼→検証→修正の往復は1サイクル単位でしか回らず、3サイクルではほぼ1往復で終わった（agent2 も同じ指摘）。批判役の起動を半サイクル遅らせる案（P7）は、サイクル1で私が「空のノート」を相手にした実体験からも支持する。

### 判断の記録
- 他者のサイクル3を待たずに締めた: PROTOCOL 上サイクル3で DONE にする必要があり、REPORT 最終版の前に修正リストを渡す方が効果が大きいと判断した。
- 修正依頼は REPORT への影響（結論を変えるか）で順位付けした。1・2・10 は結論に直結、3〜9 は精度の問題。

STATUS: DONE（agent4、3サイクル完了）
