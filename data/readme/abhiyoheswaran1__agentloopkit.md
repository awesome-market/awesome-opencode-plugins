# AgentLoopKit

<p align="center">
  <img src="https://raw.githubusercontent.com/abhiyoheswaran1/AgentLoopKit/main/docs/logo/icon.svg" alt="AgentLoopKit logo" width="96" height="96">
</p>

A drop-in engineering loop for software agents.

An open-source Baseframe Labs developer tool.

Your software agent can produce a diff. AgentLoopKit helps you decide whether that work is reviewable, verifiable, and merge-ready.

It gives Codex, Claude Code, Cursor, OpenCode, Gemini CLI, GitHub Copilot CLI, and other engineering agents a local acceptance layer: task contracts, safety rules, verification evidence, review-readiness scores, PR descriptions, and reviewer handoffs.

Unstructured automation produces code. Agentic engineering produces auditable work.

ProjScan finds the risk.
AgentLoopKit controls the work.
AgentFlight proves the result.

<p align="center">
  <img src="https://raw.githubusercontent.com/abhiyoheswaran1/AgentLoopKit/main/docs/assets/readme/agentloopkit-showcase.png" alt="AgentLoopKit workflow showing task contracts, verification reports, and handoff artifacts" width="100%">
</p>

The screenshots and terminal demos in this README are generated from committed sources in `docs/assets/readme/` with Playwright and VHS. You can regenerate them locally.

## What It Does

AgentLoopKit is a repo-level toolkit for developers using Codex, Claude Code, Cursor, OpenCode, Gemini CLI, GitHub Copilot CLI, and other engineering agents.

Keep your agent, IDE, and CLI. AgentLoopKit gives those tools a repeatable local workflow:

1. Specify the task.
2. Constrain the risk.
3. Implement the smallest useful change.
4. Verify with real commands.
5. Review the diff.
6. Hand off with evidence.
7. Ship only when the work is reviewable.

Run `init` inside an existing repository and AgentLoopKit creates:

- `.agentloop/` for tasks, reports, handoffs, gates, policies, templates, and agent instructions
- `AGENTS.md` for agent-facing repo guidance
- `AGENTLOOP.md` for the working loop
- `agentloop.config.json` for local command and path settings

Generated `AGENTS.md` includes a specialist roster for product, CLI, template, verification, security, release, docs, compatibility, MCP, and repo-steward work. It helps future agent sessions split work without adding a background service.

<p align="center">
  <img src="https://raw.githubusercontent.com/abhiyoheswaran1/AgentLoopKit/main/docs/assets/readme/agentloopkit-cli.gif" alt="Terminal demo showing AgentLoopKit init, task creation, verification, ship evidence, PR preparation, review context, run history, and file intent" width="100%">
</p>

The CLI demo shows the normal path: initialize a repo, create a task, run reviewed verification, score review readiness, draft PR copy, inspect review context, and trace why a file changed.

## Install

Use it with `npx` from the repository you want to configure:

```bash
cd /path/to/your/repo
npx agentloopkit init --dry-run
npx agentloopkit init
```

`init` writes files into the current directory. `--dry-run` previews the same plan and writes nothing.

Commit the generated harness baseline before your first feature task when you want clean diff evidence. If the harness files are still uncommitted, `explain-diff`, Guard, and resume packs will include those generated files as local work, which is accurate but noisier than the steady-state loop.

After setup, non-init commands search upward for the nearest `agentloop.config.json` and use that folder as the AgentLoop root. You can run `agentloop status`, `agentloop verify`, `agentloop ship`, or `agentloop prepare-pr` from a nested source folder and still write tasks, reports, runs, and handoffs to the initialized repo root.

Do not run `init` from your home directory unless you intend to configure your home folder. AgentLoopKit refuses that by default; `--force` allows it and prints a home-directory target warning. If you want local agent guidance but do not want to commit the generated files, use local-only mode:

```bash
npx agentloopkit init --local-only
```

