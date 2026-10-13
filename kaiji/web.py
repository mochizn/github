"""標準ライブラリだけで動く検索用 Web UI。

    python -m kaiji serve  ->  http://127.0.0.1:8765
"""

from __future__ import annotations

import html
import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlencode, urlparse

from .classify import LABELS
from .cli import parse_amount
from .db import SearchQuery, Store
from .extract import format_yen
from .textutil import truncate

KV_LABELS = {"counterparty": "相手先", "amount": "金額", "item": "内容", "period": "納期/期間",
             "revenue_timing": "売上計上", "contract_date": "日付"}

CSS = """
:root{--bg:#f7f7f5;--fg:#1d1d1f;--mut:#6b6b70;--card:#fff;--line:#e3e3e0;--acc:#1f5fbf;--pos:#137333;--neg:#b3261e;--mark:#fff1a8}
@media (prefers-color-scheme:dark){:root{--bg:#141416;--fg:#e8e8ea;--mut:#9a9aa2;--card:#1c1c1f;--line:#2c2c31;--acc:#7aa7ff;--pos:#6ccf8e;--neg:#ff8a80;--mark:#5a4b00}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
header{background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header b{font-size:17px}nav a{margin-right:12px}
main{max-width:980px;margin:0 auto;padding:16px}
form.q{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
form.q input,form.q select{padding:7px 9px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);font-size:14px}
form.q input[name=q]{flex:1 1 280px}form.q button{padding:7px 16px;border:0;border-radius:6px;background:var(--acc);color:#fff;font-size:14px;cursor:pointer}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin-bottom:10px}
.meta{color:var(--mut);font-size:13px}.ttl{font-weight:600;margin:2px 0}
.badge{display:inline-block;font-size:12px;padding:0 7px;border-radius:10px;border:1px solid var(--line);margin-right:4px;color:var(--mut)}
.b-order{border-color:var(--acc);color:var(--acc)}.b-forecast{border-color:#a05a00;color:#a05a00}
.amt{font-weight:700}.up{color:var(--pos);font-weight:700}.down{color:var(--neg);font-weight:700}
mark{background:var(--mark);color:inherit}.snip{font-size:14px;color:var(--mut)}
table{border-collapse:collapse;width:100%;background:var(--card)}td,th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;font-size:14px}
th{font-size:13px;color:var(--mut)}td.r{text-align:right;white-space:nowrap}
h2{font-size:16px;margin:18px 0 6px;border-left:4px solid var(--acc);padding-left:8px}
.pre{white-space:pre-wrap}.pos{color:var(--pos)}.neg{color:var(--neg)}
.pager{display:flex;gap:12px;margin:12px 0}.tbl{overflow-x:auto}
"""


def esc(s) -> str:
    return html.escape("" if s is None else str(s))


def highlight(text: str, terms: list[str]) -> str:
    out = esc(text)
    for t in sorted({t for t in terms if t}, key=len, reverse=True):
        out = re.sub(re.escape(esc(t)), lambda m: f"<mark>{m.group(0)}</mark>", out)
    return out


def page(title: str, body: str) -> str:
    return f"""<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} - kaiji</title><style>{CSS}</style></head>
<body><header><b><a href="/">kaiji 適時開示DB</a></b><nav>
<a href="/">検索</a><a href="/orders">受注</a><a href="/?category=forecast">業績修正</a><a href="/?category=earnings">決算短信</a>
<a href="/?watch=1">ウォッチ</a><a href="/stats">統計</a></nav></header><main>{body}</main></body></html>"""


def cat_options(selected: str | None) -> str:
    opts = ['<option value="">全カテゴリ</option>']
    for k, v in LABELS.items():
        opts.append(f'<option value="{k}"{" selected" if k == selected else ""}>{esc(v)}</option>')
    return "".join(opts)


