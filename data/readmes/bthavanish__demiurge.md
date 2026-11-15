<div align="center">

# DEMIURGE

<img src="assets/demiurge.png" width="300" alt="demiurge">

All-in-one skill for building, auditing, critiquing, and hardening code.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## About

Demiurge is an AI coding skill that combines five disciplines into one workflow: lazy problem-solving (ponytail), terse output (caveman), human-sounding code (humanizer), frontend design sense, and strict coding standards. It works with TypeScript, JavaScript, C, C++, Python, Rust, Go, Java, Kotlin, Swift, Dart, HTML, CSS, and more.

It auto-detects what you want to do from natural language. Say what you need and it figures out the right approach.

## Installation

### Skills CLI (Recommended)

```bash
npx skills add bthavanish/demiurge
```

### Claude Code

```bash
/plugin marketplace add bthavanish/demiurge
/plugin install demiurge@demiurge
```

### Manual

Clone this repo and copy `skill/` into your agent's skills directory.

## Usage

```
/demiurge [mode] [target]
```

No mode needed. Type what you want:

```bash
/demiurge                              # full audit + ask which fixes to apply
/demiurge fix the security issues in my api   # context-gather for auth, fix it
/demiurge clean up this frontend code          # context-gather, humanize it
/demiurge make a settings page                 # build it
/demiurge what can I delete from this repo     # debt mode
```

Give an exact task and it context-gathers for that change. No context and it runs a full audit.

**UI guard:** UI references only load for apps with a UI. Backend/CLI/library apps skip UI modes automatically.

### Build

| Mode | Command | Description |
|------|---------|-------------|
| `make` | `/demiurge make [feature]` | Builds on user instructions using ponytail ladder + coding standards. |
| `design-material` | `/demiurge design-material [target]` | Material Design 3 builder. Explicit only, UI apps only. |

### Evaluate

| Mode | Command | Description |
|------|---------|-------------|
| `audit` | `/demiurge audit [target]` | Full codebase audit. Security, logic, dead code, style, architecture. |
| `audit-frontend` | `/demiurge audit-frontend [target]` | Frontend/UI/UX audit. Design tokens, a11y, responsive, anti-patterns. UI apps only. |
| `audit-backend` | `/demiurge audit-backend [target]` | Backend/logic/security audit. Injection, auth, error handling, type safety. |
| `critique` | `/demiurge critique [target]` | UX design review. Nielsen heuristics (/40), cognitive load, personas. UI apps only. |
| `review` | `/demiurge review [target]` | One-line code review. Severity-tagged: bug, risk, nit, q. |

### Refine

| Mode | Command | Description |
|------|---------|-------------|
| `secure-code` | `/demiurge secure-code [target]` | Fixes bugs, vulnerabilities, logic errors, dead code directly. |
| `humanize` | `/demiurge humanize [target]` | Detects AI patterns in code and rewrites to sound human. |
| `polish` | `/demiurge polish [target]` | Final quality pass. Typography, spacing, color, motion, copy. UI apps only. |
| `harden` | `/demiurge harden [target]` | Production-readiness. Error handling, i18n, edge cases. |
| `bolder` | `/demiurge bolder [target]` | Amplifies bland designs. More decisive and committed. UI apps only. |
| `quieter` | `/demiurge quieter [target]` | Tones down aggressive or overstimulating designs. UI apps only. |

### Manage

| Mode | Command | Description |
|------|---------|-------------|
| `debt` | `/demiurge debt [target]` | Harvests `ponytail:` comment markers into a debt ledger. |
| `compress` | `/demiurge compress [filepath]` | Compresses natural language files to save tokens. |
| `commit` | `/demiurge commit` | Generates terse conventional commit messages. |

### Docs

| Mode | Command | Description |
|------|---------|-------------|
| `docs` | `/demiurge docs [target]` | Writes or restructures documentation using Diataxis framework. |
| `readme` | `/demiurge readme [target]` | Creates or improves README files with audience-specific templates. |
| `prose` | `/demiurge prose [target]` | Edits machine-generated prose to remove AI writing tropes. |

## Base Rules

Every mode applies these rules:

- **Ponytail ladder** -- simplest solution first. YAGNI. Reuse before building.
- **Caveman output** -- terse output, full accuracy. Code blocks preserved verbatim.
- **Humanizer** -- no AI slop in code or prose. No em dashes, no rule-of-three, no AI vocabulary.
- **Coding standards** -- KISS, SRP, descriptive names, no magic numbers, immutability, portable, no hallucinations.
- **Comment standards** -- why not what, no dead code, no metadata, ponytail markers for shortcuts.
- **DESIGN.md enforcement** -- follow the design system if one exists.
- **Modularity** -- small, cohesive, loosely coupled functions. Dependencies flow one direction.
- **No hardcoding** -- env vars, config files, constants, parameters.
- **Always ask before fixing.** Never auto-fix without presenting findings and getting user confirmation.

## Supported Agents

Demiurge works with multiple AI coding agents through adapter directories:

| Agent | Adapter Directory |
|-------|-------------------|
| Claude Code | `.claude/skills/demiurge/` |
| OpenCode | `.opencode/skills/demiurge/` |
| Cursor | `.cursor/skills/demiurge/` |
| Gemini | `.gemini/skills/demiurge/` |
| Kiro | `.kiro/skills/demiurge/` |
| Trae | `.trae/skills/demiurge/` |
| Trae CN | `.trae-cn/skills/demiurge/` |
| Pi | `.pi/skills/demiurge/` |
| Qoder | `.qoder/skills/demiurge/` |
| Rovo Dev | `.rovodev/skills/demiurge/` |
| Generic | `.agents/skills/demiurge/` |
| Codex | `.codex/skills/demiurge/` |

## Credits

Built on work from the security and developer tools community.

### Core Skills

| Skill | Author | Repository |
|-------|--------|------------|
| **caveman** | Julius Brussee | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) |
| **humanizer** | blader | [blader/humanizer](https://github.com/blader/humanizer) |
| **impeccable** | pbakaus | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) |
| **ponytail** | Dietrich Gebert | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
| **material-3-skill** | hamen | [hamen/material-3-skill](https://github.com/hamen/material-3-skill) |
| **maintainable-typescript & write-good-docs** | miguelspizza | [miguelspizza/skills](https://github.com/miguelspizza/skills) |

### Security and Analysis

40 skills from the [Trail of Bits skills collection](https://github.com/trailofbits/skills). Security audit methodologies, vulnerability patterns, and analysis techniques.

### Additional References

| Source | What We Took |
|--------|--------------|
| [Trail of Bits Testing Handbook](https://appsec.guide) | Security testing methodologies, tool configurations, vulnerability detection techniques |
| [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | 33 AI writing patterns for the humanizer skill |

## License

MIT. Copyright 2026 Thavanish brijesh.

Third-party references are used under their respective licenses. See individual repositories for details. Most Trail of Bits skills use the [MIT License](https://github.com/trailofbits/skills/blob/main/LICENSE).
