#!/usr/bin/env python3
"""Collect per-day npm download counts for every cataloged package.

The upstream market index only ships rolling windows (npmDownloads30d), so
long-term daily history must be accumulated here: one bulk GET per batch on
the public npm stats API, merged into append-only per-package files:

  data/dlhist/<owner>__<name>.json  {"days": {"YYYY-MM-DD": n, ...}}

Behavior:
  - window: last OCM_DL_WINDOW days (default 7) — covers npm's late
    day-finalization; files already holding data merge idempotently.
  - backfill: when a package has no history yet, fetch OCM_DL_BACKFILL
    days instead (default 180) so charts get a head start.
  - package id comes from data/repos/*.json detail.npm_id; entries without
    a real npm package id are skipped (mirrors sync_catalog semantics).
  - 'today' is excluded — npm returns partial zeros for the open day.

Env:
  OCM_DL_WINDOW    incremental window days (default 7)
  OCM_DL_BACKFILL  first-seen backfill days (default 180, cap 540)
  OCM_DL_BATCH     packages per bulk request (default 40)
  OCM_DL_LIMIT     if set, only process the first N packages (smoke runs)
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPOS_DIR = DATA_DIR / "repos"
DLHIST_DIR = DATA_DIR / "dlhist"
WATCHLIST_PATH = DATA_DIR / "watchlist.json"

API = "https://api.npmjs.org/downloads/range"
WINDOW = int(os.environ.get("OCM_DL_WINDOW", "7"))
BACKFILL = min(int(os.environ.get("OCM_DL_BACKFILL", "180")), 540)
BATCH = max(5, min(int(os.environ.get("OCM_DL_BATCH", "40")), 64))
LIMIT = int(os.environ.get("OCM_DL_LIMIT", "0"))
MAX_URL = 1800
UTC = timezone.utc


def log(msg: str) -> None:
    print(f"[sync_downloads] {msg}", flush=True)


def load_hist(fn: str) -> dict:
    p = DLHIST_DIR / f"{fn}.json"
    if not p.exists():
        return {}
    try:
        j = json.loads(p.read_text(encoding="utf-8"))
        days = j.get("days")
        return days if isinstance(days, dict) else {}
    except Exception:
        return {}


def save_hist(fn: str, days: dict) -> None:
    p = DLHIST_DIR / f"{fn}.json"
    p.write_text(json.dumps({"days": dict(sorted(days.items()))},
                            ensure_ascii=False, separators=(",", ":")),
                 encoding="utf-8")


def pkg_ids() -> dict[str, str]:
    """full_name → npm package id (from repo detail json)."""
    out: dict[str, str] = {}
    for f in REPOS_DIR.glob("*.json"):
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        pid = (j.get("detail") or {}).get("npm_id")
        if not isinstance(pid, str) or not pid.strip():
            continue
        fn = f.stem.replace("__", "/", 1)
        out[fn] = pid.strip()
    return out


def batches_pairs(pairs: list[tuple[str, str]]) -> list[list[tuple[str, str]]]:
    """Group (full_name, npm_id) pairs by encoded size — path stays < MAX_URL."""
    out, cur, size = [], [], 0
    for p in pairs:
        need = len(urllib.parse.quote(p[1], safe="")) + 1
        if cur and (len(cur) >= BATCH or size + need > MAX_URL):
            out.append(cur)
            cur, size = [], 0
        cur.append(p)
        size += need
    if cur:
        out.append(cur)
    return out


def fetch_range(group: list[str], start: str, end: str) -> dict[str, list]:
    """{package: [{day, downloads}]} — partial results tolerated."""
    enc = ",".join(urllib.parse.quote(p, safe="") for p in group)
    url = f"{API}/{start}:{end}/{enc}"
    req = urllib.request.Request(url, headers={"User-Agent": "oplugins-radar/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        j = json.load(r)
    res = {}
    if isinstance(j, dict) and "downloads" in j and isinstance(j["downloads"], list):
        # single-package reply shape
        res[j.get("package") or group[0]] = j["downloads"]
    elif isinstance(j, dict):
        for k, v in j.items():
            if isinstance(v, dict) and isinstance(v.get("downloads"), list):
                res[k] = v["downloads"]
    return res


def main() -> int:
    ids_map = pkg_ids()
    names = sorted(ids_map)
    if LIMIT:
        names = names[:LIMIT]
    DLHIST_DIR.mkdir(parents=True, exist_ok=True)

    yesterday = (datetime.now(UTC) - timedelta(days=1)).date()
    merged = fetched = skipped = failed = 0
    t0 = time.time()

    # one group covers packages sharing the same span need; simplest is to
    # fetch the union window and let each file keep what it needs — but a
    # brand-new package would re-fetch 180d every run. Split by need:
    need_backfill, need_incr = [], []
    for fn in names:
        (need_incr if load_hist(fn.replace("/", "__")) else need_backfill).append(fn)
    log(f"pkgs={len(names)} backfill={len(need_backfill)} incr={len(need_incr)}")

    def span(days: int) -> tuple[str, str]:
        s = (yesterday - timedelta(days=days - 1)).isoformat()
        return s, yesterday.isoformat()

    def run(names_: list[str], days: int) -> None:
        nonlocal merged, fetched, skipped, failed
        s, e = span(days)
        pairs = [(n, ids_map[n]) for n in names_]
        # npm stats API rejects scoped (@x/y) packages in bulk lookups —
        # batch bare ids, fetch scoped ids one per request.
        bulk = [p for p in pairs if not p[1].startswith("@")]
        solo = [p for p in pairs if p[1].startswith("@")]
        groups = batches_pairs(bulk) + [[p] for p in solo]
        for group in groups:
            try:
                data = fetch_range([pid for _, pid in group], s, e)
            except (urllib.error.URLError, TimeoutError, ValueError) as ex:
                failed += len(group)
                log(f"[warn] batch fetch failed ({len(group)}): {ex}")
                continue
            fetched += len(group)
            for fn, pid in group:
                rows = data.get(pid)
                if not rows:
                    skipped += 1
                    continue
                hist = load_hist(fn.replace("/", "__"))
                for row in rows:
                    day, n = row.get("day"), row.get("downloads")
                    if isinstance(day, str) and isinstance(n, int) and n >= 0:
                        hist[day] = n
                save_hist(fn.replace("/", "__"), hist)
                merged += 1
            time.sleep(0.1 if len(group) == 1 else 0.3)

    run(need_backfill, BACKFILL)
    run(need_incr, WINDOW)
    log(f"done fetched={fetched} merged={merged} skipped={skipped} "
        f"failed={failed} in {time.time() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
