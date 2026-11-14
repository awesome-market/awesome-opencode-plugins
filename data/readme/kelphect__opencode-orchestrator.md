# opencode-orchestrator

An [OpenCode v2](https://opencode.ai) plugin that teaches the primary agent to orchestrate subagents well. Plugins only add tools; whether the model uses them correctly comes down to instructions. This plugin supplies the missing half:

- an **`orchestrator` skill** — a cost-aware routing playbook: which agent tier to use for each kind of task, prompt templates per tier, parallelism limits, how to verify subagent reports, and when to escalate to a stronger model;
- **always-on routing instructions** injected into every primary session, and a separate **subagent conduct** text injected into every child session;
- **example agent definitions** (`examples/opencode.jsonc`) defining the six tiers the playbook routes to: `quick`, `explore`, `general`, `worker`, `video`, `hard`.

Tested with OpenCode 2.0.30.

## Install

```sh
opencode plugin add github:KelpHect/opencode-orchestrator
```

Or pin a release:

```sh
opencode plugin add github:KelpHect/opencode-orchestrator#v0.1.1
```

## Define the agents

The playbook routes by agent name. Copy `examples/opencode.jsonc` into your `opencode.json` `agents` section and fill in a model per tier — for example a free small model for `quick`, a cheap large-context model for `explore`/`general`/`worker`, a vision-capable model for `video`, and a frontier model for `hard`.

If your setup uses different agent names, the skill maps tiers by role — edit `AGENTS.md` (see `instructionsFile` below) or the skill text to match your names.

## Options

Pass options through the plugin config object:

```jsonc
{
  "plugins": [
    {
      "package": "github:KelpHect/opencode-orchestrator",
      "options": {
        "injectInstructions": true,          // routing rules into primary sessions
        "injectSubagentInstructions": true,  // conduct rules into child sessions
        "instructionsFile": "/path/to/AGENTS.md" // replace the bundled instructions
      }
    }
  ]
}
```

| Option | Default | Effect |
| --- | --- | --- |
| `injectInstructions` | `true` | Inject the routing summary into primary-session system prompts. Set `false` if you keep your own orchestration rules in a global `AGENTS.md` to avoid duplication. |
| `injectSubagentInstructions` | `true` | Inject the subagent conduct rules into child sessions (scope discipline, staging etiquette, report format). |
| `instructionsFile` | bundled `AGENTS.md` | Load instructions from your own file instead. The file is split at its `# Subagents` heading: everything before goes to primary sessions, that section goes to children. |
| `debugLogFile` | — | Append a JSON line per context hook with what was injected (for development). |

## How it works

- `ctx.skill.transform` registers the bundled `orchestrator` skill, so it appears in the skill list like any local skill and the model loads it on demand.
- `ctx.session.hook("context")` appends a text system part once per request. Sessions with a `parentID` are treated as subagents and get the subagent text; everything else gets the routing summary.
- Nothing is injected twice in one request, and sessions are classified once (cached per session ID).

## Pairs well with

- [opencode-worktrees](https://github.com/KelpHect/opencode-worktrees) — gives `worker`-style agents each an isolated git worktree (its `worktree-isolation` skill is referenced by the playbook).
- [opencode-vision](https://github.com/KelpHect/opencode-vision) — screen capture and video-analysis tools for a `video`-tier agent (`video-analysis` skill).
- [opencode-goal](https://github.com/KelpHect/opencode-goal) — persistent `/goal` mode for long multi-turn objectives.

## Notes

- The injected instructions and skill deliberately avoid recommending any provider or model; the tier names are the contract. The example config lists one possible set of models.
- Routing and delegation guidance was informed by public descriptions of Claude Code's and Codex's subagent workflows; no text is copied from them.
- If you already maintain a global `AGENTS.md` with orchestration rules, either disable `injectInstructions` or point `instructionsFile` at your file — running both duplicates the guidance.

## Development

```sh
bun install
bun test        # unit tests
bunx tsc --noEmit   # typecheck
```

## License

MIT — see [LICENSE](LICENSE).
