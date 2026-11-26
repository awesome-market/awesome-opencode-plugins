# gamefirst

A playable-first game development framework for a solo developer.

gamefirst is deliberately small: ten rules, four agents, thirteen skills, three
gates plus two checkpoints, twelve eval specs, ten tools, and six commands. It is not a studio org chart
and it does not ask for a fifty-page GDD before the first build. A mechanic is
designed only as far as the next playable test; documentation describes what
already works, never what might.

Version: `0.3.0-dev`.

## What it does

- One game is one repository; this framework stays a separate checkout.
- The core is engine-agnostic. `src/systems/` never imports the engine.
- Work moves in small parts: one mechanic, one playable loop, one test, one
  decision. A part is accepted only when it runs.
- Documents are written after the code proves the behaviour. A system card is
  one page and cites the test that verifies it.
- Gates are one-line human decisions, not reports: `G1` fun, `G2` slice and
  `G3` ship; `G0` brief and `G2.5` freeze are checkpoints.
- Autonomy is a written contract in `STATE.md`, not a mode switch.

## Requirements

- Node.js 20 or newer (the tools use only the standard library).
- One host: OpenCode (V2 `permissions`), Codex, or Claude Code.
- Git is optional; `--git` initialises the game repository.
- Windows, macOS, and Linux. Paths in documents are POSIX-style; the tools
  accept Windows paths.

## Layout

```text
gamefirst/
├── template/        # the game repository skeleton, engine-free
├── library/
│   ├── core/        # 10 rules, 4 agents, 13 skills, evals, memory, autonomy
│   ├── game/        # crews and gates for the game pipeline
│   ├── engines/     # N00 contract, phaser/unity/godot packs (beta, docs+recipes)
│   └── packs/       # release, obsidian, art, audio, narrative, localization, marketing
├── hosts/           # OpenCode/Codex/Claude Code layout and settings adapters
├── tools/           # new-project, status, verify, eval, sync, upgrade, doctor, lint, trigger, capture
├── docs/            # blueprint, build plan, review rubric, session log
└── examples/        # reserved for worked examples
```

A generated game looks like this:

```text
my-game/
├── .opencode/       # OpenCode host (only with --host opencode)
├── .agents/         # Codex host (only with --host codex)
├── .claude/         # Claude Code host (only with --host claude)
├── CLAUDE.md        # Claude Code entry point (only with --host claude)
├── src/systems/     # engine-free game logic
├── src/data/        # data tables and tuning
├── src/game/        # the only engine adapter
├── tests/
├── docs/            # systems, playtests, engine, guide, retro
├── evidence/        # proof of done
├── runs/            # autonomy and question logs
├── AGENTS.md        # the project contract
├── BRIEF.md         # the idea and its success test
├── STATE.md         # phase, mode, active part, next action
├── DECISIONS.md     # append-only decision record
├── GAME.md          # player-facing vision
├── TASTE.md         # feel, references, anti-rules
├── BACKLOG.md       # ideas that are not in scope
└── decisions.ru.md  # short Russian digest for the human
```

## Quick start

From this checkout:

```bash
# OpenCode (default)
node tools/new-project.mjs ../my-game --name "My Game" --host opencode --git

# Codex
node tools/new-project.mjs ../my-game --name "My Game" --host codex --git

# Claude Code
node tools/new-project.mjs ../my-game --name "My Game" --host claude --git
```

The flag changes only the host layout; rules, skills, gates and documents are
shared.

Open `my-game` in the chosen host and run `/start` (or `$start` on Codex).
`/start` reads the five core files, recommends a mode, and names the first
missing decision. Then:

```text
/next      # one next action
/status    # phase, active part, gate, blockers
/verify    # run the project's build/test recipe and write evidence
```

On Codex, invoke the same commands as `$next`, `$status`, `$verify`, `$retro`,
`$help`.

The first useful milestone is a playable core loop, not a document. Use
`/retro` after a loop or a failed attempt to record one change.

## Commands

| Command | OpenCode / Claude Code | Codex | What it does |
|---|---|---|---|
| `start` | `/start` | `$start` | reads the project, recommends a mode, names the first missing file |
| `status` | `/status` | `$status` | prints phase, active part, gate, next action, blockers |
| `next` | `/next` | `$next` | prints the one next action and why |
| `verify` | `/verify` | `$verify` | runs `verify.recipe`, records evidence, never fixes |
| `retro` | `/retro` | `$retro` | writes the five-line retro under `docs/retro/` |
| `help` | `/help` | `$help` | one-screen map of the project and commands |

## Hosts

One source, three layouts:

- **OpenCode** — `.opencode/` plus `opencode.json` with the V2 permissions
  array and `default_agent`.
