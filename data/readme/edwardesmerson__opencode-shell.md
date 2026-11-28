# opencode-shell

An OpenCode plugin that adds prompt-based shell execution. Enter `!!` followed by a command to run it in the current project directory. The plugin displays recent command output in the prompt area.

A single `!` still uses OpenCode's native shell mode. The plugin consumes and resets `!!` submissions before OpenCode can submit them to the model, and aborts active runs when the TUI plugin is disposed.

## Requirements and API

Version 0.2.0 targets the **v2 plugin API**, not an OpenCode 2.x release. It supports OpenCode `>=1.18.25 <2` and pins `@opencode-ai/plugin` to `1.18.25`, which already includes the Promise API and its host loader.

- The package root exports `define({ id, setup })` from `@opencode-ai/plugin/v2/promise`. Its setup intentionally registers no server hooks because shell execution is entirely local to the TUI.
- `opencode-shell/server` retains the empty legacy server entrypoint so existing server loading configurations continue to work.
- `opencode-shell/tui` exports `{ id, tui }` using `@opencode-ai/plugin/tui`. The pinned SDK has no v2 TUI entrypoint, so prompt slots, keymap interception, and lifecycle cleanup continue to use this separate API. The host automatically disposes registered slots and keymap interceptors.
- All exports point directly to TypeScript source. There is no build step.

The [v1.18.25 Promise API guide](https://github.com/anomalyco/opencode/blob/v1.18.25/packages/plugin/src/v2/promise/README.md) describes imperative setup. The [v2 loader](https://github.com/anomalyco/opencode/blob/v1.18.25/packages/core/src/config/plugin/external.ts) reads a default `{ id, setup }` export from the package root. The [TUI host](https://github.com/anomalyco/opencode/blob/v1.18.25/packages/opencode/src/plugin/tui/runtime.ts) still loads `./tui` separately and scopes registrations to the plugin lifetime.

## Install from npm

Add the package to the `plugin` array in `~/.config/opencode/tui.json`. Preserve any existing entries:

```json
{
  "plugin": ["opencode-shell@0.2.0"]
}
```

This TUI configuration is required for `!!`. Adding the package only to the server config does not enable the prompt UI. Quit and restart OpenCode after changing the configuration.

If you also want the no-op v2 server entrypoint loaded, use the v2 host's plural `plugins` array in `opencode.jsonc`:

```json
{
  "plugins": ["opencode-shell@0.2.0"]
}
```

Existing entries in the legacy singular `plugin` array in `opencode.jsonc` still load the empty `./server` export. To switch server loading to v2, move the entry to the plural `plugins` array. The TUI still uses singular `plugin` in `tui.json`.

## Install from source

```sh
git clone https://github.com/edwardEsmerson/opencode-shell.git ~/src/opencode-plugins/opencode-shell
cd ~/src/opencode-plugins/opencode-shell
npm ci
```

Add the absolute checkout directory to the `plugin` array in `~/.config/opencode/tui.json`, for example:

```json
{
  "plugin": ["/home/you/src/opencode-plugins/opencode-shell"]
}
```

For optional v2 server loading on the minimum supported host, put the absolute path to `src/index.ts` in the plural `plugins` array in `opencode.jsonc`. That loader imports local file paths directly rather than resolving checkout directories.

Use either the local checkout or the npm package in each config, never both copies. Quit and restart OpenCode after source or loading-config changes; running sessions keep the loaded code.

## Develop

```sh
npm ci
npm run typecheck
npm test
```

The plugin's TUI entrypoint is `src/tui.tsx`. `src/shell.ts` parses commands and runs Bash. The v2 server entrypoint is `src/index.ts`; `src/server.ts` retains legacy server compatibility.

Entrypoint tests exercise package export resolution and mock the TUI API; they do not render a live OpenCode UI. After restarting OpenCode, smoke-test `!! pwd` on both the home and session prompts, confirm the active project directory and inline output, verify that single-`!` mode still works and `!!` never becomes a model message, then disable the plugin during a running command to check cleanup.
