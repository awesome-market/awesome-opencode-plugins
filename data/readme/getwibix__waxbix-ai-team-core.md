# waxbix-ai-team

> A production-ready, validated multi-agent software engineering team for OpenCode V2.

[![CI](https://github.com/waxbix/waxbix-ai-team/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/waxbix/waxbix-ai-team/actions/workflows/ci.yml)
[![Validate](https://github.com/waxbix/waxbix-ai-team/actions/workflows/validate.yml/badge.svg)](https://github.com/waxbix/waxbix-ai-team/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version: 1.0.0](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)](CHANGELOG.md)
[![OpenCode V2](https://img.shields.io/badge/OpenCode-V2-purple.svg)](docs/OPENCODE-V2-COMPATIBILITY.md)

`waxbix-ai-team` is a content pack for [OpenCode V2](https://opencode.ai): a curated
team of 15 specialized AI agents, 55 skills, 10 slash commands, 6 rules, and 4
templates, plus cross-platform installers, six Python validation scripts, and a
checksum-verified manifest. The team is **orchestrator-first** — one primary agent
decomposes the task, routes subtasks to the right specialist, and assembles the
deliverable.

---

## Highlights

- **15 agents** spanning architecture, frontend, backend, mobile, database,
  integration, design, security, qa, performance, devops, ai, and review —
  coordinated by an `orchestrator` primary agent.
- **55 skills** across 14 categories, each scoped knowledge the matching
  specialist can invoke on demand.
- **10 slash commands** under the `waxbix/` namespace (`/waxbix:plan`,
  `/waxbix:build`, `/waxbix:review`, …).
- **6 rules** that constrain every agent's behavior — engineering, security,
  architecture, testing, collaboration, code-quality.
- **4 templates** for task contracts, ADRs, code reviews, and implementation
  plans.
- **Cross-platform installers** (`install`, `uninstall`, `update`, `doctor`)
  in both Bash (Linux/macOS) and PowerShell (Windows).
- **6 validation scripts** that keep the pack consistent: agents, skills,
  manifest, links, duplicates, and a SHA256 checksum verifier.
- **CI on three OSes** (ubuntu, macOS, windows) plus a deep-validation
  workflow and a draft release pipeline.

## Architecture overview

```
waxbix-ai-team/
├── agents/                      # 15 agent definitions (orchestrator + 14 subagents)
│   ├── orchestrator.md          # primary agent — owns the user conversation
│   ├── architecture/            # principal-architect
│   ├── frontend/                # frontend-engineer
│   ├── backend/                 # backend-engineer
│   ├── mobile/                  # mobile-engineer
│   ├── database/                # database-engineer
│   ├── integration/             # integration-engineer
│   ├── design/                  # ui-ux-designer
│   ├── security/                # security-engineer
│   ├── qa/                      # qa-engineer
│   ├── performance/             # performance-engineer
│   ├── devops/                  # devops-engineer
│   ├── ai/                      # ai-engineer
│   └── review/                  # code-reviewer, documentation-engineer
├── skills/                      # 55 skills in 14 category folders
│   ├── architecture/  frontend/  backend/   mobile/   database/
│   ├── integration/   design/     security/  qa/       performance/
│   ├── devops/        ai/         review/    domain/
│   └── <category>/wx-<name>/SKILL.md
├── commands/waxbix/             # 10 slash commands: plan, analyze, build, fix,
│                                # review, test, security, refactor, document, status
├── rules/                       # 6 rules: engineering, security, architecture,
│                                # testing, collaboration, code-quality
├── templates/                   # 4 templates: task-contract, architecture-decision,
│                                # code-review, implementation-plan
├── installer/                   # install / uninstall / update / doctor
│   ├── install.sh     install.ps1
│   ├── uninstall.sh   uninstall.ps1
│   ├── update.sh       update.ps1
│   ├── doctor.sh       doctor.ps1
│   └── lib/                      # shared shell + PowerShell helpers
├── scripts/                     # 6 Python validators + checksum tool
│   ├── validate-agents.py
│   ├── validate-skills.py
│   ├── validate-manifest.py
│   ├── validate-links.py
│   ├── check-duplicates.py
│   └── generate-checksums.py    # writes & verifies manifest.checksums.json
├── docs/                         # 12 reference documents
├── tests/                        # unit, integration, installer, fixtures, evaluation
├── .github/
│   ├── workflows/               # ci.yml, validate.yml, release.yml
│   └── ISSUE_TEMPLATE/          # bug_report, feature_request, config
├── manifest.json                 # the source of truth for every artifact
├── manifest.checksums.json       # SHA256 of every tracked file
├── README.md  AGENTS.md  CONTRIBUTING.md  SECURITY.md
├── CHANGELOG.md  CODE_OF_CONDUCT.md  LICENSE
└── installer/doctor.sh          # one-shot health check
```

`manifest.json` is the **single source of truth**: every agent, skill, command,
rule, template, installer, and script is listed there with its on-disk path.
`scripts/generate-checksums.py` produces `manifest.checksums.json`, a SHA256
sidecar that lets anyone verify the pack has not been tampered with.

## Quick start

### 1. Install globally

Makes the team available to every project on the machine.

**Linux / macOS:**

```bash
git clone https://github.com/waxbix/waxbix-ai-team.git
cd waxbix-ai-team
bash installer/install.sh
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/waxbix/waxbix-ai-team.git
cd waxbix-ai-team
pwsh -File installer/install.ps1
```

The installer writes into the OpenCode V2 global config directory:
`$XDG_CONFIG_HOME/opencode` (or `~/.config/opencode`) on Linux/macOS,
`%APPDATA%\opencode` on Windows.

### 2. Install into a single project

Use the same installer from inside a project repo to drop the pack into
`./opencode/` instead of the global directory:

```bash
bash installer/install.sh --project
# or: pwsh -File installer/install.ps1 -Project
```

### 3. Verify

Run the doctor to confirm the install location, OpenCode V2 compatibility,
and checksum integrity in one shot:

```bash
bash installer/doctor.sh
# or: pwsh -File installer/doctor.ps1
```

Then verify checksums explicitly:

```bash
python3 scripts/generate-checksums.py --verify
```

### 4. Use it

In an OpenCode V2 session:

- Talk to the **`orchestrator`** (the default primary agent).
- Use slash commands like `/waxbix:plan`, `/waxbix:build`, `/waxbix:review`.
- The orchestrator routes work to specialist subagents automatically.

## The 15 agents

| Agent id                   | Category     | Mode     | Owns                                                              |
|----------------------------|--------------|----------|-------------------------------------------------------------------|
| `orchestrator`             | core         | primary  | Task decomposition, routing, contracts, assembly                  |
| `principal-architect`      | architecture | subagent | System design, ADRs, technical risk                               |
| `frontend-engineer`        | frontend     | subagent | Web UI: React, Vue, Angular, TypeScript, design systems           |
| `backend-engineer`         | backend      | subagent | Services, APIs, auth, background jobs                             |
| `mobile-engineer`          | mobile       | subagent | Flutter, React Native, Kotlin/Android, iOS, offline-first         |
| `database-engineer`        | database     | subagent | PostgreSQL, MySQL, SQLite, MongoDB, Redis, query optimization      |
| `integration-engineer`     | integration  | subagent | Third-party integrations, webhooks, payment providers             |
| `ui-ux-designer`           | design       | subagent | UX flows, accessibility, responsive design                        |
| `security-engineer`        | security     | subagent | AppSec, OWASP, secrets/dependency security, security testing      |
| `qa-engineer`              | qa           | subagent | Unit, integration, e2e, regression testing                        |
| `performance-engineer`     | performance  | subagent | Frontend, backend, database performance                           |
| `devops-engineer`          | devops       | subagent | Docker, CI/CD, Linux deployment, monitoring                      |
| `ai-engineer`              | ai           | subagent | LLM integration, agentic workflows, RAG, AI eval/security         |
| `code-reviewer`            | review       | subagent | Code review, refactoring, technical documentation                 |
| `documentation-engineer`   | review       | subagent | Reference docs, runbooks, changelog                               |

## The 14 skill categories

Each category lives under `skills/<category>/wx-<name>/SKILL.md`. Specialists
discover and invoke skills via the `wx-` prefix.

| Category      | Skills | Examples                                                                  |
|---------------|-------|----------------------------------------------------------------------------|
| architecture  | 2     | `wx-system-architecture`, `wx-software-design-patterns`                   |
| frontend      | 5     | `wx-react-development`, `wx-nextjs-development`, `wx-typescript-engineering` |
| backend       | 6     | `wx-nodejs-backend`, `wx-python-backend`, `wx-api-engineering`            |
| mobile        | 6     | `wx-flutter-development`, `wx-react-native-development`, `wx-kotlin-android` |
| database      | 6     | `wx-postgresql`, `wx-mysql`, `wx-mongodb`, `wx-redis-caching`              |
| integration   | 3     | `wx-third-party-integrations`, `wx-payment-integrations`, `wx-webhooks-events` |
| design        | 3     | `wx-ui-ux-design`, `wx-accessibility`, `wx-responsive-design`             |
| security      | 4     | `wx-owasp-security`, `wx-secrets-dependency-security`, `wx-security-testing` |
| qa            | 3     | `wx-unit-integration-testing`, `wx-e2e-testing`, `wx-regression-testing`  |
| performance   | 3     | `wx-frontend-performance`, `wx-backend-performance`, `wx-database-performance` |
| devops        | 4     | `wx-docker-containers`, `wx-ci-cd-pipelines`, `wx-linux-deployment`       |
| ai            | 4     | `wx-llm-integration`, `wx-agentic-workflows`, `wx-rag-embeddings`         |
| review        | 3     | `wx-code-review`, `wx-refactoring`, `wx-technical-documentation`          |
| domain        | 3     | `wx-pos-business-systems`, `wx-automotive-inventory-barcode`, `wx-printing-escpos-labels` |

**Total: 55 skills in 14 categories.** For the full catalog see
[`docs/SKILLS.md`](docs/SKILLS.md).

## The 10 commands

All commands live under the `waxbix/` namespace and are invoked as
`/waxbix:<name>`.

| Command                | Purpose                                                        |
|------------------------|----------------------------------------------------------------|
| `/waxbix:plan`         | Decompose a request into a task contract + subagent routing    |
| `/waxbix:analyze`      | Deep analysis of a system, file, or incident                   |
| `/waxbix:build`        | Implement a feature end-to-end across one or more specialists  |
| `/waxbix:fix`          | Reproduce, diagnose, and fix a bug                             |
| `/waxbix:review`       | Code review against the project's rules + checklist           |
| `/waxbix:test`         | Author and run unit/integration/e2e tests                      |
| `/waxbix:security`     | Threat-model + security review                                 |
| `/waxbix:refactor`     | Refactor without behavior change                               |
| `/waxbix:document`     | Generate or update reference docs, ADRs, runbooks              |
| `/waxbix:status`       | Show task progress, open contracts, outstanding work           |

See [`docs/COMMANDS.md`](docs/COMMANDS.md).

## Agent routing summary

The orchestrator follows a fixed routing policy:

1. **Receive intent** from the user or a `/waxbix:*` command.
2. **Decompose** into discrete subtasks; record each in
   `templates/task-contract.md`.
3. **Route** each subtask to exactly one specialist. Routing is driven by
   the subtask's primary concern, not by the agent's name. When two concerns
   are equally weighted, the orchestrator picks the one closer to the user
   (frontend over backend, backend over database, etc.).
4. **Verify** each subagent's output against the contract before merging.
5. **Assemble** the final answer; the orchestrator is the only agent that
   talks back to the user.
6. **Escalate** ambiguity rather than guess — the orchestrator asks the user
   when no single specialist can fully own a subtask.

See [`docs/AGENTS.md`](docs/AGENTS.md) for the full routing table and
fallback rules, and [`docs/TASK-PROTOCOL.md`](docs/TASK-PROTOCOL.md) for
the contract format.

## Task protocol summary

Every non-trivial task produces a task contract (see
`templates/task-contract.md`) that captures:

- **Goal** — one sentence.
- **Context** — links, prior art, constraints.
- **Subtasks** — the decomposed list, each with an owner agent and a
  definition of done.
- **Acceptance criteria** — observable, testable.
- **Risks & open questions** — explicitly tracked.
- **Status** — `pending | in-progress | blocked | done`.

Specialists update the contract as they work; the orchestrator never
loses track of incomplete subtasks. See [`docs/TASK-PROTOCOL.md`](docs/TASK-PROTOCOL.md).

## Security model summary

`waxbix-ai-team` is content, not infrastructure. The security model has
three layers:

1. **Definitions are prompts.** Agents, skills, and commands are Markdown
   files interpreted by OpenCode V2. They cannot execute code by themselves;
   they only instruct the LLM, which then asks OpenCode V2 to run tools.
   The OpenCode V2 **permission system** is the enforcement boundary for
   every filesystem, network, or shell action.
2. **Validators enforce consistency.** The six Python scripts ensure no
   duplicate ids, no broken links, no missing files, and no manifest drift.
3. **Checksums enforce integrity.** `scripts/generate-checksums.py`
   produces a SHA256 sidecar; run `--verify` after every clone, install,
   or update to detect tampering or corruption.

For the full model — including prompt-injection mitigation, secret handling,
and the integrity-vs-authenticity distinction — see
[`docs/SECURITY-MODEL.md`](docs/SECURITY-MODEL.md) and [`SECURITY.md`](SECURITY.md).

## CI

Three workflows live in [`.github/workflows/`](.github/workflows/):

| Workflow       | Trigger                                     | What it does                                                            |
|----------------|---------------------------------------------|-------------------------------------------------------------------------|
| `ci.yml`       | `push` to `main`, PR to `main`, manual      | Matrix on ubuntu/macOS/windows: run all validators, shell + PowerShell syntax check, markdown link check, upload report artifact. Cancels in-progress runs on the same branch. |
| `validate.yml` | `workflow_dispatch`, tag push                | Deep validation on ubuntu: runs all six scripts plus `generate-checksums.py --verify`, emits a JSON report artifact and a job summary. |
| `release.yml`  | Tag push `v*.*.*`, manual                   | Verifies manifest version matches the tag, runs all validators, refreshes checksums, builds `tar.gz` + `zip`, computes SHA256, extracts release notes from `CHANGELOG.md`, **creates a DRAFT release** (a maintainer promotes it to public/latest after human review). |

## Troubleshooting

Common problems — wrong install target, broken checksums, missing OpenCode
V2 config, duplicate ids — are cataloged in
[`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md). Start there before
opening an issue, and run `bash installer/doctor.sh` (or
`pwsh -File installer/doctor.ps1`) to capture a snapshot for the maintainers.

## Contributing

We welcome contributions. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md)
(short pointer) and [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) (full
guide) first. The short version:

1. Fork and branch (`feat/<slug>`, `fix/<slug>`, `docs/<slug>`).
2. Run all six validators locally before pushing.
3. If you add or change any tracked file, regenerate
   `manifest.checksums.json` with `python3 scripts/generate-checksums.py`.
4. Open a PR against `main`; fill in `.github/PULL_REQUEST_TEMPLATE.md`.
5. Use [Conventional Commits](https://www.conventionalcommits.org/).

By contributing, you agree your contributions are licensed under the
[MIT license](LICENSE) and that you will abide by the
[Code of Conduct](CODE_OF_CONDUCT.md).

## License

Copyright (c) 2025 Waxbix AI Team Contributors. Licensed under the
[MIT License](LICENSE).