- **Codex** — `.agents/` with rules, skills, roles, crews and gates; the six
  commands are installed as skills and invoked as `$start`, `$next`, and so on.
  Codex has no custom subagent files, so A04 critic is a separate read-only
  pass.
- **Claude Code** — `.claude/` with rules, skills, subagents, crews, gates and
  commands, plus `CLAUDE.md` and `.claude/settings.json`.

`status`, `verify` and `doctor` work in all three. `sync-agent` and `upgrade`
remain OpenCode-first in v0.3. See [hosts/README.md](hosts/README.md) for the
scope of the adapter.

## Tools

| Tool | Purpose |
|---|---|
| `new-project.mjs` | create a game repository for OpenCode, Codex or Claude Code |
| `status.mjs` | read-only snapshot of `STATE.md`, `BACKLOG.md`, `agent.lock.json` |
| `verify.mjs` | run the recipe in `project.config.json`, write `evidence/` |
| `eval.mjs` | run deterministic eval fixtures against a game |
| `sync-agent.mjs` | pull/push/diff library parts through `agent.lock.json` |
| `upgrade.mjs` | dry-run, diff, then apply a framework upgrade |
| `doctor.mjs` | read-only health check for links, encoding, placeholders, host settings |
| `lint-agent-context.mjs` | check token budgets and instruction priority |
| `trigger-check.mjs` | lexical check that skills/agents are selectable |
| `capture.mjs` | screenshot a running game into `evidence/` |

## Packs and engines

`library/engines/` holds the engine contract and three engine packs:

- `phaser/` - beta docs and recipes, pinned to Phaser 4.2.1; no starter project yet;
- `unity/` — beta, Unity 6000 LTS;
- `godot/` — beta, Godot 4.x.

`library/packs/` holds seven optional domain packs: `release`, `obsidian`,
`art`, `audio`, `narrative`, `localization`, `marketing`. They are reference
material: a pack has a `PACK.md`, an eight-key `manifest.json`, a template, and
an offline `selftest.mjs`.

In v0.3, `new-project` installs `core` and `game` only; the default is now
`core,game`, so the game pipeline is present. Engine and domain packs are not
auto-installed yet; `--packs` rejects them explicitly. Copy the pack you need
into the game, or wait for the v0.4 installer. Do not pretend a pack is loaded
when it is only present in the library.

`evals/` ships eval specs, not fixtures. `eval.mjs` exits non-zero when no
fixture is runnable; a green run means checks actually ran. The same is true for
`/verify`: an empty `verify.recipe` is a FAIL, not a pass.

## Updating a game

```bash
node tools/sync-agent.mjs diff ../my-game
node tools/upgrade.mjs ../my-game --dry-run
node tools/upgrade.mjs ../my-game --apply
node tools/doctor.mjs ../my-game
```

`upgrade` writes `docs/UPGRADE-<from>-to-<to>.md`; `doctor` is read-only and
returns a non-zero exit on errors. On a fresh project the empty `verify.recipe`
is an expected warning; use `--strict` after an engine is chosen. In v0.3 `upgrade --apply` overwrites changed
parts without a three-way merge: commit or back up a game before applying it,
especially if you edited rules or skills by hand.

## Tests

```bash
# every pack has an offline selftest
node library/packs/art/selftest.mjs

# the framework smoke checks used while building v0.3
node tools/lint-agent-context.mjs --root .
node tools/trigger-check.mjs --root .
```

The framework was assembled one part at a time; each accepted part has its
`JUSTIFICATION.md`, `SOURCES.md`, and `REPORT.md` under `docs/build/<ID>/`.

## Limits in v0.3

- Engine and domain packs are not installed by `new-project`.
- `new-project` does not create a runnable app: no `package.json`, no
  `index.html`, and the default `verify.recipe` is empty until an engine is
  chosen.
- `sync-agent` and `upgrade` are OpenCode-first in v0.3.
- Unity and Godot packs are beta; their pitfalls need runtime reproduction.
- Command execution is covered by structural checks, not a live software
  runtime.
- P04–P07 are offline references; none is wired to a runtime.
- Packs close to their size caps (P05, P07) need a re-measure after any edit.

## Where to read more

- [Blueprint](docs/V0.3-BLUEPRINT.md) — what exists and why.
- [Build plan](docs/BUILD-PLAN.md) — every part and its status.
- [Review rubric](docs/REVIEW-RUBRIC.md) — how a part is accepted.
- [Russian guide](GUIDE.ru.md) — how to start a project step by step.
- [Russian quick start](docs/QUICKSTART.ru.md) — one page for the human.
- [Host adapters](hosts/README.md) — OpenCode, Codex, Claude Code.
