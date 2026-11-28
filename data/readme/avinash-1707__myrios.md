<p align="center">
  <img src="https://res.cloudinary.com/dqvjmhrh8/image/upload/v1783417716/IMG_20260707_151704_fjyxpk.png" alt="Myrios: countless agents, one orchestrator" width="100%" />
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/oc-myrios"><img src="https://img.shields.io/npm/v/oc-myrios?color=8b5cf6&label=npm" alt="npm version" /></a>
  <img src="https://img.shields.io/badge/runtime-bun-f9f1e1" alt="bun" />
  <img src="https://img.shields.io/badge/for-OpenCode-0a0a12" alt="OpenCode" />
</p>

Myrios is an <a href="https://opencode.ai">OpenCode</a> plugin that turns the primary agent into an orchestrator. It adds a crew of five specialized subagents, parallel background tasks, auto-loaded MCPs, bundled skills, and living project documentation. One install, zero config.

## Install

```bash
bunx oc-myrios install
```

The installer adds `oc-myrios` to your `opencode.json` plugins, walks you through MCP selection, and installs the bundled skills.

Prefer manual? Add the plugin yourself:

```jsonc
// opencode.json
{
  "plugin": ["oc-myrios"]
}
```

Restart OpenCode. Agents, tools, MCPs, and skills are live. No configuration required.

## The Crew

Five subagents, registered automatically. Build and Plan agents get a delegation prompt injected, so they know when and how to use each one without being told.

| Agent | Role | Default model | Execution | Can write? |
|-------|------|---------------|-----------|------------|
| **scout** | Find code. Contextual grep for the codebase | Haiku 4.5 | background | no |
| **atlas** | Research the world. Docs, GitHub, OSS, with cited permalinks | Sonnet 5 | background | no |
| **sage** | Think deeply. Architecture, debugging strategy, code review | Opus 5 | sync | no |
| **canvas** | Build interfaces. A designer-turned-developer with write access | Sonnet 5 | sync | files + shell |
| **verifier** | Say no. Runs tests, build, and lint, then reports PASS or FAIL against a Definition-of-Done | Sonnet 5 | sync | shell only |