`--local-only` writes the harness, asks Git for this clone's metadata directory, then adds a marked block to that clone's `info/exclude` for `.agentloop/`, `AGENTS.md`, `AGENTLOOP.md`, and `agentloop.config.json`. It does not edit `.gitignore`, global Git config, shell profiles, or other project files.

The examples below use `agentloop` after setup. If you are not installing the package locally or exposing its binary on `PATH`, keep using the one-off form, for example `npx --yes agentloopkit@latest doctor --redact-paths`.

Check the published package explicitly:

```bash
npx --yes agentloopkit@latest version
npx --yes agentloopkit@latest init
```

For repeatable CI or team setup, replace `@latest` with a vetted version.

Before initialization, exploratory preflight can be advisory:

```bash
npx --yes agentloopkit@latest doctor --advisory --redact-paths
```

Advisory mode keeps missing-setup diagnostics visible but exits `0` so first-run scripts can continue. Use plain `doctor` or `doctor --strict` for gates that should fail on setup errors.

Pinned team usage:

```bash
pnpm add -D agentloopkit
pnpm agentloop init
```

## Existing Repos

Repos that already use AgentLoopKit can update the CLI without rewriting local harness files:

```bash
cd /path/to/existing/repo
npx --yes agentloopkit@latest version
npx --yes agentloopkit@latest doctor --redact-paths
npx --yes agentloopkit@latest upgrade-harness --details --redact-paths
npx --yes agentloopkit@latest init --dry-run
```

These commands inspect the published package. This repository may document unreleased guidance before the next publish; check [release status](docs/release-status.md) before expecting `agentloopkit@latest` to include new subcommands.

`init` skips existing generated files and appends to unmarked `AGENTS.md` files instead of overwriting maintainer edits. Use `upgrade-harness` to find older guidance that does not tell agents to run `agentloop doctor` and `agentloop start` before broad reads, list handles with `agentloop context handles` when available, or expand source truth with `agentloop context show <handle>`. Copy only the useful pieces into `AGENTS.md`, `AGENTLOOP.md`, or `.agentloop/harness/*`.

You can use the latest loop before refreshing old guidance:

```bash
npx --yes agentloopkit@latest create-task --type bugfix --title "Fix checkout bug"
npx --yes agentloopkit@latest start --for generic --goal implement --redact-paths
npx --yes agentloopkit@latest verify
npx --yes agentloopkit@latest ship
npx --yes agentloopkit@latest prepare-pr
npx --yes agentloopkit@latest maintainer-check
```

## Core Workflow

First useful loop after `init`:

```bash
agentloop doctor
agentloop create-task --type bugfix --title "Fix checkout bug" --include-config-commands
agentloop status --brief
agentloop start --for codex --goal implement --redact-paths
agentloop loop create --goal "Keep checkout work release-ready" --budget-tokens 50000 --max-iterations 5
agentloop loop tick
agentloop loop scorecard
agentloop ready
agentloop verify --task-commands --progress
agentloop ship
agentloop prepare-pr
agentloop task done
```

That sequence creates a task contract, checks the repo setup, gives the next software agent a compact start briefing, records a local loop contract with token receipts, scores whether another loop pass should continue, checks readiness gates, runs only reviewed verification commands, records review-readiness evidence, drafts PR copy, and closes the active task. It does not post to GitHub, publish packages, call an LLM, execute a coding agent, or run hidden commands.

### Make Your Agent Start Here

Before a software agent broad-scans the repo, run:

```bash
agentloop doctor --redact-paths
agentloop start --for codex --goal implement --redact-paths
agentloop context handles --redact-paths
agentloop context show <handle-from-start> --redact-paths
```

`doctor` checks the Agent Readiness Matrix: Doctor-before-Start guidance, Start guidance, context-handle guidance, broad-read avoidance, MCP guidance, and installed agent instruction files. `start` gives the current task, proof, risk, context budget, and source handles. `context handles` lists which handles are available now. `context show` expands exact local source truth only when the agent needs detail.

