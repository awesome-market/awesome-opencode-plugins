# opencode-goal

Persistent `/goal` mode for [OpenCode](https://opencode.ai) v2. Set an objective once and the session keeps working toward it across turns: when a turn ends successfully and the goal is still active, the plugin sends a continuation prompt, until the model proves the goal complete, hits a token budget, gets blocked, or you pause it.

This is a port of the `/goal` mode from [OpenAI Codex](https://github.com/openai/codex) (`codex-rs/ext/goal`). The continuation, budget-limit and objective-updated prompts and the tool descriptions are adapted from Codex under the Apache License 2.0 (see `NOTICE`).

Tested with OpenCode 2.0.30 (`@opencode/plugin` 2.0.30).

## Features

- `/goal <objective>` with an optional token budget (`--tokens 250K`, `--tokens 1.5M`).
- Automatic continuation after every successful turn, with a completion audit and a blocked audit baked into the prompts.
- Token accounting (input plus output tokens per step) and wall-clock time while the goal is active. When the budget is used up the goal becomes `budget_limited`, the model is told to wrap up once, and continuation stops.
- Model tools `get_goal`, `create_goal` and `update_goal`. The model can only mark a goal `complete`, `blocked` or `paused`; it can never re-activate a goal or clear a budget limit.
- Safety guards: subagent sessions never continue, failed turns do not continue, a user interrupt pauses the goal, duplicate idle events produce one continuation, and a hard cap (`maxContinuations`, default 200) pauses the goal and tells you.
- The goal survives context compaction: its objective and status are added to the system prompt of every request.
- State is stored per session through the plugin storage API, so it survives server restarts.
- A bundled skill (`goal`) that teaches the model how to behave under a goal.

## Install

```sh
opencode plugin add github:KelpHect/opencode-goal
```

Or pin a release:

```sh
opencode plugin add github:KelpHect/opencode-goal#v0.2.1
```

Manual configuration in `opencode.json`:

```jsonc
{
  "plugins": [
    "github:KelpHect/opencode-goal#v0.2.1",
    // or with options:
    // { "package": "github:KelpHect/opencode-goal#v0.2.1", "options": { "maxContinuations": 100 } }
  ]
}
```

Restart the OpenCode service (`opencode service restart`) after changing plugins.

## Usage

| Command | Effect |
| --- | --- |
| `/goal <objective>` | Set (or replace) the goal and start working on it. |
| `/goal --tokens 250K <objective>` | Same, with a token budget. `K` and `M` suffixes are accepted. |
| `/goal` or `/goal status` | Show objective, status, tokens used, time and continuation count. |
| `/goal pause` | Stop continuing. |
| `/goal resume` | Resume (resets the continuation counter) and kick off the next turn. |
| `/goal clear` | Delete the goal. |

Objectives are limited to 4000 characters.

### Model tools

| Tool | Purpose |
| --- | --- |
| `get_goal` | Current goal, status, usage and remaining tokens. |
| `create_goal {objective, token_budget?}` | Only when the user explicitly asks the agent to set a goal. Fails if an unfinished goal exists. |
| `update_goal {status}` | `complete`, `blocked` or `paused` only. Returns the final usage report on completion. |

## Configuration

| Option | Default | Description |
| --- | --- | --- |
| `maxContinuations` | `200` | Automatic continuations before the goal is paused. |
| `debugLogFile` | none | Append plugin diagnostics and session events to this file. |

## The bundled skill

Plugins provide tools; they cannot tell the model when to use them. The bundled `goal` skill (`skills/goal/SKILL.md`) is registered automatically and teaches the model the working rules: make real progress each turn, keep the full objective, complete only after an evidence-based audit, use `blocked` only after the same blocker repeats for three turns, and pause only when the user asks.

## How it works

- The `/goal` command, tools, context hook and event subscription are all registered through the OpenCode v2 plugin API.
- Continuation is triggered by `session.execution.succeeded` (the `session.idle` event is not delivered to plugin event streams in 2.0.30). The plugin only continues if a new turn started since its last prompt, which deduplicates events.
- Tokens are summed from `session.step.ended` events while the goal is active.

## Limitations and known issues

- `opencode run "/goal ..."` does not execute plugin commands (the text is sent to the model as a plain prompt). Use the TUI, or `session.command` through the API.
- `/goal status` and the pause/clear notices are delivered as a synthetic message that costs one short model turn.
- Tokens used by the step that calls `update_goal complete` are not counted.
- Plugins are instantiated once per project location; state is shared through storage, so this is invisible in practice.

## Development

```sh
bun install
bun test
bunx tsc --noEmit
```

## License and credits

Apache License 2.0, see `LICENSE`. Copyright (c) 2026 KelpHect. Prompts and tool descriptions are adapted from OpenAI Codex (Apache-2.0), see `NOTICE`.
