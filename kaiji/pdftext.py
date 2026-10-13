"""PDF -> テキスト抽出。"""

from __future__ import annotations

import io
import logging

log = logging.getLogger(__name__)


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