```bash
npx agentloopkit init
agentloop create-task --title "Fix login redirect bug" --type bugfix \
  --acceptance "Password-reset login redirects to the requested page" \
  --include-config-commands \
  --verification "npm test -- auth"

# Run Codex, Claude Code, Cursor, OpenCode, Gemini CLI, or another software agent.

agentloop verify --task-commands --only-task-commands --progress
agentloop ship --github-comment
agentloop prepare-pr
```

`create-task` sets the new contract as the active task. Use `agentloop task set <path>` only when you need to switch to another contract.
Add `--include-config-commands` when you want the task contract to copy non-empty `test`, `lint`, `typecheck`, and `build` commands from `agentloop.config.json`. Task creation records those commands; it does not run them. Use `verify --task-commands --only-task-commands` when the active contract already includes the full check list.
Use `verify --post-verification-gates` only for reviewed task gates that need the verification report to exist first.
After verification and `ship`, use `agentloop prepare-pr` for reviewer copy and `agentloop task done` to close the active task before starting unrelated work.

Use `agentloop status` or `agentloop next` when an agent needs the next local action without reading every file:

```bash
npx agentloopkit status
npx agentloopkit status --brief
npx agentloopkit next
npx agentloopkit next --redact-paths
```

When `status` or `next` recommends `create-task` in a dirty repo, the reason calls out existing dirty non-evidence files so agents can confirm the next task scope before implementation. When `create-task` sees that same pre-existing dirty work, it also adds a bounded Risk Notes bullet to the generated task contract so later review evidence preserves the baseline count and examples.

Use `agentloop start --for codex --goal implement --redact-paths` when a software agent needs the repo truth before broad reads. Start is the preflight: current task when one exists, decisive state, next safe command, read-first handles, risk summary, verification freshness, context-budget impact, and source handles. Use `agentloop context handles` to list available handles and normal empty states, then `agentloop context show <handle>` to expand source truth only when needed. Use `agentloop context pack --for codex --goal continue --redact-paths` when you need the lower-level receipt and omission details directly. Use `agentloop guard` when you want a live local check for scope drift, stale verification, proof debt, and context-budget pressure before review. Use `agentloop explain-diff` when you need to understand whether the current changed files are covered by task scope, recent run evidence, fresh verification, and risk guidance. Use `agentloop resume-pack --for codex`, `--for claude`, `--for cursor`, `--for generic`, or `--for human` when you need the older compact continuation surface. These commands are read-only by default and use local evidence only.

`agentloop start` is the agent starting point. It keeps agents from guessing by turning task state, changed files, verification, risk, and context pressure into one compact preflight. The Context Contract sits underneath it: `context pack` explains why each item is present, names what was left out, and provides local handles for the source truth. A large changed-file list becomes a small briefing the agent can expand only when it needs detail.

`agentloop loop` adds a local loop contract on top of normal task contracts. `agentloop loop create` records the goal, budget, stop conditions, suggested commands, native task path, and a token receipt. `agentloop loop tick` records one iteration decision from local evidence: continue, stop, ask for human review, or mark the loop ready when gates pass. Once a loop asks for human review, AgentLoopKit rejects another tick until someone reviews the loop report and resolves the blocking evidence. Use `agentloop ready` when you need the current review-readiness gate summary without creating a loop.

Use `agentloop harden [task]` before work starts to interrogate a task contract for unresolved soft spots — placeholder text, unbounded scope, unstated assumptions, untestable acceptance criteria, and contradictions between Acceptance Criteria and Non-Goals. It defaults to the active task and exits non-zero when a blocking soft spot remains. Resolve one with `agentloop harden --resolve <id> --answer "..."`, which records the answer in the contract's Hardening Log. `agentloop create-task` reports the same soft spots by default right after creating a contract.

For a bounded autonomous pass, configure one local runner command and let AgentLoopKit record the iteration:

