"""PDF -> テキスト抽出。

pypdfium2 を優先(pdfplumber より十数倍速く、行構造はほぼ同等)。
失敗時や文字が取れない場合は pdfplumber -> pypdf の順にフォールバックする。
"""

from __future__ import annotations

import io
import logging
import re

log = logging.getLogger(__name__)


def is_readable(text: str) -> bool:
    """抽出テキストが意味のある文字列かを判定する。

    - 画像のみのPDF: 空になる
    - フォントにUnicode対応表が無いPDF: pdfplumberでは (cid:123) の羅列、pdfiumでは無関係な漢字・記号の羅列になる
      日本語の文章には必ず平仮名が一定割合含まれるので、それを手掛かりにする(英文PDFはラテン文字比率で許容)。
    """
    body = re.sub(r"\s+", "", text)
    if len(body) < 20:
        return False
    if len(re.findall(r"\(cid:\d+\)", text)) * 8 > len(body) * 0.3:
        return False
    if len(body) < 200:
        return True
    hira = len(re.findall(r"[\u3041-\u309f]", body))
    latin = len(re.findall(r"[A-Za-z]", body))
    return hira / len(body) >= 0.03 or latin / len(body) >= 0.4


def _pdfium(data: bytes, max_pages: int) -> str:
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(data)
    try:
        pages = []
        for i in range(min(max_pages, len(doc))):
            page = doc[i]
            tp = page.get_textpage()
            pages.append(tp.get_text_range())
            tp.close()
            page.close()
    finally:
        doc.close()
    return "\n".join(pages).replace("\r\n", "\n").replace("\r", "\n")


def _pdfplumber(data: bytes, max_pages: int) -> str:
    import pdfplumber

    with pdfplumber.open(io.BytesIO(data)) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages[:max_pages])


def _pypdf(data: bytes, max_pages: int) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    return "\n".join((p.extract_text() or "") for p in reader.pages[:max_pages])


def pdf_to_text(data: bytes, max_pages: int = 30) -> str:
    fallback = ""
    for name, fn in (("pdfium", _pdfium), ("pdfplumber", _pdfplumber), ("pypdf", _pypdf)):
        try:
            text = fn(data, max_pages)
        except ImportError:
            continue
        except Exception as e:  # noqa: BLE001 - 壊れたPDFは次のエンジンへ
            log.warning("%s failed: %s", name, e)
            continue
        if is_readable(text):
            return text
        fallback = fallback or text
    return fallback
