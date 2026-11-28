<p align="center">
  <img src="https://raw.githubusercontent.com/mjmirza/foundry/main/assets/logo.png" alt="Foundry" height="96" />
</p>

<p align="center">The agent skill that makes any AI coding assistant an expert at building agentic tooling.</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-B45309.svg" alt="MIT License" />
  <a href="https://www.npmjs.com/package/@nex8n/foundry"><img src="https://img.shields.io/npm/v/@nex8n/foundry.svg?color=B45309" alt="npm @nex8n/foundry" /></a>
  <img src="https://img.shields.io/badge/tests-39%20checks%20passing-2E7D32.svg" alt="39 checks passing" />
  <img src="https://img.shields.io/badge/format-Agent%20Skill-B45309.svg" alt="Agent Skills format" />
  <img src="https://img.shields.io/badge/works%20with-Claude%20%C2%B7%20Codex%20%C2%B7%20Gemini%20%C2%B7%20Cursor%20%C2%B7%20Cline%20%C2%B7%20Copilot-7C2D12.svg" alt="Works with many assistants" />
</p>

Foundry is one installable, portable agent skill that teaches an AI coding assistant to build, review, and harden agentic tooling at a high standard. Skills, hooks, MCP servers, subagents, slash commands, context engineering, settings, and security. It is the full agentic stack, not one framework, and it works across Claude Code, Codex, Gemini CLI, Cursor, Cline, and Copilot.

It is modeled on the dense, anti mistake style of the SwiftUI Agent Skill, and extended into the accumulated practice of the whole field, mined from the real open issues and pull requests of the top agent tooling repos.

## What you get

The install is one line. Here is what that one line buys you.

- **Your assistant builds it right the first time.** When you ask for a hook, a skill, or an MCP server, it writes one that actually fires, instead of one you debug for an hour because the description never triggers or a shell setting swallowed the block.
- **It catches the mistake while reviewing, yours or the assistant's.** Point a checker at a hook you already have and it tells you the exact line and the rule broken, before that bug reaches a user.
- **You learn it once and it works everywhere.** The same skill installs correctly into Claude Code, Codex, Gemini, Cursor, Cline, and Copilot, so the lesson carries across every tool you use.
- **It is honest about your code.** It flags and reports, it never rewrites your working files on its own, and every rule says when not to apply it.
- **The bugs it prevents are real and specific.** A skill description too vague to ever trigger. A hook whose `set -e` quietly eats its own block. A regex that passes on Linux and fails on a Mac. An MCP server registered in the wrong config file so its tools never appear. Foundry knows each one and the fix.

If you build agent tooling and you are tired of the same class of mistake coming back, that is the time this saves you.

## From install to first win, in three steps

```bash
# 1. install Foundry into your project

[![OpenRoots ORA 2.3](https://openroots.org/badge/ora.svg)](https://openroots.org/licenses/ora/2.3)

npx @nex8n/foundry

# 2. point a checker at a hook you already have
bash foundry/scripts/check-hook.sh path/to/your/hook.sh

# 3. read the finding. it names the file and the rule broken, or says it is clean.
```

That is the whole loop. You went from nothing to a real review of your own code in three commands. Everything below is depth on top of that.

## What is this, in plain terms

When an assistant writes a hook, a skill, or an MCP server, it makes the same handful of mistakes again and again. A skill whose description is too vague to ever trigger. A hook that uses a shell setting which silently swallows its own block. A regex that works on Linux and fails on a Mac. A server registered in the wrong config file so its tools never appear. Foundry encodes those mistakes and their fixes, so the assistant builds the thing correctly the first time and catches the error when reviewing yours.

## What it covers

| Area | What Foundry teaches |
|---|---|
| Skills | Description as a router, the three layer model, frontmatter, paths, packaging |
| Hooks | Events, exit codes, stdin parsing, fail open, the real footguns |
| MCP servers | Registration, tool naming, token cost, supply chain safety |
| Subagents | Context isolation, parallelism, what a subagent does not inherit |
| Commands | Frontmatter, and when a job should be a command, a hook, or a skill |
| Context engineering | Lean context, index do not paste, measure the budget |
| Settings | Merge not overwrite, least privilege, per assistant config |
| Security | Injection defense, egress, secrets, supply chain, no attribution |
| Portability | The install path matrix and translating a capability across assistants |
| Testing and evals | The seven case test and how to prove an artifact works |

## Why an agent skill for this

The same idea that makes a code review skill valuable applies to agent tooling. Most of the value is encoding the mistakes that happen in practice, not restating what the model already knows. Foundry follows five doctrines.

