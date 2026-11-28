<div align="center">

<img src="assets/banner.svg" alt="opencode-connect-f-production-skills — 8 gated production & security skills" width="100%">

<br>

**Eight [OpenCode](https://opencode.ai) Agent Skills + `/connect-f` command that replace reckless AI edits with an *interview-first, evidence-based, phase-approved* engineering workflow.**

[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e.svg?style=flat-square)](LICENSE)
[![OpenCode](https://img.shields.io/badge/OpenCode-Skills-38bdf8.svg?style=flat-square)](https://opencode.ai/docs/skills/)
[![Skills](https://img.shields.io/badge/skills-8-818cf8.svg?style=flat-square)](#-the-eight-skills)
[![Command](https://img.shields.io/badge/command-%2Fconnect--f-a78bfa.svg?style=flat-square)](#-six-stage-gated-workflow)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-d97757.svg?style=flat-square)](#-one-standard-three-agents)
[![Codex](https://img.shields.io/badge/Codex%20CLI-compatible-10a37f.svg?style=flat-square)](#-one-standard-three-agents)
[![CI](https://img.shields.io/github/actions/workflow/status/abduallahJamal/opencode-connect-f-production-skills/validate.yml?branch=main&style=flat-square&label=CI&color=0ea5a4)](.github/workflows/validate.yml)
[![Docs](https://img.shields.io/badge/docs-English%20%2B%20العربية-0f172a.svg?style=flat-square)](#-usage)

**🌐 English** · **[العربية](README.ar.md)**

</div>

---

## 📌 The idea in one line

Left unchecked, coding agents scan wildly, overwrite local edits, guess root causes, and claim "production-ready!" without running a single test. **Connect F** enforces a strict operating contract: **interview first → read-only audit with evidence → prioritized phased plan → explicit approval before a single file changes**.

| | Without Connect F | With Connect F |
|---|---|---|
| **First action** | Starts scanning and editing immediately | **Asks 6 structured scoping questions first**, summarizes agreement |
| **Discovery** | Modifies lockfiles, runs risky commands | Strictly **read-only** discovery; preserves uncommitted user work |
| **Findings** | Mixes guesses with facts | Separates **confirmed defects** (with path + evidence) from hypotheses |
| **Security & secrets** | May echo `.env` values or weaken checks | Redacts secrets, checks server-side authz/OWASP boundaries |
| **Execution** | Giant unreviewable diff | Small, reversible **approved phases** with acceptance criteria & rollback |
| **Verification** | Claims "all tests pass" without running them | Reports **only commands actually executed**; `UNKNOWN` stays `UNKNOWN` |

---

## 🧩 The eight skills

### 🧭 `connect-f-workflow` — Orchestrator & `/connect-f` Slash Command
Guides the full 6-stage lifecycle: mandatory 6-question intake interview, safe read-only discovery, multi-domain audit, risk-prioritized phased plan, explicit approval gate, and verified incremental execution.

### 🔍 `connect-f-audit` — Read-Only Technical Audit
Inspects architecture, module boundaries, circular dependencies, validation, error handling, concurrency, data access, API contracts, CI, and operational posture — producing severity-ranked findings (`Critical` → `Informational`) with zero file modifications.

### 🛡️ `connect-f-security` — Application Security Review
Audits authentication & session lifecycle, server-side object/tenant authorization, injection/XSS/CSRF/SSRF/path traversal, file uploads, rate limits, secret exposure, CORS/headers/cookies, parameterized queries, and webhook replay protection.

### ⚡ `connect-f-performance` — Evidence-Based Performance
Separates measured bottlenecks from guesswork across hot paths: N+1 queries, repeated API/DB calls, payload bloat, expensive serialization, memory leaks, unbounded queues, and cache invalidation/tenant isolation risks.

### 🧪 `connect-f-testing` — Risk-Based Verification
Discovers the project's existing test runner, establishes a clean baseline (pre-existing failures vs regressions), prioritizes critical user journeys and denied-authorization paths, and adds deterministic regression tests before bug fixes.

### 🔧 `connect-f-refactor` — Behavior-Preserving Refactoring
Executes small, single-purpose structural improvements after phase approval — tracing callers, public schemas, DB fields, and side effects while adding characterization tests when existing coverage is thin.

### 🐛 `connect-f-bug-fix` — Root-Cause Debugging
Traces control and data flow to prove root cause with evidence before editing, applies minimal targeted fixes at the right layer (no swallowed exceptions or arbitrary `sleep` patches), and verifies adjacent flows.

### 🚀 `connect-f-production-readiness` — Release Go/No-Go Gate
Evaluates 11 operational gates (reproducible builds, secrets, CI, authz, dependencies, migrations/backups, observability, health checks/graceful shutdown, rollback) — marking each `PASS`, `FAIL`, or `UNKNOWN` strictly by evidence.

---

## 🔄 Six-stage gated workflow

When you run `/connect-f` (or ask the agent to start **Connect F**), the agent follows six non-negotiable stages:

1. **Intake Interview (No scanning yet)** — Asks 6 concise questions covering Goal, Scope, Mode (`audit-only` vs `audit + approved fixes`), Priority, Constraints, and Approval policy.
2. **Stage 1: Safe Read-Only Discovery** — Checks `git status --short` to protect local edits, maps stack, entry points, data stores, test runners, and CI without installing packages or mutating files.
3. **Stage 2: Evidence-Based Audit** — Loads `connect-f-audit` plus relevant domain skills (`security`, `performance`, `testing`, `production-readiness`) and documents every finding with ID, severity, confidence, location, impact, and fix.
4. **Stage 3: Risk-Prioritized Phased Plan** — Orders phases from security/data-loss risks down to cleanup, defining scope, acceptance criteria, verification commands, risks, and rollback for each phase.
5. **Stage 4: Explicit Approval Gate** — Stops completely in `audit-only` mode, or waits for explicit sign-off before executing Phase 1.
6. **Stage 5 & 6: Reversible Execution & Honest Reporting** — Applies small patches, runs real checks, inspects `git diff` for regressions or leaked secrets, and reports exact commands run vs not run.

---

## 🧩 One standard, three agents

Built on the open [Agent Skills specification](https://agentskills.io/specification) — the same `SKILL.md` files work across OpenCode, Claude Code, and Codex CLI:

| Agent | Project path | Global path | Invocation |
|---|---|---|---|
| **OpenCode** | `.opencode/skills/` + `.opencode/commands/` | `~/.config/opencode/` | `/connect-f` or `Connect F` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | `/connect-f-workflow`, `/connect-f-security`, … |
| **Codex CLI** | `.agents/skills/` | `~/.agents/skills/` | `$connect-f-workflow` or `/skills` |

`.opencode/skills/` is the **single source of truth**; `.claude/skills/` and `.agents/skills/` are generated and verified via SHA-256 checksums:

```bash
./scripts/sync-platforms.sh          # regenerate .claude/ and .agents/ copies
./scripts/sync-platforms.sh --check  # fail on drift (enforced in GitHub Actions CI)
```

---

## 🚀 Installation

### Option 1 — Multi-agent installer (recommended)

```bash
git clone https://github.com/abduallahJamal/opencode-connect-f-production-skills.git
cd opencode-connect-f-production-skills

# Global install for all agents (OpenCode + Claude Code + Codex)
./install.sh --all --global

# Or install into a specific target repository
./install.sh --all --project /path/to/your-repo

# Optional: copy the Connect F operating contract & report templates into target repo
cp templates/connect-f-AGENTS.md /path/to/your-repo/AGENTS.md
cp -r templates /path/to/your-repo/templates
```

### Option 2 — Manual copy (OpenCode)

```bash
cp -r opencode-connect-f-production-skills/.opencode /path/to/your-repo/
cp opencode-connect-f-production-skills/templates/connect-f-AGENTS.md /path/to/your-repo/AGENTS.md
```

### Option 3 — Git submodule

```bash
git submodule add https://github.com/abduallahJamal/opencode-connect-f-production-skills.git .opencode/vendor/connect-f
./.opencode/vendor/connect-f/install.sh --all --project .
```

---

## 📋 Included templates

Ready-to-use structured Markdown deliverables in [`templates/`](templates/):

| Template | Purpose |
|---|---|
| [`templates/audit-report.md`](templates/audit-report.md) | Full read-only technical audit report with baseline table, findings matrix, and phased plan |
| [`templates/phase-plan.md`](templates/phase-plan.md) | Per-phase contract: scope, preserved behaviors, steps, acceptance criteria, and rollback |
| [`templates/release-checklist.md`](templates/release-checklist.md) | 11-gate production Go/No-Go checklist (`PASS` / `FAIL` / `UNKNOWN` with evidence) |
| [`templates/connect-f-AGENTS.md`](templates/connect-f-AGENTS.md) | Drop-in `AGENTS.md` operating contract for any target repository |

---

## 🧪 Usage

Open your target project in OpenCode and run:

```text
/connect-f
```

Or invoke a focused domain skill directly in any supported agent:

```text
Run connect-f-security in read-only audit mode on src/auth and api/permissions.
```

See ready-to-copy prompts in **[English Usage Examples](docs/usage-examples.en.md)** and **[أمثلة الاستخدام بالعربية](docs/usage-examples.md)**.

---

## 📁 Repository structure

```text
opencode-connect-f-production-skills/
├── .opencode/
│   ├── commands/connect-f.md                      # /connect-f slash command
│   └── skills/                                    # canonical source of truth (8 skills)
│       ├── connect-f-workflow/SKILL.md
│       ├── connect-f-audit/SKILL.md
│       ├── connect-f-security/SKILL.md
│       ├── connect-f-performance/SKILL.md
│       ├── connect-f-testing/SKILL.md
│       ├── connect-f-refactor/SKILL.md
│       ├── connect-f-bug-fix/SKILL.md
│       └── connect-f-production-readiness/SKILL.md
├── .claude/skills/                                # generated → Claude Code
├── .agents/skills/                                # generated → Codex CLI / Cursor / Gemini
├── templates/                                     # audit, phase-plan, release checklist & AGENTS contract
├── docs/                                          # bilingual prompt examples (EN + AR)
├── assets/banner.svg                              # repository header banner
├── scripts/
│   ├── sync-platforms.sh                          # multi-agent generator + drift check
│   ├── validate.py                                # Python CI validator (frontmatter + sync + docs)
│   └── publish.sh                                 # GitHub publishing helper
├── install.sh                                     # multi-agent CLI installer
├── AGENTS.md                                      # repository context & non-negotiable rules
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

---

## 🤝 Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Before opening a pull request, run:

```bash
bash -n install.sh scripts/*.sh
./scripts/sync-platforms.sh --check
python3 scripts/validate.py
```

---

## 📜 License

Released under the [MIT License](LICENSE). Skills enforce engineering discipline and safety gates, but do not substitute for formal penetration testing, compliance certification, or human code review.
