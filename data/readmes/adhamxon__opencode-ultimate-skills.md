# OpenCode Skills — Ultimate Agent Skill Collection

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenCode](https://img.shields.io/badge/OpenCode-Ready-6C47FF)](https://opencode.ai)
[![Skills](https://img.shields.io/badge/Skills-384-success)](https://github.com/Adhamxon/opencode-ultimate-skills)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Adhamxon/opencode-ultimate-skills/pulls)
[![Maintained](https://img.shields.io/badge/maintained-yes-success)](https://github.com/Adhamxon/opencode-ultimate-skills)

A comprehensive, production-ready collection of **384 curated skills**, **9 specialized agents**, and **9 custom commands** for [OpenCode](https://opencode.ai) — the AI-powered coding assistant.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Skills Catalog](#skills-catalog)
- [Whats New v30](#whats-new-v30)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Features

- **384 Pre-installed Skills** — Curated from top community collections (Anthropic, Matt Pocock, Addy Osmani, Google Cloud, HuggingFace, Wondelai book skills, project management, animation experts, and more)
- **9 Specialized Agents** — Full-stack developer, code reviewer, DevOps engineer, TDD practitioner, architect, security auditor, QA engineer, bug hunter, UI/UX designer
- **9 Custom Commands** — Quick-access commands for review, deploy, test, fix, design, security audit, and architecture planning
- **Multi-language Support** — TypeScript, Python, Java, C#, Go, Rust, Kotlin, Swift, and more
- **Multi-cloud Ready** — GCP (GKE, Cloud Run, BigQuery, Spanner), Azure, AWS patterns
- **Zero-config Setup** — Drop into any project and OpenCode auto-discovers everything

---

## Quick Start

### Prerequisites

- [OpenCode](https://opencode.ai) installed

### Installation

```bash
# Clone this repository into your project
git clone https://github.com/Adhamxon/opencode-ultimate-skills.git .opencode

# Or copy manually into your project
cp -r opencode-ultimate-skills/.opencode /path/to/your/project/.opencode

# Restart OpenCode for changes to take effect
```

OpenCode automatically discovers the `.opencode/` directory. No additional configuration needed.

---

## Usage

### Agents

Switch between agents during your OpenCode session:

| Agent | Description | Permission |
|---|---|---|
| `fullstack-dev` | Frontend + Backend + Database development | edit: allow, bash: git/npm allow |
| `code-reviewer` | Code quality, security, performance review | edit: deny, read-only |
| `devops-engineer` | CI/CD, Docker, Kubernetes, Cloud | docker/kubectl allow |
| `tdd-developer` | Test-Driven Development cycle | npm test allow |
| `architect` | Domain modeling, codebase design, patterns | read-only |
| `security-auditor` | OWASP, dependency audit, secret scanning | read-only |
| `qa-engineer` | E2E testing, test plans, Playwright | deny edit |
| `bug-hunter` | Bug diagnosis, root cause analysis, fix | edit: allow |
| `designer` | UI/UX, animation, responsive CSS | edit: allow |

### Commands

Quick commands available in your OpenCode session:

```
/review     — Code review with detailed analysis
/deploy     — Build and deploy to production
/test       — Run tests and analyze coverage
/fix        — Diagnose and fix bugs
/build      — Build the project
/arch       — Architecture consultancy
/design     — UI/UX design generation
/security   — Security audit
/tdd        — Start TDD cycle (red-green-refactor)
```

### Agents via OpenCode config

Agents are defined both inline in `opencode.json` and as individual Markdown files in `.opencode/agents/`. You can customize any agent by editing its `.md` file or overriding fields in `opencode.json`.

---

## Skills Catalog

The collection includes **384 skills** organized by source:

### Anthropic Skills (16)
`claude-api` · `mcp-builder` · `skill-creator` · `webapp-testing` · `frontend-design` · `theme-factory` · `brand-guidelines` · `canvas-design` · `algorithmic-art` · `xlsx` · `pptx` · `docx` · `pdf-anthropic` · `internal-comms` · `doc-coauthoring` · `web-artifacts-builder`

### Matt Pocock Engineering Skills (22)
`matt-code-review` · `matt-tdd` · `matt-diagnosing-bugs` · `matt-domain-modeling` · `matt-implement` · `matt-research` · `matt-prototype` · `matt-wayfinder` · `matt-triage` · `matt-to-spec` · `matt-to-tickets` · `matt-codebase-design` · `matt-resolving-merge-conflicts` · `matt-improve-codebase-architecture` · `matt-writing-great-skills` · `matt-teach` · `matt-handoff` · `matt-grilling` · `matt-setup-pre-commit` · `matt-git-guardrails` · `matt-scaffold-exercises` · `matt-migrate-to-shoehorn`

### Addy Osmani Agent Skills (22) ⭐ NEW
`spec-driven-development` · `code-simplification` · `debugging-and-error-recovery` · `security-and-hardening` · `ci-cd-and-automation` · `incremental-implementation` · `planning-and-task-breakdown` · `frontend-ui-engineering` · `context-engineering` · `git-workflow-and-versioning` · `source-driven-development` · `shipping-and-launch` · `documentation-and-adrs` · `api-and-interface-design` · `doubt-driven-development` · `deprecation-and-migration` · `browser-testing-with-devtools` · `code-review-and-quality` · `observability-and-instrumentation` · `idea-refine` · `interview-me` · `using-agent-skills`

### Curated Skills (25)
`figma` · `figma-code-connect-components` · `figma-create-design-system-rules` · `figma-create-new-file` · `figma-generate-design` · `figma-implement-design` · `figma-use` · `playwright` · `playwright-interactive` · `vercel-deploy` · `netlify-deploy` · `cli-creator` · `security-best-practices` · `security-threat-model` · `sentry` · `linear` · `screenshot` · `speech` · `define-goal` · `yeet` · `sys-openai-docs` · `sys-skill-creator` · `sys-skill-installer` · `pdf` · `code-review` (full multi-language)

### Animation Skills (8)
`anim-animation-vocabulary` · `anim-apple-design` · `anim-emil-design-eng` · `anim-find-animation-opportunities` · `anim-improve-animations` · `anim-pick-ui-library` · `anim-prototype` · `anim-review-animations`

### Google Cloud Skills (17)
`gcp-gke-basics` · `gcp-cloud-run-basics` · `gcp-bigquery-basics` · `gcp-bigquery-ai-ml` · `gcp-cloud-storage-basics` · `gcp-cloud-sql-basics` · `gcp-spanner-basics` · `gcp-alloydb-basics` · `gcp-firebase-basics` · `gcp-gemini-api` · `gcp-gemini-agents-api` · `gcp-gcloud` · `gcp-cloud-logging-configuration-basics` · `gcp-workload-manager-basics` · `gcp-datalineage-summary` · `gcp-google-cloud-waf-security` · `gcp-detection-engineering-coverage-evaluation`

### HuggingFace ML/AI Skills (3) ⭐ NEW
`trl-training` · `transformers-js` · `train-sentence-transformers`

### Awesome LLM Agent Skills (5) ⭐ NEW
`commit-archaeologist` · `project-graveyard` · `scope-creep-detector` · `thinking-out-loud` · `advisor-orchestrator-worker`

### Karpathy Guidelines (1) ⭐ NEW
`karpathy-guidelines`

### Wondelai Book Skills (62) ⭐⭐ NEW
`37signals-way` · `blue-ocean-strategy` · `clean-architecture` · `clean-code` · `cold-start-problem` · `contagious` · `continuous-discovery` · `create-app` · `create-business` · `create-website` · `cro-methodology` · `crossing-the-chasm` · `ddia-systems` · `design-code-architecture` · `design-everyday-things` · `design-sprint` · `domain-driven-design` · `drive-motivation` · `good-strategy-bad-strategy` · `grow-app` · `grow-business` · `grow-website` · `high-output-management` · `high-perf-browser` · `hooked-ux` · `hundred-million-offers` · `improve-app` · `improve-business` · `improve-code-quality` · `improve-retention` · `improve-website` · `influence-psychology` · `inspired-product` · `ios-hig-design` · `jobs-to-be-done` · `lean-analytics` · `lean-startup` · `lean-ux` · `made-to-stick` · `microinteractions` · `mom-test` · `monetizing-innovation` · `negotiation` · `obviously-awesome` · `one-page-marketing` · `pragmatic-programmer` · `predictable-revenue` · `refactoring-patterns` · `refactoring-ui` · `release-it` · `remove-technical-debt` · `scorecard-marketing` · `software-design-philosophy` · `steve-jobs-design-review` · `storybrand-messaging` · `system-design` · `team-topologies` · `top-design` · `traction-eos` · `ux-heuristics` · `web-typography` · `working-with-legacy-code`

### Project Management Skills (68) ⭐⭐ NEW
`ab-test-analysis` · `analyze-feature-requests` · `ansoff-matrix` · `beachhead-segment` · `brainstorm-experiments-existing` · `brainstorm-experiments-new` · `brainstorm-ideas-existing` · `brainstorm-ideas-new` · `brainstorm-okrs` · `business-model` · `cohort-analysis` · `competitive-battlecard` · `competitor-analysis` · `create-prd` · `customer-journey-map` · `draft-nda` · `grammar-check` · `growth-loops` · `gtm-motions` · `gtm-strategy` · `ideal-customer-profile` · `identify-assumptions-existing` · `identify-assumptions-new` · `intended-vs-implemented` · `interview-script` · `job-stories` · `lean-canvas` · `market-segments` · `market-sizing` · `marketing-ideas` · `metrics-dashboard` · `monetization-strategy` · `north-star-metric` · `opportunity-solution-tree` · `outcome-roadmap` · `pestle-analysis` · `porters-five-forces` · `positioning-ideas` · `pre-mortem` · `pricing-strategy` · `prioritization-frameworks` · `prioritize-assumptions` · `prioritize-features` · `privacy-policy` · `product-name` · `product-strategy` · `product-vision` · `release-notes` · `retro` · `review-resume` · `sentiment-analysis` · `shipping-artifacts` · `sprint-plan` · `sql-queries` · `stakeholder-map` · `startup-canvas` · `strategy-red-team` · `summarize-interview` · `summarize-meeting` · `swot-analysis` · `test-scenarios` · `user-personas` · `user-segmentation` · `user-stories` · `value-prop-statements` · `value-proposition` · `wwas`

### iOS & Swift Skills (16) ⭐⭐ NEW
`app-store-changelog` · `bug-hunt-swarm` · `github` · `ios-debugger-agent` · `macos-menubar-tuist-app` · `macos-spm-app-packaging` · `orchestrate-batch-refactor` · `project-skill-audit` · `react-component-performance` · `review-and-simplify-changes` · `review-swarm` · `swift-concurrency-expert` · `swiftui-liquid-glass` · `swiftui-performance-audit` · `swiftui-ui-patterns` · `swiftui-view-refactor`

### Obsidian Skills (5) ⭐⭐ NEW
`defuddle` · `json-canvas` · `obsidian-bases` · `obsidian-cli` · `obsidian-markdown`

### Web & Framework Skills (45) ⭐⭐ NEW
`supabase-postgres-best-practices` · `supabase` · `sveltekit` · `tailwind-design-system` · `tailwind-patterns` · `tanstack-query-expert` · `threejs-animation` · `threejs-fundamentals` · `threejs-interaction` · `threejs-materials` · `threejs-postprocessing` · `threejs-textures` · `trpc-fullstack` · `turborepo-caching` · `typescript-advanced-types` · `typescript-expert` · `ui-a11y` · `ui-component` · `ui-motion` · `ui-tokens` · `unslop` · `unslop-commit` · `unslop-file` · `unslop-review` · `using-git-worktrees` · `uv-package-manager` · `vector-database-engineer` · `vercel-ai-sdk-expert` · `verification-before-completion` · `vitest-skill` · `weaviate` · `workflow-automation` · `writing-great-skills` · `zod-validation-expert` · `zustand-store-ts`

### Security Testing Skills (42) ⭐⭐ NEW
`performing-api-security-testing-with-postman` · `performing-cve-prioritization-with-kev-catalog` · `performing-docker-bench-security-assessment` · `performing-ssl-tls-security-assessment` · `performing-web-application-penetration-test` · `remediating-s3-bucket-misconfiguration` · `scanning-container-images-with-grype` · `scanning-docker-images-with-trivy` · `scanning-iac-and-images-with-trivy` · `scanning-kubernetes-manifests-with-kubesec` · `scanning-network-with-nmap-advanced` · `securing-api-gateway-with-aws-waf` · `securing-aws-iam-permissions` · `securing-aws-lambda-execution-roles` · `securing-github-actions-workflows` · `securing-kubernetes-on-cloud` · `securing-serverless-functions` · `sql-injection-testing` · `testing-api-authentication-weaknesses` · `testing-api-for-broken-object-level-authorization` · `testing-api-for-mass-assignment-vulnerability` · `testing-api-security-with-owasp-top-10` · `testing-cors-misconfiguration` · `testing-for-business-logic-vulnerabilities` · `testing-for-email-header-injection` · `testing-for-host-header-injection` · `testing-for-json-web-token-vulnerabilities` · `testing-for-open-redirect-vulnerabilities` · `testing-for-sensitive-data-exposure` · `testing-for-xss-vulnerabilities` · `testing-for-xxe-injection-vulnerabilities` · `testing-jwt-token-security` · `testing-oauth2-implementation-flaws` · `testing-patterns` · `testing-prompt-injection-in-rag-pipelines` · `testing-websocket-api-security` · `threat-modeling-expert` · `verifying-build-provenance-with-slsa-sigstore` · `vulnerability-scanner` · `wcag-audit-patterns` · `web-security-testing` · `systematic-debugging`

### Custom Enhanced Skills (11) ⭐ NEW
`ai-ml-engineering` · `api-design-best-practices` · `auth-authorization` · `database-optimization` · `message-queues` · `mobile-development` · `observability` · `performance-optimization` · `system-design` · `testing-strategies` · `web-accessibility`

### Copilot Community Skills (24)
`copilot-cli-mastery` · `copilot-codeql` · `copilot-conventional-commit` · `copilot-diagnose` · `copilot-draw-io-diagram-generator` · `copilot-git-commit` · `copilot-github-actions-efficiency` · `copilot-mcp-cli` · `copilot-postgresql-optimization` · `copilot-postgresql-code-review` · `copilot-sql-optimization` · `copilot-sql-server-table-reconciliation` · `copilot-security-review` · `copilot-typescript-mcp-server-generator` · `copilot-python-mcp-server-generator` · `copilot-java-springboot` · `copilot-csharp-async` · `copilot-dotnet-best-practices` · `copilot-azure-architecture-autopilot` · `copilot-terraform-azurerm-set-diff-analyzer` · `copilot-react-audit-grep-patterns` · `copilot-playwright-generate-test` · `copilot-architecture-blueprint-generator` · `copilot-create-implementation-plan`

---

## What's New (v3.0)

This massive update adds **230 new skills** from 5 major new collections:

| Source | Skills Added |
|--------|-------------|
| **Wondelai Book Skills** | 62 book-based skills (clean architecture, DDD, pragmatic programmer, system design, UX, business strategy, etc.) |
| **Project Management** | 68 PM skills (OKRs, PRDs, sprints, roadmaps, user stories, market research, GTM strategy, etc.) |
| **iOS & Swift Skills** | 16 iOS/Swift development skills (SwiftUI, concurrency, debugging, etc.) |
| **Web & Framework Skills** | 45 modern web development skills (TypeScript, Three.js, Tailwind, TanStack, tRPC, SvelteKit, etc.) |
| **Security Testing** | 42 security testing skills (OWASP, API security, cloud security, container scanning, penetration testing, etc.) |

**[View full changelog →](CHANGELOG.md)**

## Configuration

The main configuration file is `.opencode/opencode.json`. Key settings:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-6",
  "default_agent": "fullstack-dev",
  "skills": {
    "paths": [".opencode/skills"]
  },
  "permission": {
    "edit": "allow",
    "bash": { "git *": "allow", "npm *": "allow", "npx *": "allow", "*": "ask" }
  }
}
```

See [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) for detailed configuration guide.

---

## Project Structure

```
Opencode_skills/
├── .opencode/                        # Auto-discovered by OpenCode
│   ├── opencode.json                 # Main configuration
│   ├── agents/                       # 9 agent definitions
│   ├── commands/                     # 9 command definitions
│   ├── skills/                       # 384 skill folders
│   ├── plugins/                      # Extensible plugin directory
│   └── references/                   # Reference materials
├── docs/                             # Documentation
│   ├── GETTING_STARTED.md
│   ├── SKILLS_REFERENCE.md
│   ├── AGENTS_REFERENCE.md
│   └── COMMANDS_REFERENCE.md
├── scripts/                          # Setup & utility scripts
│   └── setup.ps1
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT — free for personal and commercial use. See [LICENSE](LICENSE) for full terms.

Copyright (c) 2026 Adkhamkhon

See [NOTICE.md](NOTICE.md) for attribution requirements if you reuse individual files.

---

## Acknowledgments

- [Anthropic](https://anthropic.com) — Official Claude skills collection and Claude Code
- [Matt Pocock](https://github.com/mattpocock) — Engineering workflow skills
- [Addy Osmani](https://github.com/addyosmani) — Agent development patterns
- [Google Cloud](https://cloud.google.com) — Cloud product skills
- [HuggingFace](https://huggingface.co) — ML/AI training tools
- [Awesome GitHub Copilot](https://github.com/copilot) — Community skills collection
- [Wondelai](https://github.com/wondelai) — Book-based engineering skills

---

*Built for OpenCode. Powered by the community. Maintained by Adkhamkhon.*