1. Correctness over confidence. Ship only guidance you can ground in the live tool. A confident wrong rule is worse than none.
2. Precision over zeal. Every rule has a leave alone clause. Foundry flags and reports. It does not rewrite your working code on its own.
3. Portability is first class. Write once, install everywhere, with the correct per assistant path.
4. Token budget discipline. Encode edge cases and real mistakes, keep the entry file lean.
5. Lifecycle and clarity. Keep manifest versions in sync and document the layout.

## Install

Install into Claude Code, Codex, Gemini, Cursor, and more with the skills installer.

```bash
npx skills add https://github.com/mjmirza/foundry --skill foundry
```

Or install it straight from npm, which runs the same non destructive installer and drops the skill into the current project.

```bash
npx @nex8n/foundry
```

If `npx` is missing you need Node. On a Mac, `brew install node`.

Claude Code users can add the marketplace and install the plugin directly.

```text
/plugin marketplace add mjmirza/foundry
/plugin install foundry@foundry
```

You can also clone the repository and run `bash foundry/install.sh --project`, which writes the universal `.agents/skills/foundry` copy that Codex, Gemini, Cursor, and Cline read directly, plus the `.claude/skills/foundry` symlink for Claude Code. It never deletes a file you placed there. Copilot reads AGENTS.md at the repo root rather than the skill format, so Foundry reaches Copilot through AGENTS.md. See `foundry/references/portability.md`.

## Using Foundry

In Claude Code.

```text
/foundry
```

In Codex.

```text
$foundry
```

Pass an argument to focus the work.

```text
/foundry review ./.claude/hooks      audit existing hooks for the mistakes
/foundry build hook                  build a new hook to the standard
/foundry harden                      run a security pass
/foundry port codex                  map your tooling to another assistant
```

Or trigger it in natural language.

```text
Use the Foundry skill to check my MCP server setup.
```

## What makes Foundry different

- It ships executable linters, not only prose. `check-skill.sh`, `check-hook.sh`, `check-mcp.sh`, and `check-command.sh` catch the common mistakes in your own tooling.
- It ships markdown hygiene as a first class check. `check-docs.sh` finds broken links, broken heading anchors, missing images, and orphan docs that nothing references. The orphan pass is the docs equivalent of dead code, so a markdown file never sits disconnected from the rest.
- It ships an eval harness that proves the guidance is enforceable. The linters are run against good and bad fixtures and must catch every bad one and pass every good one.
- It ships a correct installer and a doctor. install.sh writes the single universal copy and the per assistant symlink without ever clobbering your files, and doctor checks an install is healthy.
- It is deep tested. An end to end test runs the real install, doctor, and linter commands in sequence and asserts the artifacts they produce, not only that they exit cleanly.
- It carries a surveyed install path matrix across assistants, the most reported and least solved problem in the field. The machine readable map lives at `foundry/data/install-paths.json`.
- It is built from real community requests. The reference files answer the open issues and pull requests of the top agent tooling repos, not a guess at what matters.

## Command, hook, or skill

A frequent question when building agent tooling is which shape to use. Foundry's short answer.

| Use a | when |
|---|---|
| command | the user triggers an action on purpose, like a review or a ship flow |
| hook | a behavior must fire automatically on an event, like a check before a push |
| skill | a body of know how applies when context matches, with references and scripts behind it |

If the user has to remember to run it, it should have been a hook. The full reasoning is in `foundry/references/commands.md`.

## Run the checks

```bash
bash foundry/scripts/check-hook.sh path/to/your/hook.sh
bash foundry/scripts/check-skill.sh path/to/your/skill-dir
bash foundry/scripts/check-mcp.sh path/to/your/mcp-config.json
bash foundry/scripts/check-command.sh path/to/your/command.md
bash foundry/scripts/check-docs.sh .           # markdown hygiene, broken links and orphan docs
bash foundry/scripts/doctor.sh                 # health check this checkout or an install
bash foundry/install.sh --project              # install correctly into the current project
bash foundry/evals/run-evals.sh                # unit checks, prove the linters work
bash foundry/evals/integration.sh              # deep end to end, run the real commands and verify
```

## Built from the community

Foundry's reference content is traced back to real asks across the top repos in Cursor rules, Claude Code resources, MCP, and the AGENTS.md standard. See `docs/COVERAGE.md` for the map from a community request to the Foundry rule that answers it, and `docs/RESEARCH.md` for the repo and gap view.

## Contributing

Contributions of new checks, sharper rules, and fixes are all welcome. Two rules keep the skill useful.

- Respect the token budget. Every line in a reference is loaded into a real session. Keep it dense and cut anything the model already knows.
- Ground every rule. A rule must be true on the live tool. Correctness over confidence. Ship a test or a fixture for anything a linter enforces.

See `CONTRIBUTING.md` for the full bar and `CODE_OF_CONDUCT.md` for the community standard.

## License

Foundry is available under the [MIT License](LICENSE), which permits commercial use, modification, distribution, and private use.
