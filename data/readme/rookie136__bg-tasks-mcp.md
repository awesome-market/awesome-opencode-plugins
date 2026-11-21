# bg-tasks-mcp

> Let your AI agent manage background processes. One sentence to start, monitor, and stop dev servers, builds, and tests — without leaving the conversation.

## Why

Working on a full-stack project means juggling multiple terminal windows to start dev servers, check logs, and kill processes. Every context switch breaks your flow. **You're the process manager, not the AI.**

bg-tasks flips this: the LLM manages background processes for you.

```
Before:
┌──────────┐   ┌──────────────┐   ┌──────────────┐
│ opencode │   │ Terminal #1  │   │ Terminal #2  │
│ write code│   │ npm run dev  │   │ go run .      │
│ ask Q     │   │ check logs   │   │ check logs    │
└──────────┘   └──────────────┘   └──────────────┘
   ↑ Alt+Tab, manual PID hunting, context switching

After:
┌──────────────────────────────────────────────────┐
│ opencode                                         │
│                                                  │
│ "Start frontend and backend with bg-tasks"       │
│ → bg_start("frontend", "npm run dev")            │
│ → bg_start("backend", "go run .")               │
│                                                  │
│ "Show me frontend logs"                          │
│ → bg_logs(id="frontend", tail=20)                │
│                                                  │
│ "Stop the backend"                                │
│ → bg_kill(id="backend")                          │
│                                                  │
│ Dashboard: http://127.0.0.1:9876                 │
└──────────────────────────────────────────────────┘
```

## Use Cases

| Scenario | Example |
|----------|---------|
| Dev servers | `bg_start("fe", "npm run dev")` + `bg_start("be", "python app.py")` |
| Builds | `bg_start("build", "npm run build")` → `bg_wait("build")` → `bg_logs("build")` |
| Tests | `bg_start("test", "npm test")` → `bg_wait("test")` |
| Long scripts | `bg_start("seed", "node seed-db.js")` — check progress with `bg_logs` |
| Multi-project | Open two opencode windows → dashboard shows both projects' tasks |

## Installation

### npm (recommended)

```json
{"command": ["npx", "-y", "bg-tasks-mcp"]}
```

No install needed — `npx` downloads and runs on first use.

### Manual install

```bash
npm install -g bg-tasks-mcp
```

Then configure:

```json
{"command": ["bg-tasks-mcp"]}
```

### Git clone

```bash
git clone https://github.com/rookie136/bg-tasks-mcp.git
cd bg-tasks-mcp
npm install
```

Then:

```json
{"command": ["node", "/path/to/bg-tasks-mcp/index.js"]}
```

```md
When you need to start, monitor, or stop background processes (dev servers, builds, tests),
use the bg-tasks tools.
```

## Usage

### 6 MCP Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `bg_start` | Start a background task | `bg_start(name="frontend", command="npm run dev")` |
| `bg_wait` | Wait for completion or timeout | `bg_wait(id="frontend", timeout=30)` |
| `bg_logs` | Read task output | `bg_logs(id="frontend", tail=20, stream="stdout")` |
| `bg_status` | Inspect or list tasks | `bg_status(id="frontend")` / `bg_status()` |
| `bg_send` | Send text or signal | `bg_send(id="frontend", input="<Enter>")` |
| `bg_kill` | Terminate a task | `bg_kill(id="frontend")` / `bg_kill(id="frontend", force=true)` |

### 5 MCP Resources

| Resource | Description |
|----------|-------------|
| `bg://status` | All tasks as JSON |
| `bg://{id}/status` | Single task detail + log summary |
| `bg://{id}/logs` | Combined stdout/stderr |
| `bg://{id}/logs/stdout` | stdout only |
| `bg://{id}/logs/stderr` | stderr only |

## Web Dashboard

When the first opencode window starts, the HTTP dashboard comes online automatically:

```
http://127.0.0.1:9876          English (default)
http://127.0.0.1:9876/?lang=zh 中文
```

Features:
- Tabbed layout: **Running** / **Favorites** / **History**
- Window list (owner PID, remote PIDs, task counts, last active time)
- Running tasks with kill (✕) and favorite (☆) buttons
- **Favorites**: save frequently used commands (name + command + cwd), one-click start, edit via dialog, delete — persisted in `favorites.json`
- Per-window history with clear buttons
- Bilingual UI (EN/中文 toggle)

## Remote Mode (Optional)

The default `type: "local"` (stdio) starts and stops with each opencode window. When your machine sleeps, the stdio pipe breaks — and opencode does **not** reconnect stdio MCP servers, so the bg-tasks connection drops until you restart the window.

**Remote mode** serves MCP over HTTP (Streamable HTTP). After sleep, opencode automatically reconnects the TCP connection, so bg-tasks tools keep working without restarting opencode.

### Start the server

```powershell
# One-time: register auto-start at logon (requires admin PowerShell; crash auto-restart 3x)
Register-ScheduledTask -TaskName "bg-tasks" -Force `
  -Action (New-ScheduledTaskAction -Execute "node" -Argument "<path-to-bg-tasks-mcp>\index.js --serve" -WorkingDirectory "<path-to-bg-tasks-mcp>") `
  -Trigger (New-ScheduledTaskTrigger -AtLogOn) `
  -Settings (New-ScheduledTaskSettingsSet -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1))

# Without admin: drop a .vbs into the Startup folder (no crash auto-restart)
#   %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\bg-tasks.vbs
#     CreateObject("WScript.Shell").Run """node"" ""<path-to-bg-tasks-mcp>\index.js"" --serve", 0, False

