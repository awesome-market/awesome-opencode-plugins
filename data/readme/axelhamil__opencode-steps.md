# opencode-steps

Deterministic agent workflows for [OpenCode](https://opencode.ai) V2. You write the steps in a small file, as a tree read top to bottom. Code decides what runs next, from each step's result. No model chooses the order, so no step gets skipped.

Work in progress: built and tested against OpenCode 2.3.0. The plugin API it uses is young and may change without notice.

## Why

A skill or an orchestrator agent describes a process in prose, and the model decides how closely to follow it. Here the process is a state machine:

- a step hands over only when its exit condition is true, checked by code;
- a `loop` block restarts its steps until they pass, up to a cap;
- an agent that returns nothing (crash, limit, timeout, no verdict) blocks the run. It never counts as a success or as a normal failure;
- agents cannot commit, push or ask for permissions.

## Install

Add the plugin to your OpenCode config (`~/.config/opencode/opencode.json`):

```jsonc
{
  "plugins": ["opencode-steps@git+https://github.com/axelhamil/opencode-steps.git"]
}
```

Then put each workflow in its own folder of `~/.config/opencode/workflows/`: `<name>/<name>.ts`, with the agents it needs in `<name>/agents/`. Each workflow becomes a slash command named after it.

The plugin also brings a skill, `writing-workflows`, so an agent can write the workflow with you, and shows the current run in the status line and the sidebar of the terminal UI.

Documentation: [getting started](docs/getting-started.md), [writing workflows](docs/writing-workflows.md), [reference](docs/reference.md), [how it works](docs/how-it-works.md).

## A workflow

```ts
// ~/.config/opencode/workflows/review-loop/review-loop.ts
import type { Kit } from "opencode-steps/kit"

export default ({ workflow, agent, check, parallel, loop }: Kit) =>
  workflow("review-loop", [
    loop({ max: 2 }, [
      agent("write", {
        agent: "build",
        prompt: "Implement the ticket in the work directory, with its tests.",
      }),
      check("checks", { commands: ["npm test"] }),
      parallel("review", {
        agents: [
          { agent: "build", name: "correctness", prompt: "Review the uncommitted changes against the ticket." },
          { agent: "build", name: "simplicity", prompt: "Review the uncommitted changes for code the ticket does not need." },
        ],
      }),
    ]),
  ])
```

Read it top to bottom: `write`, then `checks`, then `review`. When `checks` or `review` fails, the `loop` restarts from `write` with the failure as feedback, twice at most; a third failure blocks the run.

Run it from any session with `/review-loop <ticket>`. That session becomes the main session of the run: progress, blocks and requests for your approval arrive there, and you pilot the run from it.

The file's default export is a function that receives the kit (`workflow`, the five step builders, the `each` and `loop` blocks, and `z` from Zod), so it needs no install of its own. The file runs on Bun, the runtime OpenCode runs plugins on, so Bun's APIs (`Bun.file`, `Bun.$`, `import.meta.dir`) are available. The `import type` line is optional and only gives you types and inline documentation; with `@types/bun` and `"types": ["bun"]` your editor also knows Bun's APIs. To have them in your editor, see [Types in your editor](docs/writing-workflows.md#types-in-your-editor).

## The five steps

| Step | What it does | How it ends |
|---|---|---|
| `talk(name, options)` | The main session discusses with you. It may only write the file named by `writes`, inside the run directory. | The main session submits its verdict when you both agree. |
| `agent(name, options)` | One agent in its own session. | The agent submits `done` or `blocked`, with `data` if the step has an `output` schema. |
| `parallel(name, options)` | Several agents at the same time, read-only. | Each submits `approved`, `needs_fixes` (with findings) or `blocked`. All approved: the run moves on. Any findings: the step fails. |
| `check(name, options)` | Shell commands run by code, in order. | Exit codes. A failing command fails the step, with its output as the failure. |
| `code(name, options)` | A function, no model. Built-ins: `isolate`, `setup`, `push`, `cleanup`. | The function's result. |

## The two blocks

| Block | What it does |
|---|---|
| `each(key, { commit }, steps)` | Runs `steps` once per item of the list `data[key]`, in order. Every step of the block receives the item. With `commit: "field"`, the work tree is committed after each item with the item's `field` as subject. An empty or missing list blocks the run. `{ commit }` can be left out. |
| `loop({ max, repair }, steps)` | Runs `steps`. When one of them fails, `repair` (one `agent` step) runs with the failure, then `steps` restart from the first one; without `repair`, they restart with the failure as feedback. After `max` restarts, the next failure blocks the run. `max` is required. A restart runs everything again: an `each` inside starts again at its first item. |

Only `check` and `parallel` steps fail. A failure restarts the closest enclosing `loop`; outside any `loop`, it blocks the run. Blocks nest freely. No step names another step: the indentation is the control flow.

### Options

| Option | On | Meaning |
|---|---|---|
| `approve: "label"` | every step | After the step succeeds, the run waits for you with `waiting for you to approve the <label>`: `/workflow approve`, `/workflow revise <remarks>` (same step again, with your remarks) or `/workflow back` (closest `talk` step written before, or the same step when there is none). |
| `deny: [{ action, resource }]` | `agent`, `parallel` | Extra permission rules denied to the step's agents. |
| `timeoutMs` | `agent`, `parallel`, `check` | Maximum duration of one agent session of the step, or of each command of a `check`. Past it, the run is blocked. |

| Step | Its own options |
|---|---|
| `talk` | `skills`, `writes`, `prompt` |
| `agent` | `agent` (required), `model`, `skills`, `prompt`, `writes` (a file of the run directory it may write), `output` (Zod schema of the result) |
| `parallel` | `agents` (names, or `{ agent, model, name, prompt, when, skills }`), `model`, `skills`, `prompt` |
| `check` | `commands` (defaults to the `checks` list of the run data) |
| `code` | `run` (your function; without it the step name must be a built-in) |

An option a step or a block does not have is refused when the workflow loads, such as `writes` on a `check`, `max` on an `each` or `commit` on a `loop`.

`model` is written `provider/model` or `provider/model#variant`, for example `"claude-agent/sonnet"`. It replaces the model of the agent's definition for that step, or for one agent of a `parallel` step. Without it, each agent keeps its own model.

`prompt` is a string or a function of `{ ticket, runDir, worktree, data, item, feedback }`.

`skills` lists skill ids. The plugin attaches them to the first prompt of the session, after the skills of the agent's definition, and checks in the message OpenCode stored that each one arrived with its content. A skill that is missing blocks the run, and the reason names it. The agent has nothing to load.

### Agents of a workflow

A workflow folder may carry its own agents, one file per agent in `agents/`. The file name is the agent's name. The plugin registers them in OpenCode. Give it a name no other agent has. When a built-in agent or an agent of your configuration has the same name, yours is the one that runs (OpenCode applies a configuration agent on top of the workflow's), the skills of the workflow's file are not attached, and `/workflow status` reports it.

