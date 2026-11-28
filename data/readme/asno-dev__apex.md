<p align="center">
  <img src="https://img.shields.io/npm/v/@asno-dev/apex?style=flat-square&color=0ea5e9" alt="npm version" />
  <img src="https://img.shields.io/npm/dm/@asno-dev/apex?style=flat-square&color=38bdf8" alt="npm downloads" />
  <img src="https://img.shields.io/npm/l/@asno-dev/apex?style=flat-square&color=22c55e" alt="license" />
  <img src="https://img.shields.io/badge/agents-13-blueviolet?style=flat-square" alt="agents" />
  <img src="https://img.shields.io/badge/tools-56-orange?style=flat-square" alt="tools" />
  <img src="https://img.shields.io/badge/adapters-13-blue?style=flat-square" alt="adapters" />
  <img src="https://img.shields.io/badge/node-%3E%3D18-green?style=flat-square" alt="node" />
</p>

<h1 align="center">⚡ APEX</h1>

<p align="center">
  <strong>10-Agent Senior Engineering Team for Any CLI Coding Agent</strong>
</p>

<p align="center">
  A zero-dependency orchestrator that routes your requests to 10 specialist AI agents — each with domain expertise, purpose-built tools, and the ability to dynamically call peers mid-task. Works with <strong>13 coding agents</strong> out of the box.
</p>

<p align="center">
  <a href="#-agents">Agents</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-mcp-servers">MCP Servers</a> •
  <a href="#%EF%B8%8F-commands">Commands</a> •
  <a href="#-composio-integration">Composio</a> •
  <a href="#%F0%9F%94%8B-mirage-vfs">Mirage VFS</a> •
  <a href="#-license">License</a>
</p>

---

## Quick Start

```bash
npx @asno-dev/apex <agent>   # Replace <agent> with your coding agent (see below)
```

One command. Installs shared files, agent configs, MCP servers, and commands.

Then use `@agentName` in your coding agent:

```
@arch refactor this                → Max compresses your code
@ui build a login form             → Zara paints a WCAG AA form
@debug fix this error              → Kai runs 5-step debug protocol
@perf this is slow                 → Rex profiles & optimizes
@sec review auth code              → Vex scans for OWASP Top 10
@infra dockerize this              → Io outputs production-grade config
@nova any ideas?                   → Nova proposes non-obvious angles
@reed best caching strategy        → Dr. Reed compares options with evidence
@review check this code            → Rila gives structured PR review
@flex what's the MVP?              → Flex scores Value×Cost and cuts scope
```

---

## Agents

APEX ships with **10 specialist agents**, each with a unique persona, domain expertise, and set of purpose-built tools.

| Badge | Tag | Name | Role | Specialty |
|:-----:|:---:|:----:|:-----|:----------|
| `[Arch]` | `@arch` | **Max** | Architect | System design, refactoring, structure. Compresses 50→1 line. |
| `[UI]` | `@ui` | **Zara** | UI/UX Designer | Mood-first, anti-slop. shadcn/ui + Tailwind. WCAG AA. 10 palettes. |
| `[Dbg]` | `@debug` | **Kai** | Debugger | 5-step protocol: reproduce → isolate → hypothesize → fix → prevent. |
| `[Perf]` | `@perf` | **Rex** | Performance Engineer | Profile first. Algorithm → DB → bundle → render. Baseline → optimize → measure. |
| `[Sec]` | `@sec` | **Vex** | Security Engineer | OWASP Top 10. CRITICAL/HIGH/MEDIUM. Every input is malicious. |
| `[Inf]` | `@infra` | **Io** | Infrastructure | Docker/k8s/CI-CD. Multi-stage builds. Non-root. Rollback always. |
| `[Nov]` | `@nova` | **Nova** | Creative | Non-obvious angles. Lib + npm + POC + downside analysis. |
| `[Res]` | `@reed` | **Dr. Reed** | Researcher | Evidence-based. ≥2 options with O(?) complexity. No opinions without data. |
| `[Rev]` | `@review` | **Rila** | Code Reviewer | Blocking → Suggestions → Praise. Specific praise always. |
| `[Fnd]` | `@flex` | **Flex** | Founder / PM | Value(1-3) × Cost(1-3). Ships 60%, defers 30%, kills 10%. |

### Routing

