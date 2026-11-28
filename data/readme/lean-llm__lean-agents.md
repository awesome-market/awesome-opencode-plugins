# Lean Agents

Short prompts for coding agents. Less text per turn, one clear rule set.

See `BENCHMARK.md` for the tests so far.

## How it works

`AGENTS.md` is the one shared policy. Two roles:

| Role | Who | Does |
| --- | --- | --- |
| `ORCHESTRATOR` | Primary agent (`build`) | Small single fixes itself. Features, refactors and multi-file work go to a worker, one per independent task. |
| `CODER` | Worker (`general`, or `worker` on Codex) | Investigates, edits, tests, repairs inside its scope. Never delegates. |

Up to 10 workers run in parallel on independent tasks; the primary waits for all. Agents never ask the user questions; they resolve things themselves. Delete the `## Questions` section in `AGENTS.md` if you want questions back.

## What's inside

| Path | What |
| --- | --- |
| `AGENTS.md` | Shared policy: roles, routing, engineering, output. |
| `agents/` | Agent files: `build.md` (primary), `general.md` / `worker.toml` (CODER), plus optional `lean-*` and `explore` helpers. |
| `skills/lean-code` | Smallest complete change, lean pass after coding, dedup. Load for all coding. |
| `skills/lean-java` | Java/JVM: Maven, Gradle, JUnit, concurrency, Spring. |
| `skills/lean-web` | JS/TS, Node, React/Next.js, Fastify, auth, tests. |
| `skills/lean-plan` | Plan a feature from scratch. |
| `extensions/` | Pi: `subagent` tool for `general`. |
| `mods/` | Command Code: loads the `build` prompt. |
| `plugins/` | Legacy OpenCode no-op, kept so old installs get overwritten. |
| `.chatgpt/` | Prompt for ChatGPT projects that write plans for coding agents. |

Agents load the skills that fit the task and workspace.

## Install

Put `AGENTS.md` at the repo root (or the host's global instructions path). Start a fresh session and check it loaded. Merge with existing config; don't overwrite.

- **OpenCode:** copy `agents/build.md` and `agents/general.md` to `.opencode/agents/` or `~/.config/opencode/agents/`. Set `default_agent: "build"`.
- **Claude Code:** copy the same two files to `.claude/agents/` or `~/.claude/agents/`. Run `claude --agent build`. Add `@AGENTS.md` to `CLAUDE.md` if needed.
- **Codex:** copy `agents/worker.toml` to `.codex/agents/`. Turn on multi-agent. Root `AGENTS.md` makes Codex the orchestrator.
- **Command Code:** reads `AGENTS.md`. Optional: install `mods/lean-primary.ts` (keep `agents/build.md` beside it). Its built-in `general` can't be overridden, so give `Role: CODER` in the handoff.
- **Pi:** use `extensions/lean-subagents.ts` (keep `agents/general.md` beside it). Load `AGENTS.md` yourself if the host doesn't.

## Limits

Prompts are not enforcement. The model may skip delegation. Check the first tool calls of a fresh session.

## License

MIT. See `LICENSE`.