```bash
agentloop loop create \
  --goal "Keep checkout work release-ready" \
  --runner-command "node scripts/agentloop-runner.mjs" \
  --runner-timeout-ms 600000 \
  --budget-tokens 50000 \
  --max-iterations 5

agentloop loop run
agentloop loop scorecard
agentloop ready --strict
agentloop loop report
```

`loop scorecard` is the pre-flight gate before another autonomous pass. It reads the loop contract, readiness state, context pack, token budget, iteration budget, runner guardrails, and scope evidence, then returns `continue`, `ask-human`, `stop`, or `ready`. It does not execute the runner or run verification.

`loop run` executes only the command saved in the loop contract. It uses `shell: false`, rejects shell syntax, blocks publish and destructive command families, caps runner output, records changed files, and still applies the max-iteration and token-budget stop conditions. AgentLoopKit controls the goal, budget, scope, gates, evidence, and stop decision. Your agent, script, CI job, or AgentFlight session does the implementation work.

JSON and MCP context budget/pack payloads keep that boundary: they include compact evidence fields and the `evidence-map:current` handle, but they do not send the full changed-file list unless the agent expands that local handle.

Start uses a strict current-work rule. It accepts active or open task contracts. Archived, `done`, `deferred`, and AgentFlight placeholder tasks stay as previous evidence. Start and Context omit `task:active` handles and `agentloop ship` guidance for old work. In a clean repo with only previous evidence, Start tells the agent that no active task exists.

```text
Your software agent / app
  (Codex, Claude Code, Cursor, OpenCode, Gemini CLI, Copilot CLI,
   LangChain, Agno, Strands, your own scripts...)
        |
        | task contracts - diffs - verification - runs - research notes - logs
        v
 +------------------------------------------------------------------------+
 | AgentLoop Start Preflight + Context Contract (source truth stays here) |
 |------------------------------------------------------------------------|
 | State -> Next Safe Command -> Read First -> Risk -> Impact -> Handles   |
 |                                      |                                  |
 |                                      +-- task:active (current work only)|
 |                                      +-- verification:latest            |
 |                                      +-- run:latest                     |
 |                                      +-- evidence-map:current           |
 |                                      +-- context-budget:current         |
 |                                                                        |
 | Goals: implement - continue - review - debug - handoff - research       |
 | MCP tools - generated agent instructions - transparent local heuristics |
 +------------------------------------------------------------------------+
        |
        | compact preflight + retrieval handles
        v
Agent session / review / research handoff
```

<p align="center">
  <img src="https://raw.githubusercontent.com/abhiyoheswaran1/AgentLoopKit/main/docs/assets/readme/agentloopkit-context-budget.png" alt="AgentLoopKit context budget example showing broad changed-file context compressed into a compact context pack with transparent token estimates" width="100%">
</p>

The context-budget example is generated from local AgentLoopKit output in this repository. Token estimates use `ceil(character_count / 4)` for planning, not provider tokenizer counts or billing claims. The percentage changes with repo state; the point is that agents can start from selected evidence and expand source handles instead of pasting broad history.

Run the repeatable [Start usefulness demo](docs/start-usefulness-demo.md) to create a temporary messy repo and see `agentloop doctor` check agent-readiness guidance, then `agentloop start` report context avoided, broad files avoided, stale proof, scope drift, source handles, and the next safe command.

<p align="center">
  <img src="https://raw.githubusercontent.com/abhiyoheswaran1/AgentLoopKit/main/docs/assets/readme/agentloopkit-context-contract.gif" alt="Terminal demo running AgentLoopKit Start preflight with state, next command, context budget, source-handle expansion, and verification evidence" width="100%">
</p>

The terminal demo is generated from committed VHS sources in this repository. It shows the intended agent workflow: check readiness with Doctor, run Start preflight, see what not to broad-scan, expand the current task handle when one exists, and verify with local evidence.

<p align="center">
  <img src="https://raw.githubusercontent.com/abhiyoheswaran1/AgentLoopKit/main/docs/assets/readme/agentloopkit-verification.png" alt="AgentLoopKit verification report with command results, task evidence, changed files, and review gates" width="100%">
