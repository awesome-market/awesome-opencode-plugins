# omo-mem

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![opencode plugin](https://img.shields.io/badge/opencode-plugin-blue)](https://opencode.ai)

Your AI forgets everything when the session ends. omo-mem fixes that — permanently, without a cloud service, without a database, without an API key.

## Why omo-mem

Most "AI memory" plugins store memories in proprietary databases, require third-party sync services, or inject bloated context that slows your LLM down. omo-mem is different in three ways:

**Plain markdown files.** Your memory lives in files you can read, edit, grep, and version-control. No black boxes. If the plugin breaks, your memory still exists. If you switch tools, you take it with you.

**Apple Notes sync — zero config.** If you use a Mac, you already have iCloud. omo-mem ships a lightweight daemon that bridges your markdown files to Apple Notes, giving you seamless sync across all your Macs without configuring Syncthing, S3, or anything else.

**No API keys, no cloud, no lock-in.** Works entirely offline. There is no omo-mem server. Your memories never leave your machine (except through iCloud, which you control).

## What it does

omo-mem injects three memory layers into every session automatically:

| File | Purpose |
|------|---------|
| `SOUL.md` | AI identity — behavior principles, work style, non-negotiables |
| `MEMORY.md` | Long-term knowledge — machines, projects, lessons, preferences |
| `memory/YYYY-MM-DD.md` | Daily log — session context, decisions, next-session notes |

The AI gets 6 tools to actively manage its own memory as you work — no manual updates needed.

## Installation

### One-line (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/autosquid/omo-mem/master/install.sh | bash
```

Or clone and run:

```bash
git clone https://github.com/autosquid/omo-mem ~/workspace/omo-mem
cd ~/workspace/omo-mem && ./init.sh
```

> **Custom install path:** `OMO_MEM_DIR=/your/path ./init.sh`

Start opencode in any project. Memory is injected automatically. No `@mention` required.

### Pin a specific version

```bash
OMO_MEM_VERSION=v2.0.0 curl -fsSL https://raw.githubusercontent.com/autosquid/omo-mem/master/install.sh | bash
```

### Agent-driven install

```text
Install and configure omo-mem by following:
https://raw.githubusercontent.com/autosquid/omo-mem/master/docs/install.md
```

## Memory Tools

| Tool | Description |
|------|-------------|
| `memory_list` | List all memory files |
| `memory_read` | Read SOUL, MEMORY, or any daily note |
| `memory_write` | Overwrite a file (SOUL.md is write-protected) |
| `memory_append` | Append to a file without reading first |
| `memory_patch` | Find-and-replace (exact match) |
| `memory_delete_lines` | Delete a line range (1-indexed, inclusive) |

## Cross-Machine Sync (macOS)

`init.sh` installs `scripts/notes-sync.js` as a launchd background service. It syncs your memory files bidirectionally with Apple Notes every 60 seconds.

```bash
tail -f /tmp/omo-mem-sync.log                                         # monitor
launchctl unload ~/Library/LaunchAgents/com.omo-mem.sync.plist        # stop
launchctl load ~/Library/LaunchAgents/com.omo-mem.sync.plist          # start
```

## Release Packages

Each tagged release ships a bundled `omo-mem.js`, `SHA256SUMS`, and `manifest.json`. Verify what you installed:

```bash
shasum -a 256 omo-mem.js  # compare with SHA256SUMS from the same release
```

## Development

After editing `plugin/omo-mem.js`, rebuild and redeploy:

```bash
./scripts/build.sh
```

Requirements: [Bun](https://bun.sh) ≥ 1.0

## Directory Structure

```
~/workspace/omo-mem/
├── SOUL.md             # AI behavior principles (identity)
├── MEMORY.md           # Long-term memory (curated)
├── AGENTS.md           # Memory system rules (injected as project context)
├── init.sh             # Installation script
├── plugin/
│   └── omo-mem.js      # opencode plugin source
├── scripts/
│   ├── build.sh        # Rebuild & redeploy plugin bundle
│   └── notes-sync.js   # Apple Notes ↔ disk bidirectional sync (macOS)
└── memory/             # Daily notes (gitignored — local only)
    └── YYYY-MM-DD.md
```

## Origins

The three-layer file convention (SOUL.md, MEMORY.md, daily notes) was inspired by [OpenClaw](https://github.com/openclaw). The opencode plugin, Apple Notes sync, and tooling here are our own.

## Support

If omo-mem saves you from repeating yourself to your AI, consider [starring the repo](https://github.com/autosquid/omo-mem) — it helps others find it. If you want to go further, [buy me a coffee](https://buymeacoffee.com/autosquid).

## License

MIT — see [LICENSE](LICENSE)
