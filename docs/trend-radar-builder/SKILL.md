---
name: trend-radar-builder
description: >-
  Build a complete trend/leaderboard site for any data domain (arXiv papers,
  HuggingFace models, npm packages, extensions, papers-with-code — anything
  with a numeric popularity signal that changes over time) as a static site
  with daily snapshots, computed rankings, SSR detail pages, news coverage
  and GitHub Actions automation. Use when the user wants "a trending site /
  rank radar / leaderboard for X". The reference implementation is the public
  repo github.com/awesome-market/trending-rank-radar — clone it first, then
  adapt; do NOT write the site from scratch.
---

# Trend radar builder

Build a self-updating trend site: snapshot the domain's entities on a
schedule, store history as timestamped JSON, compute leaderboards, emit a
fully static site (list pages + one detail page per entity), deploy on
GitHub Pages via Actions. Everything below assumes you cloned the reference
implementation and are adapting it — the pipeline shape is proven, the
domain-specific parts are what you change.

**Reference implementation**: `git clone https://github.com/awesome-market/trending-rank-radar`
(tracks GitHub repos; ~3000 tracked entities, twice-daily snapshots, eight
boards, bilingual UI, live at zhuikan.com). Read `docs/02-data-pipeline.md`
and `docs/03-ranking.md` in it before writing code.

## Step 0 — ask the user, in ONE batch, before writing anything

These are the blocking questions. Ask them together, propose a sensible
default for each, and only ask what you cannot infer from context. Do not
start coding until items 1–3 have real answers.

1. **Entity + popularity signal** — what is being tracked, and what is the
   numeric metric that moves over time? *This is the project's existence
   condition: no time-varying metric → no trends, stop and resolve this
   first.* Repos→stars; HF models→likes/downloads; npm→weekly downloads;
   arXiv→has NO native metric (see domain notes). Also: the entity's stable
   ID and its canonical URL pattern (detail pages key off it).
2. **Source + history** — the API/scrape endpoint, auth needed? rate limit?
   Can historical values be backfilled from somewhere (an existing tracker,
   a stats API, dated snapshots)? If not, the site starts empty and the
   30-day boards only fill up after ~30 days of collection — tell the user
   this explicitly.
3. **Universe + cadence** — which subset gets tracked (a category list? top
   N by current metric?) and how often the metric meaningfully moves.
   Default: 2 snapshots/day for fast signals (stars, likes), 1/day for
   slower ones (downloads, citations). Universe size drives runtime:
   ~1500 entities ≈ 5–10 min/run for a typical REST/GraphQL batch API.
4. **Deployment** — GitHub Pages alone, or a custom domain? If the audience
   is mainly in China, GitHub Pages is unreliable — flag that a VPS or
   CDN-fronted origin may be needed (reference repo already went through
   this decision).
5. **Language** — monolingual or bilingual UI? Bilingual doubles the string
   table and adds per-block language visibility rules for news/readme
   sections. Default to the audience's single language unless asked.
6. **Detail-page material** — what rich content belongs on an entity page
   (README → abstract/model-card/package-docs; issues→comments/papers)?
   One rich block is enough for v1.
7. **News** — keep the bundled HN + Google/Bing News fetchers (they work for
   any entity with a name/URL) or skip? Any domain-specific news source
   worth adding?

With answers in hand, restate the plan in ≤10 lines and build.

## Architecture (copy this shape)

```
scripts/collect.py   # universe → API → data/snapshots/{date}T{hh}.json
scripts/<src>.py     # domain API client (pagination, retry, rate-limit)
scripts/rank.py      # snapshots → history series → boards → site/data/*.json
                     #   + SSR inject into site/*.html + site/repos/*.html
                     #   + sitemap.xml + robots.txt + llms.txt
scripts/news.py      # HN Algolia + Google/Bing News RSS → data/news/*.json
.github/workflows/   # cron: collect → news → rank → commit → Pages deploy
site/                # static shell (index/app/repo templates) — the artifact
data/                # snapshots, per-entity meta, news — inputs to rank.py
```

Invariants: `data/` holds raw/history inputs, `site/` is the only deployed
artifact and must be self-contained (Pages can only serve files under it).

## Adaptation map — what changes per domain

| Component | Action |
|---|---|
| source client (`scripts/gh.py`) | **rewrite** for the domain API; keep its retry/backoff/batch structure |
| `scripts/collect.py` | rewrite entity discovery + snapshot row schema; keep the snapshot-file format (`{date}T{hh}.json`, one row per entity, append-only) |
| snapshot columns | the first column is always entity identity; keep positional schema, version it when it grows, never rewrite old files |
| `scripts/rank.py` | keep the pipeline; rename metric fields; redefine boards to fit the domain (see board recipe) |
| `site/index.html` / `app.js` | re-skin labels/icons/i18n strings; keep SSR markers + hydration logic untouched |
| `site/repo.html` / `repo.js` | re-skin the detail page sections; keep fetch→render flow and language-toggle mechanics |
| `scripts/news.py` | reuse unchanged; adjust the search query string (entity name/URL pattern) |
| workflow | reuse as-is; adjust cron + deploy branch |
| sitemap/robots/llms | regenerate; llms.txt describes YOUR new schema |

## Board recipe

Derive boards from the metric history series; a good default set:

- **new** — entities created <90d, by current metric
- **daily / weekly / monthly growth** — metric delta over 1/7/30 days
- **daily / weekly / monthly growth-rate** — delta ÷ starting value
  (surfaces small-but-exploding entities the absolute boards hide)
- **all-time** — current metric, descending

Rate boards need ≥window+1 days of history; mark boards empty rather than
faking partial-window numbers.

## Invariants — the non-negotiable decisions

