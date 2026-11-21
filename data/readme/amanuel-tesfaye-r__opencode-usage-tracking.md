# OpenCode Usage Tracking

> Track your AI coding sessions — tokens, models, tools, files, and cost — all in your browser.

[![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=nextdotjs)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19-61dafb?logo=react)](https://react.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-read--only-003b57?logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

OpenCode Usage Tracking is a **local-first analytics dashboard** for [OpenCode](https://opencode.ai). It reads your OpenCode SQLite database and visualizes every session — token usage, model breakdowns, tool calls, files edited, todos, and cost — so you can understand exactly how you work with AI.

No cloud. No telemetry. No sign-up. 100% local.

---

## What It Tracks

| Metric | Description |
|---|---|
| **Sessions** | Every AI coding session with timestamps, duration, and agent |
| **Tokens** | Input, output, reasoning, and cache-read tokens per session |
| **Models** | Which AI models you use and how much you use them |
| **Tools** | Every tool call (read, write, bash, etc.) with success/error counts |
| **Projects** | Activity breakdown across all your codebases |
| **Files** | Most-edited files ranked by patch count |
| **Todos** | Tasks created and completed during sessions |
| **Agents** | Per-agent session counts, tokens, and tool usage |
| **Cost** | Token cost per session, model, and project |

---

## Quick Start

### Option 1: Standalone (Recommended)

```bash
# Clone the repo
git clone https://github.com/Amanuel-Tesfaye-R/opencode-usage-tracking.git
cd opencode-usage-tracking

# Install dependencies
npm install

# Start the dashboard
npm run dev
```

Open **http://localhost:3777** in your browser.

### Option 2: Auto-launch with OpenCode

Run this once to set up automatic launch:

```bash
npm run setup
```

This configures OpenCode to open the usage tracking dashboard in your browser every time it starts.

### Option 3: Docker

```bash
docker run -v ~/.local/share/opencode:/data -p 3777:3777 amanuel/opencode-usage-tracking
```

---

## Setup Script

The `npm run setup` command creates a **launcher script** that:

1. Starts the OpenCode Usage Tracking server in the background
2. Opens your browser automatically
3. Configures OpenCode to launch it on startup

### Manual Setup

If you prefer to set up manually:

1. Build the app: `npm run build`
2. Create a launcher script (see `scripts/launch.sh` or `scripts/launch.ps1`)
3. Configure OpenCode to run it on startup via your OpenCode config

---

## Data Source

OpenCode Usage Tracking reads your local OpenCode database:

| Platform | Default Path |
|---|---|
| Linux/macOS | `~/.local/share/opencode/opencode.db` |
| Windows | `%USERPROFILE%\.local\share\opencode\opencode.db` |

The database is opened with `PRAGMA query_only` — the dashboard **never modifies** your OpenCode data.

### Custom Database Path

```bash
OPENCODE_DB_PATH="/path/to/opencode.db" npm run dev
```

---

## Pages

| Route | Description |
|---|---|
| `/` | **Overview** — KPIs, activity chart, token flow, cache rate, models, tools, projects |
| `/sessions` | **Sessions** — searchable table with project filters and range selection |
| `/sessions/[id]` | **Session Detail** — full message timeline, tool calls, files changed, todos |
| `/tools` | **Tool Calls** — every tool call across all sessions, filterable and paginated |
| `/projects` | **Projects** — activity breakdown across your codebases |
| `/models` | **Models** — model usage distribution and cost breakdown |
| `/files` | **Files** — most-edited files across all sessions |
| `/todos` | **Todos** — tracked tasks with status and priority |
| `/agents` | **Agents** — per-agent usage statistics |
| `/gateway` | **Gateway Wall** — live Zen free-tier status, ping history, and the runtime readout (API keys, context, spend, LSP) |

---

## Tech Stack

- **Framework**: Next.js 16 App Router (React Server Components)
- **Runtime**: Node.js with `node:sqlite` (zero native dependencies)
- **Styling**: Tailwind CSS v4 with custom design tokens
- **Charts**: Recharts
- **UI**: shadcn/ui + Radix UI primitives
- **Fonts**: Geist Sans + Geist Mono

---

## Browser Support

Works best in Chromium-based browsers (Chrome, Edge, Arc). Firefox and Safari are supported but may have minor rendering differences.

---

## FAQ

**Is my data uploaded anywhere?**
No. Everything stays on your machine. The dashboard reads your local SQLite file and never sends data anywhere.

**Does it modify my OpenCode database?**
No. It opens the database with `PRAGMA query_only` and never writes to it.

**Which OpenCode version is required?**
Any version that writes to the standard SQLite database at `~/.local/share/opencode/opencode.db`.

**Can I use this without OpenCode?**
Not really — the dashboard reads the OpenCode database. But if you have the database file, it works standalone.

**Why port 3777?**
Because OpenCode uses 3777 by default. The dashboard sits alongside it on the same port.

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <sub>Built with care for the OpenCode community</sub>
</div>
