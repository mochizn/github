"""SQLite ストア + FTS5(trigram) 全文検索。"""

from __future__ import annotations

import datetime as dt
import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

from .textutil import nfkc

SCHEMA = """
CREATE TABLE IF NOT EXISTS disclosures (
    id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    time TEXT NOT NULL DEFAULT '',
    code TEXT NOT NULL DEFAULT '',
    name TEXT NOT NULL DEFAULT '',
    title TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT 'other',
    tags TEXT NOT NULL DEFAULT '',
    importance INTEGER NOT NULL DEFAULT 0,
    is_correction INTEGER NOT NULL DEFAULT 0,
    pdf_url TEXT,
    xbrl_url TEXT,
    exchange TEXT,
    history TEXT,
    status TEXT NOT NULL DEFAULT 'new',      -- new / done / meta / error
    attempts INTEGER NOT NULL DEFAULT 0,
    error TEXT,
    fetched_at TEXT,
    processed_at TEXT,
    summary TEXT NOT NULL DEFAULT '',
    lead TEXT NOT NULL DEFAULT '',
    outlook TEXT NOT NULL DEFAULT '',
    reason TEXT NOT NULL DEFAULT '',
    qualitative TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    kv_json TEXT,
    order_json TEXT,
    order_mentions_json TEXT,
    signals_json TEXT,
    metrics_json TEXT,
    direction TEXT NOT NULL DEFAULT '',
    amount_yen REAL,
    llm_json TEXT,
    llm_model TEXT,
    notified_at TEXT
);
CREATE INDEX IF NOT EXISTS ix_disc_date ON disclosures(date DESC, time DESC);
CREATE INDEX IF NOT EXISTS ix_disc_code ON disclosures(code, date DESC);
CREATE INDEX IF NOT EXISTS ix_disc_cat ON disclosures(category, date DESC);
CREATE INDEX IF NOT EXISTS ix_disc_status ON disclosures(status);

CREATE VIRTUAL TABLE IF NOT EXISTS disclosures_fts USING fts5(
    title, name, code, summary, lead, outlook, reason, qualitative, body,
    content='disclosures', content_rowid='rowid', tokenize='trigram'
);
CREATE TRIGGER IF NOT EXISTS disclosures_ai AFTER INSERT ON disclosures BEGIN
    INSERT INTO disclosures_fts(rowid, title, name, code, summary, lead, outlook, reason, qualitative, body)
    VALUES (new.rowid, new.title, new.name, new.code, new.summary, new.lead, new.outlook, new.reason, new.qualitative, new.body);
END;
CREATE TRIGGER IF NOT EXISTS disclosures_ad AFTER DELETE ON disclosures BEGIN
    INSERT INTO disclosures_fts(disclosures_fts, rowid, title, name, code, summary, lead, outlook, reason, qualitative, body)
    VALUES ('delete', old.rowid, old.title, old.name, old.code, old.summary, old.lead, old.outlook, old.reason, old.qualitative, old.body);
END;
CREATE TRIGGER IF NOT EXISTS disclosures_au AFTER UPDATE OF title, name, code, summary, lead, outlook, reason, qualitative, body ON disclosures BEGIN
    INSERT INTO disclosures_fts(disclosures_fts, rowid, title, name, code, summary, lead, outlook, reason, qualitative, body)
    VALUES ('delete', old.rowid, old.title, old.name, old.code, old.summary, old.lead, old.outlook, old.reason, old.qualitative, old.body);
    INSERT INTO disclosures_fts(rowid, title, name, code, summary, lead, outlook, reason, qualitative, body)
    VALUES (new.rowid, new.title, new.name, new.code, new.summary, new.lead, new.outlook, new.reason, new.qualitative, new.body);
END;

CREATE TABLE IF NOT EXISTS watchlist (
    code TEXT PRIMARY KEY,
    note TEXT NOT NULL DEFAULT '',
    added_at TEXT
);
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
);
"""