</p>

Verification reports turn local commands into review evidence. They keep command status, failure summaries, task links, changed-file context, and follow-up gates in one artifact reviewers can inspect.

## Dogfood Gate

AgentLoopKit uses its own loop in this repo. Contributors can run the same local self-check:

```bash
npm run dogfood
```

That command checks task-folder hygiene, current loop status, public docs hygiene, dependency audit results, harness upgrade state, review gates, artifact inventory, maintainer reviewability, agent review context, AgentFlight health, and ProjScan health. It does not publish packages, create tags, post comments, read tokens, read `.env` contents, or run verification commands.

Use JSON output when an agent or CI job needs a structured dogfood summary:

```bash
npm run dogfood:json
npm run dogfood:strict:json
```

The JSON summary reports the mode, overall status, step results, exit codes, durations, and safety notes. It redacts the current workspace root as `[git-root]` before printing structured output.

Run the public-doc check by itself when you edit README, examples, or release-channel docs:

```bash
npm run check:public-docs
```

Use the stricter gate before a release or final handoff:

```bash
npm run dogfood:strict
```

Use the maintenance gate when typecheck, release-proof or npm-status command health, public docs, SchemaStore, policy packs, GitHub metadata, AgentFlight, or ProjScan behavior changes:

```bash
npm run maintenance:check
```

`maintenance:check` covers unit tests, typecheck, public docs, links, non-strict npm release-proof smoke coverage, read-only npm-status safety tests, SchemaStore output and consistency tests, policy-pack inventory and safety tests, GitHub metadata safety and ship-score neutrality tests, AgentFlight, ProjScan, and the non-strict dogfood self-check. Use `npm run dogfood:strict` after fresh handoff or ship evidence exists, when review-gate warnings should block the handoff. maintainer-check warnings remain reviewer guidance unless the command exits non-zero. Strict public release proof remains part of approved release gates.

## Commands

The package exposes two binaries:

```bash
agentloop init
agentloopkit init
```

| Command                          | Purpose                                                                        |
| -------------------------------- | ------------------------------------------------------------------------------ |
| `agentloop init`                 | Generate the repo harness and config                                           |
| `agentloop doctor`               | Check setup health, agent readiness, commands, git state, and risk files; use `--advisory` for first-run preflight |
| `agentloop create-task`          | Create a scoped task contract                                                  |
| `agentloop task ...`             | List, show, pin, update, archive, and inspect task state                       |
| `agentloop status`               | Show active task, latest report, latest run, dirty files, and next step        |
| `agentloop next`                 | Print only the next recommended loop action                                    |
| `agentloop start`                | Run a repo-native agent preflight with task, evidence, risk, proof, and impact |
| `agentloop review-context`       | Show one read-only reviewability context snapshot                              |
| `agentloop context`              | List handles, build context budgets and packs, and expand source truth         |
| `agentloop ready`                | Check task, scope, verification, and context-budget readiness                  |
| `agentloop harden`               | Interrogate a task contract for unresolved soft spots before work starts        |
| `agentloop loop`                 | Record local loop goals, guarded runner passes, scorecards, token receipts, iteration decisions, and stop reasons |
| `agentloop guard`                | Check local drift, proof debt, and context-budget pressure                     |
| `agentloop explain-diff`         | Explain the current diff with local task, verification, run, and risk evidence |
| `agentloop resume-pack`          | Generate a compact local continuation brief for agents or reviewers            |
| `agentloop verify`               | Run configured checks and write a verification report                          |
| `agentloop ship`                 | Score review readiness, write a ship report, and optionally print a PR comment |
| `agentloop prepare-pr`           | Generate a PR title, grouped body, and optional GitHub comment                 |
| `agentloop summarize`            | Preview a deterministic reviewer summary                                       |
| `agentloop handoff`              | Write a reviewer handoff summary                                               |
| `agentloop check-gates`          | Check review evidence without running tests                                    |
| `agentloop runs --latest`        | Show the newest local ship, verify, or handoff run entry                       |
| `agentloop show-run <id>`        | Show one local run ledger entry                                                |
| `agentloop intent <file>`        | Show bounded newest-first run matches for one file and why                     |
| `agentloop maintainer-check`     | Check whether an agent-assisted PR is reviewable                                  |
| `agentloop artifacts`            | Inventory local tasks, reports, ship reports, badges, and run evidence         |
| `agentloop artifacts --stale`    | Preview capped older local evidence candidates without deleting files          |
| `agentloop upgrade-harness`      | Inspect older generated guidance without overwriting local edits               |
| `agentloop report`               | Write a local static HTML evidence report                                      |
| `agentloop badge`                | Write a local SVG evidence badge                                               |
| `agentloop ci-summary`           | Summarize CI context and existing AgentLoop evidence                           |
| `agentloop release-notes`        | Draft local release notes from repo evidence                                   |
| `agentloop release-check`        | Check local release readiness without publishing                               |
| `agentloop release-proof`        | Check post-release proof across public release channels                        |
| `agentloop npm-status`           | Check npm registry status without publishing                                   |
| `agentloop mcp-server`           | Start the read-only MCP stdio server                                           |
| `agentloop policy ...`           | Read and compare local safety policies                                         |
| `agentloop schemastore`          | Print the config schema catalog entry                                          |
| `agentloop github import`        | Import explicit local GitHub issue or PR JSON                                  |
| `agentloop install-agent <name>` | Add agent-specific instructions                                                |
| `agentloop list-templates`       | List bundled templates                                                         |
| `agentloop completion <shell>`   | Print shell completion scripts                                                 |
| `agentloop version`              | Print the CLI version                                                          |

