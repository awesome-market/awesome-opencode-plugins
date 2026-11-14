# 🚀 Cross-Platform AI Agent & Skill Sync Engine

A tool-agnostic configuration pipeline that manages your AI coding personas (`agents`) and automated utility capabilities (`skills`) across multiple projects and platforms.

---

## What This Does

Different AI coding tools expect configuration files in different locations:

| Tool | Expected Location |
|------|-------------------|
| **OpenCode** | `.opencode/` |
| **Claude Code** | `.claude/` |
| **Standard** | `.agents/` |

This package acts as a **single source of truth** that syncs your agents and skills to whatever tool each project uses. No broken symlinks, no cross-platform issues.

---

## Installation

**Published on npm** as `agentic-toolbox`. Requires Node.js `>=18`.

```bash
# Install from npm registry (recommended)
npm install --save-dev agentic-toolbox

# Or pin to a specific version
npm install --save-dev agentic-toolbox@0.5.0
```

This adds to your `package.json`:

```json
{
  "devDependencies": {
    "agentic-toolbox": "^0.5.0"
  }
}
```

### 2. Add npm Scripts (optional)

```json
{
  "scripts": {
    "at": "agentic-toolbox"
  }
}
```

The binary `agentic-toolbox` is exposed via `package.json:bin` → `dist/index.js` and is available automatically through `npx` / npm scripts.

### 3. Create Config File

Create `agentic-toolbox.json` in your project root:

```json
{
  "targets": ["opencode", "claude"]
}
```

### 4. Run Sync

```bash
npm run at
# or directly
npx agentic-toolbox
npx agentic-toolbox --config ./agentic-toolbox.json
```

### Updating

```bash
npm update agentic-toolbox
# or reinstall specific version
npm install --save-dev agentic-toolbox@latest
```

---

## Commands

| Command | Description |
|---------|-------------|
| `agentic-toolbox` | Sync agents/skills from toolkit to target dirs |
| `agentic-toolbox --config <path>` | Use a non-default config file |
| `agentic-toolbox --dry-run` | Preview what would be synced without making changes |
| `agentic-toolbox --verbose` | Enable verbose output |
| `agentic-toolbox --help` | Show help message |

Via npm scripts:

```bash
npm run at        # → agentic-toolbox
```

---

## Configuration

### `agentic-toolbox.json`

Located in the **parent project root** (alongside `package.json`).

| Field | Description |
|-------|-------------|
| `targets` | Array of target platforms: `opencode`, `claude`, or `agents` |

### Example Configurations

Sync to OpenCode only:
```json
{ "targets": ["opencode"] }
```

Sync to both OpenCode and Claude:
```json
{ "targets": ["opencode", "claude"] }
```

Sync to all platforms:
```json
{ "targets": ["opencode", "claude", "agents"] }
```

### Auto-Discovery

If `agentic-toolbox.json` is missing, the engine auto-detects:
- `opencode.json` → targets `.opencode/`
- `claude.json` or `.clauderc` → targets `.claude/`
- Otherwise → targets `.agents/`

### Custom Config Path

```bash
agentic-toolbox --config ./my-custom-config.json
```

---

## Repository Structure

### When installed via npm

```
parent-project/
├── package.json
├── agentic-toolbox.json
├── node_modules/agentic-toolbox/
│   ├── package.json         # CLI binary: agentic-toolbox → dist/index.js
│   ├── dist/                # Compiled output (generated)
│   │   └── index.js         # Sync engine
│   ├── AGENTS.md            # Instructions for AI models
│   ├── README.md            # This file
│   ├── agents/              # Agent definitions
│   │   ├── Agent.md.sample
│   │   └── *.md
│   └── skills/              # Skill definitions
│       ├── SKILL.md.sample
│       └── */               # Skill dirs with SKILL.md
├── .opencode/               # Generated (gitignored)
├── .claude/                 # Generated (gitignored)
└── .agents/                 # Generated (gitignored)
```

