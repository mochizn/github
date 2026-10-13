"""Claude API による要約(任意機能)。

環境変数:
  KAIJI_LLM=1              有効化(既定: 無効。認証情報が無ければ自動で無効)
  KAIJI_LLM_MODEL          既定 claude-opus-5-5
  KAIJI_LLM_MAX_PER_RUN    1回の実行で要約する最大件数(既定 30)
  KAIJI_LLM_CATEGORIES     対象カテゴリ(既定 order,forecast,earnings,mtp,alliance,new_biz,subsidy)
"""

from __future__ import annotations

import json
import logging
import os

from .classify import LABELS
from .textutil import truncate

log = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-opus-5-5"
DEFAULT_CATEGORIES = "order,forecast,earnings,mtp,alliance,new_biz,subsidy"

SYSTEM = """あなたは日本株の個人投資家を支援するアナリストです。
適時開示(TDnet)の本文から、投資判断と後日の振り返りに役立つ事実を簡潔な日本語で整理します。
- 事実のみを書き、本文に無い推測や数値を作らないこと
- 金額・時期・相手先・業績影響など定量/定性の要点を優先すること
- 定型文(「下記のとおりお知らせします」等)や会社概要は省くこと"""

SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string", "description": "要約(150字以内)"},
        "key_points": {"type": "array", "items": {"type": "string"}, "description": "要点(最大5つ、各60字以内)"},
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral", "mixed"]},
        "earnings_impact": {"type": "string", "description": "業績への影響(本文記載どおり。記載が無ければ空文字)"},
        "topics": {"type": "array", "items": {"type": "string"}, "description": "検索用キーワード(製品名・顧客業界・テーマ等 最大6つ)"},
    },
    "required": ["summary", "key_points", "sentiment", "earnings_impact", "topics"],
    "additionalProperties": False,
}


def enabled() -> bool:
    if os.environ.get("KAIJI_LLM", "0") not in ("1", "true", "yes"):
        return False
    try:
        import anthropic  # noqa: F401
    except ImportError:
        log.warning("KAIJI_LLM=1 ですが anthropic パッケージがありません (pip install anthropic)")
        return False
    return True


def target_categories() -> set[str]:
    return set(os.environ.get("KAIJI_LLM_CATEGORIES", DEFAULT_CATEGORIES).split(","))


def model_name() -> str:
    return os.environ.get("KAIJI_LLM_MODEL", DEFAULT_MODEL)


def build_prompt(row: dict) -> str:
    cats = "、".join(LABELS.get(t, t) for t in row.get("tag_list") or [])
    parts = [
        f"会社: {row['name']} ({row['code']})",
        f"開示日時: {row['date']} {row['time']}",
        f"タイトル: {row['title']}",
        f"分類: {cats}",
    ]
    if row.get("order"):
        parts.append("ルール抽出した受注情報: " + json.dumps(row["order"], ensure_ascii=False))
    # 決算短信は本文(財務諸表)より定性情報を渡す
    sections = [("定性情報", row.get("qualitative")), ("見通し", row.get("outlook")), ("理由", row.get("reason"))]
    if not row.get("qualitative"):
        sections.append(("本文", row.get("body")))
    for label, txt in sections:
        if txt:
            parts.append(f"<{label}>\n{truncate(txt, 12000)}\n</{label}>")
    return "\n".join(parts)


class Summarizer:
    def __init__(self, model: str | None = None):
        import anthropic

        self.anthropic = anthropic
        self.client = anthropic.Anthropic()
        self.model = model or model_name()

    def summarize(self, row: dict) -> dict | None:
        a = self.anthropic
        kwargs = dict(
            model=self.model,
            max_tokens=4000,
            system=SYSTEM,
            messages=[{"role": "user", "content": build_prompt(row)}],
            output_config={"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
        )
        try:
            if self.model.startswith(("claude-opus-5", "claude-fable-5-1", "claude-sonnet-5-5")):
                resp = self.client.beta.messages.create(
                    betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs
                )
            else:
                resp = self.client.messages.create(**kwargs)
        except a.RateLimitError as e:
            log.warning("LLM rate limited: %s", e)
            raise
        except a.APIStatusError as e:
            log.warning("LLM API error %s: %s", e.status_code, e)
            return None
        except a.APIConnectionError as e:
            log.warning("LLM connection error: %s", e)
            return None
        if resp.stop_reason == "refusal":
            log.warning("LLM refused for %s", row.get("id"))
            return None
        text = next((b.text for b in resp.content if b.type == "text"), "")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            log.warning("LLM returned non-JSON for %s", row.get("id"))
            return None
