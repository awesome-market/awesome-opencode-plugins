# context-md

**Live `context.md` for AI agents.**

## What it is / how it works

Your repository carries one live file — **`context.md`** — containing the
complete, always-current description of your project: what it is, how it is
built, the decisions already made, the current focus, and a timestamped change
log of everything that happened in it. Install it once (`npx agent-context-md
install`) and every AI agent you use reads that file first. From then on,
every hook-capable agent (Claude Code, Codex, Gemini CLI, Cursor; opencode via
a plugin) is wired with five local mechanisms: **(1)** on session start the
hook refreshes `context.md` and injects "MANDATORY: read this first" into the
agent, **(2)** the agent cannot edit any file until it has read `context.md`
this session (the edit tool is hard-denied), **(3)** every file edit is
appended to the change log in real time, **(4)** ending the turn/session is
blocked while an edit was made without `context.md` being updated, and **(5)**
CI can fail on stale context (`context-md verify`). Instruction files cover
20+ agents (Copilot, Windsurf, Devin, Continue, Junie, Amazon Q, Cline, Roo,
Kilo, Augment, Tabnine, Zed, Aider…), all hooks run locally with **no API
keys, no server, no telemetry** — and you get the whole thing out of the box
by installing once.

## The problem

Every new AI coding session starts with amnesia: the agent re-derives your
stack, re-learns conventions, forgets yesterday's decisions, and its context
window compacts away whatever it eventually figured out. Teams lose hours per
week re-explaining their own project to machines.

Existing answer candidates (`CLAUDE.md` by hand, Cline Memory Bank, heavy
frameworks like `skill-memory-bank`, MCP memory servers, repo packing) all
either put the burden on you, only support a subset of agents, or require
servers/Python/bash. None of them *enforce* a single live file every agent
must respect.

## What this does

```bash
npx agent-context-md install      # in any repo, or in every project on your machine
```

After install:

1. **Before any work**, the agent reads `context.md` at the repo root — what
   the project is, its structure, decisions, current focus, change log.
2. **Every file edit** is appended to that file's Change Log — real-time.
3. **Every prompt** steers the agent toward the live file (Claude/Codex/Gemini).
4. **Editing is hard-blocked** until `context.md` has been read this session.
5. **Ending the turn/session is hard-blocked** while files changed without
   `context.md` being updated (Claude/Codex/Gemini/Cursor).
6. **CI can fail** when `context.md` is stale (`context-md verify`).

If the repo was never backfilled, the agent gets a one-time deep pass: read
README/manifests/key sources, run `git log --oneline -50`, and rewrite
`context.md` Purpose + Key Knowledge with real project facts.

## Quick start

### Per repository (share with your team)

```bash
npx agent-context-md install          # interactive: pick your agents (TTY)
npx agent-context-md install --all    # wire all supported agents
npx agent-context-md install --clients claude-code,codex,gemini-cli   # pick by id
cd your-repo && context-md verify .   # CI freshness check
```

`context.md` is created with snapshot + structure + an agent-maintained
knowledge section; commit it so teammates (and their agents) get full context
for free.

### Globally, on your machine (every project, zero setup)

```bash
npx agent-context-md install --global        # one time
# or pick specific agents:
npx agent-context-md install --global --clients claude-code,gemini-cli
```

Creates a standalone `~/.context-md/` runtime and wires your user-level agent
configs (`~/.claude/settings.json`, `~/.codex/hooks.json`, `~/.gemini/settings.json`,
`~/.cursor/hooks.json`, global opencode plugin). From then on, **every
project-like folder you open with these agents gets `context.md` automatically** —
no per-repo step. The global runtime only activates in folders containing
`.git` or a known manifest, defers to a repo's local wiring when present,
and is fully reversible with `context-md uninstall --global`.

### What you will see

```
context-md: detecting agents on this machine…
  [1] Claude Code    (command on PATH, config ~/.claude seen)
  [2] Codex (OpenAI) (config ~/.codex seen)
  ...
Enter = all detected, numbers "1,3" = pick, "a" = all, "n" = none
```

(Selection only controls **hook adapters**. Instruction files are installed for
every supported agent regardless.)

## What gets created in your repo

```
your-repo/
  context.md                 ← the shared brain (commit it)
  AGENTS.md                  ← protocol block for every agent (cross-vendor standard)
  CLAUDE.md / GEMINI.md ...  ← same protocol, one per agent convention
  .clinerules                ← Cline
  .github/copilot-instructions.md
  .kiro/steering/context-md.md
  .cursor/rules/context-md.mdc
  .devin/rules/context-md.md / .windsurf/rules/context-md.md
  .continue/rules/context-md.md   (Continue)
  .junie/guidelines.md            (JetBrains Junie)
  .amazonq/rules/context-md.md    (Amazon Q)
  .roo/rules/context-md.md        (Roo Code)
  .kilocode/rules/context-md.md   (Kilo Code)
  .augment/rules/context-md.md    (Augment)
  .tabnine/guidelines/context-md.md
  .rules / CONVENTIONS.md         (Zed / Aider)
  .context/                     ← the runtime the hooks call (commit it)
    hooks/session-start.js      ← fires on session start: refresh + brief the agent
    hooks/read-gate.js          ← fires pre-tool: deny edits until context.md is read
    hooks/prompt-gate.js        ← fires per prompt: strict protocol injection
    hooks/post-tool.js          ← fires on every edit: change-log + snapshot refresh
    hooks/stop-check.js         ← fires on turn end: block if context.md not updated
    lib/scan.js, lib/context-file.js
    package.json                ← {"type":"module"} so hooks always parse
  .claude/settings.json         ← hook wiring (backed up as *.bak-<ts>)
  .codex/hooks.json
  .gemini/settings.json
  .cursor/hooks.json
  .opencode/plugins/context-md.js
```