A sixth, **forge**, appears only when `wave.enabled` is on — see [Parallel Waves](#parallel-waves).

The mental model: scout and atlas work like grep commands. Fire them in the background and keep working. Sage answers before you proceed. Canvas implements. Verifier decides whether you are actually done.

The verifier closes the loop. Implementations get checked against an explicit "Done when:" line, failures route back to a fix, and an unchanged failure signature escalates to sage instead of retrying blindly.

### Why the tool lists deny things explicitly

OpenCode's agent `tools` record is **default-allow** — a tool left out of it stays reachable. So "read-only" has to be spelled out: omitting `bash` from a research agent leaves it a shell, and a shell can write files.

Every non-writing agent therefore spreads a shared `READ_ONLY_TOOLS` policy that denies `write`, `edit`, `patch`, `bash`, and `task` by name (`src/agents/tool-policy.ts`). Verifier re-enables `bash` after the spread because running your checks is its whole purpose. Canvas states `write`, `edit`, and `bash` deliberately.

One subtlety worth knowing before editing these: `write`, `edit`, and `patch` all collapse onto a single permission key, applied in key order. A `patch: false` placed after a `write: true` silently denies editing — which is why canvas does not spread the policy. `test/agent-tool-policy.test.ts` locks all of this down.

## Background Tasks

Fire-and-forget parallel agents:

```
background_task(agent="scout", description="Find auth code", prompt="...")
background_task(agent="atlas", description="JWT best practices", prompt="...")
// keep working. You are notified when all complete.
background_output(task_id="bg_abc123")
```

- Toast notifications on launch, completion, and failure
- Completion notifications are scoped to the launching session, so there is no cross-session bleed
- Concurrency cap (default 6 running) plus a per-session circuit breaker (default 50) so a runaway loop cannot burn your usage
- Hung tasks are aborted after a timeout (default 30 min) and reported as failed, so a stuck agent cannot hold a slot forever
- `background_list` shows this session's tasks and statuses, with per-task usage and a session token/cost total; `background_output` includes a usage footer
- Deleting a session aborts its still-running background tasks

## Keyword Triggers

Type these anywhere in a prompt to unlock modes:

| Keyword | Effect |
|---------|--------|
| `ultrawork` / `ulw` | Maximum multi-agent coordination with aggressive parallel research |
| `autoplan` | Staged pre-build pipeline (problem framing, architecture, design) that locks a plan with a machine-checkable "Done when:" before any code |
| `deep research` | Comprehensive exploration. Fires 3 to 5 background agents |
| `explore codebase` | Codebase mapping with parallel scouts |
| `review` / `self-review` / `code review` | Sage code-review mode: one task, full diff, severity-ranked findings |
| `parallel mode` / `fan out` | Single-writer waves. Only registered when `wave.enabled` is on — see [Parallel Waves](#parallel-waves) |

## Todo Pipelining

Working a todo list serially wastes time re-deriving context at every step, so the delegation prompt tells the agent to overlap the read-only parts:

- **On a fresh plan**, fire scouts for the next one or two todos to get a **file manifest**: the paths that todo touches and the conventions already in use there.
- **On the last todo**, start `verifier` and the Sage review early so they run while you finish rather than queueing behind it.

This is guidance in the system prompt, not automation. An earlier version of this hooked the `todo.updated` event and injected the advice mid-run; that was removed in 0.2.1 because injecting a message into a busy session displaces the agent's own todo updates. See the note in [Parallel Waves](#parallel-waves) about why only the parent writes.

## Parallel Waves

Opt-in (`"wave": { "enabled": true }`) **and** gated on the `parallel mode` keyword. Off by default.

Real parallel implementation without the usual danger: **workers never touch your working tree**. A `forge` worker is read-only and returns the complete new contents of the files it owns; the parent applies them. One writer means workers cannot clobber each other, a bad payload is rejected instead of discovered as a half-edit, and changes land in order so a broken build stays attributable.

| Tool | What it does |
|------|--------------|
| `wave_apply` | The only path from a wave to disk. Reads each worker's payload straight from its session, so contents never enter the parent's context |
| `wave_rollback` | Restores every file the wave wrote and deletes the ones it created |

`wave_apply` refuses to write when a path is claimed by two workers, when a worker never signalled completion, when a worker reported blocked, or when a path is unsafe. Payloads are untrusted model output, so writes pass four independent layers:

- **Lexical** — no absolute paths, no `..`, not the project root itself.
- **Policy** — a deny-list covering `.git`, `.opencode`, `.myrios`, `.github`, `.husky`, `node_modules`, plus `opencode.json`, `package.json`, lockfiles, `.env*`, and key/cert files. Without it, a read-only worker could rewrite agent config and gain a shell on the next turn.
- **On-disk** — `realpath` containment plus `O_NOFOLLOW`, because path checks are lexical and any symlink in the repo would otherwise defeat them.
- **Content** — rejects elision markers like `// ... rest unchanged`, overwrites that shrink a substantial file by more than half or empty it, and overwrites of non-UTF-8 files.

Backups are written and flushed **before** any file changes, so an interrupt mid-wave still leaves a complete rollback record. Files you edit *after* a wave are skipped by rollback unless you force it.

Fan out only for 3+ substantial todos whose file sets you have actually verified to be disjoint. A wave multiplies token spend by the number of workers and failed waves still bill; if one lands badly you have to read several diffs you did not write, which usually costs more than writing them serially would have.

## Tools

| Tool | What it does |
|------|--------------|
| `background_task` / `background_output` / `background_list` / `background_cancel` | Parallel agent execution |
| `session_list` / `session_search` | Learn from past sessions ("how did we do this last time?") |
| `find_symbols` / `lsp_status` | LSP-backed symbol search and language-server health |
| `save_project_guideline` | Living documentation. Writes lasting decisions to AGENTS.md / CLAUDE.md with dedup and date stamps |
| `memory_save` / `memory_recall` / `memory_forget` | Project memory, see below |
| `wave_apply` / `wave_rollback` | Land or undo a parallel wave. Only when `wave.enabled` is on |

## Project Memory

Sessions start amnesiac. Memory fixes that. A per-project store at `.myrios/memory/` holds typed entries:

- **convention**: durable decisions ("use bun test, not vitest")
- **mistake**: errors made and how to avoid repeating them
- **state**: where work left off (open issue, blocker, next step). Overwritten per workstream, never accumulates

Token-friendly by design. Only a generated `INDEX.md` (one line per entry, capped at 30 lines) is injected into primary agents' system prompts. Full entry bodies are fetched on demand with `memory_recall` (keyword-scored, top 3). Bodies are soft-capped at 150 words, and `memory_save` rejects near-duplicates (65%+ keyword overlap) by pointing at the existing entry instead.

The store self-ignores via `.myrios/memory/.gitignore`. Set `memory.git_track: true` to share it with your team through git.

## MCPs

Auto-loaded, free, no API keys. Your existing MCPs are preserved, and any of these can be disabled via config.

- **exa**: web search, code context, URL crawling
- **grep_app**: instant code search across millions of GitHub repos
- **firecrawl**: developer-index search over docs, issues, PRs, and READMEs
- **sequential-thinking**: structured multi-step reasoning

## Skills

Bundled skills install into `~/.config/opencode/skills/` and stay in sync with the plugin version. Myrios never touches a skill you created or edited yourself. Ownership is tracked per skill via a manifest.

| Skill | Purpose |
|-------|---------|
| `frontend-design` | Baseline for any UI work. Avoids generic "AI slop" aesthetics |
| `grill-me` | Stress-test a plan before committing to it |
| `design-motion-principles` | Motion and animation guidance (repo installs only, not shipped on npm pending upstream license) |

## Also Included

- **Todo enforcer**: a session going idle with incomplete todos gets nudged to continue (10s cooldown, skips plan mode)
- **Auto-update**: startup version toast, npm check, and cache invalidation so the next restart picks up new versions
- **Orchestration prompt**: build and plan agents learn the delegation rules, verification protocol, and self-review protocol automatically

## Configuration

Entirely optional. Create `~/.config/opencode/myrios.json` (user-level) or `<project>/.opencode/myrios.json` (project-level). Project values win, and disabled lists merge across both.

```jsonc
{
  "$schema": "https://unpkg.com/oc-myrios/schema.json",

  // per-agent overrides
  "agents": {
    "sage": { "model": "openai/gpt-5.5", "variant": "high" },
    "scout": { "model": "anthropic/claude-haiku-4-5" }
  },

  // turn things off
  "disabled_agents": ["canvas"],
  "disabled_mcps": ["exa"],
  "disabled_skills": ["grill-me"],

  // background task limits
  "background": {
    "max_concurrent": 4,     // max simultaneously running tasks (default 6)
    "max_per_session": 30,   // lifetime spawn cap per session (default 50)
    "timeout_minutes": 30    // hung tasks are aborted after this (default 30)
  },

  // which primary agents get the delegation prompt (default: build + plan)
  "orchestration": { "agents": ["build", "plan", "my-custom-agent"] },

  // project memory (.myrios/memory/)
  "memory": {
    "enabled": true,         // memory tools + index injection (default true)
    "max_index_lines": 30,   // index lines injected into the system prompt
    "body_max_words": 150,   // soft cap per entry body (longer saves warn)
    "git_track": false       // true = share the store via git (skips self-gitignore)
  },

  // single-writer parallel waves (opt-in; also needs the "parallel mode" keyword)
  "wave": { "enabled": false },

  "todo_enforcer": { "enabled": true },
  "auto_update": { "show_startup_toast": true }
}
```

Every field is optional. Invalid config is ignored with a warning and never breaks startup.

Config is read once at plugin startup, so restart OpenCode after editing `myrios.json`. Background task state is in-memory: reloading the plugin forgets running tasks (their sessions finish on their own, but results must be fetched from session history).

## CLI

```bash
bunx oc-myrios install       # add to opencode.json, pick MCPs, install skills
bunx oc-myrios mcp           # enable/disable MCP servers interactively
bunx oc-myrios skills        # install/update bundled skills
bunx oc-myrios skills list   # list bundled skills
bunx oc-myrios update        # upgrade to latest (updates version pin, clears OC plugin cache)
```

## Development

```bash
bun install
bun test           # unit tests (background limits & scoping, config loader, skill sync)
bun run typecheck
bun run build      # plugin (bun target) + CLI (node target) + declarations
```

## Credits

Architecture ported and adapted from [Zenox](https://github.com/CYBERBOYAYUSH/zenox) by Ayush. Bundled skills retain their original licenses, see [`skills/NOTICE.md`](skills/NOTICE.md).

## Contact

Built by Avinash. Questions, bugs, or ideas: reach out at [avinashnarwariya5@gmail.com](mailto:avinashnarwariya5@gmail.com).
