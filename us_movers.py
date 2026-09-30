"""米国株の大型株（時価総額100億ドル以上）で、当日 ±5% 以上動いた銘柄とその理由をまとめる。

使い方:
    python us_movers.py                     # 標準出力に Markdown レポート
    python us_movers.py -o report.md        # ファイルに保存
    python us_movers.py --no-ai             # Claude を使わずニュース見出しだけ列挙
    python us_movers.py --min-cap 5e10 --threshold 3

データ: Yahoo Finance（yfinance のスクリーナー + 銘柄ニュース）
理由の要約: Claude API（ANTHROPIC_API_KEY などの認証情報が必要）+ Web 検索
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from dataclasses import dataclass, field

import yfinance as yf
from yfinance import EquityQuery

MODEL = "claude-opus-5-5"
MAX_NEWS_PER_TICKER = 8
# 米国の取引所（ADR も含む）。OTC は除外する。
US_EXCHANGES = ["NMS", "NYQ", "NGM", "NCM", "ASE", "PCX", "BTS"]


@dataclass
class Mover:
    symbol: str
    name: str
    change_pct: float
    price: float | None
    market_cap: float | None
    sector: str | None
    headlines: list[dict] = field(default_factory=list)


def fetch_movers(min_cap: float, threshold: float) -> list[Mover]:
    """Yahoo Finance のスクリーナーで条件に合う銘柄を取得する。"""
    query = EquityQuery("and", [
        EquityQuery("eq", ["region", "us"]),
        EquityQuery("is-in", ["exchange", *US_EXCHANGES]),
        EquityQuery("gte", ["intradaymarketcap", min_cap]),
        EquityQuery("or", [
            EquityQuery("gte", ["percentchange", threshold]),
            EquityQuery("lte", ["percentchange", -threshold]),
        ]),
    ])

    quotes: list[dict] = []
    offset, page = 0, 250
    while True:
        res = yf.screen(query, offset=offset, size=page,
                        sortField="percentchange", sortAsc=False)
        batch = res.get("quotes", [])
        quotes.extend(batch)
        offset += len(batch)
        if not batch or offset >= res.get("total", 0):
            break

    movers = []
    seen = set()
    for q in quotes:
        sym = q.get("symbol")
        pct = q.get("regularMarketChangePercent")
        if not sym or pct is None or sym in seen:
            continue
        # スクリーナー側の値と念のため突き合わせる
        if abs(pct) < threshold or (q.get("marketCap") or 0) < min_cap:
            continue
        seen.add(sym)
        movers.append(Mover(
            symbol=sym,
            name=q.get("longName") or q.get("shortName") or sym,
            change_pct=pct,
            price=q.get("regularMarketPrice"),
            market_cap=q.get("marketCap"),
            sector=q.get("sector"),
        ))
    movers.sort(key=lambda m: m.change_pct, reverse=True)
    return movers


def fetch_headlines(symbol: str) -> list[dict]:
    """銘柄ごとの直近ニュース見出しを取得する（yfinance の新旧フォーマット両対応）。"""
    try:
        items = yf.Ticker(symbol).news or []
    except Exception as e:  # ニュース取得失敗はレポート全体を止めない
        print(f"[warn] {symbol}: news fetch failed: {e}", file=sys.stderr)
        return []
    out = []
    for item in items[:MAX_NEWS_PER_TICKER]:
        c = item.get("content", item)
        url = (c.get("canonicalUrl") or {}).get("url") or c.get("link")
        publisher = (c.get("provider") or {}).get("displayName") or c.get("publisher")
        title = c.get("title")
        if title:
            out.append({"title": title, "publisher": publisher,
                        "date": c.get("pubDate") or c.get("providerPublishTime"),
                        "url": url})
    return out


def fmt_cap(v: float | None) -> str:
    if not v:
        return "-"
    return f"${v / 1e12:.2f}T" if v >= 1e12 else f"${v / 1e9:.1f}B"


def summarize_with_claude(movers: list[Mover], date: str) -> str:
    """Claude に見出し + Web 検索で値動きの理由を日本語でまとめてもらう。"""
    import anthropic

    client = anthropic.Anthropic()

    lines = []
    for m in movers:
        lines.append(f"### {m.symbol} ({m.name}) {m.change_pct:+.2f}% "
                     f"価格 {m.price} / 時価総額 {fmt_cap(m.market_cap)} / {m.sector or '-'}")
        for h in m.headlines:
            lines.append(f"- {h['title']} ({h['publisher']}, {h['date']}) {h['url'] or ''}")
        if not m.headlines:
            lines.append("- (ニュース見出しなし)")
    data = "\n".join(lines)

    prompt = f"""以下は {date} の米国株市場で、時価総額100億ドル以上かつ前日比±5%以上動いた銘柄の一覧と、各銘柄の直近ニュース見出しです。