Clean up finished task contracts after verification and review-readiness evidence:

```bash
agentloop task archive --status done --dry-run
agentloop task archive --status done
```

See [docs/cli-reference.md](docs/cli-reference.md) for command examples, JSON modes, and safety notes.

See [docs/loop-contracts.md](docs/loop-contracts.md) for local loop contracts, readiness gates, token receipts, and dogfood loops.

See [Baseframe Suite Integration v1](docs/integrations/baseframe-suite-v1.md) for the local JSON handoff between ProjScan, AgentLoopKit, and AgentFlight.

Maintainers can run a faster focused sanity set while iterating:

```bash
npm run test:quick
npm run test:integration
```

Run the full suite before release:

```bash
npm run test:release
npm run release-flow
```

`test:quick` runs the fast unit-oriented set. `test:integration` runs slower CLI workflow coverage. `test:release` is the full Vitest suite. `release-flow` runs the local release gate without publishing packages, creating tags, or creating GitHub releases.

## Agent Setup

Install instructions for the agent you use:

```bash
agentloop install-agent codex
agentloop install-agent claude-code
agentloop install-agent cursor
agentloop install-agent opencode
agentloop install-agent gemini-cli
agentloop install-agent github-copilot-cli
agentloop install-agent all
agentloop install-agent all --json --redact-paths
```

AgentLoopKit writes repo-local Markdown instructions. Re-running `install-agent` is safe: existing `.agentloop/agents/<agent>.md` files are skipped so local edits are preserved, while `AGENTS.md` is updated with any missing AgentLoopKit references. Use `--redact-paths` before sharing setup output; it hides local roots in human and JSON output without changing where files are written. When exact third-party config conventions are uncertain, it keeps the output generic instead of pretending to own another tool's setup.

## Safety Model

AgentLoopKit is intentionally boring:

- no postinstall scripts
- no telemetry
- no cloud backend
- no database
- no API keys
- no hidden network calls
- no reading `.env` contents
- no destructive actions during install

Env files are reported by path only. Verification commands run only when you explicitly run `agentloop verify`.

`agentloop ship` reuses current verification evidence by default. Pass `--run-verify` when you want it to run verification as part of the readiness flow. Pass `--github-comment` when CI needs compact Markdown for a pull request comment. AgentLoopKit does not post the comment itself.

