# opencode-node

[![npm](https://img.shields.io/npm/v/@matrix2305/opencode-node)](https://www.npmjs.com/package/@matrix2305/opencode-node)

A node plugin for OpenCode V2: a local OpenCode server connects to a remote
OpenCode server ("hub") and loads its agents, skills, commands, MCP servers and
file-based memory from there.

Status: **0.2.0** — setup + memory sync, CLI, cache-first startup, TUI
commands, conflict-safe push, tests, build and publish pipeline.

## How it works

```
hub (OpenCode 2.x, /home/matrix2305)
  ├─ /api/agent, /api/skill, /api/command, /api/config
  ├─ /api/fs/list, /api/fs/read
  └─ ~/.config/opencode, ~/agents

node (this machine)
  ├─ ~/.config/opencode-node/config.json     hub URL + passwordRef
  ├─ ~/.local/share/opencode-node/
  │    ├─ snapshot.json                      cached setup + hashes
  │    ├─ skills/<id>/SKILL.md               materialised skills
  │    └─ backup/<timestamp>/...             backups before overwrite
  ├─ ~/.config/opencode/agents/*.md          written from the hub
  ├─ ~/.config/opencode/commands/*.md        written from the hub
  └─ opencode.jsonc                          hub config + node plugin entry
```

On every OpenCode start the plugin applies the cached snapshot immediately
(skills are registered at runtime, agents/commands are files), then refreshes in
the background if the cache is older than `cacheSeconds`.

## Install

From npm:

```bash
npm i -g @matrix2305/opencode-node
oc-node init \
  --hub https://matrix2305.tailbd26da.ts.net \
  --password-ref keychain:opencode-matrix2305
```

With custom sync dirs:

```bash
oc-node init \
  --hub https://hub.example \
  --password-ref keychain:my-hub \
  --root remote=.config/opencode,local=~/.config/opencode,type=setup \
  --root remote=opencode-memory,local=~/opencode-memory,type=memory \
  --root remote=shared-docs,local=~/docs,type=mirror
```

From this repo:

```bash
npm install
npm run build
node dist/cli.js init --hub <url> --password-ref <ref>
```

- `--password-ref` accepts `keychain:<service>`, `secret:<name>`, `file:<path>`,
  `env:<VAR>` or a raw password (not recommended).
- `--config` replaces `~/.config/opencode/opencode.jsonc` with the hub config
  (mode 0600, backup kept) and removes the legacy `opencode.json` so only one
  document is active. The node plugin entry is preserved.
- `--restart` runs `opencode service restart`.
- Without `--config`, only agents/skills/commands/MCP are synced; local
  providers/models stay untouched.

## CLI

```bash
oc-node status           # hub, cache age, counts, applied state, config drift
oc-node doctor           # config, password, plugin entry, hub reachability
oc-node pull             # refresh snapshot + materialise files
oc-node push             # push locally changed memory back (conflict-safe)
oc-node pull --config    # also replace local opencode.jsonc with the hub config
oc-node config           # apply the config from the current snapshot
oc-node restart          # opencode service restart
```

The published CLI is `dist/cli.js` (Node >= 22). In the repo you can also run
`node src/cli.ts <command>` (Node 23+).

## Model list

`pull` fetches the hub's model list (`/api/model`) and the server plugin applies
it with a model transform: any local model that the hub does not have is set
`enabled: false`, so the picker shows exactly the hub's models. Disabled models
are not deleted — if the hub re-adds them later, the next refresh re-enables
them.

## Provider credentials (live, no files)

`sync.auth` (default on) pushes the hub's provider credentials **straight into
the local OpenCode server's credential store** during `init`, `pull` and every
background refresh:

- CLI path: `POST /api/integration/<id>/connect/key` on the local server.
- Plugin path: `ctx.integration.connect.key` with a stable label
  (`opencode-node:<hub>`), so re-syncs replace instead of stacking.
- Keys are never written to `auth.json` or any file, never logged, and never
  persisted in the snapshot (only a count + hash of provider names).
- Works without restarting the server — new keys are usable immediately.

## Plugins

`sync.plugins` (default on) pulls the plugin layer from the hub during
`oc-node init` and every `oc-node pull`:

- hub `plugins` / `plugin` entries are appended to the local `plugins` array
  (object form and options preserved, local entries never removed, idempotent);
- `~/.config/opencode/plugin/` and `plugins/` trees are copied;
- `package.json` dependencies are merged (local wins on conflicts).

The server plugin does the same on startup and after each refresh, then emits
`plugins` so the TUI can prompt for a restart. OpenCode installs npm plugins into
`~/.cache/opencode/npm` on the next start or `opencode reload`.

```bash
oc-node pull            # syncs setup, memory and plugins
oc-node pull --config   # also replaces opencode.jsonc with the hub config
```

## Multiple hubs

```bash
oc-node hub list
oc-node hub add work --url https://work.example --password-ref secret:opencode-work
oc-node hub use work --pull
oc-node hub remove work [--purge]
```

Each hub has its own `snapshot.json`, `applied.json` and skill cache under
`~/.local/share/opencode-node/hubs/<name>/`. Local agents, commands, memory and
`opencode.jsonc` are shared; the active hub's pull owns them (with backups).
Legacy single-hub configs migrate automatically.

## Config/providers modes

`sync.config` controls the raw hub `opencode.jsonc` (providers, models, plugins,
MCP):

| Mode | Behavior |
| --- | --- |
| `off` | never touch the local config |
| `manual` | only `oc-node config` / `oc-node pull --config` |
| `auto` | write the hub config when its hash changes |

```bash
oc-node config --mode auto      # set + apply now
oc-node config --mode manual
oc-node config --dry-run
```

Auto apply keeps the node plugin entry, removes the legacy `opencode.json`,
records `applied.config`, backs up every overwritten file, and logs
`config:auto-applied`. Restart OpenCode for a guaranteed clean load.
`auth.json` (provider credentials stored outside config) is not synced.

## What is synced

| Category | Mechanism |
| --- | --- |
| Skills | `ctx.skill.transform` at runtime; `SKILL.md` materialised under the data dir |
| Agents | `~/.config/opencode/agents/<id>.md` + `ctx.agent.reload()` |
| Commands | `~/.config/opencode/commands/<name>.md` + `ctx.command.reload()` |
| MCP | `ctx.mcp.transform` from the hub config |
| Config/providers | raw hub `opencode.jsonc` written locally (0600), plugin entry preserved, `off`/`manual`/`auto` modes |
| Sync dirs | configurable at init (`--root`): setup / memory / mirror types, repeatable |
| Memory | `~/agents/<agent>/` folder mirror with conflict-safe push (no memory tools; the hub memory plugin does that) |
| Plugins | hub `plugins` list merged into the local config, `plugin/` files copied, `package.json` dependencies merged |
| Auth | hub provider credentials connected **live** into the local OpenCode server (`connect/key`); never written to files |
| Models | hub model list applied at runtime; local-only models are disabled (`enabled: false`), nothing deleted |

## TUI

Server slash commands:

- `/node-status` — hub, cache age, counts, memory state.
- `/node-sync` — force a pull.
- `/node-push` — push memory changes.

TUI part (home footer + palette commands, live via RPC):

- footer status: `node 9s · 62m` (skills · memory, `↑` = pending)
- **opencode-node: status** — dialog with hub/cache/counts/memory.
- **opencode-node: sync now** — pull + toast.
- **opencode-node: push memory** — push + conflict/upload toast.
- Startup and `updated` event toasts.

## RPC

The server registers `matrix2305.opencode-node`:

- `status`, `sync`, `push`
- event `updated` (`kind`, `summary`)

```bash
curl -u opencode:<password> -X POST -H 'Content-Type: application/json' \
  -d '{"input":{}}' \
  'http://127.0.0.1:49374/api/rpc/matrix2305.opencode-node/status?location[directory]=/home/me'
```

## Memory (folder sync only)

Memory is a **folder mirror**, not a memory implementation. The hub config
installs the memory plugin; that plugin owns search, storage and prompts.

- Hub workspace `~/agents/<agent>/` is mirrored to `~/agents/<agent>/` on the
  node (paths rewritten between `/home/matrix2305/agents` and the local root).
- A locally modified file is never overwritten by a pull; it stays until pushed.
- Push is three-way: hub sha vs local hash vs last synced `localSha`. If both
  sides changed, a `.conflict-<node>-<timestamp>` copy is written and the hub is
  left untouched.
- A 10 s scan (`memory.syncIntervalSeconds`) pushes pending changes;
  `node.sync` and RPC `sync` pull and then push; `oc-node push` and RPC `push`
  are manual.
- No custom memory tools and no prompt injection. The only tools this plugin
  exposes are `status` and `sync`.

## Runtime constraints found in 2.3.0

- `AgentEditor` has no `add`; agents must be files + reload (asynchronous).
- `Skill.Info.path` must point to an existing file.
- Do not pass optional fields as `undefined` (`autoinvoke: undefined` silently
  drops the skill).
- `Command.Info` has no template; command files are copied instead.
- `/api/config` contains provider keys; never log it.
- `/api/fs/*` resolves relative paths against `location[directory]`; the client
  always sends the configured remote root.
- MCP transforms apply immediately, but `ctx.mcp.list()` is empty until the
  server connects.

See `docs/M0-FINDINGS.md` for the spike report.

## Security

- `config.json`, `opencode.jsonc` and the password file are `0600`.
- Secrets are never logged. Prefer `keychain:`/`secret:` over a password file.
- The hub password gives full filesystem access to the hub; treat it as a
  server admin credential.
- Every overwritten file is backed up under
  `~/.local/share/opencode-node/backup/<timestamp>/`.

## Development

```bash
npm install
npm run typecheck
npm test
npm run build
node dist/cli.js status
```

Build: tsup → `dist/index.js` (server), `dist/tui.js` (terminal),
`dist/cli.js` (CLI). See `docs/PUBLISH.md` and `docs/COMPATIBILITY.md`.

Repo layout:

```
src/config.ts    config file, password refs, paths
src/hub.ts       OpenCode hub client (Basic auth)
src/sync.ts      pull, snapshot, materialise, config apply
src/index.ts     OpenCode V2 plugin (cache-first + refresh + node tools)
src/cli.ts       oc-node CLI
docs/            findings and design notes
```
