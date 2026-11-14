# Claude Agent for DeepSeek Harness

A `claude-agent` model provider for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) that follows the design **opencode** shipped in its own `claude-agent` provider: it runs the user's installed `claude` binary through Anthropic's **official Claude Agent SDK**. Claude Code keeps its own authentication, its own client and its own request; the plugin adds the harness's UI, tools and history around it.

In steady state this provider gets **>90% prompt-cache hits** (96–100% per tool round in our measurements on Claude Code 2.1.317). See [Prompt caching](#prompt-caching).

> Not affiliated with, endorsed by, or sponsored by Anthropic, opencode, or DeepSeek. "Claude" and "Claude Agent" are used descriptively under Anthropic's branding guidelines; the product name of this plugin is Claude Agent, not Claude Code.

## Why this design

The short version: **do not become a third-party client for subscription credentials.** Let the unmodified Claude Code binary make the request.

- The plugin never reads `~/.claude/.credentials.json`, never runs an OAuth flow, and has no login screen.
- Every model request is made by the `claude` program the user installed and signed in with, on the user's machine, under the user's own account.
- Nothing is collected, stored, proxied or replayed: the plugin only passes documented SDK options and environment variables.
- The binary is not modified, and no authentication method is disabled. On the contrary, the plugin clears `CLAUDE_CODE_SIMPLE`, which would skip the login.
- Branding follows the [Agent SDK branding guidelines](https://code.claude.com/docs/en/agent-sdk/overview.md#branding-guidelines): "Claude Agent" is allowed, "Claude Code" as a product name is not.

Anthropic's current [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance.md) page says OAuth tokens are for "ordinary use of Claude Code and other native Anthropic applications", and that developers may not "offer Claude.ai login into their own applications, or route requests through Free, Pro, Max, or Ultra plan credentials on behalf of their users", nor "collect, store, or intermediate Claude.ai credentials or session tokens". The same page expressly allows an end user to sign in to the **unmodified Claude Code binary** with their own subscription.

That is the case this plugin implements: the user signs in with `claude`, and the plugin drives that binary. It works with a subscription, an API key, Bedrock, Vertex, Foundry or an enterprise gateway because it does not force any billing route.

For a **hosted product** that offers Claude to third parties, use API key authentication (or a commercial agreement), as the [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview.md) recommends. A local plugin running the user's own Claude Code is a different case. The full analysis, with references to opencode's specification and source, is in [docs/opencode-approach.md](docs/opencode-approach.md).

## Features

- **Claude models from your own login**: Opus, Sonnet, Haiku and the explicit model ids Claude Code reports, discovered at runtime and cached.
- **Harness tools over MCP**: Claude Code's built-in tools are off. The harness's tools are exposed through an in-process MCP server with their JSON Schemas sent verbatim.
- **Tool rounds that survive**: a Claude turn parks at a tool boundary and resumes when the harness returns the results, instead of losing the process.
- **History that resumes**: the harness history is the source of truth; only what Claude has not seen is sent, and Claude's transcript is resumed across restarts.
- **Isolation**: no Claude Code settings files, hooks, skills, `CLAUDE.md`, MCP servers, auto-memory, auto-compaction, advisor, tool search, or non-streaming/refusal fallbacks.
- **Correct usage reporting**: per-call token usage, including cache reads and writes, so the harness can show the real prompt-cache hit rate.
- **Lazy SDK**: the SDK is loaded on first use and can be swapped for one from `PATH` or a configured executable.

## Requirements

- DeepSeek Harness 0.2.1 or later (the provider is a Host bundle).
- Claude Code **2.1.248 or later** installed and signed in:

  ```sh
  claude --version
  claude auth login
  ```

- The `claude` binary must be on `PATH`, or set `executable` in the plugin config.

The plugin does **not** use the binary that the SDK downloads; it runs yours, so your CLI version and your login are the ones in charge.

## Install

In DeepSeek Harness Desktop, open the **Plugin Manager** and install a bundle from this directory. The bundle inserts one row, `claude-agent`, and disables nothing else.

On a profile that Electron does not manage:

```sh
dsh plugin --profile <profile> add /path/to/dsh-claude-agent
```

Reload the plugin (or restart DSH) after replacing the files, so the Host loads the new module generation.

Then pick **Claude Agent** in the model selector, or set it as the default:

```yaml
- id: agent-default-model
  config:
    provider: claude-agent
    model: opus          # or sonnet, haiku, claude-opus-5-5, ...
    reasoningEffort: high
```

## Configuration

```yaml
- id: claude-agent
  name: 'dsh-claude-agent'
  config:
    # Optional. Defaults to `claude` on PATH.
    executable: /usr/local/bin/claude
    # Optional. Working directory for the Claude process.
    cwd: /home/you/project
    # Optional. Output cap, passed as CLAUDE_CODE_MAX_OUTPUT_TOKENS.
    maxOutputTokens: 32000
    # Minutes of inactivity before the process is stopped (default 5).
    idleMinutes: 5
    # Minutes a parked tool round is kept (default 30).
    parkedMinutes: 30
    # Connection settings, mapped exactly like opencode.
    baseURL: https://api.anthropic.com
    apiKey: sk-ant-...
    # authToken, headerTimeout, chunkTimeout, headers, body
```

| Plugin config | Claude Code setting |
| --- | --- |
| `baseURL` | `ANTHROPIC_BASE_URL` |
| `apiKey` | `ANTHROPIC_API_KEY` |
| `authToken` | `ANTHROPIC_AUTH_TOKEN` |
| `headerTimeout` | `API_TIMEOUT_MS` |
| `chunkTimeout` | `CLAUDE_STREAM_IDLE_TIMEOUT_MS` |
| `headers` | `ANTHROPIC_CUSTOM_HEADERS` |
| `body` | `CLAUDE_CODE_EXTRA_BODY` |
| `maxOutputTokens` | `CLAUDE_CODE_MAX_OUTPUT_TOKENS` |

Without explicit connection settings the plugin inherits the environment and lets the `claude` login decide. Config wins over the shell.

## Prompt caching

Prompt caching is the difference between a usable agent and an expensive one. The adapter is built to keep Claude's prefix stable:

- One long-running `claude` process per harness session; tool rounds park it instead of restarting it.
- The system prompt, tool list and connection settings are hashed; the process restarts only when one of them really changes.
- The harness history is fingerprinted. Only the messages Claude has not seen are appended; if the history changed (edit, undo, model switch), one `<conversation-checkpoint>` rebuild is sent instead of pretending the old prefix still applies.
- Usage is reported from each API message, never from the SDK's whole-turn aggregate (see below).

Measured on one real turn with `claude-haiku` (Claude Code 2.1.317), per harness step:

| Step | Cached input | New cache write | Hit |
| --- | ---: | ---: | ---: |
| 1 (first call of the prefix) | 0 | 24,401 | 0% |
| 2 | 24,401 | 952 | 96.2% |
| 3 | 25,353 | 1,422 | 94.7% |
| 4 (after a 69k-token thinking block) | 24,401 | 71,814 | 25.4% |
| 5 | 96,215 | 23,337 | 80.5% |
| 6 | 119,552 | 2,260 | 98.1% |
| 7 | 121,812 | 683 | 99.4% |
| 8 | 122,495 | 656 | 99.5% |
| 9 | 123,151 | 1,011 | 99.2% |
| 10 | 124,162 | 198 | 99.8% |
| 11 | 124,360 | 1,312 | 99.0% |

Across the complete 28-step turn on that session, the real totals are **3,348,680 cached input**, 161,101 cache writes and 110 uncached input — **95.4% overall**, and 97–99.8% from step 6 onwards. The session log recorded 6,539,797 cached input for the same turn because the last step carried the whole-turn aggregate; that is exactly the inflation the second fix removes.

Two details matter:

1. **The first call of a new prefix always writes it.** Starting a session, or switching a large conversation to Claude Agent, pays one full cache write. After that, the same prefix is read.
2. **A new reasoning block is new prefix.** Extended thinking that is sent back with a tool call has to be cached on the next call, which is the 25% step above. Native Claude Code behaves the same way; it is not a plugin restart.

Two bugs were found and fixed while measuring this, and the fixes are in this repository:

- The adapter used to omit `totalTokens`. DSH's turn panel computes cache hit as `cacheRead / (totalTokens - outputTokens)`, so the panel showed a broken or very low percentage even when the real hit was 99%. The snapshot now reports `totalTokens = input + cacheRead + cacheWrite + output`.
- The adapter used to apply the SDK's `SDKResultMessage.usage` on top of the per-message usage. That field is the **whole Claude turn's aggregate**, so a multi-step turn reported its cache reads twice. The result usage is now a fallback only when no per-message usage arrived.

## How it works

```
DeepSeek Harness ──MCP tools──►  `claude` (your login)  ──►  Anthropic
       history, UI                  official Agent SDK
```

- **Tools**: the harness's tool schemas become an MCP server named `harness`. A `PreToolUse` hook carries the `tool_use` id (with the MCP `_meta` id as a fallback), the adapter emits a normal `tool-call` chunk, the harness executes the tool, and the result is fed back into the parked process.
- **History**: the harness session is the source of truth. The Claude transcript is resumed by id; what Claude missed is sent as a checkpoint. Assistant replies are persisted by the harness like any other model's.
- **Lifecycle**: one process per session, stopped after `idleMinutes` of inactivity, with a separate `parkedMinutes` window while a tool round waits. Cancellation interrupts the child and keeps what Claude already wrote.
- **Models**: `initializationResult().models` provides the catalog, aliases, context windows and effort levels; it is cached in `$DSH_HOME/state/claude-agent/models.json` so the picker works before a process starts.

## Limitations

- No `forkSession` on an edited history: the plugin starts a new Claude transcript and sends a checkpoint. Correct, but it loses the cached prefix.
- Titles and compaction run in an ephemeral process without tools, instead of a cached branch of the conversation.
- `cwd` is a provider setting; DSH does not pass the session directory in `GenerateOptions`.
- PDFs are not sent as documents: DSH file attachments arrive as text handles, like every other provider.
- The whole DSH system prompt is appended to Claude Code's prompt, so its date/environment section may appear twice.
- The plugin follows Anthropic's policies as published at the time of writing (November 2026). Policies can change; check [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance.md) before relying on a subscription-based workflow.

## Verification

With Claude Code 2.1.317 and a subscription login:

- the SDK starts, reports the account and 12 models;
- a prompt returns the expected answer;
- a `bash` tool call produces `tool_call` → `tool_result` → a second model call → the final answer;
- a second DSH process on the same session resumes Claude's transcript (`41` → `42`) with a high cache-read count;
- the desktop Host reloads the bundle and rewrites the model catalog, proving the SDK runs inside the app.

The repository contains no credentials and no machine-specific state. The stores live under `$DSH_HOME/state/claude-agent/` at runtime and are not committed.

## License

MIT. Anthropic's Claude Agent SDK is a dependency under its own license.

## Documentation

- [docs/opencode-approach.md](docs/opencode-approach.md) — how opencode's provider works, with source references, and how this plugin maps onto it.
- [docs/opencode-analysis.es.md](docs/opencode-analysis.es.md) — the same analysis in Spanish.
- [docs/HANDOFF.md](docs/HANDOFF.md) — maintenance handoff: architecture, measured cache results, open work and release checklist.
