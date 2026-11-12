<div align="center">

<img src="docs/assets/icon.svg" alt="asset-inventory icon" width="96" height="96">

# Asset Inventory

**Know exactly what your OpenCode setup can actually invoke — every plugin, skill, command, MCP server, agent, and host capability, each with provenance.**

[![License: MIT](docs/assets/badge-license.svg)](LICENSE)
[![OpenCode Skill](docs/assets/badge-opencode.svg)](#compatibility)
[![skills.sh](https://skills.sh/b/sogeisetsu/asset-inventory)](https://skills.sh/sogeisetsu/asset-inventory)

[English](README.md) · [中文](README-ZH.md) · [日本語](readmes/README-JA.md) · [한국어](readmes/README-KO.md) · [Русский](readmes/README-RU.md) · [العربية](readmes/README-AR.md) · [Español](readmes/README-ES.md)

<img src="docs/assets/banner.svg" alt="asset-inventory banner" width="100%">

</div>

**asset-inventory** is an OpenCode skill that inventories your setup in one shot — every plugin, skill, command, MCP server, agent, and outer-app capability on your machine, each with **provenance** (where it came from). For every asset it answers three questions: **what it is, who brought it in, how to use it**. 🎯

## 🚀 Quick start

```
list my plugins
```

Install the skill (one scope), then invoke it — no configuration needed. Just ask in plain language ("list my plugins") and the agent will load it automatically, or name it explicitly. Add a target to cover only part of your setup — mention 'mcp', 'agents', 'hosts', 'skills', 'diff', or 'usage' in your request (plain language like "MCP servers only" works too). See [Targeting](docs/guides/how-it-works.md#targeting) for what each target scans and what it writes.

## 📦 Install

> 🌍 **Recommended: install globally.** One copy to install and update, available in every project.

```sh
git clone https://github.com/sogeisetsu/asset-inventory.git
cd asset-inventory
# copy only SKILL.md + references/ to your skills dir
```

- **Global:** `~/.config/opencode/skills/asset-inventory/`
- **Project-scoped:** `<project-root>/.opencode/skills/asset-inventory/`

### 📥 Install via skills.sh

One-liner via the [skills.sh](https://skills.sh) CLI — it detects your agents (OpenCode, Claude Code, Codex, GitHub Copilot, …) and installs the skill into each:

```sh
npx skills add sogeisetsu/asset-inventory
```

Add `-g` for a global (user-level) install, `-y` to skip prompts, or `--copy` to copy files instead of symlinking.

### 🤖 Install via AI

Send the text below to your AI and it will install the skill for you:

```
Install the OpenCode skill "asset-inventory" from <https://github.com/sogeisetsu/asset-inventory>.

1. First ask me exactly one question: install globally, or into the current project only.
2. Get the repository with `git clone https://github.com/sogeisetsu/asset-inventory.git` — required; do not fall back to a ZIP download (a ZIP from the Releases page may be outdated).
3. Copy only the two runtime items (SKILL.md and references/) into <target>/asset-inventory/, where <target> is the skills root:
   - Global <target>: ~/.config/opencode/skills/ (Windows: $env:USERPROFILE\.config\opencode\skills\)
   - Project-scoped <target>: .opencode/skills/ inside the current project.
   Create <target>/asset-inventory/ if it is missing. Do not copy the README, docs, or scripts.
4. If <target>/asset-inventory/ already exists, overwrite it (that is an update) — do not ask a second time.
5. When done, verify <target>/asset-inventory/SKILL.md exists, and read the installed version from its frontmatter `metadata.version`.
6. Treat the source as read-only and do not modify any skill content. Report only the install location and the version.
```

📖 Full steps (all platforms) + AI auto-install + updating → **[Install & update](docs/guides/install-and-update.md)**

## 📤 What you get

```
your-project-root/
└── output/
    ├── inventory.md         # the 7-table inventory
    ├── usage-guide.md       # "when to use" guide, by scenario & frequency
    └── asset-inventory.json # machine-readable rows (PK: table + name)
```

👀 **See real examples:** 📄 [inventory.md](docs/samples/inventory.md) · 🧭 [usage-guide.md](docs/samples/usage-guide.md) · 🧾 [asset-inventory.json](docs/samples/asset-inventory.json)

## ✨ Highlights

- 🧭 **Provenance** — built into OpenCode, brought by a plugin, created by you, or injected by a host app. A plugin-managed skill is credited to its plugin, never mislabeled "local".
- 🚦 **Five-state labels** — ✅available / ❌disabled / 📦shelf-only / 🚫absent / 🛑broken
- 🔒 **Read-only & masked** — changes no config; masks keys, paths, and private project names by default
- 🖥️ **Host-aware** — binary-scans the app bundle for injected commands that plain grep misses
- 🔀 **Diff mode** — paste the previous JSON and get only additions and removals
- 🌐 **Multilingual output** — the deliverable follows your language (English, Chinese, Japanese, …)

## 📚 Detailed guides

| Guide | What's inside |
|---|---|
| 🧠 [How it works](docs/guides/how-it-works.md) | Core idea, the 7 tables, provenance, the three files |
| 📦 [Install & update](docs/guides/install-and-update.md) | All platforms, AI auto-install, `update.ps1` options |
| 🧭 [Repository & contributing](docs/guides/repository-and-contributing.md) | Which file to read, layout, contributing, versioning |

## 🔗 Links

- 🖥️ **Landing page:** <https://sogeisetsu.github.io/asset-inventory/>
- 🖼️ **Slash commands & usage:** see [How it works](docs/guides/how-it-works.md)
- 📝 **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- 🤝 **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

## ✅ Compatibility

**Scope: this skill is only tested in OpenCode** (including outer apps that wrap OpenCode, such as OpenChamber). It is **not verified in other AI coding assistants** (Claude Code, Cursor, Windsurf, etc.).

Requires [OpenCode](https://opencode.ai) (skills are loaded on-demand via the native `skill` tool).

## 📄 License

MIT — see [LICENSE](LICENSE).
