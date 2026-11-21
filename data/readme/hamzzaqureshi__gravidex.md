# GraviDex

[![Capabilities](https://img.shields.io/badge/capabilities-21%20active-success.svg)](./CAPABILITIES/capability-registry.yaml)
[![Tests](https://img.shields.io/badge/tests-29%2F29%20passed%20(100%25)-brightgreen.svg)](./test_all.py)
[![Dependencies](https://img.shields.io/badge/dependencies-zero%20(stdlib)-success.svg)](#system-requirements--prerequisites)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Antigravity%20%7C%20OpenCode%20%7C%20Claude%20Code-purple.svg)](#quickstart--installation-tracks)

> A curated, modular capability library for Google Antigravity IDE, OpenCode, and Claude Code. Built on the Python standard library with zero runtime dependencies.

[CAPABILITIES](./CAPABILITIES/capability-registry.yaml) • [INSTALLATION](#quickstart--installation-tracks) • [SHARING](./SHARING.md) • [CONTRIBUTING](./CONTRIBUTING.md) • [LICENSE](./LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Architecture & Data Flow](#architecture--data-flow)
- [The 21 Active Capabilities Matrix](#the-21-active-capabilities-matrix)
- [System Requirements & Prerequisites](#system-requirements--prerequisites)
- [Quickstart & Installation Tracks](#quickstart--installation-tracks)
  - [Interactive Setup (Recommended)](#interactive-setup-recommended)
  - [Track 1: Google Antigravity IDE](#track-1-google-antigravity-ide)
  - [Track 2: Claude Code CLI](#track-2-claude-code-cli)
  - [Track 3: OpenCode CLI](#track-3-opencode-cli)
  - [Track 4: Project-Local Workspace](#track-4-project-local-workspace)
- [Packaging & Sharing](#packaging--sharing)
- [Unified Verification Harness](#unified-verification-harness)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

AI coding agents often struggle with four common failure modes: agreeing with broken code without executing verification tests, defaulting to cluttered visual interfaces with generic glow effects, introducing unnecessary third-party dependencies for single-line changes, and loading dozens of overlapping skills that exhaust the context window.

GraviDex is designed for developers, engineering teams, and autonomous agents to solve these problems. It replaces hundreds of loose, conflicting skill files with a curated library of 21 modular capabilities (8 domain packs and 13 focused specialist tools). Each capability follows progressive disclosure: the agent loads a compact entry point first, reading deeper reference guides and executing sandboxed tools only when needed.

---

## Architecture & Data Flow

GraviDex organizes capabilities into two distinct scopes. When an agent receives a prompt, it resolves the required capability from the central registry, reviews the compact guidelines in `SKILL.md`, and pulls targeted references on demand:

```text
+-------------------------------------------------------------------------+
|                              USER PROMPT                                |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  AGENT HARNESS (Antigravity / Claude / OpenCode)        |
+-------------------------------------------------------------------------+
                                     |
                    Resolves capability from registry
                                     |
                                     v
+-------------------------------------------------------------------------+
|                          GRAVIDEX CAPABILITIES                          |
|                                                                         |
|  Curated Capability Packs (8)          Retained Specialists (11)        |
|  ├── autonomous-agent-engineering      ├── agentshield   ├── rev-engineer|
|  ├── backend-engineering               ├── asd-ste100    ├── scrapling   |
|  ├── design-systems                    ├── awwwards      ├── skillforge  |
|  ├── frontend-engineering              ├── boardui                       |
|  ├── interface-design                  ├── jury                          |
|  ├── quality-engineering               ├── last30days                    |
|  ├── security-audit                    ├── lemo-opuscar                  |
|  └── technical-documentation           └── motionsites-web-builder       |
+-------------------------------------------------------------------------+
         |                                           |
         v                                           v
+-----------------------------+             +-----------------------------+
|   Progressive Disclosure    |             |   Pure Python / Zero Pip    |
|   SKILL.md  ──▶ references/  |             |   Deterministic execution   |
|             ──▶ scripts/    |             |   Verified by test_all.py   |
+-----------------------------+             +-----------------------------+
```

### Directory Structure

```text
gravidex/
├── CAPABILITIES/                             # Active Capability Library
│   ├── capability-registry.yaml              # Central registry of all 21 capabilities
│   ├── curated/                              # Curated domain packs (8 packs)
│   │   ├── autonomous-agent-engineering/
│   │   ├── backend-engineering/
│   │   ├── design-systems/
│   │   ├── frontend-engineering/
│   │   ├── interface-design/
│   │   ├── quality-engineering/
│   │   ├── security-audit/
│   │   └── technical-documentation/
│   └── retained-specialists/                 # Independent specialist tools (13 tools)
│       ├── agentshield/
│       ├── asd-ste100/
│       ├── awwwards/
│       ├── boardui/
│       ├── jury/
│       ├── karpathy-guidelines/
│       ├── last30days/
│       ├── lemo-opuscar/
│       ├── motionsites-web-builder/
│       ├── rev-engineer/
│       ├── scrapling/
│       ├── skillforge/
│       └── stageshow/
├── .agents/skills/                           # Pre-synchronized Antigravity workspace skills
├── .claude/skills/                           # Pre-synchronized Claude Code workspace skills
├── .opencode/skills/                         # Pre-synchronized OpenCode workspace skills
├── install.sh                                # Cross-platform shell installer
├── install.py                                # Standard library Python installer
├── package.py                                # Archive and release packager
└── test_all.py                               # 31-suite parallel verification harness
```

Capabilities are organized into two tiers:

- Eight curated capability packs consolidate broad disciplines, including frontend architecture, backend services, and autonomous agent orchestration, into single entry points backed by structured reference guides.
- Thirteen retained independent specialists provide focused, single-purpose tools for security analysis, controlled language validation, faux UI choreography, web scraping, reverse engineering, and cinematic rendering.

---

## The 21 Active Capabilities Matrix

| Capability ID | Category | Core Workflows & Integrated Disciplines |
| :--- | :---: | :--- |
| **`autonomous-agent-engineering`** | Curated Pack | Minimal diff discipline (Ponytail), 14-domain self-interrogation (Socratic), multi-agent deliberation (Court, Arena), model routing & 429 failover (Model Router), Impeccable lifecycle, ECC memory vault. |
| **`backend-engineering`** | Curated Pack | Production API design, Express/Next.js API routes, cross-language error handling (TS/Python/Go), and Model Context Protocol (MCP) server architecture. |
| **`design-systems`** | Curated Pack | Design token foundations (TypeUI 67 themes), Sanzo Wada Japanese color matrix (348 palettes), SVG brand identity (Logo Design), and editorial diagramming (Diagram Design). |
| **`frontend-engineering`** | Curated Pack | React/Next.js component architecture, state management, render optimization, Three.js WebGL scenes, and Playwright browser QA. |
| **`interface-design`** | Curated Pack | Apple Human Interface Guidelines (HIG), UI/UX Pro Max rules (22 frameworks), 9-pass anti-slop redline craft, and taste motion calibration. |
| **`quality-engineering`** | Curated Pack | Test-driven development (TDD guide, 80%+ coverage), empirical verification gates (Rigor), E2E automation, and formal evaluation harness. |
| **`security-audit`** | Curated Pack | OWASP Top 10 vulnerability hunting, coverage ledgers, AST security analysis, and static security reviews. |
| **`technical-documentation`** | Curated Pack | README-driven development (50-point rubric), Architectural Decision Records (ADRs), codebase onboarding guides, and git collaboration workflows. |
| **`agentshield`** | Specialist | Hardened security auditor for agent harnesses, MCP configurations, hook safety, and prompt injection detection. |
| **`asd-ste100`** | Specialist | Simplified Technical English (Issue 9) & Karpathy 80% Pragmatic Mode. Zero-ambiguity agent instructions, tool schemas, 4 cognitive modalities, and deterministic Python linter. |
| **`awwwards`** | Specialist | Award-caliber site builder from one-line prompts. Art direction, typography, motion choreography, WebGL (OGL), page transitions, and browser QA to Awwwards Site of the Day bar. |
| **`boardui`** | Specialist | React design system for agentic interfaces: 69 source components, 400+ semantic tokens, React Aria accessibility, Tailwind CSS v4, RTL/direction support, and agent design rules. |
| **`jury`** | Specialist | Objective website scoring the way an Awwwards jury would. Blind critic model, automated audits (LCP, CLS, FPS, axe a11y, hover feedback, SEO), ranked fixes. |
| **`karpathy-guidelines`** | Specialist | Behavioral guidelines to reduce common LLM coding mistakes: 4 core pillars (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution) and pitfall prevention. |
| **`last30days`** | Specialist | Real-time cross-platform social consensus, crowd pulse, and temporal research engine. |
| **`lemo-opuscar`** | Specialist | Algorithmic film directing and production engine: 67 styles, Canvas/WebGL deterministic rendering, Kokoro TTS voice, procedural audio, and director manual. |
| **`motionsites-web-builder`** | Specialist | Award-level cinematic landing page engine, 40 prompt examples, media shelf (50+ videos, 30 cutouts), 55+ motion recipes, and Playwright screenshot QA loop. |
| **`rev-engineer`** | Specialist | Reverse engineering binary router and deconstruction tools for native, web, and packaged targets. |
| **`scrapling`** | Specialist | Adaptive web scraping, stealth browsing, and anti-bot bypass. |
| **`skillforge`** | Specialist | Autonomous agent skill lifecycle management, specification generation, regression testing, and ecosystem doctor. |
| **`stageshow`** | Specialist | Faux product UI engine: interactive React components, cursor arcs, Dynamic Island/macOS chrome geometry, and contact-sheet frame verification. |

---

## System Requirements & Prerequisites

| Package | Minimum Version | Necessity | Purpose |
| :--- | :--- | :--- | :--- |
| **Python** | 3.10+ | **Mandatory** | Core runtime for linters, inspectors, and parallel test harness. |
| **Bash** | 4.0+ | Optional | Shell installer (`install.sh`). |
| **Node.js** | Node 18+ | Optional | Only needed if executing live AST validators in `secure-audit` or `rev-engineer` MCP. |

> [!NOTE]
> There are zero external dependencies or pip wheels to install. All engines, BM25 indexers, and test runners use the native Python standard library.

---

## Quickstart & Installation Tracks

### Interactive Setup (Recommended)
Run the guided interactive installer:

```bash
# Using Bash (Linux / macOS):
./install.sh

# Using Python (Windows / Linux / macOS):
python3 install.py
```

### Track 1: Google Antigravity IDE
Install all 21 capabilities globally into your Antigravity configuration directory (`~/.gemini/config/skills`):

```bash
./install.sh --all --global
```

### Track 2: Claude Code CLI
Install capabilities globally into Claude Code (`~/.claude/skills`):

```bash
./install.sh --all --claude
```

### Track 3: OpenCode CLI
Install capabilities globally into OpenCode (`~/.config/opencode/skills`):

```bash
./install.sh --all --opencode
```

### Track 4: Project-Local Workspace
If you want capabilities installed directly into your current project:

```bash
# For Antigravity (.agents/skills):
./install.sh --all --project

# For Claude Code (.claude/skills):
./install.sh --all --claude-project

# For OpenCode (.opencode/skills):
./install.sh --all --opencode-project
```

---

## Packaging & Sharing

GraviDex includes an automated distribution packager that creates clean, self-contained archives containing only the capabilities and installers:

```bash
python3 -B package.py
```

This generates:
- `dist/gravidex.zip`: Universal ZIP archive ready to share via Discord, Telegram, Slack, or Google Drive.
- `dist/gravidex.tar.gz`: Standard Unix gzip tarball.
- `dist/gravidex-pack/`: Antigravity Plugin folder ready to drop into `~/.gemini/config/plugins/`.
- `dist/checksums.sha256`: Cryptographic verification hashes.

For detailed instructions on sharing, see [SHARING.md](./SHARING.md).

---

## Unified Verification Harness

Run the unified test runner anytime to confirm all 29 sandboxes and capabilities are operational:

```bash
python3 -B test_all.py
```

Expected output:
```text
========================================================================
          GRAVIDEX CAPABILITY & SKILLS SUITE - TEST RUNNER
========================================================================
Mode: High-Performance Parallel (29 suites across isolated sandboxes)

  [gravidex-capabilities   ] PASS in 0.238s (Layer B Curated & Retained Capability Verification (9 tests))
  [gravidex-governance     ] PASS in 0.344s (Governance, Identity & Zero-Emoji Verification (8 tests))
  [capability-validator    ] PASS in 0.055s (Deterministic Structural & Frontmatter Validator)
  [rebuild-drift-engine    ] PASS in 0.122s (Three-Way Upstream Drift & Rebuild Verification)
  ...
  [asd-ste100              ] PASS in 1.735s (ASD-STE100 Simplified Technical English & Karpathy 80% Engine)

========================================================================
Total Suite Runtime: 2.071s | Result: ALL PASS (100%)
========================================================================
```

---

## Contributing

Contributions, bug reports, and new capabilities are welcome. Please ensure that:
1. All capabilities maintain zero external runtime dependencies (Python standard library first).
2. Strict zero-emoji compliance is maintained across code, tests, documentation, and commits.
3. `python3 -B test_all.py` passes with a 100% success rate.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

## License

GraviDex is open-source software licensed under the [MIT License](./LICENSE).
