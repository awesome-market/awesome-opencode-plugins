<p align="center">
  <img src="logo/ariadne-hero.svg" alt="Ariadne — the thread through the labyrinth of your product vision" width="100%">
</p>

<p align="center">
  <a href=".github/workflows/validate.yml"><img alt="CI" src="https://github.com/jbalint/ariadne-product-discovery/actions/workflows/validate.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-2ea44f"></a>
  <a href="agents"><img alt="OpenCode V2" src="https://img.shields.io/badge/OpenCode-V2-11162A"></a>
  <a href="claude"><img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-D97757"></a>
  <a href="skills"><img alt="DeepSeek Harness" src="https://img.shields.io/badge/DeepSeek%20Harness-skills-4D6BFE"></a>
  <img alt="Status: early (0.x)" src="https://img.shields.io/badge/status-early%20(0.x)-E8B04B">
</p>

<p align="center">
  <strong>Your AI coding agent is a great builder and a terrible product manager.</strong><br>
  Ariadne is the product-discovery front-end that runs before code, so the agent stays
  faithful to your intent instead of treating the current codebase as the spec.
</p>

> **Status: early (0.x).** The prompts and artifact format may change between minor versions. Failure reports are very welcome.

---

## The problem

AI coding agents are extraordinary at turning a clear specification into working code. They are bad at finding out what the specification should be.

Ask one to "add an upload flow" and it will produce a plausible upload flow — modeled on whatever the codebase already does, whatever pattern is most common on the internet, and whatever makes the implementation look complete. Requirements get invented to fill gaps. Assumptions get presented as decisions. The current implementation quietly becomes the specification, and you discover the mismatch after the code exists.

The cost is not the code. It is that **the wrong thing gets built quickly, and then defended**. Reviewing generated code for product fidelity is much harder than discovering intent up front.

## What Ariadne does

Ariadne is a three-stage product-discovery pipeline for AI coding agents. Each stage is a separate agent, and each leaves a Markdown artifact you can read, diff, and hand to the next stage.

```
  .ariadne/discovery.md        .ariadne/audit.md         .ariadne/plan.md
  ┌──────────────────┐        ┌─────────────────┐       ┌────────────────┐
  │    DISCOVER      │───────▶│      AUDIT      │──────▶│   ARCHITECT    │
  │  what & why      │        │  is it sound?   │       │  how to build  │
  └──────────────────┘        └─────────────────┘       └────────────────┘
     interviews you            prior art, novelty         repo-aware plan
     finds the workflow        risks, alternatives        thin vertical slices
```

- **Discover** (`ariadne-discover`) — interviews you like a product manager would, converting "this feels awkward" into a canonical workflow, an explicit requirements register, usability gaps, and prioritized open questions.
- **Audit** (`ariadne-audit`) — stress-tests the resulting idea against prior art, novelty, architecture, failure modes, and the strongest competing design.
- **Architect** (`ariadne-architect`) — maps the clarified vision onto the actual repository and produces an implementation-ready plan without writing code.

Use all three, or just Discover — it works alone.

## See it in action

```
You:      The upload flow feels awkward. I expected it to just work.

Ariadne:  What is the user trying to accomplish at that moment?
          (Uncertainty: is "awkward" about the number of steps, the
          wording, or the lack of feedback while it runs?)

You:      They already picked the file. Asking them to confirm again is silly.

Ariadne:  → R7 (latent, high confidence): once a file is selected, the system
            begins the upload without a second confirmation; the user can
            cancel while it runs.
          → C2 (conflict): the current "Review & upload" step exists because
            the API needs a separate commit call. That is an implementation
            artifact, not product intent.
          → Q3 (open): what must remain visible during the upload, and what
            should happen on failure?

          I've written these to .ariadne/discovery.md. Two questions before
          I update the canonical workflow...
```

No code. No architecture. A requirement was extracted, an implementation artifact was named, and an assumption was not silently promoted to a decision.

## Why Ariadne