---

## Creating New Agents

### Option A: Use the Creation Pipeline (Recommended)

The toolkit includes an orchestration agent `agentic-tools-creator` that uses three skills to create agents:

1. **agentic-resource-gatherer** — Searches public repos for similar agents
2. **agent-creator** — Generates the agent file
3. **agentic-tools-creator** — Orchestrates the workflow

Invoke via your AI assistant (Claude/OpenCode) with the agentic-tools-creator agent.

### Option B: Manual Creation

1. Copy the template:

   ```bash
   cp node_modules/agentic-toolbox/agents/Agent.md.sample agents/MyAgent.md
   ```

2. Edit the new file with your agent's configuration

3. Run sync:

   ```bash
   npm run at
   ```

### Agent Description Format

Every agent description MUST be a free-flowing paragraph that includes:
- What this agent does (its core capability)
- When to call this agent (trigger conditions)
- What NOT to use it for (exclusions)
- What it returns (for subagents, omit for primary agents)

---

## Creating New Skills

### Option A: Use the Creation Pipeline

Same as agents — use the `agentic-tools-creator` agent with type="skill".

### Option B: Manual Creation

1. Create a directory for the skill:
   ```bash
   mkdir -p skills/my-skill
   ```

2. Copy the template:

   ```bash
   cp node_modules/agentic-toolbox/skills/SKILL.md.sample skills/my-skill/SKILL.md
   ```

3. Edit the new file with your skill's configuration

4. Run sync:

   ```bash
   npm run at
   ```

### Skill File Structure

Skills must be placed in a directory with `SKILL.md` as the entrypoint:

```
skills/
└── my-skill/
    ├── SKILL.md           # Main instructions (required)
    ├── template.md        # Optional template
    ├── examples/
    │   └── sample.md      # Optional examples
    └── scripts/
        └── helper.sh      # Optional scripts
```

### Skill Description Format

Every skill description MUST be a free-flowing paragraph that includes:
- What this skill does (its purpose)
- When to invoke it (trigger conditions)
- What NOT to use it for (exclusions)
- What it returns (output structure)

---

## Gitignore

Add these to your parent project's `.gitignore`:

```gitignore
# AI Agent Toolkit - Generated directories
.opencode/
.claude/
.agents/
```

---

## Platform Compatibility

This toolkit works with both Claude and OpenCode. Agent files use a superset of both platforms' configuration options:

| Feature | Claude | OpenCode |
|---------|--------|----------|
| Tool control | `tools` field | `permission` field |
| Model selection | `model` aliases | `provider/model-id` |
| Permission modes | `permissionMode` | `permission` object |
| Turn limits | `maxTurns` | `steps` |
| Memory | `memory` field | Not supported |
| MCP servers | `mcpServers` field | Not in agents |

For detailed field documentation, see `agents/Agent.md.sample`.

---

## How It Works

The sync engine (`dist/index.js`, published as `agentic-toolbox` binary) reads your master agent/skill files (which contain a **superset** of all platform fields), then **transforms** them per target:

- **For OpenCode**: Strips Claude-only fields (`tools`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, `initialPrompt`)
- **For Claude**: Strips OpenCode-only fields (`permission`, `mode`, `temperature`, `steps`, `disable`, `prompt`, `hidden`, `top_p`, `reasoningEffort`, `textVerbosity`)
- **For Standard**: No transformation (keeps all fields)

This means you maintain **one master file** per agent/skill, and get platform-optimized configs automatically.

---

## Troubleshooting

### Sync not working

1. Verify `agentic-toolbox.json` exists in project root
2. Check the toolkit is installed:
   ```bash
   ls node_modules/agentic-toolbox/dist/index.js
   npx agentic-toolbox --config ./agentic-toolbox.json
   ```

### Wrong target directory

Check your `agentic-toolbox.json` `targets` value, or let auto-discovery work by removing the config file.

---

## License

MIT — See LICENSE for details.