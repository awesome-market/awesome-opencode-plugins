# ctxray

<p align="center">
  <a href="https://github.com/MairwunNx/ctxray/actions/workflows/ci.yml"><img alt="Build" src="https://img.shields.io/github/actions/workflow/status/MairwunNx/ctxray/ci.yml?branch=master&label=build"></a>
  <img alt="Status: early development" src="https://img.shields.io/badge/status-early%20development-orange">
  <img alt="Bun 1.4" src="https://img.shields.io/badge/Bun-1.4-000000?logo=bun&logoColor=white">
  <img alt="TypeScript 7" src="https://img.shields.io/badge/TypeScript-7-3178C6?logo=typescript&logoColor=white">
  <img alt="Languages: English, Russian" src="https://img.shields.io/badge/languages-en%20%7C%20ru-blue">
  <img alt="Telemetry: none" src="https://img.shields.io/badge/telemetry-none-brightgreen">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/MairwunNx/ctxray"></a>
  <br>
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-D97757?logo=claude&logoColor=white">
  <img alt="Codex" src="https://img.shields.io/badge/Codex-412991">
  <img alt="Cursor" src="https://img.shields.io/badge/Cursor-000000?logo=cursor&logoColor=white">
  <img alt="Gemini CLI" src="https://img.shields.io/badge/Gemini%20CLI-1A73E8?logo=googlegemini&logoColor=white">
  <img alt="OpenCode" src="https://img.shields.io/badge/OpenCode-4B5563">
</p>

🩻 **ctxray** is an X-ray for agent harnesses. It shows what Claude Code, Codex, Cursor, Gemini CLI, or OpenCode loaded into the model: rules, skills, MCP tools, the system prompt, and the tokens each one costs. Then it checks that in CI, so a broken rule never reaches your team.

[Русская версия](https://github.com/MairwunNx/ctxray/blob/master/README.RU.md)

> [!WARNING]
> ctxray is in early development, and nothing is released yet. Until 1.0, minor versions may change the API.

## What you get

- 🔍 **See what the agent loaded.** `ctxray inspect` lists the rules, skills, MCP servers and their tools, commands, and the system prompt your agent works with in this repository.
- 🪙 **Tokens for every piece.** Each rule, skill, and MCP server shows its token count, so you know what fills the context. Estimates are marked ≈, and counts are exact when the model provider counts them.
- ❓ **Why it's there.** Every piece says why it loaded: it's always on, a file path matched, or the model asked for it.
- ✅ **Tests for your agent setup.** `*.ctxray.ts` files read like Bun or Vitest tests: “payment rules load for payment code”, “the context stays under 25k tokens”, “this prompt picks the refunds skill”.
- 🧪 **One test, every agent.** The same test runs against each agent you use. You don't copy it per tool.
- 🎯 **Does the model pick the right skill?** A prompt runs a few dozen times against a real model, and ctxray reports how often the skill loaded, with a confidence interval. Record the answers once, and every merge request replays them for free.
- 📉 **What a merge request changes.** `ctxray diff` compares with the main branch: a new MCP server with 14 tools, a rule that grew by 6k tokens.
- 📋 **Your organisation's rules.** Token limits, banned MCP servers, a required AGENTS.md: checked on every merge request, without calling a model.
- 🏢 **Works in a closed network.** Corporate LLM gateways, proxies, your own CA certificates, and internal npm registries all work.
- 🔒 **Secrets stay out.** API keys, tokens, emails, phone and card numbers are hidden before anything is written to disk.
- 📊 **Reports for people and for CI.** A live view in the terminal, an HTML report, JUnit, Allure, JSON, and a short Markdown summary for the merge request.
- 🌍 **English and Russian.** ctxray picks your system's language, or the one you pass with `--lang`.

## Supported agents

ctxray reads each agent's files without launching it. Where the agent allows it, ctxray can also launch the agent and record its requests to the model, or record a session you run yourself.

| Agent | Reads files | Launches and records | Records your session |
|---|:-:|:-:|:-:|
| Claude Code | ✓ | ✓ | ✓ |
| Codex | ✓ | ✓ | |
| Gemini CLI | ✓ | ✓ | |
| OpenCode | ✓ | ✓ | |
| Cursor CLI | ✓ | experimental | ✓ |
| Cursor (editor) | ✓ | | ✓ |
| Claude Code Desktop | ✓ | | ✓ |

## The Loadout Stack

ctxray checks your agent setup in seven layers, from cheap to expensive. The first three only read files. The rest launch the agent.

| Layer | What it checks |
|---|---|
| L1 Lint | The rule, skill, and config files are valid |
| L2 Policy | The setup follows your organisation's rules |
| L3 Resolve | The right rules apply to the files you work on |
| L4 Assemble | The agent really sent them to the model |
| L5 Wire | The agent adds the right rule when it reads a file or calls a skill |
| L6 Activate | The model picks the right skill for a prompt |
| L7 Scenario | The agent gets the task done the right way |

## Get started

These commands work from the first release on.

1. See what your agent loads:

   ```sh
   bunx @mairwunnx/ctxray inspect
   ```

2. Create a config and an example test with `ctxray init`.
3. Run `ctxray test` locally, then add it to CI.

## Documentation

The [wiki](https://github.com/MairwunNx/ctxray/wiki) holds the manual. It grows with ctxray.

## Related projects

- **[Feature-Action Architecture](https://github.com/MairwunNx/Feature-Action-Architecture)** – the architecture ctxray's code follows.
- **[Allay AI](https://allay.chat)** – an AI helper for Minecraft servers that answers players from their real game.

## Content disclosures

- 🤖 **AI-generated code.** AI agents wrote much of the code.
- 📡 **No telemetry.** ctxray sends nothing about you anywhere. It talks only to the model provider or gateway you set up, and only in tests that launch an agent.
- Free under the MIT license.

> 🫡 Made by Pavel Erokhin (Павел Ерохин), aka mairwunnx.
