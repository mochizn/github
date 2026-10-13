import json

import pytest

httpx = pytest.importorskip("httpx2")

anthropic = pytest.importorskip("anthropic")

from kaiji import llm  # noqa: E402


def make_client(handler):
    return anthropic.Anthropic(api_key="test", base_url="https://api.test", http_client=httpx.Client(transport=httpx.MockTransport(handler)))


def response(text: str, stop_reason: str = "end_turn") -> httpx.Response:
    return httpx.Response(200, json={
        "id": "msg_1", "type": "message", "role": "assistant", "model": "claude-opus-5-5",
        "content": [{"type": "text", "text": text}], "stop_reason": stop_reason, "stop_sequence": None,
        "usage": {"input_tokens": 10, "output_tokens": 10},
    })


ROW = {"id": "x", "name": "テスト", "code": "1234", "date": "2026-10-01", "time": "15:00", "title": "大口受注に関するお知らせ",
       "tag_list": ["order"], "order": {"amount_yen": 4.5e9}, "body": "当社は大口受注をいたしました。", "qualitative": "",
       "outlook": "業績予想に織り込み済み", "reason": ""}


def test_summarize_request_and_parse(monkeypatch):
    seen = {}
    out = {"summary": "45億円の受注", "key_points": ["a"], "sentiment": "positive", "earnings_impact": "織り込み済み", "topics": ["半導体"]}

    def handler(req: httpx.Request):
        seen["body"] = json.loads(req.content)
        seen["beta"] = req.headers.get("anthropic-beta")
        return response(json.dumps(out, ensure_ascii=False))

    s = llm.Summarizer.__new__(llm.Summarizer)
    s.anthropic, s.client, s.model = anthropic, make_client(handler), "claude-opus-5-5"
    assert s.summarize(ROW) == out
    body = seen["body"]
    assert body["model"] == "claude-opus-5-5"
    assert body["output_config"]["format"]["type"] == "json_schema"
    assert body["fallbacks"] == "default"
    assert "server-side-fallback-2026-07-01" in seen["beta"]
    assert "大口受注" in body["messages"][0]["content"]


def test_summarize_refusal_returns_none():
    s = llm.Summarizer.__new__(llm.Summarizer)
    s.anthropic, s.client, s.model = anthropic, make_client(lambda req: response("", "refusal")), "claude-haiku-5-5"
    assert s.summarize(ROW) is None


def test_enabled_flag(monkeypatch):
    monkeypatch.delenv("KAIJI_LLM", raising=False)
    assert not llm.enabled()
    monkeypatch.setenv("KAIJI_LLM", "1")
    assert llm.enabled()