Per-session runtime state (`.context/session-state.json`, `.context/.last-scan`,
`*.bak-*` backups) is auto-gitignored by the installer; `.context/` itself is
meant to be committed.

## The `context.md` file, section by section

```markdown
# context.md — live project context
> Maintained by context-md — every agent MUST read it; hooks maintain it.

## Snapshot                        ← auto-managed (between markers)
- Updated: 2026-11-18T15:06:53Z
- Git: main @ 501286e · 3 uncommitted changes
- Stack: Node.js + TypeScript · Next.js · pnpm
- Files (excl. deps/build): 132 · dependencies: 47
- Scripts: dev=`next dev`, test=`node --test`

## Structure                       ← auto-managed (between markers)
src/  (42 files)
test/ (6 files)
package.json ...

## Purpose                         ← agent-owned
(what this project IS — the agent writes this once it understands the repo)

## Key Knowledge                   ← agent-owned
Stack & architecture: decisions, patterns, constraints
Conventions: naming, testing, commit style
Gotchas: things that would bite a newcomer

## Current Focus / Next Steps      ← agent-owned
(what is being worked on RIGHT NOW, and what comes next)

## Change Log                      ← auto-managed (between markers)
- 2026-11-18T10:29:08Z context.md created
- 2026-11-18T11:02:51Z edited "src/index.ts"
- ...
```

