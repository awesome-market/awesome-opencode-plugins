# oc-sidebar-extra

Four sidebar blocks for the OpenCode v2 TUI that the host does not ship: subagents,
usage detail, workspace state and tool activity.

One `append` claim on `sidebar.content`, so the blocks render underneath the
built-in Context, Limit, MCP and Todo blocks.

## Blocks

| Block | Shows |
| --- | --- |
| **SUBAGENTS** | Child sessions of the current one: running dot, title, elapsed time, cost. Click a row to focus that session. |
| **USAGE** | OpenCode Go allowance meters (rolling 5h, weekly, monthly), plus input/output/thinking/cache tokens, output speed and session cost for the current step. |
| **WORKSPACE** | Directory name, branch, clean/modified/conflict state, modified file count, `+added`/`−removed` from `git diff --numstat`, untracked, binary and submodule counts. |
| **TOOLS** | The last four tool calls of the current step with status glyph and duration. |

Everything is signal-driven off `context.data`; there is no render loop. The only
timers are a 1 s tick while a session is actually running and a 5 min refresh of
the Go usage limits. Git is spawned at turn boundaries, never per tool call.

## Install

Tested on OpenCode 2.3.0 with `@opencode/plugin` 2.2.4.

```sh
git clone https://github.com/b-rucel/oc-sidebar-extra.git
cd oc-sidebar-extra
bun install
```

Discovery loads bare directories from `~/.config/opencode/plugins/`, and skips
any directory that contains a `package.json`. So the live entry point is two
shims that re-export this package:

```sh
mkdir -p ~/.config/opencode/plugins/oc-sidebar-extra
```

`~/.config/opencode/plugins/oc-sidebar-extra/server.ts`

```ts
export { default } from "/absolute/path/to/oc-sidebar-extra/src/server.ts"
```

`~/.config/opencode/plugins/oc-sidebar-extra/tui.ts`

```ts
export { default } from "/absolute/path/to/oc-sidebar-extra/src/tui.tsx"
```

Restart OpenCode. The shims hold no manifest, so edits to `src/` reload from the
clone directly.

### Why there is a server stub

A TUI-only plugin still needs `server` and `index` to resolve, or `PluginModule.load`
throws `Plugin entrypoint not found` and the plugin never reaches `plugin.list`.
`src/server.ts` registers the id and does nothing else.

## Layout

```
src/tui.tsx     the four panels, JSX via @opentui/solid
src/lib.ts      pure selectors: token buckets, tps, tool rows, elapsed, formatters
src/server.ts   no-op server half
```

`src/lib.ts` is deliberately free of JSX, timers and I/O so the numbers can be
checked without a terminal.

## Development

```sh
bun run typecheck
```

## Lineage

Ported from the Atelier sidebar, a Claude Code plugin that opened a fixed 30×24
pane and re-rendered it on every frame. This version moves the same information
into a native TUI slot, reads it from the session store instead of an atom cache,
and stops spawning git on every tool call — the original did two git processes
per call.

## License

MIT
