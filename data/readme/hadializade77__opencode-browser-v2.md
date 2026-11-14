<div align="center">

# OpenCode Browser v2

**Chrome browser automation for [OpenCode](https://opencode.ai) 2 — control your *real* browser from the agent.**

Tabs · Navigation · Accessibility snapshots · Clicks · Form filling · JavaScript eval · Screenshots — over the Chrome DevTools Protocol, no browser extension required.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenCode v2](https://img.shields.io/badge/OpenCode-v2-7C3AED.svg)](https://opencode.ai)
[![Chrome 144+](https://img.shields.io/badge/Chrome-144%2B-4285F4.svg?logo=googlechrome&logoColor=white)](https://www.google.com/chrome/)
[![Protocol](https://img.shields.io/badge/protocol-CDP-orange.svg)](https://chromedevtools.github.io/devtools-protocol/)
[![Node >= 20](https://img.shields.io/badge/node-%3E%3D20-339933.svg?logo=node.js&logoColor=white)](https://nodejs.org)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

A V2-ready fork of [different-ai/opencode-browser](https://github.com/different-ai/opencode-browser) — ported to the OpenCode 2 plugin API, with real bug fixes and new tab management tools.

</div>

---

## Table of contents

- [Why this fork](#why-this-fork)
- [Features](#features)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Tools reference](#tools-reference)
- [How it works](#how-it-works)
- [Using your real Chrome profile](#using-your-real-chrome-profile)
- [Manual installation](#manual-installation)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Security](#security)
- [Project layout](#project-layout)
- [Credits](#credits)
- [License](#license)

## Why this fork

The original [opencode-browser](https://github.com/different-ai/opencode-browser) is an excellent Chrome automation plugin — but it targets the **OpenCode 1 plugin API**. OpenCode 2 intentionally changed the plugin contract, and V1 plugin implementations **do not load** in V2 (you get `Plugin must export a default definition with an id and an effect or setup function`).

This project is a drop-in replacement for OpenCode 2 users. It:

- ✅ **Ports the plugin to the OpenCode V2 API** (`Plugin.define` + `ctx.tool.transform`), exposing all tools natively to the agent (`options.codemode: false`).
- 🐛 **Fixes the accessibility snapshot bug** — the original walker discarded ignored AX subtrees, so `browser_snapshot` returned only the page root on most sites and `browser_click`/`browser_fill` could never resolve a UID. Snapshots now contain the full tree.
- 🐛 **Fixes screenshots hanging on background tabs** — `Page.bringToFront` is issued before capture.
- 🆕 **Adds tab management**: `browser_new_tab` (works even where `window.open` is popup-blocked, because it uses the DevTools protocol) and `browser_close_tab`.
- 🧹 **Drops the external dependency chain** in the tool layer — the tools use the built-in `fetch` and `WebSocket` only.
- 🔌 **Ships a tiny local bridge** that makes the plugin work with your **everyday Chrome profile** (tabs, cookies, logins) despite Chrome 136+'s remote-debugging hardening — see [Using your real Chrome profile](#using-your-real-chrome-profile).

## Features

- **Drive the browser the user actually uses** — your tabs, your sessions, your logins.
- **10 first-class agent tools** for listing tabs, navigating, snapshotting, clicking, filling, evaluating JavaScript and capturing screenshots.
- **Accessibility-tree snapshots** with stable `[uid]` markers for reliable clicking and typing.
- **No Chrome extension, no native messaging host, no broker** — direct CDP over local HTTP + WebSocket.
- **Works with Chrome, Chromium, Electron and remote/proxied CDP endpoints** — any endpoint reachable over `/json/*`.
- **Safe by default**: the bridge binds to `127.0.0.1`, and real-profile access still requires a per-session Chrome toggle and Allow prompt.

## Requirements

| Requirement | Notes |
|---|---|
| OpenCode v2.0.32+ | V2 plugin API |
| Node.js ≥ 20 | for the local bridge and the plugin runtime |
| Chrome / Chromium 144+ | for the `chrome://inspect/#remote-debugging` toggle (older versions work with `--remote-debugging-port` instead) |
| Linux, macOS or Windows | the plugin is cross-platform; the installer auto-starts the bridge via systemd on Linux only |

## Quick start

```bash
# 1. Clone
git clone https://github.com/HadiAlizade77/opencode-browser-v2.git
cd opencode-browser-v2

# 2. Install (plugin + bridge + service + config entry, with backup)
./scripts/install.sh

# 3. Enable remote debugging in Chrome (once per browser start)
#    open chrome://inspect/#remote-debugging and switch it on

# 4. Restart OpenCode
```

Then try:

```text
List my browser tabs, open example.com in a new tab, take a screenshot and close it.
```

## Tools reference

| Tool | What it does | Key parameters |
|---|---|---|
| `browser_list` | Lists page targets (tabs) with IDs, titles and URLs | `browser_url` |
| `browser_new_tab` | Opens a new tab via CDP — popup blockers never apply | `url` (default `about:blank`) |
| `browser_close_tab` | Closes a tab by target ID | `target_id` |
| `browser_navigate` | Navigates a tab and waits for load | `url`, `target_id` |
| `browser_snapshot` | Accessibility tree with `[uid]` markers for click/fill | `target_id` |
| `browser_click` | Clicks an element by snapshot UID (real mouse events, JS fallback) | `uid`, `target_id` |
| `browser_fill` | Clears and fills an input by snapshot UID (native setter + `Input.insertText`) | `uid`, `value`, `target_id` |
| `browser_eval` | Evaluates JavaScript in the page and returns the value | `expression`, `target_id` |
| `browser_screenshot` | Saves a PNG screenshot and returns its path | `target_id` |
| `browser_version` | Reports the installed plugin version | — |

All tools accept an optional `browser_url`. It defaults to the local bridge (`http://127.0.0.1:9333`), and to `OPENCODE_BROWSER_URL` when set.

## How it works

```text
┌────────────────────┐   native tools    ┌─────────────────────────────┐
│     OpenCode 2     │ ────────────────▶ │  opencode-browser-v2 plugin │
│       agent        │                   │  (V2 API, no dependencies)  │
└────────────────────┘                   └──────────────┬──────────────┘
                                                        │ HTTP + WebSocket (CDP)
                                            ┌───────────▼────────────┐
                                            │  bridge  127.0.0.1:9333 │
                                            └───────────┬────────────┘
                                                        │ browser WebSocket
                                            ┌───────────▼────────────┐
                                            │  Chrome (your profile)  │
                                            └────────────────────────┘
```

- The **plugin** registers the ten tools and speaks CDP: `/json/list`, `/json/new`, `/json/close/<id>` for discovery and one WebSocket per tab for commands.
- The **bridge** exists for one reason: since Chrome 136, Chrome ignores `--remote-debugging-port` for the default profile, and the sanctioned `chrome://inspect/#remote-debugging` toggle (Chrome 144+) exposes **only a WebSocket** — no `/json` HTTP endpoints. The bridge reads `DevToolsActivePort`, keeps one browser-level WebSocket to Chrome, and presents a standard CDP-looking HTTP surface on `127.0.0.1:9333` that the plugin understands.

If you launch Chrome yourself with `--remote-debugging-port=9222 --user-data-dir=<somewhere>` (a dedicated automation profile), you don't need the bridge at all — pass `browser_url: "http://127.0.0.1:9222"` and the tools talk to Chrome directly.

## Using your real Chrome profile

Chrome deliberately blocks remote debugging on the default profile. The supported path is Chrome's own toggle:

1. In Chrome, open `chrome://inspect/#remote-debugging`.
2. Enable **Remote debugging**. Chrome shows a permission dialog the first time an agent connects — click **Allow**.
3. Keep Chrome open. After a full browser restart, enable the toggle again.

That's it — the agent can now see and drive the tabs you already have open, with your existing logins.

The bridge auto-detects the standard Chrome, Chromium, Brave and Edge user-data directories on Linux, macOS and Windows. If your browser keeps its profile elsewhere, set `CHROME_PROFILE_DIR` to that directory.

> **Alternative:** run a dedicated debug profile instead of your real one:
> `google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/opencode/chrome-profile"`
> and point tools at `http://127.0.0.1:9222`. No toggle, no permission prompt, separate sessions.

## Manual installation

<details>
<summary>Prefer to do it by hand? Click to expand.</summary>

**1. The plugin**

```bash
mkdir -p ~/.config/opencode/plugins/opencode-chrome-devtools
cp src/index.ts src/lib.js ~/.config/opencode/plugins/opencode-chrome-devtools/
```

**2. The config entry** (`~/.config/opencode/opencode.json`)

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "/home/YOU/.config/opencode/plugins/opencode-chrome-devtools"
  ]
}
```

**3. The bridge** (only needed for the real-profile toggle route)

```bash
mkdir -p ~/.local/share/opencode-chrome-bridge ~/.local/bin
npm install --prefix ~/.local/share/opencode-chrome-bridge ws@8
cp bridge/opencode-chrome-bridge.js ~/.local/bin/
NODE_PATH=~/.local/share/opencode-chrome-bridge/node_modules \
  node ~/.local/bin/opencode-chrome-bridge.js
```

For autostart on Linux, copy `bridge/opencode-chrome-bridge.service` to `~/.config/systemd/user/`, replace `__NODE_BIN__` with the absolute path of your `node` binary (`command -v node`), `__BRIDGE_JS__` and `__NODE_PATH__` with your paths, then:

```bash
systemctl --user daemon-reload
systemctl --user enable --now opencode-chrome-bridge.service
```

On macOS/Windows, start the same command via your login items / Task Scheduler.

</details>

## Troubleshooting

| Symptom | Cause & fix |
|---|---|
| `HTTP 503 — Enable remote debugging first` | The Chrome toggle is off. Open `chrome://inspect/#remote-debugging` and enable it. |
| `Target … not found` | The tab was closed since you listed it. Call `browser_list` again. |
| `No snapshot cached. Call browser_snapshot first.` | Snapshot UIDs expire per call; re-run `browser_snapshot` before click/fill. |
| Tools missing from the agent | Restart OpenCode; check `plugins` in `opencode.json` points at the plugin directory. |
| `EADDRINUSE` on 9333 | Another bridge instance is running: `systemctl --user restart opencode-chrome-bridge`. |
| `env: 'node': No such file or directory` in the journal | The systemd user session cannot see your Node install (nvm/fnm/asdf/volta). Re-run `./scripts/install.sh`, which pins the absolute node path in `ExecStart`; the old installer used `/usr/bin/env node`. |
| Permission dialog keeps appearing | Chrome asks per debug session; click **Allow**. Restarting Chrome resets the toggle. |
| Screenshot is blank/slow | The plugin brings the tab to front first; if a page renders lazily, wait and retry. |

Logs: `journalctl --user -u opencode-chrome-bridge -f`

## FAQ

**Can OpenCode control my browser?**
Yes — this plugin gives the OpenCode 2 agent ten browser tools: list tabs, open/close tabs, navigate, snapshot the accessibility tree, click, fill forms, run JavaScript and take screenshots. It drives your real, logged-in Chrome.

**Does it need a Chrome extension?**
No. It speaks the Chrome DevTools Protocol over local HTTP + WebSocket. Nothing is installed into Chrome itself.

**Why does `--remote-debugging-port` no longer work with my normal profile?**
Chrome 136 hardened remote debugging: the flag is ignored for the default profile, and Chrome 144+ provides the `chrome://inspect/#remote-debugging` toggle instead. This project's bridge implements the missing HTTP layer for that toggle so existing CDP tooling keeps working.

**Can the agent see my logins and cookies?**
Only within the tabs it's allowed to attach to, and only while you keep the Chrome toggle enabled and have clicked Allow. Nothing leaves your machine.

**Which browsers are supported?**
Chrome and Chromium (including Edge), Electron apps that expose a CDP endpoint, and remote/proxied CDP endpoints — anywhere `/json/list` and page WebSockets are reachable.

**Does it work on Windows/macOS?**
The plugin and bridge are plain Node.js and run anywhere. The bundled installer's service autostart is Linux/systemd; elsewhere start the bridge via login items or Task Scheduler.

**How is this different from the original opencode-browser?**
It's a V2 port (the original targets OpenCode 1 and won't load in V2), plus fixes for the snapshot subtree bug and background-tab screenshots, plus `browser_new_tab`/`browser_close_tab`, plus the real-profile bridge.

## Security

- The bridge listens on `127.0.0.1` only, and every CDP connection stays on your machine.
- Real-profile access is gated by Chrome itself: the agent cannot attach until you enable `chrome://inspect/#remote-debugging` and approve the connection.
- Treat the debug port and the toggle as sensitive: anyone who can reach the endpoint can control the browser. Don't expose it beyond localhost.
- The bridge keeps a single browser-level WebSocket so the permission prompt appears as rarely as Chrome allows.

## Project layout

```text
opencode-browser-v2/
├── src/
│   ├── index.ts                 # OpenCode V2 plugin wrapper (Plugin.define)
│   └── lib.js                   # the ten tools + CDP client + snapshot walker
├── bridge/
│   ├── opencode-chrome-bridge.js    # CDP HTTP/WS bridge for the real-profile toggle
│   └── opencode-chrome-bridge.service
├── scripts/
│   └── install.sh               # one-shot installer (plugin + bridge + config)
└── .opencode/skill/browser-automation/SKILL.md   # optional agent skill
```

## Contributing

Issues and PRs are welcome. If you found a bug in the *original* V1 plugin
(`different-ai/opencode-browser`) that also applies here, please report it
[there](https://github.com/different-ai/opencode-browser/issues) as well — this
fork prefers to stay a thin, well-documented layer on top.

## Credits

- Original project: [different-ai/opencode-browser](https://github.com/different-ai/opencode-browser) by Benjamin Shafii and contributors (MIT).
- Inspired by Claude in Chrome.
- Built on the [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/).

## License

[MIT](LICENSE) © 2026 Hadi Alizadeh — includes portions of the original project © 2025 different-ai / Benjamin Shafii.