**Auto-managed sections** (Snapshot / Structure / Change Log) are rewritten by
hooks and must never be hand-edited — they are regenerated from the repo state.
**Agent-owned sections** (Purpose / Key Knowledge / Current Focus) are yours
(and the agent's) to keep current; the stop gate makes sure they are.

If `context.md` loses its markers (hand-edit gone wrong), the session-start
hook does NOT delete it — it moves the broken file aside as
`context.md.broken-<timestamp>` and starts fresh, preserving your data.

## Every supported agent — and how much is enforced

**All agents get the protocol via committed instruction files** (inert
markdown; an agent that does not understand a file just skips it):

| Surface | Agents covered |
|---|---|
| `AGENTS.md` (cross-vendor standard) | Claude Code, Codex, Gemini CLI, Cursor, opencode, Copilot, Windsurf, Devin, Continue, Kiro, Junie, Jules, Factory, Warp, Tabnine, Zed, Roo, Kilo, most 2026 coding agents |
| `CLAUDE.md` | Claude Code |
| `GEMINI.md` | Gemini CLI |
| `.github/copilot-instructions.md` | GitHub Copilot (VS Code / CLI / coding agent) |
| `.kiro/steering/context-md.md` | Kiro |
| `.cursor/rules/context-md.mdc` | Cursor (always-apply rule) |
| `.devin/rules/context-md.md` + `.windsurf/rules/` | Devin / Windsurf |
| `.continue/rules/context-md.md` | Continue (VS Code / JetBrains) |
| `.junie/guidelines.md` | JetBrains Junie |
| `.amazonq/rules/context-md.md` | Amazon Q Developer |
| `.clinerules` | Cline |
| `.roo/rules/context-md.md` | Roo Code |
| `.kilocode/rules/context-md.md` | Kilo Code |
| `.augment/rules/context-md.md` | Augment |
| `.tabnine/guidelines/context-md.md` | Tabnine |
| `.rules` | Zed |
| `CONVENTIONS.md` | Aider (and any agent using conventions files) |

**Hook API agents get hard enforcement on top** — read gate before any file
edit, per-edit real-time logging, stop gate at turn end:

| Agent | Hooks (all committable, machine-independent) |
|---|---|
| Claude Code | `SessionStart` inject · `UserPromptSubmit` strict rule · `PreToolUse deny` (read gate) · `PostToolUse` log · `Stop` block |
| Codex (OpenAI) | `SessionStart` · `UserPromptSubmit` · `PreToolUse deny` · `PostToolUse` · `Stop` |
| Gemini CLI | `SessionStart` · `BeforeAgent` · `BeforeTool deny` · `AfterTool` · `AfterAgent` deny→retry |
| Cursor | `sessionStart` · `preToolUse deny` · `postToolUse` · `stop` followup (loop-limited) |
| opencode | plugin v1+v2 (session + post-edit log; no verified turn-end hook) |

Everyone else: protocol via instruction files + `context-md verify` in CI.

## Why there are no API keys

context-md is **not** an LLM. It ships no model, no server, no phone-home, no
telemetry. The only processes are the hook scripts your agent invokes; they
read the repo, write `context.md`, print JSON for the agent. Your subscription,
your models, your data — untouched.

## How the real-time update works (the honest version)

| Layer | What happens |
|---|---|
| Session open | Hook refreshes Snapshot/Structure, injects "MANDATORY: read context.md first" + backfill protocol if needed |
| Every user prompt | Strict protocol reminder injected (Claude/Codex/Gemini) |
| Before any edit | **Read gate**: file edits are *denied* until context.md was read this session |
| After every edit | One line appended to Change Log; snapshot refreshed when stack manifests change |
| End of turn | **Stop gate**: turn is blocked while an edit was made without updating context.md (max 2 re-blocks, then releases) |
| CI | `context-md verify` fails the build when files changed without a context.md refresh |

No tool can make an LLM retain everything it never writes down. What context-md
guarantees: nothing is *silently* lost — every edit is logged, reading is
enforced before editing, and ending a turn without syncing is blocked on hook-capable
agents. What an agent still cannot do for you is remember a decision it never
wrote; that's why the backfill pass exists.

## Commands

```bash
context-md install [dir] [--all] [--clients a,b]   # wire a repo
context-md install --global [--all] [--clients a,b] # machine-wide default
context-md uninstall [dir]                          # remove wiring (keeps context.md)
context-md uninstall --global                        # remove machine-wide wiring
context-md uninstall --remove-context [dir]          # also delete context.md
context-md backfill [dir]                            # regenerate + print the backfill protocol
context-md refresh [dir]                             # rebuild snapshot/structure now
context-md verify [dir]                              # CI check, exits 1 when stale
context-md doctor [dir]                              # health check (all green = ready)
context-md status [dir]                              # what is wired (repo + global)
context-md --help | --version
```

`verify` prints `OK: context.md is fresh` or `STALE: … Run context-md refresh.`
`doctor` prints PASS/FAIL per check and exits non-zero on any failure.

### CI example (GitHub Actions)

```yaml
name: test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx agent-context-md install --all .   # wire in CI (optional)
      - run: npx agent-context-md verify .
```

## Uninstall (clean, provable)

```bash
context-md uninstall .              # removes blocks + hook wiring, KEEPS context.md
context-md uninstall --remove-context .
context-md uninstall --global
```

Removes only what context-md created: marked blocks in instruction files
(restored), context-md hook entries (other hooks you wrote are preserved),
`.context/`, and for `--global` the `~/.context-md` runtime and global hook
entries. Config files are backed up before every edit (`*.bak-<timestamp>`);
back up your config if you want to double-check with `git diff`.

## Troubleshooting

- **Codex does not fire hooks** — Codex requires trust review: open `/hooks`,
  review and trust the context-md entries.
- **Gemini hooks seem ignored** — Gemini fingerprints project hooks; changed
  hooks need re-review. SessionStart output uses scaffolding; context.md is the
  source of truth regardless.
- **User's settings "went away"** — they didn't: invalid/BOM-prefixed JSON is
  never overwritten (the adapter skips that agent with an error). Look for
  `*.bak-<timestamp>` next to the file.
- **"context.md has broken markers"** after a hand-edit — session start moves
  the broken file to `context.md.broken-<timestamp>` and rebuilds; your content
  is preserved there.
- **Install reports `invalid JSON — not touched`** — the config file exists but
  is corrupt/non-standard. Fix it or remove it, then re-run.
- **Everything looks fine but `verify` fails** — files changed after
  `context.md`; run `context-md refresh`, then commit context.md.

## Security

Committed `.context/` is executable code that every clone runs when an agent
opens the repo — treat it like CI workflow changes in review. The installer
never overwrites an existing (possibly hand-edited) `context.md`, refuses to
write through symlinks, and leaves unrelated config untouched. See
[SECURITY.md](SECURITY.md) for the threat model, safe use, and reporting.

## FAQ

**Does the agent see `context.md` if its IDE is closed?** The hooks only run
while the agent runs — but the committed `context.md` is always on disk; the
next session re-injects it.

**Do teammates need to install?** No — if you commit `context.md` and
`.context/`, any teammate with a supported agent gets the wiring for free on
their next session.

**Does it cost money?** No. Zero API keys, zero servers, zero telemetry.

**Does it work on Windows?** Yes — tested on Windows 11 (PowerShell, Git Bash)
with Claude/Codex/Gemini/Cursor paths. The hook commands are
machine-independent and committed with relative/env-var paths
(`${CLAUDE_PROJECT_DIR}`, `./.context/hooks/…`, `$GEMINI_PROJECT_DIR/…`,
`$(git rev-parse --show-toplevel)/…`).

**Can I use only one agent?** Yes: `--clients claude-code` (or any subset),
or pick interactively.

**What if I don't want it in a repo?** Don't commit `.context/` there — or
remove the wiring with `context-md uninstall`.

## Contributing / developing

See [CONTRIBUTING.md](CONTRIBUTING.md). `npm test` runs 27 end-to-end tests
(temp git repos, no network). Every user-facing artifact is plain Node ESM
with zero dependencies.

## License

MIT — see [LICENSE](LICENSE).