These took real debugging to learn. Keep all of them; skip none unless the
user explicitly says so.

1. **SSR everything crawlers should see.** Static shells hydrated by JS are
   invisible to non-JS crawlers (Baidu et al.). Inject rendered lists/detail
   content into `<!--MARK-->…<!--/MARK-->` anchors at build time; JS
   replaces it after hydration. Verify: `curl page.html` contains content.
2. **Asset cache-busting `?v=N` on every css/js tag** — and generated pages
   must embed the same version as their template. Bump on every frontend
   change; a stale cached JS will erase new SSR content.
3. **Failure-preserving merges.** Every external fetch merges new data INTO
   stored data keyed by stable IDs; a failed source contributes nothing and
   never erases stored items. Never truncate a dataset on fetch failure.
4. **Decouple input dirs per producer.** One directory per data producer
   (`data/news/`, `data/repos/`); two scripts must never write the same
   file — whoever runs later would silently drop the other's fields.
5. **`continue-on-error: true` on non-critical workflow steps** (news, any
   optional enrichment). A third-party outage must not block ranking/deploy.
6. **Positional snapshot schema, append-only.** Old files keep their column
   count; readers pad missing columns with null. Add columns only at the end.
7. **Language by content, not by fetch locale.** Tag news/readme blocks by
   detecting the text (CJK presence), not by which API locale returned it —
   aggregators routinely return cross-language results.
8. **Tiered fetch scope.** Hot set daily (current board union), universe
   weekly. Long-tail entities rarely produce new news; don't pay for them daily.
9. **Canonical URLs + hreflang + JSON-LD + sitemap.xml + robots.txt +
   llms.txt** on every entity page from day one — retrofitting SEO onto
   thousands of generated pages is miserable.
10. **`?board=`/`?period=` params collapse to one canonical URL.** Multiple
    list views are JS state, not separate pages.

## Verification gate — done means all of these

- `curl https://<domain>/` contains a rendered ranking (not an empty shell)
- `curl` one entity page: title/description/JSON-LD/metrics present, news
  block present if the entity has coverage
- `sitemap.xml` lists every entity page; `robots.txt` allows crawling
- JS assets return 200 at the `?v=N` referenced by generated pages
- the workflow completed twice on schedule with green rank+deploy steps
- a failed source (block it locally) leaves stored data intact
- non-JS: `<details>` month/year sections open; month cards visible

## Domain notes

**arXiv** — no native popularity metric. Options: Semantic Scholar citation
counts (free API, keyless), HF Papers likes (scrapes), alphaXiv; or pivot
the product to "new papers per day/week per category" where the metric is
paper velocity, not popularity. Resolve this with the user at question 1.

**HuggingFace** — models have `likes` + `downloads` via keyless API
(`huggingface.co/api/models?author=&sort=&limit=`); no history endpoint →
accumulate snapshots from day one. Model card = README equivalent
(`/api/models/{id}` returns cardData/body). Universe by task tag
(text-generation, image-to-image, …). Trending-ish feed exists at
`huggingface.co/api/trending` — use for the hot set.

**npm** — `api.npmjs.org/downloads/range/last-month/{pkg}` gives daily
download history (backfillable 18 months!); package metadata incl. README
from `registry.npmjs.org`. Universe via top-dependents lists.

**PyPI** — downloads via pepy.tech/pypistats (third-party), metadata via
`pypi.org/pypi/{pkg}/json` (keyless, has descriptions).

**Steam** — arguably the best-fit domain. Entity = appid; popularity =
concurrent players via keyless
`api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=`
(real-time engagement, better signal than cumulative stars), plus review
counts via `store.steampowered.com/appreviews/{appid}?json=1`. Rich detail
material from keyless `store.steampowered.com/api/appdetails?appids=`
(description, screenshots, genres, release date, price). Backfill:
SteamCharts per-game monthly avg/peak tables are scrapeable. Two domain
decisions to surface in the questions: CCU is diurnal — sample at a fixed
UTC hour for comparability or record daily peak via multiple samples; and
metric choice IS the product — CCU says "what's played", reviews say
"what's loved", wishlist/top-sellers say "what will be bought". The
snapshot schema can carry several at once.

**News/hot-list trends** — partial fit; the entity model inverts. Items
are ephemeral (a topic lives 1–3 days) and have no cross-platform stable
ID — the one hard problem is fuzzy title clustering so "同一事件" across
sources becomes one entity. Boards become cross-platform presence, hours
on list, peak rank, climb speed — not metric deltas. Cadence moves to
hourly (hot lists shift fast; still cheap — one call per source).
Sources: tophub.today mirrors, RSSHub routes (微博/知乎/百度/抖音 hot
lists), Google Trends daily RSS, HN frontpage, PullPush Reddit; hot-list
archive repos on GitHub allow backfill. Everything else — pipeline
skeleton, SSR, failure-preserving merge (hot-list APIs are flakier than
most), workflow, SEO kit — carries over unchanged.

Single-platform variant (e.g. **Douyin/抖音 hot list**): clustering
disappears (one platform ⇒ stable item titles/ids) and Douyin items carry
a real numeric 热度值, so boards like heat-velocity, hours-on-list and
peak-rank come for free — the best of both models. The hard part moves to
acquisition: no official API, the hot-list endpoint is signature+captcha
protected — consume it through an aggregator layer (DailyHotApi `/douyin`,
tophub.today which also keeps per-item history pages for backfill, RSSHub
`/douyin/hot`). Douyin is hostile to non-CN IPs: run the scraper layer
via CN-hosted public instances, never from an overseas VPS.

Any domain: if an existing tracker exists for it (like DiscoverHub was for
GitHub trending), check whether its archive pages can be scraped for
backfill — that single trick turned a 1-day-old site into a 60-day archive.
