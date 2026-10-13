"""TDnet 適時開示情報閲覧サービスからの一覧取得。

一覧ページ: https://www.release.tdnet.info/inbs/I_list_{page:03d}_{YYYYMMDD}.html
TDnet上で閲覧できるのは直近約1か月分のみ。
"""

from __future__ import annotations

import datetime as dt
import logging
import re
import time
from dataclasses import asdict, dataclass

import requests
from bs4 import BeautifulSoup

from .textutil import nfkc

log = logging.getLogger(__name__)

BASE_URL = "https://www.release.tdnet.info/inbs/"
USER_AGENT = "kaiji-bot/0.1 (+https://github.com/mochizn/github)"


@dataclass
class Disclosure:
    id: str  # PDFファイル名から拡張子を除いたもの(TDnet内で一意)
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    code: str  # 証券コード(4桁 or 英字含む4桁)
    name: str
    title: str
    pdf_url: str
    xbrl_url: str | None
    exchange: str
    history: str

    @property
    def disclosed_at(self) -> str:
        return f"{self.date} {self.time}"

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_code(raw: str) -> str:
    """TDnetの5桁コード(末尾0)を4桁へ。例: 72030 -> 7203, 130A0 -> 130A"""
    c = nfkc(raw).strip().upper()
    if len(c) == 5 and c.endswith("0"):
        return c[:4]
    return c


def parse_list_html(html: str, date: dt.date) -> tuple[list[Disclosure], int]:
    """一覧HTMLをパースし、(開示一覧, 全件数)を返す。"""
    soup = BeautifulSoup(html, "lxml")
    items: list[Disclosure] = []
    for tr in soup.select("#main-list-table tr"):
        a = tr.select_one(".kjTitle a")
        if a is None or not a.get("href"):
            continue

        def cell(cls: str) -> str:
            td = tr.select_one(cls)
            return td.get_text(" ", strip=True) if td else ""

        href = a["href"].strip()
        xa = tr.select_one(".kjXbrl a")
        items.append(
            Disclosure(
                id=re.sub(r"\.pdf$", "", href.rsplit("/", 1)[-1]),
                date=date.isoformat(),
                time=cell(".kjTime"),
                code=normalize_code(cell(".kjCode")),
                name=re.sub(r"\s+", " ", nfkc(cell(".kjName"))).strip(),
                title=re.sub(r"\s+", " ", a.get_text(" ", strip=True)).strip(),
                pdf_url=BASE_URL + href,
                xbrl_url=(BASE_URL + xa["href"].strip()) if xa and xa.get("href") else None,
                exchange=cell(".kjPlace"),
                history=cell(".kjHistroy").replace("　", "").strip(),
            )
        )
    m = re.search(r"全\s*(\d+)\s*件", soup.get_text())
    total = int(m.group(1)) if m else len(items)
    return items, total


class TdnetClient:
    def __init__(self, session: requests.Session | None = None, interval: float = 1.0, timeout: float = 30.0):
        self.s = session or requests.Session()
        self.s.headers.setdefault("User-Agent", USER_AGENT)
        self.interval = interval
        self.timeout = timeout
        self._last = 0.0

    def _get(self, url: str) -> requests.Response | None:
        wait = self.interval - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        for attempt in range(4):
            try:
                r = self.s.get(url, timeout=self.timeout)
                self._last = time.monotonic()
                if r.status_code == 404:
                    return None
                r.raise_for_status()
                return r
            except requests.RequestException as e:
                if attempt == 3:
                    raise
                backoff = 2 ** (attempt + 1)
                log.warning("GET %s failed (%s); retry in %ss", url, e, backoff)
                time.sleep(backoff)
        return None

    def list_day(self, date: dt.date) -> list[Disclosure]:
        """指定日の開示一覧(全ページ)を取得。存在しない日は空リスト。"""
        out: list[Disclosure] = []
        page = 1
        while True:
            url = f"{BASE_URL}I_list_{page:03d}_{date:%Y%m%d}.html"
            r = self._get(url)
            if r is None:
                break
            r.encoding = "utf-8"
            items, total = parse_list_html(r.text, date)
            out.extend(items)
            if not items or len(out) >= total:
                break
            page += 1
        # 同一IDの重複を除去(ページ境界での重複対策)
        seen: set[str] = set()
        uniq = []
        for d in out:
            if d.id not in seen:
                seen.add(d.id)
                uniq.append(d)
        return uniq

    def download(self, url: str) -> bytes | None:
        r = self._get(url)
        return r.content if r is not None else None
