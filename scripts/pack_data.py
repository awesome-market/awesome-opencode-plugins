#!/usr/bin/env python3
"""Pack site/data/** into a single sqlite blob store: site-data.db.

Why: Cloudflare Pages caps deployments at 20k files and the data tree
(per-repo JSON, README markdown, day/tag feeds) is ~16k files on its own.
CI uploads this file via POST /data-upload on api-site; the frontend then
hydrates from https://api.oplugin.com/data/<path> instead of static
/data/*.json files. gh-pages keeps the full tree as backup.

Schema:
  data(path TEXT PRIMARY KEY, blob BLOB) — tree files as blobs
  meta(k, v)                             — provenance
  search_items / search_fts              — REAL tables: the search corpus
                                           as rows, queried directly by
                                           the API via ATTACH (replaces
                                           the sync_search.py cron hop)

Paths are the tree-relative posix names
(repos/owner__name.json, readme/owner__name.md, days/2026-11-12.json, ...).
"""
import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "site" / "data"
OUT = ROOT / "site-data.db"

# mirrors zhuikan-api's search schema — kept identical by convention:
# the API CREATEs the same tables inside its ATTACH of this file
SEARCH_SCHEMA = """
CREATE TABLE search_items (
    site         TEXT NOT NULL,
    item_id      TEXT NOT NULL,
    name         TEXT,
    owner        TEXT,
    description  TEXT,
    lang         TEXT,
    stars        INTEGER DEFAULT 0,
    forks        INTEGER NOT NULL DEFAULT 0,
    watchers     INTEGER NOT NULL DEFAULT 0,
    news_titles  TEXT,
    synced_at    INTEGER,
    PRIMARY KEY (site, item_id)
);
CREATE VIRTUAL TABLE search_fts USING fts5(
    name, owner, description, news_titles,
    content='search_items', content_rowid='rowid',
    tokenize='unicode61'
);
CREATE TRIGGER si_ai AFTER INSERT ON search_items BEGIN
    INSERT INTO search_fts(rowid, name, owner, description, news_titles)
    VALUES (new.rowid, new.name, new.owner, new.description, new.news_titles);
END;
CREATE TRIGGER si_ad AFTER DELETE ON search_items BEGIN
    INSERT INTO search_fts(search_fts, rowid, name, owner, description, news_titles)
    VALUES ('delete', old.rowid, old.name, old.owner, old.description, old.news_titles);
END;
CREATE TRIGGER si_au AFTER UPDATE ON search_items BEGIN
    INSERT INTO search_fts(search_fts, rowid, name, owner, description, news_titles)
    VALUES ('delete', old.rowid, old.name, old.owner, old.description, old.news_titles);
    INSERT INTO search_fts(rowid, name, owner, description, news_titles)
    VALUES (new.rowid, new.name, new.owner, new.description, new.news_titles);
END;
"""


def _pack_search(con) -> int:
    """search-index.json + search-news.json → real search_items rows
    (the INSERT triggers fill search_fts as we go)."""
    idx_p, news_p = DATA_DIR / "search-index.json", DATA_DIR / "search-news.json"
    if not idx_p.is_file():
        return 0
    idx = json.loads(idx_p.read_text())
    news = {}
    if news_p.is_file():
        news = {e["n"]: e.get("nw") or [] for e in json.loads(news_p.read_text())}
    t = int(time.time())
    n = 0
    for e in idx:
        name = e.get("n") or ""
        if "/" not in name:
            continue
        owner, _, repo = name.partition("/")
        con.execute(
            "INSERT INTO search_items(site,item_id,name,owner,description,"
            " lang,stars,forks,watchers,news_titles,synced_at)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            ("oplugins", name, repo, owner, e.get("d") or "",
             e.get("l") or "", int(e.get("s") or 0),
             int(e.get("f") or 0), int(e.get("w") or 0),
             "\n".join(news.get(name, [])), t))
        n += 1
    return n


def main() -> int:
    if not DATA_DIR.is_dir():
        print(f"[pack_data] {DATA_DIR} missing — run rank.py first",
              file=sys.stderr)
        return 1
    rows = [(f.relative_to(DATA_DIR).as_posix(), f.read_bytes())
            for f in sorted(DATA_DIR.rglob("*")) if f.is_file()]
    if not rows:
        print("[pack_data] no files under site/data — aborting",
              file=sys.stderr)
        return 1

    tmp = OUT.with_suffix(".db.tmp")
    if tmp.exists():
        tmp.unlink()
    con = sqlite3.connect(tmp)
    con.execute("PRAGMA journal_mode=DELETE")   # never WAL — upload swaps
                                              # only the .db file, no -wal
    con.execute("CREATE TABLE data(path TEXT PRIMARY KEY, blob BLOB NOT NULL)")
    con.execute("CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT NOT NULL)")
    con.executemany("INSERT INTO data VALUES(?,?)", rows)
    con.executemany("INSERT INTO meta VALUES(?,?)", [
        ("built_at", datetime.now(timezone.utc).isoformat(timespec="seconds")),
        ("files", str(len(rows))),
    ])
    con.executescript(SEARCH_SCHEMA)
    n_search = _pack_search(con)
    con.commit()
    con.close()
    os.replace(tmp, OUT)
    mb = OUT.stat().st_size / 1e6
    print(f"[pack_data] {len(rows)} files + {n_search} search rows"
          f" → {OUT.name} ({mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
