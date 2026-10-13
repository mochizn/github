"""日本語テキストの正規化ユーティリティ。"""

from __future__ import annotations

import re
import unicodedata

_CJK = r"　-ヿ㐀-䶿一-鿿＀-￯々〆ヶ"
# PDF抽出で「会 社 名」のように和文字の間に入る空白
_CJK_CHAR = re.compile(rf"[{_CJK}]")
# 「受注金額 747百万円」のような項目名と値の区切りは残すため、和文字→数字は年月等の後のみ詰める
_DIGIT_CJK_SPACE = re.compile(rf"(?<=[0-9]) (?=[{_CJK}])|(?<=[年月約第]) (?=[0-9])")


def _collapse_letter_spacing(s: str) -> str:
    """「受 注 金 額」「株 式会社」のような字間スペースだけを詰める。

    1文字の和文字トークンに隣接するスペースのみ除去し、
    「受注先 国内大手企業」のような語の区切りは残す。
    """
    toks = s.split(" ")
    if len(toks) < 2:
        return s
    out = [toks[0]]
    prev_single = len(toks[0]) == 1 and bool(_CJK_CHAR.fullmatch(toks[0]))
    for t in toks[1:]:
        single = len(t) == 1 and bool(_CJK_CHAR.fullmatch(t))
        prev = out[-1]
        if t and prev and (single or (prev_single and len(t) <= 2)) and _CJK_CHAR.fullmatch(prev[-1]) and _CJK_CHAR.fullmatch(t[0]):
            out[-1] = prev + t
        else:
            out.append(t)
        prev_single = single
    return " ".join(out)


def nfkc(s: str) -> str:
    """全角英数・記号を半角へ寄せる(検索・パターンマッチ用)。"""
    return unicodedata.normalize("NFKC", s or "")


def clean_line(s: str) -> str:
    s = nfkc(s).replace("　", " ")
    s = re.sub(r"[ \t]+", " ", s).strip()
    # 「2026 年 10 月」「1,000 百万円」のような数字と和文字の間の空白を詰める
    s = _DIGIT_CJK_SPACE.sub("", s)
    return _collapse_letter_spacing(s)


_PAGE_NO = re.compile(r"^[-－‐ー―]?\s*\d{1,3}\s*[-－‐ー―]?$")
_TOC_LEADER = re.compile(r"(…|‥|･･|・・|\.\.\.\.|………)")
# 決算短信の各ページ上部に付くランニングヘッダ(例: ㈱リソー教育グループ(4714) 2027年２月期 ...決算短信)
_RUNNING_HEAD = re.compile(r"^.{0,40}\(\d{3}[0-9A-Z]\d?\).{0,60}(決算短信|四半期|期末|説明資料)?.{0,20}$")


def clean_text(raw: str) -> str:
    """PDF抽出テキストを行単位で正規化し、ページ番号・目次・ランニングヘッダを落とす。"""
    out: list[str] = []
    for line in (raw or "").splitlines():
        c = clean_line(line)
        if not c:
            continue
        if _PAGE_NO.match(c) or re.fullmatch(r"[\(（]?\d{3}[0-9A-Z][\)）]?", c):
            continue
        if _TOC_LEADER.search(c):
            continue
        if _RUNNING_HEAD.match(c) and ("決算短信" in c or "四半期" in c or "説明資料" in c):
            continue
        out.append(c)
    return "\n".join(out)


# 行頭が見出し・箇条書きなら改行を維持する
_BLOCK_START = re.compile(
    r"^("
    r"[0-9]{1,2}[\.．、]|"  # 1. 1、
    r"\([0-9a-zA-Z]{1,2}\)|"  # (1)
    r"[①-⑳]|"
    r"[■□●○◆◇・※＊*【〔\[]|"
    r"(記|以上|以 上)$|"
    r"注\s?\d|"
    r"[ア-ン][\.．]"
    r")"
)


def join_wrapped_lines(text: str, wrap_min: int = 30) -> str:
    """PDFの折り返しで切れた行を連結して段落に戻す。

    直前の物理行が短い(=段落末)か句点で終わる場合、または次行が見出し・箇条書き
    で始まる場合は改行を維持する。
    """
    paras: list[str] = []
    last_len = 0
    for line in text.splitlines():
        if paras:
            prev = paras[-1]
            keep = (
                _BLOCK_START.match(line)
                or prev.endswith(("。", ":", "："))
                or last_len < wrap_min
            )
            if not keep:
                sep = " " if re.search(r"[A-Za-z0-9,]$", prev) and re.match(r"[A-Za-z0-9]", line) else ""
                paras[-1] = prev + sep + line
                last_len = len(line)
                continue
        paras.append(line)
        last_len = len(line)
    return "\n".join(paras)


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=。)|\n", text)
    return [p.strip() for p in parts if p and p.strip()]


def truncate(s: str, n: int) -> str:
    s = s or ""
    return s if len(s) <= n else s[: n - 1] + "…"
