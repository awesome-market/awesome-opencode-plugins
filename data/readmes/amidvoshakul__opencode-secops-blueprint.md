# OpenCode SecOps Blueprint

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License" />
  <img src="https://img.shields.io/badge/Version-1.0.0-green.svg" alt="Version" />
  <img src="https://img.shields.io/badge/OpenCode-✓-purple.svg" alt="OpenCode Compatible" />
  <img src="https://img.shields.io/badge/Security-OWASP_Agentic_Top_10-red.svg" alt="Security" />
</p>

<p align="center">
  <strong>Enterprise-grade configuration framework to supercharge, discipline, and secure autonomous AI agents inside the OpenCode ecosystem.</strong>
</p>

<p align="center">
  Drop-in <code>.opencode/</code> directory that injects multi-agent pipelines, automatic capability discovery, and strict security guardrails into any development workspace.
</p>

---

## 🚀 Installation

Choose your preferred method. All methods clone the blueprint, copy `.opencode/` to your project, and auto-configure paths.

Run from your project's root directory. If `.opencode/` already exists, you'll be prompted before overwriting.

### Quick Install

```bash
# Node.js / npm (any OS)
npx opencode-setup

# Linux / macOS
curl -fsSL https://raw.githubusercontent.com/AmidVoshakul/opencode-secops-blueprint/main/install.sh | bash

# Windows PowerShell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/AmidVoshakul/opencode-secops-blueprint/main/install.ps1 | Invoke-Expression
```

### Fallback (Python)

Download `install.py` from the repository and run:
```bash
python install.py
```

### Manual Install

```bash
git clone https://github.com/AmidVoshakul/opencode-secops-blueprint.git
cd opencode-secops-blueprint
mkdir -p ../.opencode
cp -r .opencode/* ../.opencode/
cd .. && rm -rf opencode-secops-blueprint
```

Then update `--project-path` in `.opencode/opencode.json` to your project directory.

---

## ⚡ Quick Start

1. **Install the blueprint** (choose one method):
   ```bash
   # Node.js / npm (any OS) — prompts for token if not set
   npx opencode-setup

   # Linux / macOS
   curl -fsSL https://raw.githubusercontent.com/AmidVoshakul/opencode-secops-blueprint/main/install.sh | bash

   # Windows PowerShell
   Invoke-WebRequest -Uri https://raw.githubusercontent.com/AmidVoshakul/opencode-secops-blueprint/main/install.ps1 | Invoke-Expression
   ```
   - The installer automatically configures your GitHub token from `$GITHUB_PERSONAL_ACCESS_TOKEN`
   - If the variable is not set, you'll be prompted to enter it interactively
   - **Never hardcode tokens** — the blueprint uses `__GITHUB_TOKEN__` placeholder in the repository

2. **Install skills** (optional, 1,459+ skills):
   ```bash
   npx antigravity-awesome-skills --path .opencode/skills --category development,backend
   ```
   Browse the full catalog: [agents-awesome-skills](https://github.com/AmidVoshakul/agents-awesome-skills)

3. **Launch OpenCode** in your project:
   ```bash
   opencode
   ```

4. **Run initialization**:
   ```
   /init
   ```

---

## 🔧 Slash Commands

| Command | Description |
|---|---|
| `/init` | Auto-detect tech stack, generate `AGENTS.md` |
| `/doctor-env` | Full environment audit: config, LSP, Git permissions |
| `/onboard` | Deep project reconnaissance: git history, plans, competitors |
| `/architect` | Scaffold new modules following project patterns |
| `/pro-test` | Mutation testing, coverage audit, test generation |
| `/cleaner` | Remove dead code, unused imports, trailing whitespaces |
| `/doctor` | Debug runtime errors via GitHub Issues and web research |
| `/doc-sync` | Synchronize documentation with codebase changes |
| `/git` | Safe atomic commits with secret detection |
| `/review` | Code review focused on bugs, security, performance |
| `/guard` | Adversarial security audit (OWASP Agentic Top 10) |
| `/compare` | Cross-project benchmarking and competitor analysis |
| `/pr-master` | Create feature branch, push to GitHub, open PR |

---

## 🤖 Sub-Agents

Specialized agents run in isolated context windows — they don't pollute your main conversation.

| Agent | Tools | Purpose |
|---|---|---|
| `@security-auditor` | 🔍 readonly | Security audit, OWASP Top 10, CVE scanning |
| `@docs-writer` | ✏️ write+edit | Documentation creation and maintenance |
| `@test-engineer` | 🧪 bash+write+edit | Test writing, coverage, mutation testing |
| `@code-reviewer` | 🔎 readonly | Code review, best practices, performance |

Invoke agents directly with `@agent-name` or through their dedicated commands.

---

## 🔌 MCP Servers

The blueprint configures **12 MCP servers** out of the box:

| Server | Purpose |
|---|---|
| `time` | Temporal context (2026 anchor) |
| `searxng` | Private web search |
| `sequential-thinking` | Complex reasoning |
| `filesystem` | File operations |
| `fetch` | URL content retrieval |
| `chrome-devtools` | Browser automation |
| `playwright_mcp` | E2E testing automation |
| `context7` | Library documentation lookup |
| `memory` | Session knowledge graph |
| `git` | Version control via MCP |
| `code-index` | Deep symbol indexing |
| `github` | PR, issues, repo operations |

All Git operations are protected by `"ask"` permissions — no automatic commits, pushes, or branch switches.

---

## 🛡️ Security

Hardened against **OWASP Agentic Top 10 2026**:

- **Pre-commit secret detection** — scans for hardcoded tokens (GitHub PAT, OpenAI keys, AWS keys, JWT, private keys) before every commit
- **Input sanitization** — all shell parameters validated via `if/fi` guards
- **Skill firewall** — `"*": "allow"` for lazy-loaded skills, explicit allowlist for critical operations
- **Isolated execution** — Python runs via `uv run` in ephemeral environments
- **Zero-trust Git** — all 8 Git operations require explicit user approval

### 🔑 GitHub Token Management

The blueprint uses a **placeholder-based** system to prevent accidental credential exposure:

| State | `opencode.json` value | Status |
|---|---|---|
| Repository (default) | `__GITHUB_TOKEN__`, `__PROJECT_PATH__`, `__FILESYSTEM_PATH__` | ✅ Safe to commit |
| After install | `ghp_...` (real token), `/path/to/project`, `/path/to/filesystem` | ⚠️ Local only, never commit |
| Missing | `__GITHUB_TOKEN__` | ℹ️ Run installer or `/doctor-env` |

**How it works:**
1. Installer detects `$GITHUB_PERSONAL_ACCESS_TOKEN` or prompts for token
2. Validates token via GitHub API (`/user` endpoint)
3. Replaces `__GITHUB_TOKEN__` → real token in local `opencode.json`
4. Pre-commit hook blocks commits containing real tokens

### 📁 Filesystem Path Configuration

The installer prompts for a filesystem root path that the MCP filesystem server will have access to:
- Set `$FILESYSTEM_PATH` environment variable for non-interactive installs
- Or enter the path interactively when prompted
- The path is validated (must exist as a directory) before being configured

### 📁 .gitignore Handling

The installer automatically manages `.gitignore` to protect local config:

- **No `.gitignore` in project** → Creates one from template (covers dependencies, build outputs, IDE, secrets, env files)
- **`.gitignore` exists** → Appends `.opencode/` if not already present

The `.opencode/` directory contains your GitHub token and project-specific skill configuration — it should **never** be committed to version control.

---

## 📄 License

[MIT License](./LICENSE)
