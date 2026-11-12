#!/usr/bin/env python3
"""One-shot backfill: import OpenDock's star-history into snapshot files.

OpenDock (github.com/qunqin24/opendock) accumulates daily star counts for
~1.4k OpenCode packages since 2026-09. Its history.json shape is
{npm_id: {"YYYY-MM-DD": stars}}. For every day it covers, emit a synthetic
snapshot data/snapshots/<UTC-date>T00.json with rows in the positional
format — stars column filled, download columns None — so the whole
rank/history machinery gains ~2 months of depth with zero changes.

Days that already have a REAL snapshot file are skipped: real rows carry
richer columns (downloads/created/flags) and must win. Re-running is safe.

Row columns beyond stars are filled from the current data/repos detail
when available (created/type/deprecated) so boards behave sensibly;
packages absent from our catalog are imported anyway (they may re-enter
the catalog later) unless --catalog-only is passed.

Usage:
  python scripts/import_opendock.py [path-or-url-to-history.json]
                                     [--catalog-only] [--from YYYY-MM-DD]
"""
from __future__ import annotations

import json
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SNAP_DIR = DATA_DIR / "snapshots"
REPOS_DIR = DATA_DIR / "repos"

DEFAULT_SRC = ("https://raw.githubusercontent.com/qunqin24/opendock/"
               "main/data/history.json")


def log(msg: str) -> None:
    print(f"[import_opendock] {msg}", flush=True)


def load_source(src: str) -> dict:
    if src.startswith(("http://", "https://")):
        req = urllib.request.Request(
            src, headers={"User-Agent": "oplugins-radar/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    return json.loads(Path(src).read_text(encoding="utf-8"))


def current_meta() -> tuple[dict[str, tuple], dict[str, str]]:
    """(full_name -> (created, type, deprecated), npm_id -> full_name)."""
    out: dict[str, tuple] = {}
    by_npm: dict[str, str] = {}
    for f in REPOS_DIR.glob("*.json"):
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        det = j.get("detail") or {}
        fn = f.stem.replace("__", "/", 1)
        out[fn] = (
            (j.get("pushed_at") or "")[:10] or None,
            det.get("type") or "plugin",
            bool(det.get("deprecated")))
        pid = det.get("npm_id")
        if isinstance(pid, str) and pid.strip():
            by_npm[pid.strip()] = fn
    return out, by_npm


def main() -> int:
    src = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") \
        else DEFAULT_SRC
    catalog_only = "--catalog-only" in sys.argv
    cutoff = None
    if "--from" in sys.argv:
        cutoff = sys.argv[sys.argv.index("--from") + 1]

    hist = load_source(src)
    log(f"history.json: {len(hist)} packages")

    meta, by_npm = current_meta()
    existing_days = {f.stem[:10] for f in SNAP_DIR.glob("*.json")}
    SNAP_DIR.mkdir(parents=True, exist_ok=True)

    # history key is an npm id; our full_name may differ (GitHub-sourced
    # entries key on repo slug) — resolve via detail.npm_id first, then
    # verbatim, then the npm/ synthetic-owner convention.
    catalog_names = set(meta)
    rows_by_day: dict[str, list] = defaultdict(list)
    skipped_pkgs = 0
    for pid, days in hist.items():
        if not isinstance(pid, str) or not isinstance(days, dict):
            continue
        full_name = (by_npm.get(pid)
                     or (pid if pid in catalog_names else None)
                     or f"npm/{pid}")
        if catalog_only and full_name not in catalog_names:
            skipped_pkgs += 1
            continue
        created, typ, dep = meta.get(full_name) or (None, "plugin", False)
        for day, stars in days.items():
            if not isinstance(day, str) or len(day) != 10:
                continue
            if cutoff and day < cutoff:
                continue
            if day in existing_days:
                continue  # real snapshot wins
            if not isinstance(stars, int) or stars < 0:
                continue
            rows_by_day[day].append(
                [full_name, stars, None, None, None, None, None,
                 created, typ, False, dep, None, None, None, None, None])

    written = 0
    for day, rows in sorted(rows_by_day.items()):
        if not rows:
            continue
        snap = {"date": f"{day}T00",
                "run_at": f"{day}T00:00:00Z",
                "imported_from": "opendock history.json",
                "repos": sorted(rows), "errors": []}
        (SNAP_DIR / f"{day}T00.json").write_text(
            json.dumps(snap, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")
        written += 1
    log(f"backfilled {written} days "
        f"({min(rows_by_day) if rows_by_day else '-'} → "
        f"{max(rows_by_day) if rows_by_day else '-'}), "
        f"skipped_pkgs={skipped_pkgs}, existing_days_preserved={len(existing_days)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
