#!/usr/bin/env python3
"""Rebuild rankings and site/data JSON from collected snapshots.

Reads data/snapshots/*.json, groups by Beijing (Asia/Shanghai) calendar day
(last run of the day = "close"), computes the 11 boards per docs/03-ranking.md,
and writes:

  site/data/index.json
  site/data/days/YYYY-MM-DD.json
  site/data/months/YYYY-MM.json
  site/data/years/YYYY.json
  site/data/langs/<slug>.json    — latest-day boards re-ranked per language
  site/langs/<slug>.html         — static per-language board pages (day view)
  site/index.html                — latest landing board SSR'd into #listWrap
  site/feed.xml                  — Atom: latest day's debut + daily tops
  site/sitemap.xml, site/robots.txt

Usage:
  python scripts/rank.py [--site-base URL]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from bisect import bisect_left, bisect_right
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SNAP_DIR = DATA_DIR / "snapshots"
REPOS_DIR = DATA_DIR / "repos"
SITE_DIR = ROOT / "site"
SITE_DATA = SITE_DIR / "data"

BEIJING = timezone(timedelta(hours=8))
UTC = timezone.utc

# snapshot tuple indexes (data/snapshots format; 11-column rows predate the
# 16-column format — use _col() for indexes >10)
I_NAME, I_STARS, I_FORKS, I_WATCHERS, I_ISSUES, I_PRS, I_RELEASES = range(7)
I_CREATED, I_LANG, I_IS_FORK, I_IS_ARCH = 7, 8, 9, 10
I_ISSUES_OPEN, I_ISSUES_CLOSED, I_PRS_OPEN, I_PRS_CLOSED, I_PRS_MERGED = 11, 12, 13, 14, 15


def _col(row, i: int):
    """Safe column access for rows written before trailing fields existed."""
    return row[i] if len(row) > i else None

TOPN = 200          # precomputed per board; frontend filters then shows top 100
SERIES_DAYS = 30    # sparkline points
STALE_GRACE_DAYS = 14
NOMINAL = {"daily": 1, "weekly": 7, "monthly": 30}
GROWTH_BOARDS = ["daily", "weekly", "monthly"]
RATE_BOARDS = ["daily_rate", "weekly_rate", "monthly_rate"]
# metric dimension boards: daily growth on the download counters
# (I_FORKS col carries npmDownloads30d, I_WATCHERS carries downloadsMonth —
#  daily delta of the month-to-date counter ≈ yesterday's downloads)
METRIC_BOARDS = {"daily_downloads": I_FORKS, "daily_dl_yday": I_WATCHERS}
ALL_BOARDS = ["new", "debut", "daily", "daily_rate", "weekly", "weekly_rate",
              "monthly", "monthly_rate", "total",
              "daily_downloads", "daily_dl_yday"]
NEW_WINDOW_DAYS = 90
NEW_MIN_STARS = 10
GROWTH_MIN_STARS = 30
RATE_MIN_BASE = 50

DEFAULT_SITE_BASE = "https://opencode-plugins.zhuikan.com"


def log(msg: str) -> None:
    print(f"[rank {datetime.now(UTC).strftime('%H:%M:%S')}] {msg}", flush=True)


def parse_run_at(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def d(s: str) -> date:
    return date.fromisoformat(s)


# ------------------------------------------------------------------ loading --
def load_day_closes() -> tuple[dict[str, dict], dict[str, datetime]]:
    """Group snapshots by Beijing day; keep the latest run per day.

    Returns (day_close, run_at) where day_close[bdate] = {repo: tuple}.
    """
    by_day: dict[str, dict] = {}
    run_at: dict[str, datetime] = {}
    files = sorted(SNAP_DIR.glob("*.json")) if SNAP_DIR.exists() else []
    for f in files:
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            log(f"[warn] skip unreadable snapshot {f.name}: {e}")
            continue
        try:
            rt = parse_run_at(j["run_at"])
        except Exception:
            continue
        bdate = rt.astimezone(BEIJING).date().isoformat()
        cur = by_day.get(bdate)
        if cur is None or rt > run_at[bdate]:
            by_day[bdate] = {t[0]: tuple(t) for t in j.get("repos", []) if isinstance(t, list)}
            run_at[bdate] = rt
    return by_day, run_at


def build_repo_index(day_close: dict[str, dict]) -> dict[str, tuple[list, list]]:
    """repo -> (sorted beijing days, [metric tuples]) — tuples shared, low memory."""
    idx: dict[str, tuple[list, list]] = {}
    for day in sorted(day_close):
        for name, tup in day_close[day].items():
            ent = idx.get(name)
            if ent is None:
                ent = idx[name] = ([], [])
            ent[0].append(day)
            ent[1].append(tup)
    return idx


def load_repo_meta() -> dict[str, dict]:
    meta: dict[str, dict] = {}
    if REPOS_DIR.exists():
        for f in REPOS_DIR.glob("*.json"):
            try:
                j = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            owner_name = f.stem
            owner, _, name = owner_name.partition("__")
            if owner and name:
                meta[f"{owner}/{name}"] = j
    return meta


# ------------------------------------------------------------------ helpers --
def closest_day(days: list[str], target: str, before: str | None = None) -> str | None:
    """Valid day closest to `target`; ties → earlier. Optionally require < before."""
    i = bisect_left(days, target)
    cands = []
    if i < len(days) and (before is None or days[i] < before):
        cands.append(days[i])
    if i - 1 >= 0 and (before is None or days[i - 1] < before):
        cands.append(days[i - 1])
    if not cands:
        return None
    td = d(target)
    return min(cands, key=lambda x: (abs((d(x) - td).days), x))


def board_base_day(days: list[str], day: str, nominal: int) -> tuple[str, int, bool]:
    """Return (base_day, window_days, approx_board)."""
    target = (d(day) - timedelta(days=nominal)).isoformat()
    base = closest_day(days, target, before=day)
    if base is None:
        base = days[0]
    window_days = (d(day) - d(base)).days
    return base, window_days, window_days < nominal


def repo_value_at(ridx: dict, name: str, day: str):
    """Latest (day, tuple) for repo with repo-day <= `day`."""
    ds, vs = ridx[name]
    end = bisect_right(ds, day) - 1
    if end < 0:
        return None
    return ds[end], vs[end]


def repo_base_near(ridx: dict, name: str, base_day: str, day: str):
    """Repo day closest to base_day, restricted to days < `day`.

    Returns (repo_base_day, tuple) or None if repo has no usable base.
    """
    ds, vs = ridx[name]
    i = bisect_left(ds, base_day)
    cands = []
    if i < len(ds) and ds[i] < day:
        cands.append(i)
    if i - 1 >= 0 and ds[i - 1] < day:
        cands.append(i - 1)
    if not cands:
        return None
    bd = d(base_day)
    j = min(cands, key=lambda k: (abs((d(ds[k]) - bd).days), ds[k]))
    return ds[j], vs[j]


def series_for(ridx: dict, name: str, day: str, n: int = SERIES_DAYS) -> list[int]:
    ds, vs = ridx[name]
    end = bisect_right(ds, day)
    start = max(0, end - n)
    return [int(v[I_STARS] or 0) for v in vs[start:end]]


def make_entry(name: str, rank: int, cur, meta: dict, *,
               growth=None, rate=None, approx=False, stale=False,
               series=None, tag_pages=None) -> dict:
    owner, _, repo = name.partition("/")
    m = meta.get(name) or {}
    det = m.get("detail") or {}
    topics = (m.get("topics") or [])[:6]
    tp = tag_pages or ()
    return {
        "rank": rank,
        "owner": owner,
        "name": repo,
        "full_name": name,
        "description": m.get("description"),
        "avatar": det.get("avatar"),
        "homepage": m.get("homepage"),
        "topics": topics,
        "tag_pages": [s for s in (tag_slug(t) for t in topics) if s and s in tp],
        "language": cur[I_LANG],
        "stars": cur[I_STARS],
        "downloads30d": cur[I_FORKS],
        "downloads_month": cur[I_WATCHERS],
        "created_at": cur[I_CREATED],
        "growth": growth,
        "rate": rate,
        "approx": approx,
        "stale": stale,
        "series": series if series is not None else [],
    }


# ------------------------------------------------------------- repo pages --
def _esc(s) -> str:
    import html as _h
    return _h.escape(str(s or ""), quote=True)


def _plain(text: str, limit: int) -> str:
    text = re.sub(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", "", text or "")
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return _esc(re.sub(r"[#*`>]", "", text).strip()[:limit])


def _owner_url(p: dict) -> str:
    """Owner landing page: GitHub user when a real repo is known, else the
    npm profile ('npm' = synthetic owner for unscoped packages → registry)."""
    src_repo = p.get("source_repo") or ""
    owner = p.get("owner") or ""
    if "/" in src_repo:
        return f"https://github.com/{src_repo.split('/', 1)[0]}"
    if owner == "npm":
        return "https://www.npmjs.com"
    return f"https://www.npmjs.com/~{urllib.parse.quote(owner.lstrip('@'))}"


def _initial_avatar(name: str) -> str:
    """Offline-safe initials avatar for entries without a GitHub avatar."""
    ini = (name or "?")[0].upper()
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96">'
           f'<rect width="96" height="96" rx="10" fill="#1f6feb"/>'
           f'<text x="48" y="66" font-size="52" text-anchor="middle" '
           f'fill="#fff" font-family="sans-serif">{_esc(ini)}</text></svg>')
    import base64
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def _ssr_repo(p: dict) -> str:
    """Server-rendered repo detail HTML — readable by crawlers and no-JS
    clients, mirroring the layout repo.js produces (side card + info column,
    then all content sections; tabs aren't needed for crawlers)."""
    m = p.get("metrics") or {}
    def num(v): return f"{int(v):,}" if isinstance(v, (int, float)) else "–"
    stat_icons = {"stars": "★", "downloads30d": "↓", "downloads_month": "↧"}
    stats = "".join(
        f'<span class="rp-stat" title="{k}">{stat_icons[k]} <b>{num(m[k])}</b></span>'
        for k in ("stars", "downloads30d", "downloads_month")
        if m.get(k) is not None)
    _tag_pages = p.get("tag_pages") or frozenset()
    topics = "".join(
        (f'<a class="rp-topic" href="../tags/{_esc(tag_slug(t))}">{_esc(t)}</a>'
         if tag_slug(t) in _tag_pages
         else f'<a class="rp-topic" href="https://www.npmjs.com/search?q={_esc(t)}">{_esc(t)}</a>')
        for t in (p.get("topics") or [])[:8])
    _VERIF_ZH = {"verified": "已实测可装可用", "failed": "装不上或加载失败",
                 "skipped": "有高危信号没跑", "unverified": "还没验"}
    _VERIF_EN = {"verified": "Tested: installs & loads",
                 "failed": "Install or load failed",
                 "skipped": "Skipped — high-risk signals",
                 "unverified": "Not verified yet"}
    _vs = ((p.get("verification") or {}).get("status") or "unverified")
    verif_bit = (f'<span class="rp-meta-bit rp-verif-{_esc(_vs)}">'
                 f'{_bi(_VERIF_ZH.get(_vs, _vs), _VERIF_EN.get(_vs, _vs))}</span>')
    bits = [x for x in [
        verif_bit,
        f'<span class="rp-meta-bit">{_esc(p["language"])}</span>' if p.get("language") else "",
        f'<span class="rp-meta-bit">{_esc(p["license"])}</span>' if p.get("license") else "",
        f'<span class="rp-meta-bit">Created {_esc((p.get("created_at") or "")[:10])}</span>'
        if p.get("created_at") else "",
        (f'<a class="rp-meta-bit rp-home" href="{_esc(p["homepage"])}" rel="noopener">'
         f'{_esc(re.sub(r"^https?://", "", p["homepage"])[:60])}</a>'
         if re.match(r"^https?://", str(p.get("homepage") or ""), re.I) else ""),
    ] if x]
    order = ["new", "daily", "daily_rate", "weekly", "weekly_rate",
             "monthly", "monthly_rate", "total", "cumulative"]
    chips = "".join(
        f'<a class="rp-board-chip" href="../?board={b}">{b} <b>#{(p["boards"] or {})[b]}</b></a>'
        for b in order if (p.get("boards") or {}).get(b) is not None)
    growth = p.get("growth") or {}
    def gcell(k):
        g = growth.get(k)
        if not g or g.get("stars") is None:
            return ""
        up = g["stars"] >= 0
        lbl = {"day": "日增长", "week": "周增长", "month": "月增长"}[k]
        return (f'<div class="rp-metric"><div class="rp-metric-num '
                f'{"up" if up else "down"}">{"+" if up else ""}{num(g["stars"])}</div>'
                f'<div class="rp-metric-label">{lbl}</div></div>')
    growth_mets = gcell("day") + gcell("week") + gcell("month")
    met_keys = ["stars", "downloads30d", "downloads_month"]
    mets = "".join(
        f'<div class="rp-metric"><div class="rp-metric-num">{num(m[k])}</div>'
        f'<div class="rp-metric-label">{k}</div>'
        + '</div>' for k in met_keys if k in m)

    def lst(items, base):
        return "".join(
            f'<a class="rp-item" href="{base}/{i.get("number", "")}">'
            f'<span class="rp-item-num">#{i.get("number", "")}</span>'
            f'<span class="rp-item-title">{_esc(i.get("title"))}</span>'
            f'<span class="rp-item-extra">{i.get("comments", 0)} comments · '
            f'{_esc((i.get("created_at") or "")[:10])}</span></a>'
            for i in (items or [])[:8])

    rel = p.get("latest_release")
    rel_html = ""
    if rel:
        body = _plain(rel.get("body") or "", 600)
        pre = ('<span class="rp-rel-pre">Pre-release</span> '
               if rel.get("is_prerelease") else "")
        rel_html = (f'<h3 class="rp-ph">Latest release</h3>'
                    f'<a class="rp-rel" href="{_esc(p["url"])}/releases">'
                    f'<b>{_esc(rel.get("name") or rel.get("tag") or "")}</b> '
                    f'<span class="rp-rel-tag">{_esc(rel.get("tag") or "")}</span> '
                    f'{pre}'
                    f'<span class="rp-item-extra">{_esc((rel.get("published_at") or "")[:10])}</span></a>'
                    + (f'<pre class="rp-pre">{body}</pre>' if body else ""))
    dl_html = ""
    if rel and rel.get("tag"):
        tag = str(rel["tag"])
        vm = re.search(r"(\d[\d.]*)$", tag)
        ver = vm.group(1) if vm else tag
        base = (re.split(r"[:：\s]+", str(rel.get("name") or p["name"]))[0]
                or p["name"])
        file = (tag if not re.match(r"^v?\d[\d.]*$", tag, re.I)
                else (base if ver.lower() in base.lower() else f"{base}-{ver}"))
        rel_url = (rel.get("url")
                   or f'{p["url"]}/releases/tag/{urllib.parse.quote(tag, safe="")}')
        dl_html = (f'<div class="rp-dl">'
                   f'<span class="rp-dl-label">下载：</span>'
                   f'<span class="rp-dl-t">{_esc(rel.get("name") or tag)}</span>'
                   f'<a class="rp-dl-a" href="{_esc(rel_url)}">{_esc(file)} ↓</a>'
                   f'<span class="rp-dl-ver">{_esc(ver)}</span>'
                   f'<span class="rp-dl-date">'
                   f'{_esc((rel.get("published_at") or "")[:10])}</span></div>')
    readme = p.get("readme_excerpt")
    readme_html = (f'<h3 class="rp-ph">README</h3>'
                   f'<pre class="rp-pre rp-readme">{_plain(readme, 3000)}</pre>'
                   if readme else "")
    sec_i = sec_d = ""  # catalog has no issue/discussion feeds
    av_url = _esc(p.get("avatar") or "")
    same_links = "".join(
        f'<a class="rp-same-link" href="{_esc(x["full_name"]).replace("/", "__")}">'
        f'<img class="rp-same-av" src="{av_url}" alt="" loading="lazy">{_esc(x["name"])}</a>'
        for x in (p.get("same_owner") or [])[:20])
    if same_links:
        same_links = (f'<div class="rp-same-label">同作者插件</div>'
                      f'<div class="rp-same-row">{same_links}</div>')
    page_fn = _esc(p["full_name"]).replace("/", "__")
    news_html = _ssr_news(p.get("news") or [])
    owner_url = _owner_url(p)
    if p.get("avatar"):
        av_img = (f'<img class="rp-side-av" src="{_esc(p["avatar"])}?s=300" width="300" '
                  f'height="300" alt="{_esc(p["owner"])} avatar">')
    else:
        _ini = (p["name"] or "?")[0].upper()
        _svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300">'
                f'<rect width="300" height="300" rx="18" fill="#1f6feb"/>'
                f'<text x="150" y="195" font-size="150" text-anchor="middle" '
                f'fill="#fff" font-family="sans-serif">{_esc(_ini)}</text></svg>')
        av_img = ('<img class="rp-side-av" width="300" height="300" alt="" '
                  'src="data:image/svg+xml;base64,'
                  + __import__("base64").b64encode(_svg.encode()).decode() + '">')
    av = f'<a href="{page_fn}">{av_img}</a>'
    return f"""
<nav class="rp-crumb"><a href="../">Boards</a><span class="rp-crumb-sep">/</span>
<span class="rp-crumb-cur">{_esc(p['full_name'])}</span></nav>
<div class="rp-top">
  <aside class="rp-side">
    {av}
    <div class="rp-side-body card">
      <div class="rp-side-name">{_esc(p['name'])}</div>
      <a class="rp-side-owner" href="{_esc(owner_url)}">{_esc(p['owner'])}</a>
    </div>
  </aside>
  <div class="rp-main">
    <div class="rp-main-head">
      <h1 class="rp-htitle">
        <a class="rp-owner" href="{_esc(owner_url)}">{_esc(p['owner'])}</a>
        <span class="rp-sep">/</span><span class="rp-name">{_esc(p['name'])}</span>
      </h1>
      <div class="rp-head-chips">{chips}</div>
    </div>
    <p class="rp-desc">{_esc(p.get('description') or '')}</p>
    <div class="rp-statrow">{stats}</div>
    <div class="rp-topics">{topics}</div>
    <div class="rp-meta">{''.join(bits)}</div>
    <div class="rp-foot-row"><div class="rp-same">{same_links}</div>
      <div class="rp-actions"><a class="rp-btn" href="{_esc(p['url'])}">npm ↗</a></div></div>
  </div>
</div>
<section class="rp-panel card">{dl_html}<div class="rp-metric-grid">{growth_mets}{mets}</div>
{readme_html}{sec_i}{sec_d}{rel_html}</section>
{news_html}
{_ssr_comments(p.get('cm_items'))}
<p class="rp-meta">Snapshot: {_esc(p.get('snapshot_at'))} · Data license Apache-2.0 ·
<a href="../data/repos/{_esc(p['owner'])}__{_esc(p['name'])}.json">JSON</a></p>"""


