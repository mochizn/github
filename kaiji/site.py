"""検索可能な単一HTMLファイルを生成する(ブラウザで開くだけで使える)。

サーバ不要でスマホ等でも閲覧できるよう、データをHTMLに埋め込み、検索はブラウザ内で行う。
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from .classify import LABELS
from .db import Store
from .extract import format_yen
from .textutil import truncate

TEMPLATE = """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>kaiji 適時開示DB</title>
<style>
:root{--bg:#f7f7f5;--fg:#1d1d1f;--mut:#6b6b70;--card:#fff;--line:#e3e3e0;--acc:#1f5fbf;--pos:#137333;--neg:#b3261e;--mark:#fff1a8}
@media (prefers-color-scheme:dark){:root{--bg:#141416;--fg:#e8e8ea;--mut:#9a9aa2;--card:#1c1c1f;--line:#2c2c31;--acc:#7aa7ff;--pos:#6ccf8e;--neg:#ff8a80;--mark:#5a4b00}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,"Hiragino Sans","Noto Sans JP",sans-serif}
header{background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px}main{max-width:980px;margin:0 auto;padding:12px 16px}
.f{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px}.f input,.f select{padding:7px 9px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);font-size:14px}
.f input#q{flex:1 1 260px}.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin-bottom:10px}
.meta{color:var(--mut);font-size:13px}.ttl{font-weight:600}.badge{font-size:12px;padding:0 7px;border-radius:10px;border:1px solid var(--line);margin-right:4px;color:var(--mut)}
.amt{font-weight:700}.up{color:var(--pos);font-weight:700}.down{color:var(--neg);font-weight:700}mark{background:var(--mark);color:inherit}
details{margin-top:6px}details .pre{white-space:pre-wrap;font-size:14px}a{color:var(--acc)}
</style></head><body><header><b>kaiji 適時開示DB</b> <span class="meta">__RANGE__ / 生成 __GENERATED__</span></header><main>
<div class="f"><input id="q" placeholder="例: 受注 半導体 / 上方修正 -訂正"><input id="code" placeholder="コード" size="6">
<select id="cat"><option value="">全カテゴリ</option>__OPTIONS__</select><input id="min" placeholder="最低金額(億円)" size="9">
<select id="sort"><option value="date">新しい順</option><option value="amount">金額順</option></select></div>
<div class="meta" id="count"></div><div id="list"></div></main>
<script>
const LABELS=__LABELS__;const DATA=__DATA__;
const $=id=>document.getElementById(id);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","'":"&#39;"}[c]));
const yen=v=>v==null?"":v>=1e12?(v/1e12).toFixed(2)+"兆円":v>=1e8?(v/1e8).toFixed(1)+"億円":v>=1e6?Math.round(v/1e6)+"百万円":Math.round(v)+"円";
const nf=s=>s.normalize("NFKC");
function hl(t,terms){let o=esc(t);for(const w of terms){if(!w)continue;o=o.split(esc(w)).join("<mark>"+esc(w)+"</mark>")}return o}
function render(){
 const raw=nf($("q").value).trim().split(/\\s+/).filter(Boolean);
 const inc=raw.filter(w=>!w.startsWith("-")),exc=raw.filter(w=>w.startsWith("-")&&w.length>1).map(w=>w.slice(1));
 const code=nf($("code").value).trim().toUpperCase(),cat=$("cat").value,min=parseFloat($("min").value)*1e8;
 let rows=DATA.filter(r=>{if(code&&r.c!==code)return false;if(cat&&!r.tg.includes(cat))return false;
  if(min&&!(r.a>=min))return false;const t=r._t||(r._t=nf([r.ti,r.n,r.s,r.x].join(" ")));
  return inc.every(w=>t.includes(w))&&!exc.some(w=>t.includes(w))});
 if($("sort").value==="amount")rows.sort((a,b)=>(b.a||0)-(a.a||0));
 $("count").textContent=rows.length+"件"+(rows.length>300?"(先頭300件を表示)":"");
 $("list").innerHTML=rows.slice(0,300).map(r=>`<div class="card"><div class="meta">${esc(r.d)} ${esc(r.t)} · ${esc(r.c)} ${esc(r.n)} · ${r.tg.map(t=>`<span class="badge">${esc(LABELS[t]||t)}</span>`).join("")}
 ${r.a?`<span class="amt">${yen(r.a)}</span>`:""}${r.dir==="up"?' <span class="up">↑上方</span>':r.dir==="down"?' <span class="down">↓下方</span>':""}</div>
 <div class="ttl"><a href="${esc(r.u)}" target="_blank" rel="noopener">${hl(r.ti,inc)}</a></div><div>${hl(r.s,inc)}</div>
 ${r.x?`<details><summary>詳細</summary><div class="pre">${hl(r.x,inc)}</div></details>`:""}</div>`).join("");
}
for(const id of ["q","code","cat","min","sort"])$(id).addEventListener("input",render);render();
</script></body></html>"""


def _detail(r: dict) -> str:
    parts = []
    o = r.get("order") or {}
    for k, lab in (("item", "内容"), ("counterparty", "相手先"), ("amount_text", "金額"), ("period", "納期/期間"), ("revenue_timing", "計上")):
        if o.get(k):
            parts.append(f"{lab}: {o[k]}")
    llm = r.get("llm") or {}
    if llm.get("key_points"):
        parts.append("要点: " + " / ".join(llm["key_points"]))
    for k, lab, n in (("reason", "理由", 800), ("outlook", "見通し", 600), ("qualitative", "定性情報", 2500)):
        if r.get(k):
            parts.append(f"【{lab}】\n{truncate(r[k], n)}")
    for m in r.get("metrics") or []:
        yoy = "" if m.get("yoy_pct") is None else f" (前年比 {m['yoy_pct']:+.1f}%)"
        parts.append(f"{m['metric']}: {format_yen(m['value_yen'])}{yoy}")
    if r.get("order_mentions"):
        parts.append("【受注への言及】\n" + "\n".join(r["order_mentions"]))
    return "\n".join(parts)


def build_site(store: Store, out: str | Path, months: int = 12) -> Path:
    since = (dt.date.today() - dt.timedelta(days=31 * months)).isoformat()
    data = []
    for r in store.iter_all("date >= ? AND category != 'fund'", (since,)):
        llm = r.get("llm") or {}
        data.append({
            "id": r["id"], "d": r["date"], "t": r["time"], "c": r["code"], "n": r["name"], "ti": r["title"],
            "tg": r["tag_list"], "s": truncate(llm.get("summary") or r.get("summary") or "", 300),
            "a": r.get("amount_yen"), "dir": r.get("direction") or "", "u": r.get("pdf_url"), "x": _detail(r),
        })
    data.sort(key=lambda x: (x["d"], x["t"], x["id"]), reverse=True)
    rng = f"{data[-1]['d']} 〜 {data[0]['d']} / {len(data)}件" if data else "データなし"
    opts = "".join(f'<option value="{k}">{v}</option>' for k, v in LABELS.items())
    html = (TEMPLATE.replace("__RANGE__", rng)
            .replace("__GENERATED__", dt.datetime.now().strftime("%Y-%m-%d %H:%M"))
            .replace("__OPTIONS__", opts)
            .replace("__LABELS__", json.dumps(LABELS, ensure_ascii=False))
            .replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")))
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "index.html"
    path.write_text(html, encoding="utf-8")
    return path
