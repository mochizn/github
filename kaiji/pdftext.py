"""PDF -> テキスト抽出。"""

from __future__ import annotations

import io
import logging
import re

log = logging.getLogger(__name__)


def is_readable(text: str) -> bool:
    """フォントにUnicode対応表が無いPDFは (cid:123) の羅列になる。画像のみのPDFは空になる。"""
    if len(text.strip()) < 20:
        return False
    cids = len(re.findall(r"\(cid:\d+\)", text))
    return cids * 8 < len(text) * 0.3


def pdf_to_text(data: bytes, max_pages: int = 30) -> str:
    """pdfplumberで抽出し、失敗時はpypdfにフォールバックする。"""
    try:
        import pdfplumber

        with pdfplumber.open(io.BytesIO(data)) as pdf:
            pages = []
            for page in pdf.pages[:max_pages]:
                pages.append(page.extract_text() or "")
            text = "\n".join(pages)
            if text.strip():
                return text
    except Exception as e:  # noqa: BLE001 - 壊れたPDFはフォールバック
        log.warning("pdfplumber failed: %s", e)
    try:
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(data))
        return "\n".join((p.extract_text() or "") for p in reader.pages[:max_pages])
    except Exception as e:  # noqa: BLE001
        log.warning("pypdf failed: %s", e)
        return ""