# Or start now (for testing):
node index.js --serve --port 9876
```

### Configure opencode

```json
{ "bg-tasks": { "type": "remote", "url": "http://127.0.0.1:9876/mcp" } }
```

### Behavior differences

| | local (stdio) | remote (HTTP) |
|---|---|---|
| Lifecycle | starts/stops with opencode window | standalone service |
| After sleep | connection drops, needs window restart | auto-reconnects (TCP) |
| Tasks when window closes | killed with process | keep running (independent) |
| Task cleanup | auto on shutdown | `bg_kill` / dashboard Kill / service stop |

Both modes use port `9876` — run one or the other, not both.

Remote mode groups all tasks in one process-level session — tasks from every window are managed together (no per-window separation).

## Architecture

### Multi-Window Design

```
┌─ opencode window #1 (owner) ──────────────────────────────────────┐
│  bg-tasks process                                                  │
│                                                                     │
│  serveStdio (MCP stdio)  ←─ LLM tool calls                         │
│  HTTP :9876                                                         │
│    GET /              → dashboard HTML (bilingual)                 │
│    GET /status        → JSON API                                   │
│    GET /logs/{id}     → log page                                   │
│    POST /api/report   → receive remote window tasks               │
│    GET /api/health    → liveness probe                             │
│                                                                     │
│  orphan check (30s) → parent alive? → 3 fails → self-terminate    │
└─────────────────────────────────────────────────────────────────────┘

┌─ opencode window #2 (non-owner) ───────────────────────────────────┐
│  bg-tasks process                                                  │
│                                                                     │
│  serveStdio (MCP stdio)  ←─ own LLM tool calls                    │
│  mini HTTP :9877                                                    │
│    GET /logs/{id} → log page (read-only)                          │
│                                                                     │
│  reporter → every 10s POST /api/report (:9876) push task state    │
│  health check → every 5s GET /api/health (:9876) → owner alive?   │
│    → takeover :9876 → become new owner → close mini HTTP           │
└─────────────────────────────────────────────────────────────────────┘
```

### Owner/Takeover Lifecycle

```
Window #1 starts → binds :9876 → owner → dashboard online
Window #2 starts → EADDRINUSE → non-owner → mini HTTP :9877 → reporter push
Window #3 starts → EADDRINUSE → non-owner → mini HTTP :9878 → reporter push

Window #1 closes → health check fails → Window #2 jitter 500-1500ms → binds :9876
  → new owner → closes mini HTTP :9877 → tasks become local

Window #2 closes → Window #3 takes over
All windows closed → orphan check triggers → self-terminate
```

### Data Flow

```
non-owner window                  owner window
─────────────────                 ─────────────
bg_start("server", ...)  ──┐
bg_start("client", ...)  ──┤
                              │
reporter (10s interval)  ◄────┘
  │
  │ POST /api/report { pid, port, tasks: [...] }
  ▼
owner dashboard ──► aggregates remote + local tasks
  │
  ├─ GET / → dashboard HTML (window list, running, history)
  ├─ GET /logs/{id} → local task logs (from MemoryLogStore)
  └─ remote task links → http://127.0.0.1:{port}/logs/{id} (mini HTTP)
```

### Logging System

JSONL format written to `<install-dir>/.log`:

```jsonl
{"ts":"20260809T023839","evt":"owner_ok","pid":30508,"port":9876,"ppid":11972}
{"ts":"20260809T023900","evt":"bg_start","pid":30508,"id":"d26c6305","name":"backend","cmd":"python..."}
{"ts":"20260809T024200","evt":"bg_exit","pid":30508,"id":"d26c6305","exit":0,"ms":60000}
{"ts":"20260809T024503","evt":"orphan_check","pid":30508,"attempt":1,"alive":false}
{"ts":"20260809T030000","evt":"shutdown","pid":30508,"reason":"SIGTERM"}
```

Auto-rotation: 1MB per file, keeps last 2 backups (`.log.0`, `.log.1`).

## i18n

Translations are JSON files in `lib/i18n/`. To add a new language, copy `en.json` to `<lang>.json` and translate the values.

```
lib/i18n/
├── en.json     # English (default, fallback)
└── zh.json     # 中文
```

## File Structure

```
bg-tasks-mcp/
├── index.js              # entry: MCP stdio + owner detection + orphan check
├── lib/
│   ├── args.js            CLI arg parsing (--serve, --port, --help)
│   ├── store.js           MemoryLogStore (ring buffer, 4MB per key)
│   ├── registry.js        TaskRegistry (state machine, onTaskEvent hook)
│   ├── launch.js          task launch (shared by bg_start & favorites)
│   ├── favorites.js       favorites store (persisted to favorites.json)
│   ├── platform.js        Windows/Unix adaptation (shell, kill, signal)
│   ├── session.js         session ID generation (process-level)
│   ├── mcp-server.js      MCP server factory (shared by stdio & remote)
│   ├── mcp-http.js        Streamable HTTP transport (remote mode)
│   ├── status-http.js     HTTP dashboard + routes + multi-window aggregation
│   ├── reporter.js        non-owner task state push (10s interval)
│   ├── logger.js          JSONL file logger (1MB rotation)
│   ├── i18n.js            i18n loader (in-memory cache, en fallback)
│   └── i18n/
│       ├── en.json         English translations
│       └── zh.json         中文翻译
├── tools/                 6 MCP tools (bg_start, bg_wait, bg_logs, etc.)
├── resources/             MCP resources (bg://status, bg://{id}/logs, etc.)
└── test/                  Node.js native test runner
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BG_TASKS_NO_ORPHAN_CHECK` | Set to `1` to disable orphan detection | off |

## Platform

Node.js 18+, Windows/Linux/macOS. Windows uses `taskkill` instead of POSIX signals.

## License

MIT