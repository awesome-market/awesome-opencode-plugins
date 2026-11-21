# Slopnought

<img src="assets/slopnought.png" alt="Slopnought" width="300">

An AI coding skill that makes generated code maintainable. Not just "feature complete" — **future developer friendly.**

LLMs are great at solving today's problem. They're terrible at leaving code you can safely change tomorrow. Slopnought fixes that by injecting maintainability constraints directly into AI agent prompts at session start.

---

## The Problem

AI-generated code often works today but becomes a liability tomorrow. Business logic is duplicated, architecture drifts by accident, and nobody documented *why* anything was built the way it was. Slopnought makes maintainability a first-class requirement — enforced while code is written, not as an afterthought.

---

## Architecture

Slopnought utilizes a clean, two-layer integration architecture designed to work across any agent harness:

```
┌────────────────────────────────────────────────────────┐
│               Harness-Agnostic Skills                  │
│  Main instructions (SKILL.md) & Ref Mode instructions   │
│  The agent already knows its own tools.                 │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│               Bootstrap Injectors                      │
│ Hooks, plugins, & context files loaded at session start│
└────────────────────────────────────────────────────────┘
```

1. **Harness-Agnostic Skills**: Core rules and procedures for writing clean, structured code (`skills/slopnought/SKILL.md`). Skills describe actions ("read a file", "edit a file") — the agent translates them to its own tools.
2. **Bootstrap Injectors**: Environment-specific configuration files and hooks that inject the instructions into the agent's context (e.g., hooks, `.pi/`, `antigravity-plugin/`, or `gemini-extension.json`).

---

## Key Features & Modes

### 1. Code Generation Mode
Automatically active whenever an agent produces code. It enforces:
* **Strict Boundaries**: Clear separation between UI, business logic, data access, and infrastructure.
* **Size Limits**: Hard ceiling on file sizes (under 200–400 lines) and functions (under 20–40 lines).
* **Defensive Errors**: Error messages that explain exactly what happened and how to fix it.
* **Documented Intent**: Inline comments explaining *why* a choice was made, rather than *what* the code is doing.

### 2. Codebase Refactoring Mode (`/slopnought-audit`)
When invoked, the agent performs a comprehensive tech debt audit of the codebase, evaluating:
* Hidden coupling and architectural drift.
* Duplicate code patterns and copy-paste structures.
* Brittle shortcuts (magic numbers, swallowed exceptions, unconfigured environments).
* Test coverage gaps.
* Security risks.
It outputs a prioritized remediation plan and can apply fixes upon approval.

### 3. Anti-Patterns Catalog
A compiled reference of 7 common LLM-generated code failure modes:
1. Duplicated logic.
2. Context collapse (ignoring surrounding patterns).
3. Brittle shortcuts.
4. Leaky abstractions.
5. Ghost dependencies.
6. Silent/generic errors.
7. Commented-out dead code.

---

## Repository Structure

```
├── skills/slopnought/
│   ├── SKILL.md                          # Main skill instructions & rules
│   ├── references/
│   │   ├── anti-patterns.md              # Common LLM code failure modes
│   │   ├── code-generation-mode.md       # Detailed guide for writing new code
│   │   ├── refactoring-mode.md           # Instructions for auditing codebases
│   │   └── architecture-records.md       # Guidelines for writing ADRs
│   └── assets/
│       └── adr-template.md               # Markdown template for Architecture Decision Records
├── skills/slopnought-audit/
│   └── SKILL.md                          # Audit mode skill instructions
├── hooks/                                # Bootstrap injection scripts
│   ├── session-start                     # Bash bootstrap (Claude Code / Copilot)
│   ├── session-start.py                  # Python fallback
│   ├── session-start-codex               # Bash bootstrap (Codex CLI)
│   ├── session-start-codex.py            # Python fallback (Codex CLI)
│   ├── run-hook.cmd                      # Windows polyglot wrapper
│   ├── hooks.json                        # Claude Code hook config
│   ├── hooks-codex.json                  # Codex CLI hook config
│   └── hooks-cursor.json                 # Cursor hook config
├── .claude-plugin/plugin.json            # Claude Code manifest
├── .codex-plugin/plugin.json             # Codex CLI manifest
├── .cursor-plugin/plugin.json            # Cursor manifest
├── .kimi-plugin/plugin.json              # Kimi Code manifest
├── .opencode/plugins/slopnought.js       # OpenCode plugin module
├── .pi/extensions/slopnought.ts          # Pi extension module
├── antigravity-plugin/plugin.json        # Antigravity manifest
├── gemini-extension.json                 # Gemini CLI manifest
├── GEMINI.md                             # Gemini context file (@-includes)
├── ANTIGRAVITY.md                        # Antigravity context file
├── AGENTS.md                             # Agent instructions
├── install-agy.sh                        # Antigravity installer (bash)
├── install-agy.ps1                       # Antigravity installer (PowerShell)
├── package.json                          # Plugin metadata and dependencies
└── docs/                                 # Documentation
```

---

## Supported Environments

Slopnought supports:
* **Claude Code** — clone + copy skills directory
* **Codex CLI / Codex App** — clone + plugin config
* **Cursor** — clone + copy skills directory
* **Copilot CLI** — reuses Claude Code setup
* **Gemini CLI** — clone + context file (auto-loaded)
* **OpenCode** — git URL plugin spec
* **Pi** — git URL package spec
* **Antigravity** — clone + `agy plugin install`
* **Kimi Code** — clone + plugin config
* **Factory Droid** — reuses Claude Code setup

---

## Installation & Setup

**Prerequisites:** Git, Bash (Git Bash on Windows), Python 3.6+

### Claude Code

```bash
git clone https://github.com/BhumitChaudhry/Slopnought.git
cp -r Slopnought/skills/slopnought ~/.claude/skills/slopnought
cp -r Slopnought/skills/slopnought-audit ~/.claude/skills/slopnought-audit
```

### OpenCode

Add to your `opencode.json`:
```json
{
  "plugin": ["slopnought@git+https://github.com/BhumitChaudhry/Slopnought.git"]
}
```

### Pi

```bash
pi install git:github.com/BhumitChaudhry/Slopnought
```

### Antigravity

```bash
git clone https://github.com/BhumitChaudhry/Slopnought.git
cd Slopnought && bash install-agy.sh
```

### Other agents

Clone the repo and point your agent's context files at `skills/slopnought/SKILL.md`. See [docs/installation.md](docs/installation.md) for agent-specific details.

---

## The Core Principles

Every code change must satisfy these five rules:
1. **Maintainability is a requirement, not a nice-to-have.** A fast, working solution that cannot be safely modified later is a liability.
2. **Optimize for the next reader, not for fewest keystrokes now.** Write code as if the next developer has zero context.
3. **Every non-obvious decision needs a visible reason.** Document the *why*, either through inline comments, docstrings, or Architecture Decision Records (ADRs).
4. **Consistency beats local optimality.** Adhere to existing patterns in the codebase rather than quietly introducing competing paradigms.
5. **The 2:00 AM Rule:** If you wouldn't want to debug it at 2:00 AM with no memory of writing it, don't ship it.

---

## License

MIT