def _fetch_comments() -> dict[str, list]:
    """Approved-comment snapshot for SSR, one bulk call to zhuikan-api.
    Crawlers/no-JS clients get the build-time snapshot; repo.js hydration
    overwrites it with live API data on load. Failure → empty map (comments
    are additive content, never worth failing the whole build over)."""
    api = os.environ.get("ZK_API_BASE", "https://api-openplugins.zhuikan.com")
    try:
        req = urllib.request.Request(
            f"{api.rstrip('/')}/comments/all_approved?site=oplugins",
            headers={"User-Agent": "trending-rank-radar-build"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read()).get("items") or {}
    except Exception as e:
        log(f"comments fetch failed ({e}) — pages render without SSR comments")
        return {}


def _ssr_comments(items: list) -> str:
    """Static comment tree mirroring repo.js loadComments(): newest top-level
    first, replies nested under .cm-kids (indent capped at two levels).
    Interactive bits (buttons, pending badges, translations) are omitted —
    hydration replaces this whole block with the live rendering anyway."""
    if not items:
        return ""
    by_id = {c["id"]: c for c in items}
    kids: dict[int, list] = {}
    tops = []
    for c in items:
        pid = c.get("parent_id")
        if pid and pid in by_id:
            kids.setdefault(pid, []).append(c)
        else:
            tops.append(c)
    tops.sort(key=lambda c: c["id"], reverse=True)

    def row(c: dict) -> str:
        av = (f'<img class="cm-av" src="{_esc(c["avatar_url"])}" width="24" '
              f'height="24" alt="" loading="lazy">'
              if c.get("avatar_url") else '<span class="cm-av cm-av-ph"></span>')
        pid = c.get("parent_id")
        p = by_id.get(pid) if pid else None
        rt = (f'<span class="cm-rt">↳ '
              f'{_esc(p.get("display_name") or p.get("username") or "")}</span>'
              if p else "")
        ts = c.get("created_at")
        try:
            when = datetime.fromtimestamp(int(ts), UTC).strftime("%Y-%m-%d")
        except (TypeError, ValueError):
            when = ""
        return (f'<div class="cm-item" data-id="{_esc(str(c["id"]))}">{av}'
                f'<div class="cm-main"><div class="cm-head">'
                f'<b>{_esc(c.get("display_name") or c.get("username") or "")}</b>'
                f'<span class="cm-time">{when}</span>{rt}</div>'
                f'<div class="cm-body">{_esc(c.get("body") or "")}</div>'
                f'</div></div>')

    def tree(c: dict, depth: int) -> str:
        cs = sorted(kids.get(c["id"], []), key=lambda k: k["id"])
        ind = min(depth + 1, 2)
        inner = "".join(tree(k, ind) for k in cs)
        return (row(c) + f'<div class="cm-kids"'
                + (' data-flat' if ind >= 2 else '')
                + f'>{inner}</div>' if inner else row(c))

    body = "".join(tree(c, 0) for c in tops)
    return (f'<section class="rp-panel card rp-cm-ssr">'
            f'<h3 class="rp-ph">评论 ({len(items)})</h3>'
            f'<div class="rp-cm-list">{body}</div></section>')


def _load_news(owner: str, repo: str) -> list:
    p = DATA_DIR / "news" / f"{owner}__{repo}.json"
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("items") or []
    except Exception:
        return []


def _ssr_news(items: list) -> str:
    """Bilingual press block for repo pages. Both languages render into the
    HTML (crawlable); the non-default one carries `hidden`, and repo.js
    flips visibility on language switch / re-render."""
    if not items:
        return ""
    zh = [i for i in items if i.get("lang") == "zh"]
    en = [i for i in items if i.get("lang") != "zh"]

    def row(i: dict) -> str:
        extra = _esc(i.get("date") or "")
        if i.get("source") == "Hacker News" and isinstance(i.get("points"), int):
            c = i.get("comments")
            extra = (f"▲ {i['points']:,}"
                     + (f" · {c:,} comments" if isinstance(c, int) else "")
                     + f" · {_esc(i.get('date') or '')}")
        return (f'<a class="rp-item" '
                f'href="{_esc(i.get("hn") or i.get("url") or "")}" '
                f'target="_blank" rel="noopener">'
                f'<span class="rp-news-src">{_esc(i.get("source") or "")}</span>'
                f'<span class="rp-item-title">{_esc(i.get("title") or "")}</span>'
                f'<span class="rp-item-extra">{extra}</span></a>')

    def block(lst: list, lang: str, title: str, hidden: bool) -> str:
        lattr = ' lang="zh-CN"' if lang == "zh" else ' lang="en"'
        h = " hidden" if hidden else ""
        more = ""
        if len(lst) > 10:
            label = f"展开其余 {len(lst) - 10} 条" if lang == "zh" \
                else f"{len(lst) - 10} more"
            more = (f'<details class="rp-news-more"><summary>{label}</summary>'
                    f'{"".join(row(i) for i in lst[10:])}</details>')
        return (f'<div class="rp-news-block"{lattr}{h}>'
                f'<h3 class="rp-ph">{title} ({len(lst)})</h3>'
                f'<div class="rp-list">{"".join(row(i) for i in lst[:10])}'
                f'{more}</div></div>')

    visible = "zh" if zh else "en"   # SSR default: zh first (site default lang)
    return ('<section class="rp-news card">'
            + (block(zh, "zh", "相关报道", visible != "zh") if zh else "")
            + (block(en, "en", "News &amp; coverage", visible != "en") if en else "")
            + "</section>")


# ------------------------------------------------------------ index SSR --
SSR_BEGIN, SSR_END = "<!--SSR-->", "<!--/SSR-->"
# landing-order fallback mirrors app.js (default board = 'daily')
SSR_BOARDS = ("daily", "new", "total", "weekly", "monthly")
SSR_LABELS = {"new": ("新星榜", "New Repos"), "debut": ("首登榜", "Debut"),
              "daily": ("日飙升榜", "Daily Growth"),
              "daily_rate": ("日增速榜", "Daily Rate"),
              "weekly": ("周飙升榜", "Weekly Growth"),
              "weekly_rate": ("周增速榜", "Weekly Rate"),
              "monthly": ("月飙升榜", "Monthly Growth"),
              "monthly_rate": ("月增速榜", "Monthly Rate"),
              "total": ("总榜", "All-Time"),
              "daily_downloads": ("下载日增榜", "Downloads Daily"),
              "daily_dl_yday": ("昨日下载榜", "Yesterday's Downloads")}
SSR_TOP = 50


def _bi(zh: str, en: str) -> str:
    """Bilingual inline: both languages baked, CSS shows the active one
    (html[lang] driven by common.js). Crawlers see and index both."""
    return (f'<span class="i18n-zh">{_esc(zh)}</span>'
            f'<span class="i18n-en">{_esc(en)}</span>')


def _board_label(board: str) -> tuple[str, str]:
    return SSR_LABELS.get(board, (board, board))


def _ssr_row(e: dict) -> str:
    """Crawler/first-paint row — mirrors app.js .rank-row markup."""
    owner, name = e["owner"], e["name"]
    href = f"repos/{owner}__{name}"
    rank = e.get("rank") or 0
    stars = e.get("stars")
    meta = []
    if e.get("language"):
        meta.append(f'<span class="lang-tag">{_esc(e["language"])}</span>')
    for glyph, val, key in (("★", stars, "stars"), ("↓", e.get("downloads30d"), "downloads30d"),
                            ("↧", e.get("downloads_month"), "downloads_month")):
        if isinstance(val, int):
            meta.append(f'<span class="m" title="{key}">{glyph} {val:,}</span>')
    desc = (e.get("description") or "").strip()
    if e.get("growth") is not None:
        side = f'<div class="row-growth"><span class="up-tri">▲</span>+{e["growth"]:,}</div>'
    else:
        side = (f'<div class="row-stars-big">★ {stars:,}</div>'
                if isinstance(stars, int) else "")
    tp = set(e.get("tag_pages") or [])
    pills = "".join(
        (f'<a class="row-tag" href="tags/{_esc(tag_slug(t))}">{_esc(t)}</a>'
         if tag_slug(t) in tp else
         f'<a class="row-tag" href="https://www.npmjs.com/search?q={_esc(t)}">{_esc(t)}</a>')
        for t in (e.get("topics") or [])[:4])
    foot = ('<div class="row-foot"><div class="row-soc"></div>'
            + (f'<div class="row-tags">{pills}</div>' if pills else "") + "</div>")
    return (f'<div class="rank-row" data-fn="{_esc(e.get("full_name") or "")}"><span class="row-rank{" top" if rank <= 3 else ""}">{rank}</span>'
            f'<a class="row-avatar" href="{href}"><img src="{_esc(e.get("avatar") or _initial_avatar(name))}" alt="" loading="lazy" width="48" height="48"></a>'
            f'<div class="row-body"><div class="row-name"><a class="row-link" href="{href}">'
            f'<span class="row-owner">{_esc(owner)}</span><span class="row-sep">/</span>'
            f'<span class="row-repo">{_esc(name)}</span></a></div>'
            f'<div class="row-meta">{"".join(meta)}</div>'
            + (f'<div class="row-desc">{_esc(desc)}</div>' if desc else "")
            + foot
            + f'</div><div class="row-side">{side}</div></div>')


def _inject(html: str, marker: str, block: str) -> tuple[str, int]:
    """Replace the <!--MARK-->...<!--/MARK--> span with marker+block (idempotent)."""
    begin, end = f"<!--{marker}-->", f"<!--/{marker}-->"
    return re.subn(re.escape(begin) + ".*?" + re.escape(end),
                   lambda _: begin + block + end, html, count=1, flags=re.S)


def _ssr_month_top10(days_entries: list) -> str:
    """Latest month's daily Top-10 chips — mirrors app.js .top10-day markup."""
    out = []
    for day in days_entries:
        chips = []
        for e in day.get("items") or []:
            href = f"repos/{e['owner']}__{e['name']}"
            g = e.get("growth")
            num = f"+{g:,}" if isinstance(g, int) else (
                f"★{e['stars']:,}" if isinstance(e.get("stars"), int) else "")
            chips.append(f'<span class="top10-chip"><a href="{href}">'
                         f'<span class="row-owner">{_esc(e["owner"])}</span>/{_esc(e["name"])}</a>'
                         + (f" <b>{num}</b>" if num else "") + "</span>")
        out.append(f'<div class="top10-day"><div class="top10-date">{_esc(day["date"])}</div>'
                   f'<div class="top10-items">{"".join(chips)}</div></div>')
    return "".join(out)


def _ssr_month_cards(months: list) -> str:
    """Month-index cards — mirrors app.js .month-card markup."""
    out = []
    for i, m in enumerate(months):
        y, mo = m.split("-")
        partial = (i == len(months) - 1)   # latest month is always in progress
        sub = "本月进行中 / in progress" if partial else "完整月 / full month"
        out.append(f'<div class="month-card{" partial" if partial else ""}">'
                   f'<div class="m-name">{_esc(y)}年{int(mo)}月</div>'
                   f'<div class="m-sub">{sub}</div></div>')
    return "".join(out)


def inject_index_ssr(board: str, items: list, day: str,
                     months: list, daily_top10: dict) -> None:
    """Bake current-data fallbacks into index.html so crawlers (Baidu doesn't
    run JS) and first paint on slow links see real content; app.js overwrites
    each block on hydrate."""
    path = SITE_DIR / "index.html"
    html = path.read_text(encoding="utf-8")
    html = re.sub(r'\.(js|css)\?v=\d+', rf'.\1?v={int(time.time())}', html)

    zh, en = _board_label(board)
    note = (f'<p style="color:var(--muted,#8b949e);font-size:13px;margin:0 4px 10px">'
            f'{_esc(day)} · {_bi(zh, en)} Top {len(items)} · '
            f'{_bi("每日快照", "daily snapshot")}</p>')
    # same static board nav as the /b/* pages — the JS-rendered tab bar
    # leaves #boardTabs empty for crawlers that don't execute scripts
    nav = ('<p style="color:var(--muted,#8b949e);font-size:12px;margin:0 4px 8px">'
           + " · ".join(f'<a href="b/{b}">{_esc(e2)}</a>'
                        for b, (_, e2) in SSR_LABELS.items())
           + "</p>")
    rows = (note + nav + '<div class="rank-list">'
            + "".join(_ssr_row(e) for e in items) + "</div>")
    html, n1 = _inject(html, "SSR", rows)

    n2 = n3 = 0
    if months and daily_top10.get(months[-1]):
        html, n2 = _inject(html, "SSRMT",
                           _ssr_month_top10(daily_top10[months[-1]]))
    if months:
        html, n3 = _inject(html, "SSRMG", _ssr_month_cards(months))

    if n1 + n2 + n3:
        path.write_text(html, encoding="utf-8")
        log(f"index SSR: board={board} rows={len(items)} "
            f"top10_days={bool(n2)} month_cards={bool(n3)}")
    else:
        log("[warn] index.html missing SSR markers; skipped")


# ---------------- per-language static pages ----------------
# docs/06 phase-4 `?lang=python`, realized as static pages: the candidate pool
# is filtered by language BEFORE ranking (full-fidelity per-language rank, not
# a clipped view of the global top-200). Latest-day boards only — day view.
LANG_TOP = 15             # static pages for at most this many languages
LANG_MIN_REPOS = 50       # a language page needs this many tracked repos
LANG_SLUGS = {"C++": "cpp", "C#": "csharp", "F#": "fsharp",
              "Objective-C": "objc", "Jupyter Notebook": "jupyter-notebook",
              "Vim Script": "vimscript", "Common Lisp": "common-lisp"}


def lang_slug(lang: str) -> str:
    return LANG_SLUGS.get(lang) or re.sub(
        r"[^a-z0-9]+", "-", lang.lower()).strip("-")


# ---------------- per-tag static pages ----------------
# /tags/<slug> — repos grouped by GitHub topic. Same skeleton trick as langs:
# index.html + data-tag attrs, app.js hydrates a single star-sorted list.
TAG_MIN_REPOS = 3         # a tag page needs at least this many tracked repos
TAG_TOP = 100             # list cap per tag page
TAG_MAX_PAGES = 200       # cap total tag pages — the 2-3-repo topic tail is
                          # thin SEO junk and file count is a hard deploy limit


def tag_slug(tag: str) -> str:
    """GitHub topics are already lowercase-slug format; sanitize anyway so a
    stray 'C++'/'Machine Learning' topic still maps to a stable page name."""
    return re.sub(r"[^a-z0-9-]+", "-", tag.lower()).strip("-")


def render_tag_page(tag: str, slug: str, items: list, day: str,
                    template: str, base: str) -> str:
    """Static /tags/<slug>.html — single star-sorted repo list for the tag."""
    url = f"{base}/tags/{slug}"
    html = template.replace(
        "<body>",
        f'<body data-base="../" data-tag="{_esc(slug)}" '
        f'data-tag-name="{_esc(tag)}">', 1)
    html = re.sub(r"<title>.*?</title>",
                  lambda _: f"<title>#{_esc(tag)} · OpenCode Plugins</title>",
                  html, count=1, flags=re.S)
    desc = (f"OpenCode {tag} 类插件趋势榜 · "
            f"{len(items)} OpenCode plugins tagged {tag} · "
            "OpenCode 插件市场趋势榜单")
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{_esc(desc)}">',
                  html, count=1)
    html = html.replace(
        '<link rel="canonical" href="https://opencode-plugins.zhuikan.com/">',
        f'<link rel="canonical" href="{_esc(url)}">')
    html = html.replace(
        '<meta property="og:url" content="https://opencode-plugins.zhuikan.com/">',
        f'<meta property="og:url" content="{_esc(url)}">')
    note = (f'<p style="color:var(--muted,#8b949e);font-size:13px;margin:0 4px 10px">'
            f'{_esc(day)} · #{_esc(tag)} · {len(items)} '
            f'{_bi("个插件 · 按 star 排序", "repos · by stars")}</p>')
    html, _ = _inject(html, "SSR",
                      note + '<div class="rank-list">'
                      + "".join(_ssr_row(e) for e in items[:SSR_TOP]) + "</div>")
    html, _ = _inject(html, "SSRMT", "")
    html, _ = _inject(html, "SSRMG", "")
    html = html.replace('"assets/', '"../assets/')
    html = html.replace('href="./"', 'href="../"')
    html = html.replace('href="repos/', 'href="../repos/')
    html = html.replace('href="tags/', 'href="../tags/')
    html = html.replace('href="data/', 'href="../data/')
    html = html.replace('href="manifest.webmanifest"',
                        'href="../manifest.webmanifest"')
    for leaf in ("feed.xml", "llms.txt", "sitemap.xml"):
        html = html.replace(f'href="{leaf}"', f'href="../{leaf}"')
    return html