def search_form(p: dict) -> str:
    g = lambda k: esc(p.get(k, ""))  # noqa: E731
    sort = p.get("sort", "date")
    sorts = "".join(f'<option value="{k}"{" selected" if k == sort else ""}>{v}</option>'
                    for k, v in (("date", "新しい順"), ("amount", "金額順"), ("relevance", "関連度順")))
    return f"""<form class="q" method="get" action="/">
<input name="q" value="{g('q')}" placeholder="例: 受注 半導体 / データセンター -訂正 / &quot;過去最高&quot;" autofocus>
<input name="code" value="{g('code')}" placeholder="コード" size="6">
<select name="category">{cat_options(p.get('category'))}</select>
<input name="since" value="{g('since')}" type="date"><input name="to" value="{g('to')}" type="date">
<input name="min" value="{g('min')}" placeholder="最低金額 例:10億" size="10">
<select name="sort">{sorts}</select><button>検索</button></form>"""


def row_card(r: dict, terms: list[str]) -> str:
    badges = "".join(f'<span class="badge b-{t}">{esc(LABELS.get(t, t))}</span>' for t in r["tag_list"])
    extra = ""
    if r.get("amount_yen"):
        extra += f' <span class="amt">{esc(format_yen(r["amount_yen"]))}</span>'
    if r.get("direction") == "up":
        extra += ' <span class="up">↑上方</span>'
    elif r.get("direction") == "down":
        extra += ' <span class="down">↓下方</span>'
    llm = r.get("llm") or {}
    summary = llm.get("summary") or r.get("summary") or ""
    snip = r.get("snippet") if terms else ""
    snip_html = f'<div class="snip">{highlight(snip, terms)}</div>' if snip and snip != summary else ""
    return f"""<div class="card"><div class="meta">{esc(r['date'])} {esc(r['time'])} ·
<a href="/c/{quote(r['code'])}">{esc(r['code'])} {esc(r['name'])}</a> · {badges}{extra}</div>
<div class="ttl"><a href="/d/{quote(r['id'])}">{highlight(r['title'], terms)}</a></div>
<div>{highlight(truncate(summary, 260), terms)}</div>{snip_html}</div>"""


def query_from_params(p: dict, **over) -> SearchQuery:
    def num(k):
        try:
            return int(p[k]) if p.get(k) else None
        except ValueError:
            return None

    try:
        min_amount = parse_amount(p.get("min"))
    except ValueError:
        min_amount = None
    q = SearchQuery(
        text=p.get("q", ""), code=p.get("code") or None, category=p.get("category") or None,
        date_from=p.get("since") or None, date_to=p.get("to") or None, min_amount=min_amount,
        min_importance=num("importance"), direction=p.get("direction") or None,
        watch_only=p.get("watch") == "1", sort=p.get("sort", "date"),
        limit=min(num("limit") or 50, 500), offset=num("offset") or 0,
    )
    for k, v in over.items():
        setattr(q, k, v)
    return q


