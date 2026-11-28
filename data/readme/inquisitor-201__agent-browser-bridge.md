# Agent Browser Bridge

Drive **your real Chrome** — the window you actually use, with all your logins
intact — from any local AI agent. One Chrome extension, one zero-dependency
Node bridge, and two ways to call it: MCP tools or a CLI.

No debug port. No second Chrome profile. No lost cookies.

---

## Why this exists

Every "let the agent use my browser" path breaks somewhere:

| Approach | What goes wrong |
|---|---|
| `--remote-debugging-port` on your normal profile | Chrome 136+ refuses to open the port on the default user-data-dir |
| Launch a separate debug profile | Empty browser: no logins, no extensions, no history |
| Copy your profile to a new directory | Chrome protects the profile; the copy is unreadable or takes forever |
| Headless / cloud browser | Needs re-authentication, and internal sites may not allow it |

This project takes the one path Chrome still allows: a **local extension with the
`debugger` permission**. The extension is already inside your browsing session,
so it can attach to a tab and speak the DevTools Protocol — without opening any
port and without leaving your profile.

No dependency on ChatGPT, Codex, Playwright, Puppeteer, or any cloud service.
Plain Node (>= 18) and Chrome.

---

## How it works

```
agent (MCP client or CLI)
        │  JSON-RPC over stdio        │  HTTP on 127.0.0.1:9333
        ▼                             ▼
  MCP server (node)  ──── queue ───► hub ──── long poll ───► Chrome extension
                                                                │ chrome.debugger
                                                                ▼
                                                          your live tabs
```

