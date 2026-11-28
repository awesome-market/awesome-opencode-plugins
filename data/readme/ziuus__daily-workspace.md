<div align="center">

# ⚡ Daily
### The Central Local Workspace Hub Connecting All Your AI Agents & Automation

*A developer-first, high-density workspace that acts as the single central bridge linking all your AI agents (OpenCode, Hermes, Claude, Cursor, Antigravity, Windsurf) into one unified intelligence feed, theme studio, and task hub.*

[![npm version](https://img.shields.io/npm/v/@ziuus/daily.svg?color=10B981&style=for-the-badge)](https://www.npmjs.com/package/@ziuus/daily)
[![License: MIT](https://img.shields.io/badge/License-MIT-38BDF8.svg?style=for-the-badge)](LICENSE)
[![MCP Server](https://img.shields.io/badge/MCP-Stdio%20Ready-A855F7.svg?style=for-the-badge)](mcp/index.js)
[![Node.js](https://img.shields.io/badge/Node.js-v22+-green.svg?style=for-the-badge)](https://nodejs.org)

</div>

> Building this in the open — if it saves you time, a star helps others find it.
> Found a bug, or have an idea? [Open an issue](https://github.com/ziuus/daily-workspace/issues).
> New feed sources and automation ideas welcome.

---

## 🖥️ Dashboard Interface Preview

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [D] DAILY WORKSPACE v1.1 • MCP: Online • Workers 3/3            [Search ⌘K] [🎨 Themes] [+New Entry]   │
├───────────────────────────┬────────────────────────────────────────────┬───────────────────────────────┤
│ FEED TIMELINE             │ READING CANVAS                             │ WORKSPACE METRICS             │
│                           │                                            │                               │
│ [OS REPO] browser-use     │ # browser-use: Web Automation Engine       │ ┌───────────────────────────┐ │
│ ⚡ +1,420 stars/day        │                                            │ │ OS Repos Tracked    5     │ │
│ 2m ago                    │ Explosive open-source browser automation   │ │ Active Cron Jobs    3/4   │ │
│                           │ framework for LLM agents.                  │ └───────────────────────────┘ │
│ [AI TOOL] Claude 3.7      │                                            │                               │
│ Hybrid Reasoning          │ ```python                                  │ AUTONOMOUS TASKS              │
│ 1h ago                    │ agent = Agent(task="Scrape news...")       │                               │
│                           │ await agent.run()                          │ ● reddit-warmup    [RUN NOW]  │
│ [NEWS] Node.js 22 LTS     │ ```                                        │ ● ai-news-scraper  [RUN NOW]  │
│ Native SQLite & WS        │                                            │ ◐ repo-star-track  [PAUSED]   │
│ 1d ago                    │ > [!NOTE] Native Stdio MCP Integration     │ ● system-watchdog  [RUN NOW]  │
└───────────────────────────┴────────────────────────────────────────────┴───────────────────────────────┘
```

---

## 🌟 Key Features

* **🔗 Multi-Agent Central Bridge**: Serves as the shared memory and central feed connecting OpenCode, Hermes, Antigravity, Cursor, Claude Desktop, Windsurf, and custom AI scripts into one dashboard.
* **📰 Curated Intelligence Feed**: Track shortlisted viral open-source repositories (velocity, star growth, repo links), trending AI tools & LLM releases, and high-signal tech news.
* **🎨 22-Theme Studio & Dynamic Workspace Engine**: 22 hand-curated color presets (11 Light / 11 Dark) that transform 100% of the workspace interface (headers, sidebars, badges, buttons, dots, and surfaces).
* **☀️/🌙 Paired Light & Dark Mode Toggling**: The Sun/Moon header button smoothly toggles between paired Light and Dark versions of your active theme family (e.g. *Rose Quartz* ↔ *Velvet Crimson Rose*).
* **🤖 Autonomous Task & Cron Hub**: Manage background scripts (Python scripts, scrapers, system health watchdogs). Monitor status (`active`, `paused`, `running`, `error`), last/next run times, and live terminal logs.
* **🔌 Built-in MCP Server (`daily-mcp`)**: Native Stdio Model Context Protocol integration enabling AI agents to push markdown updates, read feed entries, and trigger tasks on demand.
* **✍️ Rich GFM Markdown Renderer**: Built-in renderer with code syntax highlighting, copy-to-clipboard buttons, formatted tables, task checklists, and GFM callout blocks (`[!NOTE]`, `[!TIP]`, `[!WARNING]`).
* **📦 Zero-Dependency SQLite Storage**: Powered by Node.js native `node:sqlite` for high-performance WAL-mode storage in `~/.daily/data/daily.db`.

---

## 🚀 Installation & Quick Start

### Global Installation via `npm`

```bash
npm install -g @ziuus/daily
```

### Starting the Workspace Dashboard

```bash
# Open visual dashboard in browser (http://localhost:3456)
daily

# Background Daemon Process Controls
daily start     # Start background daemon on port 3456
daily stop      # Stop background daemon
daily restart   # Restart server & sync web assets
daily status    # Check daemon PID and server health
```

---

## 🤖 MCP Server Agent Configurations

Different agents use different configuration formats (YAML, JSON, CLI flags, or custom keys). Daily supports all standard Stdio MCP parameters (`npx -y @ziuus/daily mcp`).

Below are the exact setup snippets for each agent framework:

### 1. OpenCode Agent
Add to `~/.opencode/mcp.json` or run `opencode mcp add`:

```json
{
  "mcpServers": {
    "daily": {
      "command": "npx",
      "args": ["-y", "@ziuus/daily", "mcp"]
    }
  }
}
```
Or via OpenCode CLI:
```bash
opencode mcp add daily -- npx -y @ziuus/daily mcp
```

### 2. Hermes Agent *(YAML Format)*
Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  daily:
    command: "npx"
    args:
      - "-y"
      - "@ziuus/daily"
      - "mcp"
```

### 3. Claude Desktop *(JSON Format)*
Add to `claude_desktop_config.json`:
* macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
* Windows: `%APPDATA%\Claude\claude_desktop_config.json`
* Linux: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "daily": {
      "command": "npx",
      "args": ["-y", "@ziuus/daily", "mcp"]
    }
  }
}
```

### 4. Cursor IDE
Go to **Cursor Settings** -> **Features** -> **MCP**, or add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "daily": {
      "command": "npx",
      "args": ["-y", "@ziuus/daily", "mcp"]
    }
  }
}
```

### 5. Antigravity / Gemini CLI
Add to `~/.gemini/antigravity-cli/mcp/daily/daily.json`:

```json
{
  "name": "daily",
  "command": "npx",
  "args": ["-y", "@ziuus/daily", "mcp"]
}
```

### 6. Windsurf / Codeium Cascade
Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "daily": {
      "command": "npx",
      "args": ["-y", "@ziuus/daily", "mcp"]
    }
  }
}
```

### 7. Roo Code / Cline (VS Code)
Add to `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "daily": {
      "command": "npx",
      "args": ["-y", "@ziuus/daily", "mcp"]
    }
  }
}
```

### 8. Goose CLI *(Terminal Command)*
Run in terminal:

```bash
goose mcp add daily -- npx -y @ziuus/daily mcp
```

### 9. Continue.dev *(Custom Key Format)*
Add to `~/.continue/config.json`:

```json
{
  "experimental": {
    "modelContextProtocol": [
      {
        "name": "daily",
        "command": "npx",
        "args": ["-y", "@ziuus/daily", "mcp"]
      }
    ]
  }
}
```

### 10. Zed Editor *(Custom Key Format)*
Add to `~/.config/zed/settings.json`:

```json
{
  "context_servers": {
    "daily": {
      "command": "npx",
      "args": ["-y", "@ziuus/daily", "mcp"]
    }
  }
}
```

### 11. Python Frameworks (LangChain / LlamaIndex / CrewAI)

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(command="npx", args=["-y", "@ziuus/daily", "mcp"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            updates = await session.call_tool("daily_get_updates", {"limit": 5})
            print(updates)

asyncio.run(main())
```

### 12. Node.js / TypeScript SDK

```typescript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const transport = new StdioClientTransport({ command: 'npx', args: ['-y', '@ziuus/daily', 'mcp'] });
const client = new Client({ name: 'custom-agent', version: '1.0.0' }, { capabilities: {} });
await client.connect(transport);
const updates = await client.callTool({ name: 'daily_get_updates', arguments: { limit: 5 } });
```

---

## 🛠️ Exposed MCP Tools Reference

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `daily_add_update` | `title`, `category`, `markdown_content`, `tags`, `metadata` | Push a new markdown intelligence entry to the workspace feed. |
| `daily_get_updates` | `since`, `category`, `limit`, `read_status` | Fetch recorded updates between a given timestamp and now. |
| `daily_list_tasks` | `status_filter` | List all registered autonomous background tasks and status. |
| `daily_trigger_task` | `task_id` | Manually trigger immediate execution of a task. |

---

## 💻 Command Line Interface (CLI) Commands

| Command | Description |
| :--- | :--- |
| `daily` | Launches/opens the Web Dashboard at `http://localhost:3456` in your default browser. |
| `daily start` | Starts the background daemon server on port `3456`. |
| `daily stop` | Gracefully stops the running background daemon server. |
| `daily restart` | Restarts the background daemon server and syncs the web assets. |
| `daily status` | Checks process status, PID, port, and health of the daemon server. |
| `daily list` | Prints formatted intelligence feed entries to the terminal. |
| `daily list --category os_project` | Filters terminal output by category (`os_project`, `ai_tool`, `tech_news`, `custom`). |
| `daily add [flags]` | Inserts a new markdown update entry directly from the CLI. |
| `daily task list` | Displays an ASCII status table of all registered autonomous background tasks. |
| `daily task trigger <id>` | Manually triggers immediate execution of task `<id>`. |
| `daily task pause <id>` | Pauses automatic cron execution for task `<id>`. |
| `daily task resume <id>` | Resumes automatic cron execution for task `<id>`. |
| `daily task add [flags]` | Registers a new autonomous cron script. |
| `daily serve` | Runs the REST API server and task scheduler in the foreground. |
| `daily mcp` | Launches the Stdio MCP Server for AI agents. |

---

## 🎨 22-Theme Studio Presets

Click the **Themes 🎨** button in the header bar to choose from 22 hand-crafted color combinations:

| Category | Presets |
| :--- | :--- |
| **Light Themes (11)** | *Cream & Emerald (Original)*, *Rose Quartz*, *Vercel Blue Slate*, *Warm Clay & Amber*, *Nordic Sage*, *Lavender Haze*, *Terracotta Gold*, *High Tech Cyan*, *Pure Monochrome*, *Sahara Dune*, *Pacific Sky*. |
| **Dark Themes (11)** | *Emerald Studio Dark (Original)*, *Velvet Crimson Rose*, *Linear Indigo Graphite*, *Obsidian Amber Luxe*, *Pine Needle Forest*, *Cosmic Neon Purple*, *Dracula Gothic Pink*, *Neo Tokyo Cyberpunk*, *Pure Monokai Code*, *Retro 80s Synthwave*, *Midnight Abyss Cyan*. |

---

## 🌐 REST API Specification

The local HTTP server on port `3456` exposes JSON REST endpoints:

* `GET /api/stats` — Workspace metrics (counts, unread, task statuses, system health).
* `GET /api/updates` — Query feed updates (`?category=...&search=...&limit=...`).
* `POST /api/updates` — Add a new update entry.
* `PATCH /api/updates/:id/read` — Toggle read/unread status.
* `DELETE /api/updates/:id` — Delete an update entry.
* `GET /api/tasks` — List all registered tasks (`?status=...`).
* `POST /api/tasks` — Register a new autonomous task.
* `POST /api/tasks/:id/trigger` — Execute task immediately.
* `GET /api/tasks/:id/logs` — Fetch execution log history for a task.
* `DELETE /api/tasks/:id` — Delete a task registration.

---

## 📁 Storage & Data Isolation

All runtime database state, task logs, and configuration remain isolated in `~/.daily/`:

```
~/.daily/
├── data/
│   ├── daily.db               # SQLite WAL database (updates, tasks, execution logs)
│   └── config.json            # User & server configuration
├── web/
│   └── dist/                  # Built production Web Dashboard assets
├── mcp/
│   └── index.js               # Stdio MCP Server
├── server/
│   ├── index.js               # REST API & static file server
│   └── scheduler.js           # Autonomous background task scheduler
└── bin/
    └── daily.js               # Global CLI entrypoint
```

---

## 📄 License

[MIT](LICENSE) © [ziuus](https://github.com/ziuus)
