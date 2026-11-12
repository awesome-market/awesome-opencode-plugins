#!/usr/bin/env python3
"""Sync the upstream OpenCode-market catalog into this repo's data layout.

One HTTPS GET on the published catalog index (GitHub Pages mirror), then emit:

  data/snapshots/<UTC-hour>.json   positional metric rows (same shape as the
                                 radar pipeline; semantic remap below)
  data/repos/<owner>__<name>.json  per-entity detail (meta + detail blocks)
  data/watchlist.json              entity roster

Column semantics are remapped for this domain (positional format unchanged —
growth/boards/history machinery needs zero changes):

  I_STARS    = metrics.stars            → "stars" board
  I_FORKS    = metrics.npmDownloads30d  → "30 天下载" board
  I_WATCHERS = metrics.downloadsMonth   → "本月下载" board
  I_CREATED  = entry.createdAt
  I_LANG     = entry.type ('plugin' | 'skill')
  I_IS_ARCH  = entry.deprecated

The catalog is UNTRUSTED INPUT: only known keys are read, values are
type-coerced and string lengths capped (see _txt).

Env:
  OCM_INDEX_URL — catalog index URL (default: dev fork Pages mirror;
                  production points at awesome-market upstream)
  OCM_TOP_README — if set, also fetch npm registry readmes for the top-N
                   entities by downloads (bounded; off by default)
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SNAP_DIR = DATA_DIR / "snapshots"
REPOS_DIR = DATA_DIR / "repos"
WATCHLIST_PATH = DATA_DIR / "watchlist.json"

INDEX_URL = os.environ.get(
    "OCM_INDEX_URL",
    "https://terry2010.github.io/awesome-opencode-market/index.json",
)
UTC = timezone.utc
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
MAX_TXT = 4000


def log(msg: str) -> None:
    print(f"[sync_catalog] {msg}", flush=True)


def _txt(v, cap: int = MAX_TXT) -> str | None:
    """Untrusted-string coercer: type check, strip control chars, cap length."""
    if not isinstance(v, str):
        return None
    s = CTRL.sub("", v).strip()
    return s[:cap] if s else None


def _int(v) -> int | None:
    try:
        n = int(v)
    except (TypeError, ValueError):
        return None
    return n if n >= 0 else None


def _strs(v, cap: int = 40) -> list[str]:
    if not isinstance(v, list):
        return []
    out = []
    for x in v[:cap]:
        s = _txt(x, 200)
        if s:
            out.append(s)
    return out


def _split_name(slug: str) -> tuple[str, str]:
    """'@scope/name' | 'owner/name' → verbatim split; bare 'name' → ('npm', 'name').

    Bare npm packages live under the unscoped registry; 'npm/' prefix keeps
    owner/name ⇄ filename '__' round-trip exact and prevents scoped/unscoped
    collisions ('user/x' vs bare 'x')."""
    if "/" in slug:
        owner, name = slug.split("/", 1)
        return owner or "npm", name or slug
    return "npm", slug


def _entry_url(e: dict) -> str:
    src = e.get("source") or {}
    repo = _txt(src.get("repo"), 200)
    if repo and "/" in repo:
        return f"https://github.com/{repo}"
    pid = _txt(src.get("id"), 300) or _txt(e.get("name"), 300)
    return f"https://www.npmjs.com/package/{pid}" if pid else "https://www.npmjs.com"


def _version_url(e: dict, ver: str) -> str | None:
    """npm version page when the package id is known; github releases page
    for repo-sourced entries; else None."""
    src = e.get("source") or {}
    pid = _txt(src.get("id"), 300)
    if pid:
        return f"https://www.npmjs.com/package/{pid}/v/{urllib.parse.quote(ver, safe='')}"
    repo = _txt(src.get("repo"), 200)
    if repo and "/" in repo:
        return f"https://github.com/{repo}/releases"
    return None


def _avatar(e: dict, owner: str) -> str | None:
    """GitHub avatar only when a real repo is known — synthetic npm owners
    have no avatar endpoint, so leave None (frontend renders initials)."""
    src = e.get("source") or {}
    repo = _txt(src.get("repo"), 200)
    if repo and "/" in repo:
        return f"https://github.com/{repo.split('/', 1)[0]}.png"
    return None


def convert(e: dict) -> dict | None:
    """catalog entry → our detail json; None when unusable."""
    slug = _txt(e.get("slug") or e.get("name"), 300)
    if not slug:
        return None
    desc = e.get("description") or {}
    if not isinstance(desc, dict):
        desc = {}
    m = e.get("metrics") or {}
    ver = e.get("verification") or e.get("checks") or {}
    caps = e.get("capabilities") or {}
    if not isinstance(caps, dict):
        caps = {}
    maintainers = _strs(e.get("maintainers"))
    owner, name = _split_name(slug)
    if not name:
        return None
    latest = _txt(e.get("latestVersion"), 80)
    published = _txt(e.get("publishedAt"), 60)
    return {
        "description": _txt(desc.get("en"), 2000),
        "homepage": _txt(e.get("homepage") or (e.get("source") or {}).get("homepage"), 500),
        "topics": _strs(e.get("category")) + _strs(e.get("features")),
        "pushed_at": published or _txt(e.get("modifiedAt"), 60),
        "url": _entry_url(e),
        "updated_at": _txt(e.get("modifiedAt"), 60),
        "detail": {
            "description_zh": _txt(desc.get("zh"), 2000),
            "source_repo": _txt((e.get("source") or {}).get("repo"), 200),
            "npm_id": _txt((e.get("source") or {}).get("id"), 300),
            "avatar": _avatar(e, owner),
            "license": _txt(e.get("license"), 80),
            "latest_release": ({
                "name": latest, "tag": latest, "published_at": published,
                "body": None,
                # npm version page — GitHub-style /releases/tag/ doesn't exist
                "url": _version_url(e, latest),
            } if latest else None),
            "verification": {
                "status": _txt(ver.get("status"), 40) or "unverified",
                "level": _txt(ver.get("level"), 40),
                "run_url": _txt(ver.get("runUrl") or ver.get("run_url"), 500),
            },
            "approval": _txt(e.get("approval"), 20) or "legacy",
            "capabilities": {
                "findings": _strs(caps.get("findings")),
                "red_flags": _strs(caps.get("redFlags") or caps.get("red_flags")),
            },
            "type": _txt(e.get("type"), 20) or "plugin",
            "contains": _strs(e.get("contains")),
            "deprecated": bool(e.get("deprecated")),
            "deprecated_message": _txt(e.get("deprecatedMessage"), 500),
            "maintainers": maintainers,
            "first_seen_at": _txt(e.get("firstSeenAt"), 60),
        },
    }


def main() -> int:
    log(f"fetch {INDEX_URL}")
    req = urllib.request.Request(INDEX_URL, headers={"User-Agent": "oplugins-radar/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = json.load(r)
    entries = raw.get("plugins") or []
    removed = raw.get("removed") or []
    log(f"entries={len(entries)} removed={len(removed)} generatedAt={raw.get('generatedAt')}")

    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    REPOS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(UTC)
    stamp = now.strftime("%Y-%m-%dT%H")

    prev_wl = {}
    if WATCHLIST_PATH.exists():
        try:
            prev_wl = (json.loads(WATCHLIST_PATH.read_text()) or {}).get("repos") or {}
        except Exception:
            prev_wl = {}

    rows, wl, written, skipped = [], {}, 0, 0
    for e in entries:
        if not isinstance(e, dict):
            continue
        conv = convert(e)
        if conv is None:
            skipped += 1
            continue
        slug = _txt(e.get("slug") or e.get("name"), 300)
        det = conv["detail"]
        m = e.get("metrics") or {}
        owner, name = _split_name(slug)
        full_name = f"{owner}/{name}"
        stars = _int(m.get("stars"))
        dl30 = _int(m.get("npmDownloads30d"))
        dlm = _int(m.get("downloadsMonth"))
        rows.append([full_name, stars, dl30, dlm, None, None, None,
                     _txt(e.get("createdAt"), 60) or _txt(e.get("firstSeenAt"), 60),
                     det["type"], False, bool(det["deprecated"]),
                     None, None, None, None, None])
        prev = prev_wl.get(full_name) or {}
        wl[full_name] = {
            "first_seen": prev.get("first_seen") or (det["first_seen_at"] or "")[:10]
                        or now.strftime("%Y-%m-%d"),
            "sources": sorted(set((prev.get("sources") or []) + ["catalog"])),
            "last_seen": now.strftime("%Y-%m-%d"),
            "stars": stars or 0,
            "last_fetch": now.strftime("%Y-%m-%d"),
        }
        (REPOS_DIR / f"{owner}__{name}.json").write_text(
            json.dumps(conv, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")
        written += 1

    snap = {"date": stamp, "run_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "repos": rows, "errors": []}
    (SNAP_DIR / f"{stamp}.json").write_text(
        json.dumps(snap, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    WATCHLIST_PATH.write_text(json.dumps(
        {"updated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "repos": wl},
        ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # prune repos/*.json for entries no longer in the catalog
    live = {"{}__{}.json".format(*_split_name(
        _txt(e.get("slug") or e.get("name"), 300) or ""))
        for e in entries if isinstance(e, dict)}
    pruned = 0
    for f in REPOS_DIR.glob("*.json"):
        if f.name not in live:
            f.unlink()
            pruned += 1
    log(f"written={written} skipped={skipped} pruned={pruned} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
