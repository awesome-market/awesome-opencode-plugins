# hook-everything

[![CI](https://github.com/Vumb-VibeCoder/hook-everything/actions/workflows/ci.yml/badge.svg)](https://github.com/Vumb-VibeCoder/hook-everything/actions/workflows/ci.yml)
![Version](https://img.shields.io/badge/version-5.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Skills](https://img.shields.io/badge/skills-13-orange)

Skills that help an AI assistant write copy people actually want to read, and design flows people actually want to finish. It also ships a small scanner that tells you when a text sounds like a machine wrote it.

The test I apply to everything here: if the reader saw your design notes, would they still trust the page?

## Quickstart (2 minutes)

**1. Install the skills**

Claude Code plugin (easiest):

```text
/plugin marketplace add Vumb-VibeCoder/hook-everything
/plugin install hook-everything@hook-everything
```

Or copy the files by hand:

```bash
git clone https://github.com/Vumb-VibeCoder/hook-everything.git
cd hook-everything

# Claude Code
mkdir -p .claude/skills .claude/tools
cp -r skills/* .claude/skills/
cp -r tools/* .claude/tools/
```

For Cursor, Windsurf, Codex or other agents, copy `AGENTS.md` into your project root (or append it to `.cursorrules` / `CLAUDE.md`) and keep `skills/` and `tools/` in the workspace.

**2. Ask your assistant**

```text
Rewrite this product announcement so it sounds human, then check it with the scanner.
```

**3. Check any text yourself**

```bash
python3 tools/slop_scan.py draft.txt --fix-hints
```

You get a score from 0 to 100 and a list of what to rewrite. Aim for 15 or lower. Needs Python 3.10+ and nothing else.

## Which skills does my task need?

| I want to... | Skills (in order) |
|---|---|
| Humanize or clean up a text in any language | `anti-slop` → `self-review` → `value-check` |
| Write a short email, release note or headline | `writing-hooks` → `anti-slop` → `self-review` → `value-check` |
| Write an essay, article or newsletter | `audience-calibration` → `trust-architecture` → `hook-compounding` → `writing-hooks` → `anti-slop` → `self-review` → `value-check` |
| Build a landing page, ad or outreach sequence | `market-intelligence` → `audience-calibration` → `trust-architecture` → `hook-compounding` → `marketing-hooks` → `visual-ux-hooks` → `anti-slop` → `self-review` → `value-check` |
| Design onboarding or a product flow | `psychology-map` → `trust-architecture` → `visual-ux-hooks` → `hook-compounding` → `product-hooks` → `value-check` |
| Find fresh angles and ideas | `market-intelligence` → `creative-ideation` → `hook-compounding` → `anti-slop` → `self-review` → `value-check` |

Short edits use the **Lite Lane** (2 to 3 skills). Campaigns and new products use the **Full Lane**. Details are in `AGENTS.md`.

## The 13 skills

| Skill | What it does |
|---|---|
| `psychology-map` | 30 behavior mechanisms, each rated by evidence strength |
| `trust-architecture` | Builds trust before asking for anything |
| `market-intelligence` | Reads live reviews and competitor gaps, and drops forced trend-jacking |
| `audience-calibration` | Matches speed, tone and proof to the reader |
| `creative-ideation` | Throws out the first obvious ideas and combines unrelated ones |
| `hook-compounding` | Layers 3 to 4 mechanisms into one hook |
| `visual-ux-hooks` | Layout, contrast, choice limits and response timing |
| `marketing-hooks` | Conversion copy without fake urgency or inflated claims |
| `writing-hooks` | Openers and mid-article retention |
| `product-hooks` | Onboarding, habits and humane offboarding |
| `anti-slop` | 85 rules for natural, non-hype writing |
| `self-review` | Rereads a draft as a native reader in any language and rewrites it if it still sounds machine-made |
| `value-check` | 13-point ethics and quality gate before you ship |

## Scanner cheatsheet

```bash
# Score a file and get rewrite hints
python3 tools/slop_scan.py draft.txt --fix-hints

# Scan a doc that quotes banned phrases on purpose
python3 tools/slop_scan.py skills/anti-slop/SKILL.md --strip-markdown

# Fail a CI job when the score is above 15
python3 tools/slop_scan.py README.md --max-score 15

# Report invisible Unicode (zero-width, U+202F, bidi, tag block, lookalikes)
python3 tools/slop_scan.py draft.txt --hidden

# Write a cleaned copy, or fail a CI job if any hidden character is found
python3 tools/slop_scan.py draft.txt --clean draft.clean.txt
python3 tools/slop_scan.py draft.txt --fail-on-hidden

# JSON output, or run the built-in tests
python3 tools/slop_scan.py draft.txt --json
python3 tools/slop_scan.py --selftest
```

## Do AI models watermark their text?

Claude does, but not with characters. Anthropic says its watermark biases word choice using a secret key, adds no hidden characters, and can only be checked by someone holding the key. So no local tool can detect or strip it, this scanner included. ChatGPT text sometimes carries odd spaces such as U+202F, but those also come from copy-paste and are weak evidence. `--hidden` finds and removes invisible characters from any source. Sources and caveats are in `research/WATERMARKS.md`.

The 15-point threshold is a working heuristic for dense clusters of AI and marketing tropes. It does not prove who wrote a text.

## Repository layout

```text
hook-everything/
├── AGENTS.md        # Routing rules for agents
├── SKILL.md         # Root skill manifest
├── skills/          # The 13 skills
├── tools/           # slop_scan.py
├── tests/           # unittest suite
├── research/        # Sources, evidence ratings, watermark notes
└── examples/        # Before/after rewrites
```

## Contributing

Run the checks before a pull request:

```bash
python3 tools/slop_scan.py --selftest
python3 -m unittest discover -s tests
```

See `CHANGELOG.md` for version history. Licensed under MIT.