```md
<!-- ~/.config/opencode/workflows/deliver/agents/planner-writer.md -->
---
description: Writes the implementation plan of a ticket
model: claude-agent/opus
skills: [writing-plans]
---
You write the plan of the ticket you are given, task by task.
```

Frontmatter: `description` (required), `model`, `mode` (`subagent` by default, `primary`, `all`), `hidden`, `skills`, `permissions` (list of `{ action, resource, effect }`). An unknown key is reported. The body is the agent's system prompt.

### From the earlier layout

Move `workflows/x.ts` to `workflows/x/x.ts`, and write `skill: "a"` as `skills: ["a"]`. A file left at the top of the workflows directory is not loaded; `/workflow status` lists it.

`onFail`, `max` and `then` on a step, and `each` on a step, were replaced by blocks. A workflow that still uses them is refused with the block to write; the table in [writing workflows](docs/writing-workflows.md#from-onfail-then-and-each) shows each rewrite. A run started by an older version cannot be resumed: `/workflow abort`, then start it again.

### Run data

The `data` an agent submits, and the object a `code` step returns, are merged into the run data. Later steps read it: `each("tasks", ...)` iterates `data.tasks`, `check` reads `data.checks`, `when: "sql"` runs a reviewer only if `data.sql` is truthy.

### Built-in code steps

| Name | What it does |
|---|---|
| `isolate` | Creates a branch and a git worktree for the run. Later steps work there. |
| `setup` | Runs the `setup` commands of the run data in the worktree. |
| `push` | Folds leftover changes into the last commit, checks signatures when signing is on, renames the branch to `data.branch` if set, pushes to `origin` and writes `pr.md` in the run directory. Needs `isolate` before it. |
| `cleanup` | Removes the worktree. The branch stays. |

## Piloting a run

Everything happens in the main session.

| Command | Effect |
|---|---|
| `/workflow status` | The workflow as a tree with the current step marked, the item and restart counters, the block reason, the run directory. |
| `/workflow approve`, `revise <remarks>`, `back [remarks]` | Answer a request for approval. |
| `/workflow pause` | Finish the current unit, then stop. |
| `/workflow resume` | Continue a paused, blocked or interrupted run. Finished steps are not replayed, and the restart counter of the loop the run was blocked in starts again from zero. |
| `/workflow abort` | Interrupt the agents and stop. The worktree and the state are kept. |
| `/workflow reload` | Reload the workflow folders and their agents. |

A blocked run tells you why and where to look. Fix the cause by hand, then `/workflow resume`. There is no way to force a step through.

While a run is running, talking or waiting for your approval, the main session cannot edit files (except the file a `talk` step names) nor commit. It is free again when the run is blocked, paused or over.

## What the plugin enforces

- **Order**: only the engine picks the next step.
- **Verdicts**: agents answer through the `workflow_submit` tool. A session that ends without calling it gets one reminder, then the run is blocked.
- **No commit by agents**: `git commit`, `git push` and `gh` are refused. After each agent, code checks that HEAD did not move. Reviewers must leave the work tree untouched.
- **Writes**: an agent can only edit inside the work directory, plus the one file of the run directory its step names with `writes`. Reviewers cannot edit at all. Step agents cannot launch subagents.
- **No permission prompt**: in a step's session, a permission that would be asked is denied.
- **State on disk**: each run has a directory with `state.json`, `events.ndjson` (every transition and every refused tool call), `reports/` and a final `report.md`.

Limits to know: the shell lock matches the command text, so a command that hides `git commit` behind a script is only caught by the HEAD check afterwards. Shell commands can still write files outside the work directory.

## Plugin options

```jsonc
{
  "plugins": [
    {
      "package": "opencode-steps@git+https://github.com/axelhamil/opencode-steps.git",
      "options": { "runsDir": "~/.opencode/plan", "agentTimeoutMinutes": 45 }
    }
  ]
}
```

| Option | Default |
|---|---|
| `workflowsDir` | `~/.config/opencode/workflows` |
| `runsDir` | `~/.opencode/plan` (a run lives in `<runsDir>/<project>/<run>/`) |
| `agentTimeoutMinutes` | 45 |
| `checkTimeoutMinutes` | 15 |
| `nudgeTimeoutMinutes` | 5 |
| `autoUpdate` | `true` |

## Updates

Installed this way, the plugin follows the `main` branch, which only moves when a version is released.

OpenCode checks for a newer version when its server starts, but does not install it. The plugin does: when the terminal UI opens and a newer version exists, it asks OpenCode to install it, unless a run is at work, in which case it waits for the run to stop. It makes no network request of its own: the check and the install are OpenCode's. An install that fails is not tried again from the same version; you are told instead.

| You want | Do |
|---|---|
| To be told only | Set the option `autoUpdate` to `false`. When you choose, run `opencode plugin update` followed by the package string of your config; without it, every outdated plugin is updated |
| A fixed version | Install a release tag, for example `...opencode-steps.git#v0.1.0`. A release tag never moves, so nothing is installed after it |
| A version that can never change | Install a full commit hash: OpenCode never checks it |

## Development

```sh
pnpm install
bun run hooks   # once: installs the git hooks (commitlint, checks before push)
bun run check   # biome, tsc, bun test, knip
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md).

## License

[MIT](LICENSE)
