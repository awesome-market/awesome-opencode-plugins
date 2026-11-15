# SkillLane

> **Skills are infrastructure for agents.**

Open-source skill runtime and registry for AI agents — create, validate, install, run, and share reusable agent skills.

[![npm](https://img.shields.io/badge/npm-%40talocode%2Fskilllane-blue)](https://www.npmjs.com/package/@talocode/skilllane)
[![PyPI](https://img.shields.io/badge/PyPI-talocode--skilllane-green)](https://pypi.org/project/talocode-skilllane/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Why SkillLane

Every AI agent today writes the same debugging prompts, code reviews, and content generation from scratch. Skills solve this — reusable, validated, portable bundles of agent behavior.

**SkillLane** is the runtime that makes skills first-class infrastructure:

- **Create** skills from templates or scratch
- **Validate** skills with a 100-point scoring system (secrets detection, schema checks, content quality)
- **Install** from local paths, git repos, or built-in skills
- **Run** skills to generate structured prompts for any agent target
- **Share** via a local registry (remote marketplace coming soon)

---

## How it works

```
┌─────────────────────────────────────────────────────────┐
│                     SkillLane                           │
│                                                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐           │
│  │ Creator  │──▶│Validator │──▶│ Installer│           │
│  │ (scaffold)│  │ (100pts) │   │ (copy +  │           │
│  └──────────┘   └──────────┘   │ registry)│           │
│                                 └────┬─────┘           │
│                                      │                  │
│                                      ▼                  │
│                          ┌───────────────────┐          │
│                          │  Local Registry   │          │
│                          │  ~/.skilllane/    │          │
│                          │  registry.json    │          │
│                          └────────┬──────────┘          │
│                                   │                     │
│                    ┌──────────────┼──────────────┐      │
│                    ▼              ▼              ▼      │
│              ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│              │  Runner  │  │API Server│  │MCP Server│  │
│              │ (prompts)│  │ (:3080)  │  │(stdio)   │  │
│              └──────────┘  └──────────┘  └──────────┘  │
│                    │              │              │       │
│                    ▼              ▼              ▼       │
│              ┌──────────────────────────────────────┐   │
│              │     Agent Targets                    │   │
│              │  codex │ opencode │ codra │ tera     │   │
│              └──────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Install

### npm

```bash
npm install -g @talocode/skilllane
```

### pip

```bash
pip install talocode-skilllane
```

### From source

```bash
git clone https://github.com/talocode/skilllane.git
cd skilllane
npm install
npm run build
npm link
```

**Requirements:** Node.js >= 18.0.0

---

## Quickstart

```bash
# Initialize SkillLane storage
skilllane init

# Install a built-in skill
skilllane install --builtin systematic-debugging

# Run it
skilllane run systematic-debugging --task "Debug a TypeError in UserProfile"

# See all installed skills
skilllane list

# Create your own skill
skilllane create my-skill --title "My Skill" --category engineering

# Validate it
skilllane validate ./my-skill

# Check system health
skilllane doctor
```

---

## Skill Format

Every skill is a directory containing these files:

| File | Required | Description |
|------|----------|-------------|
| `metadata.json` | Yes | Name, version, tags, category, targets |
| `SKILL.md` | Yes | Role, instructions, constraints, workflow |
| `tools.json` | Yes | Tool definitions the skill needs |
| `examples.md` | Yes | Example inputs/outputs for reference |
| `eval.md` | Yes | Success criteria and evaluation checks |

### metadata.json schema

```json
{
  "name": "my-skill",
  "version": "0.1.0",
  "title": "My Skill",
  "description": "What this skill does",
  "author": "Your Name",
  "license": "MIT",
  "tags": ["engineering", "debugging"],
  "category": "engineering",
  "targets": ["codex", "opencode", "codra", "mcp"],
  "requiresTools": [],
  "createdAt": "2026-01-01T00:00:00.000Z",
  "updatedAt": "2026-01-01T00:00:00.000Z"
}
```

---

## Built-in Skills

SkillLane ships with 8 skills ready to install:

| Skill | Category | Description |
|-------|----------|-------------|
| `systematic-debugging` | engineering | Structured approach to diagnosing and fixing code errors |
| `agent-code-review` | engineering | Code review covering correctness, security, performance, maintainability |
| `context-engineering` | engineering | Manage context windows, summarize, compact information efficiently |
| `screen-aware-command` | engineering | Create precise agent commands from rough user instructions |
| `launch-thread-writer` | marketing | Generate concise product launch threads in Talocode style |
| `x-growth` | marketing | Write X posts, replies, hooks, and launch threads that get engagement |
| `product-launch` | marketing | Turn shipped products into launch copy, docs, X threads, and release notes |
| `frontend-design` | design | Produce better UI with deliberate aesthetic, hierarchy, typography, color choices |

---

## CLI Commands

```bash
skilllane init                        # Initialize ~/.skilllane directory
skilllane create <name>               # Create a new skill from template
skilllane validate <path>             # Validate a skill folder
skilllane install <source>            # Install a skill from a path
skilllane list                        # List installed skills
skilllane search <query>              # Search installed skills
skilllane show <name>                 # Show skill details
skilllane run <name>                  # Run a skill
skilllane remove <name>               # Remove an installed skill
skilllane export <name>               # Export a skill to a tarball
skilllane serve                       # Start the HTTP API server
skilllane mcp                         # Start the MCP server
skilllane doctor                      # Check system health
skilllane demo                        # Run deterministic demo

# Registry management
skilllane registry path               # Show registry file path
skilllane registry rebuild            # Rebuild registry from installed skills
skilllane registry stats              # Show registry statistics

# Configuration
skilllane config get <key>            # Get a config value
skilllane config set <key> <value>    # Set a config value
skilllane config list                 # List all config values
```

### Create options

```bash
skilllane create my-skill \
  --title "My Skill" \
  --description "Does something useful" \
  --category engineering \
  --tags "debugging,troubleshooting" \
  --targets "codex,opencode" \
  --template debugging \
  --out ./skills
```

### Run options

```bash
skilllane run systematic-debugging \
  --task "Fix this TypeError" \
  --context "Cannot read property 'name' of undefined" \
  --target opencode \
  --out result.json
```

### Install options

```bash
skilllane install --builtin systematic-debugging     # Install built-in
skilllane install ./my-skill                          # Install from path
skilllane install https://github.com/user/skill.git  # Install from git
skilllane install ./my-skill --force                  # Overwrite existing
```

---

## SDK Usage

### TypeScript

```typescript
import { SkillLaneClient } from '@talocode/skilllane';

const client = new SkillLaneClient();

// Initialize
await client.init();

// Create a skill
await client.createSkill({
  name: 'my-skill',
  description: 'A custom skill',
  category: 'engineering',
  outDir: './skills',
});

// Validate
const result = await client.validateSkill('./my-skill');
console.log(`Score: ${result.score}/100`);

// Install
await client.installSkill('./my-skill');

// List skills
const skills = await client.listSkills({ category: 'engineering' });

// Run a skill
const run = await client.runSkill({
  skillName: 'systematic-debugging',
  task: 'Debug a runtime error',
  context: 'TypeError at line 42',
  target: 'opencode',
});

console.log(run.prompt);
```

### Connect to remote API

```typescript
const client = new SkillLaneClient({
  baseUrl: 'http://localhost:3080',
  authToken: 'your-token',
});
```

---

## API Routes

Start the API server with `skilllane serve`.

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| GET | `/health` | No | Health check |
| GET | `/v1/skilllane/health` | No | Health check (v1) |
| GET | `/v1/skilllane/doctor` | No | System diagnostics |
| POST | `/v1/skilllane/init` | Yes | Initialize storage |
| POST | `/v1/skilllane/skills/create` | Yes | Create a new skill |
| POST | `/v1/skilllane/skills/validate` | Yes | Validate a skill |
| POST | `/v1/skilllane/skills/install` | Yes | Install a skill |
| GET | `/v1/skilllane/skills` | No | List installed skills |
| GET | `/v1/skilllane/skills/search` | No | Search skills |
| GET | `/v1/skilllane/skills/:name` | No | Get skill details |
| POST | `/v1/skilllane/skills/:name/run` | Yes | Run a skill |
| POST | `/v1/skilllane/skills/:name/export` | Yes | Export a skill |
| DELETE | `/v1/skilllane/skills/:name` | Yes | Remove a skill |
| GET | `/v1/skilllane/registry` | No | Get registry info |
| POST | `/v1/skilllane/registry/rebuild` | Yes | Rebuild registry |
| GET | `/v1/skilllane/registry/stats` | No | Registry statistics |
| POST | `/v1/skilllane/demo` | No | Run demo |

### Example: Run a skill via API

```bash
curl -X POST http://localhost:3080/v1/skilllane/skills/systematic-debugging/run \
  -H "Content-Type: application/json" \
  -d '{"task": "Debug a TypeError", "context": "Cannot read property of undefined"}'
```

---

## MCP Tools

Start the MCP server with `skilllane mcp`. Exposes 12 tools via the Model Context Protocol (JSON-RPC over stdio):

| Tool | Description |
|------|-------------|
| `skilllane_init` | Initialize local storage |
| `skilllane_create` | Create a new skill |
| `skilllane_validate` | Validate a skill directory |
| `skilllane_install` | Install a skill from a path |
| `skilllane_list` | List installed skills |
| `skilllane_search` | Search skills by query |
| `skilllane_show` | Show skill details |
| `skilllane_run` | Run a skill with a task |
| `skilllane_remove` | Remove an installed skill |
| `skilllane_doctor` | Run health checks |
| `skilllane_demo` | Run the demo |
| `skilllane_registry_stats` | Get registry statistics |

### MCP Configuration

```json
{
  "mcpServers": {
    "skilllane": {
      "command": "skilllane",
      "args": ["mcp"]
    }
  }
}
```

---

## Python Package

The Python package provides an HTTP client that talks to a running SkillLane API server.

```bash
pip install talocode-skilllane
```

```python
from talocode_skilllane import SkillLaneClient

client = SkillLaneClient(base_url="http://localhost:3080")

# Check health
print(client.health())

# List skills
skills = client.list_skills(category="engineering")

# Run a skill
result = client.run_skill(
    name="systematic-debugging",
    task="Debug a TypeError",
    context={"error": "Cannot read property of undefined at line 42"}
)
print(result)
```

### Python CLI

```bash
skilllane-py health
skilllane-py list --category engineering
skilllane-py search debugging
skilllane-py validate ./my-skill --strict
skilllane-py run systematic-debugging --task "Fix this bug"
skilllane-py demo
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SKILLLANE_URL` | `http://localhost:3080` | API server URL |
| `SKILLLANE_TOKEN` | (none) | Auth token |

---

## Local Registry

All data lives in `~/.skilllane/`:

```
~/.skilllane/
├── config.json          # Configuration
├── registry.json        # Installed skills index
├── skills/              # Skill directories
│   ├── systematic-debugging/
│   ├── agent-code-review/
│   └── ...
└── runs/                # Run history
```

### Registry management

```bash
skilllane registry path     # Show path to registry.json
skilllane registry rebuild  # Rescan skills/ and rebuild registry
skilllane registry stats    # Show skill counts by category/tag
```

---

## Validator

The validator scores skills on a 100-point scale:

| Check | Points | Type |
|-------|--------|------|
| Each missing required file | -15 | error |
| metadata.json invalid JSON | -15 | error |
| Each metadata field error | -10 | error |
| Empty metadata.title | -5 | error |
| Empty metadata.description | -5 | error |
| Empty metadata.targets | -5 | error |
| Empty metadata.tags | -3 | warning |
| tools.json invalid JSON | -10 | error |
| No tools defined | -3 | warning |
| SKILL.md empty | -15 | error |
| SKILL.md too short | -5 | warning |
| examples.md empty | -10 | error |
| No example section header | -5 | warning |
| eval.md empty | -10 | error |
| No criteria section header | -5 | warning |
| File exceeds 1MB | -5 | warning |
| Secret detected in file | -15 | error |

**Score interpretation:**
- **80-100:** Production-ready
- **50-79:** Usable with warnings
- **0-49:** Needs work

```bash
skilllane validate ./my-skill
skilllane validate ./my-skill --strict   # Fail on first error
skilllane validate ./my-skill --json     # JSON output
```

---

## Creator

Scaffold new skills from templates:

```bash
skilllane create my-skill --template basic
skilllane create my-bug-fixer --template debugging
skilllane create my-writer --template writing
skilllane create my-launcher --template product-launch
```

Each template generates all 5 required files with pre-filled content matching the template's domain.

---

## Runner

The runner takes an installed skill and generates a structured prompt for any agent target.

```bash
skilllane run systematic-debugging --task "Fix the login bug"
```

**Output modes:**

| Mode | Description |
|------|-------------|
| `prompt` | Plain text sections with `[Section]` headers |
| `markdown` | Markdown with `## Section` headers and `---` dividers |
| `json` | JSON array of `{section, content}` objects |

**Target descriptions injected into prompts:**

| Target | Description |
|--------|-------------|
| `codex` | OpenAI Codex CLI — terminal commands and file operations |
| `opencode` | OpenCode CLI — bash tool, file tools |
| `codra` | Codra — codebase context and editor features |
| `tera` | Tera — code generation and inline suggestions |
| `mcp` | MCP protocol — tool-based interactions |
| `clipboard` | Output to clipboard |
| `stdout` | Plain text response |
| `all` | General-purpose instructions |

---

## Security & Privacy

- **Local-first:** All data stored in `~/.skilllane/`. No telemetry.
- **Secrets detection:** Validator scans for AWS keys, private keys, API keys, tokens, passwords, bearer tokens.
- **Auth support:** Optional Bearer token auth for API routes. Configurable via `SKILLLANE_REQUIRE_AUTH` and `SKILLLANE_API_AUTH_TOKEN`.
- **No remote calls:** v0.1 does not call external services by default.

---

## Talocode Ecosystem

SkillLane is part of the **Talocode** ecosystem:

- **SkillLane** — Skill runtime and registry
- **OpenCode** — AI coding CLI (primary target)
- **Codex** — OpenAI's coding agent
- **Codra** — Code intelligence platform

---

## Demo Video

Run the built-in demo to see SkillLane in action:

```bash
skilllane demo
```

This validates a built-in skill, installs it, runs it with a sample TypeScript error, and saves output to `demo/demo-output.json`.

---

## Roadmap

| Version | Milestone |
|---------|-----------|
| **v0.1** | Local runtime, CLI, SDK, API, MCP, 8 built-in skills |
| **v0.2** | Remote registry, `skilllane publish`, `skilllane update`, skill versioning |
| **v0.3** | Skill dependencies, skill composition, plugin hooks |
| **v1.0** | Production-ready remote marketplace, enterprise features |

See [docs/ROADMAP.md](docs/ROADMAP.md) for details.

---

## Limitations

Be aware of these current limitations:

- **Local only (v0.1):** No remote registry or sharing. You can't `skilllane install` from a central marketplace yet.
- **Prompt generation, not execution:** The runner generates structured prompts — it does not execute code or call LLMs directly.
- **No skill versioning:** Skills are identified by name, not version. Updating requires `--force`.
- **No skill dependencies:** Skills cannot depend on other skills.
- **Remote marketplace planned:** A hosted registry for discovering and publishing skills is planned for v0.2.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.
