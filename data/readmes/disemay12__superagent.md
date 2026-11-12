# Superagent

> An operating contract that turns a DeepSeek-class coding agent into a self-directed engineer: fewer explanations, fewer check-ins, verified results.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![validate](https://github.com/disemay12/superagent/actions/workflows/validate.yml/badge.svg)](https://github.com/disemay12/superagent/actions/workflows/validate.yml)
[![OpenCode](https://img.shields.io/badge/OpenCode-2.x-111111.svg)](https://opencode.ai)
[![Agents](https://img.shields.io/badge/agents-DeepSeek%20%7C%20Claude%20%7C%20GPT-black.svg)](#compatibility)

Claude infers the steps it was not given. DeepSeek-class models do not — they need an explicit trigger for every branch, a hard rule for every temptation, and a check they cannot skip. This skill supplies exactly that, so the human explains the task once instead of supervising the process.

One command. One report. No approval gates, no progress narration, no "tests pass" without the output.

## What it does

| Capability | Behaviour |
|---|---|
| **Intake** | At most 3 questions, each with a default; 0 for trivial tasks, skipped when the request is concrete |
| **Automatic calibration** | First run in a repo writes `.superagent/project.md` (gate, setup, env, do-not-touch) and updates only facts proven by execution |
| **Lanes** | Solo by default; an `explore` lane only when the files are unknown; parallel writers only for ≥2 independent areas; a verifier only for risky changes |
| **Owns verification** | Runs the project's real gate — tests, lint, typecheck, build, e2e, smoke, live probe — and fixes what its diff broke |
| **No green by weakening** | Never skips, deletes or loosens a test; never swallows an error; never excludes files from lint/types |
| **Budget & resume** | Tool-call caps, a state file outside the repo, continuation after compaction or restart |
| **One report** | `Status`, `Criteria`, evidence, diffstat, risks, and a numbered menu of optional follow-ups |
| **Batch** | Several tasks in one message become separate tickets with separate statuses |

## Install

```powershell
# Windows (PowerShell)
Copy-Item -Recurse .\skills\superagent "$HOME\.config\opencode\skills\"
Copy-Item .\commands\superagent.md "$HOME\.config\opencode\commands\"
```

```bash
# macOS / Linux
cp -r skills/superagent ~/.config/opencode/skills/
cp commands/superagent.md ~/.config/opencode/commands/
```

Restart OpenCode. Requires OpenCode 2.x; the `question` tool is used for intake when available and falls back to plain text.

## Usage

```
/superagent fix the failing OrderService test and add a regression test
/superagent add a /health endpoint with a database check and tests
/superagent 1) remove duplication in services/billing 2) add missing error handling to the invoice job
```

Empty `/superagent` asks for the task in one line. The skill also activates on phrases like "just do it" or "don't ask me", if your agent config exposes it that way.

## What a run looks like

1. **Restate** the task in one line and write 2–4 acceptance checks.
2. **Intake** — up to three questions that would change the files you touch, each with a recommended default.
3. **Calibrate** — read `.superagent/project.md`, or create it silently on first use.
4. **Read before edit** — no file is edited before it is read in the same session.
5. **Loop** — edit → run the gate → fix the cause → rerun only the failed check, at most 5 iterations.
6. **Self-check** — six yes/no questions; any "no" is fixed before reporting.
7. **Report** — one message, at most 20 lines.

## The report

```
Status: ready|blocked|failed|dropped
Criteria: c1 ✓ · c2 unverified — reason
Result: what now works (verified: cmd → result | unverified: what)
Changed: path (+X/−Y) — why
Risks: assumptions, pre-existing failures, or none
Next (reply with a number, 0 = nothing):
1. improvement — S/M/L, value
```

`ready` means the project's gate actually ran and passed. A diff is not ready. `blocked` carries one concrete question and the failing output. `dropped` means there was nothing to do.

## Calibration file

Created automatically on first run in a repository, never overwritten:

```md
# Project calibration
gate: npm test && npm run lint && npx tsc --noEmit
test_related: npx jest --findRelatedTests {files}
setup: npm ci
env: DB via docker compose up -d db; .env.local required
do_not_touch: src/generated/**, migrations/*.sql
## observed
- 2026-11-04 gate green after `npm ci` (3m12s)
- flaky: tests/e2e/login.spec.ts — failed twice, passed on rerun
```

Human lines are never rewritten. The agent appends at most one verified fact per run. Values are command and variable names, never secrets. Outside a git worktree the file lives in `~/.config/opencode/superagent/repos/`.

## Layout

```
skills/superagent/
├── SKILL.md              # the contract: start order, lanes, loop, self-check, failure modes
├── references/
│   ├── calibration.md    # project file: location, template, update rules
│   ├── checks.md         # gates by stack + definition of done per artifact
│   ├── examples.md       # bugfix, feature, refactor, blocked
│   └── eval.md           # benchmark protocol
└── scripts/
    └── eval.ps1          # headless benchmark runner
commands/
└── superagent.md         # /superagent entry point
```

## Design principles

- **Attention is a cost.** Every question, acknowledgement or progress line must buy something.
- **Deterministic over clever.** A trigger the model can check beats a principle it must interpret.
- **Verification over claims.** A result without a command output from this session is `unverified`.
- **Smallest correct diff.** Mechanical consequences are in scope; discoveries go to the follow-up menu.
- **Honest statuses.** A draft is not ready, and a blocked task says what is missing.
- **People merge.** The skill never pushes to the default branch, force-pushes or merges; commits only when asked.

## Eval

`references/eval.md` defines three tasks (bugfix, feature, refactor), pass bars and metrics. The runner drives them headless and appends CSV rows:

```powershell
powershell -File skills/superagent/scripts/eval.ps1 -Repo C:\path\to\sandbox -Tasks tasks.txt -Runs 3
```

Compare `status` and `seconds` against a baseline variant. The point is not a leaderboard — it is to notice when the skill itself gets slower or starts cutting corners.

## Compatibility

Works with any agent that can load a markdown skill and run shell commands. Optional integrations degrade gracefully:

- **graphify** or a **codebase-memory MCP** for cheap structural lookups;
- domain skills such as `better-design`, `security-review`, `database-migrations`, `e2e-testing`;
- `question` tool for the intake block (plain text otherwise).

## License

MIT — see [LICENSE](LICENSE).