- **Intent before implementation.** The agent is explicitly forbidden from writing code, producing patches, or turning the session into an engineering plan.
- **Interviewing, not document generation.** It asks small batches of focused questions tied to concrete workflow moments. It does not dump a giant questionnaire or invent requirements to look complete.
- **Five-way epistemic hygiene.** Every claim is tagged **Observed**, **Stated**, **Inferred**, **Uncertain**, or **Conflicting**, with confidence and evidence. Inferences are never presented as settled requirements.
- **Contradictions stay visible.** It surfaces incompatible product models and asks you to choose — rather than picking one and moving on.
- **Explicit anti-convergence.** It assumes the current implementation may have accidentally shaped your workflow, and asks what must remain true even if the interface changes completely.
- **A real artifact.** Every round updates a living `.ariadne/discovery.md`, so the deliverable is tangible and the next stage has something to consume.
- **Tool-agnostic.** Native OpenCode agents, a Claude Code plugin, Agent Skills for DeepSeek Harness and other skill-aware tools, and a plain prompt you can paste anywhere.

## How it compares

Spec-driven development tools such as [GitHub Spec Kit](https://github.com/github/spec-kit), [Kiro](https://kiro.dev) specs, and the [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) formalize intent you already have into specs and tasks. Ariadne runs **before** them: it finds out what the intent is, so the spec they formalize is yours and not a rationalization of the current code.

| | **Ariadne** | Spec Kit / Kiro specs | BMAD Method | "Write me a PRD" prompt |
|---|---|---|---|---|
| Primary job | find out intent | formalize intent into spec → plan → tasks | agile multi-agent delivery | one-shot document |
| Runs before a spec exists | ✅ | ⚠️ assumes you can state it | ⚠️ analyst phase | ⚠️ |
| Interviews instead of generating | ✅ | ⚠️ clarify step | ⚠️ | ❌ |
| Tags observed / stated / inferred / uncertain / conflicting | ✅ | ❌ | ❌ | ❌ |
| Surfaces contradictions instead of resolving them | ✅ | ⚠️ open questions | ❌ | ❌ |
| Resists converging on the current implementation | ✅ | ❌ | ❌ | ❌ |
| Produces a living artifact a spec tool can consume | ✅ | ✅ spec | ✅ PRD | ⚠️ |

See [`docs/comparison.md`](docs/comparison.md) for the longer version.

## Install

### Claude Code (plugin)

```
/plugin marketplace add jbalint/ariadne-product-discovery
/plugin install ariadne@ariadne-product-discovery
```

The plugin adds the three agents, the `/ariadne:discover`, `/ariadne:audit` and `/ariadne:architect` commands, and a hook that keeps Ariadne agents from writing outside `.ariadne/`.

### OpenCode

```sh
curl -fsSL https://raw.githubusercontent.com/jbalint/ariadne-product-discovery/v0.3.0/install.sh | sh -s -- --opencode
```

Or from a clone:

```sh
git clone https://github.com/jbalint/ariadne-product-discovery.git
cd ariadne-product-discovery
./install.sh --opencode
```

| Flag | Effect |
|---|---|
| `--opencode` | Install the three agents into `~/.config/opencode/agents/` |
| `--claude` | Install the three slash commands into `~/.claude/commands/` (no tool limits; prefer the plugin) |
| `--dsh` | Install the three skills into `~/.dsh/skills/` (no tool limits) |
| `--all` | All three. With no tool flag, the installer does `--opencode --claude` |
| `--dry-run` | Print what would be written, change nothing |
| `--uninstall` | Remove Ariadne; leaves `.ariadne/` project artifacts alone |

The curl installer downloads the tagged release named in its URL. Set `ARIADNE_REF=<tag>` to choose another.

### DeepSeek Harness (dsh)

```sh
curl -fsSL https://raw.githubusercontent.com/jbalint/ariadne-product-discovery/v0.3.0/install.sh | sh -s -- --dsh
```

This installs the three stages as [Agent Skills](https://agentskills.io) under `~/.dsh/skills/` (or `$DSH_HOME/skills/`). To scope them to one project instead, copy `skills/ariadne-*` into that project's `.agents/skills/`.

### Anything else

[`skills/`](skills) holds each stage as an [Agent Skill](https://agentskills.io) (`SKILL.md`), for tools that load skills. For anything else (Cursor, Windsurf, a chat window), copy the body of the relevant file in `agents/`, drop the YAML frontmatter, and use it as the system prompt, custom mode, or rule.

## Quick start

**Claude Code.** Run the stage as the session's agent, so its tool limits apply:

```sh
claude --agent ariadne:discover
```

Then describe what you are building:

```
I'm building a CLI that turns a folder of screenshots into a design spec.
The current version technically works but the flow feels clunky.
```

`/ariadne:discover <subject>` works inside an ordinary session too, but then it runs with that session's tools (see [Permissions](#permissions)).

**OpenCode.** Open the agent picker, choose `ariadne-discover`, and describe what you are building.

**DeepSeek Harness.** Type `/ariadne-discover` followed by what you are building, then `/ariadne-audit` and `/ariadne-architect` for the later stages.

Then follow the pipeline:

```sh
claude --agent ariadne:audit      # once discovery.md reflects your intent
claude --agent ariadne:architect  # once the idea has survived the audit
```

## How it works

Ariadne maintains a five-section living document at `.ariadne/discovery.md`:

1. **Product intent** — who it is for, the job, the feel, the emerging principles.
2. **Canonical workflow** — the happy path plus meaningful alternates and recovery paths, stage by stage.
3. **Requirements register** — explicit vs. latent, with evidence, confidence, and status.
4. **Usability gaps** — current vs. intended behavior, and which principle each gap violates.
5. **Open questions** — prioritized by leverage, with the evidence that would resolve each one.

Every round follows the same loop:

> state the current belief → name the most consequential uncertainty → ask 2–3 focused questions → update the document → report what changed

When evidence conflicts, it uses a fixed priority: **your clarified intent** → observable user goals → documented product decisions → current behavior → incidental implementation details. The current behavior is fourth, not first, on purpose.

## The three agents

| Agent | Mode | Writes | Job |
|---|---|---|---|
| `ariadne-discover` | primary | `.ariadne/discovery.md` | Interview you into a precise product intent and workflow |
| `ariadne-audit` | primary | `.ariadne/audit.md` | Prior art, novelty map, risks, alternatives |
| `ariadne-architect` | primary | `.ariadne/plan.md` | Repo-aware plan: slices, tasks, acceptance criteria |

### Permissions

Each agent can write only under `.ariadne/`. Discovery cannot edit code or run shell commands. The architect can inspect the repo but must ask before running shell commands.

| | Tool limits | Writes limited to `.ariadne/` |
|---|---|---|
| OpenCode agents | ✅ `permissions` block | ✅ `permissions` block |
| Claude Code, `claude --agent ariadne:<stage>` | ✅ agent `tools:` list | ✅ plugin `PreToolUse` hook |
| Claude Code, `/ariadne:<stage>` in an ordinary session | ❌ the session's tools | ❌ the prompt asks; nothing enforces it |
| DeepSeek Harness skills | ❌ the session's tools | ❌ the prompt asks; nothing enforces it |
| Installed commands, other Agent Skills hosts, pasted prompt | ❌ | ❌ the prompt asks; nothing enforces it |

dsh has no per-path write guard to hook into. Its agent presets compose tools, but its own docs say they are not security boundaries. Until it gains such a guard, keep the dsh session's permission mode as narrow as you are comfortable with.

## Design principles

Ariadne is built on a few opinions worth stating plainly:

- **The product owner is the source of truth, not the codebase.** Existing behavior is evidence, not intent.
- **Uncertainty is information.** A marked unknown is more valuable than a confident guess.
- **Fewer, better questions.** A small batch tied to a concrete moment beats a comprehensive questionnaire.
- **The deliverable is understanding, not a document.** The Markdown is a byproduct of getting the model right.
- **Discovery ends when you recognize your own vision**, not when the template is full.

## Roadmap

- [x] Three-stage pipeline with per-stage artifacts
- [x] OpenCode agents + Claude Code commands
- [x] Claude Code plugin with enforced tool and write limits
- [x] Agent Skills port
- [ ] Session memory across discovery rounds
- [ ] Structured YAML/JSON output for downstream agents
- [ ] Issue-tracker import (seed discovery from existing tickets)
- [ ] Cursor rules and other ports beyond Agent Skills
- [ ] Example gallery from real sessions

See [`docs/roadmap.md`](docs/roadmap.md) for details.

## Documentation

- [`docs/examples.md`](docs/examples.md) — full worked sessions
- [`docs/methodology.md`](docs/methodology.md) — the reasoning discipline in depth
- [`docs/comparison.md`](docs/comparison.md) — positioning against adjacent tools
- [`docs/roadmap.md`](docs/roadmap.md) — what is next

## Contributing

Issues and pull requests are welcome. The most useful contributions are **real discovery transcripts** (with anything sensitive removed) and **failure cases** where the agent converged too early or accepted an implementation artifact as a requirement. Both have [issue forms](https://github.com/jbalint/ariadne-product-discovery/issues/new/choose). See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT — see [`LICENSE`](LICENSE).