`agentloop prepare-pr` groups changed files by review area, including risk-sensitive paths, source, tests, AgentLoop evidence, docs, CI, config, and other files.

`agentloop start` briefs software agents with the active task, decisive preflight state, next safe command, read-first source handles, risk summary, verification freshness, context-budget impact, and source handles. `agentloop context` turns local task, diff, verification, and run evidence into a compact context budget or source-handled pack for software agents. It is read-only and explains what was included, what was omitted, why, and how to expand local source truth. `agentloop guard` adds drift, proof-debt, baseline, and context-budget checks on top of the evidence map. It is read-only unless you explicitly pass `--write-report` or `--write-baseline`. `agentloop explain-diff` shows the evidence map directly. `agentloop resume-pack` packages the same local evidence into the older compact continuation brief with context-budget estimates. They do not run tests, call external APIs, read `.env` contents, post comments, publish packages, create tags, intercept prompts, proxy provider traffic, or change task state.

For narrower evidence history, `agentloop verify --write-run` and `agentloop handoff --write-run` can add their own local run records without changing the default command behavior.

`agentloop status` includes the newest local run ledger entry when `.agentloop/runs/` exists, so agents can see the latest review-readiness or verification evidence without opening every report.
Run ledger output uses safe display paths: `.agentloop/...` for AgentLoopKit artifacts, repo-relative paths for repo files, and filenames for older outside absolute paths.
Use `--redact-paths` with `doctor`, `task list`, `task show`, `task set`, `task status`, `task done`, `task archive`, `task clear`, `status`, `next`, `start`, `review-context`, `context`, `guard`, `explain-diff`, `resume-pack`, `check-gates`, `artifacts`, `report`, `badge`, `runs`, `show-run`, `intent`, `verify`, `summarize`, `handoff`, `ship`, `prepare-pr`, `maintainer-check`, `upgrade-harness`, `ci-summary`, `release-notes`, `schemastore`, `github import`, `install-agent`, `release-check`, or `release-proof` before pasting output into a public issue, PR, or CI log. That mode replaces local root paths with a placeholder. Default JSON output keeps raw paths for scripts unless the redaction flag is passed. `task show` applies redaction to displayed task contract content. `task list`, `artifacts`, `runs`, `show-run`, `intent`, `schemastore`, and `github import` already use repo-relative paths or catalog metadata, and accept the flag for command consistency.
`agentloop review-context --json` gives non-MCP agents one read-only local snapshot with status, active-task risk-note count, compact evidence map, context-budget estimates, gates, policies, artifacts, recent runs, latest ship evidence, and the next action. It omits the full changed-file list by default and points agents to `agentloop context show evidence-map:current` when they need file-level detail.
`agentloop upgrade-harness` is read-only. It tells existing users which generated guidance files need manual review after a CLI upgrade. It does not merge templates or overwrite local edits.
`agentloop schemastore --json` prints the catalog entry for `agentloop.config.json`. Use it when preparing a SchemaStore contribution; the CLI does not submit that contribution for you. `schemastore --redact-paths` is accepted for consistency; catalog values are not local filesystem paths, so output values do not change.
`agentloop github import --issue-json issue.json --pr-json pr.json` imports explicit local GitHub metadata into `.agentloop/github/context.json`. `review-context`, `prepare-pr`, and `maintainer-check` use that local context when it exists. Missing metadata does not block the loop. `github import --redact-paths` is accepted for consistency; metadata paths are already repo-relative, so output values do not change. The CLI does not call GitHub APIs, read tokens, or run `gh`.
`agentloop release-proof` checks post-release evidence for npm, GitHub Releases, GitHub Marketplace, GHCR, and MCP Registry. Use `--only <channel>` to re-check one channel. It can query public metadata or read captured JSON files that you pass explicitly. It does not publish, tag, upload, post comments, or read tokens.
Shell completions include fixed values for task types, task-list status filters, status transitions, the `done` archive status, agent names, policy subcommands, completion shells, artifact types, badge sources, `summarize` and `handoff` formats, and `release-proof --only` channels.

