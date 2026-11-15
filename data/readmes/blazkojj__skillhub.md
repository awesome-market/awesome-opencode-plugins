# ⚡ SkillHub

> **The Universal Package Manager & Registry for AI Coding Agents**  
> *"NPM & Homebrew for AI Coding Agent Environments"*

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Tests: 17 Passed](https://img.shields.io/badge/Tests-17%20Passed-brightgreen)](tests/)
[![Skills: 630+](https://img.shields.io/badge/Skills-633%20Verified-teal)](packages/registry-api/src/catalog.js)
[![Agent Targets: 15](https://img.shields.io/badge/Agent%20Targets-15%20Supported-purple)](#-supported-agent-environments)
[![Security Guardrails: 9](https://img.shields.io/badge/Security-9%20Active%20Rules-emerald)](#-security-guardrails--scoring-engine)
[![CI: Node 20/22/24](https://img.shields.io/badge/CI-Node%2020%2F22%2F24%20%7C%20Ubuntu%2FWin%2FMac-blue)](.github/workflows/ci.yml)

**Community:**
[![GitHub Discussions](https://img.shields.io/badge/Discussions-Join%20the%20community!-purple)](https://github.com/Blazkojj/skillhub/discussions)
[![Contributions Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen)](CONTRIBUTING.md)
[![Star This Repo](https://img.shields.io/badge/⭐-Star%20on%20GitHub-yellow)](https://github.com/Blazkojj/skillhub)

---

## ⭐ Show Your Support

If SkillHub saves you time managing AI agent skills, please consider:

1. **⭐ Starring this repository** — helps others discover it!
2. **📢 Sharing on social media** — tag `@AnthropicAI`, `@cursor_ai`, `@opencode`
3. **🐦 Tweet about it**: *"Just discovered @Blazkojj's SkillHub — it's like NPM for AI coding agents! 630+ skills, 15 targets, one command. 🚀"*
4. **📝 Writing a blog post or making a YouTube tutorial**.
5. **🤝 Contributing a skill** — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 💡 What is SkillHub?

**SkillHub** is a universal package manager for AI coding agents (**Claude Code**, **OpenCode**, **Cursor**, **Windsurf**, **RooCode**, **Copilot**, **Zed**, etc.). 

Instead of manually copy-pasting `.cursorrules` or prompt files into different project folders, SkillHub allows developers to:
- Browse and install from **630+ verified AI coding skills** (*ui-ux-pro-max*, *nextjs-15-app-router-pro*, *fastapi-production-pro*, *owasp-top-10-pro-guard*, *clean-architecture-solid-pro*, etc.).
- Auto-adapt skills into native file formats for **15 supported agent environments**.
- Run automated **Security & Prompt Injection Audits** before installing any skill.
- Maintain project dependencies via `skillhub.json` and lockfiles.

---

## 💻 Installation & Setup Tutorial

### Option 1: Global Linking (Recommended for Local Development)
To use `skillhub` globally in any terminal (**Command Prompt**, **PowerShell**, **Git Bash**, **macOS Terminal**, or **Linux**):

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Blazkojj/skillhub.git
   cd skillhub
   ```

2. **Link the package globally:**
   ```bash
   npm link
   ```

3. **Verify installation:**
   ```bash
   skillhub --help
   ```
   Now the `skillhub` command is available everywhere across your system!

---

### Option 2: Run via npx (Zero Installation)
You can run SkillHub directly without global installation:
```bash
npx skillhub
```

---

## 🎮 Interactive TUI Menu Walkthrough

Launch the interactive split-pane TUI menu by typing:
```bash
skillhub
```

### Controls in TUI Browser:
- `↑` / `↓` — Navigate skills with **instant live preview** in the bottom panel.
- `Tab` — Switch category tabs (*Frontend*, *Backend*, *Database*, *DevOps*, *Security*, *Testing*, *Architecture*, *AI/LLM*, *Mobile*).
- `/` — Start instant search filtering by name, tag, or technology.
- `Enter` — Open target selection modal and install to selected agents (**Claude Code**, **OpenCode**, **Cursor**, etc.).
- `q` / `Esc` — Back to previous menu or exit.

---

## 🛠️ CLI Commands Reference

| Command | Description | Example |
|---|---|---|
| `skillhub` | Launch interactive TUI split-pane browser | `skillhub` |
| `skillhub install <name>` | Install a skill to active project agents | `skillhub install ui-ux-pro-max` |
| `skillhub search <query>` | Search the 630+ skills registry catalog | `skillhub search nextjs` |
| `skillhub audit <path>` | Audit SKILL.md for security & injections | `skillhub audit ./SKILL.md` |
| `skillhub list` | List installed skills in active project | `skillhub list` |
| `skillhub targets` | List all 15 supported agent target paths | `skillhub targets` |
| `skillhub init` | Auto-detect agents & create `skillhub.json` | `skillhub init` |
| `skillhub uninstall <name>` | Remove a skill and clean up target files | `skillhub uninstall ui-ux-pro-max` |

---

## 🎯 Supported Agent Environments

| Target ID | Agent Platform | Output File Path |
|---|---|---|
| `claude-code` | **Claude Code CLI** | `.claude/skills/<name>/SKILL.md` |
| `opencode` | **OpenCode CLI / Desktop** | `.opencode/skills/<name>/SKILL.md` |
| `cursor` | **Cursor IDE** | `.cursor/rules/<name>.mdc` |
| `windsurf` | **Windsurf IDE** | `.windsurfrules` (appended) |
| `roocode` | **RooCode / Cline** | `.roo/rules-code/<name>.md` |
| `copilot` | **GitHub Copilot** | `.github/copilot-instructions.md` |
| `continue` | **Continue.dev** | `.continue/skillhub-<name>.yaml` |
| `codeium` | **Codeium** | `.codeium/instructions/<name>.md` |
| `aider` | **Aider CLI** | `.aider/prompts/<name>.md` |
| `zed` | **Zed Editor** | `.zed/skillhub-<name>.md` |
| `void` | **Void Editor** | `.void/skills/<name>.md` |
| `tabnine` | **Tabnine** | `.tabnine/skills/<name>.md` |
| `gemini` | **Gemini Code Assist** | `.gemini/skillhub-<name>.md` |
| `kilo-code` | **Kilo Code** | `.kilocode/rules/<name>.md` |
| `universal` | **Universal Fallback** | `.skills/<name>/SKILL.md` |

---

## 🛡️ Security Guardrails & Scoring Engine

SkillHub evaluates every skill using a multi-dimensional scoring algorithm:
1. **Security & Safety AST Engine (50% weight):**
   - `SEC-001 (Critical):` Destructive root / wildcard deletion (`rm -rf /`)
   - `SEC-002 (Critical):` Unsafe remote shell pipe (`curl | bash`)
   - `SEC-003 (High):` Prompt Injection & safety override attempts
   - `SEC-004 (High):` Hardcoded API Keys / Secrets (OpenAI, AWS, Stripe)
   - `SEC-005 (Medium):` Environment variable exfiltration
   - `SEC-006 (Low):` Obfuscated Base64 shell payloads
   - `SEC-007 (High):` Dynamic arbitrary execution (`eval()`)
   - `SEC-008 (Medium):` Unrestricted exfiltration network beacons
   - `SEC-009 (Low):` Denial-of-service fork bomb loops
2. **Directive Quality & Completeness (35% weight):** Detailed rules, structure, and actionable guidelines.
3. **Cross-Platform Target Coverage (15% weight):** Multi-agent adapter compatibility.

---

## 🌟 How to Make This Project Blow Up on GitHub 🚀

Want to help SkillHub reach **#1 Trending on GitHub**? Follow this battle-tested open-source growth strategy:

### 1. Optimize the Repository Assets
- **Add a Demo GIF / Video Screen Recording**: Record a 15-second terminal GIF showing `skillhub` TUI in action (using [vhs](https://github.com/charmbracelet/vhs) or [asciinema](https://asciinema.org/)) and place it at the top of `README.md`.
- **Add GitHub Topics**: Tag the repository with: `ai`, `claude-code`, `opencode`, `cursor-rules`, `agent-skills`, `cli`, `developer-tools`, `package-manager`, `typescript`.

### 2. Share in AI & Developer Communities
- **Post on Reddit**:
  - `r/LocalLLaMA` — *"We built SkillHub: NPM for AI Coding Agents (Claude Code, OpenCode, Cursor, Windsurf)"*
  - `r/programming` and `r/node` — Show the interactive terminal UI and security scanner.
  - `r/ClaudeAI` and `r/Cursor` — Explain how it eliminates manual `.cursorrules` copy-pasting.
- **Show HN (Hacker News)**: Post as `Show HN: SkillHub – Universal Package Manager for AI Agent Skills`.
- **Post on X (Twitter)**: Tag `@AnthropicAI`, `@cursor_ai`, `@opencode` with a 15s video showing 1-command installation across Claude Code and Cursor.

### 3. Submit to AI Directories & Awesome Lists
- Submit a PR to [Awesome Cursor Rules](https://github.com/PatrickJS/awesome-cursorrules) adding SkillHub as a package manager.
- List on Product Hunt & Hacker News.

---

## 🗺️ Roadmap

### v1.1 (Next)
- [ ] Community skill marketplace (publish your own skills to the registry)
- [ ] `skillhub update` — auto-update all installed skills to latest versions
- [ ] `skillhub lock` — deterministic lockfile generation for reproducible builds

### v1.2
- [ ] Remote registry API at `https://api.skillhub.dev/v1`
- [ ] `skillhub publish` — publish skills directly to the cloud registry
- [ ] Skill versioning with semver resolution and dependency trees

### v1.3+
- [ ] VS Code extension — browse and install skills without leaving the editor
- [ ] AI-powered skill recommendation engine ("suggest skills based on my project")
- [ ] Multi-language skill format (TypeScript, Python, Go configs)

---

## 📄 License

Apache-2.0 License. Created by SkillHub Contributors.
