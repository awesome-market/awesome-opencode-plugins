# OpenCode Prompt Forge

**Turn rough coding ideas into scoped, verifiable instructions for OpenCode.**

A lightweight, provider-neutral skill and three slash commands by **Asadullah Shafique — Agentic AI Engineer**. No extra service, runtime dependency, or API key is required by this package. OpenCode itself still requires a configured model and may incur usage costs.

Version 0.1.0 is an initial package: structural validation and installer tests are available; live model behavior has not yet been evaluated. No benchmark or cost-reduction claim is made.

## Use it

```text
/forge Add a search box to the existing products page
/forge-review Review this prompt: rebuild the whole app and make it perfect
/forge-debug Login sometimes fails after refreshing the page
```

Commands draft prompts; they do not implement the requested work. When useful, the drafting agent may inspect repository context with read-only tools. Review the output and submit it as a separate implementation task.

## Install

Download and extract this repository, then use Python 3.10 or newer.

Project installation on Windows PowerShell:

```powershell
py scripts/install.py --project "D:\GitHub\your-project"
```

Project installation on Linux, macOS, or WSL:

```bash
python3 scripts/install.py --project /path/to/your-project
```

Global installation:

```bash
python3 scripts/install.py --global
```

The installer previews the destination and refuses to overwrite existing package files. `--force` explicitly permits replacing those files; other configuration remains untouched. It copies only the skill and three commands, not the entire repository. Restart OpenCode after installation and confirm the commands appear when typing `/`.

Alternatively copy `.opencode/skills/prompt-forge` and the three files from `.opencode/commands` into the corresponding directories in your project. Global locations are `~/.config/opencode/skills` and `~/.config/opencode/commands`.

To uninstall, remove only `skills/prompt-forge` and `commands/forge.md`, `commands/forge-review.md`, and `commands/forge-debug.md` from the location you installed into. Do not remove your whole `.opencode` directory.

## Example

Before: “Fix login; sometimes it fails.”

Illustrative output, not a recorded model run:

```text
Goal
Identify and fix the intermittent login failure.

Context
The trigger and root cause are unknown. Inspect repository instructions,
authentication flow, and relevant tests. Separate observations from assumptions.

Scope
Limit changes to the cause and relevant regression coverage. Preserve unrelated work.

Verification
Attempt to reproduce the failure before changing code. Run the appropriate
project checks. Report anything that remains unverified.

Done
Explain the cause, changed files, and verification evidence. If blocked after
two unsuccessful repetitions of the same approach, report the blocker and next option.
```

## How it works

| Stage | Result |
| --- | --- |
| Intent | A specific outcome with unknowns identified |
| Context | Relevant repository facts or explicit placeholders |
| Scope | Clear change boundaries and preserved authorization |
| Verification | Observable acceptance criteria and appropriate checks |
| Output | A copyable prompt for a separate OpenCode task |

The skill loads on demand. Commands explicitly request the skill and use OpenCode's plan agent. They do not override tool permissions. If the skill is denied by your configuration, allow it according to your organization's policy rather than bypassing that policy.

## Validate and evaluate

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

See [the evaluation guide](evals/README.md) and [ten cases](evals/cases.json). These are behavioral evaluation fixtures, not automated proof that an LLM follows the instructions. Record the OpenCode version, model/provider, output, and rubric results for every actual run.

## Contribute

**Contributions welcome:** help test real OpenCode behavior, improve examples, report bugs, or suggest focused enhancements. Start with [open issues](https://github.com/asadullah48/opencode-prompt-forge/issues), comment on a task you want to take, and submit a pull request from your fork. First-time contributors are welcome.


See [CONTRIBUTING.md](CONTRIBUTING.md). Useful contributions include recorded evaluations, clearer examples, and reproducible compatibility fixes. Keep the core skill small and model-neutral.

## Attribution and license

Inspired by the idea of tool-aware prompt generation in [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master). This project's instructions and implementation are independently written; upstream text is not bundled. No affiliation with Prompt Master or OpenCode is implied.

MIT licensed. Official integration references: [OpenCode skills](https://opencode.ai/docs/skills/) and [commands](https://opencode.ai/docs/commands/), checked September 30, 2026.
