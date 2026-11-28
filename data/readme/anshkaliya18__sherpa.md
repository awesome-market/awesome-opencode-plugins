# Sherpa

**Build the right thing. Prove it works. Show why it matters.**

Sherpa is a portable Agent Skill and plugin for Claude Code, Codex, Gemini CLI, Qwen Code, OpenCode, and Kilo Code. It mentors hackathon projects from rules and idea selection through planning, implementation, testing, and submission.

```bash
npm install -g sherpa-skill
sherpa install
```

Then in your agent:
```text
/sherpa-suggest
/sherpa-plan
/sherpa-demo
/sherpa-submission
```

The exact invocation depends on the client. OpenCode registers native `/sherpa-*` commands; Claude Code exposes the generated operation skills; Codex discovers Agent Skills without Sherpa slash-command registration. Kilo provides generated workflow commands.

**What you get right away:**
- **One install:** generates client-specific skill and command files for Claude Code, OpenCode, Codex, and Kilo; project state lives in `.sherpa/` and survives restarts and context switches.
- **Evidence-led:** facts vs assumptions, with `UNKNOWN` when information is missing — no invented details.
- **Human approval gates:** Sherpa recommends, never silently picks an idea or writes code without you confirming.
- **Full lifecycle:** idea → plan → build → verify → demo → submission → postmortem.

