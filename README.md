# OpenCode Plugins

<div align="center">

<br>

<h3>An open-data trend ranking for the OpenCode plugin / skill catalog — synced daily, all data freely downloadable.</h3>
<h3>🌐 <a href="https://opencode-plugins.zhuikan.com">opencode-plugins.zhuikan.com</a> · Mirror: <a href="https://awesome-market.github.io/awesome-opencode-plugins/">GitHub Pages</a> · <a href="README.zh.md">中文版</a></h3>

[**New Arrivals**](#new-board) • [**Boards**](#boards) • [**Data Sources**](#data-sources) • [**Features**](#features) • [**Architecture**](#architecture) • [**Run Locally**](#run-locally)

<hr>

</div>

<div id="new-board"></div>

<h3>🔥 New Arrivals · Top 20</h3>

<!-- BOARD:TOP20 -->
> Plugins listed in the last 90 days, ranked by current stars (≥10★). Full boards and history curves on the <a href="https://opencode-plugins.zhuikan.com">live site</a>.

| Plugin | Stars | Description |
| :--- | ---: | :--- |
| [**@omniroute/opencode-plugin-v2**](https://github.com/diegosouzapw/OmniRoute) | 86,882 | OmniRoute OpenCode plugin (v2 Promise API): catalog transform with models,… |
| [**upstash/context7**](https://github.com/upstash/context7) | 64,706 | Official Context7 plugin for OpenCode — wires up the Context7 MCP server and a… |
| [**volcengine/openviking**](https://github.com/volcengine/OpenViking) | 41,919 | OpenViking integration for Magpie: memory recall/capture and model switching… |
| [**othmanadi/planning-with-files**](https://github.com/OthmanAdi/planning-with-files) | 28,028 | Native OpenCode plugin for planning-with-files: per-turn plan injection, write… |
| [**different-ai/openwork**](https://github.com/different-ai/openwork) | 24,499 | Use OpenWork Cloud in OpenCode: sign in once, and your organization's AI… |
| [**startrail-org/pixelrag**](https://github.com/StarTrail-org/PixelRAG) | 10,855 | Give opencode eyes — screenshot any URL or document with pixelshot and read it… |
| [**npm/victrid-oh-my-opencode-slim**](https://github.com/alvinunreal/oh-my-opencode-slim) | 10,122 | Lightweight agent orchestration plugin for OpenCode - a slimmed-down fork of… |
| [**weave-os/router**](https://github.com/weave-os/router) | 5,621 | One-command installer that points Claude Code, Codex, opencode, or pi at the… |
| [**@plfavreau/opencode-dcp**](https://github.com/Opencode-DCP/opencode-dynamic-context-pruning) | 4,489 | Temporary build of @tarquinen/opencode-dcp 3.2.0 with the restart cache fix… |
| [**vshulcz/deja-vu**](https://github.com/vshulcz/deja-vu) | 1,531 | deja-vu memory for opencode: the session history of forty-two other coding… |
| [**npm/oh-my-agent-opencode**](https://github.com/first-fluke/oh-my-agent) | 1,422 | oh-my-agent hook bridge for OpenCode and Kilo Code |
| [**agents-universe/agents-universe**](https://github.com/agents-universe/agents-universe) | 903 | 不是问答机器人，而是能真正干活的数字分身。共享智能体，共享项目上下文，让项目所有成员一起协同工作。同时智能体会像人一样通过资料或者工作抽象和总结经验到项目上下文… |
| [**keli-wen/agy-staff**](https://github.com/keli-wen/agy-staff) | 862 | Hire Google's Antigravity CLI (agy) as a fast Gemini staffer for Claude Code,… |
| [**with-pebbly/aseprite-ai-artist**](https://github.com/with-pebbly/aseprite-ai-artist) | 653 | Agent-native control layer for Aseprite. MCP server (2025-11-25 spec, designed… |
| [**coldteadotai/abide**](https://github.com/coldteadotai/abide) | 625 | Make your coding agent abide by all your project rules |
| [**@aerovato/operator-opencode-v2**](https://github.com/aerovato/operator-memory) | 512 | Operator Memory adapter for OpenCode V2. |
| [**aerovato/operator-memory**](https://github.com/aerovato/operator-memory) | 500 | Operator Memory: durable context for agent-driven development. |
| [**tiger-zzz/mini-trellis**](https://github.com/Tiger-zzZ/mini-trellis) | 434 | Minimal memory layer for AI coding agents: spec, research, journal, and… |
| [**fishbottle7/opencode2dsh**](https://github.com/FishBottle7/opencode2dsh) | 398 | Free OpenCode Zen models for DeepSeek Harness (DSH): native dsh-llm adapter… |
| [**useagenthq/useagent**](https://github.com/useagenthq/useagent) | 384 | The open-source Devin alternative. Run Claude Code, Codex or OpenCode in… |
<!-- /BOARD:TOP20 -->

## Boards

| Board | Methodology |
|---|---|
| New Arrivals | Listed within the last 90 days, ranked by current stars (≥10★) |
| Debut | Entries first seen in the tracking scope on that day |
| Daily / Weekly / Monthly Surge | Absolute star growth over the window, descending (delta > 0, current ≥30★) |
| Daily / Weekly / Monthly Growth Rate | Relative growth = delta ÷ stars at window start × 100 (base ≥50) |
| Daily Downloads | Real per-day npm download counts, descending (see "Download data" below) |
| Yesterday Downloads | npm per-day downloads for the previous day |
| All-Time | Current cumulative stars, descending |

- Star growth is derived from **daily snapshot diffs**; when a window is incomplete, the earliest available snapshot is used and the actual range is annotated
- Historical browsing by day / month / year: month-end eight-board view, cumulative monthly growth, yearly growth and Top-10 summaries

## Data Sources

| Data | Source | Cadence |
|---|---|---|
| Catalog, stars, 30-day downloads, verification status | Upstream catalog [awesome-opencode-market](https://github.com/awesome-market/awesome-opencode-market) `index.json` | CI twice daily (UTC 03:00 / 15:00) |
| **Per-day downloads** | Official npm stats `api.npmjs.org/downloads/range` | Same as above, incrementally merged and kept long-term |
| Chinese descriptions | [OpenDock](https://github.com/qunqin24/opendock) `plugins.json`, filled in when upstream is missing | Every sync |
| Star history (since 2026-09-13) | OpenDock `history.json`, one-time backfill | Continued by this repo's snapshots afterwards |

The upstream catalog only publishes **rolling-window metrics** (`npmDownloads30d`), so this site maintains two long-term series of its own:

- `data/snapshots/<UTC-hour>.json` — full metric rows per sync (stars / 30-day downloads / month downloads), **committed to git and never deleted**
- `data/dlhist/<owner>__<name>.json` — real per-day download history `{date: count}` per plugin (180-day backfill on first sight, then a rolling 7-day incremental merge)

Entries whose source is GitHub-only (not published to npm) have no download data — stars only. That is a boundary of the data itself.

## Features

- **Bilingual UI**: `EN`/`中` toggle in the top-right corner, persisted locally
- **Dark / light themes**: manual toggle + system-preference fallback, flicker-free boot
- **Plugin detail pages**: metric cards, verification verdicts (verified / failed / flagged / unverified), capabilities & red flags (collapsed by default), version info, star-history curve, share card
- **Social**: sign-up & login, comments, likes, favorites, view counts, user center
- **SEO / GEO**: fully SSR'd detail pages, canonical / OG / JSON-LD, feeds, sitemap, llms.txt

## Architecture

```
awesome-opencode-market index.json        api.npmjs.org/downloads/range
        │  CI twice daily                          │  CI twice daily
        ▼                                          ▼
data/snapshots/*.json  data/repos/*.json   data/dlhist/*.json
        │  (the git repo IS the database — long-term archive)
        └──────────►  scripts/rank.py  ◄──────────┘
                            │  (boards + history + precomputed details)
                            ▼
               site/data/*.json + site/ static pages
                  │                │
        Cloudflare Pages    gh-pages mirror    site-data.db upload
```

- **Zero-dependency Python 3**: collection and computation use the standard library only
- **Pure static frontend**: vanilla HTML/CSS/JS, no build tooling
- **Data as archive**: snapshots and download history are committed to git — the repo itself is a downloadable historical database

## Methodology Notes

- New Arrivals / All-Time rank within **this site's tracking scope** (~5,200 entries, full upstream catalog)
- Growth rate = delta ÷ stars at window start, rounded to integer percent
- `30-day downloads` comes from upstream `metrics.npmDownloads30d` (rolling window); `per-day downloads` comes from official npm stats (UTC calendar days, ~1-day lag, labeled `approx` in the UI)
- `npm/` is a synthetic owner prefix used to normalize bare package names — it does not denote a maintainer
- Data is provided for reference only

## Run Locally

```bash
# Sync the upstream catalog → data/snapshots + data/repos + data/watchlist.json
python3 scripts/sync_catalog.py            # OCM_INDEX_URL overrides the source

# Collect per-day npm downloads → data/dlhist/*.json
python3 scripts/sync_downloads.py          # OCM_DL_LIMIT=8 for a smoke run

# Rebuild boards + site data → site/data + static pages
python3 scripts/rank.py --site-base https://opencode-plugins.zhuikan.com

# One-time OpenDock star-history backfill (optional, already run)
python3 scripts/import_opendock.py --catalog-only
```

## Directory Layout

```
data/snapshots/    Full metric snapshots (one per sync, kept forever)
data/repos/        Per-plugin detail JSON (upstream fields + filled Chinese descriptions)
data/dlhist/       Per-plugin daily npm download history
data/watchlist.json  Tracking roster (first-seen / last-seen dates)
scripts/           sync_catalog / sync_downloads / rank / pack_data / import_opendock
site/              Static frontend + generated data/ and pages (CI artifacts)
```

## License

MIT — data files are published as a repository; remix and re-use welcome.
