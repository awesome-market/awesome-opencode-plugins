# opencode-firefox

[![npm](https://img.shields.io/npm/v/opencode-firefox?color=2563eb)](https://www.npmjs.com/package/opencode-firefox)
[![CI](https://github.com/rimar/opencode-firefox/actions/workflows/ci.yml/badge.svg)](https://github.com/rimar/opencode-firefox/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Give your OpenCode agent a real Firefox to drive.

`opencode-firefox` is an [OpenCode](https://opencode.ai) plugin that talks to
Firefox over **WebDriver BiDi**. If Firefox is already running with remote
debugging, it attaches to it and uses that session — cookies, logins, open tabs.
If not, it launches its own copy with a separate profile, so it never touches
your normal browser by accident. No extension, no Playwright, no Selenium.

```text
you:    book the cheapest direct flight on Friday
agent:  firefox_navigate → firefox_snapshot → firefox_click → firefox_fill
        (already signed in, no login wall, no CAPTCHA detour)
```

## Why

- **Your session when you want it.** Attach to the Firefox you are already
  using, and sites you are signed in to stay signed in. When the plugin has to
  launch a browser, it uses a separate profile instead of hijacking yours.
- **Zero browser tooling.** One WebSocket to Firefox's BiDi endpoint and plain
  JavaScript in the page. No driver to install, no extension to keep updated,
  no Playwright version to match.
- **Made for agents.** A compact page snapshot with numbered refs (`e0`, `e1`,
  …) that `click` and `fill` accept, plus visible text. Small, stable tool
  surface instead of a giant automation API.
- **Firefox-first.** Firefox stopped shipping CDP; most "AI browser" tooling
  still assumes Chrome. This speaks the protocol Firefox actually exposes.

## Requirements

- Firefox 100 or newer (WebDriver BiDi)
- OpenCode 2.x
- Linux, macOS, or Windows. Tested on Linux; the macOS/Windows paths use the
  standard Firefox install locations and `taskkill` for restart.

## Install

### With the OpenCode CLI

```sh
opencode plugin add opencode-firefox
```

This installs the package and adds it to your global
`~/.config/opencode/opencode.jsonc`. Pin a release with
`opencode plugin add opencode-firefox@0.1.1`.

Manage it with:

```sh
opencode plugin list                   # installed plugins
opencode plugin check                  # check for updates
opencode plugin update                 # update package plugins
opencode plugin remove opencode-firefox
```

`plugin add` only writes global configuration. For a project-local install,
edit the project's `opencode.jsonc` instead (next section).

If you previously copied `firefox-bidi.ts` into `~/.config/opencode/plugins/`,
remove it after installing the package, otherwise both register the same
`firefox.*` tools.

### With configuration

Add the plugin to `opencode.jsonc` — global or project:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["opencode-firefox"]
}
```

OpenCode installs the package automatically. To pass plugin options, use the
object form described in [Configuration](#configuration).

To use a local checkout during development:

```jsonc
{
  "plugins": ["/absolute/path/to/opencode-firefox"]
}
```

Then pick how Firefox starts:

- **Let the agent launch it** — run `firefox_start`. It uses an isolated profile
  (`~/.local/share/opencode-firefox/profile` on Linux) that can run next to your
  normal Firefox. Nothing is shared with your personal session.
- **Attach to your real session** — start Firefox yourself with the port open:

  ```sh
  firefox --remote-debugging-port 9222
  ```

  The plugin attaches to whatever Firefox owns that port, with whatever profile
  it was started with. If Firefox is already open without the flag, the new
  process can forward to the existing instance and the port never opens — quit
  Firefox first, or start a separate profile.

See [Profiles](#profiles-which-firefox-the-agent-gets) for the full rules.

## Configuration

Configure the plugin through the object form in `opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "opencode-firefox",
      "options": {
        "port": 9222,
        "binary": "/usr/lib/firefox/firefox",
        "profile": "/home/me/.mozilla/firefox/abc.agent",
        "defaultProfile": false
      }
    }
  ]
}
```

| Option | Environment fallback | Default | Meaning |
|---|---|---|---|
| `port` | `FIREFOX_BIDI_PORT` | `9222` | Debugging port the plugin connects to |
| `binary` | `FIREFOX_BIN` | auto-detected | Firefox executable |
| `profile` | `FIREFOX_PROFILE` | isolated profile | `-profile` directory used when the plugin launches Firefox |
| `defaultProfile` | `FIREFOX_DEFAULT_PROFILE` | `false` | Launch with your normal Firefox profile instead of an isolated one |

Options win when both are set; the environment variables are there for CI and
shell wrappers. Settings are read when the plugin loads, so save the config to
reload it (or run `/reload`).

### Profiles: which Firefox the agent gets

Attaching is not affected by these settings. If Firefox already has the
debugging port open, the plugin uses that instance with whatever profile it was
started with.

When the plugin **launches** Firefox (`firefox_start`, `firefox_restart`) it
picks a profile in this order:

1. **`profile: "/path/to/dir"`** — that profile. Create one with
   `firefox -P` → **Create Profile…**, then read its **Root Directory** from
   `about:profiles`. The directory is created if it does not exist.
2. **`defaultProfile: true`** — no `-profile` flag, so Firefox uses your
   normal default profile: every cookie, logged-in account, history entry, and
   extension you browse with. The agent can act as you anywhere you are signed
   in. It also hits Firefox's single-instance rule (if your normal Firefox is
   already open, the launch forwards to it and the port never opens), and
   `firefox_restart` may have to kill every Firefox process because it cannot
   tell its own instance apart.
3. **Neither (the default)** — an isolated, plugin-managed profile:

   | Platform | Location |
   |---|---|
   | Linux | `$XDG_DATA_HOME/opencode-firefox/profile` (default `~/.local/share/...`) |
   | Linux (snap Firefox) | `~/snap/firefox/common/opencode-firefox/profile` |
   | macOS | `~/Library/Application Support/opencode-firefox/profile` |
   | Windows | `%LOCALAPPDATA%\opencode-firefox\profile` |

   It starts with no cookies or logins and runs alongside your normal Firefox.
   It persists between launches, so sites you sign in to there stay signed in.
   This is a separate identity, **not** a sandbox: the agent controls everything
   inside it.

If you start Firefox yourself, pass the profile on that command line instead:

```sh
firefox -profile /path/to/profile --remote-debugging-port 9222
```

## Tools

All tools live in the `firefox` namespace and are also available in Code Mode
as `tools.firefox.*`.

| Tool | Purpose |
|---|---|
| `firefox_status` | Port/session/tab health check; attaches if needed |
| `firefox_start` | Launch Firefox with debugging if it is not running (isolated profile by default) |
| `firefox_restart` | Stop and relaunch the Firefox it launched, reopening the current page |
| `firefox_navigate` | Open a URL, optionally in a new tab |
| `firefox_snapshot` | URL, title, numbered interactive elements (`e0`, `e1`, …), visible text |
| `firefox_click` | Click by ref, CSS selector, or visible text / aria-label |
| `firefox_fill` | Fill input/textarea/select; optionally submit with Enter |
| `firefox_press` | Enter, Tab, Escape, arrows, PageDown, … |
| `firefox_eval` | Evaluate JavaScript in the page and return JSON |
| `firefox_screenshot` | Save a PNG to disk (open it with the `read` tool) |
| `firefox_tabs` | List, switch, or close tabs |
| `firefox_bidi` | Escape hatch for any raw BiDi command |
| `firefox_mask_automation` | Hide `navigator.webdriver` for sites that block automation |

Typical loop:

```text
firefox_navigate → firefox_snapshot → firefox_click / firefox_fill → firefox_snapshot
```

Take a fresh snapshot before clicking by ref, because refs point at the page
state from the last snapshot.

## Security

Attaching gives the agent the same reach as your browsing session: cookies,
logged-in accounts, and any site you can open. A malicious or compromised page
can try to prompt-inject the agent into acting on your behalf.

- The default launch mode is an isolated profile with no logins. You only expose
  your real session when you attach to your running Firefox, or when you opt in
  with `defaultProfile: true` (or `FIREFOX_DEFAULT_PROFILE=1`).
- Prefer sites you trust, and review actions on sensitive accounts.
- `firefox_mask_automation` exists because some legitimate sites (airlines,
  banks) block automated browsers outright. It changes only `navigator.webdriver`
  for the current session; use it only where you would browse manually.

An isolated profile limits the blast radius of injection, but it is not a
sandbox: the agent still controls everything inside that browser, and it can
reach any site you sign in to there.

Please report security issues privately via GitHub's **Security → Report a
vulnerability** flow, not a public issue. See [SECURITY.md](SECURITY.md).

## Notes and limitations

- Firefox allows **one** BiDi session at a time, and it does not release the
  session when a client disconnects. If OpenCode is killed hard, the next
  connection fails with `Maximum number of active sessions`; `firefox_restart`
  clears it when the plugin launched the browser. If you started Firefox
  yourself, quit that Firefox and relaunch it with the debugging port.
- `firefox_restart` stops the Firefox the plugin launched, matched by profile,
  so your normal browser keeps running. With `defaultProfile: true` there is
  no profile to match, so it falls back to killing every Firefox process
  (`pkill -x firefox` / `taskkill /IM firefox.exe /F`). Unsaved tabs in that
  instance are lost — use it only to recover.
- The plugin has no network interception, download handling, or multi-browser
  abstraction. It is a small, intentionally direct Firefox driver.
- Firefox stopped shipping CDP, so Chrome DevTools-based tooling cannot attach
  to the debugging port.

## How it works

Firefox exposes WebDriver BiDi at `ws://127.0.0.1:9222/session`. The plugin opens
one WebSocket, creates a session, and sends commands such as
`browsingContext.navigate`, `script.evaluate`, `input.performActions`, and
`browsingContext.captureScreenshot`. Page helpers (snapshot, click, fill) are
JavaScript evaluated in the page, which is why there is nothing else to install.

## Development

```sh
pnpm install
pnpm check   # typecheck + tests
```

To try a local checkout in OpenCode, point `plugins` at the repository
directory (see [Install](#install)) or link it with `npm link`.

## License

MIT — see [LICENSE](LICENSE).