{data}

各銘柄について、その日の値動きの主な理由を日本語で簡潔にまとめてください。
- 見出しで理由がはっきりしない銘柄は Web 検索で確認してください（決算、ガイダンス、格付け変更、M&A、規制、セクター全体の動き、マクロ要因など）。
- 理由が確認できない場合は推測で埋めず「明確な材料は見つからず」と書き、考えられる背景があれば「推測」と明記してください。
- 出力は Markdown で、まず全体の傾向を2〜3文、続いて「上昇銘柄」「下落銘柄」の見出しごとに、
  `| ティッカー | 銘柄名 | 騰落率 | 理由 |` の表を作ってください。表の後に主要な情報源URLを列挙してください。"""

    messages = [{"role": "user", "content": prompt}]
    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 20}]

    for _ in range(5):  # pause_turn の再開上限
        with client.beta.messages.stream(
            model=MODEL,
            max_tokens=64000,
            thinking={"type": "adaptive"},
            output_config={"effort": "medium"},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            tools=tools,
            messages=messages,
        ) as stream:
            response = stream.get_final_message()

        if response.stop_reason == "pause_turn":
            messages = [messages[0], {"role": "assistant", "content": response.content}]
            continue
        if response.stop_reason == "refusal":
            raise RuntimeError("Claude が要約を拒否しました")
        break

    return "".join(b.text for b in response.content if b.type == "text").strip()


def render_plain(movers: list[Mover]) -> str:
    """Claude を使わない場合のレポート（ニュース見出しを列挙）。"""
    out = []
    for title, group in (("上昇銘柄", [m for m in movers if m.change_pct > 0]),
                         ("下落銘柄", [m for m in movers if m.change_pct < 0])):
        out.append(f"## {title}\n")
        if not group:
            out.append("該当なし\n")
        for m in group:
            out.append(f"### {m.symbol} {m.name}  {m.change_pct:+.2f}% "
                       f"(時価総額 {fmt_cap(m.market_cap)})")
            for h in m.headlines[:5]:
                link = f" — {h['url']}" if h["url"] else ""
                out.append(f"- {h['title']} ({h['publisher']}){link}")
            if not m.headlines:
                out.append("- ニュース見出しなし")
            out.append("")
    return "\n".join(out)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--min-cap", type=float, default=1e10, help="最低時価総額 (USD, 既定 1e10)")
    p.add_argument("--threshold", type=float, default=5.0, help="騰落率のしきい値 %% (既定 5)")
    p.add_argument("--no-ai", action="store_true", help="Claude による要約を行わない")
    p.add_argument("-o", "--output", help="レポートの保存先 (Markdown)")
    args = p.parse_args()

    date = dt.date.today().isoformat()
    print(f"[info] スクリーニング中 (時価総額 >= {fmt_cap(args.min_cap)}, "
          f"|騰落率| >= {args.threshold}%)", file=sys.stderr)
    movers = fetch_movers(args.min_cap, args.threshold)
    print(f"[info] {len(movers)} 銘柄が該当", file=sys.stderr)

    for m in movers:
        m.headlines = fetch_headlines(m.symbol)

    header = (f"# 米国大型株 値動きレポート ({date})\n\n"
              f"条件: 時価総額 {fmt_cap(args.min_cap)} 以上 / 騰落率 ±{args.threshold}% 以上 / "
              f"該当 {len(movers)} 銘柄\n\n")

    if not movers:
        body = "該当銘柄はありませんでした。\n"
    elif args.no_ai:
        body = render_plain(movers)
    else:
        print("[info] Claude で理由を要約中...", file=sys.stderr)
        body = summarize_with_claude(movers, date)

    report = header + body + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[info] {args.output} に保存しました", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
