"""開示PDFテキストからの情報抽出(ルールベース)。

- 受注開示: 受注先 / 受注金額(円換算) / 内容 / 納期 / 売上計上時期 / 業績影響
- 決算短信: 経営成績の概況(定性的情報) / 業績見通し / 受注高・受注残への言及
- 業績修正: 修正の理由 / 上方・下方
- その他: リード文・見通し・キーバリュー
- 共通: ポジティブ/ネガティブなシグナル文
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from .textutil import clean_text, join_wrapped_lines, nfkc, split_sentences, truncate

# ---------------------------------------------------------------------------
# 金額
# ---------------------------------------------------------------------------

_UNIT = {"兆": 10**12, "億": 10**8, "千万": 10**7, "百万": 10**6, "十万": 10**5, "万": 10**4, "千": 10**3, "": 1}
_CUR = r"(円|米ドル|USドル|US\$|ドル|ユーロ|EUR|人民元|元|ポンド|USD)"
_NUM = r"[0-9][0-9,]*(?:\.[0-9]+)?"
_AMOUNT_RE = re.compile(
    rf"(?P<approx>約|概算|総額|およそ)?\s*"
    rf"(?:(?P<oku>{_NUM})\s*億\s*(?:(?P<sen>[0-9]+)\s*千)?\s*(?:(?P<hyaku>[0-9]+)\s*百)?\s*(?P<man>{_NUM})?\s*万\s*(?P<cur1>{_CUR})"
    rf"|(?P<num>{_NUM})\s*(?P<unit>兆|億|千万|百万|十万|万|千)?\s*(?P<cur2>{_CUR}))"
)


@dataclass
class Amount:
    value: float  # 通貨単位での値(円なら円)
    currency: str  # JPY / USD / EUR / CNY / GBP
    raw: str
    approx: bool = False

    @property
    def yen(self) -> float | None:
        return self.value if self.currency == "JPY" else None


def _cur_code(s: str) -> str:
    if s == "円":
        return "JPY"
    if s in ("ユーロ", "EUR"):
        return "EUR"
    if s in ("人民元", "元"):
        return "CNY"
    if s == "ポンド":
        return "GBP"
    return "USD"


def parse_amounts(text: str) -> list[Amount]:
    t = nfkc(text)
    out: list[Amount] = []
    for m in _AMOUNT_RE.finditer(t):
        if m.group("oku"):
            man = (int(m.group("sen") or 0) * 1000 + int(m.group("hyaku") or 0) * 100
                   + float((m.group("man") or "0").replace(",", "")))
            v = float(m.group("oku").replace(",", "")) * 10**8 + man * 10**4
            cur = m.group("cur1")
        else:
            v = float(m.group("num").replace(",", "")) * _UNIT[m.group("unit") or ""]
            cur = m.group("cur2")
        out.append(Amount(v, _cur_code(cur), m.group(0).strip(), bool(m.group("approx"))))
    return out


def best_yen(text: str) -> tuple[float | None, bool]:
    """テキスト中の円建て金額(なければNone)と「約」表記かを返す。

    外貨併記(例: 20.4百万USドル(3,212百万円))の場合は円換算額を採用する。
    「年間X円(3年総額Y円)」のような併記は先頭(年間)を採用する。
    """
    for a in parse_amounts(text):
        if a.currency == "JPY" and a.value >= 1000:
            return a.value, a.approx
    return None, False


def format_yen(v: float | None) -> str:
    if v is None:
        return ""
    if v >= 10**12:
        return f"{v / 10**12:,.2f}兆円"
    if v >= 10**8:
        return f"{v / 10**8:,.1f}億円"
    if v >= 10**6:
        return f"{v / 10**6:,.0f}百万円"
    return f"{v:,.0f}円"


# ---------------------------------------------------------------------------
# 構造解析
# ---------------------------------------------------------------------------

_HEADER_HINT = re.compile(r"(各位|会社名|代表者|問合せ|問い合わせ|コード|TEL|電話|上場会社名|URL|上場取引所)", re.I)
_L1 = re.compile(r"^(?:[0-9]{1,2}|[一二三四五六七八九十]{1,2})\s*[\.．、]\s*(?P<h>\S.{0,48})$")
_L2 = re.compile(r"^[\(（](?:[0-9]{1,2}|[一二三四五六七八九十])[\)）]\s*(?P<h>\S.{0,48})$")
_L3 = re.compile(r"^[①-⑳]\s*(?P<h>\S.{0,48})$")
_KI = re.compile(r"^記$")
_END = re.compile(r"^以\s*上$")


def _norm_key(s: str) -> str:
    return re.sub(r"\s+", "", nfkc(s))


def strip_header(lines: list[str], title: str) -> list[str]:
    """会社名・代表者・問合せ先等の冒頭ブロックとタイトル行(折り返し含む)を除去する。"""
    nt = _norm_key(title)
    start = None
    for i, ln in enumerate(lines[:30]):
        nk = _norm_key(ln)
        if len(nk) >= 6 and not _HEADER_HINT.search(ln) and (nk in nt or nt[:12] in nk):
            start = i
            break
    if start is None:
        last = -1
        for i, ln in enumerate(lines[:20]):
            if _HEADER_HINT.search(ln):
                last = i
        return lines[last + 1 :]
    # タイトルが複数行に折り返されている場合は続く行もスキップ
    j = start + 1
    acc = _norm_key(lines[start])
    while j < len(lines) and j < start + 4:
        nk = _norm_key(lines[j])
        if nk and (acc + nk) in nt or (nk and nk in nt and len(nk) <= 30 and nt.endswith(nk)):
            acc += nk
            j += 1
        else:
            break
    return lines[j:]


@dataclass
class Section:
    level: int
    heading: str
    lines: list[str]

    @property
    def text(self) -> str:
        return join_wrapped_lines("\n".join(self.lines))


def _heading_level(line: str) -> tuple[int, str] | None:
    for lv, rx in ((1, _L1), (2, _L2), (3, _L3)):
        m = rx.match(line)
        if m:
            h = m.group("h")
            # 本文的な長文や数値行は見出しとみなさない
            if h.endswith("。") or re.match(r"^[0-9,.\s△▲%％]+$", h):
                return None
            return lv, h
    return None


def find_sections(lines: list[str], pattern: str, max_chars: int = 4000) -> list[str]:
    """見出しが pattern にマッチするセクション本文を返す(同レベル以上の次見出しまで)。"""
    rx = re.compile(pattern)
    out: list[str] = []
    i = 0
    while i < len(lines):
        hl = _heading_level(lines[i])
        bare = None if hl else (lines[i] if len(lines[i]) <= 40 and rx.search(lines[i]) and not lines[i].endswith("。") else None)
        if (hl and rx.search(hl[1])) or bare:
            level = hl[0] if hl else 1
            body: list[str] = []
            j = i + 1
            while j < len(lines):
                h2 = _heading_level(lines[j])
                if h2 and h2[0] <= level:
                    break
                if _END.match(lines[j]):
                    break
                body.append(lines[j])
                j += 1
            txt = join_wrapped_lines("\n".join(body)).strip()
            if txt:
                out.append(truncate(txt, max_chars))
            i = j
            continue
        i += 1
    return out


# ---------------------------------------------------------------------------
# キーバリュー
# ---------------------------------------------------------------------------

KV_KEYS: dict[str, str] = {
    "counterparty": r"受注先|発注者|発注元|契約(?:の)?相手(?:先|方)?|相手先|取引先|顧客名?|納入先|委託者|販売先|契約先|供給先|発注先|ライセンス先|導出先",
    "amount": r"受注金額|契約金額|受注額|受注総額|契約総額|落札金額|契約額|受託金額|事業費|補助金(?:額|交付額|交付決定額)?|交付決定額|採択金額|助成金額?|総事業費|金額",
    "item": r"受注製品|受注品目|受注内容|受注の内容|受注案件|受注施工|案件名|件名|業務名|契約(?:の)?内容|製品名|品目|対象製品|事業名|プロジェクト名|工事名|受注業務|契約の概要|業務内容|納入製品",
    "period": r"納期|契約納期|納入時期|納入予定(?:時期)?|納品(?:時期|予定)|引渡し?(?:時期|予定)?|契約期間|工期|履行期間|施工(?:完了|期間)|提供(?:時期|期間|開始)|サービス開始|実施期間|事業期間|完成予定",
    "revenue_timing": r"売上計上(?:予定|時期)?|計上(?:予定)?時期|収益計上(?:時期)?|売上(?:予定|時期)",
    "contract_date": r"受注日|契約(?:締結)?日|締結日|採択日|交付決定日|受注年月日",
}
_KV_ANY = "|".join(f"(?P<{k}>{v})" for k, v in KV_KEYS.items())
_KV_LINE = re.compile(
    rf"^(?:[\(（]?[0-9]{{1,2}}[\)）\.．]|[①-⑳]|[・●■◆])?\s*(?:{_KV_ANY})\s*(?P<sep>[:：]|\s)?\s*(?P<val>.+)$"
)


def extract_kv(lines: list[str]) -> dict[str, str]:
    """「受注金額 ： 約7.7億円」のような行を抽出する。継続行は連結する。"""
    found: dict[str, str] = {}
    cur_key: str | None = None
    for ln in lines:
        m = _KV_LINE.match(ln)
        if m and not m.group("sep") and (ln.endswith("。") or len(ln) > 80 or re.match(r"[はがをにのでと、]", m.group("val"))):
            m = None  # 区切りのない文章は対象外
        if m:
            key = next(k for k in KV_KEYS if m.group(k))
            val = m.group("val").strip(" :：")
            if re.match(r"^(\(.{1,10}\))?(の概要|の状況|の内容|等$|について)", val) or len(val) < 2:
                val = ""  # 「相手先(親会社)の概要」のような表見出し
            if key not in found and val:
                found[key] = val
                cur_key = key
            else:
                cur_key = None
            continue
        if cur_key and _heading_level(ln) is None and not _END.match(ln) and len(found[cur_key]) < 300:
            # 折り返し・注記(※)を継続行として連結
            prev_val = found[cur_key]
            wrapped = len(prev_val) >= 28 or prev_val.endswith(("、", ",", "及び", "および", "並びに", "ならびに", "・"))
            if ln.startswith("※") or (wrapped and not re.match(r"^[\(（]?注", ln)):
                found[cur_key] += " " + ln
                continue
        cur_key = None
    return found


# ---------------------------------------------------------------------------
# シグナル
# ---------------------------------------------------------------------------

_POS = re.compile(
    r"過去最高|最高益|増収増益|上方修正|好調|堅調|伸長|上回る|上回り|上回った|上振れ|"
    r"受注.{0,8}(増加|拡大|好調|伸長|積み上が)|需要.{0,6}(拡大|旺盛|回復|増加)|価格(改定|転嫁)|値上げ|黒字(化|転換)|増配|復配"
)
_NEG = re.compile(
    r"減収減益|下方修正|下回る|下回り|下回った|下振れ|低調|悪化|遅延|ずれ込|減損|赤字|低迷|停滞|"
    r"受注.{0,8}(減少|低迷|減速)|需要.{0,6}(減少|低迷|減速|弱含)|無配|減配|延期|中止"
)


# マクロ環境の説明文はシグナルから除外する
_MACRO = re.compile(r"(わが国|我が国|日本|世界|米国|中国|欧州)(の)?経済|景気|先行き(は|が)?不透明|為替相場|金融市場")


def extract_signals(text: str, limit: int = 6) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for s in split_sentences(text):
        if len(s) < 12 or _MACRO.search(s):
            continue
        p, n = _POS.search(s), _NEG.search(s)
        if not (p or n):
            continue
        key = s[:40]
        if key in seen:
            continue
        seen.add(key)
        pol = "mixed" if (p and n) else ("pos" if p else "neg")
        out.append({"polarity": pol, "text": truncate(s, 220)})
        if len(out) >= limit:
            break
    return out


# ---------------------------------------------------------------------------
# 抽出本体
# ---------------------------------------------------------------------------

_BOILER = re.compile(
    r"(ので|ため)?、?\s*(下記|以下)の?(とおり|通り)\s*(お知らせ|ご報告|ご案内)(いた|致)?します。?"
    r"|ので、?\s*お知らせ(いた|致)?します。?"
)


@dataclass
class Extracted:
    lead: str = ""
    summary: str = ""
    outlook: str = ""
    reason: str = ""
    qualitative: str = ""
    kv: dict = field(default_factory=dict)
    order: dict = field(default_factory=dict)
    order_mentions: list = field(default_factory=list)
    metrics: list = field(default_factory=list)  # 受注高・受注残高などの数値
    direction: str = ""  # forecast: up/down/mixed
    signals: list = field(default_factory=list)
    amount_yen: float | None = None
    body: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _lead(lines: list[str]) -> str:
    buf: list[str] = []
    for ln in lines:
        if not buf and len(ln) < 60 and re.search(r"(お知らせ|について|に関する件)$", ln):
            continue  # 残ったタイトル行
        if _KI.match(ln) or _heading_level(ln) and buf:
            break
        buf.append(ln)
        if sum(map(len, buf)) > 800:
            break
    text = join_wrapped_lines("\n".join(buf))
    text = _BOILER.sub("。", text).replace("。。", "。")
    return truncate(text.strip(), 600)


def _first_sentences(text: str, n: int = 2, max_len: int = 220) -> str:
    sents = [s for s in split_sentences(text) if len(s) >= 8]
    return truncate("".join(sents[:n]), max_len)


def _extract_order(ex: Extracted, lines: list[str], full: str) -> None:
    kv = ex.kv
    order: dict = {}
    for k in ("counterparty", "item", "period", "revenue_timing", "contract_date"):
        if kv.get(k):
            order[k] = truncate(kv[k], 200)
    amt_src = kv.get("amount", "")
    if not amt_src:
        m = re.search(r"(受注|契約|落札|総)(金)?額[はがを]?\s*(約)?[^。\n]{0,40}?円", full)
        amt_src = m.group(0) if m else ""
    if amt_src and best_yen(amt_src)[0] is None and parse_amounts(amt_src):
        # 外貨建ての場合、注記の円換算額を探す
        m = re.search(r"円換算[^。]{0,80}?" + _NUM + r"\s*(兆|億|百万|万|千)?円", nfkc(full))
        if m:
            amt_src = amt_src + " / " + m.group(0)
    if amt_src:
        order["amount_text"] = truncate(amt_src, 160)
        yen, approx = best_yen(amt_src)
        if yen is not None:
            order["amount_yen"] = yen
            order["amount_approx"] = approx
            ex.amount_yen = yen
        fx = [a for a in parse_amounts(amt_src) if a.currency != "JPY"]
        if fx:
            order["amount_foreign"] = {"value": fx[0].value, "currency": fx[0].currency}
    if re.search(r"非開示|開示を?差し?控え|守秘義務", amt_src or ""):
        order["amount_undisclosed"] = True
    m = re.search(r"売上高(?:の)?\s*([0-9]+(?:\.[0-9]+)?)\s*[%％]\s*(以上|超|相当)?", nfkc(full))
    if m:
        order["sales_ratio"] = f"売上高の{m.group(1)}%{m.group(2) or ''}"
    ex.order = order


def _extract_earnings(ex: Extracted, lines: list[str]) -> None:
    qual = find_sections(
        lines,
        r"経営成績(等)?(の|に関する)(概況|説明|分析)|経営成績の概況|定性的情報|経営成績等の状況",
        max_chars=6000,
    )
    if qual:
        ex.qualitative = qual[0]
    outlook = find_sections(
        lines,
        r"将来予測情報|今後の見通し|次期の見通し|通期の見通し|業績予想(など|等)?に関する|今後の業績見通し",
        max_chars=2500,
    )
    if outlook:
        ex.outlook = outlook[0]
    text = ex.qualitative or "\n".join(lines)
    sents = split_sentences(text)
    head = next((s for s in sents if ("以上の結果" in s or "その結果" in s or "売上高" in s) and re.search(r"[0-9]", s)
                 and re.search(r"(売上|営業収益|収益|利益)", s) and re.search(r"円", s)), "")
    if not head:
        head = next((s for s in split_sentences(text) if re.search(r"(売上高|営業収益|売上収益)", s) and re.search(r"円", s) and re.search(r"[%％]", s)), "")
    ex.summary = truncate(head, 300)
    ex.metrics = extract_order_metrics("\n".join([ex.qualitative, ex.outlook]))
    ex.order_mentions = [
        truncate(s, 200) for s in split_sentences("\n".join([ex.qualitative, ex.outlook])) if re.search(r"受注(高|残|額|残高|環境|状況)", s)
    ][:6]


_UP = r"上回る|上回り|上回った|上方修正|増加する見込み|上振れ|増益"
_DOWN = r"下回る|下回り|下回った|下方修正|減少する見込み|下振れ|減益|損失(の|を)?計上"


def forecast_direction(title: str, text: str) -> str:
    """業績修正の方向。タイトル明記 > 利益に関する記述 > 全体 の順で判定。"""
    t = nfkc(title)
    if "上方修正" in t and "下方修正" not in t:
        return "up"
    if "下方修正" in t and "上方修正" not in t:
        return "down"
    # 「売上高は上回ったが、利益は下回った」を分けて評価するため節単位に分割
    sents = [c for x in split_sentences(nfkc(text)) for c in re.split(r"が、|ものの|一方[、で]?|しかしながら", x) if c]
    profit = [x for x in sents if re.search(r"利益|損益|損失", x)]
    for group in (profit, sents):
        up = sum(len(re.findall(_UP, x)) for x in group)
        down = sum(len(re.findall(_DOWN, x)) for x in group)
        if up or down:
            return "up" if up > down * 1.5 else "down" if down > up * 1.5 else "mixed"
    return ""


_METRIC_RE = re.compile(r"(新規受注高|受注残高|受注残|受注高|受注額|受注金額)")
_YOY_RE = re.compile(r"前年同期比\s*([0-9]+(?:\.[0-9]+)?)\s*[%％]\s*(増|減)")


def extract_order_metrics(text: str, limit: int = 6) -> list[dict]:
    """「受注高は37,270百万円(前年同期比52.2%増加)」のような記述を数値化する。"""
    out: list[dict] = []
    for sent in split_sentences(nfkc(text)):
        for m in _METRIC_RE.finditer(sent):
            tail = sent[m.end(): m.end() + 45]
            # 次の指標名・「売上高」等が出てくる前の金額だけを対象にする
            stop = re.search(r"受注|売上|利益|損失|件数", tail)
            window = tail[: stop.start()] if stop else tail
            amts = [a for a in parse_amounts(window) if a.currency == "JPY"]
            if not amts:
                continue
            a = amts[0]
            after = sent[m.end(): m.end() + 80]
            y = _YOY_RE.search(after[: after.find("。") if "。" in after else None])
            yoy = None
            if y:
                yoy = float(y.group(1)) * (1 if y.group(2) == "増" else -1)
            metric = "受注残高" if m.group(1).startswith("受注残") else "受注高"
            out.append({"metric": metric, "value_yen": a.value, "yoy_pct": yoy, "text": truncate(sent, 160)})
            if len(out) >= limit:
                return out
    return out


def _extract_forecast(ex: Extracted, lines: list[str], full: str, title: str) -> None:
    reason = find_sections(lines, r"修正の理由|差異の理由|理由|修正の内容及び理由|背景", max_chars=2500)
    if reason:
        ex.reason = reason[0]
    ex.direction = forecast_direction(title, ex.reason or full)


def extract(raw_text: str, title: str, tags: list[str] | tuple[str, ...] = ()) -> Extracted:
    lines = clean_text(raw_text).splitlines()
    body_lines = strip_header(lines, title)
    ex = Extracted()
    ex.body = truncate(join_wrapped_lines("\n".join(body_lines)), 30000)
    ex.lead = _lead(body_lines)
    ex.kv = extract_kv(body_lines)

    outlook = find_sections(
        body_lines, r"今後の見通し|業績への影響|業績に与える影響|業績に及ぼす影響|今後の業績|将来の見通し|今後の展開|当社業績への影響", 1500
    )
    if outlook:
        ex.outlook = outlook[0]

    tagset = set(tags)
    if "earnings" in tagset:
        _extract_earnings(ex, body_lines)
    if "forecast" in tagset:
        _extract_forecast(ex, body_lines, ex.body, title)
    if tagset & {"order", "subsidy"} or (ex.kv.get("amount") and tagset & {"alliance", "new_biz"}):
        _extract_order(ex, body_lines, ex.body)

    ex.signals = extract_signals("\n".join(x for x in (ex.qualitative, ex.outlook, ex.reason, ex.lead) if x))
    if not ex.summary:
        ex.summary = rule_summary(ex, tagset)
    return ex


def rule_summary(ex: Extracted, tags: set[str]) -> str:
    if ex.order:
        o = ex.order
        parts = []
        if o.get("item"):
            parts.append(f"内容: {truncate(o['item'], 60)}")
        if o.get("counterparty"):
            parts.append(f"相手先: {truncate(o['counterparty'], 50)}")
        if o.get("amount_yen"):
            parts.append(f"金額: {'約' if o.get('amount_approx') else ''}{format_yen(o['amount_yen'])}")
        elif o.get("amount_undisclosed"):
            parts.append("金額: 非開示" + (f"({o['sales_ratio']})" if o.get("sales_ratio") else ""))
        elif o.get("amount_text"):
            parts.append(f"金額: {truncate(o['amount_text'], 50)}")
        for k, lab in (("period", "納期/期間"), ("revenue_timing", "計上")):
            if o.get(k):
                parts.append(f"{lab}: {truncate(o[k], 40)}")
        head = " / ".join(parts)
        lead = _first_sentences(ex.lead, 1, 160)
        return truncate(f"{head}。{lead}" if head else lead, 400)
    if "forecast" in tags and ex.reason:
        d = {"up": "【上方】", "down": "【下方】", "mixed": "【修正】"}.get(ex.direction, "")
        return d + _first_sentences(ex.reason, 2, 300)
    return _first_sentences(ex.lead, 2, 300)
