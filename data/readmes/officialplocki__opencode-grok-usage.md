<h1 align="center">opencode-grok-usage</h1>

<p align="center">
  Live Grok usage in the OpenCode V2 sidebar — SuperGrok weekly credits or xAI API rate limits.<br/>
  A small standalone plugin: server RPC + TUI panel + <code>grok_usage</code> tool.
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg" />
  <img alt="OpenCode" src="https://img.shields.io/badge/OpenCode-V2-111111" />
  <img alt="Status" src="https://img.shields.io/badge/status-experimental-orange" />
  <img alt="GitHub stars" src="https://img.shields.io/github/stars/officialPlocki/opencode-grok-usage?style=flat" />
</p>

> [!WARNING]
> **Unofficial and not affiliated with xAI.** The subscription mode reads the
> billing endpoints used by the Grok CLI and grok.com. Those are undocumented,
> can change at any time, and using them may violate xAI's terms. Use your own
> account at your own risk. The API mode uses the official xAI API and
> Management API. Read [`LEGAL.md`](LEGAL.md).

## What it shows

| Mode | Data | Source |
| --- | --- | --- |
| **Subscription** (SuperGrok / X Premium+) | Weekly credit usage %, reset time, per-product breakdown, monthly dollar allowance, on-demand/prepaid balance | `cli-chat-proxy.grok.com/v1/billing` with the xAI login stored in OpenCode, or `~/.grok/auth.json` |
| **API** (`XAI_API_KEY`) | Requests/tokens rate-limit remaining, optional prepaid balance | `api.x.ai/v1/models` rate-limit headers; Management API balance |

`auto` mode prefers the xAI login already stored in OpenCode, then a Grok CLI
login, then `XAI_API_KEY`.

## Prerequisites

- OpenCode **2.x**.
- Node **22.18+** for the helper CLI.
- One of:
  - **OpenCode xAI login** (this is what a running Grok session already uses): `opencode auth login`, then choose xAI → SuperGrok Subscription.
  - **Grok CLI login**: install the Grok CLI, run `grok login`, and keep `~/.grok/auth.json`.
  - **API key**: `XAI_API_KEY` on the OpenCode server, or an xAI API key saved in OpenCode.
  - Optional for balance: `XAI_MANAGEMENT_KEY` and `XAI_TEAM_ID`.

## Install

```bash
git clone https://github.com/officialPlocki/opencode-grok-usage.git ~/.local/share/opencode-grok-usage-src
cd ~/.local/share/opencode-grok-usage-src
npm install --omit=dev
```

Add it to `~/.config/opencode/opencode.json`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "/home/you/.local/share/opencode-grok-usage-src",
      "options": { "mode": "auto" }
    }
  ]
}
```

Reload (`/reload`). The panel appears when an `xai/...` model is selected.

> [!NOTE]
> OpenCode caches plugin modules by path. After updating, install into a
> versioned directory (`npm run install:local`) or restart the service.

## Usage

```text
/grok-status     # detailed report
/grok-refresh    # bypass the 30 s cache
```

The `grok_usage` tool exposes the same data to agents.

### Sidebar

Subscription:

```text
GROK USAGE
SuperGrok · weekly
██████  11% used
reset Fri 09:34
$29.31 / $150.00 month
```

API:

```text
GROK USAGE
xAI API
req 119/120
tok 4.2M/5M
balance $10.00
```

The panel is only shown while an xAI model is selected. Set `alwaysShow: true`
to keep it visible for every model.

## Authentication

### Subscription

OpenCode stores a SuperGrok login in its own credential store, not in
`~/.grok/auth.json`. The plugin reads the active `xai` connection
(`ctx.integration.connection`) and, if that is unavailable, the same row in
`~/.local/share/opencode/opencode.db`. Expired grants are refreshed with the
client id already inside the access token. A rotated refresh token is written
back to that row so OpenCode keeps working. Disable the write-back with
`refreshTokens: false`.

A Grok CLI login is still accepted. The plugin reads the first usable entry
from `~/.grok/auth.json` (or `GROK_AUTH_FILE`) when that file exists:

```json
{
  "entry-id": {
    "key": "<access token>",
    "refresh_token": "<refresh token>",
    "expires_at": "2026-11-09T12:00:00.000Z",
    "email": "you@example.com",
    "oidc_issuer": "https://auth.x.ai",
    "oidc_client_id": "<client id>"
  }
}
```

Expired tokens are refreshed through the issuer's OIDC discovery. Refreshed
tokens are written back to the file with mode `0600` so the Grok CLI stays in
sync. Disable the write-back with `refreshTokens: false`.

For CI or a custom login, set `GROK_ACCESS_TOKEN` and skip the file entirely.

### API

Set `XAI_API_KEY` on the OpenCode server:

```bash
XAI_API_KEY=xai-... opencode --standalone
```

For the shared service:

```bash
opencode service set env XAI_API_KEY xai-...
```

Optional balance (official Management API):

```bash
XAI_MANAGEMENT_KEY=...
XAI_TEAM_ID=...
```

## Options

```jsonc
{
  "plugins": [
    {
      "package": "/home/you/.local/share/opencode-grok-usage-src",
      "options": {
        "mode": "auto",
        "pollMs": 30000,
        "refreshTokens": true,
        "alwaysShow": false
      }
    }
  ]
}
```

| Option | Default | Meaning |
| --- | --- | --- |
| `mode` | `auto` | `auto`, `subscription`, or `api` |
| `authFile` | `~/.grok/auth.json` | Alternative credential file |
| `refreshTokens` | `true` | Persist refreshed OIDC tokens back to the file |
| `pollMs` | `30000` | TUI poll interval (minimum 10 s); server cache is 30 s |
| `alwaysShow` | `false` | Show the panel for every model, not just xAI |
| `teamId` | `XAI_TEAM_ID` | Team for the prepaid balance |

Environment: `GROK_AUTH_FILE`, `GROK_ACCESS_TOKEN`, `XAI_API_KEY`,
`XAI_MANAGEMENT_KEY`, `XAI_TEAM_ID`.

## How it works

```
OpenCode TUI ──RPC (30 s)──▶ server plugin ──▶ cli-chat-proxy.grok.com
                                    │          or api.x.ai
                                    ├─ OpenCode xAI connection (SuperGrok)
                                    └─ ~/.grok/auth.json (optional CLI login)
```

- Tokens never leave the local server; the RPC returns usage only.
- No analytics, no third-party relays.
- Subscription requests send `x-grok-client-mode: cli`, the header the Grok CLI
  uses for its billing call.
- The Management API balance ledger is inverted (a top-up appears negative); the
  plugin displays the absolute cent value.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `No Grok login found` | Connect xAI in OpenCode (`opencode auth login`), run `grok login`, or set `GROK_ACCESS_TOKEN` |
| `Grok rejected the token` | Re-run `grok login`; the refresh token was revoked |
| No API numbers | `XAI_API_KEY` missing or the server has no rate-limit headers |
| Panel missing | Select an `xai/...` model, or set `alwaysShow: true` |
| `balance` wrong | Management balance parsing is best-effort; verify in the xAI console |

## Development

```bash
npm install
npm test
npm run typecheck
npm run install:local
```

Tests cover auth file parsing, OIDC refresh, billing shapes, balance extraction
and options. No network is used.

## Legal

The subscription mode uses an undocumented billing endpoint. It is not
affiliated with xAI and may stop working or violate their terms. The API mode
uses the official xAI API. See [`LEGAL.md`](LEGAL.md) for the full notice.

## License

MIT — see [`LICENSE`](LICENSE).
