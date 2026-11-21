# OpenCode Starter 🚀

<div align="center">
  <strong>English</strong> | <a href="README.id.md">Bahasa Indonesia</a> | <a href="README.zh.md">简体中文</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.fr-ca.md">Français (CA)</a> | <a href="README.de.md">Deutsch</a> | <a href="README.fr.md">Français</a> | <a href="README.pt-br.md">Português (BR)</a> | <a href="README.vi.md">Tiếng Việt</a> | <a href="README.pl.md">Polski</a> | <a href="README.ja.md">日本語</a> | <a href="README.ko.md">한국어</a> | <a href="README.es.md">Español</a> | <a href="README.tr.md">Türkçe</a> | <a href="README.it.md">Italiano</a> | <a href="README.ru.md">Русский</a> | <a href="README.uk.md">Українська</a> | <a href="README.nl.md">Nederlands</a> | <a href="README.sv.md">Svenska</a> | <a href="README.ro.md">Română</a>
</div>
<br>

<div align="center">
  <h3><strong>The smartest code assistants need the safest boundaries.</strong></h3>
  <p><strong>A high-performance, modular starter template optimized for the OpenCode.ai agent ecosystem, featuring secure granular permissions and built-in diagnostic controls.</strong></p>

  <p>Stop worrying about AI agents executing destructive terminal commands or leaking private environment variables. Experience safe, high-speed autonomous coding.</p>
</div>

> 📦 Free template by **andiupn** ([kuncimu.com](https://kuncimu.com)) · Licensed under [MIT License](LICENSE)  
> ☕ If useful, [buy me a coffee](https://ko-fi.com/andiupn) · 🚀 Need more features? Try the [PRO version](https://github.com/sponsors/andiupn?frequency=monthly)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/andiupn/opencode-starter)](https://github.com/andiupn/opencode-starter/releases)
[![Ko-Fi](https://img.shields.io/badge/Ko--fi-Support-ff5f5f?logo=ko-fi)](https://ko-fi.com/andiupn)
[![Patreon](https://img.shields.io/badge/Patreon-Support-f96854?logo=patreon)](https://patreon.com/AndiUpn)
[![Trakteer](https://img.shields.io/badge/Trakteer-Support-red?logo=trakteer)](https://trakteer.id/andi_upn/gift)
[![Saweria](https://img.shields.io/badge/Saweria-Support-yellow?logo=saweria)](https://saweria.co/andiupn)

---

Welcome to **OpenCode Starter**, an experimental modular workspace configuration optimized for collaborating with AI Agents using the OpenCode.ai platform. Featuring secure access control guidelines and highly precise division of agent roles, you can build any project faster, safer, and with complete control.

---

## 💡 The Problem: The "Autonomous Risk"
Fully autonomous AI agents are incredibly powerful, but they bring risks. Without boundaries, an agent might run harmful bash commands, accidentally delete systemic configurations, or read/expose your private `.env` files.

---

## ⚡ The Solution: Guarded High-Speed Autonomy

### 1. 🛡️ Granular Permission Safeguards
Pre-configured secure guidelines in `opencode.json` that explicitly deny access to sensitive files (like `.env`), while safely allowing git and grep operations automatically. High speed with zero security anxiety.

### 🤖 2. 5 Modular AI Roles
Get an organized, specialized team of 5 autonomous agents configured directly in `.opencode/agents/`:
- **`code`** — Writing and editing code safely.
- **`research`** — Explores and maps codebase architecture.
- **`debug`** & **`refactor`** — Diagnosing, fixing, and clean optimization.
- **`document`** — Maintaining documentations without code contamination.

### 🌐 3. Built-in Slash Diagnostics
Instant execution commands like `/analyze` to map project structure, `/fix` to scan and fix bugs, and `/explain` to break down complex files in milliseconds.

---

## 📊 LITE vs PRO: The Premium Upgrade

`opencode-starter` is designed to be a clean baseline. For professional monorepos and advanced workflows:

| Feature | 🆓 LITE (Starter) | 💎 PRO (Premium) |
|---|:---:|:---:|
| **Specialized Agents** | 5 (Code, Research, etc.) | 5 (Modular System) |
| **Workflow Skills** | 2 (`coding-conventions`, `testing`) | 15+ (Database, Ops, etc.) |
| **Workspace Structure** | Simple | Status-first Monorepo (`active/`, etc.) |
| **Project Presets** | ❌ | 10 Presets (Next, Laravel, Flutter, etc.) |
| **Ops & Server Sync** | ❌ | ✅ (Docker Compose & Caddyfile ready) |

👉 **[View Full Comparison & Upgrade Guide](COMPARISON.md)**

---

## 📂 Repository Structure

```
your-workspace/
  .opencode/           # OpenCode agent rules, automation skills, and prompts
    agents/            # Instruction directives for 5 AI agents
    skills/            # Coding conventions and testing guides
  .env.example         # Template for environment variables
  .gitignore           # Standard Git ignore file
  AGENTS.md            # Master rules for AI Agents
  opencode.json        # OpenCode permissions, model selection, and command maps
  LICENSE              # Project license (MIT License)
```

---

## 🚀 Quick Start

### 1. Copy and Setup Environment
Copy your project environment variables template:
```bash
cp .env.example .env
```
Open the `.env` file and insert your `GITHUB_TOKEN` to enable repository integrations.

### 2. Begin Agent Collaboration
Launch the OpenCode AI Agent CLI or load the `opencode.json` configuration file in your AI-friendly editor. Utilize the following built-in commands:
- **Project Analysis:** `/analyze`
- **Diagnose & Fix Vulnerabilities:** `/fix`
- **Explain Module:** `/explain [filename]`

---

## 💖 Support This Project (Donations)

If this starter template helps speed up your coding workflow, consider supporting or donating via the following links:
- **Ko-fi:** [ko-fi.com/andiupn](https://ko-fi.com/andiupn)
- **Patreon:** [patreon.com/AndiUpn](https://patreon.com/AndiUpn)
- **Trakteer:** [trakteer.id/andi_upn/gift](https://trakteer.id/andi_upn/gift)
- **Saweria:** [saweria.co/andiupn](https://saweria.co/andiupn)

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more information.