- **extension/** — MV3 service worker. Polls the hub, executes actions against
  tabs through `chrome.debugger` (CDP), manages tab groups, draws the cursor.
- **bin/mcp-server.mjs** — owns the hub port, exposes 21 MCP tools. If the port
  is already taken, it silently becomes a *client* of the running hub, so several
  agents can share one Chrome.
- **bin/abb.mjs** — the same operations from a shell, plus `doctor` and `selftest`.

---

## Requirements

- Node.js >= 18 (no npm packages are installed)
- Google Chrome (or any Chromium 116+ browser that supports MV3 + `debugger`)
- macOS, Linux or Windows

---

## Install

### 1. Get the code

```bash
git clone https://github.com/<you>/agent-browser-bridge.git
cd agent-browser-bridge
```

### 2. Load the extension (once per Chrome profile)

1. Open `chrome://extensions`
2. Turn on **Developer mode** (top right)
3. Click **Load unpacked** and select this repo's `extension/` folder
4. Pin the extension so you can see it

Chrome does **not** auto-reload unpacked extensions. After any edit inside
`extension/`, click the reload arrow on its card.

> The extension shows a "…is debugging this browser" bar while attached. That is
> normal and disappears when the agent stops using the tab.

### 3. Connect your agent

**Option A — MCP (recommended).** Point your agent at the server:

```json
{
  "mcpServers": {
    "agent-browser": {
      "command": "node",
      "args": ["/absolute/path/to/agent-browser-bridge/bin/mcp-server.mjs"],
      "env": { "ABB_CLIENT_ID": "claude" }
    }
  }
}
```

- **Claude Code**: `claude mcp add agent-browser -- node /abs/path/bin/mcp-server.mjs`
- **Cursor / Windsurf**: paste the JSON above into the MCP settings file
  (`.cursor/mcp.json` or the app's MCP panel)
- **Qoder** and other GUI clients: add a stdio connector with the same
  command/args (see `docs/tools.md` for a per-client table)
- **Any other MCP client**: the server speaks standard MCP over stdio

**Option B — CLI only.** No MCP client needed:

```bash
node bin/abb.mjs doctor          # is everything wired up?
node bin/abb.mjs selftest        # end-to-end check against your Chrome
node bin/abb.mjs group_begin '{"title":"research","url":"https://example.com"}'
node bin/abb.mjs text '{"limit":3000}'
node bin/abb.mjs group_end
```

Add `alias abb="node /abs/path/bin/abb.mjs"` to your shell rc to shorten that.

### 4. Verify

```bash
node bin/abb.mjs selftest
```

It starts a tiny local page, then exercises handshake, task group, read, click,
type, accessibility snapshot, screenshot and cleanup. All checks should pass.

---

## The usage rule: one task, one tab group

The bridge is designed around a habit that keeps the user's browser sane:

- `browser_group_begin { title }` — start each task in its own named group
- every later call targets that group, even if the user switched tabs
- `browser_group_end` — finish; tabs stay open for review

This is also what makes multi-agent use safe: each agent keeps its own pointer
(`ABB_CLIENT_ID`), so two agents never steal each other's tabs.

---

## Tools

| Tool | What it does |
|---|---|
| `browser_status` | Bridge + extension health, versions |
| `browser_group_begin` / `browser_group_end` / `browser_groups` | Task groups |
| `browser_tabs` / `browser_tab_new` / `browser_tab_select` / `browser_tab_close` | Tabs |
| `browser_open` | Navigate the task tab |
| `browser_text` / `browser_html` | Read the page |
| `browser_snapshot` | Accessibility tree (best for finding elements) |
| `browser_screenshot` | PNG of the tab |
| `browser_click` / `browser_type` / `browser_press_key` | Interact |
| `browser_wait_for` / `browser_scroll` | Timing and long pages |
| `browser_upload` | Set files on a file input |
| `browser_eval` | Run JS in the page (escape hatch) |
| `browser_visual_cursor` | Toggle the on-page cursor |

Full schemas and examples: [docs/tools.md](docs/tools.md).

---

## The visual cursor

Clicks and typing draw a large glowing pointer, highlight the target element and
play a ripple, so a human watching can follow along. It is an overlay inside the
page:

- does not move the system pointer
- `pointer-events: none`, so it never blocks a click
- disappears on navigation (re-injected on the next action)
- silent while the tab is hidden or Chrome is in the background
  (`browser_visual_cursor { backgroundSilent: false }` to always show it)
- not available on `chrome://` pages

---

## Security model

- Everything runs on `127.0.0.1`. Nothing is sent anywhere.
- The extension has `debugger` + `tabs` + `tabGroups` + `storage`; it can read any
  page you have open. Treat it like giving an agent your browser session.
- There is no authentication on the local port: any local process can submit
  commands while the bridge runs. On shared machines, stop the MCP server when
  you are not using it.
- The agent should never type passwords or one-time codes. Log in yourself; the
  bridge reuses the session.

---

## Limitations

- Unpacked extension = one manual "Load unpacked" per Chrome profile, and a
  manual reload after editing extension files.
- `chrome://`, the Chrome Web Store and other protected pages cannot be scripted.
- Iframes are reachable only through `browser_eval`, not through `browser_click`.
- Chrome must be running with a window open; the extension cannot drive a closed
  browser (start Chrome first).
- One Chrome window can be driven by several agents, but each agent works in its
  own tab group; two agents editing the *same* form will conflict.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `extension is not connected` | Load `extension/` at `chrome://extensions`, then reload the card |
| `unknown action: hello` | The extension on disk is newer than the loaded one — click reload |
| `element not found` | Use `browser_snapshot`, then match on visible text |
| Everything times out | `abb doctor`; check the port matches the extension's options page |
| Port already in use | Another agent owns the hub. That is fine — this one becomes a client |

More: [docs/troubleshooting.md](docs/troubleshooting.md).

---

## Development

```bash
node --check bin/mcp-server.mjs     # syntax
node bin/abb.mjs doctor             # environment
node bin/abb.mjs selftest           # end-to-end against live Chrome
node test/mcp-smoke.mjs             # protocol test with two independent agents
ABB_PORT=9444 node bin/abb.mjs status   # use a different port
```

Layout:

```
bin/         mcp-server.mjs (MCP stdio), abb.mjs (CLI)
lib/         hub.mjs (HTTP + queue), client.mjs, tools.mjs
extension/   manifest.json, sw.js, options.html/js
docs/        architecture, tools, troubleshooting
SKILL.md     agent-skill entry point
```

See [docs/architecture.md](docs/architecture.md) for the protocol details.

---

## License

MIT
