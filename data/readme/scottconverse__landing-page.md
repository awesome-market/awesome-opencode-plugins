# landing-page

**A Claude skill that builds a real landing-page website for your repository — from what the
code actually does, not from what the README claims.**

[Install](#install) · [Project site](https://scottconverse.github.io/landing-page/) · [SKILL.md](SKILL.md) · [Changelog](CHANGELOG.md)

---

## For everyone (the plain-English version)

You have a repository. Soon someone who isn't you — a user, a contributor, a customer, your
boss — is going to look at it. Right now the only thing to look at is a README.

Ask most AI tools for a landing page and you get one of three disappointments: your README
chopped into cards, a design *proposal* that leaves the building to you, or a page full of
confident fiction — invented user counts, imaginary testimonials, "enterprise-grade" stamped on
a prototype.

`landing-page` is written against all three:

1. **It reads your code, not your README.** Source files, schemas, migrations, CI config,
   tests, live TODOs. Where the README and the implementation disagree, the implementation
   wins. Features that only exist as a stub get labeled honestly; capabilities that are real but
   undocumented get pulled onto the page — that's the thing projects most often under-sell.
2. **It builds the site.** Actual files: styling, responsive layouts, working navigation, build
   scripts, a deployment path. Then it runs the site, looks at it at desktop, tablet, and phone
   widths, and fixes what's broken. Stopping at a plan is a failure.
3. **It refuses to make things up.** Every claim is sorted into confirmed / partial / planned /
   unverified first, and the tier picks the wording. No invented metrics, testimonials, logos,
   awards, benchmarks, or roadmap dates.

The README it writes at the end is deliberately short — a technical entry point that links to
the site, not a second copy of it.

**Why it works this way:** the first version of this skill produced only a `README.md`, because
its source prompt asked for GitHub-flavored Markdown. Held up against a full hosted site built
from the same brief, it wasn't close. The rewrite made the website the deliverable, and that is
what version 1.0.0 is.

## For developers (the technical version)

`landing-page` is an [Agent Skill](https://code.claude.com/docs/en/skills) — a model-agnostic protocol
that any Claude instance (Opus, Sonnet, Haiku, Fable) can load and execute. Six Markdown files, no
runtime dependencies, no model-specific code:

```
SKILL.md                    the protocol — always loaded
references/investigation.md Phase 1 · repository investigation checklist
references/stack.md         Phase 2 · existing stack + brand, stack choice, location, deploy
references/design.md        Phase 4 · the design system
references/structure.md     Phase 5 · section structure and scroll narrative
references/review.md        Phase 6 · run it, look at it, fix it — plus the quality review
```

The references are progressive disclosure: each is opened at the phase that needs it, so the
model isn't reading a design checklist while it's still reading your source tree.

### The seven phases

| # | Phase | What happens |
|---|---|---|
| 1 | Investigate | Product identity, audience, capability inventory, hidden value, honest maturity |
| 2 | Assess the stack | Existing site/design system/brand; lightest viable stack; where the site lives |
| 3 | Position | One category, audience, problem, differentiator, value prop, 3–6 themes, 2 CTAs |
| 4 | Design | The design system, written down before any markup |
| 5 | Build | Section structure, scroll narrative, visual rhythm — as real source files |
| 6 | Verify | Run, render, inspect at three widths, fix, repeat; then the full quality review |
| 7 | README | A short entry point, written last |

**Phase 2 runs before any design work, deliberately.** If the repository already declares design
tokens, brand colors, or typefaces, *that is the product's visual identity* and the site inherits
it. Inventing a parallel palette is how you get a template with the right words on it — the skill
says so because that mistake was made first.

### Evidence classification

Every material claim is classified before it reaches the page, and the tier chooses the verb:

| Tier | Meaning | Language |
|---|---|---|
| Confirmed | Backed by code, tests, config, or current docs | supports · includes · provides · runs |
| Partial | Present but incomplete, gated, or lightly tested | *includes experimental support for…* |
| Planned | Only in a roadmap, issue, spec, or placeholder | labeled **planned**, never "available" |
| Unverified | Suggested but not supported | cut, or described cautiously |

Hard exclusions: customer counts, usage numbers, testimonials, customer logos, awards, press
mentions, unmeasured benchmarks, uptime or security guarantees, roadmap dates, stock photography,
fabricated screenshots, and dead placeholder links in the rendered page.

### Checks

```bash
python scripts/validate_skill.py
```

Verifies the bundle structurally — frontmatter and version, every `references/*.md` cited by
`SKILL.md` is shipped (and nothing ships orphaned), both installers fetch every reference,
in-document anchors resolve to real headings, and no file carries a UTF-8 BOM. Runs in CI on
every push and pull request. Stdlib only, Python 3.8+.

### This repository's own site

[`docs/index.html`](docs/index.html) was built with this skill, applied to this repository. One
static HTML file, no build step — which is what Phase 2 selects for a project made of six
Markdown files. It's served by GitHub Pages from `/docs` on `main`.

## Install

Works with Claude Code, Claude Cowork, or claude.ai (Skills enabled).

**Windows PowerShell:**

```powershell
iwr -useb https://raw.githubusercontent.com/scottconverse/landing-page/main/install.ps1 | iex
```

**macOS / Linux:**

```bash
curl -fsSL https://raw.githubusercontent.com/scottconverse/landing-page/main/install.sh | bash
```

Both copy `SKILL.md` and `references/` into `~/.claude/skills/landing-page/`. Re-run to update;
uninstall by deleting that folder.

**Manual:** clone this repo and copy `SKILL.md` and `references/` into
`~/.claude/skills/landing-page/`.

## Use

Say any of these to Claude:

- `/landing-page`
- "build a landing page for this repo"
- "make this repo look legit"
- "what does this project even do?"
- "write the pitch for this repo"

It also triggers on its own before a repository is announced, open-sourced, or released.

## Project status

Version 1.0.0 — first public release. Functional and in regular use; single author. Model-agnostic:
works with any Claude model (Opus, Sonnet, Haiku, Fable). It is a protocol, not a guarantee: output
quality depends on the model and on how much your repository reveals. The Verify phase does more
when the environment has a browser or renderer available, and the skill is required to say so when
it doesn't.

## License

[MIT](LICENSE) © 2026 Scott Converse
