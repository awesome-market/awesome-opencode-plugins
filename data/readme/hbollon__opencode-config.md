# opencode-config

> My personal OpenCode agent configuration — a multi-model, multi-agent coding environment tuned for DevOps, IaC, Go, and full-stack development.

## Philosophy

- **Human still master** — no agent can perform destructive operations (`git push --force`, `terraform apply`, state mutations, secret modifications). Every risky action requires human approval.
- **Cost-aware by design** — each agent gets the cheapest model that can do the job well. Orchestrator picks the right specialist at the right price point. Token budgets are explicit.
- **Specialized agents over monolithic reasoning** — each task type gets the right model, skill set, and MCP tools
- **Determinism and reproducibility** — IaC mindset applied to the coding environment itself
- **Explicit over magic** — every agent, skill, and permission is explicitly declared

## Architecture

```
~/.config/opencode/
├── AGENTS.md                         # Agent constitution & rulebook
├── opencode.json                     # Main config: permissions, MCPs, plugins, skills
├── oh-my-opencode-slim.json          # Agent presets, model assignments, council config
├── dcp.jsonc                         # Dynamic Context Pruning thresholds & strategies
├── tui.json                          # Terminal UI: theme, keybinds, attention
│
├── plugins/
│   └── rtk.ts                        # Command rewriting for token savings
│
├── command/                          # Custom Plannotator commands
│   ├── plannotator-annotate.md
│   ├── plannotator-last.md
│   └── plannotator-review.md
│
├── skills/                           # Local custom skills
│   └── cartography/                  # Codebase mapping & change detection
│
├── skills-ext/                       # Git submodule → github.com/hbollon/skills
│   ├── entropy-audit/                # Dead code & entropy detection
│   ├── git-smart-commit/             # Atomic conventional commits
│   └── rtk-disable/                  # RTK output injection bypass
│
└── oh-my-opencode-slim/              # Local agent prompt overrides
    ├── janitor.md
    └── orchestrator_append.md
```

## Agents

Two presets available via `oh-my-opencode-slim`: **personal** (default) and **copilot**.

### Personal preset

| Agent | Model | Role |
|---|---|---|
| **Orchestrator** | `deepseek-v4-pro` | Workflow manager — plans, delegates, reconciles |
| **Oracle** | `kimi-k2.6` | Architecture, debugging strategy, code review |
| **Librarian** | `deepseek-v4-flash` | Documentation & library research |
| **Explorer** | `deepseek-v4-flash` | Fast codebase search & pattern matching |
| **Designer** | `gemini-3.1-pro` | UI/UX design, visual polish, responsive layouts |
| **Fixer** | `qwen3.6-plus` | Bounded code implementation |
| **Observer** | `kimi-k2.6` | Visual/media analysis (screenshots, PDFs, diagrams) |
| **Janitor** | `deepseek-v4-pro` | Code entropy audit & cleanup planning |

### Copilot preset

| Agent | Model |
|---|---|
| Orchestrator | `claude-opus-4.6` |
| Oracle | `claude-opus-4.6` |
| Librarian | `grok-code-fast-1` |
| Explorer | `grok-code-fast-1` |
| Designer | `gemini-3.1-pro-preview` |
| Fixer | `claude-sonnet-4.6` |
| Janitor | `gpt-5.4` |

Built-in agents `explore` and `general` are explicitly disabled.

### Council

Multi-model consensus via parallel councillor execution (3 councillors, 480s timeout). Used for high-stakes architectural and security decisions.

## Skills

Skills are managed from three sources:

### 1. Local custom skills (`skills/`)

| Skill | Description |
|---|---|
| **cartography** | Hierarchical codemap generation for unfamiliar repositories with change detection |

### 2. Git submodule (`skills-ext/`)

