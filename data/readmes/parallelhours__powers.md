# parallel-powers

Human-in-the-loop framework for agentic-assisted product development. Adds session management skills, automated hooks, and MCP servers that give coding agents time tracking and workflow powers — useful for anyone whose agentic workflow needs structured session start/end, prompt counting, and token logging against a time-tracking backend.

## Components

### agent-docs-bootstrap — Documentation Kit Template

The `agent-docs-bootstrap/` directory is a template for initializing the [Diátaxis](https://diataxis.fr/) documentation framework in any project. It provides skeleton files for all 14 doc categories (readme, explanation, tutorials, how-tos, reference, plans, etc.), frontmatter conventions, and persona templates.

→ [Installer guide](agent-docs-bootstrap/installer.md) — instructions for agents to bootstrap a new project's docs

### Plugin — Session Management Powers

The repo is a **Claude Code plugin**, **Codex plugin**, and **OpenCode plugin** that adds session-tracking skills and automated hooks.

| Component | What it does |
|-----------|-------------|
| **Skills** (`skills/`) | Multi-step workflows, run by the user as slash commands or by the agent when asked — see full list below |
| **Hooks** (`hooks/`) | Trigger automatically on events: warn on missing timer at startup, count prompts on each message, log tokens on stop, lint before git commit |
| **OpenCode plugin** (`.opencode/`) | JS plugin with equivalent hook behavior, plus skills for OpenCode's `skill` tool |

#### Skills (v1.4.7)

| Skill | Invoke as | Description |
|-------|-----------|-------------|
| `session-start` | `/parallel-powers:session-start` | Start a tracked development session for a GitHub issue. Verifies git state, creates or finds the matching parallelhours task, transitions it to in_progress, and starts a timer. |
| `session-end` | `/parallel-powers:session-end` | End the current tracked development session. Stops the active timer, logs AI usage, pushes the branch, and transitions the task to the appropriate status. |
| `editorial-reviewer` | `/parallel-powers:editorial-reviewer` | Review any content — code comments, docs, web pages, CLI output, error messages, or prose — for inclusive language, sentiment, and tone. |
| `github-sprint-board` | `/parallel-powers:github-sprint-board` | Display a real-time sprint board from GitHub issues organized by status (not-started, in-progress, blocked, review, done). |
| `github-burndown` | `/parallel-powers:github-burndown` | Generate a burndown chart from GitHub issues for a sprint (milestone). Shows story point burn rate, scope changes, velocity, and completion forecast. |
| `diataxis-install` | `/parallel-powers:diataxis-install` | Bootstrap a Diátaxis agent-docs structure for a new or undocumented project. Runs a structured interview and executes all installer phases. |
| `diataxis-refresh` | `/parallel-powers:diataxis-refresh` | Refresh stale Diátaxis agent-docs after code changes, architectural decisions, or sprint completion. |

Install the parallelhours MCP separately using `mcps/installer.py` (see MCP Servers section below). Set these env vars before starting your agent:

| Variable | Required | Default |
|----------|----------|---------|
| `TKPI_PAT` | Yes | — |
| `TKPI_BASE_URL` | No | `https://parallelhours.io` |
| `TKPI_PROJECT` | No | — |

**Claude Code:**

```bash
# From release (no clone needed):
claude --plugin-url https://github.com/parallelhours/powers/releases/download/v1.4.7/parallel-powers.zip

# Or from a local clone:
claude --plugin-dir /path/to/powers
```

Skills are namespaced: `/parallel-powers:<skill-name>` (e.g. `/parallel-powers:session-start`)

Run `/reload-plugins` after adding new skills to the `skills/` directory.

**Codex:**

```bash
codex plugin marketplace add parallelhours/powers
```

Then inside a session: `/plugin install parallel-powers`

Skills are available via the `$` mention or `/skills` picker.

**OpenCode:**

Add to `opencode.json`:
```json
{ "plugin": ["powers@git+https://github.com/parallelhours/powers.git"] }
```

### MCP Servers

Install the parallelhours MCP using `mcps/installer.py`:

```bash
python -m mcps.installer --mcp parallelhours --agent claude --location project
python -m mcps.installer --mcp parallelhours --agent opencode --location project
python -m mcps.installer --list              # list available MCPs
python -m mcps.installer --mcp all --agent claude --location global  # install all globally
```

### agent-docs — Project Documentation

All project docs follow the Diátaxis framework in `agent-docs/`. See the [docs readme](agent-docs/00-readme/) for the full structure.