def render_lang_page(lang: str, slug: str, boards: dict, day: str,
                     template: str, base: str) -> str:
    """Static /langs/<slug>.html — reuses the index.html skeleton so tabs,
    podium, rows, theme and i18n all work via app.js `data-lang` mode."""
    url = f"{base}/langs/{slug}"
    html = template.replace(
        "<body>",
        f'<body data-base="../" data-lang="{_esc(slug)}" '
        f'data-lang-name="{_esc(lang)}">', 1)
    html = re.sub(r"<title>.*?</title>",
                  lambda _: f"<title>{_esc(lang)} · OpenCode Plugins</title>",
                  html, count=1, flags=re.S)
    html = html.replace(
        '<meta name="description" content="',
        f'<meta name="description" content="{_esc(lang)} OpenCode 插件榜单 · '
        f'{_esc(lang)} trending OpenCode plugins · ', 1)
    html = html.replace(
        '<link rel="canonical" href="https://opencode-plugins.zhuikan.com/">',
        f'<link rel="canonical" href="{_esc(url)}">')
    html = html.replace(
        '<meta property="og:url" content="https://opencode-plugins.zhuikan.com/">',
        f'<meta property="og:url" content="{_esc(url)}">')
    # SSR the language's daily board; month/year widgets don't apply here
    items = ((boards.get("daily") or {}).get("items") or [])[:SSR_TOP]
    zh, en = _board_label("daily")
    note = (f'<p style="color:var(--muted,#8b949e);font-size:13px;margin:0 4px 10px">'
            f'{_esc(day)} · {_esc(lang)} · {_bi(zh, en)} Top '
            f'{len(items)} · {_bi("每日快照", "daily snapshot")}</p>')
    html, _ = _inject(html, "SSR",
                      note + '<div class="rank-list">'
                      + "".join(_ssr_row(e) for e in items) + "</div>")
    html, _ = _inject(html, "SSRMT", "")
    html, _ = _inject(html, "SSRMG", "")
    # subdirectory page — every root-relative ref needs ../ (covers the
    # injected rows' repos/ links too since they were just injected)
    html = html.replace('"assets/', '"../assets/')
    html = html.replace('href="./"', 'href="../"')
    html = html.replace('href="repos/', 'href="../repos/')
    html = html.replace('href="tags/', 'href="../tags/')
    html = html.replace('href="data/', 'href="../data/')
    html = html.replace('href="manifest.webmanifest"',
                        'href="../manifest.webmanifest"')
    for leaf in ("feed.xml", "llms.txt", "sitemap.xml"):
        html = html.replace(f'href="{leaf}"', f'href="../{leaf}"')
    return html