Maintained in a [separate repo](https://github.com/hbollon/skills). Registered via `skills.paths` in `opencode.json`.

| Skill | Description |
|---|---|
| **entropy-audit** | Code entropy audit producing `CLEANING_PLAN.md` with evidence and prioritization |
| **git-smart-commit** | Atomic conventional commit splitting and execution |
| **rtk-disable** | Temporarily disable RTK output injection for raw command output analysis |

### 3. `npx skills` packages (`~/.agents/skills/`)

Installed via [`npx skills`](https://skills.sh) — a package manager for AI agent skills. The lockfile lives at `~/.agents/.skill-lock.json` (43 skills). Key categories:

**Planning & Discovery** — `brainstorming`, `find-skills`, `skill-creator`

**Web & Mobile Design** — `frontend-design`, `web-design-guidelines`, `mobile-design`, `react-native-design`

**Vue / Nuxt / Vite** — `vue`, `nuxt`, `vite`, `vitest`

**Flutter** (20 skills) — full lifecycle from setup to deployment: `flutter-architecting-apps`, `flutter-managing-state`, `flutter-building-layouts`, `flutter-building-forms`, `flutter-theming-apps`, `flutter-animating-apps`, `flutter-testing-apps`, `flutter-handling-http-and-json`, `flutter-working-with-databases`, `flutter-handling-concurrency`, `flutter-implementing-navigation-and-routing`, `flutter-localizing-apps`, `flutter-reducing-app-size`, `flutter-embedding-native-views`, `flutter-interoperating-with-native-apis`, `flutter-building-plugins`, `flutter-improving-accessibility`, `flutter-adding-home-screen-widgets`, plus platform setup skills (Linux, macOS, Windows)

**Plannotator** — `plannotator-compound`, `plannotator-setup-goal`, `plannotator-visual-explainer`

**DevOps & Tools** — `agent-browser`, `audit-website`, `code-reviewer`, `kubernetes-specialist`, `web-search`

**Utilities** — `context7-mcp`, `simplify`

## MCP Servers

| Server | Provider | Purpose | Managed by |
|---|---|---|---|
| **context7** | [Context7](https://context7.com) | Up-to-date library documentation | `opencode.json` |
| **stitch** | [Google Stitch](https://stitch.google) | Design system generation & UI prototyping | `opencode.json` |
| **grep_app** | [grep.app](https://grep.app) | GitHub code search across millions of repos | OMO-slim plugin |
| **websearch** | [Exa](https://exa.ai) | AI-powered web search & content extraction | OMO-slim plugin |

`context7` and `stitch` are defined explicitly in `opencode.json` using environment variable references (`${CONTEXT7_API_KEY}`, `${STITCH_API_KEY}`).

`grep_app` and `websearch` are **injected at runtime** by the `oh-my-opencode-slim` plugin. They're defined in its source code (`src/mcp/grep-app.ts`, `src/mcp/websearch.ts`) and merged into the OpenCode MCP config on startup. Agent access is controlled per-preset in `oh-my-opencode-slim.json`.

## Plugins

| Plugin | Purpose |
|---|---|
| `@plannotator/opencode` | Interactive plan annotation & approval workflow |
| `@tarquinen/opencode-dcp` | Dynamic Context Pruning for token window management |
| **`oh-my-opencode-slim`** | Agent preset system, council, multiplexer, built-in MCPs (see below) |
| `plugins/rtk.ts` | Bash command rewriting through `rtk` for token savings |

### oh-my-opencode-slim fork

I maintain a [personal fork](https://github.com/hbollon/oh-my-opencode-slim) (branch `v2-custom`) of [@alvinunreal/oh-my-opencode-slim](https://github.com/alvinunreal/oh-my-opencode-slim). My PRs upstream didn't integrate cleanly, so the fork carries several patches.

## Configuration

### Permissions (`opencode.json`)

- **Bash**: everything requires approval (`"ask"`) except explicitly allowed commands: `git *`, `npm *`, `yarn *`, `go *`, `flutter *`, `grep *`, `sort *`, `mkdir *`, `ls *`, `find *`, `tree *`, `head *`, `tail *`, `pwd`, `realpath *`, `cat *`, `touch *`, `cd *`, `sed *`, `echo *`, `jq *`, `wc *`, `rtk *`
  - Extra guard: `git push *`, `rtk git push *` are hard-denied
  - Extra guard: `rtk rm *` requires approval
- **Edit**: allowed in `~/git/*` and `/tmp/*`; `/*` prompts for confirmation

### Terminal UI (`tui.json`)

- Theme: **Catppuccin**
- oh-my-opencode-slim TUI sidebar integration
- Leader key: `Ctrl+X`
- Command list: `Ctrl+P`
- Mouse enabled, scroll acceleration
- Sound notifications on attention events

### Context Management (`dcp.jsonc`)

Dynamic context pruning with per-model memory limits, turn protection (4 turns), compression mode (`range`), deduplication, and error-purging. Sub-agent context is explicitly never touched.

## Setup

```bash
# 1. Clone this repo as your OpenCode config
git clone git@github.com:hbollon/opencode-config ~/.config/opencode

# 2. Initialize the skills submodule
cd ~/.config/opencode && git submodule update --init

# 3. Install rtk (optional — enables command rewriting)
cargo install --git https://github.com/rtk-ai/rtk
rtk init -g --opencode

# 4. Set required environment variables
export CONTEXT7_API_KEY="your-key"
export STITCH_API_KEY="your-key"
export EXA_API_KEY="your-key"        # for websearch MCP (optional)

# 5. Install npm dependencies
npm install

# 6. Install npx skills (optional — managed separately in ~/.agents)
npx skills install

# 7. Launch OpenCode
opencode
```

## Requirements

- [OpenCode](https://opencode.ai)
- Node.js 20+ (for plugins)
- Optional: [rtk](https://github.com/rtk-ai/rtk) for command rewriting
- Optional: Python 3 for the cartography skill
- Optional: [npx skills](https://skills.sh) for the external skill ecosystem

---

**Author:** [Hugo Bollon](https://github.com/hbollon) — DevOps & Fullstack Engineer, Grenoble, France