JSON_FIELDS = ("kv_json", "order_json", "order_mentions_json", "signals_json", "metrics_json", "llm_json")
TEXT_FIELDS = ("summary", "lead", "outlook", "reason", "qualitative", "body")
# アーカイブ(JSONL)に保存する列
ARCHIVE_FIELDS = (
    "id", "date", "time", "code", "name", "title", "category", "tags", "importance", "is_correction",
    "pdf_url", "xbrl_url", "exchange", "history", "status", "processed_at",
    "summary", "lead", "outlook", "reason", "qualitative", "body", "kv_json", "order_json",
    "order_mentions_json", "signals_json", "metrics_json", "direction", "amount_yen", "llm_json", "llm_model", "notified_at",
)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).isoformat(timespec="seconds")


class Store:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        if str(path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.executescript(SCHEMA)
        self._migrate()

    def _migrate(self) -> None:
        """古いDBに後から追加した列を足す。"""
        cols = {r[1] for r in self.conn.execute("PRAGMA table_info(disclosures)")}
        for col in ("metrics_json",):
            if col not in cols:
                self.conn.execute(f"ALTER TABLE disclosures ADD COLUMN {col} TEXT")
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # ------------------------------------------------------------------ write
    def upsert_meta(self, d: dict, category: str, tags: list[str], importance: int, is_correction: bool, deep: bool) -> bool:
        """一覧から得たメタ情報を登録。新規ならTrue。"""
        cur = self.conn.execute("SELECT status FROM disclosures WHERE id=?", (d["id"],)).fetchone()
        if cur is not None:
            self.conn.execute("UPDATE disclosures SET history=?, xbrl_url=COALESCE(?, xbrl_url) WHERE id=?",
                              (d.get("history", ""), d.get("xbrl_url"), d["id"]))
            return False
        self.conn.execute(
            """INSERT INTO disclosures (id, date, time, code, name, title, category, tags, importance, is_correction,
                   pdf_url, xbrl_url, exchange, history, status, fetched_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (d["id"], d["date"], d["time"], d["code"], d["name"], d["title"], category, ",".join(tags), importance,
             int(is_correction), d.get("pdf_url"), d.get("xbrl_url"), d.get("exchange", ""), d.get("history", ""),
             "new" if deep else "meta", now_iso()),
        )
        return True

    def update(self, id_: str, **fields: Any) -> None:
        if not fields:
            return
        for k in JSON_FIELDS:
            if k in fields and not isinstance(fields[k], (str, type(None))):
                fields[k] = json.dumps(fields[k], ensure_ascii=False)
        cols = ", ".join(f"{k}=?" for k in fields)
        self.conn.execute(f"UPDATE disclosures SET {cols} WHERE id=?", (*fields.values(), id_))

    def import_rows(self, rows: Iterable[dict]) -> int:
        """アーカイブ(JSONL)からの取り込み。既存IDは上書き。"""
        n = 0
        for r in rows:
            r = {k: r.get(k) for k in ARCHIVE_FIELDS if k in r}
            for k in JSON_FIELDS:
                if k in r and r[k] is not None and not isinstance(r[k], str):
                    r[k] = json.dumps(r[k], ensure_ascii=False)
            for k in TEXT_FIELDS:
                r[k] = r.get(k) or ""
            self.conn.execute("DELETE FROM disclosures WHERE id=?", (r["id"],))
            cols = ",".join(r)
            self.conn.execute(f"INSERT INTO disclosures ({cols}) VALUES ({','.join('?' * len(r))})", tuple(r.values()))
            n += 1
        self.commit()
        return n

    def commit(self) -> None:
        self.conn.commit()

    def get_meta(self, key: str, default: str | None = None) -> str | None:
        r = self.conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return r[0] if r else default

    def set_meta(self, key: str, value: str) -> None:
        self.conn.execute("INSERT INTO meta(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))

    # ------------------------------------------------------------------ watchlist
    def watch_add(self, code: str, note: str = "") -> None:
        self.conn.execute("INSERT OR REPLACE INTO watchlist(code, note, added_at) VALUES (?,?,?)", (code.upper(), note, now_iso()))
        self.commit()

    def watch_remove(self, code: str) -> None:
        self.conn.execute("DELETE FROM watchlist WHERE code=?", (code.upper(),))
        self.commit()

    def watchlist(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM watchlist ORDER BY code")]

    # ------------------------------------------------------------------ read
    def get(self, id_: str) -> dict | None:
        r = self.conn.execute("SELECT * FROM disclosures WHERE id=?", (id_,)).fetchone()
        return row_to_dict(r) if r else None

    def pending(self, limit: int = 200, max_attempts: int = 3) -> list[dict]:
        rows = self.conn.execute(
            """SELECT * FROM disclosures WHERE status IN ('new','error') AND attempts < ?
               ORDER BY importance DESC, date DESC, time DESC LIMIT ?""",
            (max_attempts, limit),
        )
        return [row_to_dict(r) for r in rows]

    def iter_all(self, where: str = "1=1", params: tuple = ()) -> Iterator[dict]:
        for r in self.conn.execute(f"SELECT * FROM disclosures WHERE {where} ORDER BY date, time, id", params):
            yield row_to_dict(r)

    def order_metrics(self, metric: str | None = None, min_yoy: float | None = None, since: str | None = None,
                      code: str | None = None, limit: int = 100) -> list[tuple[dict, dict]]:
        """決算短信等から抽出した受注高・受注残高を (開示, 指標) で返す。銘柄×開示ごとに先頭の指標のみ。"""
        where, params = ["metrics_json IS NOT NULL"], []
        if since:
            where.append("date >= ?")
            params.append(since)
        if code:
            where.append("code = ?")
            params.append(code.upper())
        out = []
        for r in self.iter_all(" AND ".join(where), tuple(params)):
            seen = set()
            for m in r.get("metrics") or []:
                if m["metric"] in seen or (metric and m["metric"] != metric):
                    continue
                seen.add(m["metric"])
                if min_yoy is not None and (m.get("yoy_pct") is None or m["yoy_pct"] < min_yoy):
                    continue
                out.append((r, m))
        out.sort(key=lambda x: (x[1].get("yoy_pct") if x[1].get("yoy_pct") is not None else -1e9), reverse=True)
        return out[:limit]

    def stats(self) -> dict:
        c = self.conn
        return {
            "total": c.execute("SELECT COUNT(*) FROM disclosures").fetchone()[0],
            "by_status": dict(c.execute("SELECT status, COUNT(*) FROM disclosures GROUP BY status").fetchall()),
            "by_category": dict(c.execute("SELECT category, COUNT(*) FROM disclosures GROUP BY category ORDER BY 2 DESC").fetchall()),
            "date_range": tuple(c.execute("SELECT MIN(date), MAX(date) FROM disclosures").fetchone()),
            "orders": c.execute("SELECT COUNT(*) FROM disclosures WHERE ','||tags||',' LIKE '%,order,%'").fetchone()[0],
        }

    def search(self, q: SearchQuery) -> list[dict]:
        sql, params = q.to_sql()
        rows = [row_to_dict(r) for r in self.conn.execute(sql, params)]
        for r in rows:
            r["snippet"] = make_snippet(r, q.terms)
        return rows


def row_to_dict(r: sqlite3.Row) -> dict:
    d = dict(r)
    for k in JSON_FIELDS:
        v = d.get(k)
        if isinstance(v, str) and v:
            try:
                d[k[:-5]] = json.loads(v)
            except json.JSONDecodeError:
                d[k[:-5]] = None
        else:
            d[k[:-5]] = None
    d["tag_list"] = [t for t in (d.get("tags") or "").split(",") if t]
    return d


# ---------------------------------------------------------------------- search

_TERM_RE = re.compile(r'"([^"]+)"|(\S+)')


def parse_terms(q: str) -> tuple[list[str], list[str]]:
    """検索語を (含む語, 除外語) に分解。-語 で除外、"..." でフレーズ。"""
    inc: list[str] = []
    exc: list[str] = []
    for m in _TERM_RE.finditer(nfkc(q or "").replace("　", " ")):
        t = m.group(1) or m.group(2)
        if not t:
            continue
        if m.group(2) and t.startswith("-") and len(t) > 1:
            exc.append(t[1:])
        elif t.upper() != "AND":
            inc.append(t)
    return inc, exc


_LIKE_COLS = "(" + " || ' ' || ".join(f"d.{c}" for c in ("title", "name", "summary", "lead", "outlook", "reason", "qualitative", "body")) + ")"


@dataclass
class SearchQuery:
    text: str = ""
    code: str | None = None
    category: str | None = None
    date_from: str | None = None
    date_to: str | None = None
    min_amount: float | None = None
    min_importance: int | None = None
    direction: str | None = None
    title_only: bool = False
    watch_only: bool = False
    sort: str = "date"  # date / amount / relevance
    limit: int = 50
    offset: int = 0

    @property
    def terms(self) -> list[str]:
        return parse_terms(self.text)[0]

    def to_sql(self) -> tuple[str, list]:
        inc, exc = parse_terms(self.text)
        where: list[str] = []
        params: list = []
        fts_terms = [t for t in inc if len(t) >= 3]
        short_terms = [t for t in inc if len(t) < 3]
        join = ""
        if fts_terms:
            col = "{title name} : " if self.title_only else ""
            match = " AND ".join(col + '"' + t.replace('"', '""') + '"' for t in fts_terms)
            join = "JOIN disclosures_fts f ON f.rowid = d.rowid"
            where.append("disclosures_fts MATCH ?")
            params.append(match)
        target = "(d.title || ' ' || d.name)" if self.title_only else _LIKE_COLS
        for t in short_terms:
            where.append(f"instr({target}, ?) > 0")
            params.append(t)
        for t in exc:
            where.append(f"instr({target}, ?) = 0")
            params.append(t)
        if self.code:
            codes = [c.strip().upper() for c in re.split(r"[,\s]+", nfkc(self.code)) if c.strip()]
            where.append(f"d.code IN ({','.join('?' * len(codes))})")
            params.extend(codes)
        if self.watch_only:
            where.append("d.code IN (SELECT code FROM watchlist)")
        if self.category:
            cats = [c for c in self.category.split(",") if c]
            where.append("(" + " OR ".join("(',' || d.tags || ',') LIKE ?" for _ in cats) + ")")
            params.extend(f"%,{c},%" for c in cats)
        if self.date_from:
            where.append("d.date >= ?")
            params.append(self.date_from)
        if self.date_to:
            where.append("d.date <= ?")
            params.append(self.date_to)
        if self.min_amount is not None:
            where.append("d.amount_yen >= ?")
            params.append(self.min_amount)
        if self.min_importance is not None:
            where.append("d.importance >= ?")
            params.append(self.min_importance)
        if self.direction:
            where.append("d.direction = ?")
            params.append(self.direction)
        order = "d.date DESC, d.time DESC, d.id DESC"
        if self.sort == "amount":
            order = "d.amount_yen IS NULL, d.amount_yen DESC, d.date DESC"
        elif self.sort == "relevance" and fts_terms:
            order = "f.rank, d.date DESC"
        sql = (
            f"SELECT d.* FROM disclosures d {join} "
            f"WHERE {' AND '.join(where) if where else '1=1'} ORDER BY {order} LIMIT ? OFFSET ?"
        )
        params.extend([self.limit, self.offset])
        return sql, params


def make_snippet(row: dict, terms: list[str], width: int = 70) -> str:
    """最初にヒットした箇所の前後を切り出す。"""
    fields = ("summary", "lead", "outlook", "reason", "qualitative", "body")
    for t in terms:
        for f in fields:
            text = row.get(f) or ""
            i = text.find(t)
            if i >= 0:
                s = max(0, i - width)
                e = min(len(text), i + len(t) + width)
                return ("…" if s else "") + text[s:e].replace("\n", " ") + ("…" if e < len(text) else "")
    return (row.get("summary") or row.get("lead") or "")[: width * 2]
