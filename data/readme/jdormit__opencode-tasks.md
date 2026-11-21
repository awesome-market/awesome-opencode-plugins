# opencode-tasks

Schedule background work in [OpenCode 2](https://opencode.ai/v2/docs). Recurring tasks live in cron markdown files; one-off tasks and session loops live in SQLite. A scheduler daemon executes due work through OpenCode's shared service.

Requires OpenCode 2.0.29 or later and [Bun](https://bun.sh). Version 1.0.0 targets the V2 plugin and client APIs.

## Installation

Add the plugin to your OpenCode config:

```json
{
  "plugins": ["opencode-tasks"]
}
```

Install the scheduler, which ticks every 60 seconds through launchd on macOS or a user systemd timer on Linux:

```sh
bunx opencode-tasks --install
```

The installer stages a bundled daemon in `~/.local/share/opencode-tasks/` so it survives package-manager cache cleanup and moved checkouts. It captures a sanitized `PATH`, `HOME`, and any XDG directory overrides, and chooses a stable Bun executable. Make sure OpenCode 2 is on that PATH. Re-run `--install` after upgrading or changing these paths. After successful installation, it removes unmodified V1 `loop.md`, `loop-stop.md`, and `loop-list.md` files from the configured global `command/` and `commands/` directories. Customized commands are preserved; rename or remove them yourself if they shadow the plugin's commands. When `XDG_CONFIG_HOME` is set, cleanup is confined to that configuration root.

The daemon discovers the shared service. If it isn't running, it invokes `opencode service start`, then discovers it again. Configure secrets, MCP tokens, environment, port, and other service settings in `$XDG_CONFIG_HOME/opencode/service.json` (normally `~/.config/opencode/service.json`). The daemon does not forward task-specific environments or the obsolete background-subagents flag.

Optionally install the agent skill:

```sh
bunx opencode-tasks --install-skill
```

Restart the OpenCode service after adding or upgrading the plugin. Slash commands are registered by the plugin; no command-file installation is required.

## Recurring tasks

Create `~/.config/opencode/tasks/daily-standup.md`:

```yaml
---
description: Summarize yesterday's work
schedule: "0 9 * * 1-5"
cwd: ~/projects/my-app
permission:
  - { action: shell, resource: "*", effect: deny }
  - { action: shell, resource: "git *", effect: allow }
  - { action: edit, resource: "*", effect: deny }
---

Summarize yesterday's git commits, including the files changed.
```

The filename is the task name. Schedules use the system's local timezone and standard five-field cron expressions: minute, hour, day of month, month, day of week.

| Field | Default | Meaning |
|---|---|---|
| `schedule` | Required | Cron expression, such as `0 9 * * 1-5` or `*/30 * * * *`. |
| `cwd` | Required | Working directory; `~` expands to HOME. |
| `description` | None | Human-readable description. |
| `session_name` | None | Reuse a named session; omit for a new session each run. |
| `model` | Service default | `provider/model#variant`; the variant is optional. |
| `agent` | Service default | Agent name. |
| `timeout` | `1h` | Duration such as `30m`, `2h`, or `1d`; numbers mean seconds. |
| `permission` | Agent/service rules | V2 ordered ruleset, or a legacy V1 permission object. |
| `enabled` | `true` | Set `false` to disable a task. |

## One-off tasks

Ask an agent to schedule work, or enqueue it from the CLI:

```sh
bunx opencode-tasks --schedule-task \
  --prompt "Run the test suite and summarize failures" \
  --description "Morning test run" --cwd ~/projects/my-app \
  --at 2026-11-01T08:00:00 \
  --permission '[{"action":"shell","resource":"bun test*","effect":"allow"}]'
```

Use `--now` to enqueue for the next tick. `--task <name>` copies a recurring task's prompt and settings into a one-off run. `--session-name`, `--model`, `--agent`, and `--permission` override those settings. Run `--schedule-task --help` for details. One-off runs have no execution timeout.

Task tools are exposed through V2 Code Mode. Agents use the catalog, or its `search(...)` discovery function when needed, then call the exact tool path inside `execute`. For example, if the catalog lists `tools.list_tasks`, use `execute` with `{ "code": "return await tools.list_tasks({})" }`. Calls return readable text; await them before execution ends. Slash commands remain directly available to users.

| Code Mode tool | Purpose |
|---|---|
| `schedule_task` | Schedule a one-off task. |
| `list_tasks` | List recurring and one-off tasks. |
| `cancel_task` | Cancel a pending one-off task or disable a recurring task. |
| `task_history` | Show outcomes, session IDs, timing, and errors. |
| `get_task_instructions` | Get the recurring frontmatter format. |
| `start_loop` | Start a loop in the calling session. |
| `list_loops` | List that session's active loops. |
| `stop_loop` | Stop a loop by full ID or an unambiguous prefix of at least eight characters. |

## Session loops

Loops deliver recurring prompts into an existing session, using its agent, model, and permissions. They are useful for checking CI or monitoring a deployment. The daemon drives them, so they continue with the UI closed and survive plugin or service restarts.

| Command | Result |
|---|---|
| `/loop 5m check the deploy` | Schedule a prompt every five minutes. |
| `/loop check the deploy` | Use the default five-minute interval. |
| `/loop 5m` | Use the default maintenance prompt. |
| `/loop` | Use the default interval and prompt. |
| `/loop-list` | List active loops in this session. |
| `/loop-stop <id>` | Stop one loop. |
| `/loop-stop` | Stop all loops in this session. |

Commands report their result as a visible synthetic notice without an LLM round trip. The same operations are available through agent tools.

Intervals are cron-aligned: `1m`–`59m`, `1h`–`23h`, or `1d`–`31d`. Sub-minute intervals are unsupported. Each loop expires after three days. Missed ticks are coalesced into one delivery, and transient failures retry at the next scheduled tick. Delivery is queued so it does not interrupt a busy session; at most one undelivered prompt per loop is retained. A missing session causes its loops to be deleted on the next delivery attempt.

## Permissions

Unattended task runs immediately reject permission asks with feedback to the model, which can continue without the denied action. They also cancel session-scoped questions and forms, including those from child sessions. Other users' sessions and global forms on the shared service are left alone. Loop deliveries use the existing session's normal permission handling.

Use V2 ordered rulesets in task frontmatter or as JSON in the `permission` tool/CLI argument:

```yaml
permission:
  - { action: shell, resource: "*", effect: deny }
  - { action: shell, resource: "git *", effect: allow }
  - { action: external_directory, resource: "/tmp/*", effect: allow }
```

Session rules are evaluated after agent rules. The **last matching rule wins**, so broad rules belong first and specific overrides last. Explicitly allow actions a task needs; `ask` cannot obtain approval in a background run. In particular, allow `external_directory` for paths outside the working directory.

Existing V1 task files still work. For example, `permission: { bash: { "git *": allow }, edit: deny }` is converted in declaration order. The renamed actions are `bash` → `shell`, `task` → `subagent`, and `write`/`patch` → `edit`. Other action and resource names are preserved.

## Session behavior

Each task run creates a session on the shared service with its directory, title, agent, model, permissions, and `metadata.opencodeTasks` provenance. The session ID is recorded before prompting, so a running task is visible from another client.

Set `session_name` to retain context across runs. A SQLite mapping stores the session ID; if that session is deleted, the next run creates a replacement. Runs without a name always create fresh sessions. Resume a task session with `opencode --session <session-id>`.

Success comes from the session's terminal `outcome`, after `session.wait`: only `succeeded` completes a task. Failed and interrupted executions are recorded as failures. Execution error messages are captured from events, with message history as a fallback. Recurring-task timeouts interrupt the service session before recording failure.

## CLI reference

```text
opencode-tasks --install                 Install/update scheduler and clean legacy commands
opencode-tasks --uninstall               Remove scheduler
opencode-tasks --install-skill           Install agent skill
opencode-tasks --status [--limit N]      Scheduler status and recent tasks
opencode-tasks --list [--limit N]        Task list and next run times
opencode-tasks --schedule-task --help    One-off scheduling options
opencode-tasks --run-once                Run a scheduler tick manually
opencode-tasks --help                    Help
```

## Architecture

`dist/index.js` is a `Plugin.define` server plugin, instantiated per location. It registers tools and code-backed commands and opens short-lived database connections. It has no timers or event subscriptions.

`dist/cli.js` is a standalone bundled Bun CLI. Each scheduler tick reaps failed workers and starts detached `--exec-task` workers for due recurring and one-off tasks before delivering loops. Loop delivery has a shared ten-second service connection deadline and parallel five-second delivery deadlines, so one stalled session cannot block other loops or task scheduling. Workers use `@opencode/client` to create or reuse sessions, subscribe before prompting, reject unattended input requests, wait for completion, and record outcomes. They do not spawn `opencode run` or parse NDJSON.

Task definitions remain in `~/.config/opencode/tasks/*.md`; the plugin and daemon share `~/.config/opencode/.tasks.db`. Loop rows include the session ID, directory, prompt, cron interval, next run, and expiry. A conditional database claim prevents concurrent ticks from delivering the same due loop twice. The installer preserves the scheduler's PATH so CLI service startup works under launchd's minimal environment.

## Using OpenCode 1.x

Install `opencode-tasks@0.5.3`, the last V1-compatible npm version, or use the `v1` git tag:

```json
{ "plugin": ["opencode-tasks@0.5.3"] }
```

```sh
bunx opencode-tasks@0.5.3 --install
```

The source is also available as `github:jdormit/opencode-tasks#v1`.

## Development

```sh
bun install
bun run test
bun run typecheck
```

`bun run test` builds first. After building, `bun test` runs the suite directly. The real-service test is opt-in through `TASKS_E2E=1` and requires the isolated `tasks` environment with service port 49403, mock model port 50403, and `HOME=/tmp/oc2-tasks/home`; see `src/__tests__/service-e2e.test.ts`.

## License

MIT
