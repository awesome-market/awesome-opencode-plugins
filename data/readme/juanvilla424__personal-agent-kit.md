# 🧠 Personal Agent Kit

![CI/CD](https://img.shields.io/badge/CI/CD-Pipeline-blue)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.6-blue.svg)
![Build Status](https://github.com/JuanVilla424/personal-agent-kit/actions/workflows/ci.yml/badge.svg?branch=dev)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)

**Personal Agent Kit** (PAK) is a brain and governance layer for Claude Code and OpenCode: a local
memory, guards that run before an action, versioned protocols and a team of personas. It has no
agent loop of its own, and no cloud provider or platform lock-in.

It runs as your own user, from wherever you clone it. It creates no Linux user.

> **Status:** in development. [`docs/prd.md`](docs/prd.md) says what is shipped and what is planned.

## 📚 Table of Contents

- [Features](#-features)
- [Agents](#-agents-persona--opencode)
- [Getting Started](#-getting-started)
  - [Prerequisites](#-prerequisites)
  - [Installation](#-installation)
  - [Language](#️-language)
  - [Pre-Commit Hooks](#-pre-commit-hooks)
  - [Slack Bot](#-slack-bot-optional)
- [Usage](#️-usage)
- [Monitoring Stack](#-monitoring-stack)
- [Contributing](#-contributing)
  - [Creating a New Agent](#️-creating-a-new-agent)
- [Contact](#-contact)
- [License](#-license)

## 🌟 Features

- **AI Agent Team:** Kai (Infrastructure), Raven (Cybersecurity), Iris (Reports) and Elena
  (Database). The full BMAD team joins them with `--with-bmad`.
- **Create Your Own Agents:** with BMAD active, the BMAD Builder module walks you from a one-line
  idea to a working agent (`/bmad:bmb:agents:bmad-builder`).
- **Local Memory Brain:** a local Qdrant collection and `memory_service`, reached through MCP from
  Claude Code and OpenCode alike: one memory that depends on neither engine, consolidated every
  night, with lessons that tie each control to its incident and its expiry. No external service.
- **A Guard Before Every Action:** one rule set judges every shell command, write and web fetch,
  in Claude Code and OpenCode alike: force pushes, deletes, credential exfiltration, downloaded
  code, SSRF and secrets in URLs. Challenges ask the human, and nothing approves a block. Deleting
  is replaced by a reversible quarantine. The rules read each command as bash would run it, so
  quotes, variables, `sudo` and `bash -c` do not hide it. A corpus of 279 commands runs through
  both engines, and `bin/tests/guard-e2e/run.sh` proves the wiring in the real engines with no key.
  On 121 commands written for neither guard, it stops 57 of 91 harmful ones and lets 26 of 30
  harmless ones run; Hermes Agent's checks stop 36 and let 24 run
  ([`docs/guard-benchmark.md`](docs/guard-benchmark.md)). It stops all 89 commands that Hermes
  Agent's own tests require it to block ([`docs/hermes-comparison.md`](docs/hermes-comparison.md)).
  See [`protocols/decision-protocol.md`](protocols/decision-protocol.md).
- **Snapshots Behind the Guard:** every session and every challenge first copies the repository to
  `~/.pak/snapshots`, outside it and without touching its `.git`. `pak snapshot restore` brings
  back what a script deleted, and deletes nothing.
- **Backups of the Brain:** the memory is the only state that exists nowhere else — `pak brain
backup` snapshots every Qdrant collection with generation marks under `~/.pak/backups`, keeps
  the last N, and `pak brain restore --yes` brings a collection back with a full replace.
  `pak brain-health` reports each layer's real state in one run.
- **An Isolated Worker:** `pak task` hands a task to Claude Code in a container with no network but
  the model API, a read-only root and nothing of yours mounted but a clone. It returns a reviewed
  patch and never commits. Every connection it asks for is recorded.
- **Injection Scanning:** memories and the instruction files a session loads are scanned for
  hidden instructions, including HTML comments and invisible or bidirectional characters.
- **A Memory That Finds the Fact:** hybrid search (meaning and exact words), facts that replace
  their older version without deleting it, and a brief injected once at session start. On a
  public synthetic benchmark it finds the right fact at rank 1 for 89 % of the held-out questions,
  against 56 % for a baseline built from Hermes Agent's documented memory, which still wins on
  exact identifiers. See [`docs/memory-benchmark.md`](docs/memory-benchmark.md).
- **One Language Policy:** [`ai18n.yaml`](ai18n.yaml) decides the language of each surface.
- **Report Generation:** Excel and PDF report generators for structured data.
- **Protocols Library:** versioned agent protocols (commit rules, dependency management, token
  management, A2A inter-agent communication) available in three densities: full, ultra
  (agent-load), and compact (fallback).
- **A2A Inter-Agent Protocol:** structured agent-to-agent delegation — inline in IDE party-mode
  (`[A2A → Agent]` blocks) and across sessions through `pak a2a`: `delegate` hands a bounded task
  to a persona (a one-shot OpenCode run answering a Standard Verdict Block), `send` reaches a
  live OpenCode or Claude session, with trust tagging, a hop loop guard, the auto-guard on every
  task, and an append-only registry.
- **OpenCode CLI Integration:** `bin/install-opencode.sh` sets up OpenCode (a custom
  OpenAI-compatible provider of your choice + Z.AI GLM as a second example, LSP servers, bash
  timeout); `bin/opencode/build-config.sh` builds the full `~/.config/opencode/opencode.json`
  (providers, LSP, MCP servers, and every agent) from the repo's `opencode.base.json` +
  `agents/*.prompt`.
- **Voice Output (TTS):** Claude Code's responses and permission prompts are spoken aloud via
  `Stop`/`Notification` hooks — swappable engines (edge-tts by default, self-hosted Chatterbox
  as an offline fallback), a distinct voice per BMAD agent in party-mode, and a personal,
  gitignored persona override. See `docs/stories/tts-hook-persona.md`.
- **Automated Version Control:** automatic version bumping on every version-bump commit via
  pre-commit/pre-push hooks.

## 🤖 Agents (persona ↔ OpenCode)

Each persona is exposed as an **OpenCode agent**, the key defined in
`bin/opencode/opencode.base.json`. Invoke one with `opencode run --agent <key>`. The first four are
always there; the rest need `--with-bmad`, which also makes `bmad-master` the default agent.

| Agent (key)      | Persona        | Role                                |
| ---------------- | -------------- | ----------------------------------- |
| `infra-agent`    | **Kai** 🔧     | Infrastructure (CI/CD, k8s, Docker) |
| `security-agent` | **Raven** 🛡️   | Cybersecurity                       |
| `reports-agent`  | **Iris** 📊    | Reports                             |
| `database`       | **Elena** 🗄️   | Database Architect                  |
| `bmad-master`    | **BMad** 🧙    | Orchestrator                        |
| `architect`      | **Winston** 🏗️ | Architect                           |
| `analyst`        | **Mary** 📊    | Business Analyst                    |
| `pm`             | **John** 📋    | Product Manager                     |
| `sm`             | **Bob** 🏃     | Scrum Master                        |
| `dev`            | **Amelia** 💻  | Developer                           |
| `tea`            | **Murat** 🧪   | Test Architect                      |
| `tech-writer`    | **Paige** 📚   | Tech Writer                         |
| `ux-designer`    | **Sally** 🎨   | UX Designer                         |
| `quick-flow`     | **Barry** 🚀   | Quick Flow Solo Dev                 |

## 🚀 Getting Started

### 📋 Prerequisites

- **Linux with `apt` and systemd.** Ubuntu 24.04 is the tested target.
- **An account with `sudo`.** The installer uses your own account and creates no user.
- **An AI provider:** a Claude account or API key for Claude Code, and/or an OpenAI-compatible
  endpoint for OpenCode.
- **For `pak task`:** Docker (the installer sets it up) and `ANTHROPIC_API_KEY` or
  `CLAUDE_CODE_OAUTH_TOKEN`. See [INSTALL.md](INSTALL.md#-the-autonomous-worker-pak-task).

### 🔨 Installation

```bash
git clone --recurse-submodules https://github.com/JuanVilla424/personal-agent-kit.git
cd personal-agent-kit
bash bin/install.sh
```

Use `--yes` to run without prompts, or `--dry-run` to see the plan first. [INSTALL.md](INSTALL.md)
lists every option and the manual setup. Once installed, `bash bin/update.sh` brings the kit to
the repo's version unattended (ff-only pull, hooks, config rebuild, services restart only when
code moved) — and `bash bin/opencode/guard-smoke.sh` proves the guards really block after it.

### 🗣️ Language

Replies are in English by default. `bash bin/install.sh --language es` changes the replies and the
voice. The repo itself stays in English.

### 🛸 Pre-Commit Hooks

The installer sets them up. They cover Markdown, Python format and lint, YAML, and version control:

```bash
pre-commit run --all-files
```

### 📌 Slack Bot (optional)

```bash
bash bin/install.sh --with-slack
# Fill in local/scripts/notify/.env: SLACK_BOT_TOKEN (xoxb-...), SLACK_APP_TOKEN (xapp-...),
#   SLACK_WEBHOOK_URL, SLACK_CHANNEL_IDS and SLACK_ALLOWED_USERS
```

The bot is closed by default: it answers only the users in `SLACK_ALLOWED_USERS`, in the channels
in `SLACK_CHANNEL_IDS`, and nobody while either is empty.

## 🛠️ Usage

**To use this kit, follow these steps**:

1. **Check every layer:** `pak doctor`.
   - `pak guard "<command>"` judges a command, and `pak memory search "<question>"` searches the
     memory.
   - `pak brain backup` snapshots the memory — the only state that exists nowhere else — and
     `pak brain restore --yes` brings a collection back; `pak brain-health` checks every layer
     in one run.
   - `pak task add "<task>" --repo <path>` followed by `pak task run` hands a task to the
     autonomous worker, which runs it in a container and returns a reviewed patch, never a commit.
   - `pak snapshot list` and `pak snapshot restore <id>` bring back a copy of the repository from
     before a session or a challenge.

2. **Open in the AI tool**
   - Open the `personal-agent-kit` directory in Claude Code or OpenCode.
   - With BMAD active, Party Mode engages the whole team:
     ```
     /bmad:core:workflows:party-mode
     ```

3. **Version Bumping**
   - Add `[patch candidate]`, `[minor candidate]`, or `[major candidate]` to your commit message
     to trigger a version bump.
   - The pre-push hooks automatically bump the version in `pyproject.toml` and
     `.bumpversion.cfg` and amend the commit.

## 📊 Monitoring Stack

Local telemetry for everything the agent does — Claude Code sessions and any of your own
scripts — lives in [`local/monitoring/`](local/monitoring/README.md):

| Service     | Port | Purpose                                      |
| ----------- | ---- | -------------------------------------------- |
| Prometheus  | 9390 | TSDB (scrape)                                |
| Pushgateway | 9391 | One-shot script metrics                      |
| Grafana     | 9392 | Provisioned boards + optional Slack alerting |

Start with `docker compose up -d` inside `local/monitoring/`. Every board follows the canonical
rules in [`local/monitoring/GRAFANA-DASHBOARD-RULES.md`](local/monitoring/GRAFANA-DASHBOARD-RULES.md).
Claude Code session telemetry is registered by `bin/install.sh`.

## 🤝 Contributing

Work happens on the `dev` branch:

1. **Commit your change** as a single commit:

   ```bash
   git commit -m "feat(core): your feature description in lowercase"
   ```

   Scope is always `core`. One commit per task. No emojis in the message.

2. **Run the checks** before pushing:

   ```bash
   .venv/bin/python -m pytest -m "not integration"
   (cd .opencode && bun test)
   .venv/bin/pre-commit run --all-files
   ```

[DEVELOPMENT.md](DEVELOPMENT.md) has the whole development loop and every check, and
[ARCHITECTURE.md](ARCHITECTURE.md) how the parts fit together. Please follow the
[Code of Conduct](CODE_OF_CONDUCT.md) and the [Contribution Guidelines](CONTRIBUTING.md).

### 🛠️ Creating a New Agent

Don't hand-edit persona files. Activate BMAD (`bash bin/install.sh --with-bmad`) and use BMAD Builder:

1. **Load BMad Builder** in your IDE:
   ```
   /bmad:bmb:agents:bmad-builder
   ```
2. Choose **`[CA] Create Agent`** and follow the 11-step guided workflow (brainstorm → persona →
   commands → validation → deploy).
3. If you also want the new agent reachable from OpenCode, add its key to the `agent` block in
   `bin/opencode/opencode.base.json` (copy an existing entry as a template) and re-run
   `bash bin/opencode/build-config.sh`.

## 📫 Contact

For any inquiries or support, please open an issue or contact [r6ty5r296it6tl4eg5m.constant214@passinbox.com](mailto:r6ty5r296it6tl4eg5m.constant214@passinbox.com).

---

## 📜 License

2026 — This is private, proprietary software. All rights reserved. See the [LICENSE](LICENSE)
file included in this repository.
