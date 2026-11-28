# opencode plugin template

A starting point for an [opencode](https://opencode.ai) v2 plugin with all
four parts: server, TUI, GUI (OpenCode Desktop, experimental) and RPC. Each
part implements one or two small examples and lists every other area it can
extend as commented-out code. Uncomment what you need and delete the rest.

## Use the template

1. Click **Use this template** on GitHub (or clone and re-init git).
2. Rename the plugin:
   - `package.json` `name` (also the import path other plugins use for
     `<name>/rpc`)
   - `PLUGIN_ID` in `src/shared/constants.ts` (server id, TUI id prefix,
     tool namespace, RPC id)
   - the example agent (`agents/example.md`) and skill
     (`skills/example/`), plus their ids in `src/server/agents.ts` and
     `src/server/skills.ts`
   - the `example` reference (`references/example-docs/`, registered in
     `src/server/references.ts`)
3. Install and check:

   ```bash
   bun install
   bun run typecheck
   bun test
   bun run build      # GUI bundle -> dist/gui-experimental.cjs
   ```

4. Pin `@opencode/plugin` in `package.json` to your `opencode --version`.

## Load it in opencode

Add the checkout to `plugins` in `opencode.json(c)` (global or project):

```jsonc
{
  "plugins": ["<path-to-this-checkout>"]
}
```

With options for the server part (`ctx.options`). The example reads one:
`node`, the command that runs `mcp/hello_mcp.js` (default `node`; `bun` or
a full path also work):

```jsonc
{
  "plugins": [{ "package": "<path-to-this-checkout>", "options": { "node": "bun" } }]
}
```

One entry loads every part: the TUI loads the TUI parts of the plugins its
server loads, and OpenCode Desktop loads GUI parts from the global config.
Run `bun run build` (or `bun run build:watch`) before Desktop can show the
GUI part; the other parts run from source.

What the examples do once loaded:

| Part | Example | Try it |
| --- | --- | --- |
| Server | `example` agent, `example` skill, `hello` tool, `example` reference, `hello-mcp` MCP server, RPC handler | pick the agent; ask for the example skill, the hello tool or the MCP hello tool; attach the `example` reference and ask about chapter 1 |
| TUI | palette + `/plugin-ping` command | shows the server's RPC answer as a toast |
| GUI | "Ping the plugin's server part" palette command | shows the answer in a dialog |
| RPC | `ping` method | called by the TUI and GUI examples |

## Layout

```
package.json        exports: one key per part (".", "./server", "./tui", "./gui-experimental", "./rpc")
vite.config.ts      GUI build (the only part that needs one)
agents/             one agent per .md file (frontmatter + system prompt)
skills/             one skill per folder (SKILL.md)
references/         one directory per reference (example-docs/ is the "example" reference; attach it by alias)
mcp/                MCP servers the plugin ships (hello_mcp.js: stdio, no dependencies)
src/server/         server part: server.ts wires one file per domain
src/tui/            TUI part: tui.tsx wires one file per area
src/gui/            GUI part: gui.tsx wires one file per registry
src/rpc/            RPC contract shared by every part and outside callers
src/shared/         code more than one part imports
tests/              bun test
```

`AGENTS.md` describes the conventions for coding agents working in a plugin
made from this template.

## opencode V1 support

V1 support is included as an example. Target V2 first: build features on
the V2 API, and add V1 hooks only where they extend compatibility to
opencode 1.x users. Nothing in V1 should drive the design.

The server entry also works on opencode 1.x (1.18.29 or later). Its default
export is one object with both entry points:

- `setup()` (from `Plugin.define`): what V2 runs.
- `server()` (`src/server/v1.ts`): what V1 runs. It returns V1 hooks; the
  example's `config` hook adds the same agent and MCP server, reusing the
  loaders the V2 code calls.

V1 loads the plugin with `"plugin"` (singular) in `opencode.json`:
`{ "plugin": ["file://<path-to-this-checkout>"] }`. Targeting V2 only?
Delete `v1.ts`, its import and the `server: v1Server` line, and export
`Plugin.define(...)` directly.

## Before you add JSX

- **TUI** (OpenTUI + Solid): add `@opentui/core`, `@opentui/solid` and
  `solid-js` to `devDependencies` and to `peerDependencies`. `src/tui/tui.tsx`
  already carries the `@jsxImportSource @opentui/solid` pragma.
- **GUI** (Solid in Electron): `solid-js` is already a dev dependency; import
  only modules the desktop app provides (see the GUI docs, "Shared modules").

## Publish

Build the GUI first (`dist/` is in `files`), then `npm publish`. Users then
list the package name in `plugins` instead of a path.

## Docs

- [Plugins](https://opencode.ai/docs/build/plugins)
- [Server](https://opencode.ai/docs/build/plugins/server),
  [TUI](https://opencode.ai/docs/build/plugins/cli),
  [GUI](https://opencode.ai/docs/build/plugins/gui),
  [RPC](https://opencode.ai/docs/build/plugins/rpc)
