#!/usr/bin/env python3
"""Fetch GitHub repo stats (watchers / open PRs / open issues / releases /
forks) for every catalog entry, via one GraphQL connection.

The upstream catalog publishes no GitHub-side counters beyond stars — these
fields power the "repo stats" cards on the detail overview tab.

Data:  data/ghmeta.json  { "<owner>/<repo>": {watchers, open_prs,
                              open_issues, releases, forks, checked} }
Runs:  daily-update workflow, after sync_readmes.py
Env:   GH_TOKEN / GITHUB_TOKEN   required (Actions' GITHUB_TOKEN works)
       OCM_GH_BATCH              repos per GraphQL query (default 45)
       OCM_GH_REFRESH_DAYS       re-check cadence (default 7)
       OCM_GH_LIMIT              smoke-test cap on pending repos
       OCM_GH_FORCE              re-fetch everything
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REPOS_DIR = DATA_DIR / "repos"
OUT_PATH = DATA_DIR / "ghmeta.json"

GQL = "https://api.github.com/graphql"
GH_RE = re.compile(r"^https?://(?:www\.)?github\.com/([\w.-]+)/([\w.-]+?)(?:\.git|/)?$")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
BATCH = int(os.environ.get("OCM_GH_BATCH", "45"))
REFRESH_DAYS = int(os.environ.get("OCM_GH_REFRESH_DAYS", "7"))
LIMIT = int(os.environ.get("OCM_GH_LIMIT", "0"))
FORCE = os.environ.get("OCM_GH_FORCE") == "1"
WORKERS = int(os.environ.get("OCM_GH_WORKERS", "4"))

FIELDS = """watchers{totalCount} forkCount
issues(states:OPEN){totalCount} pullRequests(states:OPEN){totalCount}
releases{totalCount}"""


def log(msg: str) -> None:
    print(f"[ghmeta {datetime.now(UTC):%H:%M:%S}] {msg}", flush=True)


def gh_slug(d: dict) -> tuple[str, str] | None:
    m = GH_RE.match((d.get("url") or "").strip())
    if m:
        return m.group(1), m.group(2)
    return None


def targets() -> list[tuple[str, str, str]]:
    """(full_name, owner, repo) needing a (re)fetch."""
    have = {}
    if OUT_PATH.exists() and not FORCE:
        try:
            have = json.loads(OUT_PATH.read_text(encoding="utf-8"))
        except Exception:
            have = {}
    cut = datetime.now(UTC) - timedelta(days=REFRESH_DAYS)
    out = []
    for f in sorted(REPOS_DIR.glob("*.json")):
        fn = f.stem.replace("__", "/", 1)
        old = have.get(fn) or {}
        try:
            if old.get("checked") and datetime.fromisoformat(old["checked"]) > cut:
                continue
        except ValueError:
            pass
        try:
            det = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = gh_slug(det) or gh_slug(det.get("detail") or {})
        if slug:
            out.append((fn, slug[0], slug[1]))
    return out


def gql(query: str) -> dict:
    req = urllib.request.Request(
        GQL, data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"bearer {TOKEN}",
                 "User-Agent": "opencode-plugins-ghmeta",
                 "Content-Type": "application/json"})
    for attempt in (1, 2, 3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                body = json.loads(r.read())
            if body.get("errors") and "data" not in body:
                raise RuntimeError(str(body["errors"])[:200])
            return body.get("data") or {}
        except Exception as e:
            if attempt == 3:
                raise
            time.sleep(2 * attempt)
    return {}


def fetch_batch(jobs: list[tuple[str, str, str]]) -> dict[str, dict]:
    parts = [f'r{i}: repository(owner:"{o}",name:"{n}"){{{FIELDS}}}'
             for i, (_, o, n) in enumerate(jobs)]
    data = gql("query{" + "".join(parts) + "}")
    out = {}
    now = datetime.now(UTC).isoformat(timespec="seconds")
    for i, (fn, _, _) in enumerate(jobs):
        node = data.get(f"r{i}")
        if not node:
            continue
        out[fn] = {
            "watchers": (node.get("watchers") or {}).get("totalCount"),
            "forks": node.get("forkCount"),
            "open_issues": (node.get("issues") or {}).get("totalCount"),
            "open_prs": (node.get("pullRequests") or {}).get("totalCount"),
            "releases": (node.get("releases") or {}).get("totalCount"),
            "checked": now,
        }
    return out


def main() -> int:
    if not TOKEN:
        log("GH_TOKEN/GITHUB_TOKEN not set — skipping github meta fetch")
        return 0
    meta = {}
    if OUT_PATH.exists() and not FORCE:
        try:
            meta = json.loads(OUT_PATH.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
    todo = targets()
    log(f"pending={len(todo)} have={len(meta)} batch={BATCH} workers={WORKERS}")
    if LIMIT:
        todo = todo[:LIMIT]
    batches = [todo[i:i + BATCH] for i in range(0, len(todo), BATCH)]
    got = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for res in ex.map(fetch_batch, batches):
            got += len(res)
            meta.update(res)
    OUT_PATH.write_text(json.dumps(meta, ensure_ascii=False,
                                   separators=(",", ":")), encoding="utf-8")
    log(f"done got={got} total={len(meta)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
