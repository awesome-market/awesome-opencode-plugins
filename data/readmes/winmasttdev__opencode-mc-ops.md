# opencode-mc-ops

An [OpenCode](https://opencode.ai) V2 plugin that lets an AI agent **monitor and operate local Minecraft servers** (Paper / Fabric / vanilla) running on the same Linux box.

It exposes five tools in the `mc` namespace:

| Tool | Id | Purpose |
| --- | --- | --- |
| `status` | `mc_status` | Running state, uptime, memory, version, players, TPS, recent errors |
| `logs` | `mc_logs` | Tail and filter `logs/latest.log`, highlighting errors |
| `backup` | `mc_backup` | Newest backup archive + systemd backup timer state |
| `cmd` | `mc_cmd` | Run a console command over RCON (allowlist + confirmation gated) |
| `restart` | `mc_restart` | Restart a server through its systemd unit (double gated) |

The plugin has **zero runtime dependencies** and never prints the RCON password.

---

## Install

### From a local checkout (recommended)

Add the plugin to `opencode.jsonc` (global `~/.config/opencode/opencode.jsonc` or a project one):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "file:///home/winmastt/dev/opencode-mc-ops",
      "options": {
        "servers": [
          {
            "name": "SchoolServer",
            "dir": "/mnt/GamesProjects/servers/SchoolServer",
            "type": "paper",
            "service": "zenith-server.service",
            "backupTimer": "mc-backup.timer"
          },
          {
            "name": "MechanicsCubed",
            "dir": "/mnt/GamesProjects/servers/MechanicsCubed",
            "type": "fabric",
            "service": "minecraft.service",
            "backupTimer": "mc-mechanics-backup.timer"
          }
        ],
        "allowedCommands": ["list", "save-all", "save-off", "save-on", "tps", "whitelist", "seed", "time", "weather", "difficulty", "gc"],
        "dangerousCommands": ["stop", "restart", "op", "deop", "ban", "pardon", "whitelist off", "kick", "end", "save-all flush"],
        "allowRestart": true,
        "allowCommands": true
      }
    }
  ]
}
```

Restart OpenCode (or reload the plugin) so the tools are registered.

### From npm

Once the package is published:

```jsonc
{
  "plugins": [
    {
      "package": "opencode-mc-ops",
      "options": { "servers": [ /* … */ ] }
    }
  ]
}
```

---

## Options reference

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `servers` | `ServerConfig[]` | `[]` | The servers to manage. See below. |
| `allowedCommands` | `string[]` | `list, save-all, save-off, save-on, tps, whitelist, seed, time, weather, difficulty, gc` | Console commands that may be executed. Anything else is refused. |
| `dangerousCommands` | `string[]` | `stop, restart, op, deop, ban, pardon, whitelist off, kick, end, save-all flush` | Commands that additionally require `confirm: true`. |
| `allowCommands` | `boolean` | `true` | Master switch for `mc_cmd`. When `false` every command is refused. |
| `allowRestart` | `boolean` | `false` | Master switch for `mc_restart`. |
| `rconHost` | `string` | `127.0.0.1` | Default RCON host. |
| `rconPort` | `number` | `25575` | Default RCON port (used when `server.properties` has no `rcon.port`). |
| `rconPassword` | `string` | `""` | Default RCON password. Empty means "read it from `server.properties`". |
| `rconTimeoutMs` | `number` | `5000` | RCON connect/command timeout. |
| `useSudo` | `boolean` | `false` | Run the restart through `sudo -n systemctl restart …`. |
| `restartCommand` | `string` | `null` | Custom restart command template, e.g. `"sudo -n systemctl restart {unit}"`. `{unit}` is replaced by the unit name. |
| `backupDirNames` | `string[]` | `["backups", "backup"]` | Directory names searched inside a server directory for backups. |

### Server configuration

| Field | Type | Description |
| --- | --- | --- |
| `name` | `string` | Display name, used to select the server in every tool. |
| `dir` | `string` | Absolute path of the server directory. |
| `type` | `"paper" \| "fabric" \| "vanilla" \| "other"` | Server implementation. Used for hints only. |
| `service` | `string` | systemd unit that runs the server, e.g. `zenith-server.service`. Enables running state, uptime, memory and restart. |
| `backupTimer` | `string` | systemd timer that drives the backup job, e.g. `mc-backup.timer`. |
| `backupDirs` | `string[]` | Explicit backup directories. Defaults to `<dir>/backups` and `<dir>/backup`. |
| `logFile` | `string` | Log file to read. Defaults to `<dir>/logs/latest.log`. |
| `rcon.host` / `rcon.port` / `rcon.password` | `string` / `number` / `string` | Per-server RCON overrides. |
| `rconHost` / `rconPort` / `rconPassword` | `string` / `number` / `string` | Flat aliases for the same settings. |

**RCON password resolution** — the password is looked up in this order and the first non-empty value wins:

1. `servers[].rcon.password`
2. `servers[].rconPassword`
3. top level `rconPassword`
4. `rcon.password` in `<dir>/server.properties` ← the normal case

The resolved password is used for the connection only. It is never logged, never echoed in tool output and never included in error messages.

---

## Tools

### `mc_status`

**Input**

```jsonc
{
  "server": "SchoolServer" // optional: omit to inspect every configured server
}
```

**Output**

```
SchoolServer (paper) — RUNNING
  service:   zenith-server.service (active/running, since Mon 2026-10-20 09:17:55 EEST, up 2h 26min)
  memory:    4.21 GiB
  version:   Paper 26.2-84-main@26e81c4 (Minecraft 26.2)
  players:   3/120 online (live rcon)
  tps:       20.0 (1m), 20.0 (5m), 20.0 (15m) (rcon)
  rcon:      127.0.0.1:25575 (reachable)
  recent errors (1):
    - [Train_Carts] Failed to save offline group data to disk (x29)
      java.nio.file.FileSystemException: plugins/Train_Carts/trains.groupdata.tmp: Invalid argument