| Your Request | Routed To |
|:-------------|:----------|
| Code is long/complex/messy | `@arch` |
| Build UI / component / page | `@ui` |
| Error / bug / crash / undefined | `@debug` |
| Slow / memory / performance | `@perf` |
| Auth / input / secrets / vuln | `@sec` |
| Deploy / Docker / CI / k8s | `@infra` |
| New idea / library / creative | `@nova` |
| Best way / which / research | `@reed` |
| Review / PR / merge / quality | `@review` |
| Scope / MVP / what to build | `@flex` |

### Modes

| Mode | Usage | Description |
|:----:|:------|:------------|
| **Direct** | `@agent` | That agent = main agent with full authority. Calls peers via `@peerName`. |
| **Team (default)** | auto | Orchestrator routes to best agent. Agent calls peers dynamically. |
| **Select** | `/apex select a,b` | Only those agents active until changed. |

### Task States

```
🧠 Thinking  →  🔍 Exploring  →  ⚡ Working  →  🔧 Fixing  →  ✅ Verifying  →  ✨ Complete
```

---

## Installation

One command per agent. No auto-detection, no interactive prompts.

### Claude Code

```bash
npx @asno-dev/apex claude-code
```

<details>
<summary><strong>.claude/plugin.json</strong> — 10 subagents, 8 commands, 3 MCP servers, lifecycle hooks</summary>

```json
{
  "name": "apex",
  "version": "3.0.0",
  "hooks": "./hooks.json",
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"], "type": "local" },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"], "type": "local" },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"], "type": "local" }
  },
  "subagents": ["agents/arch.md", "agents/ui.md", "agents/debug.md", "agents/perf.md", "agents/sec.md", "agents/infra.md", "agents/nova.md", "agents/reed.md", "agents/review.md", "agents/flex.md"],
  "commands": ["commands/apex.md", "commands/apex-docs.md", "commands/apex-excel.md", "commands/apex-ppt.md", "commands/apex-composio-setup.md", "commands/apex-composio-status.md", "commands/apex-composio-sync.md", "commands/apex-mirage.md"]
}
```
</details>

**Installs:** `.claude/plugin.json`, `.claude/hooks.json`, `.claude/agents/` (10 `.md`), `.claude/commands/` (8 `.md`), `.claude/hooks/` (4)

**Auto-detects** — Claude Code loads `.claude/plugin.json` on startup.

---

### Codex CLI

```bash
npx @asno-dev/apex codex
```

<details>
<summary><strong>.codex/</strong> — plugin.json, codex.json, config.toml, 10 agents, 9 commands, plugins/apex.json</summary>

```json
{
  "name": "apex",
  "version": "3.0.0",
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"], "type": "local" },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"], "type": "local" },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"], "type": "local" }
  },
  "subagents": ["agents/arch.toml", "agents/ui.toml", "agents/debug.toml", "agents/perf.toml", "agents/sec.toml", "agents/infra.toml", "agents/nova.toml", "agents/reed.toml", "agents/review.toml", "agents/flex.toml"],
  "commands": ["commands/apex.md", "commands/apex-team.md", "commands/apex-docs.md", "commands/apex-excel.md", "commands/apex-ppt.md", "commands/apex-composio-setup.md", "commands/apex-composio-status.md", "commands/apex-composio-sync.md", "commands/apex-mirage.md"]
}
```
</details>

**Installs:** `.codex/plugin.json`, `.codex/codex.json`, `.codex/config.toml`, `.codex/plugins/apex.json`, `.codex/agents/` (10 `.toml`), `.codex/commands/` (9 `.md`), `.codex/SKILLS.md`

**Auto-detects** — Codex CLI loads `.codex/plugin.json` on startup (v0.142+).

**Prerequisite:** `npm install -g @openai/codex` (v0.142.5+)

---

### Gemini CLI

```bash
npx @asno-dev/apex gemini
```

