# opencode-llama-server-slot-save
[![npm version](https://img.shields.io/npm/v/opencode-llama-server-slot-save.svg)](https://www.npmjs.com/package/opencode-llama-server-slot-save)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://opensource.org/licenses/MIT)
[![OpenCode Plugin](https://img.shields.io/badge/OpenCode-Plugin-8B5CF6?style=flat)](https://opencode.ai/)

This plugin uses the llama-server `/slots` REST API to save the KV cache of the primary slot (`0`) to disk,
so it can be restored instantaneously after dispatching subagents. This avoids costly prefills 
when switching back to the primary agent/orchestrator. No prefill will occur and no input tokens will be
used.

The plugin saves the slot state before a subagent `task` dispatch, as well as on exiting the client.
It restores the KV cache on resume, with compaction-aware invalidation. Your prefill happens once and survives 
subagents and client restarts (see [Known Limitations](#known-limitations) 
for issues which affect this plugin at time of release).

## Why?

- Currently running multi-agent workflows can be very inefficient if you only have a single slot running
on your llama-server. We were seeing prefills of 2-5 minutes on the orchestrator every time a subagent task
ended and control was returned to the orchestrator. 

- Even with multi-slot setups, OpenCode (as of 1.18.31) seems to keep multi-agent workflows running on a single 
slot. This could also be a defect in llama-server.


## Features

- Saves the parent session's slot state before every `task` tool dispatch. When the
  parent's next LLM call runs, the plugin restores it.
- Saves on exit (`dispose`), so a resumed session can restore the last known state.
- Compaction-aware: a compaction leaves the slot holding the pre-compaction context,
  so the plugin invalidates the saved file immediately and saves it once the slot
  has been prefilled with the post-compaction context. A stale pre-compaction
  state can never be restored.
- Subagent sessions never save or restore.
- A single rotating filename bounds disk use to one file. Call `/slots/0?action=erase`
  to remove the file remotely.
- A per-user manifest records what the file currently holds (session, model, token
  count, timestamp), so a file saved by another session or model is never restored.
- Any save/restore error is logged and the session continues with a cold
  prefill.

## Requirements

- llama-server with slot save/restore support. Run with `--parallel 1` and `--slot-save-path <dir>`.
- An opencode provider whose `baseURL` points at that server. The plugin talks to the
  slot API on the same base URL (a trailing `/v1` is stripped), or to an explicit
  `serverUrl` option.

## Install

### From NPM

Add the plugin to `opencode.jsonc`:

```jsonc
{
	"plugin": ["opencode-llama-server-slot-save"]
}
```

Or if you have a `/slots` endpoint separate from the provider:

```jsonc
{
	"plugin": [
		["opencode-llama-server-slot-save", { "serverUrl": "http://127.0.0.1:8080" }]
	]
}
```

### Development (from a source checkout)

```sh
bun install
bun all
```

## Options

| Option | Type | Default | Notes |
| --- | --- | --- | --- |
| `enabled` | boolean | `true` | Master switch. `false` makes every hook a no-op. |
| `providerId` | string | `"llama.cpp"` | The opencode providerID to manage. Only LLM calls made through this provider trigger save/restore. |
| `serverUrl` | string | `null` (derived) | llama-server base URL, without `/v1`. When omitted, the base URL is derived from the provider's `baseURL` at request time. |
| `slot` | number | `0` | The llama-server slot index to save/restore. The server must run with a single slot (`--parallel 1`). |
| `filename` | string | `"oc-primary.bin"` | Slot-cache filename under the server's `--slot-save-path`. Every save overwrites the same file, bounding disk use to one file. |
| `timeoutMs` | number | `30000` | Per-request timeout for the save/restore HTTP calls. |

## How it works

- **Restore on takeover.** On every LLM call, if the calling session does not own the
  slot and the manifest matches (same session, provider, and model), the saved file
  is restored into the slot before the request goes out.
- **Save before `task` dispatch.** The `task` tool runs in the parent session and its
  child will take over the single slot. The plugin persists the parent's context first,
  so the child's clobber is recoverable.
- **Save on exit.** The `dispose` hook saves the current context, so it can be
  restored by a later process. The save is skipped when the slot still holds a stale
  pre-compaction context (a resync is pending) or when the last LLM call was a
  subagent's.
- **Compaction resync.** On `session.compacted` the manifest is invalidated (the file
  still holds the pre-compaction context). After the next LLM call it prefills the
  slot with the post-compaction context, then the file is saved (the `session.idle`
  event is a retry point if the first attempt fails).
- **Manifest missing = cold prefill.** If the file is missing, or was saved by another
  session or model, the restore is skipped and the session simply cold-prefills. A
  400 from the server (file invalid for the loaded model) clears the manifest so it
  is not retried for that session.

## Files

| File | Location |
| --- | --- |
| Slot cache | `<--slot-save-path>/<filename>`, on the server |
| Manifest | `~/.local/share/opencode/llama-slot-save/manifest.json`, per user |
| Log | `~/.local/share/opencode/log/opencode-llama-server-slot-save.log`, per user |

## Known limitations

- **Single slot only.** The plugin manages one slot of one server. The server must
  run with `--parallel 1`.
- **Exit-resume restore is blocked upstream (as of 0.1.0).** Restoring a slot state
  that the slot already holds (or holds a superset of) does not produce a usable KV in
  current llama.cpp builds, so the first turn after a client restart cold-prefills.
  This is tracked in upstream issues
  [ggml-org/llama.cpp#26676](https://github.com/ggml-org/llama.cpp/issues/26676) and
  [ggml-org/llama.cpp#28276](https://github.com/ggml-org/llama.cpp/issues/28276).
  The in-process save/restore around `task` dispatch works today and is the main
  case this plugin targets. Once a PR is merged for these issues, the plugin should
  work for the other cases.
- **File size grows with the cached tokens.** Expect tens of KB per cached token for
  a 27B-class model at long context (a 50k-token state is a multi-gigabyte file).
  Size the `--slot-save-path` volume accordingly.

## Logging

- Logs go to `~/.local/share/opencode/log/opencode-llama-server-slot-save.log`. Info
  level covers plugin load, every save/restore, compaction invalidations, and
  cold-prefills
- Debug adds the subagent/ownership checks. The log level  follows OpenCode's own 
  level (`--log-level` / `OPENCODE_LOG_LEVEL`).

## Troubleshooting

- **no llama-server URL / slot caching inactive:** The provider has no `baseURL`
  and no `serverUrl` option is set, or the LLM call is going through a provider
  whose ID does not match `providerId`.
- **404 on save/restore:** The server build predates the slot save/restore API, or
  the base URL is wrong. Check the log for the URL used.
- **cold prefill (no matching cache):** No manifest entry, or the file was saved
  by a different session/model. Expected - the session cold-prefills.
- **slot restore missed / manifest cleared:** The file was deleted, or the server
  loaded a different model than the one the file was saved for. Expected.
- **full prefill after a client restart:** See the upstream issues in
  [Known limitations](#known-limitations). The plugin is working as designed. The
  restore itself is a no-op in current llama.cpp builds.

## Development scripts

```sh
bun run build          # Compile TypeScript to dist/
bun run bundle         # Bundle with bun build for a single file bundle
bun run clean          # Remove build output, tarball and coverage reports
bun run deploy         # Build, pack, and install to local OpenCode cache
bun all                # Full cycle: clean -> build -> test -> deploy -> clean
bun start              # Run plugin directly (for debugging)
bun test               # Run tests
bun lint               # Lint source files with biome
bun run coverage       # Run tests with coverage report. This command requires `genhtml` to be installed. Run `bun test --coverage` for CLI reports.
```

## License

MIT