class App:
    def __init__(self, store: Store):
        self.store = store
        self.lock = threading.Lock()

    def search(self, q: SearchQuery) -> list[dict]:
        with self.lock:
            return self.store.search(q)

    def h_index(self, p: dict) -> str:
        q = query_from_params(p)
        rows = self.search(q)
        terms = q.terms
        cards = "".join(row_card(r, terms) for r in rows) or "<p>該当なし</p>"
        nav = ""
        base = {k: v for k, v in p.items() if k != "offset"}
        if q.offset:
            nav += f'<a href="/?{urlencode(base | {"offset": max(0, q.offset - q.limit)})}">← 前へ</a>'
        if len(rows) == q.limit:
            nav += f'<a href="/?{urlencode(base | {"offset": q.offset + q.limit})}">次へ →</a>'
        return page("検索", search_form(p) + cards + f'<div class="pager">{nav}</div>')

    def h_orders(self, p: dict) -> str:
        q = query_from_params(p, category="order", limit=200)
        rows = self.search(q)
        trs = []
        for r in rows:
            o = r.get("order") or {}
            amt = format_yen(r.get("amount_yen")) or ("非開示" if o.get("amount_undisclosed") else "-")
            if o.get("sales_ratio") and not r.get("amount_yen"):
                amt += f"<br><span class='meta'>{esc(o['sales_ratio'])}</span>"
            detail = "<br>".join(esc(truncate(x, 90)) for x in (o.get("item"), o.get("counterparty")) if x)
            timing = esc(truncate(o.get("revenue_timing") or o.get("period") or "", 40))
            trs.append(
                f"<tr><td>{esc(r['date'])}</td><td><a href='/c/{quote(r['code'])}'>{esc(r['code'])}<br>{esc(r['name'])}</a></td>"
                f"<td><a href='/d/{quote(r['id'])}'>{esc(r['title'])}</a><div class='meta'>{detail}</div></td>"
                f"<td class='r amt'>{amt}</td><td>{timing}</td></tr>"
            )
        p2 = dict(p)
        p2.setdefault("sort", "date")
        form = search_form(p2).replace('action="/"', 'action="/orders"')
        table = ("<div class='tbl'><table><tr><th>日付</th><th>銘柄</th><th>内容</th><th>金額</th><th>計上/納期</th></tr>"
                 + "".join(trs) + "</table></div>") if trs else "<p>該当なし</p>"
        return page("受注一覧", "<h2>受注・契約獲得</h2>" + form + table)

    def h_detail(self, id_: str) -> str:
        with self.lock:
            r = self.store.get(id_)
        if not r:
            return page("not found", "<p>見つかりません</p>")
        parts = [f"""<div class="meta">{esc(r['date'])} {esc(r['time'])} · <a href="/c/{quote(r['code'])}">{esc(r['code'])} {esc(r['name'])}</a>
 · {''.join(f'<span class="badge b-{t}">{esc(LABELS.get(t, t))}</span>' for t in r['tag_list'])}</div>
<h1 style="font-size:20px">{esc(r['title'])}</h1><p><a href="{esc(r['pdf_url'])}" target="_blank" rel="noopener">PDFを開く (TDnet)</a></p>"""]
        if r.get("llm"):
            lm = r["llm"]
            pts = "".join(f"<li>{esc(x)}</li>" for x in lm.get("key_points", []))
            imp = f"<p><b>業績影響:</b> {esc(lm.get('earnings_impact'))}</p>" if lm.get("earnings_impact") else ""
            parts.append(f"<h2>AI要約</h2><div class='card'><p>{esc(lm.get('summary'))}</p><ul>{pts}</ul>{imp}</div>")
        if r.get("summary"):
            parts.append(f"<h2>要約</h2><div class='card'>{esc(r['summary'])}</div>")
        if r.get("order"):
            o = r["order"]
            rows = [(lab, o.get(k)) for k, lab in (("item", "内容"), ("counterparty", "相手先"), ("amount_text", "金額(原文)"),
                                                   ("period", "納期/期間"), ("revenue_timing", "売上計上"), ("sales_ratio", "規模"),
                                                   ("contract_date", "日付")) if o.get(k)]
            if r.get("amount_yen"):
                rows.append(("金額(円)", format_yen(r["amount_yen"])))
            parts.append("<h2>受注情報</h2><table>" + "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in rows) + "</table>")
        for key, lab in (("reason", "理由"), ("outlook", "見通し・業績への影響"), ("qualitative", "経営成績の概況(定性情報)")):
            if r.get(key):
                parts.append(f"<h2>{lab}</h2><div class='card pre'>{esc(r[key])}</div>")
        if r.get("order_mentions"):
            parts.append("<h2>受注への言及</h2><ul>" + "".join(f"<li>{esc(s)}</li>" for s in r["order_mentions"]) + "</ul>")
        if r.get("signals"):
            lis = "".join(f"<li class='{'pos' if s['polarity'] == 'pos' else 'neg' if s['polarity'] == 'neg' else ''}'>{esc(s['text'])}</li>"
                          for s in r["signals"])
            parts.append(f"<h2>シグナル</h2><ul>{lis}</ul>")
        if r.get("lead") and not r.get("qualitative"):
            parts.append(f"<h2>本文冒頭</h2><div class='card pre'>{esc(r['lead'])}</div>")
        if r.get("kv"):
            parts.append("<h2>抽出項目</h2><table>" + "".join(f"<tr><th>{esc(KV_LABELS.get(k, k))}</th><td>{esc(v)}</td></tr>" for k, v in r["kv"].items()) + "</table>")
        if r.get("body"):
            parts.append(f"<details><summary>本文テキスト</summary><div class='card pre'>{esc(r['body'])}</div></details>")
        return page(r["title"], "".join(parts))

    def h_company(self, code: str, p: dict) -> str:
        q = query_from_params(p, code=code, limit=200)
        rows = self.search(q)
        name = rows[0]["name"] if rows else code
        with self.lock:
            watched = any(w["code"] == code.upper() for w in self.store.watchlist())
        btn = (f"<form method='post' action='/watch'><input type='hidden' name='code' value='{esc(code)}'>"
               f"<input type='hidden' name='action' value='{'rm' if watched else 'add'}'>"
               f"<button>{'ウォッチ解除' if watched else 'ウォッチに追加'}</button></form>")
        cards = "".join(row_card(r, []) for r in rows) or "<p>該当なし</p>"
        return page(name, f"<h2>{esc(code)} {esc(name)} の開示タイムライン</h2>{btn}<p></p>{cards}")

    def h_stats(self) -> str:
        with self.lock:
            s = self.store.stats()
            last = self.store.get_meta("last_run")
            watch = self.store.watchlist()
        cats = "".join(f"<tr><td><a href='/?category={esc(k)}'>{esc(LABELS.get(k, k))}</a></td><td class='r'>{v}</td></tr>"
                       for k, v in s["by_category"].items())
        w = ", ".join(f"<a href='/c/{esc(x['code'])}'>{esc(x['code'])}</a>" for x in watch) or "なし"
        return page("統計", f"""<h2>統計</h2><p>総件数 {s['total']} / 期間 {esc(s['date_range'][0])} 〜 {esc(s['date_range'][1])}
 / 最終実行 {esc(last)}</p><p>ウォッチリスト: {w}</p><table><tr><th>カテゴリ</th><th>件数</th></tr>{cats}</table>""")

    def api_search(self, p: dict) -> str:
        rows = self.search(query_from_params(p))
        keep = ("id", "date", "time", "code", "name", "title", "category", "tag_list", "summary", "amount_yen",
                "direction", "order", "llm", "pdf_url", "snippet")
        return json.dumps([{k: r.get(k) for k in keep} for r in rows], ensure_ascii=False)


def make_handler(app: App):
    class H(BaseHTTPRequestHandler):
        def _send(self, body: str, ctype: str = "text/html; charset=utf-8", status: int = 200) -> None:
            data = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self) -> None:  # noqa: N802
            u = urlparse(self.path)
            p = {k: v[-1] for k, v in parse_qs(u.query).items()}
            path = u.path
            try:
                if path == "/":
                    self._send(app.h_index(p))
                elif path == "/orders":
                    self._send(app.h_orders(p))
                elif path.startswith("/d/"):
                    self._send(app.h_detail(path[3:]))
                elif path.startswith("/c/"):
                    self._send(app.h_company(path[3:], p))
                elif path == "/stats":
                    self._send(app.h_stats())
                elif path == "/api/search":
                    self._send(app.api_search(p), "application/json; charset=utf-8")
                else:
                    self._send(page("404", "<p>Not Found</p>"), status=404)
            except Exception as e:  # noqa: BLE001
                self._send(page("error", f"<pre>{esc(e)}</pre>"), status=500)

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/watch":
                self._send("", status=404)
                return
            n = int(self.headers.get("Content-Length") or 0)
            p = {k: v[-1] for k, v in parse_qs(self.rfile.read(n).decode()).items()}
            code = p.get("code", "")
            if code:
                with app.lock:
                    (app.store.watch_remove if p.get("action") == "rm" else app.store.watch_add)(code)
            self.send_response(303)
            self.send_header("Location", f"/c/{quote(code)}")
            self.end_headers()

        def log_message(self, *args) -> None:
            pass

    return H


def serve(store: Store, host: str = "127.0.0.1", port: int = 8765) -> None:
    srv = ThreadingHTTPServer((host, port), make_handler(App(store)))
    print(f"kaiji web: http://{host}:{port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
