# Humanize Writing

An agent skill that rewrites drafts to remove AI tells, cut defensive language, and sound human. Supports matching a persistent user style profile built from historical writing samples.

Primarily for English prose: papers, stories, emails, reports, or any text that currently feels machine-generated or over-defensive.

## What it does

- Scans for common AI writing tells (delve, tapestry, not-X-but-Y, uniform sentence length, throat-clearing openers, empty emphasis, etc.)
- **Cuts defensive language**: stacked hedges, preemptive apologies, self-disqualification, reader management, reflexive limitations, and assistant-style boilerplate
- **Separates calibrated caution from defensive protection**: keeps evidence-linked uncertainty and required disclosures, removes the self-protection
- Rewrites while preserving meaning, facts, intent, and claim strength
- Varies sentence rhythm deliberately
- Prefers plain, spoken-like language
- Optionally loads and matches a persistent user style profile
- Handles academic and narrative genres with different playbooks

## Why defensive language matters (new in 0.2.0)

Defensive language is one of the strongest AI tells, and the one most likely to survive a normal "humanize" edit. It looks like caution but functions as self-protection: "it is important to note", "may potentially suggest", "though this is only a preliminary observation", "I may be wrong, but", "you might wonder why". In a paper it makes the authors sound unsure of their own work; in a story it makes the narrator explain the scene before it has earned anything.

The skill removes the performance of caution without inflating the claim. For example:

> **Before**: Although this study may potentially offer some tentative insights, it is important to note that the findings should be interpreted with caution, and further research is needed.
>
> **After**: The cross-sectional design cannot establish temporal order, so the findings describe an association, not a causal effect.

The hedge is not deleted. It is converted into a specific sentence about the design. See [`references/defensive-language.md`](references/defensive-language.md) for the full taxonomy (A–J), genre playbooks, boundaries, and verification checklist.

## Structure

- `SKILL.md` — Core workflow, focused defensive-language pass, rules, and resources
- `references/defensive-language.md` — Defensive-language taxonomy, calibrated-vs-defensive test, academic/narrative/email playbooks, boundaries, checklist
- `references/ai-tells.md` — English AI tells and preferred alternatives
- `references/style-profile.md` — How to create, store, update, and apply a persistent style profile
- `references/examples.md` — Before/after pairs, including defensive academic and defensive narrative examples
- `evals/evals.json` — Skill behavior test cases (including defensive-language cases)
- `evals/triggers.json` — Trigger phrase tests (English and Chinese)
- `evals/validate_skill.py` — Static validator for skill structure, links, and required content
- `evals/acceptance/` — Blind acceptance harness: unseen cases, rubric, protocol, staging script, generated outputs, metric checker, and independent verifier report
- `ACCEPTANCE.md` — Acceptance report with the frozen case hash, results, and known limitations
- `assets/example-style-profile.md` — Sample style profile

## Install

Copy or symlink this folder into your agent's skills directory. For a DeepSeek Harness profile:

```bash
git clone https://github.com/east18047-zmjjkk/humanize-writing.git ~/.dsh/skills/humanize-writing
```

For other agents, use their skill directory (for example `~/.claude/skills/humanize-writing`). The skill is plain Markdown and has no runtime dependencies beyond Python for the optional validators.

## Usage

Tell the agent:

- "Rewrite this draft to remove the AI flavor"
- "Humanize this paragraph"
- "Edit this to match my usual writing style"
- "Make this academic section sound less AI-generated"
- "Cut the defensive hedging in this Discussion section, but keep the real limitations"
- "This paragraph sounds like it's apologizing for itself; make it direct"
- "Reduce the defensive language in this narrative without changing the character's voice"
- "减少防御性语言，别让审稿人一眼看出是 AI 写的"

Provide 300–800 words of your own writing the first time so the agent can build a style profile. Later rewrites will match it automatically.

## Quality gates

The skill applies these gates to defensive-language work:

- Defensive markers cut by at least half, or down to ≤2 per 500 words
- Numbers, units, citations, names, dates, and disclosures preserved
- Every remaining hedge points to a reason the reader can see
- No claim upgraded (association stays association; single study stays single study)
- Required disclosures (ethics, consent, COI, funding, data availability, AI use) preserved
- If a text is already well calibrated, minimal edits or none

## Validation and acceptance

Static validation:

```bash
python3 evals/validate_skill.py
```

Blind behavioral acceptance:

```bash
python3 evals/acceptance/stage_blind.py --out /tmp/humanize-writing-blind
# run the rewriter on the blind copy, copy outputs back, then:
python3 evals/acceptance/check_outputs.py
```

The frozen blind run passes **4/4** automated cases, and the independent verifier rates the result **PASS** (aggregate 4.92/5, no hard-gate failures; 0 blockers after documentation corrections). Full scores, the case hash, round history, and residual risks are in [`ACCEPTANCE.md`](ACCEPTANCE.md). The behavioral test uses an independent rewriter plus a separate verifier agent so the result is not just the author's self-assessment; the first verifier review failed an earlier target-fitted case set, and that report is retained for audit.

## Status

Version 0.2.0 (2026-11-03). Initial version 0.1.0 shipped 2026-11-03. Focused on English draft rewriting with optional persistent style matching; defensive-language reduction added in 0.2.0. Static validation passes (186 checks), the frozen blind behavioral run passes 4/4, and the independent verifier verdict is **PASS** (4.92/5); details and residual risks are in [`ACCEPTANCE.md`](ACCEPTANCE.md).
