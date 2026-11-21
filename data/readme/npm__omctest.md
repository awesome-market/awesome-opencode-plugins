<div align="center">

# Oh My Crew

### A role-based agent fork of [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)

Clean, role-descriptive agent names with content-filter-safe system prompts for AI proxy providers.

[![npm version](https://img.shields.io/npm/v/oh-my-crew)](https://www.npmjs.com/package/oh-my-crew)
[![GitHub stars](https://img.shields.io/github/stars/michaelxer/oh-my-crew?style=social)](https://github.com/michaelxer/oh-my-crew)
[![npm downloads](https://img.shields.io/npm/dm/oh-my-crew)](https://www.npmjs.com/package/oh-my-crew)

[English](README.md) | [Bahasa Indonesia](README.id.md)

</div>

---

## User Documentation

- **Start here:** [Beginner-friendly OMC User Guide](docs/guide/user-guide.md)
- **Bahasa Indonesia:** [Panduan Pengguna OMC](docs/guide/user-guide.id.md)
- **Install:** [Installation Guide](docs/guide/installation.md)
- **Advanced reference:** [Complete Features Reference](docs/reference/features.md)

## What is this?

**Oh My Crew** is a fork of [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) (by [@code-yeongyu](https://github.com/code-yeongyu)), based on [oh-my-china](https://github.com/enowdev/oh-my-china) (by [@enowdev](https://github.com/enowdev)), with the following modifications:

1. **System prompts adjusted** to pass through AI proxy content filters
2. **All agents renamed** to clean, role-descriptive crew names -- no political, cultural, or mythological references

### Agent Roster

| Original | Crew Name | Role |
|----------|-----------|------|
| Sisyphus | **Captain** | Main orchestrator. Steers the ship. |
| Hephaestus | **Strategist** | Autonomous deep worker. Plans and executes. |
| Oracle | **Sage** | Read-only consultant. Wisdom without action. |
| Librarian | **Scribe** | External docs search. Finds written knowledge. |
| Explore | **Scout** | Codebase search. Reconnaissance specialist. |
| Atlas | **Foreman** | Todo orchestrator. Keeps work on track. |
| Prometheus | **Architect** | Strategic planner. Designs before building. |
| Metis | **Advisor** | Pre-planning consultant. Identifies risks. |
| Momus | **Auditor** | Plan reviewer/critic. The quality gate. |
| Sisyphus-Junior | **Cadet** | Task executor. Follows orders. |
| Multimodal Looker | **Lookout** | Vision/PDF analysis. Sharp-eyed observer. |

### Content Filter Fix

The phrase `"Powerful AI Agent"` combined with identity override directives triggers some AI proxy content filters. This fork replaces it with softer phrasing that passes through.

### Session Guardian (NEW)

Built-in skill that gives agents **autonomous session lifecycle management**:

| Feature | What It Does |
|---------|-------------|
| **Git Checkpoints** | Auto-commits after each completed task. One commit per task, conventional commit messages. |
| **Context Monitoring** | Tracks context window usage via heuristics + system signals. Knows when to stop. |
| **Smart Handoff Timing** | Never interrupts mid-task. Finishes current work first, then creates handoff. |
| **Structured Handoff Docs** | Generates `HANDOFF_DOC/handoff-NNN.md` with full context for the next session. |
| **Chain Continuity** | Each handoff carries forward decisions and context from ALL previous sessions. |
| **Copy-Paste Resume** | Outputs a ready-to-paste prompt for starting the next session seamlessly. |
| **Credentials Protection** | Manages `.credentials/` folder for API keys, tokens, passwords. Auto-added to `.gitignore`. Agents never hardcode secrets in source code. |

**How it works:**

```text
Agent works -> completes task -> git commit -> checks context level
  |- Context OK -> picks up next task
  \- Context high (65%+) -> creates handoff -> provides resume prompt -> stops
```

The handoff files are saved to `HANDOFF_DOC/` in your project root (auto-added to `.gitignore`). Sensitive credentials go in `.credentials/` (also auto-gitignored). When starting a new session, paste the provided prompt and the agent picks up exactly where it left off.

Session Guardian is **auto-loaded** for Captain and Strategist -- no configuration needed.

---

## Installation

### Prerequisites

- [OpenCode](https://opencode.ai/docs) installed
- [Node.js](https://nodejs.org/) installed (includes npm)

### Step 1: Install Oh My Crew

#### Agent-guided install

Paste this into your LLM agent session. The agent will ask the setup questions in chat, then run the installer with `--no-tui` so the terminal command itself does not open a menu:

```text
Install and configure oh-my-crew by following the instructions here:
https://raw.githubusercontent.com/michaelxer/oh-my-crew/refs/heads/oh-my-crew/docs/guide/installation.md
```

This URL is instructions for the agent, not the installer itself. LLM agents should fetch/read the guide with `curl.exe` on Windows PowerShell or `curl` in POSIX shells:

```bash
curl -fsSL https://raw.githubusercontent.com/michaelxer/oh-my-crew/refs/heads/oh-my-crew/docs/guide/installation.md
```

If you are installing directly as a human, skip the `curl` step and run the terminal wizard below.

If you paste the guide into OpenCode and the agent says the `opencode` command is missing, that usually only means the CLI is not on the agent shell's PATH. Since you are already inside OpenCode, the agent should continue the OMC setup and ask you to restart OpenCode after configuration.

#### Terminal wizard

If you are installing yourself, run this in a real terminal such as PowerShell, Windows Terminal, Terminal, iTerm, or your Linux shell. Do not run the interactive wizard inside an OpenCode agent/chat message, because agents usually cannot display terminal menus. The terminal wizard will ask the setup questions there:

```bash
npx oh-my-crew@latest install
```

or:

```bash
bunx oh-my-crew@latest install
```

If you want an OpenCode agent to install OMC for you, use the agent-guided prompt above instead. The agent will ask questions in chat and then run the non-interactive installer with your answers.

#### Updating existing installs

Already installed? Run the same command again, then fully restart OpenCode:

```bash
npx oh-my-crew@latest install
```

The installer preserves provider settings, removes duplicate legacy plugin entries, rewrites visible crew agent/MCP entries, and refreshes `oh-my-crew.json`. If OpenCode still shows old or missing agents after restart, see the clean update steps in the [OMC User Guide](docs/guide/user-guide.md#updating-omc).

The npm package runs the JS installer directly, so normal `npx`/`bunx` installs do not require any separate Windows, Linux, or macOS binary package.

For scripted setup and full LLM-agent instructions, see [docs/guide/installation.md](docs/guide/installation.md). In this project, `--no-tui` means "no terminal menu"; it does not mean "no questions". The agent can still ask questions in chat and pass your answers as flags.

The installer supports Claude, OpenAI/ChatGPT, Gemini, GitHub Copilot, OpenCode Zen, Z.ai, Kimi, OpenCode Go, Vercel AI Gateway, and custom OpenAI-compatible providers. It asks only the setup questions needed for the provider path you choose.

At the end, the installer writes the OpenCode plugin entry, visible crew agent/MCP entries, `oh-my-crew.json`, and the generated model assignments. Agent-guided installs should verify the config after the installer finishes, then summarize each crew role and the main OMC features: `ultrawork`/`ulw`, Architect/Planner mode, background agents, Session Guardian handoffs, built-in MCPs, LSP/AST-Grep tools, and model fallbacks.

Manual config is also supported, but the installer is recommended because current OpenCode Desktop builds may need the visible agent/MCP entries in addition to the plugin entry.

Edit `~/.config/opencode/opencode.json` (or `opencode.jsonc`) and add `"oh-my-crew"` to the plugin array:

```json
{
  "plugin": ["oh-my-crew"]
}
```

> **Recommended:** Use `"oh-my-crew"` only. It includes everything you need from OMO and avoids dropdown duplication plus sub-agent routing conflicts.
>
> **Important:** If you keep `"oh-my-openagent@latest"` alongside OMC, you may get duplicate dropdown entries and old OMO sub-agent prompts can still win at runtime. For the cleanest setup, remove OMO and run OMC independently.

### Step 2: Restart OpenCode

OpenCode will auto-install the plugin from npm on startup. If the crew agents don't appear, install manually:

```bash
cd ~/.config/opencode
npm install oh-my-crew --save
```

Then restart OpenCode again.

### Step 3: Verify

```bash
opencode
opencode agent list
# You should see Captain, Strategist, Foreman, Sage, etc. in the agent dropdown/list
# Type "ultrawork" to activate all agents
```

### Configure your proxy provider

```json
{
  "provider": {
    "your-proxy": {
      "type": "openai",
      "url": "http://your-proxy:port/v1",
      "key": "your-api-key"
    }
  }
}
```

Anonymous telemetry is enabled by default to track active installations (DAU/WAU/MAU). A single event is sent at most once per UTC day per machine using a hashed installation identifier, never the raw hostname, and PostHog person profiles are not created. Disable with `npx oh-my-crew install --disable-telemetry`, `OMO_SEND_ANONYMOUS_TELEMETRY=0`, or `OMO_DISABLE_POSTHOG=1`. See [Privacy Policy](docs/legal/privacy-policy.md) and [Terms of Service](docs/legal/terms-of-service.md).

---

## Install from source (for developers)

Only needed if you want to modify the code:

```bash
git clone https://github.com/michaelxer/oh-my-crew.git
cd oh-my-crew
bun install
bun run build
bun link
```

Then add `"oh-my-crew"` to your `opencode.json` plugin array.

---

## Features In Short

Oh My Crew keeps the upstream orchestration power and adds OMC-specific naming, install, and session-continuity improvements. Short version:

| Feature | Description |
|---------|-------------|
| **Crew Agents** | Clear role names like Captain, Strategist, Architect, Foreman, Sage, Scout, Scribe, and Lookout. |
| **`ultrawork` / `ulw`** | One keyword tells OMC to understand the task, coordinate agents, execute, and verify until done. |
| **Architect / Planner Mode** | Planning-first workflow for risky or unclear work before files are changed. |
| **Team Mode** | Creates a temporary multi-agent team with shared messages, tasks, and status tracking. |
| **Hyperplan** | Adversarial planning mode where multiple agents challenge assumptions before a final plan is produced. |
| **Background Agents** | Specialists can research, implement, or review in parallel while the main agent continues. |
| **Session Guardian** | Git checkpoints, context monitoring, handoff docs, resume prompts, and credentials protection. |
| **Built-in MCPs** | Web search, Context7 documentation lookup, and grep.app/GitHub code search when available. |
| **LSP + AST-Grep** | IDE-like navigation and structure-aware code search/refactoring for safer edits. |
| **Model Fallbacks** | Agents can continue with configured backup models when a provider or model is unavailable. |
| **Claude Code Compatibility** | Many Claude Code-style hooks, commands, skills, agents, and MCP configs can be reused. |
| **Installer** | Guided setup for OpenCode, model assignments, provider choices, AXR AI, and config backups. |

For a non-technical walkthrough with examples and use cases, read the [OMC User Guide](docs/guide/user-guide.md). For Indonesian users, read [Panduan Pengguna OMC](docs/guide/user-guide.id.md). For exhaustive technical detail, see the [Features Reference](docs/reference/features.md) and the [upstream project](https://github.com/code-yeongyu/oh-my-openagent).

---

## Syncing with Upstream

This is a proper GitHub fork. To pull latest upstream changes:

```bash
git remote add upstream https://github.com/code-yeongyu/oh-my-openagent.git
git fetch upstream
git merge upstream/dev
```

---

## Credits

This project is based on:

- **[oh-my-opencode / oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)** by **[@code-yeongyu](https://github.com/code-yeongyu)** (YeonGyu Kim) -- the original architecture, agents, tools, hooks, and all core features
- **[oh-my-china](https://github.com/enowdev/oh-my-china)** by **[@enowdev](https://github.com/enowdev)** -- the China-compatible fork with content filter fixes that this project builds upon

This fork renames all agents from cultural/political themed names to clean, role-descriptive crew names while preserving all upstream functionality.

- **Original repo**: [github.com/code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)
- **China fork**: [github.com/enowdev/oh-my-china](https://github.com/enowdev/oh-my-china)
- **npm**: [oh-my-crew](https://www.npmjs.com/package/oh-my-crew)
- **npm (original)**: [oh-my-opencode](https://www.npmjs.com/package/oh-my-opencode)
- **License**: [SUL-1.0](LICENSE.md) (inherited from upstream)
- **Discord**: [Join the community](https://discord.gg/PUwSMR9XNk)

---

## Support

If you find Oh My Crew useful, consider:

- Give it a [star on GitHub](https://github.com/michaelxer/oh-my-crew) to help others discover it
- Report issues or suggest features in [GitHub Issues](https://github.com/michaelxer/oh-my-crew/issues)
- Join the [Discord community](https://discord.gg/PUwSMR9XNk) for discussion

---

## License

This fork follows the same [SUL-1.0 license](LICENSE.md) as the upstream project.
See [NOTICE.md](NOTICE.md) for modification details as required by the license.
