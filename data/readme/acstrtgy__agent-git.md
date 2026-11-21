# agent-git

**The operating contract for your personal AI software factory.**

`agent-git` gives coding agents a small, verifiable Git and delivery protocol:
isolate every task, prove the workspace is safe, promote only verified changes,
and reconcile release branches before cleanup.

[![CI](https://github.com/acstrtgy/agent-git/actions/workflows/ci.yml/badge.svg)](https://github.com/acstrtgy/agent-git/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Shell](https://img.shields.io/badge/runtime-Bash-4EAA25.svg)](bin/agent-git)
[![Version](https://img.shields.io/badge/version-1.0.0--beta.1-orange.svg)](CHANGELOG.md)

[Explore the operating contract](https://acstrtgy.github.io/agent-git/) ·
[Read the two-minute quickstart](docs/quickstart.md)

> Your coding agent can write code. `agent-git` teaches it how to ship without
> editing protected branches, reusing the wrong task, or cleaning up too early.

## Why it exists

Coding agents are fast at implementation but delivery is where autonomy often
breaks: work starts on `main`, unrelated changes share a checkout, branch
ownership becomes ambiguous, checks are skipped, or cleanup happens before a
release is safely contained.

`agent-git` solves that coordination problem with an explicit contract that both
humans and agents can inspect. It is intentionally a Bash CLI plus portable
instruction files—not another hosted platform.

## See it in one command

```sh
agent-git act "fix the login regression" --yes
```

```text
AGENT_GIT_WORKSPACE_READY=1
WORKTREE_PATH=/project/.agent-git/worktrees/login-regression
BRANCH=fix/login-regression
BASE_BRANCH=dev
SAFE_TO_EDIT=yes
```

The agent must enter the returned worktree and verify it before editing. If the
state is unsafe, `agent-git` blocks and prints the next safe action.

## The four-part contract

```text
ISOLATE                 VERIFY                 PROMOTE                  RECONCILE
task → own worktree  →  tests + clean diff  →  staging → production  →  main + dev → cleanup
```

1. **Isolate** — one task, one typed branch, one project-local worktree.
2. **Verify** — protected branches, dirty state, ownership, tests, and merge
   feasibility are checked before work or release.
3. **Promote** — task changes move through staging and production using dry-run
   gates and repository policy.
4. **Reconcile** — production is consolidated into the stable and integration
   branches before temporary work is removed.

Read [the branch and release model](docs/branch-model.md) for the rationale and
the optional three-branch profile.

## Quick start

Requirements: Git, Bash, and macOS or Linux. `jq` is recommended; the CLI uses
safe fallbacks for core configuration reads.

```sh
git clone https://github.com/acstrtgy/agent-git.git
cd agent-git
./install.sh --yes
```

Then, inside a project you want to manage:

```sh
agent-git install --yes
```

Restart the coding agent so it reloads the installed contract. From then on,
invoke the workflow explicitly in natural language:

```text
Use agent-git to add the pricing page and prepare a Draft PR for staging.
```

The agent will run `agent-git act "<exact request>" --yes`, work only in the
returned workspace, run configured checks, and follow the repository's release
policy.

## What you get

- natural-language branch classification in English and Italian;
- typed task branches: `feature/`, `fix/`, `refactor/`, `docs/`, `test/`,
  `chore/`, and `rescue/`;
- project-local Git worktrees with explicit ownership;
- protected-branch and dirty-worktree safety gates;
- rescue for work accidentally started in the wrong checkout;
- repository onboarding and migration diagnostics;
- configurable runtime-file copying with production-secret exclusions;
- PR-first delivery instructions for GitHub;
- direct promotion fallback for non-PR repositories;
- dry-run gates for staging, production, consolidation, and cleanup;
- Codex, OpenCode, and Cursor instruction adapters.

## Supported agents

| Agent environment | Integration |
| --- | --- |
| Codex | Global skill plus managed `AGENTS.md` contract |
| OpenCode | Global skill, commands, and guardian agent |
| Cursor | Repository rule generated during onboarding |
| Other coding agents | CLI output and the portable contract in `AGENTS.md` |

The CLI is the source of truth. Adapters make the same safety contract legible
to each agent without changing the underlying workflow.

## Documentation

- [Two-minute quickstart](docs/quickstart.md)
- [Branch and CI/CD model](docs/branch-model.md)
- [Architecture](docs/architecture.md)
- [Development philosophy](docs/philosophy.md)
- [Security model](SECURITY.md)
- [Command reference](docs/reference.md)
- [Contributor guide](CONTRIBUTING.md)
- [Roadmap](docs/roadmap.md)

## Project status

`1.0.0-beta.1` is the first public-review release. The safety contract and
release flow are usable; the beta invites feedback on portability, agent
adapters, and real-world repository policies.

See [the changelog](CHANGELOG.md) and
[open issues](https://github.com/acstrtgy/agent-git/issues).

## Philosophy

`agent-git` does not try to make every decision for an agent. It makes dangerous
or ambiguous decisions explicit, machine-readable, and stoppable.

- Safe state should be provable.
- Destructive behavior should never be the default.
- Repository policy outranks generic automation.
- Humans authorize scope; agents execute the ordinary workflow autonomously.
- A workflow is complete only when the release is verified and reconciled.

## Contributing

Small, focused contributions are welcome. Start with
[`good first issue`](https://github.com/acstrtgy/agent-git/labels/good%20first%20issue)
or read [CONTRIBUTING.md](CONTRIBUTING.md). Security reports should follow
[SECURITY.md](SECURITY.md), not public issues.

## Maintainer

Created and maintained by [Antonio Civita](https://github.com/acstrtgy), focused
on practical operating systems for safe, autonomous agent work.

## License

Licensed under the [Apache License 2.0](LICENSE).