## More Docs

- [Getting started](docs/getting-started.md)
- [CLI reference](docs/cli-reference.md)
- [Upgrading existing repos](docs/upgrading-existing-repos.md)
- [Configuration](docs/configuration.md)
- [Task contracts](docs/task-contracts.md)
- [Research tasks](docs/research.md)
- [AgentLoop Context Contract](docs/context.md)
- [Evidence map and resume packs](docs/evidence-map.md)
- [Verification reports](docs/verification-reports.md)
- [Status and next action](docs/status.md)
- [Gate checks](docs/check-gates.md)
- [HTML reports](docs/html-reports.md)
- [PR summaries and handoffs](docs/pr-summaries.md)
- [Policies](docs/policies.md)
- [SchemaStore support](docs/schemastore.md)
- [GitHub metadata import](docs/github-metadata.md)
- [Real-repo trials](docs/real-repo-trials.md)
- [Release proof](docs/release-proof.md)
- [MCP server](docs/mcp.md)
- [Template and harness upgrades](docs/template-migrations.md)
- [GitHub Actions and Marketplace Action](docs/github-actions.md)
- [Distribution channels](docs/distribution-channels.md)
- [Comparison](docs/comparison.md)

## Examples

See `examples/` for sample generated harnesses and CI recipes:

- [End-to-end workflow](examples/end-to-end/README.md)
- [Bugfix PR](examples/bugfix-pr/README.md)
- [Next.js app](examples/nextjs-app/README.md)
- [Node API](examples/node-api/README.md)
- [Python service](examples/python-service/README.md)
- [Docs-only repo](examples/docs-only/README.md)
- [Empty repo](examples/empty-repo/README.md)
- [GitHub Actions](examples/github-actions/README.md)
- [GitLab CI](examples/gitlab-ci/README.md)
- [Buildkite](examples/buildkite/README.md)
- [Security review](examples/security-review/README.md)
- [Dependency upgrade](examples/dependency-upgrade/README.md)

See [docs/stack-recipes.md](docs/stack-recipes.md) for Next.js, React/Vite, Remix, SvelteKit, Node API, Django, FastAPI, Python, docs-only, empty-repo, and monorepo verification recipes.

## Compared With Plain AGENTS.md

`AGENTS.md` gives instructions. AgentLoopKit adds process artifacts: task contracts, gates, policies, verification reports, PR summaries, and rollback notes.

The result is easier to review because the work produces evidence, not only code.

## Compared With Prompt Collections

Prompt collections help an agent respond better. AgentLoopKit gives the repository a standing workflow that compatible agents can read and follow.

## Compared With Superpowers

Superpowers is a broader agent methodology and skills system. AgentLoopKit focuses on repo-level engineering loops, task contracts, verification evidence, and handoff artifacts.

They can be complementary. You can use AgentLoopKit alongside Superpowers. AgentLoopKit has no affiliation with Superpowers.

## Stability

Starting at 1.0, AgentLoopKit's shipped surface — CLI commands and flags,
`agentloop.config.json`, the MCP tool surface, `--json` output shapes, exit
codes, and the generated harness format — is a committed public contract
under [SemVer](https://semver.org/). Build CI, an agent workflow, or an
integration on it: a 1.x release will not break you.

See [`docs/stability.md`](docs/stability.md) for the full contract and
command reference, and [`docs/versioning.md`](docs/versioning.md) for the
SemVer promise, deprecation policy, and experimental-tier rules.

Upgrading from a pre-1.0 install? Run `agentloop upgrade-harness` to check
your generated files against the current format.

## Contributing

Contributor setup:

```bash
git clone https://github.com/abhiyoheswaran1/agentloopkit
cd agentloopkit
pnpm install
pnpm test
pnpm build
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup and PR expectations.

## License

MIT.