<details>
<summary><strong>.gemini/gemini-extension.json</strong> — 8 commands, 3 MCP servers (agents auto-discovered from <code>.gemini/agents/*.md</code>)</summary>

```json
{
  "name": "apex",
  "version": "3.0.0",
  "mcpServers": {
    "apex-hands": { "command": "node apex/src/hands-server.mjs", "type": "local" },
    "mirage-vfs": { "command": "node apex/src/mirage-server.mjs", "type": "local" },
    "apex-composio": { "command": "node apex/src/composio-server.mjs", "type": "local" }
  },
  "commands": [
    {"name": "apex", "file": "commands/apex.md"},
    {"name": "apex-team", "file": "commands/apex.md"},
    {"name": "apex-docs", "file": "commands/apex-docs.md"},
    {"name": "apex-excel", "file": "commands/apex-excel.md"},
    {"name": "apex-ppt", "file": "commands/apex-ppt.md"},
    {"name": "apex-composio-setup", "file": "commands/apex-composio-setup.md"},
    {"name": "apex-composio-status", "file": "commands/apex-composio-status.md"},
    {"name": "apex-composio-sync", "file": "commands/apex-composio-sync.md"},
    {"name": "apex-mirage", "file": "commands/apex-mirage.md"}
  ]
}
```

Agents (`@arch`, `@ui`, etc.) are auto-discovered from `.gemini/agents/*.md` YAML frontmatter — no `agents` array in the extension JSON to avoid duplicate warnings.
</details>

**Installs:** `.gemini/gemini-extension.json`, `.gemini/agents/` (10 `.md`), `.gemini/commands/` (8 `.md`)

**Then:** `gemini extensions install .gemini`

---

### Cursor

```bash
npx @asno-dev/apex cursor
```

<details>
<summary><strong>.cursor/mcp.json</strong> — MCP + rules for Cursor</summary>

```json
{
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"], "type": "local" },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"], "type": "local" },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"], "type": "local" }
  }
}
```
</details>

**Installs:** `.cursor/mcp.json`, `.cursor/rules/apex.mdc`, `.cursor/agents/` (10 `.mdc`), `.cursor/commands/` (8 `.md`)

**Auto-detects** — Cursor loads `.cursor/mcp.json` and `.cursor/rules/apex.mdc` on project open.

---

### Cline / Kilo

```bash
npx @asno-dev/apex cline
```

<details>
<summary><strong>.cline/mcp.json</strong> — MCP + rules for Cline</summary>

```json
{
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"], "type": "local" },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"], "type": "local" },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"], "type": "local" }
  }
}
```
</details>

**Installs:** `.cline/mcp.json`, `.cline/rules/apex.mdc`, `.cline/agents/` (10 `.mdc`), `.cline/commands/` (8 `.md`), `.clinerules`

**Auto-detects** — Cline loads `.cline/` config on project open.

---

### OpenCode

```bash
npx @asno-dev/apex opencode
```

<details>
<summary><strong>opencode.json</strong> — Plugin config with MCP servers</summary>

```json
{
  "plugin": ["./adapters/opencode/apex.mjs"],
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"] },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"] },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"] }
  }
}
```
</details>

**Installs:** `opencode.json`, `adapters/opencode/apex.mjs`, `.opencode/agents/` (10)

**Auto-detects** — OpenCode loads `opencode.json` and `.opencode/agents/` on startup.

---

### Antigravity CLI

```bash
npx @asno-dev/apex antigravity
```

<details>
<summary><strong>antigravity-extension.json</strong> — Extension for <code>agy</code> binary</summary>

```json
{
  "name": "apex",
  "version": "3.0.0",
  "contextFileName": "AGENTS.md",
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"], "type": "local" },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"], "type": "local" },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"], "type": "local" }
  },
  "subagents": [
    {"name": "arch", "tag": "@arch", "description": "Max the Architect"},
    {"name": "ui", "tag": "@ui", "description": "Zara the UI Painter"},
    {"name": "debug", "tag": "@debug", "description": "Kai the Debugger"},
    {"name": "perf", "tag": "@perf", "description": "Rex the Performance Engineer"},
    {"name": "sec", "tag": "@sec", "description": "Vex the Security Engineer"},
    {"name": "infra", "tag": "@infra", "description": "Io the Infrastructure Engineer"},
    {"name": "nova", "tag": "@nova", "description": "Nova the Creative"},
    {"name": "reed", "tag": "@reed", "description": "Dr. Reed the Researcher"},
    {"name": "review", "tag": "@review", "description": "Rila the Reviewer"},
    {"name": "flex", "tag": "@flex", "description": "Flex the Founder"}
  ],
  "commands": [
    {"name": "apex", "description": "APEX mode switching"},
    {"name": "apex-team", "description": "Full team mode"},
    {"name": "apex-docs", "description": "Word documents"},
    {"name": "apex-excel", "description": "Excel spreadsheets"},
    {"name": "apex-ppt", "description": "PowerPoint presentations"},
    {"name": "apex-composio-setup", "description": "Connect external tools"},
    {"name": "apex-composio-status", "description": "Show connected tools"},
    {"name": "apex-composio-sync", "description": "Force sync"},
    {"name": "apex-mirage", "description": "VFS commands"}
  ],
  "features": {
    "modes": ["direct", "team", "select"],
    "composio": true,
    "mirage": true,
    "officecli": true
  }
}
```
</details>

**Installs:** `antigravity-extension.json`, `AGENTS.md`, `apex/src/` (MCP server files)

**Then:** Ensure `agy` binary is in PATH. The extension auto-detects on startup.

**Prerequisite:** [Antigravity CLI](https://github.com/antigravity-ai/agy) installed, `agy` in PATH.

---

### Devin CLI

```bash
npx @asno-dev/apex devin
```

<details>
<summary><strong>.devin/plugin.json</strong> — 10 agents, 8 commands, 3 MCP servers</summary>

```json
{
  "name": "apex",
  "version": "3.0.0",
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"], "type": "local" },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"], "type": "local" },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"], "type": "local" }
  },
  "agents": [
    {"name": "arch", "file": "agents/arch.md", "tag": "@arch"},
    {"name": "ui", "file": "agents/ui.md", "tag": "@ui"},
    {"name": "debug", "file": "agents/debug.md", "tag": "@debug"},
    {"name": "perf", "file": "agents/perf.md", "tag": "@perf"},
    {"name": "sec", "file": "agents/sec.md", "tag": "@sec"},
    {"name": "infra", "file": "agents/infra.md", "tag": "@infra"},
    {"name": "nova", "file": "agents/nova.md", "tag": "@nova"},
    {"name": "reed", "file": "agents/reed.md", "tag": "@reed"},
    {"name": "review", "file": "agents/review.md", "tag": "@review"},
    {"name": "flex", "file": "agents/flex.md", "tag": "@flex"}
  ],
  "commands": [
    {"name": "apex", "file": "commands/apex.md"},
    {"name": "apex-docs", "file": "commands/apex-docs.md"},
    {"name": "apex-excel", "file": "commands/apex-excel.md"},
    {"name": "apex-ppt", "file": "commands/apex-ppt.md"},
    {"name": "apex-composio-setup", "file": "commands/apex-composio-setup.md"},
    {"name": "apex-composio-status", "file": "commands/apex-composio-status.md"},
    {"name": "apex-composio-sync", "file": "commands/apex-composio-sync.md"},
    {"name": "apex-mirage", "file": "commands/apex-mirage.md"}
  ]
}
```
</details>

**Installs:** `.devin/plugin.json`, `.devin/agents/` (10 `.md`), `.devin/commands/` (8 `.md`)

**Auto-detects** — Devin reads `.devin/` config on startup.

---

### Hermes Agent

```bash
npx @asno-dev/apex hermes
```

<details>
<summary><strong>.hermes/plugin.json</strong> — 10 agents, 3 MCP servers, 8 commands</summary>

```json
{
  "name": "apex",
  "version": "3.0.0",
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"], "type": "local" },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"], "type": "local" },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"], "type": "local" }
  },
  "agents": [
    {"name": "arch", "file": "agents/arch.md", "tag": "@arch"},
    {"name": "ui", "file": "agents/ui.md", "tag": "@ui"},
    {"name": "debug", "file": "agents/debug.md", "tag": "@debug"},
    {"name": "perf", "file": "agents/perf.md", "tag": "@perf"},
    {"name": "sec", "file": "agents/sec.md", "tag": "@sec"},
    {"name": "infra", "file": "agents/infra.md", "tag": "@infra"},
    {"name": "nova", "file": "agents/nova.md", "tag": "@nova"},
    {"name": "reed", "file": "agents/reed.md", "tag": "@reed"},
    {"name": "review", "file": "agents/review.md", "tag": "@review"},
    {"name": "flex", "file": "agents/flex.md", "tag": "@flex"}
  ],
  "commands": [
    {"name": "apex", "file": "commands/apex.md"},
    {"name": "apex-docs", "file": "commands/apex-docs.md"},
    {"name": "apex-excel", "file": "commands/apex-excel.md"},
    {"name": "apex-ppt", "file": "commands/apex-ppt.md"},
    {"name": "apex-composio-setup", "file": "commands/apex-composio-setup.md"},
    {"name": "apex-composio-status", "file": "commands/apex-composio-status.md"},
    {"name": "apex-composio-sync", "file": "commands/apex-composio-sync.md"},
    {"name": "apex-mirage", "file": "commands/apex-mirage.md"}
  ]
}
```
</details>

**Installs:** `.hermes/plugin.json`, `.hermes/agents/` (10 `.md`), `.hermes/commands/` (8 `.md`)

**Then:** `hermes plugins install apex`

---

### Pi Agent Harness

```bash
npx @asno-dev/apex pi
```

<details>
<summary><strong>.pi/</strong> — NPM package with MCP servers, agents, and commands</summary>

```json
{
  "name": "apex",
  "version": "3.0.0",
  "main": "index.js",
  "pi": {
    "mcpServers": {
      "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"] },
      "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"] },
      "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"] }
    },
    "agents": ["arch", "ui", "debug", "perf", "sec", "infra", "nova", "reed", "review", "flex"],
    "commands": ["apex", "apex-docs", "apex-excel", "apex-ppt", "apex-composio-setup", "apex-composio-status", "apex-composio-sync", "apex-mirage"],
    "features": { "modes": ["direct", "team", "select"], "composio": true, "mirage": true, "officecli": true }
  }
}
```
</details>

**Installs:** `.pi/package.json`, `.pi/index.js`, `.pi/agents/` (10 `.md`), `.pi/commands/` (8 `.md`)

**Auto-detects** — Pi loads `.pi/` extensions on project trust.

---

### OpenClaw

```bash
npx @asno-dev/apex openclaw
```

<details>
<summary><strong>.openclaw/skills/manifest.json</strong> — 10 agent skills, 3 MCP servers</summary>

```json
{
  "name": "apex",
  "version": "3.0.0",
  "skills": ["arch", "ui", "debug", "perf", "sec", "infra", "nova", "reed", "review", "flex"],
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"] },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"] },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"] }
  }
}
```
</details>

**Installs:** `.openclaw/skills/manifest.json`, `.openclaw/skills/` (10 `.md`), `.openclaw/commands/` (8 `.md`)

**Auto-detects** — OpenClaw loads `.openclaw/skills/` on project open.

---

### GitHub Copilot CLI

```bash
npx @asno-dev/apex copilot
```

<details>
<summary><strong>.github/copilot-instructions.md</strong> — Always-on instructions for Copilot CLI</summary>

```markdown
# APEX v2 — 10-Agent Senior Engineering Team

@arch Max (Architect) | @ui Zara (UI/UX) | @debug Kai (Debugger)
@perf Rex (Performance) | @sec Vex (Security) | @infra Io (Infra)
@nova Nova (Creative) | @reed Dr.Reed (Research) | @review Rila (Review)
@flex Flex (Founder/MVP)

## MCP Servers
- apex-hands: node apex/src/hands-server.mjs
- mirage-vfs: node apex/src/mirage-server.mjs
- apex-composio: node apex/src/composio-server.mjs
```
</details>

**Installs:** `.github/copilot-instructions.md`, `.copilot/plugin.json`, `.copilot/agents/` (10 `.md`), `.copilot/commands/` (8 `.md`)

**Then:** `copilot plugin marketplace add asno-dev/apex` then `copilot plugin install apex`

---

### KiloCode / Kiro

```bash
npx @asno-dev/apex kilocode
```

<details>
<summary><strong>.kilo/mcp.json</strong> — MCP + steering + agents for KiloCode</summary>

```json
{
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"], "type": "local" },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"], "type": "local" },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"], "type": "local" }
  }
}
```
</details>

**Installs:** `.kilo/mcp.json`, `.kilo/steering/apex.md`, `.kilo/agents/` (10 `.md`), `.kilo/commands/` (8 `.md`)

**Auto-detects** — KiloCode (`kilo` binary) loads `.kilo/` config on project open.

---

## Commands

| Command | Description |
|:--------|:------------|
| `apex-docs` | Create/edit Word documents via OfficeCLI |
| `apex-excel` | Create/edit Excel spreadsheets via OfficeCLI |
| `apex-ppt` | Create PowerPoint presentations via OfficeCLI |
| `apex-composio-setup` | Connect external tools — paste API key, get OAuth link |
| `apex-composio-status` | Show connected tools and API key status |
| `apex-composio-sync` | Force sync from Composio backend |
| `apex-mirage <command>` | Execute commands across mounted virtual filesystem backends |
| `/apex-team` | Full team mode — all 10 agents work together end-to-end |
| `/apex team\|select\|off\|status\|help` | APEX mode control |

---

## MCP Servers

APEX provides **3 MCP (Model Context Protocol) servers** with **56 purpose-built tools** across all 10 agents, plus **6 virtual filesystem tools** and **1000+ external tool bridges**.

### 1. apex-hands — 56 Agent Domain Tools

| Agent | Tools |
|:------|:------|
| `@arch` | `blast_radius` `dep_graph` `complexity` `extract_refactor` `compose_check` `module_boundary` |
| `@ui` | `contrast` `palette_extract` `a11y_audit` `responsive_test` `component_search` |
| `@debug` | `reproduce` `stack_walk` `log_mine` `bisect_run` `guard_inject` `var_watch` |
| `@perf` | `profile` `memory_profile` `baseline_capture` `measure` `bundle_analyze` `big_o` |
| `@sec` | `vuln_scan` `secret_find` `input_trace` `auth_map` `owasp_score` `dependency_audit` |
| `@infra` | `docker_lint` `k8s_validate` `ci_check` `deploy_dry` `rollback_plan` `health_check` |
| `@nova` | `poc_gen` `lib_compass` `alt_angle` `trend_sniff` `downside_check` `approach_matrix` |
| `@reed` | `compare` `complexity_calc` `evidence_search` `tradeoff_matrix` `recommend` |
| `@review` | `diff_cat` `anti_pattern` `quality_gate` `praise_find` `review_card` |
| `@flex` | `value_cost` `mvp_cut` `risk_matrix` `roadmap` `effort_estimate` |

### 2. mirage-vfs — Virtual Filesystem (50+ Backends)

Unified filesystem across S3, GDrive, Slack, Redis, Postgres, and more.

**Setup:** `pip install mirage-ai && npm install -g @struktoai/mirage-cli`

**Usage:**
```
apex-mirage ls /s3/                    — List files in S3 bucket
apex-mirage cp /gdrive/report.pdf /data/  — Copy from Google Drive
apex-mirage grep -r error /s3/logs/    — Search across backends
```

### 3. apex-composio — 1000+ External Tool Bridge

Bridges Gmail, GitHub, Slack, Jira, Notion, and 1000+ more tools.

**Setup:** `apex-composio-setup`

**Usage:** `@gmail send email` | `@github create PR` | `@slack post message`

### All 3 MCP Servers in One Config

```json
{
  "mcpServers": {
    "apex-hands": { "command": ["node", "apex/src/hands-server.mjs"], "type": "local" },
    "mirage-vfs": { "command": ["node", "apex/src/mirage-server.mjs"], "type": "local" },
    "apex-composio": { "command": ["node", "apex/src/composio-server.mjs"], "type": "local" }
  }
}
```

---

## Agent Chains

### Sequential
```
Full app:        @arch → @ui → @infra      # Design → Paint → Deploy
Bug patch:       @debug → @review           # Fix → Verify
Spec to code:    @flex → @arch → @ui        # Scope → Design → Build
```

### Parallel
```
System design:   @arch ∥ @reed              # Architecture + Research in parallel
```

### Dynamic Peer Calling
- `@perf` finds SQL injection → calls `@sec`
- `@ui` needs a backend API → calls `@infra`
- `@debug` finds performance issue → calls `@perf`
- `@review` finds security concern → calls `@sec`

---

## Design System (Zara)

- **10 curated palettes**: Trust, Energy, Authority, Clarity, Warmth, Midnight, Forest, Ocean, Aurora, Minimal
- **CSS variable tokens** for all colors as `:root` variables
- **2 fonts max** per project
- **shadcn/ui** component library + **Tailwind CSS** scale
- **WCAG AA** compliance (4.5:1 contrast ratio minimum)
- **Mobile-first** responsive design
- **200ms** max transition duration
- **Semantic HTML** throughout

### Anti-Slop Rules
- No decorative elements without purpose
- No inline styles
- No hardcoded hex colors
- No gradients without justification
- No ALL CAPS text

---

## Requirements

- **Node.js** ≥ 18.0.0
- At least one supported coding agent installed

### Zero Dependencies

APEX has **zero production dependencies**. It uses only Node.js built-in modules.

---

## Development

```bash
git clone https://github.com/asno-dev/apex.git
cd apex
npm test
```

### Project Structure

| Directory | Purpose |
|:----------|:--------|
| `adapters/` | Per-agent config files (13 agents) |
| `agents/` | Canonical agent definitions (10 agents) |
| `commands/` | Canonical command definitions (8 commands) |
| `skills/` | SKILL.md files for orchestrator and agents |
| `src/` | MCP servers and tool implementations |
| `hooks/` | Lifecycle hooks for session management |
| `bin/` | CLI entry point |

---

## License

[MIT](LICENSE) © [asno-dev](https://github.com/asno-dev)

<p align="center">
  <a href="https://x.com/LKanth9406">Follow on X</a> •
  <a href="https://github.com/asno-dev/apex">GitHub</a>
</p>
