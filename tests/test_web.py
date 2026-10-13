import threading
import urllib.parse
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from kaiji.classify import classify
from kaiji.db import Store
from kaiji.web import App, make_handler


@pytest.fixture
def server():
    s = Store(":memory:")
    title = "大口受注に関するお知らせ<script>"
    c = classify(title)
    s.upsert_meta({"id": "a1", "date": "2026-10-01", "time": "15:00", "code": "6227", "name": "AIメカテック", "title": title,
                   "pdf_url": "https://example/a1.pdf", "xbrl_url": None, "exchange": "東", "history": ""},
                  c.primary, c.tags, c.importance, c.is_correction, c.deep)
    s.update("a1", status="done", summary="半導体関連メーカーから受注", amount_yen=4.5e9, order_json={"item": "装置"},
             metrics_json=[{"metric": "受注高", "value_yen": 1e9, "yoy_pct": 20.0, "text": "受注高は10億円"}])
    s.commit()
    srv = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(s)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def get(url):
    with urllib.request.urlopen(url) as r:
        return r.status, r.read().decode()


@pytest.mark.parametrize("path", ["/", "/orders", "/metrics?min_yoy=10", "/stats", "/d/a1", "/c/6227",
                                  "/?q=" + urllib.parse.quote("半導体 -訂正") + "&min=" + urllib.parse.quote("10億") + "&sort=amount"])
def test_pages_render(server, path):
    status, body = get(server + path)
    assert status == 200
    assert "<script>" not in body.split("<body>", 1)[1]  # タイトルはエスケープされる


def test_search_highlight_and_api(server):
    _, body = get(server + "/?q=" + urllib.parse.quote("半導体"))
    assert "<mark>半導体</mark>" in body
    _, js = get(server + "/api/search?q=" + urllib.parse.quote("受注"))
    assert '"id": "a1"' in js
