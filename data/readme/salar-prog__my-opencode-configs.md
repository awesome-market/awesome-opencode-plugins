# OpenCode Dotfiles

[![Skills](https://img.shields.io/badge/skills-158-7C3AED)](./opencode/skills)
[![MCP Servers](https://img.shields.io/badge/mcp_servers-10-0EA5E9)](./opencode/opencode.jsonc)
[![LSPs](https://img.shields.io/badge/LSPs-9-10B981)](./opencode/opencode.jsonc)
[![Linux](https://img.shields.io/badge/OS-Linux-4338CA)](https://www.linux.org/)
[![macOS](https://img.shields.io/badge/OS-macOS-000000)](https://www.apple.com/macos/)
[![WSL](https://img.shields.io/badge/WSL-2-003B00)](https://learn.microsoft.com/windows/wsl/)
[![OpenCode](https://img.shields.io/badge/OpenCode-V2-1.18+-ff6b35)](https://opencode.ai/v2/docs/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Salar--prog-important)](https://github.com/Salar-prog/my-opencode-configs)

> A portable, production-ready [OpenCode](https://opencode.ai) configuration that replicates an entire AI-assisted development environment across machines: **158 skills**, **10 MCP servers**, **9 language servers**, plugins, and TUI preferences — all with scripted bootstrap and agent-driven setup.

## ✨ Features

- ✅ **158 skills** — **superpowers** methodology, full **gamedev-skills pack** (77 skills + router), **hyperframes video suite**, `manage-mcps`/`manage-skills` marketplaces, plus the full `~/.agents/skills/` shared pool (74 skills).
- ✅ **10 MCP servers** — GitHub (OAuth), Playwright, Fetch, Filesystem, Memory, Docker, Kubernetes (disabled), Postgres (disabled), MySQL (disabled), rea-ready.
- ✅ **9 LSPs** — TypeScript, JSON, CSS, HTML, Tailwind, ESLint, Pyright, gopls, rust-analyzer — portable configs via `{env:HOME}`.
- ✅ **One-prompt agent setup** — paste a prompt into any AI agent; it clones the repo and runs the full bootstrap.
- ✅ **Scripted bootstrap** — `curl`-compatible `bootstrap.sh` for non-interactive setup with a full summary report.
- ✅ **Secrets never committed** — OAuth tokens and service passwords are generated per machine; env-var interpolation (`{env:VAR}`) everywhere.
- ✅ **Platform support** — Linux, macOS, and WSL2.

## 🎯 What This Replicates

| Layer | What's Included | Portability |
|-------|-----------------|-------------|
| **Global Server Config** (`opencode.jsonc`) | Plugins, MCP servers, LSPs, permissions | ✅ Fully portable (uses `{env:HOME}`) |
| **CLI/TUI Preferences** (`cli.json`) | Theme, keybindings, diffs, animations | ✅ Fully portable |
| **Skills** (`skills/`) | 158 skills — `manage-mcps`, `manage-skills`, hyperframes* suite, media-use, full gamedev-skills pack (77 + router), plus the entire `~/.agents/skills/` pool: 74 shared skills (superpowers, opencode, claude-code, awesome-design-skills, etc.) | ✅ Symlinked |
| **Plugins** | `superpowers` (git), `@dietrichgebert/ponytail` | ✅ Auto-loaded from config |
| **MCP Servers** | GitHub (OAuth), Playwright, Fetch, Filesystem, Memory, Docker, Kubernetes (disabled), Postgres (disabled), MySQL (disabled) | ✅ Config portable; OAuth re-auth per machine |
| **LSPs** | TypeScript, JSON, CSS, HTML, Tailwind, ESLint, Pyright, gopls, rust-analyzer | ✅ Config portable; binaries installed per machine |

### 🔷 Skills Breakdown

| Category | Count | Highlights |
|----------|-------|------------|
| **gamedev-skills pack** | 78 | Godot ×13, Unity ×8, Unreal ×6, Roblox ×8, three.js ×3, Phaser ×2, Bevy, pygame, PixiJS, Defold, LÖVE, Ebitengine + genres + systems + workflows + router |
| **hyperframes suite** | 4 | Video creation (hyperframes, hyperframes-cli, hyperframes-registry, media-use) |
| **opencode built-ins** | 2 | manage-mcps (MCP marketplace), manage-skills (skills marketplace) |
| **`~/.agents/skills` pool** | 74 | superpowers methodology, debugging, code review, document formats (docx/pdf/pptx/xlsx), mcp-builder, webapp-testing, skill-creator, awesome-design-skills, brand-guidelines, etc. |
| **Total** | **158** | |

### ⚠️ What's NOT Replicated (Intentional)

| Item | Why | How to Handle |
|------|-----|---------------|
| `service.json` | Contains machine-specific service auth token | **Generated fresh per machine** (recommended) |
| `~/.local/share/opencode/` | Sessions, logs, DB, tool output — per-machine state | Never replicate |
| `node_modules/` | `npx` fetches on demand | Not needed |
| **rea MCP** | Requires manual binary install + setup | Documented in [rea Setup](#-rea-manual-setup-per-machine) |
| OAuth tokens (GitHub) | Per-account, per-machine | Sign in via `/mcps` on each machine |
| Symlinks in `~/.config/opencode/skills/` pointing to `~/.claude/skills/` | Local-only cluster links; dereferenced to real files when copied | Replicated as real files (hyperframes* suite, media-use: originally symlinked, now real copies in repo) |
| Project-level `.opencode/` configs | Project-specific, live in project repos | Not in this repo |

---

## 🎯 What This Replicates

| Layer | What's Included | Portability |
|-------|-----------------|-------------|
| **Global Server Config** (`opencode.jsonc`) | Plugins, MCP servers, LSPs, permissions | ✅ Fully portable (uses `{env:HOME}`) |
| **CLI/TUI Preferences** (`cli.json`) | Theme, keybindings, diffs, animations | ✅ Fully portable |
| **Skills** (`skills/`) | 158 skills — `manage-mcps`, `manage-skills`, hyperframes* suite, media-use, full gamedev-skills pack (77 + router), plus the entire `~/.agents/skills/` pool: 74 shared skills (superpowers, opencode, claude-code, awesome-design-skills, etc.) | ✅ Symlinked |
| **Plugins** | `superpowers` (git), `@dietrichgebert/ponytail` | ✅ Auto-loaded from config |
| **MCP Servers** | GitHub (OAuth), Playwright, Fetch, Filesystem, Memory, Docker, Kubernetes (disabled), Postgres (disabled), MySQL (disabled) | ✅ Config portable; OAuth re-auth per machine |
| **LSPs** | TypeScript, JSON, CSS, HTML, Tailwind, ESLint, Pyright, gopls, rust-analyzer | ✅ Config portable; binaries installed per machine |

### ⚠️ What's NOT Replicated (Intentional)

| Item | Why | How to Handle |
|------|-----|---------------|
| `service.json` | Contains machine-specific service auth token | **Generated fresh per machine** (recommended) |
| `~/.local/share/opencode/` | Sessions, logs, DB, tool output — per-machine state | Never replicate |
| `node_modules/` | `npx` fetches on demand | Not needed |
| **rea MCP** | Requires manual binary install + setup | Documented in [rea Setup](#-rea-manual-setup-per-machine) |
| OAuth tokens (GitHub) | Per-account, per-machine | Sign in via `/mcps` on each machine |
| Symlinks in `~/.config/opencode/skills/` pointing to `~/.claude/skills/` | Local-only cluster links; dereferenced to real files when copied | Replicated as real files (hyperframes* suite, media-use: originally symlinked, now real copies in repo) |
| Project-level `.opencode/` configs | Project-specific, live in project repos | Not in this repo |

---

## 🚀 Quick Start (New Machine)

```bash
# 1. Prerequisites (one-time)
#    - Node.js 18+ (nvm recommended: https://github.com/nvm-sh/nvm)
#    - Git
#    - Optional: Go (for gopls), Rust (for rust-analyzer), Python (for pyright)

# 2. Clone and link
git clone <THIS_REPO_URL> ~/dotfiles
rm -rf ~/.config/opencode
ln -s ~/dotfiles/opencode ~/.config/opencode

# 3. Generate service auth token & start background service
opencode service restart
opencode service status
# Should show: {"status":"running","pid":...}

# 4. Launch OpenCode TUI and complete OAuth
opencode
# Inside TUI: Ctrl+P → type "/mcps" → Enter → select "github" → "Sign in"
# Other MCPs (playwright, fetch, filesystem, memory, docker) connect automatically

# 5. Verify everything works
# In TUI: type a prompt → should see tools available
# Check MCPs: /mcps → all should show "connected" (except disabled ones)
```

**Total time:** ~3 minutes (plus OAuth flow).

---

## 📦 Requirements

| Tool | Minimum Version | Required? | Notes |
|------|----------------|-----------|-------|
| Node.js | 22.20+ | ✅ Required | via nvm recommended; LSPs/MCPs fetch via npx |
| Git | any recent | ✅ Required | for cloning and plugin loading |
| OpenCode CLI | V2 (1.18+) | ✅ Required | `npm install -g @opencode-ai/opencode` |
| Go | any recent | Optional | for gopls LSP |
| Rust + rustup | any recent | Optional | for rust-analyzer LSP |
| Python 3 | 3.10+ | Optional | for pyright LSP |
| Docker daemon | any recent | Optional | for docker MCP + container work |
| Docker Desktop | any recent | Mac/Win only | for Docker MCP on macOS/Windows |

---

## 🤖 For AI Agents — One-Prompt Setup

Paste this prompt into any agent to fully bootstrap OpenCode on a new machine. The prompt includes the clone step itself, so no separate repo cloning is needed beforehand:

```
Clone https://github.com/Salar-prog/my-opencode-configs.git to ~/dotfiles.
Then read agents/bootstrap-new-machine.md and execute every step exactly in order, verifying after each.
If something fails, report the error and ask how to fix it — don't skip ahead.
For GitHub OAuth (Step 5), output exact manual instructions and wait for human confirmation.
For any optional tools (like rea), output install commands and wait for human confirmation.
At the end, run the verification checklist (Step 7) and report a summary of successes, failures, and remaining manual steps. Do not skip any steps.
```

No other files or commands are needed beyond what's already in the cloned repo.

---

## ⚡ Quick Script Bootstrap (No Agent Needed)

If you don't want an AI agent doing the setup for you, run this one command after cloning the repo. It handles everything except interactive manual steps (GitHub OAuth, optional rea):

```bash
git clone https://github.com/Salar-prog/my-opencode-configs.git ~/dotfiles && cd ~/dotfiles && ./scripts/bootstrap.sh
```

Or if you have the file already downloaded, just run the script directly. Or use curl to fetch it without cloning first:

```bash
curl -fsSL https://raw.githubusercontent.com/Salar-prog/my-opencode-configs/main/scripts/bootstrap.sh | sh -
```

The script outputs a full summary at the end showing what succeeded, what failed, and which manual steps remain. You'll always need to do two things after running it:

1. **GitHub OAuth** — run `opencode`, then inside the TUI: Ctrl+P → /mcps → github → Sign in
2. **Optional rea** — install rea binary, run `rea mcp`, or add the config block to `~/.config/opencode/opencode.jsonc`:

```jsonc
"rea": {
  "type": "local",
  "command": ["npx", "-y", "@rea/rea"],
  "enabled": true
}
```

---

## 📋 Detailed Step-by-Step Walkthrough

### Step 1: Install Prerequisites

#### Required
```bash
# Node.js 18+ (via nvm - recommended for version management)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc  # or ~/.zshrc
nvm install --lts
nvm use --lts

# Git
# Usually pre-installed; if not:
# Ubuntu/Debian: sudo apt install git
# macOS: xcode-select --install
# Fedora: sudo dnf install git
```

#### Optional (for LSPs)
```bash
# Go (for gopls) - choose one:
#   Ubuntu/Debian: sudo apt install golang-go
#   macOS: brew install go
#   Or: https://go.dev/dl/ (manual)
# After install: go install golang.org/x/tools/gopls@latest

# Rust (for rust-analyzer) - via rustup:
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
rustup component add rust-analyzer

# Python (for pyright) - usually pre-installed
# pip install pyright  # or: npx handles it
```

> **Note:** LSPs will show "disconnected" if their binaries aren't on PATH. This doesn't break OpenCode — you just won't get language features for those languages.

---

### Step 2: Clone and Link Configuration

```bash
# Clone your dotfiles repo (replace with your actual URL)
git clone https://github.com/YOUR_USERNAME/dotfiles.git ~/dotfiles

# Replace any existing OpenCode config with symlink
rm -rf ~/.config/opencode
ln -s ~/dotfiles/opencode ~/.config/opencode

# Verify the symlink
ls -la ~/.config/opencode
# Should show: opencode -> /home/USER/dotfiles/opencode
```

> **Why symlink?** Changes on any machine automatically sync to the repo. `git pull` on other machines picks them up instantly.

---

### Step 3: Generate Service Auth Token

```bash
opencode service restart
# Output: Service restarted successfully

opencode service status
# Expected:
# {
#   "status": "running",
#   "pid": 12345,
#   "port": 4096,
#   "version": "0.x.x"
# }
```

**What this does:** Creates a fresh `~/.config/opencode/service.json` with a unique random password. The background service handles sessions, tool execution, and MCP connections.

> **Do not commit `service.json` to the repo.** Each machine must have its own. If you accidentally commit it, regenerate: `opencode service restart`.

---

### Step 4: Launch & Complete OAuth

```bash
opencode
```

Inside the TUI:

1. Press `Ctrl+P` → type `/mcps` → Enter
2. You'll see a list of MCP servers. Find **github** → press Enter
3. Select **Sign in** → browser opens → authorize the GitHub app
4. Return to TUI — github should now show **Connected**

Other MCPs (playwright, fetch, filesystem, memory, docker) connect automatically on startup. Disabled ones (kubernetes, postgres, mysql) show **Disabled**.

---

### Step 5: Verify Full Functionality

In the OpenCode TUI:

```bash
# Test basic chat
> Hello, what tools do you have available?

# Test filesystem MCP
> List files in my home directory

# Test GitHub MCP (requires OAuth)
> Show my GitHub repositories

# Test playwright MCP
> Take a screenshot of example.com

# Check skills are loaded
> What skills do I have?
# Should mention: manage-mcps, manage-skills, plus game dev skills (router, godot-2d-movement, unity-input-system, etc.)
```

---

## 🔧 Per-Machine Configuration

### Environment Variables (Required)

Add these to your shell profile (`~/.bashrc`, `~/.zshrc`, `~/.config/fish/config.fish`):

```bash
# GitHub MCP (required for GitHub operations)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"  # Personal Access Token with repo scope
# OR use GitHub CLI: gh auth token (if gh is installed)

# Optional: Enable Postgres MCP
# export POSTGRES_URL="postgresql://user:pass@host:5432/db"

# Optional: Enable MySQL MCP
# export MYSQL_HOST="localhost"
# export MYSQL_PORT="3306"
# export MYSQL_USER="root"
# export MYSQL_PASSWORD="password"
# export MYSQL_DATABASE="mydb"

# Optional: Override LSP paths if not in standard locations
# export GOPLS_PATH="/custom/path/gopls"
# export RUST_ANALYZER_PATH="/custom/path/rust-analyzer"
```

> **How to get GitHub token:** GitHub Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token → select `repo` scope.

---

### LSP Binary Paths (Automatic if Standard)

The config uses `{env:HOME}` interpolation for portability:

```jsonc
"gopls": { "command": ["{env:HOME}/go/bin/gopls"] },
"rust-analyzer": { "command": ["{env:HOME}/.cargo/bin/rust-analyzer"] }
```

If you installed Go/Rust in non-standard locations, either:

1. **Symlink to standard location:**
   ```bash
   mkdir -p ~/go/bin
   ln -s /actual/path/to/gopls ~/go/bin/gopls
   ```

2. **Or set env var in shell profile:**
   ```bash
   export GOPLS_PATH="/actual/path/gopls"
   # Then update opencode.jsonc to use {env:GOPLS_PATH} instead
   ```

---

### rea (Reverse Engineering Assistant) — Manual Setup Per Machine

**rea is intentionally NOT in the replicated config** because it requires a native binary install that varies by platform.

#### Option A: Run Ad-Hoc (Recommended for Occasional Use)
```bash
# Install rea (check https://github.com/rea/rea for latest)
# Then run MCP server in a separate terminal/tmux pane:
rea mcp

# In OpenCode, it will auto-discover if running on default port
# Or add temporarily via /mcps → "Add server" → local → command: ["rea", "mcp"]
```

#### Option B: Add Permanently to Your Config
After installing rea, edit `~/.config/opencode/opencode.jsonc` (your local symlinked copy):

```jsonc
"mcp": {
  // ... existing servers ...
  "rea": {
    "type": "local",
    "command": ["npx", "-y", "@rea/rea"],
    "enabled": true
  }
}
```

> **Note:** The repo's `opencode.jsonc` includes a commented template for this.

---

## 🔄 Updating the Config Across Machines

### Making Changes

1. On any machine, edit files in `~/.config/opencode/` (they're symlinked to the repo):
   ```bash
   # Edit global config
   $EDITOR ~/.config/opencode/opencode.jsonc
   
   # Edit CLI prefs
   $EDITOR ~/.config/opencode/cli.json
   ```

2. Changes to `.jsonc`/`.json` files **auto-reload** (no restart needed for most changes).

3. Commit and push:
   ```bash
   cd ~/dotfiles
   git add -A
   git commit -m "Update: describe your change"
   git push
   ```

### Pulling Changes on Other Machines

```bash
cd ~/dotfiles && git pull

# Most changes apply immediately. For structural changes:
opencode service restart
```

---

## 🧪 Troubleshooting

### Service Won't Start

```bash
# Check logs
cat ~/.local/share/opencode/log/opencode.log | grep -i error

# Force restart
opencode service restart

# Nuclear option: stop, remove socket, restart
opencode service stop
rm -f ~/.local/share/opencode/socket
opencode service restart
```

### MCP Shows "Disconnected"

```bash
# 1. Restart service
opencode service restart

# 2. Check /mcps in TUI for specific error

# 3. Common fixes:
# - GitHub: Re-run OAuth (/mcps → github → Sign in)
# - Filesystem: Verify {env:HOME} expands correctly (echo $HOME)
# - Docker: Ensure docker daemon running (docker ps)
# - Playwright: npx playwright install (first run)
```

### LSP Not Connecting

```bash
# Check binary exists
ls -la ~/go/bin/gopls
ls -la ~/.cargo/bin/rust-analyzer

# Install if missing
go install golang.org/x/tools/gopls@latest
rustup component add rust-analyzer

# Verify on PATH
which gopls
which rust-analyzer

# Restart service after install
opencode service restart
```

### Config Not Reloading

```bash
# Force full reload in TUI
/reload

# Or restart service
opencode service restart
```

### Skills Not Loading

```bash
# Verify skills dir exists
ls ~/.config/opencode/skills/

# Should show: manage-mcps/  manage-skills/

# Restart service
opencode service restart
```

### "Permission Denied" on Symlink

```bash
# If ~/.config/opencode exists and is owned by root:
sudo rm -rf ~/.config/opencode
ln -s ~/dotfiles/opencode ~/.config/opencode
```

---

## 📁 Repository Structure

```
dotfiles/
├── opencode/
│   ├── opencode.jsonc          # Global server config (main file)
│   ├── cli.json                # CLI/TUI preferences
│   ├── skills/                  # 158 skills — auto-loaded globally by OpenCode
│   │   ├── manage-mcps/, manage-skills/   # MCP and skills marketplace managers
│   │   ├── hyperframes*, media-use/       # Video creation suite (deref'd from ~/.claude)
│   │   │
│   │   │  ── GAMDEV PACK (78 skills) ──
│   │   ├── router/              # Gamedev dispatcher
│   │   ├── godot-*/ (13), unity-*/ (8), unreal-*/ (6), roblox-*/ (8)
│   │   ├── threejs-*/ (3), phaser-*/ (2), bevy-ecs/, pygame-core/,
│   │   │   pixijs-rendering/, defold-core/, love2d-core/, ebitengine-game/
│   │   ├── genre templates: platformer/, roguelike/, rpg/, fps-shooter/,
│   │   │   card-game/, puzzle/, tower-defense/, survival-crafting/, visual-novel/
│   │   ├── systems: game-ai/, game-feel/, game-ui-ux/, camera-systems/,
│   │   │   procedural-gen/, audio-design/, physics-tuning/, save-systems/, etc.
│   │   └── workflows: prototype-fast/, game-jam/, steam-publish/, itch-publish/
│   │   │
│   │   │  ── ~/.agents/skills POOL (74 skills) ──
│   │   │   Shared cross-agent library, now also replicated for OpenCode.
│   │   ├── superpowers ecosystem: using-superpowers/, brainstorming/,
│   │   │   systematic-debugging/, test-driven-development/, tdd/,
│   │   │   executing-plans/, subagent-driven-development/, etc.
│   │   ├── engineering: code-review/, requesting-code-review/, receiving-code-review/,
│   │   │   diagnosing-bugs/, codebase-design/, domain-modeling/, writing-plans/,
│   │   │   verification-before-completion/, etc.
│   │   ├── document formats: docx/, pdf/, pptx/, xlsx/, internal-comms/,
│   │   │   doc-coauthoring/, research/, retro/, teach/
│   │   ├── platform/infra: mcp-builder/, webapp-testing/, web-artifacts-builder/
│   │   ├── meta: skill-creator/, writing-skills/, writing-for-agents/,
│   │   │   academy-guide/, ask-matt/, claude-api/, claude-handoff/
│   │   └── design/creative: awesome-design-skills/, canvas-design/,
│   │       brand-guidelines/, theme-factory/, frontend-design/,
│   │       slack-gif-creator/, algorithmic-art/
│   └── (no service.json)       # Generated per machine
├── agents/                      # AI agent bootstrap instructions
│   └── bootstrap-new-machine.md  # Self-contained agent checklist for new machines
├── scripts/                     # Automation scripts
│   └── bootstrap.sh             # Non-interactive setup script (skip interactive parts)
├── README.md                    # This file
└── .gitignore                   # Excludes service.json, node_modules, etc.
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `opencode.jsonc` | All server-side config: plugins, MCPs, LSPs, permissions. Uses `{env:VAR}` for portability. |
| `cli.json` | Terminal UI preferences: theme, diffs, tabs, animations, keybindings. |
| `skills/manage-mcps/` | Skill for discovering/adding MCP servers from mcpservers.org. |
| `skills/manage-skills/` | Skill for discovering/installing skills from skills.sh. |
| `skills/hyperframes*/` + `media-use/` | Video creation suite (deref'd from `~/.claude/skills/`). |
| `skills/router/` + `skills/godot-*/` etc. | Full [gamedev-skills pack](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) (77 skills + router) — engine, genre, and cross-engine skills. OpenCode auto-loads them by description. |
| `skills/<name>/` (74 more) | The `~/.agents/skills/` cross-agent pool — superpowers, opencode, claude, awesome-design-skills, etc. Also available to other agents via symlink. |
| `agents/bootstrap-new-machine.md` | Agent-executable bootstrap checklist. |
| `scripts/bootstrap.sh` | Non-interactive automation (clone, symlink, service, LSPs) — exits with summary of what worked/failed and what's left manual. |

---

## 🛡️ Security Notes

| Secret | Where It Lives | Rotation |
|--------|----------------|----------|
| Service auth token | `~/.config/opencode/service.json` (per machine) | `opencode service restart` |
| GitHub token | `GITHUB_TOKEN` env var (per machine) | GitHub Settings → PAT |
| Postgres/MySQL URLs | Env vars (per machine) | Rotate DB credentials |
| rea (if used) | Local binary + config | N/A |

**Never commit:**
- `service.json`
- Actual API keys/tokens in config files (use `{env:VAR}` interpolation)
- `~/.local/share/opencode/` contents

---

## 🎨 Customization Guide

### Adding a New MCP Server

```bash
# Option 1: Use the skill (interactive)
# In OpenCode: "Add an MCP server for PostgreSQL"

# Option 2: Manual edit
$EDITOR ~/.config/opencode/opencode.jsonc
# Add to "mcp" object:
"new-server": {
  "type": "local",
  "command": ["npx", "-y", "@package/mcp-server"],
  "enabled": true,
  "environment": {
    "API_KEY": "{env:MY_API_KEY}"
  }
}
```

Then: `cd ~/dotfiles && git add -A && git commit -m "Add new-server MCP" && git push`

### Adding a New Skill

```bash
# Install from skills.sh
npx skills add owner/repo/skill-name

# This adds to ~/.config/opencode/skills/ (symlinked to repo)
# Commit the new skill directory
```

### Changing Theme/Keybindings

```bash
$EDITOR ~/.config/opencode/cli.json
# Modify theme.name, keybinds, diffs, etc.
# Auto-reloads in TUI
```

---

## 📦 What's Installed by Default

### Plugins (from `opencode.jsonc`)
- **superpowers** — Advanced agent orchestration, planning, debugging tools
- **ponytail** — Lazy senior dev mode: minimal changes, YAGNI enforcement

### MCP Servers
| Server | Type | Purpose | Auth |
|--------|------|---------|------|
| github | local (npx) | GitHub API: repos, issues, PRs, search | OAuth (per machine) |
| playwright | local (npx) | Browser automation, screenshots | None |
| fetch | local (npx) | HTTP fetching, web scraping | None |
| filesystem | local (npx) | File read/write/list in `{env:HOME}` | None |
| memory | local (npx) | Persistent key-value memory | None |
| docker | local (npx) | Docker container/volume/image mgmt | Docker socket |
| kubernetes | local (npx) | K8s cluster management | kubeconfig (disabled) |
| postgres | local (npx) | PostgreSQL queries | `POSTGRES_URL` (disabled) |
| mysql | local (npx) | MySQL queries | `MYSQL_*` env vars (disabled) |

### LSPs (Language Servers)
| Language | Server | Install Command |
|----------|--------|-----------------|
| TypeScript/JS | typescript-language-server | `npm i -g typescript-language-server` (npx handles) |
| JSON/JSONC | vscode-json-language-server | npx |
| CSS/SCSS | vscode-css-language-server | npx |
| HTML | vscode-html-language-server | npx |
| Tailwind | tailwindcss-language-server | npx |
| ESLint | vscode-eslint-language-server | npx |
| Python | pyright | `pip install pyright` or npx |
| Go | gopls | `go install golang.org/x/tools/gopls@latest` |
| Rust | rust-analyzer | `rustup component add rust-analyzer` |

---

## 🌍 Platform-Specific Notes

### Linux (Ubuntu/Debian/Fedora/Arch)
- All tools work natively
- Docker: ensure user in `docker` group (`sudo usermod -aG docker $USER`)
- systemd: OpenCode service runs as user process

### macOS
- Use Homebrew for prerequisites: `brew install node git go rust`
- Docker: Docker Desktop required
- LaunchAgent: not needed; service runs on demand

### WSL2 (Windows)
- Use Linux instructions inside WSL
- Docker: Docker Desktop with WSL integration
- File paths: `{env:HOME}` resolves to `/home/user` (Linux side)
- Windows files: access via `/mnt/c/...` if needed

---

## 🤝 For Collaborators / Other Users

If you want to use this exact setup:

1. **Fork this repo** to your own GitHub/GitLab
2. **Follow Quick Start** above with your fork URL
3. **Customize** by editing `opencode.jsonc` and `cli.json`
4. **Push changes** to your fork
5. **Sync across your machines** with `git pull`

### Minimal Customization Checklist

- [ ] Set `GITHUB_TOKEN` in shell profile
- [ ] Install Go/Rust if you want those LSPs
- [ ] Set up rea if you need reverse engineering
- [ ] Enable postgres/mysql MCPs if needed (set env vars)
- [ ] Adjust `cli.json` theme/keybindings to taste

---

## 📚 References

- **OpenCode Docs:** https://opencode.ai/v2/docs/
- **Configuration Reference:** https://opencode.ai/v2/docs/config
- **MCP Servers:** https://opencode.ai/v2/docs/mcp-servers
- **CLI Settings:** https://opencode.ai/v2/docs/cli/config
- **Skills:** https://opencode.ai/v2/docs/skills
- **Plugins:** https://opencode.ai/v2/docs/build/plugins
- **mcpservers.org:** https://mcpservers.org
- **skills.sh:** https://skills.sh
- **superpowers:** https://github.com/obra/superpowers
- **ponytail:** https://github.com/dietrichgebert/ponytail
- **gamedev-skills pack:** https://github.com/gamedev-skills/awesome-gamedev-agent-skills
- **Agent Skills spec:** https://agentskills.io/specification

---

## 📝 License / Attribution

This configuration is tailored for personal/team use. Individual components have their own licenses:
- OpenCode: Apache-2.0
- superpowers: MIT
- ponytail: MIT
- MCP servers: Various (check each package)

Feel free to fork, adapt, and share.

---

## ✅ Verification Checklist (New Machine)

After setup, verify each item:

- [ ] `opencode service status` → `"status": "running"`
- [ ] `opencode` launches TUI without errors
- [ ] `/mcps` → github shows **Connected** (after OAuth)
- [ ] `/mcps` → playwright, fetch, filesystem, memory, docker show **Connected**
- [ ] `/mcps` → kubernetes, postgres, mysql show **Disabled** (unless enabled)
- [ ] `ls ~/.config/opencode/skills/` → 158 skills (manage-mcps, manage-skills, hyperframes* suite, media-use, gamedev router + 77, ~/.agents pool 74)
- [ ] `ls ~/.config/opencode/skills/ | wc -l` → 158
- [ ] `/mcps` → all 158 skills loaded (visible via `/skills` command)
- [ ] LSPs: TypeScript, JSON, CSS, HTML, Tailwind, ESLint, Pyright show **Connected**
- [ ] LSPs: gopls, rust-analyzer show **Connected** (if Go/Rust installed)
- [ ] File operations work: "List files in ~/"
- [ ] GitHub operations work: "Show my repos"
- [ ] Theme/keybindings from `cli.json` applied

---

## 🔄 Updating Upstream Skills (Maintenance)

The gamedev-skills pack is vendored as a snapshot. To pull upstream updates:

```bash
# 1. Update from upstream
tmp=$(mktemp -d)
git clone --depth 1 https://github.com/gamedev-skills/awesome-gamedev-agent-skills "$tmp/repo"
cp -R "$tmp/repo/router" ~/dotfiles/opencode/skills/router
for d in "$tmp/repo"/skills/*/*/; do cp -R "$d" ~/dotfiles/opencode/skills/$(basename "$d"); done
rm -rf "$tmp"

# 2. Review changes
cd ~/dotfiles && git status

# 3. Commit
git add -A && git commit -m "Update gamedev-skills pack from upstream" && git push
```

Or use the `skills` CLI for the global install (requires Node 22.20+):
```bash
npx skills add gamedev-skills/awesome-gamedev-agent-skills -g --copy
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Fork, make changes to config/skills, and open a PR. All config changes follow the same rule: anything in `~/.config/opencode/` is symlinked to `~/dotfiles/opencode/` on every machine, so edits sync everywhere automatically.

---

## 📬 Support & Community

- 🐛 **Bug reports & feature requests** — [GitHub Issues](https://github.com/Salar-prog/my-opencode-configs/issues)
- 💬 **Questions** — also via Issues; tag with `question`
- ⭐ **Found this useful?** — give it a star and share it with a friend

---

## 📝 License / Attribution

See [LICENSE](LICENSE). This configuration is tailored for personal/team use. Upstream components retain their original licenses:

- OpenCode — Apache-2.0
- [superpowers](https://github.com/obra/superpowers) — MIT
- [ponytail](https://github.com/dietrichgebert/ponytail) — MIT
- [gamedev-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) — MIT
- MCP servers — check each package

Feel free to fork, adapt, and share.

---

**Happy coding! 🎉** — This setup gives you a consistent, powerful AI-assisted development environment everywhere you work.