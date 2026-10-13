"""Discord / Slack Webhook 通知。

環境変数:
  KAIJI_DISCORD_WEBHOOK   Discord Webhook URL
  KAIJI_SLACK_WEBHOOK     Slack Incoming Webhook URL
"""

from __future__ import annotations

import logging
import os
import time

import requests

from .classify import LABELS
from .extract import format_yen
from .textutil import truncate

log = logging.getLogger(__name__)

EMOJI = {"order": "📦", "forecast": "📈", "earnings": "📊", "alliance": "🤝", "new_biz": "🆕", "subsidy": "🏛️",
         "mtp": "🧭", "ma": "🏢", "extraordinary": "⚠️", "monthly": "🗓️"}


def format_message(row: dict) -> str:
    cat = row.get("category", "other")
    head = f"{EMOJI.get(cat, '•')} **{row['name']} ({row['code']})** {row['date']} {row['time']}  [{LABELS.get(cat, cat)}]"
    lines = [head, row["title"]]
    if row.get("direction") in ("up", "down"):
        lines.append({"up": "↑ 上方修正/上振れ", "down": "↓ 下方修正/下振れ"}[row["direction"]])
    if row.get("amount_yen"):
        lines.append(f"金額: {format_yen(row['amount_yen'])}")
    llm = row.get("llm") or {}
    summary = llm.get("summary") or row.get("summary")
    if summary:
        lines.append(truncate(summary, 300))
    lines.append(row.get("pdf_url") or "")
    return "\n".join(x for x in lines if x)


def _post(url: str, payload: dict) -> bool:
    for attempt in range(3):
        try:
            r = requests.post(url, json=payload, timeout=15)
            if r.status_code == 429:
                time.sleep(float(r.headers.get("Retry-After", "2")))
                continue
            r.raise_for_status()
            return True
        except requests.RequestException as e:
            log.warning("webhook post failed: %s", e)
            time.sleep(2 ** attempt)
    return False


def configured() -> bool:
    return bool(os.environ.get("KAIJI_DISCORD_WEBHOOK") or os.environ.get("KAIJI_SLACK_WEBHOOK"))


def send(row: dict) -> bool:
    msg = format_message(row)
    ok = True
    if url := os.environ.get("KAIJI_DISCORD_WEBHOOK"):
        ok &= _post(url, {"content": truncate(msg, 1900)})
    if url := os.environ.get("KAIJI_SLACK_WEBHOOK"):
        ok &= _post(url, {"text": msg.replace("**", "*")})
    return ok