# ---------------- per-board static pages ----------------
# /b/<board> (latest day) and /b/<board>/<date> — gives every board state a
# real URL for search engines. Same index.html skeleton + SSR'd rows +
# data-board/data-sel attrs so app.js hydrates into the exact same view.

def render_board_page(board: str, day: str, items: list, days: list,
                      template: str, base: str, rel: str,
                      dated: bool = True) -> str:
    """day = content date; dated=False → canonical /b/<board> (latest-day entry)."""
    zh, en = _board_label(board)
    url = f"{base}/b/{board}" + (f"/{day}" if dated else "")
    html = template.replace(
        "<body>",
        f'<body data-base="{rel}" data-board="{_esc(board)}"'
        f' data-sel="{_esc(day)}">', 1)
    title = f"{zh} · {day} · OpenCode 插件趋势榜单 · OpenCode Plugins"
    html = re.sub(r"<title>.*?</title>",
                  lambda _: f"<title>{_esc(title)}</title>",
                  html, count=1, flags=re.S)
    desc = (f"{day} {zh} OpenCode 插件 Top {len(items)} · "
            f"{en} top {len(items)} trending OpenCode plugins · "
            "OpenCode 插件市场趋势榜单 · "
            "Independent OpenCode plugin-market trend radar.")
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{_esc(desc)}">',
                  html, count=1)
    html = html.replace(
        '<link rel="canonical" href="https://opencode-plugins.zhuikan.com/">',
        f'<link rel="canonical" href="{_esc(url)}">')
    html = html.replace(
        '<meta property="og:url" content="https://opencode-plugins.zhuikan.com/">',
        f'<meta property="og:url" content="{_esc(url)}">')

    # static nav so crawlers can traverse the whole board/date graph;
    # app.js replaces the block on hydrate anyway
    nav_boards = " · ".join(
        f'<a href="{rel}b/{b}">{_esc(e2)}</a>'
        for b, (_, e2) in SSR_LABELS.items())
    i = days.index(day) if day in days else -1
    prev_next = []
    if i > 0:
        prev_next.append(f'<a href="{rel}b/{board}/{days[i - 1]}">← {days[i - 1]}</a>')
    if 0 <= i < len(days) - 1:
        prev_next.append(f'<a href="{rel}b/{board}/{days[i + 1]}">{days[i + 1]} →</a>')
    nav = (f'<p style="color:var(--muted,#8b949e);font-size:12px;margin:0 4px 8px">'
           + (" | ".join(prev_next) + " · " if prev_next else "")
           + nav_boards + "</p>")

    note = (f'<p style="color:var(--muted,#8b949e);font-size:13px;margin:0 4px 10px">'
            f'{_esc(day)} · {_bi(zh, en)} Top {len(items)} · '
            f'{_bi("每日快照", "daily snapshot")}</p>')
    html, _ = _inject(html, "SSR",
                      nav + note + '<div class="rank-list">'
                      + "".join(_ssr_row(e) for e in items) + "</div>")
    html, _ = _inject(html, "SSRMT", "")
    html, _ = _inject(html, "SSRMG", "")
    # prefix every root-relative ref for this page's depth (covers the
    # injected rows' repos/ links too since they were just injected)
    html = html.replace('"assets/', f'"{rel}assets/')
    html = html.replace('href="./"', f'href="{rel}"')
    html = html.replace('href="repos/', f'href="{rel}repos/')
    html = html.replace('href="tags/', f'href="{rel}tags/')
    html = html.replace('href="data/', f'href="{rel}data/')
    html = html.replace('href="manifest.webmanifest"',
                        f'href="{rel}manifest.webmanifest"')
    html = html.replace('href="b/', f'href="{rel}b/')
    for leaf in ("feed.xml", "llms.txt", "sitemap.xml"):
        html = html.replace(f'href="{leaf}"', f'href="{rel}{leaf}"')
    return html


