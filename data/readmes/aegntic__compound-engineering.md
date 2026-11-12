# Compound Engineering

> Portable AI-powered development tools for any coding agent.

**[Claude Code](https://docs.anthropic.com/en/docs/claude-code) · [GitHub Copilot](https://github.com/features/copilot) · [OpenCode](https://github.com/opencode-ai/opencode)**

29 specialized agents · 26 commands · 28 skills · MIT License

Each unit of engineering work should make subsequent units of work easier — not harder.

---

## Why Compound Engineering?

| Problem | Solution |
|---------|----------|
| AI agents solve the same problem twice | `/workflows:compound` documents every solved problem as searchable knowledge |
| Code review is shallow and generic | 17 specialized reviewers per language and domain (Rust ownership, TypeScript types, OWASP security) |
| Planning disconnected from execution | Pipeline produces artifacts that feed the next phase — nothing is lost |
| One-shot features need manual handoffs | `/lfg` chains plan → deepen → work → review → ship autonomously |
| Knowledge leaves with the developer | `docs/solutions/` compounds institutional memory in git |

## At a Glance

```mermaid
pie title Included components
    "Agents — 29" : 29
    "Commands — 26" : 26
    "Skills — 28" : 28
```

## Install

For **Claude Code**, **Copilot CLI**, **OpenCode**, or any agent that supports skills/commands.

```bash
# Claude Code — install as plugin
claude install-plugin https://github.com/aegntic/compound-engineering

# Or clone directly into your skills directory
git clone https://github.com/aegntic/compound-engineering.git \
  ~/.claude/skills/compound-engineering

# Configure for your stack (detects languages, frameworks, picks reviewers)
/setup
```

## The Workflow

Compound Engineering provides a progression of workflows that build on each other. Each phase produces artifacts that feed the next, so nothing is lost and context compounds.

```mermaid
flowchart LR
    constitution["Define<br/>/workflows:constitution"]
    ideate["Discover<br/>/workflows:ideate"]
    brainstorm["Explore<br/>/workflows:brainstorm"]
    plan["Plan<br/>/workflows:plan"]
    deepen["Deepen<br/>/deepen-plan"]
    work["Execute<br/>/workflows:work"]
    review["Review<br/>/workflows:review"]
    compound["Compound<br/>/workflows:compound"]
    learnings[("docs/solutions/<br/>searchable learnings")]

    constitution --> ideate --> brainstorm --> plan --> deepen --> work --> review --> compound
    compound -->|documents| learnings
    learnings -. informs future work .-> plan
```

| Phase | Command | What it does |
|-------|---------|-------------|
| **Define** | `/workflows:constitution` | Establish durable project principles in `docs/constitution.md` |
| **Discover** | `/workflows:ideate` | Scan the repo, generate improvement ideas, rank them |
| **Explore** | `/workflows:brainstorm` | Establish WHY and WHAT — problem narrative, user story, architectural context |
| **Plan** | `/workflows:plan` | Structured implementation plan with tasks, dependencies, and evidence contracts |
| **Deepen** | `/deepen-plan` | Expand thin spots in the plan before execution begins |
| **Execute** | `/workflows:work` | TDD-driven execution with red-green-refactor evidence capture |
| **Review** | `/workflows:review` | Multi-agent code review using your configured reviewers |
| **Compound** | `/workflows:compound` | Document the solved problem as searchable knowledge in `docs/solutions/` |

### One-Shot Autonomous Mode

For features that don't need exploration — go straight to shipping:

```bash
/lfg add user authentication with JWT
```

This chains the entire pipeline automatically: plan → deepen → work → review → resolve → test → video → done.

For parallel swarm execution:

```bash
/slfg add user authentication with JWT
```

## Agents

### Design (3)

Review and iterate on visual implementation.

| Agent | Purpose |
|-------|---------|
| `design-implementation-reviewer` | Compare live UI against Figma designs |
| `design-iterator` | Iterative UI refinement through screenshot-analyze-improve cycles |
| `figma-design-sync` | Detect and fix visual differences between implementation and Figma |

### Research (8)

Gather knowledge before and during implementation.

| Agent | Purpose |
|-------|---------|
| `best-practices-researcher` | Research external best practices and documentation |
| `framework-docs-researcher` | Gather framework/library documentation and examples |
| `git-history-analyzer` | Archaeological analysis of git history |
| `issue-intelligence-analyst` | Analyze GitHub issues for recurring patterns |
| `learnings-researcher` | Search past solutions in `docs/solutions/` |
| `repo-research-analyst` | Research repository structure and conventions |

### Review (17)

Language-specific and cross-cutting code review.

| Agent | Purpose |
|-------|---------|
| `agent-native-reviewer` | Ensure agent-native action parity |
| `architecture-strategist` | SOLID compliance and clean architecture review |
| `code-simplicity-reviewer` | Complexity elimination and readability |
| `data-integrity-guardian` | Database migration and data model safety |
| `data-migration-expert` | Validate data migrations against reality |
| `deployment-verification-agent` | Go/No-Go deployment checklists |
| `frontend-race-conditions-reviewer` | Async UI race conditions and stale state |
| `laravel-reviewer` | Laravel 11+ / PHP 8.3+ best practices |
| `nestjs-reviewer` | NestJS simplicity, performance, security |
| `pattern-recognition-specialist` | Design patterns and anti-patterns |
| `performance-oracle` | Performance bottlenecks and algorithmic complexity |
| `python-reviewer` | Pythonic patterns, type safety, security |
| `rust-reviewer` | Ownership correctness, unsafe discipline, zero-cost abstractions |
| `schema-drift-detector` | Schema snapshot and artifact drift detection |
| `security-sentinel` | OWASP Top 10 security audit |
| `typescript-reviewer` | Type safety, modern patterns, maintainability |
| `vue-reviewer` | Vue.js/Nuxt best practices and performance |

### Workflow (3)

Automate development operations.

| Agent | Purpose |
|-------|---------|
| `bug-reproduction-validator` | Systematically reproduce and validate bug reports |
| `pr-comment-resolver` | Address PR review comments with requested changes |
| `spec-flow-analyzer` | Analyze specs for user flow completeness |

## Commands

### Workflows

The core progression — each produces artifacts that feed the next.

| Command | Description |
|---------|-------------|
| `/workflows:constitution` | Define project engineering principles |
| `/workflows:ideate` | Generate and rank improvement ideas |
| `/workflows:brainstorm` | Explore WHY and WHAT before planning |
| `/workflows:plan` | Structured implementation planning |
| `/workflows:architecture` | Architecture review and improvement |
| `/workflows:work` | TDD-driven execution with evidence capture |
| `/workflows:review` | Multi-agent code review |
| `/workflows:compound` | Document solved problems as searchable knowledge |
| `/workflows:compound-refresh` | Refresh stale learnings against current codebase |

### Operations

| Command | Description |
|---------|-------------|
| `/lfg` | Full autonomous pipeline: plan → work → review → ship |
| `/slfg` | Same as `/lfg` but with parallel swarm execution |
| `/ralph-loop` | Red-green-refactor loop with completion promise |
| `/cancel-ralph` | Cancel an active ralph loop |
| `/triage` | Triage GitHub issues |
| `/reproduce-bug` | Systematic bug reproduction |
| `/resolve_parallel` | Resolve PR comments in parallel |
| `/resolve_todo_parallel` | Resolve TODO items in parallel |
| `/test-browser` | Browser-based testing |
| `/changelog` | Generate changelog |
| `/deepen-plan` | Expand thin spots in a plan |
| `/deploy-docs` | Deploy documentation site |
| `/feature-video` | Record feature walkthrough video |
| `/heal-skill` | Repair a broken skill |
| `/create-agent-skill` | Create a new agent or skill |
| `/report-bug` | Report a bug with structured context |
| `/generate_command` | Generate a new command |

## Skills

| Skill | Purpose |
|-------|---------|
| `agent-browser` | Browser automation via Vercel agent-browser CLI |
| `agent-native-architecture` | Build applications where agents are first-class citizens |
| `agent-native-audit` | Scored audit of agent-native architecture principles |
| `brainstorming` | Explore user intent before implementing |
| `caveman` | Ultra-compressed communication (~75% token reduction) |
| `compound-docs` | Capture solved problems as searchable documentation |
| `compounding-operating-system` | Evaluate strategic decisions for long-term compounding and survivability |
| `compound-refresh` | Refresh stale learnings against current codebase |
| `create-agent-skills` | Expert guidance for authoring coding agent skills |
| `document-review` | Refine brainstorm/plan documents |
| `file-todos` | File-based todo tracking system |
| `finishing-branch` | Verify quality and clean up feature branches |
| `frontend-design` | Production-grade frontend interfaces |
| `gemini-imagegen` | Image generation via Gemini API |
| `git-worktree` | Git worktree management for parallel development |
| `grill-me` | Relentlessly interview user about a plan or design |
| `i-have-adhd` | [ADHD-friendly, action-first responses](https://github.com/ayghri/i-have-adhd) |
| `ideate` | Generate and evaluate grounded improvement ideas |
| `laravel-conventions` | Modern Laravel 11+ / PHP 8.3+ coding standards |
| `orchestrating-swarms` | Multi-agent swarm orchestration |
| `rclone` | Cloud storage file management via rclone |
| `resolve-pr-parallel` | Resolve PR comments using parallel processing |
| `setup` | Configure review agents for your stack |
| `skill-creator` | Guide for creating effective skills |
| `systematic-debugging` | Structured 4-phase debugging methodology |
| `ubiquitous-language` | DDD-style ubiquitous language glossary extraction |

## Project Structure

```
compound-engineering/
├── agents/                # 29 specialized AI agents
│   ├── design/            # Visual design review
│   ├── research/          # Knowledge gathering
│   ├── review/            # Code review (language + cross-cutting)
│   └── workflow/          # Development operations
├── commands/              # 26 invocable slash commands
│   └── workflows/         # Workflow orchestrations and reference templates
├── skills/                # 28 skills (references, templates, scripts)
├── platforms/             # Platform-specific hooks
└── plugin.yaml            # Plugin metadata
```

## Docs Convention

Workflows produce structured output in your project's `docs/` directory:

```
docs/
├── constitution.md        # Project principles (keep in git)
├── solutions/             # Compounded learnings (keep in git)
├── ideation/              # Ideation artifacts (gitignore)
├── plans/                 # Implementation plans (gitignore)
├── brainstorms/           # Brainstorm documents (gitignore)
└── execution-sessions/    # Work session logs (gitignore)
```

Solutions are institutional memory — the compounding payoff. Everything else is ephemeral scaffolding.

## Configuration

Run `/setup` to create `compound-engineering.local.md` in your project root. It auto-detects your stack and selects the right language reviewers for `/workflows:review`.

## MCP Integration

Includes Context7 MCP server for enhanced documentation lookup during research and review.

## Adding Components

### New Agent

Create `agents/{category}/{name}.md`:

```markdown
---
name: my-reviewer
description: Reviews code for X, Y, Z
model: claude-sonnet-4.6
---

## Mission
...

## Focus Areas
...

## Report
...
```

### New Command

Create `commands/{name}.md`:

```markdown
---
name: my-command
description: What this command does
argument-hint: '[optional arguments]'
---

# Command Title

Instructions...
```

### New Skill

Create `skills/{name}/SKILL.md` plus optional `references/`, `scripts/`, or `templates/` subdirectories.

## Compatibility

| Platform | Status | Install |
|----------|--------|---------|
| Claude Code | Supported | `claude install-plugin` |
| GitHub Copilot | Supported | Copy agents + skills |
| OpenCode | Supported | Copy agents + skills |
| Any MCP-compatible agent | Skills are plain markdown | Copy what you need |

## Languages & Frameworks

Built-in reviewers for: **Rust** · **TypeScript** · **Python** · **Laravel/PHP** · **Vue/Nuxt** · **NestJS** · **Frontend (React, vanilla)** · **SQL/Database migrations**

## Contributing

1. Fork the repo
2. Create your branch (`git checkout -b feat/my-agent`)
3. Add agent/command/skill with frontmatter
4. Update README counts
5. Open a PR

See `.github/ISSUE_TEMPLATE/` for agent and feature request templates.

## License

MIT — use freely in personal and commercial projects.

---

<!-- SEO: AI coding agent tools, Claude Code plugin, Copilot skills, OpenCode agents, compound engineering, TDD workflow, code review automation, AI-powered development, knowledge compounding, red green refactor, autonomous coding, AI agent orchestration, multi-agent code review, language-specific code reviewers, Rust TypeScript Python Laravel Vue NestJS, OWASP security audit, deployment verification, schema drift detection, brainstorming workflow, implementation planning -->
