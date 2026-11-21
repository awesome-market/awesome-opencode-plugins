# opencode-key-rotator

[![npm version](https://img.shields.io/npm/v/%40dmmop%2Fopencode-key-rotator)](https://www.npmjs.com/package/@dmmop/opencode-key-rotator)
[![npm downloads](https://img.shields.io/npm/dm/%40dmmop%2Fopencode-key-rotator)](https://www.npmjs.com/package/@dmmop/opencode-key-rotator)
[![CI and Release](https://github.com/dmmop/opencode-key-rotator/actions/workflows/release.yml/badge.svg)](https://github.com/dmmop/opencode-key-rotator/actions/workflows/release.yml)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://prettier.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

OpenCode v2 plugin that automatically rotates provider API keys on rate limits and quota errors.

Automatically swaps to the next saved key when OpenCode encounters rate limits (429), quota exhaustion, or resource errors during sessions.

## Features

- **Automatic rotation** — detects rate-limit and quota errors and swaps to the next available key on retry
- **OpenCode v2 plugin** — subscribes to public session events with one native v2 entrypoint
- **Live TUI notifications** — successful automatic rotations show one toast per connected TUI through the official plugin RPC
- **Persistent storage** — keys and rotation logs stored in the XDG data directory
- **Configurable** — customize rotation patterns via a sidecar config
- **Secure** — transactional SQLite writes, restrictive permissions, and credential log sanitization

## Installation

```bash
npx -y @dmmop/opencode-key-rotator init
```

Or install it globally:

```bash
npm install -g @dmmop/opencode-key-rotator
opencode-key-rotator init
```

### Runtime compatibility

Targets OpenCode 2.0.2 and `@opencode/plugin@2.0.2` (server, TUI and shared RPC contracts). Earlier V2 beta SDKs are not supported. The non-JSX TUI adapter and its shared portable RPC definition use only SDK type imports: the entire TUI runtime graph loads without locally installed SDK packages or optional Solid peers. The server still uses the SDK at runtime. Tests load the unbuilt local TUI source from an isolated directory without SDK packages; Node rejects SDK imports explicitly and Bun runs with auto-install disabled.

OpenCode runs the plugin with Bun and does not need additional flags. Node.js 22.5 or newer is also supported. In Node.js 22.5 through 22.12, `node:sqlite` is experimental: the installed `opencode-key-rotator` CLI enables `--experimental-sqlite` through its shebang, while direct package imports require:

```bash
NODE_OPTIONS=--experimental-sqlite node your-script.mjs
```

Node.js 22.13 and newer do not require this option.

## Setup

### Automatic (recommended)

Run the init command to register both OpenCode V2 entrypoints and create a default sidecar config:

```bash
npx -y @dmmop/opencode-key-rotator init
```

### Manual

The server plugin and local TUI plugin use separate OpenCode V2 configuration files. Add both entries, then restart OpenCode:

**opencode.json:**

```jsonc
{
  "plugins": ["opencode-key-rotator"],
}
```

**cli.json:**

```jsonc
{
  "plugins": ["opencode-key-rotator/tui"],
}
```

`init` creates or updates `~/.config/opencode/opencode.json`, `~/.config/opencode/cli.json`, and `~/.config/opencode/opencode-key-rotator.json` idempotently. Use `--config-dir` to target another OpenCode config directory. A direct path such as `./dist/tui.js` is only needed when developing the plugin locally.

### Uninstall

```bash
npx -y @dmmop/opencode-key-rotator uninstall
```

Saved keys and rotation logs are preserved on removal.

## CLI

```
opencode-key-rotator init [--config-dir <dir>]
opencode-key-rotator uninstall [--config-dir <dir>]
opencode-key-rotator switch [--provider <id>] [--alias <alias> | --credential-id <id>] [--data-dir <dir>]
opencode-key-rotator manage [--provider <id>] [--data-dir <dir>]
opencode-key-rotator status [--provider <id>] [--data-dir <dir>]
```

## Key management

Use `opencode-key-rotator switch` for an interactive provider and connection selector. Pass `--provider` and a unique `--alias` to use it non-interactively, or `--credential-id` to select an exact native connection. The interactive selector distinguishes duplicate labels.

Use `opencode-key-rotator manage` for an interactive local workflow that switches the active OpenCode connection. It does not use the agent. Add, rename, and remove connections exclusively through OpenCode's native connection flow.

Use `opencode-key-rotator status` to list aliases, synchronization health, and the latest automatic rotation recorded in `rotation.log.jsonl`.

The server only translates OpenCode events. Rotation policy, cooldowns, switching, and automatic rotation logs live in `rotation.ts`, while SQLite CRUD lives in `key-store.ts`; the CLI and TUI adapter call the same core operations.

The `./tui` adapter registers `/key-switch` and `/key-status`. Connections are added exclusively through OpenCode's native connection flow.

After each committed automatic rotation, the server emits `rpc.opencode-key-rotator.rotated`. The payload contains only a random event ID, timestamp, provider ID, and previous/active display aliases; it never includes credential IDs, values, errors or source event payloads. Each connected TUI suppresses duplicate toasts using a 256-entry LRU of event IDs and unsubscribes on unload. Repeated IDs refresh their position without another toast; evicted IDs can notify again if received later. Manual switching keeps its existing direct toast and does not emit this RPC event. Duplicate incidents, unknown providers, CAS skips and other non-rotation outcomes do not notify.

Notifications are live only: disconnected TUIs miss events, and transport failures do not undo a rotation or release its incident reservation. The singleton owner emits once for the shared credential database; all connected TUIs may display it regardless of their current project. This assumes the existing local shared-database setup; remote manual key commands still operate on the TUI machine's local database. There is no log polling, durable notification queue or replay. After upgrading, restart the OpenCode service (`opencode service restart`) and close/reopen every TUI so both entrypoints reload.

## Configuration

Create a sidecar config file at `~/.config/opencode/opencode-key-rotator.json`:

```json
{
  "rotation": {
    "enabled": true,
    "patterns": ["\\b429\\b", "rate\\s*limit", "quota", "resource exhausted", "usage limit", "insufficient quota"]
  }
}
```

The config file supports JSONC (comments and trailing commas). Resolution order:

1. `${configDir}/opencode-key-rotator.json`
2. Built-in defaults

## How rotation works

1. The plugin handles `session.retry.scheduled` events and evaluates every retry whose status is 429 or whose message matches the configured patterns.
2. `session.error` is a fallback and rotates on HTTP 429 or matching messages.
3. The provider comes from the event payload or the session model.
4. If at least two native connections exist for the provider, the plugin activates the next connection in a round-robin cycle. It tracks each connection by its native credential ID, so duplicate labels remain distinct.
5. If a rotated key fails on the next attempt, that connection enters a 2-minute cooldown and is skipped during subsequent rotations.
6. Switching only changes OpenCode's native `active` connection marker; credential values and rows are preserved.
7. One process-wide consumer handles all server plugin instances, including different locations and module reloads. Instances hold leases; removing the owner aborts and drains its subscription before transferring ownership to a remaining live context. Removing a non-owner leaves the subscription running.
8. Every decision is recorded in `~/.local/share/opencode/keys/rotation.log.jsonl`.

### Duplicate delivery and concurrent changes

Incident reservations are shared across contexts and module reloads, scoped to the database, and made before asynchronous provider inference. A message ID plus physical attempt identifies a failure across retry/step/execution/error phases; operation, retry, error, and event IDs are alternatives when available. Neither the active credential nor the event phase is part of the incident identity. Stable identities remain for the process lifetime in a 16,384-entry LRU; eviction is logged. Unidentified errors use a conservative 10-second, 1,024-entry cache based on a hash of normalized error fields. A phase with a message but no attempt temporarily coalesces with the corresponding explicit attempt. Distinct explicit attempts can rotate A → B → C → D without waiting for the dedupe window.

Reservations stay pending during provider inference. Concurrent copies wait rather than being discarded; `provider_unknown` releases the reservation so a waiting or later phase with a provider can proceed. Other terminal outcomes commit the reservation. Pending queues are separate from the bounded completed caches and disappear when their handlers settle; cancellation while still waiting does not consume the incident.

The active credential is captured before waiting for a pending reservation or provider inference. Automatic switching requires that credential ID to still be active inside `BEGIN IMMEDIATE`; otherwise it logs `active_changed` / `active_credential_changed_before_rotation` without selecting or activating another connection. Concurrent processes that captured the same failed credential therefore cannot advance several positions. No auxiliary tables or credential values are written.

Limits: this is bounded duplicate suppression, not durable exactly-once delivery. Evicted identities, process restarts, or unidentified duplicates arriving after 10 seconds can be processed again. Indistinguishable legitimate errors without attempt identity can be suppressed during that window. A late duplicate received by another process after a rotation cannot be attributed to the old credential because upstream events do not carry the failed credential ID. Cleanup cancels pending inference before rotation; a reserved incident interrupted there is not retried automatically. An unexpectedly ended stream emits `consumer_stream_ended`; recovery occurs on the next setup or owner handoff, not through a reconnect loop. Console diagnostics distinguish registry creation/reuse, lease counts, consumer starts, and cache eviction without logging event payloads or secrets.

## Data layout

```
~/.local/share/opencode/
  opencode.db                 # OpenCode native credentials/connections
  keys/
    rotation.log.jsonl             # Rotation decisions (JSON Lines)
```

## Troubleshooting

| Symptom                 | Cause                                                       | Fix                                      |
| ----------------------- | ----------------------------------------------------------- | ---------------------------------------- |
| `Provider unknown`      | The v2 event did not expose a provider ID                   | Check the provider event data            |
| `No fallback key`       | Only one connection exists for the provider                 | Add another OpenCode connection          |
| `All keys cooling down` | All connection labels are in cooldown after failed attempts | Wait 2 minutes or add another connection |

## Development

```bash
npm install
npm run typecheck
npm run build
npm test
npm run format
```

## Releasing

### Commit messages

`npm install` installs a Husky `commit-msg` hook. Commitlint rejects malformed
Conventional Commits before Git creates the commit (70-character header limit;
capitalized subjects are allowed). Ordinary Git merge messages are exempt, but
bare version numbers and `fixup!` messages are not. CI validates every new commit
and the PR title too, including after title edits, to cover squash merges and
hooks bypassed with `--no-verify`. The validator checks syntax, not whether an
agent chose the correct semantic type for the actual change.

### Automatic publication

The single **CI and Release** workflow tests pull requests and pushes to `main`.
It builds/typechecks and runs every test on Node 22.5 and Node 22, checks formatting,
smoke-tests the packed CLI on the minimum Node version, and runs every test on Bun.
The Bun and release jobs reuse the tested build. Only a successful push to `main`
can publish to npm and create a GitHub Release.

`semantic-release` uses Conventional Commits since the last release tag: `fix:`
produces a patch, `feat:` a minor, and `!` or a `BREAKING CHANGE:` footer a major.
Documentation, maintenance and test-only commits do not trigger a release unless
marked breaking. The largest applicable bump wins. Use conventional PR titles
when squash-merging.

Versions are tracked by Git tags and npm, not by automatic bump commits on `main`;
the published manifest receives the computed version. Tag pushes do not start
another workflow. npm Trusted Publishing must authorize this repository's
`release.yml` workflow (OIDC); publication includes provenance and needs no npm token.
If branch protection required jobs from the old `ci.yml`, update those required
checks to the new workflow's Node and Bun jobs before merging.

## License

MIT