def write_feed(latest_day: str, boards: dict, stamp: str, base: str) -> None:
    """Atom feed — debut board first ('what just appeared'), then daily top.
    One entry per repo, deduped."""
    entries = []
    seen = set()
    for kind, zh in (("debut", "首登"), ("daily", "日增")):
        for e in (boards.get(kind) or {}).get("items", [])[:15]:
            fn = e["full_name"]
            if fn in seen:
                continue
            seen.add(fn)
            g = e.get("growth")
            title = f"[{zh}] {fn}" + (f" +{g:,}★" if isinstance(g, int) else "")
            link = f"{base}/repos/{fn.replace('/', '__')}"
            entries.append(
                "  <entry>\n"
                f"    <title>{_esc(title)}</title>\n"
                f'    <link href="{_esc(link)}"/>\n'
                f"    <id>{_esc(link)}</id>\n"
                f"    <updated>{stamp}</updated>\n"
                + (f"    <summary>{_esc((e.get('description') or '')[:300])}</summary>\n"
                   if e.get("description") else "")
                + "  </entry>")
    feed = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="zh-CN">\n'
            "  <title>OpenCode Plugins</title>\n"
            f'  <link href="{_esc(base)}/feed.xml" rel="self"/>\n'
            f'  <link href="{_esc(base)}/"/>\n'
            f"  <id>{_esc(base)}/feed.xml</id>\n"
            f"  <updated>{stamp}</updated>\n"
            + "\n".join(entries) + "\n</feed>\n")
    (SITE_DIR / "feed.xml").write_text(feed, encoding="utf-8")


def render_repo_page(p: dict, template: str, base: str) -> str:
    """Patch site/repo.html into a per-repo static page: unique title/meta/
    canonical, SSR content, and data-base so repo.js fixes relative paths."""
    fn = p["full_name"]
    fname = f'{p["owner"]}__{p["name"]}'
    canon = f"{base}/repos/{fname}"
    desc = ((p.get("description") or "").replace("\n", " ")[:200]
            or f"{fn} — OpenCode plugin: downloads trend, board ranks, verification")
    title = f"{fn} · OpenCode Plugins"
    owner_url = _owner_url(p)
    ld = {
        "@context": "https://schema.org",
        "@type": "SoftwareSourceCode",
        "name": fn,
        "codeRepository": p["url"],
        "url": canon,
        "description": desc,
        "author": {"@type": "Organization", "name": p["owner"],
                   "url": owner_url},
        "isAccessibleForFree": True,
    }
    if p.get("type"):
        ld["additionalType"] = f"OpenCode {p['type']}"
    if p.get("created_at"):
        ld["dateCreated"] = str(p["created_at"])[:10]
    if p.get("license") and re.match(r"^[A-Za-z0-9.\-+]+$", str(p["license"])):
        ld["license"] = f"https://spdx.org/licenses/{p['license']}.html"
    if p.get("topics"):
        ld["keywords"] = ",".join(p["topics"][:10])
    ld_block = ('<script type="application/ld+json">'
                + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
                + "</script>")
    keywords = ", ".join(
        [p["name"], p["owner"], fn, "github stars", "github trending",
         "star growth", "star history", "开源项目", "星标增长"]
        + [t for t in (p.get("topics") or [])[:6]])
    out = template
    out = re.sub(r"<title>.*?</title>", lambda m: f"<title>{_esc(title)}</title>", out, count=1)
    out = re.sub(r'<meta name="description" content="[^"]*">',
                 lambda m: f'<meta name="description" content="{_esc(desc)}">', out, count=1)
    out = out.replace('<meta name="robots" content="noindex,follow">',
                      f'<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">\n'
                      f'<meta name="keywords" content="{_esc(keywords)}">')
    out = re.sub(r'<link rel="canonical" href="[^"]*">',
                 lambda m: f'<link rel="canonical" href="{_esc(canon)}">', out, count=1)
    out = re.sub(r'<meta property="og:title" content="[^"]*">',
                 lambda m: f'<meta property="og:title" content="{_esc(title)}">', out, count=1)
    out = re.sub(r'<meta property="og:description" content="[^"]*">',
                 lambda m: f'<meta property="og:description" content="{_esc(desc)}">', out, count=1)
    out = re.sub(r'<meta property="og:url" content="[^"]*">',
                 lambda m: f'<meta property="og:url" content="{_esc(canon)}">', out, count=1)
    out = out.replace('<meta property="og:type" content="website">',
                      '<meta property="og:type" content="article">', 1)
    out = out.replace("</head>", f"{ld_block}\n</head>", 1)
    out = out.replace('href="assets/', 'href="../assets/')
    out = out.replace('src="assets/', 'src="../assets/')
    out = out.replace('href="manifest.webmanifest"', 'href="../manifest.webmanifest"')
    out = out.replace('href="./"', 'href="../"')
    out = out.replace("<body>", f'<body data-repo="{_esc(fn)}" data-base="../">', 1)
    out = out.replace('<div id="repoContent" class="repo-page"></div>',
                      f'<div id="repoContent" class="repo-page">{_ssr_repo(p)}</div>')
    return out


# ------------------------------------------------------------------ boards --
def eligible(cur) -> bool:
    return not cur[I_IS_FORK] and not cur[I_IS_ARCH]


