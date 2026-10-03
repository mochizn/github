# レポート: 無人・長時間のマルチエージェント共同研究の設計パターン

> 更新: agent5（まとめ役）／ 現在 **サイクル1（骨組み）**。各章の「暫定」は次サイクル以降に他エージェントの成果で置き換える。
> 凡例: 出典のない主張には **推測** と書く。[aN] は notes/agentN.md 由来。

## 結論の要約
（最終サイクルで記入）

---

## 1. 役割分担: 何人で、どう分けると質が上がるか
**担当: agent2 ／ 状態: 未着手（他者の材料待ち）**

- 暫定の知見:
  - orchestrator-worker 型（リード1＋並列サブエージェント）は、単一エージェントを社内評価で 90.2% 上回った。ただし、課題を独立した並列の調査に分けられる場合に限る。[a5] https://www.anthropic.com/engineering/multi-agent-research-system
  - 人数は課題の複雑さで変える（単純な課題は1、比較は2〜4、複雑な課題は10以上）。[a5] 同上
  - 同じモデルの複数インスタンスによる討論でも事実性が上がる（Du et al.）。一方で、効果を過大評価しているという反論もある（要検証）。[a5] https://proceedings.mlr.press/v235/du24e.html , https://arxiv.org/pdf/2502.08788
- 未解決: 同質並列と役割分化の直接比較／批判役の効果の定量的な根拠

## 2. 同期・共有: 知見の共有方法と衝突・重複の防止
**担当: agent2 ／ 状態: 未着手**

- 暫定の知見:
  - 成果はファイルに書き出し、受け渡しは参照だけにする（「伝言ゲーム」の回避）。[a5] https://www.anthropic.com/engineering/multi-agent-research-system
  - 委任の指示には目的・出力形式・ツール・境界を必ず含める。欠けると重複作業や漏れが出る。[a5] 同上
  - セッションをまたぐ記憶は、進捗ファイルと git log で引き継ぐ。[a5] https://anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 未解決: 掲示板・共有ファイル・直接メッセージの比較

## 3. 品質管理: 幻覚・薄い根拠・堂々巡りの検出と抑制
**担当: agent3（＋agent4 の検証） ／ 状態: 未着手**

- 暫定の知見:
  - マルチエージェントの失敗のうち 23.5% は「タスク検証の不備」（MAST）。[a5] https://arxiv.org/abs/2503.13657
  - 早すぎる「完了」宣言を防ぐため、項目ごとの合否リストを持たせ、テストの削除や改変を禁止する。[a5] https://anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - 引用は専用エージェントで検証する。LLM-as-judge と人間レビューを併用する。[a5] https://www.anthropic.com/engineering/multi-agent-research-system
- 未解決: 堂々巡り（同じ論点の繰り返し）の検出法

## 4. コスト: トークンあたりの成果を最大化する運用
**担当: agent3 ／ 状態: 未着手**

- 暫定の知見:
  - マルチエージェントのトークン消費はチャットの約15倍。性能分散の80%はトークン量で説明できる（＝使うほど良くなるが、課題の価値が見合う場合に限る）。[a5] https://www.anthropic.com/engineering/multi-agent-research-system
- 未解決: サイクル間隔、打ち切り条件、モデルの使い分け（リード／ワーカー）

## 5. 結論: 本 PROTOCOL.md の改善提案
**担当: agent5 ／ 状態: 観察中（候補）**

| # | 観察 | 提案 | 根拠 |
|---|---|---|---|
| P1 | サイクル1ではまとめ役に統合する材料がない | まとめ役の起動を他より遅らせる（または初回は骨組み作りに限定すると明記する） | 本試運転の観察 [a5] |
| P2 | BOARD の隣接行を全員が編集する（衝突しやすいと**推測**） | 掲示板をエージェントごとのファイルに分けるか、追記だけのログにする | 推測（次サイクルで衝突ログを確認） |
| P3 | 問いごとの進捗状態が機械的に読めない | BRIEF の各問いに状態表（回答済み/根拠数/疑義）を置く | Anthropic の要件 JSON 方式 https://anthropic.com/engineering/effective-harnesses-for-long-running-agents |
| P4 | 失敗の大半は設計と不整合に由来する | 依頼のテンプレート（目的・出力・境界）を PROTOCOL に入れる | MAST https://arxiv.org/abs/2503.13657 ／ Anthropic |

---

## 付録: 未解決の疑義（BOARD から転記）
（なし）
