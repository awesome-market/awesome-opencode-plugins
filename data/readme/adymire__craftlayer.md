<div align="center">

# CraftLayer

### Build with taste. Engineer with precision.

> **Made by Adymire.com Team & Cybertron AI Team**

**Practical skills for AI coding agents — from intentional product design to production-minded engineering.**

[![CI](https://github.com/adymire/CraftLayer/actions/workflows/ci.yml/badge.svg)](https://github.com/adymire/CraftLayer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-35-6c5ce7.svg)](Docs/SKILL-CATALOG.md)

</div>

---

CraftLayer is an open-source collection of focused, reusable skills for AI
coding agents. Each skill gives an agent a practical workflow, decision
criteria, examples, failure modes, and checks for a specific kind of work.

Use the skills in an existing project to help an agent understand the
product and codebase before it changes anything. CraftLayer is designed to
complement your framework, libraries, design system, and coding agent—not
replace them.

> **Project status:** The repository contains 35 skill drafts and a tested
> agent-destination resolver. Install skills directly from GitHub with the
> commands below—no manual clone or global install is required. CraftLayer
> does not yet publish its own `craftlayer` CLI or plugin package. See
> [Implementation Status](Docs/IMPLEMENTATION-STATUS.md).

## Contents

- [What CraftLayer helps with](#what-craftlayer-helps-with)
- [Skill catalog](#skill-catalog)
- [Install without cloning the repository](#install-without-cloning-the-repository)
- [Choose the right agent folder](#choose-the-right-agent-folder)
- [What works today](#what-works-today)
- [Repository structure](#repository-structure)
- [Develop and validate CraftLayer](#develop-and-validate-craftlayer)
- [Contributing](#contributing)
- [Community and reporting](#community-and-reporting)
- [Roadmap](#roadmap)
- [License](#license)

## What CraftLayer helps with

### Design with a reason

Plan interfaces around users, product context, and real tasks. The **Unslop
Engine** challenges generic visual choices when they do not serve the
product—it does not ban familiar patterns that work.

### Engineer inside the project you already have

Skills tell agents to inspect the existing stack, conventions, tests, and
design system before making changes. They emphasize accessibility, security,
maintainability, and preserving working behavior.

### Bring the workflow to the agent you use

The canonical skill format is Markdown with Agent Skills-compatible
`SKILL.md` frontmatter. Documented destinations are provided for OpenCode,
Claude Code, OpenAI Codex, Cursor, and generic Agent Skills-compatible
tools.

### Use JavaScript, TypeScript, and Python where they fit

CraftLayer's repository tooling is TypeScript-first. The catalog also
includes dedicated JavaScript/TypeScript and Python engineering guidance,
with runnable examples and tests for both languages. These skills advise
agents to respect the host project's language and runtime rather than
forcing a migration.

## Skill catalog

The complete catalog, grouped by domain, is in the
[Skill Catalog](Docs/SKILL-CATALOG.md). All current entries are **drafts**:
they are authored and structurally validated, but have not yet completed
the evaluation and release review required to call them published.

| Area | Skills |
|---|---|
| **Design and experience** | Design Intelligence, Unslop Engine, Design Systems, Visual Design, UX Research, Premium Landing Pages, Website Architecture, Responsive Design, Animation and Motion, Image Art Direction, Iconography |
| **Frontend engineering** | Frontend Engineering, JavaScript/TypeScript Engineering, Component Engineering |
| **Dashboards and administration** | Dashboard Design, SaaS Dashboard, Admin Panel, Super-admin Panel, Analytics and Data Visualization |
| **AI products** | AI Dashboard, AI Chat Interface, AI Agent Interface, AI Engineering, RAG and Knowledge Systems |
| **Backend and platform** | Backend Architecture, Python Engineering, API Engineering, Database Engineering, Authentication and RBAC, Security Engineering, Integrations and Webhooks |
| **Quality** | Testing and Quality, Accessibility, Performance Optimization, Visual Regression |

Browse each skill's `SKILL.md` from the [catalog index](Docs/SKILL-CATALOG.md).

## Install without cloning the repository

You do **not** need to clone CraftLayer or download its files manually.
From the root of the project where you want the skill, run:

```bash
npx skills add adymire/CraftLayer
```

The installer lets you choose which skills and agent to use. It fetches the
selected skills from GitHub and installs them into the current project.
`npx` runs the community-maintained Skills CLI for this command; you do not
need to install CraftLayer or the CLI globally. The CLI may fetch the source
repository into a temporary location while it works, but you do not clone
the repository yourself or keep a CraftLayer checkout in your project.
The Skills CLI requires Node.js 22.20 or newer.

### Install one skill for a specific agent

Choose a skill ID from the [catalog](Docs/SKILL-CATALOG.md) and replace
`design-intelligence` in the examples if needed:

**OpenCode**

```bash
npx skills add adymire/CraftLayer --skill design-intelligence --agent opencode --copy -y
```

**Claude Code**

```bash
npx skills add adymire/CraftLayer --skill design-intelligence --agent claude-code --copy -y
```

**OpenAI Codex**

```bash
npx skills add adymire/CraftLayer --skill design-intelligence --agent codex --copy -y
```

**Cursor**

```bash
npx skills add adymire/CraftLayer --skill design-intelligence --agent cursor --copy -y
```

**Generic Agent Skills**

```bash
npx skills add adymire/CraftLayer --skill design-intelligence --agent universal --copy -y
```

`--copy` creates regular files instead of symlinks. `-y` skips installer
confirmation prompts; use it when the skill is not already installed.
Omit `-y` if you want to review prompts or check how an existing skill will
be handled.

### Install multiple skills

Pass `--skill` once per skill:

```bash
npx skills add adymire/CraftLayer --skill design-intelligence --skill unslop-engine --skill accessibility --agent cursor --copy -y
```

### Install for your user account

Add `--global` (or `-g`) to make a skill available across projects for your
user instead of installing it into the current repository:

```bash
npx skills add adymire/CraftLayer --skill design-intelligence --agent cursor --global --copy -y
```

### Browse skills first

```bash
npx skills add adymire/CraftLayer --list
```

The CLI lists the 35 available skills and their descriptions without
installing them. For all options, see the [Skills CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add).

### Update or remove installed skills

The Skills CLI tracks project installs in `skills-lock.json`. You can use
its commands later to check for changes, update skills, or remove a
lock-tracked installation:

```bash
npx skills check
npx skills update
npx skills remove design-intelligence
```

These are commands from the external Skills CLI, not a CraftLayer CLI.

### Use the installed skill

Open the project in the selected coding agent and give it a task that
matches the skill. For example:

> Read the `design-intelligence` skill in this project, inspect the existing
> app, then propose a plan for adding an accessible notification settings
> section. Do not edit files until I approve the plan.

Agents that automatically discover Agent Skills-compatible directories
should load the skill when relevant. If it does not appear, verify the
directory, restart or refresh the agent, and check its current official
documentation.

## Choose the right agent folder

When using the install commands above, the Skills CLI selects the
destination. For reference, these are the documented project and
user-level skill locations. Paths can vary by installer and agent version;
the links and review date are in
[Agent Compatibility](Docs/AGENT-COMPATIBILITY.md).

| Agent | Project skill folder | User/global skill folder |
|---|---|---|
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| Generic Agent Skills | `.agents/skills/` | `~/.agents/skills/` |

Use `--global` rather than manually copying files when installing through
the Skills CLI. Project-level installs can be version-controlled with your
project; global installs apply to your user account.

### Skills are not plugins

CraftLayer provides canonical skill files and tested destination
resolution. Installation is currently provided by the independent,
open-source [`skills` CLI](https://github.com/vercel-labs/skills), not by a
CraftLayer CLI. There is no `npx craftlayer` command or CraftLayer plugin
marketplace listing.

You do not need an agent plugin to use these skills. The installer places
the `SKILL.md` files where your selected agent can discover them. Plugin
packaging is a separate feature and is not currently provided by CraftLayer.

The Skills CLI reports that it collects anonymous usage telemetry by
default. To disable it:

```bash
DISABLE_TELEMETRY=1 npx skills add adymire/CraftLayer --skill design-intelligence --agent cursor --copy -y
```

In PowerShell, set the variable for the command like this:

```powershell
$env:DISABLE_TELEMETRY = "1"
npx skills add adymire/CraftLayer --skill design-intelligence --agent cursor --copy -y
```

## What works today

From the repository root, the following development commands are
implemented:

| Command | Purpose |
|---|---|
| `pnpm install` | Install workspace development dependencies |
| `pnpm validate` | Validate registry metadata, skill files, and references |
| `pnpm test` | Run TypeScript unit/integration tests |
| `pnpm test:javascript` | Run the JavaScript example tests with Node.js |
| `pnpm test:python` | Run the Python example tests (Python 3.12 required) |
| `pnpm typecheck` | Type-check the TypeScript workspace |

Agent destination resolution is implemented in
[`packages/agent-adapters`](packages/agent-adapters/src/index.ts). It is a
library used by the repository—not a user-facing installer command—and it
does not write files.

The GitHub install command is provided by the independent `skills` CLI
documented above; it is not a CraftLayer package or command.

## Repository structure

The folders below contain current project work. A folder may hold policy or
an empty registry until real, verified content is ready; CraftLayer does not
add empty skill/theme placeholders.

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/         Bug-report and skill-proposal forms
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/              CI for validation, tests, and type-checking
├── Docs/                       Project documentation and master build brief
├── assets/                     Asset policy and registry
├── CODE_OF_CONDUCT.md          Community standards
├── evals/                      Human-run skill evaluation cases
├── packages/
│   ├── agent-adapters/         Agent skill destination resolution
│   └── validation/             Registry and SKILL.md validation
├── references/                 Source research policy and registry
├── rules/                      Shared design, engineering, and safety rules
├── scripts/                    Cross-platform Python test launcher
├── skills/                     Skill catalog and registry.json
├── templates/                  Skill and project-audit templates
├── CONTRIBUTING.md             Contribution workflow
├── LICENSE                     MIT license
├── package.json                Workspace commands and requirements
├── pnpm-lock.yaml              Reproducible dependency lockfile
└── pnpm-workspace.yaml         pnpm workspace definition
```

See [Repository Structure](Docs/REPOSITORY-STRUCTURE.md) for what is
implemented versus planned, and [Architecture](Docs/ARCHITECTURE.md) for
package boundaries and decisions.

## Develop and validate CraftLayer

### Requirements

- Node.js 22 or later
- pnpm 11 (the repository pins pnpm 11.25.0 through `package.json`)
- Python 3.12 to run the Python example tests

Install dependencies and run the checks:

```sh
pnpm install
pnpm validate
pnpm test
pnpm test:javascript
pnpm test:python
pnpm typecheck
```

On Windows, the Python test script locates Python 3.12 through the `py`
launcher. If Python is installed in a non-standard location, set
`PYTHON_EXECUTABLE` to its executable path before running
`pnpm test:python`.

The validator checks that each registry entry maps to a skill directory,
the frontmatter agrees with the registry, references resolve, and every
skill has non-empty `When to use`, `When not to use`, `Workflow`, and
`Validation` sections. This is a structural check—not a substitute for
reviewing whether the advice is correct and useful.

## Contributing

CraftLayer welcomes focused improvements to skill quality, examples,
validation, documentation, and tooling. Before opening a pull request, read
[CONTRIBUTING.md](CONTRIBUTING.md), the
[Skill Authoring Guide](Docs/SKILL-AUTHORING.md), and the
[Licensing Policy](Docs/LICENSING.md).

In short:

1. Pick a clear user problem and check existing issues or skills for overlap.
2. Keep the change scoped and preserve existing behavior.
3. For skill changes, include practical guidance, edge cases, and observable
   acceptance checks; avoid generic filler.
4. Verify third-party sources and licenses. Links to references are not
   permission to copy their content.
5. Run validation, relevant tests, and type-checking; state anything you
   could not run.
6. Update documentation and registry metadata when behavior or skill
   content changes.

See [Contributing](CONTRIBUTING.md) for the full review checklist.

## Community and reporting

- [Open an issue](https://github.com/adymire/CraftLayer/issues/new/choose) to
  report a reproducible bug or propose a skill.
- Read the [Community Standards](CODE_OF_CONDUCT.md) before participating.
- For security-sensitive reports, do not post exploit details, credentials,
  or private data publicly; use GitHub's private reporting/contact options
  for the maintainers.

## Roadmap

1. **Foundation and catalog:** schema, validator, documentation, 35 skill
   drafts, and agent destination resolution.
2. **Skill evaluation:** evaluate and refine the initial eight core skills
   against the cases in `evals/` before publishing them.
3. **CLI and selective installer:** implement safe, pinned GitHub downloads,
   project/global installation, and overwrite protection.
4. **Themes and catalog growth:** add complete themes and further skill
   families with verified licensing.
5. **Release readiness:** test real agent discovery, installer security, and
   documented commands before publishing.

The detailed plan and current state live in
[Roadmap](Docs/ROADMAP.md) and
[Implementation Status](Docs/IMPLEMENTATION-STATUS.md).

## License

Original CraftLayer code and skill content are available under the
[MIT License](LICENSE). Third-party works remain under their own licenses;
see the [licensing policy](Docs/LICENSING.md).