[![npm version](https://img.shields.io/npm/v/sherpa-skill)](https://www.npmjs.com/package/sherpa-skill)
[![MIT License](https://img.shields.io/badge/license-MIT-244d47.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Anshkaliya18/sherpa)](https://github.com/Anshkaliya18/sherpa/stargazers)
[![Agent files: Claude · Codex · Gemini · Qwen · OpenCode · Kilo](https://img.shields.io/badge/agent%20files-Claude%20%7C%20Codex%20%7C%20Gemini%20%7C%20Qwen-9a4f2e)](AGENT-COMPATIBILITY.md)

![sherpa](docs/public/sherpa.gif)

## Install

The npm package is published as `sherpa-skill` (the name `sherpa` is already taken on npm).

### Option 1: npm (recommended)

```bash
npm install -g sherpa-skill
sherpa install
```

This detects installed Claude Code, OpenCode, Codex, and Kilo CLIs and installs their generated integrations, plus the `sherpa` distribution CLI. Use `--client` to select one. To preview the actual detected targets without writing files:

```bash
sherpa install --dry-run
```

To install only the skill (skip the CLI):

```bash
sherpa install --no-cli
```

To remove:

```bash
sherpa uninstall
```

The npm `sherpa` launcher supports `install`, `migrate`, and `uninstall`, and forwards `update`, `doctor`, `audit`, `clean`, `help`, and `--version` to the bundled management CLI. Management commands require Python 3.

Install with `--global` to call `sherpa` directly. For a local install, prefix commands with `npx sherpa-skill`, for example `npx sherpa-skill doctor`.

Node.js is required to run the npm package. `package.json` does not declare an `engines` field, so no specific Node version is pinned — use a current LTS release.

### Option 2: Other install methods (release installers)

The release installers download a versioned GitHub Releases archive, verify its SHA-256 checksum, and install the skill and CLI:

macOS / Linux:
```bash
curl -fsSL https://github.com/Anshkaliya18/sherpa/releases/latest/download/install.sh | bash
```

Windows PowerShell:
```powershell
irm https://github.com/Anshkaliya18/sherpa/releases/latest/download/install.ps1 | iex
```

The release installer supports Claude Code, OpenCode, Codex, and Kilo through explicit client options and project-local targets. It records managed files for upgrade and uninstall. Filesystem validation is reported separately from live client discovery and runtime execution.

## See it in action

The following is illustrative, not a guaranteed transcript. The slash commands shown are native OpenCode/Kilo entries; Claude and Codex use their discovered skills.

**Before** — a vague team idea:
> "We should build something for campus accessibility. Maybe an app?"

**After** — walking the idea through Sherpa operations:

```text
/sherpa-suggest ideas for campus accessibility
# -> Surfaces candidate ideas with pros/cons, risks, and judging-impact notes.
#    Human picks one; Sherpa never auto-selects.

/sherpa-evaluate the chosen idea
# -> Compares candidates against evidence and criteria, then recommends.

/sherpa-plan
# -> Writes an implementation-ready engineering plan to .sherpa/.
#    Architecture is not auto-approved and no code is written yet.

/sherpa-demo
# -> Produces a judge-oriented demo preparation plan from validated evidence.

/sherpa-submission
# -> Verifies and freezes submission materials without submitting.

/sherpa-status
# -> Shows where you are, what's complete, what's broken, and the risks.
```

Each operation maps to a workflow in `workflows/` and is registered in `commands/manifest.json`. Native command registration depends on the client; Codex receives skills only. See the client matrix for verified capabilities and runtime limits.

## Supported agents

| Agent | Generated integration | Installer support | Runtime status |
|---|---|---:|---|
| Claude Code | Agent Skills; operation skills are separate from command files | Global, project, custom root | Files verified; invocation NOT RUN |
| Codex CLI / Codex app | Agent Skills; no native slash command is claimed | Global, project, custom root | Files verified; invocation NOT RUN |
| OpenCode | Agent Skill plus native commands using `$ARGUMENTS` | Global, project, custom root | Project skill discovery PASS; command execution NOT RUN |
| Kilo Code | Agent Skills plus native workflows | Global, project, custom root | Windows skill discovery observed; workflow execution NOT RUN |
| Gemini CLI | Existing extension files; universal installer does not manage them | Manual/repository integration | NOT VERIFIED |
| Qwen Code | Existing extension files; universal installer does not manage them | Manual/repository integration | NOT VERIFIED |

Details and evidence: [agent compatibility](AGENT-COMPATIBILITY.md).

`scripts/build-distributions.py` builds the shared skill bundle and client-specific entrypoints from root `SKILL.md`, `commands/manifest.json`, and the top-level resource folders. The installer reports filesystem validation separately from actual client discovery and runtime execution. Compatibility claims remain NOT VERIFIED until the current host discovers and runs Sherpa.

Install supported clients with `sherpa install --client auto`, or select `claude`, `opencode`, `codex`, or `kilo`. Use `--scope project --project-dir PATH` for a project install. Gemini CLI and Qwen Code extension installation remains manual and is not reported as supported by the universal installer.

Help us verify: install Sherpa on your agent, run `/sherpa status` and `/sherpa next`, and open an issue with your results.

## Why Sherpa

- **Evidence-led:** facts, assumptions, and unknowns are kept distinct; `UNKNOWN` is used when information is unavailable.
- **Human approval gates:** recommendations never silently choose ideas or approve consequential work — you confirm each step.
- **Project-local notes:** project context and generated records live in `.sherpa/` inside your repo, not in the skill directory.
- **Full lifecycle coverage:** idea selection → planning → implementation → testing/security → demo prep → submission → postmortem.

## Contributing / Community

- [Contributing guide](CONTRIBUTING.md) — pull requests welcome.
- Look for issues labeled **good first issue**.
- [Open an issue](https://github.com/Anshkaliya18/sherpa/issues) for bugs or verification reports.
- [GitHub Discussions](https://github.com/Anshkaliya18/sherpa/discussions) for questions and ideas.

## Documentation

Field guide: https://anshkaliya18.github.io/Sherpa/ · Project references: [installation](INSTALLATION.md) · [commands](COMMANDS.md) · [workflows](WORKFLOWS.md) · [configuration](CONFIGURATION.md) · [architecture](ARCHITECTURE.md) · [security](SECURITY.md) · [migration](MIGRATION.md) · [contributing](CONTRIBUTING.md) · [changelog](CHANGELOG.md).