def compute_boards(day: str, days: list[str], ridx: dict, meta: dict,
                   day_index: dict[str, int], lang: str | None = None,
                   tag_pages=None) -> dict:
    """Compute all boards for `day`. Returns {board: {window_start?, window_days?, items}}.
    `lang` restricts candidates to repos whose current language matches —
    powers the per-language static pages (full-fidelity re-rank, not a
    filtered view of the global top-200)."""
    i = day_index[day]
    prefix = days[: i + 1]
    cutoff_stale = (d(day) - timedelta(days=STALE_GRACE_DAYS)).isoformat()

    # base days per window (closest valid day to nominal target, < day)
    bases = {}
    for kind, nominal in NOMINAL.items():
        b, w, ap = board_base_day(prefix, day, nominal)
        bases[kind] = (b, w, ap)

    # gather per-repo current values once
    cur_map: dict[str, tuple] = {}       # name -> (cur_day, tuple)
    for name in ridx:
        got = repo_value_at(ridx, name, day)
        if got is None:
            continue
        cday, ctup = got
        if cday < cutoff_stale:
            continue  # dead repo — not tracked anymore at this point in time
        if lang is not None and (ctup[I_LANG] or "") != lang:
            continue
        cur_map[name] = (cday, ctup)

    boards: dict[str, dict] = {}

    # ---- growth boards (daily/weekly/monthly + rate variants) -------------
    growth_cands: dict[str, list] = {k: [] for k in GROWTH_BOARDS + RATE_BOARDS}
    for name, (cday, ctup) in cur_map.items():
        if cday != day or not eligible(ctup):
            continue  # stale or fork/arch → never in growth boards
        cur_stars = ctup[I_STARS] or 0
        if cur_stars < GROWTH_MIN_STARS:
            continue
        for kind in GROWTH_BOARDS:
            base_day, window_days, approx_board = bases[kind]
            got = repo_base_near(ridx, name, base_day, day)
            if got is None:
                continue
            repo_base_day, btup = got
            base_stars = btup[I_STARS] or 0
            incr = cur_stars - base_stars
            if incr <= 0:
                continue
            approx = approx_board or (repo_base_day != base_day)
            entry_growth = incr
            rate = None
            if base_stars >= RATE_MIN_BASE:
                rate = int(incr * 100 // base_stars)
            growth_cands[kind].append((incr, name, ctup, approx, entry_growth, rate))
            if rate is not None:
                rate_kind = kind + "_rate"
                growth_cands[rate_kind].append((rate, name, ctup, approx, incr, rate))

    for kind in GROWTH_BOARDS + RATE_BOARDS:
        base_day, window_days, _ = bases[kind.replace("_rate", "")] if kind.endswith("_rate") else bases[kind]
        cands = growth_cands[kind]
        # sort: primary metric desc, tiebreak stars desc
        cands.sort(key=lambda x: (-x[0], -(x[2][I_STARS] or 0), x[1]))
        items = []
        for rank, (metric, name, ctup, approx, growth, rate) in enumerate(cands[:TOPN], 1):
            items.append(make_entry(
                name, rank, ctup, meta,
                growth=growth, rate=rate, approx=approx, stale=False,
                series=series_for(ridx, name, day), tag_pages=tag_pages,
            ))
        boards[kind] = {
            "window_start": base_day,
            "window_days": window_days,
            "items": items,
        }

    # ---- metric boards (daily forks / watchers growth) --------------------
    for kind, col in METRIC_BOARDS.items():
        base_day, window_days, approx_board = board_base_day(prefix, day, 1)
        m_cands = []
        for name, (cday, ctup) in cur_map.items():
            if cday != day or not eligible(ctup):
                continue
            gb = repo_base_near(ridx, name, base_day, day)
            if gb is None:
                continue
            bd, btup = gb
            incr = (ctup[col] or 0) - (btup[col] or 0)
            if incr <= 0:
                continue
            m_cands.append((incr, name, ctup, approx_board or bd != base_day))
        m_cands.sort(key=lambda x: (-x[0], -(x[2][I_STARS] or 0), x[1]))
        boards[kind] = {
            "window_start": base_day, "window_days": window_days,
            "items": [make_entry(n, r, t, meta, growth=g,
                                 approx=ap, series=series_for(ridx, n, day),
                                 tag_pages=tag_pages)
                      for r, (g, n, t, ap) in enumerate(m_cands[:TOPN], 1)]}

    # ---- new board ---------------------------------------------------------
    new_cutoff = (d(day) - timedelta(days=NEW_WINDOW_DAYS)).isoformat()
    new_cands = []
    for name, (cday, ctup) in cur_map.items():
        if not eligible(ctup):
            continue
        created = (ctup[I_CREATED] or "")[:10]
        stars = ctup[I_STARS] or 0
        if created >= new_cutoff and stars >= NEW_MIN_STARS:
            new_cands.append((stars, name, ctup, cday != day))
    new_cands.sort(key=lambda x: (-x[0], x[1]))
    boards["new"] = {"items": [
        make_entry(n, r, t, meta, growth=None, rate=None,
                   approx=False, stale=st, series=series_for(ridx, n, day),
                   tag_pages=tag_pages)
        for r, (_, n, t, st) in enumerate(new_cands[:TOPN], 1)
    ]}

    # ---- total board ---------------------------------------------------------
    total_cands = [(ctup[I_STARS] or 0, name, ctup, cday != day)
                   for name, (cday, ctup) in cur_map.items() if eligible(ctup)]
    total_cands.sort(key=lambda x: (-x[0], x[1]))
    boards["total"] = {"items": [
        make_entry(n, r, t, meta, growth=None, rate=None,
                   approx=False, stale=st, series=series_for(ridx, n, day),
                   tag_pages=tag_pages)
        for r, (_, n, t, st) in enumerate(total_cands[:TOPN], 1)
    ]}

    return boards


# ------------------------------------------------------------- month / year ---
def compute_span_board(day: str, days: list[str], ridx: dict, meta: dict,
                       base_day: str, nominal_days: int, tag_pages=None) -> dict:
    """Growth board over an arbitrary span (month cumulative / year growth)."""
    day_index = {x: i for i, x in enumerate(days)}
    i = day_index[day]
    prefix = days[: i + 1]
    cutoff_stale = (d(day) - timedelta(days=STALE_GRACE_DAYS)).isoformat()
    window_days = (d(day) - d(base_day)).days
    approx_board = window_days < nominal_days

    cands = []
    for name in ridx:
        got = repo_value_at(ridx, name, day)
        if got is None:
            continue
        cday, ctup = got
        if cday != day or cday < cutoff_stale or not eligible(ctup):
            continue
        cur_stars = ctup[I_STARS] or 0
        if cur_stars < GROWTH_MIN_STARS:
            continue
        b = repo_base_near(ridx, name, base_day, day)
        if b is None:
            continue
        repo_base_day, btup = b
        base_stars = btup[I_STARS] or 0
        incr = cur_stars - base_stars
        if incr <= 0:
            continue
        approx = approx_board or (repo_base_day != base_day)
        rate = int(incr * 100 // base_stars) if base_stars >= RATE_MIN_BASE else None
        cands.append((incr, rate, name, ctup, approx))

    cands.sort(key=lambda x: (-x[0], -(x[3][I_STARS] or 0), x[2]))
    items = []
    for rank, (incr, rate, name, ctup, approx) in enumerate(cands[:TOPN], 1):
        items.append(make_entry(name, rank, ctup, meta, growth=incr, rate=rate,
                                approx=approx, stale=False,
                                series=series_for(ridx, name, day),
                                tag_pages=tag_pages))
    return {"window_start": base_day, "window_days": window_days, "items": items}


def compute_debut_board(names: set, day: str, days: list[str], ridx: dict,
                        meta: dict, day_index: dict[str, int],
                        tag_pages=None) -> dict:
    """'Debut' board — repos entering any board for the first time at `day`
    (their names weren't in any earlier day's board items). Ranked by
    daily-window star growth; repos without a usable base fall to the tail
    sorted by stars and display their star total instead of a delta."""
    i = day_index[day]
    base_day, _, _ = board_base_day(days[: i + 1], day, NOMINAL["daily"])
    rows = []
    for name in names:
        got = repo_value_at(ridx, name, day)
        if not got:
            continue
        cday, ctup = got
        growth, approx = 0, False
        gb = repo_base_near(ridx, name, base_day, day)
        if gb is not None:
            delta = (ctup[I_STARS] or 0) - (gb[1][I_STARS] or 0)
            if delta > 0:
                growth, approx = delta, gb[0] != base_day
        rows.append((growth, ctup, approx, cday != day, name))
    rows.sort(key=lambda r: (-r[0], -(r[1][I_STARS] or 0), r[4]))
    return {"items": [
        make_entry(name, rank, ctup, meta,
                   growth=g or None, rate=None, approx=approx, stale=st,
                   series=series_for(ridx, name, day),
                   tag_pages=tag_pages)
        for rank, (g, ctup, approx, st, name) in enumerate(rows[:TOPN], 1)]}


def month_bounds(month: str) -> tuple[str, str]:
    y, m = int(month[:4]), int(month[5:7])
    first = date(y, m, 1)
    last = date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)
    return first.isoformat(), last.isoformat()


# -------------------------------------------------------------------- main ---
def main() -> int:
    ap = argparse.ArgumentParser(description="Rebuild rankings & site data")
    ap.add_argument("--site-base",
                    default=os.environ.get("SITE_BASE") or DEFAULT_SITE_BASE,
                    help="absolute site URL for sitemap/canonical (default: %(default)s)")
    args = ap.parse_args()
    args.site_base = (args.site_base or "").strip() or DEFAULT_SITE_BASE

    day_close, run_at = load_day_closes()
    days = sorted(day_close)
    if not days:
        log("no snapshots found — nothing to build")
        return 1
    day_index = {x: i for i, x in enumerate(days)}
    ridx = build_repo_index(day_close)
    meta = load_repo_meta()
    log(f"days={len(days)} ({days[0]}..{days[-1]}) repos_tracked={len(ridx)} meta={len(meta)}")

    SITE_DATA.mkdir(parents=True, exist_ok=True)
    for sub in ("days", "months", "years"):
        (SITE_DATA / sub).mkdir(parents=True, exist_ok=True)

    months_present = sorted({x[:7] for x in days})
    years_present = sorted({x[:4] for x in days})

    base_url = args.site_base.rstrip("/")
    tpl_index = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    # bust the browser/CDN cache for versioned assets on every build —
    # browsers otherwise keep stale app.js/repo.js for max-age=4h
    asset_v = str(int(time.time()))
    tpl_index = re.sub(r'\.(js|css)\?v=\d+', rf'.\1?v={asset_v}', tpl_index)
    bdir = SITE_DIR / "b"
    # dated board pages only cover recent history — file count is a hard
    # Cloudflare Pages deploy limit and they grow ~11/day otherwise
    bcut = (d(days[-1]) - timedelta(days=45)).isoformat()
    # drop stale /b pages beyond current history (e.g. after data pruning)
    if bdir.is_dir():
        for stale_html in bdir.glob("*/*.html"):
            if stale_html.stem not in set(days) and stale_html.stem != "index":
                stale_html.unlink()

    # Repo detail pages: every repo whose latest data is within the stale
    # grace window gets a page — board entries link here, so a tracked repo
    # that merely missed today's run shouldn't 404. Computed before the day
    # loop because board items carry tag pills resolved against tag_pages.
    latest_day = days[-1]
    stale_cutoff = (d(latest_day) - timedelta(days=STALE_GRACE_DAYS)).isoformat()
    detail_repos = dict(day_close[latest_day])
    for name in ridx:
        if name in detail_repos:
            continue
        ds0, vs0 = ridx[name]
        if ds0 and ds0[-1] >= stale_cutoff:
            detail_repos[name] = vs0[-1]

    owner_map: dict[str, list[str]] = {}
    for name in detail_repos:
        owner_map.setdefault(name.split("/")[0], []).append(name)

    # Tag index — pre-pass counts repos per topic so repo pages know which
    # tags earn a static page (link) and which stay plain pills.
    tag_map: dict[str, dict] = {}
    for name in detail_repos:
        for t in ((meta.get(name) or {}).get("topics") or []):
            s = tag_slug(t)
            if s:
                tag_map.setdefault(s, {"tag": t, "names": [],
                                       "items": []})["names"].append(name)
    tag_pages = {s for s, e in tag_map.items()
                 if len(e["names"]) >= TAG_MIN_REPOS}
    if len(tag_pages) > TAG_MAX_PAGES:
        keep = sorted(tag_pages, key=lambda s: -len(tag_map[s]["names"]))
        tag_pages = set(keep[:TAG_MAX_PAGES])

    # ---------------- per-day boards ----------------
    daily_top10: dict[str, list] = {}   # month -> [{date, items}]
    month_end_day: dict[str, str] = {}
    for day in days:
        month_end_day[day[:7]] = day  # last write wins → month end

    seen_boards: set[str] = set()
    for day in days:
        boards = compute_boards(day, days, ridx, meta, day_index,
                                tag_pages=tag_pages)
        appearing = {e["full_name"] for blk in boards.values()
                     for e in blk.get("items", [])}
        # day-0 has no earlier boards to diff against — emit an empty debut
        # board rather than a copy of "total" (everything would "debut").
        boards["debut"] = ({"items": []} if day == days[0] else
                           compute_debut_board(appearing - seen_boards, day,
                                               days, ridx, meta, day_index,
                                               tag_pages=tag_pages))
        seen_boards |= appearing
        payload = {
            "date": day,
            "snapshot_at": run_at[day].astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "history_start": days[0],
            "repo_count": len(day_close[day]),
            "boards": boards,
        }
        (SITE_DATA / "days" / f"{day}.json").write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

        # per-board static page: /b/<board>/<date> — recent history only;
        # older dates stay reachable via the day-picker + data/days/*.json
        for b in ALL_BOARDS:
            items = (boards.get(b) or {}).get("items") or []
            if items and day >= bcut:
                (bdir / b).mkdir(parents=True, exist_ok=True)
                (bdir / b / f"{day}.html").write_text(
                    render_board_page(b, day, items, days, tpl_index,
                                      base_url, "../../"), encoding="utf-8")

        # collect daily-board top10 for the month summary
        top10 = []
        for e in boards["daily"]["items"][:10]:
            top10.append({
                "owner": e["owner"], "name": e["name"],
                "stars": e["stars"], "growth": e["growth"], "rate": e["rate"],
                "approx": e["approx"], "language": e["language"],
            })
        daily_top10.setdefault(day[:7], []).append({"date": day, "items": top10})

    # ---------------- month files ----------------
    for month in months_present:
        end_day = month_end_day[month]
        first_cal, last_cal = month_bounds(month)
        month_days = [x for x in days if x.startswith(month)]
        first_data_day = month_days[0]
        nominal_days = (d(last_cal) - d(first_cal)).days
        partial = end_day < last_cal

        # month-end boards = reuse the day file we just wrote
        day_payload = json.loads((SITE_DATA / "days" / f"{end_day}.json").read_text(encoding="utf-8"))

        cumulative = compute_span_board(end_day, days, ridx, meta, tag_pages=tag_pages,
                                        base_day=first_data_day,
                                        nominal_days=nominal_days)
        payload = {
            "month": month,
            "month_end": end_day,
            "month_start": first_data_day,
            "days": len(month_days),
            "partial": partial,
            "boards": day_payload["boards"],
            "cumulative": cumulative,
            "daily_top10": daily_top10.get(month, []),
        }
        (SITE_DATA / "months" / f"{month}.json").write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # ---------------- year files ----------------
    for year in years_present:
        year_days = [x for x in days if x.startswith(year)]
        end_day = year_days[-1]
        first_data_day = year_days[0]
        last_cal = f"{year}-12-31"
        nominal_days = (d(last_cal) - d(f"{year}-01-01")).days
        partial = end_day < last_cal

        growth = compute_span_board(end_day, days, ridx, meta, tag_pages=tag_pages,
                                    base_day=first_data_day,
                                    nominal_days=nominal_days)
        payload = {
            "year": year,
            "year_end": end_day,
            "year_start": first_data_day,
            "days": len(year_days),
            "partial": partial,
            "growth": growth,
            "months": [m for m in months_present if m.startswith(year)],
        }
        (SITE_DATA / "years" / f"{year}.json").write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # ---------------- per-repo detail files ----------------
    latest_day = days[-1]
    latest_boards = boards   # last day-loop payload already includes "debut"

    # latest-day board entry pages: /b/<board> (canonical, undated)
    for b in ALL_BOARDS:
        items = (latest_boards.get(b) or {}).get("items") or []
        if items:
            (bdir / f"{b}.html").write_text(
                render_board_page(b, latest_day, items, days, tpl_index,
                                  base_url, "../", dated=False),
                encoding="utf-8")

    placements: dict[str, dict] = {}
    for b, blk in latest_boards.items():
        for e in blk.get("items", []):
            placements.setdefault(e["full_name"], {})[b] = e["rank"]

    repos_out = SITE_DATA / "repos"
    readme_out = SITE_DATA / "readme"
    repos_out.mkdir(parents=True, exist_ok=True)
    readme_out.mkdir(parents=True, exist_ok=True)
    pages_out = SITE_DIR / "repos"
    pages_out.mkdir(parents=True, exist_ok=True)
    repo_tpl = (SITE_DIR / "repo.html").read_text(encoding="utf-8")
    repo_tpl = re.sub(r'\.(js|css)\?v=\d+', rf'.\1?v={asset_v}', repo_tpl)
    base = args.site_base.rstrip("/")
    cm_map = _fetch_comments()
    detail_count = 0
    search_idx: list[dict] = []
    news_idx: list[dict] = []
    for name, cur in detail_repos.items():
        owner, _, repo = name.partition("/")
        m = meta.get(name) or {}
        det = m.get("detail") or {}
        ds, vs = ridx.get(name, ([], []))
        cur_day = ds[-1] if ds else latest_day
        stale = cur_day < latest_day
        # full README texts live in standalone .md files fetched on demand —
        # keeps repo JSON small; fall back to the old 3000-char excerpt
        readme_txt = det.get("readme") or det.get("readme_excerpt")
        readme_zh_txt = det.get("readme_zh")

        growth: dict = {}
        for label, nominal in (("day", 1), ("week", 7), ("month", 30)):
            target = (d(latest_day) - timedelta(days=nominal)).isoformat()
            i = bisect_right(ds, target) - 1
            if i >= 0:
                growth[label] = {
                    "stars": int(cur[I_STARS] or 0) - int(vs[i][I_STARS] or 0),
                    "downloads30d": int(cur[I_FORKS] or 0) - int(vs[i][I_FORKS] or 0),
                    "base_day": ds[i],
                }

        payload = {
            "full_name": name, "owner": owner, "name": repo,
            "url": m.get("url") or f"https://www.npmjs.com/package/{repo}",
            "description": m.get("description"),
            "description_zh": det.get("description_zh"),
            "homepage": m.get("homepage"),
            "topics": m.get("topics") or [],
            "tag_pages": sorted({sl for t in (m.get("topics") or [])
                                 if (sl := tag_slug(t)) and sl in tag_pages}),
            "language": cur[I_LANG],
            "license": det.get("license"),
            "avatar": det.get("avatar"),
            "created_at": cur[I_CREATED],
            "pushed_at": m.get("pushed_at"),
            "metrics": {
                "stars": cur[I_STARS], "downloads30d": cur[I_FORKS],
                "downloads_month": cur[I_WATCHERS],
            },
            "source_repo": det.get("source_repo"),
            "npm_id": det.get("npm_id"),
            "verification": det.get("verification"),
            "approval": det.get("approval"),
            "capabilities": det.get("capabilities"),
            "type": det.get("type"),
            "contains": det.get("contains") or [],
            "deprecated": bool(det.get("deprecated")),
            "deprecated_message": det.get("deprecated_message"),
            "maintainers": det.get("maintainers") or [],
            "growth": growth,
            "history": {
                "dates": ds,
                "stars": [int(v[I_STARS] or 0) for v in vs],
                "downloads30d": [int(v[I_FORKS] or 0) for v in vs],
                "downloads_month": [v[I_WATCHERS] for v in vs],
            },
            "boards": placements.get(name) or {},
            # 'npm' is the synthetic owner for unscoped packages — grouping
            # them under same_owner would lump thousands of unrelated entries
            "same_owner": [] if owner == "npm" else sorted(
                ({"full_name": n, "name": n.split("/")[1],
                  "boards": placements.get(n) or {}}
                 for n in owner_map.get(owner, []) if n != name),
                key=lambda x: (x["boards"].get("total") or 9999, x["name"]))[:20],
            "latest_release": det.get("latest_release"),
            "readme": bool(readme_txt),
            "readme_zh": bool(readme_zh_txt),
            "news": _load_news(owner, repo),
            "stale": stale,
            "snapshot_at": run_at[cur_day].astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "history_start": days[0],
        }
        (repos_out / f"{owner}__{repo}.json").write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")
        detail_count += 1
        for t in (m.get("topics") or []):
            s = tag_slug(t)
            if s in tag_pages:
                tag_map[s]["items"].append({
                    "full_name": name, "owner": owner, "name": repo,
                    "description": m.get("description"),
                    "homepage": m.get("homepage"),
                    "topics": (m.get("topics") or [])[:6],
                    "tag_pages": sorted({s2 for t in (m.get("topics") or [])
                                         if (s2 := tag_slug(t)) and s2 in tag_pages}),
                    "language": cur[I_LANG],
                    "avatar": det.get("avatar"),
                    "created_at": cur[I_CREATED],
                    "stars": cur[I_STARS],
                    "downloads30d": cur[I_FORKS],
                    "downloads_month": cur[I_WATCHERS],
                    "stale": stale,
                })
        search_idx.append({
            "n": name,
            "d": (m.get("description") or "")[:160],
            "l": cur[I_LANG],
            "s": int(cur[I_STARS] or 0),
            "f": int(cur[I_FORKS] or 0),
            "w": int(cur[I_WATCHERS] or 0),
        })
        nws = [i["title"] for i in (payload["news"] or [])[:8] if i.get("title")]
        if nws:
            news_idx.append({"n": name, "s": int(cur[I_STARS] or 0), "nw": nws})
        if readme_txt:
            (readme_out / f"{owner}__{repo}.md").write_text(
                readme_txt, encoding="utf-8")
        if readme_zh_txt:
            (readme_out / f"{owner}__{repo}.zh.md").write_text(
                readme_zh_txt, encoding="utf-8")
        # SSR gets the raw text (Chinese preferred — site default lang is zh)
        ssr_payload = dict(payload, readme_excerpt=readme_zh_txt or readme_txt,
                           cm_items=cm_map.get(name) or [],
                           tag_pages=tag_pages)
        page_html = render_repo_page(ssr_payload, repo_tpl, base)
        (pages_out / f"{owner}__{repo}.html").write_text(page_html, encoding="utf-8")

    # Prune artifacts of repos that fell out of detail_repos (dropped from the
    # watchlist long enough ago that snapshots stopped). rank no longer writes
    # these files, so what remains on disk is stale — and file count is a hard
    # Cloudflare Pages deploy limit.
    live = {n.replace("/", "__") for n in detail_repos}
    pruned = 0
    for d_, pat in ((pages_out, "*.html"), (repos_out, "*.json"),
                    (readme_out, "*.md")):
        for f in d_.glob(pat):
            stem = f.stem[:-3] if f.stem.endswith(".zh") else f.stem
            if stem not in live:
                f.unlink(); pruned += 1
    if pruned:
        log(f"pruned {pruned} stale repo artifacts")

    # Drop dated board pages written by earlier builds beyond the 45-day
    # window (generation is gated on `bcut` above; this prunes the backlog).
    for f in bdir.glob("*/*.html"):
        if f.stem < bcut:
            f.unlink()

    # search indexes — published as open data (the header search box itself
    # queries api-openplugins.zhuikan.com/search remotely). Compact {n,d,l,s} fields
    # cover repo name / owner / language / description for every tracked repo;
    # news titles live in a separate file. Documented in llms.txt.
    (SITE_DATA / "search-index.json").write_text(
        json.dumps(search_idx, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")
    (SITE_DATA / "search-news.json").write_text(
        json.dumps(news_idx, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")

    # ---------------- index / sitemap / robots ----------------
    # SSR the landing board into index.html — crawlers (Baidu doesn't run JS)
    # and first paint on slow links get real rows; app.js replaces on hydrate.
    try:
        for b in SSR_BOARDS:
            items = (latest_boards.get(b) or {}).get("items") or []
            if items:
                inject_index_ssr(b, items[:SSR_TOP], latest_day,
                                 months_present, daily_top10)
                break
    except Exception as e:
        log(f"[warn] index SSR failed: {e}")

    # ---------------- per-language static pages ----------------
    lang_count: Counter = Counter()
    for t in detail_repos.values():
        if t[I_LANG]:
            lang_count[t[I_LANG]] += 1
    top_langs = [l for l, n in lang_count.most_common()
                 if n >= LANG_MIN_REPOS][:LANG_TOP]
    langs_meta = []
    langs_dir = SITE_DIR / "langs"
    (SITE_DATA / "langs").mkdir(exist_ok=True)
    for lang in top_langs:
        slug = lang_slug(lang)
        try:
            lb = compute_boards(latest_day, days, ridx, meta, day_index,
                                lang=lang, tag_pages=tag_pages)
            (SITE_DATA / "langs" / f"{slug}.json").write_text(
                json.dumps({"lang": lang, "slug": slug, "date": latest_day,
                            "repo_count": lang_count[lang], "boards": lb},
                           ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8")
            tpl = (SITE_DIR / "index.html").read_text(encoding="utf-8")
            langs_dir.mkdir(exist_ok=True)
            (langs_dir / f"{slug}.html").write_text(
                render_lang_page(lang, slug, lb, latest_day, tpl, base_url),
                encoding="utf-8")
            langs_meta.append({"lang": lang, "slug": slug,
                               "repos": lang_count[lang]})
        except Exception as e:
            log(f"[warn] lang page {lang} failed: {e}")
    if langs_meta:
        log(f"langs: {len(langs_meta)} pages — "
            + ", ".join(l["lang"] for l in langs_meta))

    # ---------------- per-tag static pages ----------------
    # /tags/<slug> for every GitHub topic shared by ≥TAG_MIN_REPOS tracked
    # repos — repo-page topic pills link here.
    tags_dir = SITE_DIR / "tags"
    tags_data_dir = SITE_DATA / "tags"
    tags_data_dir.mkdir(exist_ok=True)
    tags_meta = []
    for slug in sorted(tag_pages):
        e = tag_map[slug]
        items = sorted(e["items"],
                       key=lambda x: -(x.get("stars") or 0))[:TAG_TOP]
        for i, it in enumerate(items, 1):
            it["rank"] = i
        try:
            tags_data_dir.mkdir(exist_ok=True)
            (tags_data_dir / f"{slug}.json").write_text(
                json.dumps({"tag": e["tag"], "slug": slug,
                            "date": latest_day,
                            "repo_count": len(e["names"]),
                            "boards": {"daily": {"items": items}}},
                           ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8")
            tags_dir.mkdir(exist_ok=True)
            tpl = (SITE_DIR / "index.html").read_text(encoding="utf-8")
            (tags_dir / f"{slug}.html").write_text(
                render_tag_page(e["tag"], slug, items, latest_day, tpl, base),
                encoding="utf-8")
            tags_meta.append({"tag": e["tag"], "slug": slug,
                              "repos": len(e["names"])})
        except Exception as exc:
            log(f"[warn] tag page {slug} failed: {exc}")
    # prune pages whose tag dropped below the threshold since last build
    for f in (tags_dir.glob("*.html") if tags_dir.is_dir() else []):
        if f.stem not in tag_pages:
            f.unlink()
    for f in tags_data_dir.glob("*.json"):
        if f.stem not in tag_pages:
            f.unlink()
    # lookup for repo.js — which topic slugs got a static page this build
    (SITE_DATA / "tags-index.json").write_text(
        json.dumps({m["slug"]: {"tag": m["tag"], "repos": m["repos"]}
                    for m in tags_meta},
                   ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")
    if tags_meta:
        log(f"tags: {len(tags_meta)} pages")

    # Atom feed — debut + daily top of the latest day
    try:
        write_feed(latest_day, latest_boards,
                   run_at[latest_day].astimezone(UTC)
                   .strftime("%Y-%m-%dT%H:%M:%SZ"), base_url)
    except Exception as e:
        log(f"[warn] feed.xml failed: {e}")

    index = {
        "generated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "site_base": args.site_base,
        "repo_count": len(day_close[days[-1]]),
        "first_day": days[0],
        "latest_day": days[-1],
        "snapshot_days": len(days),
        "dates": days,
        "months": months_present,
        "years": years_present,
        "langs": langs_meta,
        "tags": tags_meta,
    }
    (SITE_DATA / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")

    base = args.site_base.rstrip("/")
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
               f"  <url><loc>{base}/</loc><lastmod>{latest_day}</lastmod></url>"]
    # board entry points — latest-day page + every dated page (real URLs)
    for b in ALL_BOARDS:
        if (bdir / f"{b}.html").exists():
            sitemap.append(f"  <url><loc>{base}/b/{b}</loc>"
                           f"<lastmod>{latest_day}</lastmod></url>")
        for f in sorted((bdir / b).glob("*.html")) if (bdir / b).is_dir() else []:
            sitemap.append(f"  <url><loc>{base}/b/{b}/{f.stem}</loc>"
                           f"<lastmod>{f.stem}</lastmod></url>")
    # per-language static pages
    for lm in langs_meta:
        sitemap.append(f"  <url><loc>{base}/langs/{lm['slug']}</loc>"
                       f"<lastmod>{latest_day}</lastmod></url>")
    # per-tag static pages
    for tm in tags_meta:
        sitemap.append(f"  <url><loc>{base}/tags/{tm['slug']}</loc>"
                       f"<lastmod>{latest_day}</lastmod></url>")
    # repo detail pages — one static HTML per tracked repo
    for name in sorted(detail_repos):
        sitemap.append(f"  <url><loc>{base}/repos/{name.replace('/', '__')}</loc>"
                       f"<lastmod>{latest_day}</lastmod></url>")
    sitemap.append("</urlset>")
    (SITE_DIR / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    # robots.txt: open-data site — welcome all crawlers incl. AI/LLM ones (GEO)
    ai_bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot",
               "Claude-User", "Claude-SearchBot", "PerplexityBot",
               "Perplexity-User", "Google-Extended", "Applebot-Extended",
               "meta-externalagent", "Bytespider", "CCBot"]
    robots = ["# OpenCode Plugins — open-data project, all crawlers welcome.",
              "User-agent: *", "Allow: /", ""]
    robots += [f"User-agent: {b}\nAllow: /\n" for b in ai_bots]
    robots.append(f"Sitemap: {base}/sitemap.xml")
    (SITE_DIR / "robots.txt").write_text("\n".join(robots) + "\n", encoding="utf-8")

    log(f"site/data written: {len(days)} days, {len(months_present)} months, "
        f"{len(years_present)} years, {detail_count} repo details")
    return 0


if __name__ == "__main__":
    sys.exit(main())
