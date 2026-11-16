# SentinelXPrime

> Stage-aware security skills for Codex, Claude Code, and OpenCode, with explicit compatibility guidance for Cursor and Kilo.

[![Support Surface](https://img.shields.io/badge/Support-Codex%20%7C%20Claude%20Code%20%7C%20OpenCode-111111?style=flat)](#installation)
[![Validation](https://img.shields.io/badge/Validation-static%20%2B%20evals-2ea043?style=flat)](#validation-and-release)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)
[![Stacks](https://img.shields.io/badge/Stacks-ASP.NET%20Core%20%7C%20Spring%20%7C%20Node%20%7C%20Python%20%7C%20Go%20%7C%20Rails%20%7C%20Laravel%20%7C%20Rust-1f6feb?style=flat)](#supported-stacks)

AI coding agents accelerate development but rarely surface security concerns at the right moment. SentinelXPrime fills that gap by embedding stage-aware security skills directly into your coding agent workflow — from planning through release.

The suite helps teams catch missing security requirements during planning, surface scoped concerns during risky implementation work, offer opt-in review help after coding, and propose a practical security check plan before release. It is advisory-first: it improves signal and consistency, but it does not certify a repository as secure, fully reviewed, or production-ready.

## How It Works

SentinelXPrime maps to four development stages, each with a dedicated skill:

1. **Planning** — `sentinelx-plan-gap`: identifies missing security requirements before code is written.
2. **Implementation** — `sentinelx-prime`: surfaces scoped security concerns during risky changes.
3. **Review** — `sentinelx-review-gate`: provides opt-in security review after implementation.
4. **Pre-release** — `sentinelx-test-rig`: proposes a stack-aware security check plan before release or handoff.

Use `using-sentinelx` as the lightweight bootstrap skill when a session needs quick orientation to the suite.

## Supported Stacks

`.NET / ASP.NET Core` · `Java / Spring` · `Node / TypeScript` · `Python` · `Go` · `Ruby on Rails` · `PHP / Laravel` · `Rust`

If the stack is unclear, SentinelXPrime falls back to common web-security guidance and notes that the stack inference is uncertain.

For crypto-sensitive discussions, cross-check [`skills/shared/crypto-guidance.md`](skills/shared/crypto-guidance.md).

## Stage Decision Aid

| Situation | Recommended Skill |
| --- | --- |
| Code is done; "is this implementation safe enough?" | `sentinelx-review-gate` |
| Next step is release or handoff hardening | `sentinelx-test-rig` |
| Stage evidence is weak or contradictory | Stay in `uncertain` mode — keep guidance advisory until the stage becomes clearer |

## Installation

| Platform | Status | Entry Point |
| --- | --- | --- |
| Codex | Supported | [`.codex/INSTALL.md`](.codex/INSTALL.md) and [`docs/README.codex.md`](docs/README.codex.md) |
| Claude Code | Supported | [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) and [`docs/README.claude.md`](docs/README.claude.md) |
| OpenCode | Supported | [`.opencode/INSTALL.md`](.opencode/INSTALL.md) and [`docs/README.opencode.md`](docs/README.opencode.md) |
| Cursor | Compatibility guidance | [`docs/README.cursor.md`](docs/README.cursor.md) |
| Kilo | Compatibility guidance | [`docs/README.kilo.md`](docs/README.kilo.md) |

**Supported** means the repository ships a documented install surface that exists in this repo. **Compatibility guidance** means the repo documents a low-risk way to reuse the instructions and skills without claiming an officially validated plugin path.

Release or handoff claims for supported platforms should be backed by recorded smoke evidence in [`docs/validation/release-readiness.md`](docs/validation/release-readiness.md). Run `node scripts/check-release-readiness.mjs` or the `Release Claim Readiness` workflow before making an external release-ready or handoff claim.

## Quick Start

Start a fresh session and try one of these prompts:

```
Use sentinelx-prime while we plan this new ASP.NET Core feature.
```

```
Use sentinelx-plan-gap to review this Node/TypeScript API design for missing security requirements.
```

```
Use sentinelx-review-gate to run a focused security review on the completed auth changes.
```

```
Use sentinelx-test-rig to propose a stack-aware security check plan for this release handoff.
```

More examples in [`docs/examples/example-prompts.md`](docs/examples/example-prompts.md).

## What's Inside

| Skill | Purpose |
| --- | --- |
| `using-sentinelx` | Lightweight bootstrap and orientation skill |
| `sentinelx-prime` | Orchestrator for stage-aware security guidance |
| `sentinelx-plan-gap` | Planning-stage security gap analysis |
| `sentinelx-review-gate` | Opt-in post-implementation security review |
| `sentinelx-test-rig` | Opt-in security test/check planning before release |
| `shared/*` | Common threat references, finding schema, and stack profiles |

## Philosophy

SentinelXPrime is built on a clear safety model:

- **Advisory-first** — guidance by default, never silent enforcement.
- **No false assurance** — findings state what was checked and what was not.
- **No silent installs** — nothing is installed or mutated without explicit user action.
- **Read-only analysis** — active analysis runs only after explicit user consent.
- **Transparent outputs** — substantial results separate reviewed areas, unreviewed areas, assumptions, and tools run.

## Updating

| Platform | Steps |
| --- | --- |
| Codex | Update the clone used by your install doc, then restart Codex |
| Claude Code | Update the plugin clone and restart the session |
| OpenCode | Update the clone or project copy used by your install path, then restart OpenCode |
| Cursor / Kilo | Refresh any copied docs or rules material from this repo |

See [CHANGELOG.md](CHANGELOG.md) for notable changes between versions.

## Troubleshooting

| Issue | Fix |
| --- | --- |
| Skills not showing up | Confirm the platform-specific install doc was followed exactly; start a fresh session |
| Hook context missing in Claude Code | Verify [`hooks/hooks.json`](hooks/hooks.json) and [`hooks/session-start`](hooks/session-start) are present in the plugin root |
| Legacy prompt names failing | Follow the migration guide at [`docs/migration-from-codex-sentinel.md`](docs/migration-from-codex-sentinel.md) — this repo does not ship old-name aliases |
| Release packaging issues | Build from the SentinelXPrime repo root only, not from a wrapper workspace or nested copy |

## Validation and Release

### Prerequisites

- Node.js 22
- Ruby (for `scripts/static-validation.sh`)
- `codex` CLI on `PATH` (for live eval runs)
- Readable Codex auth at `$CODEX_HOME/auth.json` or `~/.codex/auth.json` (for live eval runs)
- `unzip` plus either `zip` or `ditto` (for release packaging and archive verification)

### Local Verification

```bash
bash scripts/static-validation.sh
node evals/run-sentinelx-prime.mjs --manifest-json
node evals/run-sentinelx-prime.mjs --preflight-only
node evals/run-sentinelx-prime.mjs
node evals/run-sentinelx-prime.mjs --promote-artifacts
bash tests/hooks/test-session-start.sh
node scripts/check-doc-links.mjs
node scripts/check-legacy-names.mjs
```

### Release Packaging

```bash
bash scripts/package-release.sh
SENTINELX_PRIME_FORCE_NO_RSYNC=1 bash scripts/package-release.sh SentinelXPrime-fallback
node scripts/verify-release-archive.mjs dist/SentinelXPrime.zip
node scripts/verify-release-archive.mjs dist/SentinelXPrime-fallback.zip
node scripts/check-release-readiness.mjs
```

Build release archives only from a clean SentinelXPrime repo root. Do not package from wrapper workspaces, nested source trees, or Finder/manual zips. Treat `scripts/package-release.sh` as the canonical release archive flow.

## Migration

See [`docs/migration-from-codex-sentinel.md`](docs/migration-from-codex-sentinel.md) for renamed skills, command changes, archive/env var updates, and breaking changes.

## Contributing

Contributions, feedback, and bug reports are welcome. Please open an issue or submit a pull request.

## License

MIT. See [LICENSE](LICENSE).
