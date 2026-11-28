# Opencode Configuration

Personal multi-agent configuration for [Opencode](https://opencode.ai) — a programmable AI development environment with scoped agents, permission controls, and framework-specific skills.

---

## 🤖 Agent Architecture

The configuration follows a role-based multi-agent design:

### 💬 `ask`
Quick answers to questions. Read-only, no skills.

- Answers technical and code questions directly and concisely
- Explains trade-offs, patterns, and concepts on demand
- Never modifies files or executes commands
- No skills loaded — low overhead, fast responses

### 🏗️ `architect`
Staff-level software architect. Read-only.

- Analyzes requirements and surfaces trade-offs
- Produces 2-3 architectural options with pros/cons
- Outputs ADRs and phased implementation plans
- Cannot modify files or execute commands

### 🔨 `build`
Senior full-stack developer. The main coding agent.

- Follows existing codebase patterns and conventions
- Writes production-ready code with proper error handling
- Generates tests for new functionality
- Has access to all framework skills

### ♻️ `refactor`
Behavior-preserving improvement specialist.

- Improves readability, maintainability, and structure
- Applies SOLID principles selectively — not dogmatically
- Documents invariants before making changes
- Preserves public APIs and observable behavior

### 🔍 `review`
Code reviewer and security analyst. Read-only.

- Evaluates correctness, security, maintainability, performance, and testing
- Classifies issues as BLOCKER / WARNING / SUGGESTION / QUESTION / PRAISE
- Thinks like an attacker — flags injection, auth bypass, data exposure
- Explicitly states whether a change is safe to merge

---

## 📚 Skills

Framework-specific reference material loaded on demand by agents via the `skill` tool. These are kept locally in this repo rather than fetched from remote URLs.

| Skill | Description |
|-------|-------------|
| `vercel-react-best-practices` | React/Next.js performance optimization (57 rules across 8 categories) |
| `vue-best-practices` | Vue 3 Composition API patterns and workflow |
| `nestjs-best-practices` | NestJS architecture, DI, security, and performance (40 rules) |
| `mcp-builder` | Guide for building MCP servers with TypeScript or Python |

General engineering knowledge (architecture, security, DevOps, QA, etc.) is baked directly into agent prompts instead of loaded as separate skills.

---

## ⚙️ Model Configuration

This setup uses GitHub Copilot-hosted models:

- `github-copilot/claude-sonnet-4.6` — ask, build and refactor agents; default model
- `github-copilot/claude-opus-4.7` — architect agent
- `github-copilot/gpt-5.3-codex` — review agent

**Requirements:** An active GitHub Copilot subscription with Opencode authenticated via GitHub.

### 🔄 Switching Providers

Opencode supports multiple providers — see the [provider docs](https://opencode.ai/docs/providers/).

Update the model in `opencode.jsonc`:

```json
"model": "anthropic/claude-opus-4-5"
```

```json
"model": "openai/gpt-4.1"
```

### 🔑 Environment Variables

Configure the relevant key for your provider:

```bash
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GITHUB_TOKEN=
```

---

## 🔒 Permissions

- Safe, read-only commands (`git status`, `ls`, etc.) run automatically
- Broad or destructive commands require confirmation
- Skill usage is scoped per agent — only framework skills are auto-allowed
- `architect`, `review`, and `ask` agents cannot modify files or run commands

---

## 📦 Installation

### 1. Clone

```bash
git clone https://github.com/<your-username>/opencode-config.git
cd opencode-config
```

### 2. Link Configuration

Opencode reads config, agents, and skills from `~/.config/opencode/`. The recommended approach is symlinks so the repository remains your single source of truth.

**macOS / Linux**

```bash
mkdir -p ~/.config/opencode
ln -sf "$(pwd)/opencode.jsonc" ~/.config/opencode/opencode.jsonc
ln -sfn "$(pwd)/agents" ~/.config/opencode/agents
ln -sfn "$(pwd)/skills" ~/.config/opencode/skills
```

**Windows (PowerShell, run as Administrator)**

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\opencode"
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.config\opencode\opencode.jsonc" `
  -Target "$PWD\opencode.jsonc"
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.config\opencode\agents" `
  -Target "$PWD\agents"
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.config\opencode\skills" `
  -Target "$PWD\skills"
```

**Alternative — copy instead of symlink**

```bash
cp opencode.jsonc ~/.config/opencode/opencode.jsonc
cp -r agents ~/.config/opencode/agents
cp -r skills ~/.config/opencode/skills
```

> Note: If you copy, remember to re-copy after pulling changes.

### 3. Update

```bash
git pull
```

No additional steps required when using symlinks.

---

## 💡 Principles

- Separation of thinking and execution
- Behavior preservation during refactoring
- Explicit architectural trade-off analysis
- Permission-scoped tool access
- Minimal, production-focused changes
- General knowledge in prompts, framework specifics in skills

---

## 📄 License

MIT
