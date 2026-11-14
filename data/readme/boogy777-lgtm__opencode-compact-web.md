# compact-web

[![OpenCode V2](https://img.shields.io/badge/OpenCode-V2-6E56CF)](https://opencode.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/boogy777-lgtm/opencode-compact-web?include_prereleases&sort=semver)](https://github.com/boogy777-lgtm/opencode-compact-web/releases)

A server-side `/compact-web` command for **OpenCode V2** that triggers a **real session
compaction** — and it works from the **web and desktop UI**, where the built-in `/compact`
sometimes does not.

> Русская версия: [README.ru.md](README.ru.md)

## Why

In the web/desktop client, `/compact` is a **client-side** action. The composer only routes it
while that entry is enabled (an active session with visible user messages). When it does not
match, the text is submitted as an ordinary prompt — the model receives the literal string
`/compact`, and **no compaction happens**.

A command registered by a plugin is a **server-side** command. Every client (web, desktop, TUI)
receives it from `GET /api/command` and dispatches it through
`POST /api/session/{id}/command`. Its executor calls the same `Session.compact` path that the
API and the TUI use, so this is a genuine compaction, not a prompt asking the model to summarize.

## Install

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/boogy777-lgtm/opencode-compact-web/main/scripts/install.ps1 | iex
```

### macOS / Linux (bash)

```bash
curl -fsSL https://raw.githubusercontent.com/boogy777-lgtm/opencode-compact-web/main/scripts/install.sh | bash
```

### Manual

Copy [`src/compact-web.ts`](src/compact-web.ts) to the global plugin directory:

| OS | Path |
|---|---|
| Windows | `%USERPROFILE%\.config\opencode\plugins\compact-web.ts` |
| macOS / Linux | `~/.config/opencode/plugins/compact-web.ts` |

OpenCode watches the plugin directory, so no restart is required. Plugin format is **V2**
(`export default { id, setup }`).

## Usage

Type the command in any session and press Enter:

```
/compact-web
```

## Verify

```bash
opencode api get /api/command
```

The response must contain an entry whose `name` is exactly `compact-web` (no namespace).
In the session history, the result appears as a `type: "compaction"` message with
`status: completed` or `status: failed`.

## Requirements

- OpenCode **V2** (verified on 2.2.1 and 2.2.5).
- V2 plugin format: `export default { id, setup }`.
  V1 plugins (`export const X: Plugin = async (...) => {}`) are not compatible with this file.

## Caveats

- **Empty session** — the command is accepted, but compaction ends with
  `compaction.unavailable / "Nothing to compact yet"`. This is expected.
- **Cost** — compaction is a paid model call. It uses the session model or
  `agents.compaction.model`.
- **History only** — the compaction result is visible in the session as a
  `type: "compaction"` message. `GET /api/session/{id}/inbox` does not return it.

## Uninstall

```powershell
irm https://raw.githubusercontent.com/boogy777-lgtm/opencode-compact-web/main/scripts/uninstall.ps1 | iex
```

```bash
curl -fsSL https://raw.githubusercontent.com/boogy777-lgtm/opencode-compact-web/main/scripts/uninstall.sh | bash
```

Or simply delete `compact-web.ts` from the plugin directory.

## Documentation

- [Installation](docs/installation.md) — custom locations, updates, uninstall
- [How it works](docs/how-it-works.md) — dispatch path and V1/V2 plugin formats
- [Troubleshooting](docs/troubleshooting.md) — command missing, nothing happens, failures
- [Verification log](docs/verification.md) — checks performed on a live server

## License

[MIT](LICENSE)
