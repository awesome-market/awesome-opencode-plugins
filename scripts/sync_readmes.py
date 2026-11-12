#!/usr/bin/env python3
"""Fetch plugin READMEs from GitHub into data/readmes/<fn>.md.

The upstream catalog carries no README text, so this job maintains our
own archive: for every tracked entity whose source url is a GitHub repo
it tries the usual README filenames on the repo's default branch via
github.com/<owner>/<repo>/raw/HEAD/<file> (HEAD resolves automatically).

Runs inside the daily CI before rank.py; files are committed to git —
the repo is the archive. Fresh files are skipped (refresh every
OCM_README_REFRESH_DAYS), failures are tombstoned in _fails.json so a
repo without a README is not re-probed on every run.

Env:
  OCM_README_LIMIT         max fetches per run (default 3000)
  OCM_README_REFRESH_DAYS  re-fetch files older than N days (default 30)
  OCM_README_WORKERS       parallel fetches (default 8)
  OCM_README_FORCE         set to ignore freshness and fail-tombstones
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOS_DIR = ROOT / "data" / "repos"
OUT_DIR = ROOT / "data" / "readmes"
FAILS_PATH = OUT_DIR / "_fails.json"

LIMIT = int(os.environ.get("OCM_README_LIMIT", "3000"))
REFRESH_DAYS = int(os.environ.get("OCM_README_REFRESH_DAYS", "30"))
WORKERS = int(os.environ.get("OCM_README_WORKERS", "8"))
FORCE = bool(os.environ.get("OCM_README_FORCE"))
MAX_BYTES = 250 * 1024
UA = {"User-Agent": "opencode-plugins-sync/1.0"}
CANDIDATES = ("README.md", "readme.md", "README.MD", "Readme.md",
              "README", "README.mdx")
GH_RE = re.compile(r"https?://github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?/?$")
UTC = timezone.utc


def log(msg: str) -> None:
    print(f"[readme {datetime.now(UTC):%H:%M:%S}] {msg}", flush=True)


def gh_slug(detail: dict) -> tuple[str, str] | None:
    url = detail.get("url") or ""
    m = GH_RE.match(url.strip())
    return (m.group(1), m.group(2)) if m else None


def targets() -> list[tuple[str, str, str]]:
    """(full_name, owner, repo) needing a fetch."""
    fails = {}
    if FAILS_PATH.exists() and not FORCE:
        try:
            fails = json.loads(FAILS_PATH.read_text(encoding="utf-8"))
        except Exception:
            fails = {}
    fail_cut = datetime.now(UTC) - timedelta(days=7)
    fresh_cut = datetime.now(UTC) - timedelta(days=REFRESH_DAYS)
    out = []
    for f in sorted(REPOS_DIR.glob("*.json")):
        fn = f.stem.replace("__", "/", 1)
        if fn in fails:
            try:
                if datetime.fromisoformat(fails[fn]) > fail_cut:
                    continue
            except ValueError:
                pass
        have = OUT_DIR / f"{f.stem}.md"
        if have.exists() and not FORCE:
            try:
                if datetime.fromtimestamp(have.stat().st_mtime, UTC) > fresh_cut:
                    continue
            except OSError:
                pass
        try:
            det = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = gh_slug(det) or gh_slug(det.get("detail") or {})
        if slug:
            out.append((fn, slug[0], slug[1]))
    return out


def fetch_one(job: tuple[str, str, str]) -> tuple[str, str | None]:
    fn, owner, repo = job
    for cand in CANDIDATES:
        url = (f"https://github.com/{urllib.parse.quote(owner)}/"
               f"{urllib.parse.quote(repo)}/raw/HEAD/{cand}")
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status != 200:
                    continue
                raw = r.read(MAX_BYTES + 1)
        except Exception:
            continue
        if len(raw) > MAX_BYTES or b"404: Not Found" in raw[:200]:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if "<!DOCTYPE" in text[:200] or "<html" in text[:200]:
            continue
        if len(text.strip()) < 20:
            continue
        return fn, text
    return fn, None


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    todo = targets()
    log(f"pending={len(todo)} limit={LIMIT} workers={WORKERS}")
    todo = todo[:LIMIT]
    if not todo:
        return 0

    fails: dict[str, str] = {}
    if FAILS_PATH.exists():
        try:
            fails = json.loads(FAILS_PATH.read_text(encoding="utf-8"))
        except Exception:
            fails = {}

    got = missed = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for fn, text in ex.map(fetch_one, todo):
            path = OUT_DIR / f"{fn.replace('/', '__', 1)}.md"
            if text:
                path.write_text(text, encoding="utf-8")
                fails.pop(fn, None)
                got += 1
            else:
                fails[fn] = datetime.now(UTC).isoformat()
                missed += 1
            if (got + missed) % 250 == 0:
                log(f"{got + missed}/{len(todo)} got={got} miss={missed}")

    FAILS_PATH.write_text(json.dumps(fails, indent=0, sort_keys=True),
                          encoding="utf-8")
    log(f"done got={got} miss={missed} tombstoned={len(fails)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
