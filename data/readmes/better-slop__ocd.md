# opencode daemon

A process manager for opencode, built with bun and opentui.

## Commands

### `ocd`/`ocd new` - create or reuse a project server and start a session.

| Arg               | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `path`            | Project path. Defaults to current working directory. |
| `--session`/`-s`  | Reuse explicit session id.                           |
| `--continue`/`-c` | Continue latest root session.                        |
| `--attach`/`-a`   | Attach immediately after resolving session.          |

### `ocd list` - list all tracked project servers.

| Arg      | Description                                     |
| -------- | ----------------------------------------------- |
| _(none)_ | This command has no positional args or options. |

This command is also available via the global flag: `ocd --list`.

`ocd list`/`ocd --list` prints each tracked instance with status, endpoint, and all attached sessions including busy/idle state and session title (from the OpenCode `/session` API).

### `ocd top` - show project resource usage.

| Arg                              | Description                                          |
| -------------------------------- | ---------------------------------------------------- |
| `path`                           | Project path. Defaults to current working directory. |
| `--tui`/`-t`                     | Launch top in Solid/OpenTUI view.                    |
| `--watch`/`-w`                   | Continuously refresh top output.                     |
| `--intervalMs`/`--interval`/`-i` | Sampling interval in milliseconds.                   |

In `--tui` mode, instances are shown as pages (one instance per view). Keyboard:
- `j`/`k` (or `down`/`up`) to move to next/previous instance page
- `h`/`l` (or `left`/`right`) to horizontally scroll the command column
- `H`/`L` for faster horizontal command scrolling
- `r` refresh, `q`/`esc`/`ctrl+c` quit

### `ocd attach` - attach to project server in native OpenCode UI.

| Arg              | Description                                          |
| ---------------- | ---------------------------------------------------- |
| `path`           | Project path. Defaults to current working directory. |
| `--session`/`-s` | Attach specific session id.                          |
| `--latest`/`-l`  | Attach latest root session.                          |

### `ocd stop` - stop one project server or all servers.

| Arg                   | Description                                          |
| --------------------- | ---------------------------------------------------- |
| `path`                | Project path. Defaults to current working directory. |
| `--all`/`-a`          | Stop every tracked project server.                   |
| `--graceMs`/`--grace` | Grace period before SIGKILL.                         |

### `ocd restart` - restart one project server.

| Arg                   | Description                                          |
| --------------------- | ---------------------------------------------------- |
| `path`                | Project path. Defaults to current working directory. |
| `--graceMs`/`--grace` | Grace period before SIGKILL.                         |
| `--continue`/`-c`     | Continue latest root session after restart.          |
| `--attach`/`-a`       | Attach immediately after restart.                    |

### `ocd gc` - prune stale entries and idle servers.

| Arg                      | Description                   |
| ------------------------ | ----------------------------- |
| `--idleMinutes`/`--idle` | Idle cutoff in minutes.       |
| `--orphan`               | Remove dead registry entries. |

### `ocd status` - show project health.

| Arg                              | Description                                          |
| -------------------------------- | ---------------------------------------------------- |
| `path`                           | Project path. Defaults to current working directory. |
| `--watch`/`-w`                   | Continuously refresh status output.                  |
| `--intervalMs`/`--interval`/`-i` | Refresh interval in milliseconds.                    |

## Development

To install dependencies:

```bash
bun install
```

To run:

```bash
bun run src/index.ts
```

To build a standalone binary:

```bash
bun run build:bin
```

To copy the bin to `~/.local/bin`:

```bash
bun run copy
```

To build the binary and copy it to `~/.local/bin`:

```bash
bun run build
```
