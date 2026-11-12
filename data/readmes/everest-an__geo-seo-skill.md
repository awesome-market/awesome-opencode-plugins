# geo-seo-skill

> **A complete GEO + SEO system as an opencode skill** — get your content ranked by Google *and* cited by ChatGPT, Perplexity, Gemini, and Claude. Includes the battle-tested **4-step rapid method** (rank #18 → #3 in 48 hours, traffic +320%) plus ready-to-run **audit scripts** for GEO readiness and multilingual (hreflang) SEO.

> 中文版备份见 `中文版/`（Chinese backup in `中文版/`）.

**TL;DR — What is GEO?**
Generative Engine Optimization (GEO) is the practice of optimizing content so AI answer engines select and cite it. **SEO competes for rankings; GEO competes to be part of the answer.** This skill gives you both, in one system.

---

## Why GEO Matters (with data)

AI search has changed how people find answers — and AI engines now eat into search traffic that traditional SEO used to win:

| Signal | Value | Source |
|--------|-------|--------|
| AI Overviews share of natural CTR | ~68% | Field observation |
| AI-standard content citation lift | +44% | Field observation |
| Content with quotes/statistics | +30–40% AI visibility | Princeton GEO paper (arXiv 2311.09735) |
| ChatGPT share of AI referral traffic | 85.79% | Semrush |
| Brand mentions in AI answers | 26–39% of queries | Semrush |

**The one sentence to remember:** content that is clear, structured, and easy to extract gets cited — AI cites *"the clearest, most authoritative, most extractable answer,"* not "the page ranked first."

---

## What's Inside

A six-layer system covering the full stack, from GEO foundations to technical execution to monitoring:

```
references/
├── 01-foundations.md           # GEO basics, SEO vs AEO vs GEO, AI engine landscape, RAG factors
├── 02-rapid-method.md          # ★ 4-step rapid method (Dig → Design → Clean → Drive)
├── 03-content-citation.md      # Information gain, extractability, FAST framework
├── 04-technical-crawl.md       # AI crawler robots.txt, llms.txt, Schema/SSR, entities
├── 05-authority-entities.md    # E-E-A-T, entity building, brand mentions
├── 06-monitoring.md            # Metrics, tools, GA4 AI-traffic setup
├── 07-prompt-library.md        # 10 copy-paste prompts
├── 08-tools-resources.md       # Papers, tool ecosystem, case studies
├── 09-i18n-seo.md              # Multilingual SEO (hreflang, inLanguage, llms.txt i18n)
├── 11-cn-geo-playbook.md       # China GEO: 1.37% official-site stat, ecosystem split, CN sources
└── 12-engine-citation-audit.md # Why does AI not cite us? retrieval vs selection, 5-step audit```

## Quick Start

1. **48-hour ranking sprint** → open `references/02-rapid-method.md`, run `Dig → Design → Clean → Drive`.
2. **Why won't AI cite me?** → check `03` (extractability + information gain), then `04` (AI crawler access).
3. **Multilingual site (/en /zh-CN /ja)?** → `09-i18n-seo.md` + the `i18n_audit.py` script.
4. **Need ready prompts?** → `07-prompt-library.md`.

## Automation Scripts (stdlib-only, zero dependencies)

```bash
# GEO readiness audit (FAST framework + citation signals) — HTML file, directory, or URL
py scripts/geo_audit.py <file|dir|url> [--json]

# International SEO audit — hreflang coverage/x-default/BCP-47/bidirectional,
# canonical, sitemap variants, inLanguage, og:locale, llms.txt
py scripts/i18n_audit.py <dir> --base-url https://example.com [--sitemap sitemap.xml] [--llms-txt llms.txt]

# Generate a spec-compliant /llms.txt (per-locale grouping)
py scripts/llms_txt.py --name "MyBrand" --site-url https://example.com --summary "..." \
    --pages "https://example.com/en/guide | The guide" ...
```

All three scripts are pure Python 3 standard library — no pip install needed. Use `--json` for machine-readable reports.

## Claude SEO Integration (`claude-seo/`)

This repo also vendors the full open-source [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) plugin (MIT) — **25 sub-skills, 18 specialist agents, 53 execution scripts** — for Claude Code. It runs parallel technical/content/schema/GEO/local/e-commerce/intl SEO audits against your site.

```
claude-seo/
  CLAUDE.md                      # Project instructions for Claude Code
  skills/                        # 25 sub-skills (auto-discovered)
    seo/                         # Main orchestrator skill (routing table)
    seo-geo/                     # AI search / GEO optimization (citability scoring)
    seo-audit/ seo-page/ seo-technical/ seo-content/ seo-content-brief/
    seo-schema/ seo-sitemap/ seo-images/ seo-local/ seo-maps/ seo-plan/
    seo-flow/ seo-programmatic/ seo-competitor-pages/ seo-hreflang/
    seo-google/ seo-backlinks/ seo-cluster/ seo-sxo/ seo-drift/
    seo-ecommerce/ seo-dataforseo/ seo-image-gen/
  agents/                        # 18 specialist subagents (parallel fan-out)
  scripts/                       # 53 Python execution scripts (GSC, GA4, CrUX, Moz, ...)
```

**Note:** unlike this repo's own zero-dependency `geo_audit.py` / `i18n_audit.py`, the vendored claude-seo scripts require `pip install -r claude-seo/requirements.txt` (Playwright Chromium + Google API clients) and optional API keys (GSC/GA4/Moz/DataForSEO). The skills themselves are prompt-driven and work without keys.

Upstream reference: [`AgriciDaniel/claude-seo`](https://github.com/AgriciDaniel/claude-seo) (MIT). Vendored under `claude-seo/` with its LICENSE intact.

## How to Install as an opencode Skill

1. This repo already ships an `opencode.json` registering both `.opencode/skills/` (this GEO skill) and `claude-seo/skills/` (all 25 vendored Claude SEO sub-skills) in `skills.paths`.
2. Restart opencode (skills load at startup).
3. It auto-triggers on: GEO, generative engine optimization, AEO, AI SEO, get cited by AI, AI Overviews, llms.txt, hreflang, multilingual SEO, 生成式引擎优化, 多语言SEO. The vendored skills add SEO audit, schema, backlinks, local, e-commerce, and more.

## FAQ

**Is GEO replacing SEO?**
No — GEO complements SEO. AI engines pull from the same web your SEO content lives on, so solid SEO is most of the GEO battle already won.

**What content gets cited by AI most?**
Original data, authoritative definitions, step-by-step guides, comparison tables, and FAQ blocks. Quotes and statistics lift AI visibility 30–40%.

**Does llms.txt really matter?**
It's not a Google lever: Google's own docs (2026) state Google Search ignores it, and only ~0.1% of AI-bot traffic requests it. Ship one anyway — AI coding agents (Cursor, Claude Code) consume it, and it's zero-cost optionality for non-Google systems. Just don't expect it to move rankings.

**Can I run this on a multilingual site?**
Yes — `references/09-i18n-seo.md` covers hreflang, locale-self canonicals, `inLanguage`, `og:locale`, multilingual `llms.txt`, and `i18n_audit.py` validates all of it automatically.

**Is this for humans or AI agents?**
Both. The skill is written for AI coding agents (opencode), but every reference is readable and actionable for human SEO teams too.

## License

MIT — free to use, modify, and distribute. A link back (or a star) is appreciated but not required.

---

*Created from a real experiment: an aged domain with zero backlinks and zero PR moved from #18 to #3 on Google in 48 hours using only AI-driven GEO — search traffic surged 320%.*