```

When a server is **stopped** the tool says so explicitly, shows the stop reason (or the last error) and the last log lines:

```
MechanicsCubed (fabric) — STOPPED
  service:   minecraft.service (inactive/dead)
  memory:    unknown
  version:   Fabric 26.2 (Loader 0.19.5)
  players:   unknown (max 20)
  tps:       unknown
  rcon:      disabled (enable-rcon=false in server.properties)
  stop:      server was stopped — [10:06:24] [Server thread/INFO]: Stopping server
  last log lines:
    [10:06:24] [C2ME Storage #2/INFO]: Storage thread Thread[#153,C2ME Storage #2,8,main] stopped
```

Data sources:

* **running state** — `systemctl show -p ActiveState -p SubState`
* **uptime** — `systemctl show -p ActiveEnterTimestamp` (plus the monotonic clock as fallback)
* **memory** — `systemctl show -p MemoryCurrent`
* **version** — parsed from the log banner (`This server is running Paper version …`, `Loading Minecraft … with Fabric Loader …`, `Starting minecraft server version …`); when `logs/latest.log` was rotated, `server.log` / `startup.log` are checked as well
* **players** — live RCON `list`, falling back to the last `There are N of a max of M players online:` log line
* **TPS** — live RCON `tps`, falling back to the last `TPS from last 1m, 5m, 15m:` log line
* **max players** — `max-players` from `server.properties`
* **recent errors** — the last distinct `ERROR` / `FATAL` / exception messages, repeated occurrences collapsed into an `xN` counter

### `mc_logs`

**Input**

```jsonc
{
  "server": "SchoolServer",  // optional
  "grep": "Train_Carts",     // optional regular expression (case insensitive)
  "lines": 200               // optional, default 200, max 5000
}
```

**Output**

```
SchoolServer — matching /Train_Carts/ of /mnt/GamesProjects/servers/SchoolServer/logs/latest.log
scanned 20000 lines, 612 matched, 500 shown, 500 error lines
(output truncated — showing the most recent matches only)

!! [15:10:41] [TrainCarts-OfflineGroupSaver/ERROR]: [Train_Carts] Failed to save offline group data to disk
!! java.nio.file.FileSystemException: plugins/Train_Carts/trains.groupdata.tmp: Invalid argument
```

Lines that look like an error are prefixed with `!!`. An invalid regular expression is reported instead of throwing.

### `mc_backup`

**Input**

```jsonc
{
  "server": "SchoolServer" // optional
}
```

**Output**

```
SchoolServer — backups
  directories: /mnt/GamesProjects/servers/SchoolServer/backups
  newest:      zenith_backup_20261007_000000.tar.gz
    path:      /mnt/GamesProjects/servers/SchoolServer/backups/zenith_backup_20261007_000000.tar.gz
    size:      17.9 GiB
    age:       13d 11h 53min ago
  files:       2 found (1 archives)
  timer:       mc-backup.timer (active)
    last run: Tue 2026-10-20 09:17:55 EEST [success]
    next run: Wed 2026-10-21 00:00:00 EEST
```

The timer information comes from `systemctl show -p LastTriggerUSec -p NextElapseUSecRealtime -p Result`.

### `mc_cmd`

**Input**

```jsonc
{
  "server": "SchoolServer",
  "command": "list",
  "confirm": false // only needed for dangerous commands
}
```

**Output**

```
$ list  (SchoolServer)
There are 3 of a max of 120 players online: Steve, Alex
```

Refusals explain exactly what is wrong:

```
Refusing to run "say hello": it is not on the allowlist. Allowed commands: list, save-all, tps, whitelist, gc.
```

```
Refusing to run "whitelist off": it is classified as dangerous. Re-run the tool with confirm: true if you really want to execute it.
```

If RCON is not reachable:

```
RCON is unreachable for SchoolServer at 127.0.0.1:25575: connect ECONNREFUSED 127.0.0.1:25575
```

### `mc_restart`

**Input**

```jsonc
{
  "server": "MechanicsCubed",
  "confirm": true
}
```

**Output**

```
Restarted minecraft.service (MechanicsCubed). The unit is now active/running.
```

or, on failure:

```
Failed to restart minecraft.service (MechanicsCubed): Job for minecraft.service failed because the control process exited with error code.
```

---

## Safety model

The plugin is built to be safe to hand to an autonomous agent.

1. **Allowlist** — `mc_cmd` only runs commands whose name (or full form) appears in `allowedCommands`. Everything else is refused with a message that lists the allowed commands.
2. **Dangerous list** — commands in `dangerousCommands` need an explicit `confirm: true` on the tool call. A bare entry such as `stop` covers every command that starts with it; an entry with arguments such as `whitelist off` only covers that exact command (and longer variants of it).
3. **Two gates for dangerous commands** — a command has to be allowlisted *and* confirmed. `stop` is refused as long as it is not allowlisted; as soon as it is, the confirmation prompt is required.
4. **Master switches** — `allowCommands: false` disables `mc_cmd` completely, `allowRestart: false` disables `mc_restart` completely. `allowRestart` defaults to `false`, so a fresh installation cannot restart anything until it is switched on explicitly.
5. **Permission prompts** — before a console command that is not known to be read-only (`list`, `tps`, `seed`, `help`, `version`, `whitelist`) and before every restart, the plugin calls `ctx.permission.assert(...)`, so OpenCode can ask the user for approval. Errors are propagated, never swallowed.
6. **Double confirmation for restarts** — `mc_restart` requires both `allowRestart: true` in the options and `confirm: true` on the call.
7. **Read-only by default** — `mc_status`, `mc_logs` and `mc_backup` never change anything.
8. **No secret leakage** — the RCON password is never printed, never logged and never part of an error message.

---

## Requirements

* **Linux** with **systemd** (`systemctl` must be on `PATH`).
* **Node.js ≥ 22** or **Bun** — the plugin is plain TypeScript and is loaded by the OpenCode runtime.
* **A Minecraft server** reachable on the local machine, with:
  * a `server.properties` file (`max-players`, `rcon.*`),
  * a `logs/latest.log` file,
  * optionally a systemd unit (needed for `mc_status` running state and for `mc_restart`).
* **RCON** for `mc_cmd` and for live player/TPS numbers:
  * Paper: `enable-rcon=true`, `rcon.port=25575`, `rcon.password=<secret>`.
  * Fabric has no built-in RCON — enable it with a mod (e.g. `rconmod`) or use `mc_cmd` only on Paper servers.
* **Permission to restart** — `systemctl restart` normally needs root. Either run OpenCode as a user that may restart the unit, or enable `useSudo: true` (this box has passwordless sudo) or set a custom `restartCommand`.

### systemd notes

`zenith-server.service` carries a drop-in that stops the unit from starting while the sleep sentinel exists:

```ini
# /etc/systemd/system/zenith-server.service.d/sleep.conf
[Unit]
ConditionPathExists=!/mnt/GamesProjects/servers/SchoolServer/.asleep
```

If the sentinel is present, `systemctl restart zenith-server.service` succeeds but the unit stays inactive; the plugin reports the resulting state so the agent can explain what happened.

---

## How it works

```
index.ts                 plugin entry point: registers the five tools in the "mc" namespace
src/core.ts              all logic — option parsing, log parsing, command policy, formatting
src/systemd.ts           systemctl helpers + server.properties reader
src/rcon.ts              minimal Source-RCON client (no dependencies)
types/opencode.d.ts      ambient declaration of the OpenCode V2 plugin API
tests/core.test.ts       unit tests (node:test)
```

* **No OpenCode imports in the logic.** `src/core.ts` and `src/systemd.ts` do not import `@opencode/plugin`, so they can be unit tested with plain `node --test`. Only `index.ts` touches the plugin API, and it does so with `import type` (type-only, erased at runtime).
* **Bounded I/O.** The servers live on an NTFS mount where directory walks are slow, so the plugin never scans a world directory. Logs are read by seeking to the tail of the file and reading a bounded number of bytes (512 KiB normally, 4 MiB when a grep filter is used). Backup directories are only listed one level deep and only the file metadata is read.
* **systemd first.** Running state, uptime and memory come from `systemctl show` (single invocation per server), not from log scraping.
* **Live data with graceful fallback.** RCON is probed with a short timeout. When it is disabled or unreachable the plugin falls back to the log and says which source it used.
* **Pure helpers.** Parsing (`server.properties`, log lines, versions, TPS, player counts) and the command policy are pure functions, which is what the test suite exercises.

---

## Development

```bash
npm install          # installs the dev dependencies (typescript, @types/node)
npm run typecheck    # tsc --noEmit
npm test             # node --test tests/
```

The test suite is hermetic: it uses inline fixtures and never touches the network or a real server.

## License

MIT — Copyright (c) 2026 winmasttdev
