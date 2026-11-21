# Joe Skills — OpenCode Bundle

Joe Skills is a complete OpenCode setup with 14 specialist agents, 50+ skills, 13 MCP servers, and a cross-platform installer.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Platforms](#platforms)
- [Agents](#agents)
- [MCP Servers](#mcp-servers)
- [Skills](#skills)
- [Multi-Agent Collaboration](#multi-agent-collaboration)
- [Environment Variables](#environment-variables)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **Multi-Agent Harness** — Orchestrator routes tasks to 13 specialists (UI, UX, Frontend, Backend, Security, MCP, Media, Research, SkillScout, Reviewer, Coder, Planner, Pentest).
- **50+ Skills** — Anthropic skills, video editing, accessibility, testing, performance, and more.
- **13 MCP Servers** — Pexels, Playwright, Semgrep, Snyk, MagicUI, Claude-Mem, Artemis, Context7, Sentry, GitHub (OAuth), Filesystem, Exa, Brave.
- **Cross-Platform Installer** — GUI (Python/Tkinter) + PowerShell + Docker.
- **Goal Management** — Big goals + small goals + auto-review before close.
- **Memory (claude-mem)** — Persistent notes across sessions.
- **Free & Paid Models** — Uses free OpenCode models; supports paid (GPT-5.5, Claude Opus, Gemini Pro).

---

## Quick Start

### Option 1: GUI Installer (Recommended)
1. Download `JoeSkillsInstaller` from [Releases](https://github.com/yousseftallal/-open-code-full-power-/releases).
2. Run `install.bat` (Windows) or `python installer.py` (all platforms).
3. Select components → Start Install.
4. Restart OpenCode.

### Option 2: PowerShell Installer
```powershell
.\install.ps1
```

### Option 3: Docker
```bash
docker-compose up --build
```

### Option 4: Manual
1. Copy `agents/` → `~/.config/opencode/agents/`
2. Copy `skills/` → `~/.config/opencode/skills/`
3. Merge `opencode.jsonc` into `~/.config/opencode/opencode.jsonc`
4. Set environment variables
5. Restart OpenCode

---

## Installation

### Step 1: Install OpenCode
Download from https://opencode.ai/v2/docs/ (Desktop or CLI).

### Step 2: Install Dependencies

The installer auto-detects your OS and installs deps via:
- **Windows:** winget
- **macOS:** brew
- **Linux:** apt

Or run `download_deps.ps1` for direct links.

| Dependency | Windows | macOS | Linux |
|---|---|---|---|
| Python 3.12 | winget | brew | apt |
| Node.js >=20 | winget | brew | apt |
| ffmpeg | winget | brew | apt |
| scrcpy | winget | brew | apt |
| Docker | winget | brew --cask | apt |
| Bun | winget | brew | curl |
| uv | pip | brew | pip |

### Step 3: Copy Files
- `agents/` → `~/.config/opencode/agents/`
- `skills/` → `~/.config/opencode/skills/`

### Step 4: Merge Config
Merge `opencode.jsonc` into your global config.

### Step 5: Set Environment Variables
- `PEXELS_API_KEY` (Pexels)
- `GITHUB_PERSONAL_ACCESS_TOKEN` (GitHub MCP) — or OAuth
- `BRAVE_API_KEY` (Brave Search) — optional
- `EXA_API_KEY` (Exa) — optional
- `LLM_API_KEY` (Strix)
- `STRIX_LLM` (Strix model)
- `GEMINI_API_KEY` / `GOOGLE_API_KEY` (Artemis)
- `OPEN_ROUTER_API_KEY` (Artemis/OpenRouter)

### Step 6: Restart OpenCode
Restart OpenCode Desktop/CLI to load agents, skills, and MCPs.

### Step 7: Verify
- `/mcps` → check connected servers
- Ask: "List available agents and their models"
- Try: "Use ui-designer + frontend-dev + backend-dev to build a login page"

---

## Platforms

### Windows
- Use `install.bat` (double-click) or `python installer.py`.
- winget for deps.
- Docker Desktop for Strix/GitHub OAuth.

### macOS
- Use `python installer.py`.
- brew for deps.
- Docker Desktop for Strix/GitHub OAuth.

### Linux
- Use `python installer.py`.
- apt for deps.
- Docker for Strix/GitHub OAuth.

---

## Agents (Multi-Model Harness)

| Agent | Model | Role |
|---|---|---|
| orchestrator | opencode/beam-free | Router / coordinator |
| planner | opencode/deepseek-v4.1-flash-free | Planning / analysis |
| ui-designer | opencode/glm-5.3-flash-free | UI / visual design |
| ux-researcher | opencode/deepseek-v4.1-flash-free | UX / research |
| frontend-dev | opencode/glm-5.3-flash-free | Frontend code |
| backend-dev | opencode/minimax-m3.1-flash-free | Backend / auth |
| security-auditor | opencode/minimax-m3.1-flash-free | Security audit |
| mcp-integrator | opencode/longcat-2.5-free | MCP / connectivity |
| media-analyst | opencode/gemini-3.5-flash | Images/text/video (vision) |
| web-researcher | opencode/longcat-2.5-free | Web search / assets |
| skill-scout | opencode/deepseek-v4.1-flash-free | Find skills/MCPs |
| reviewer | opencode/mimo-v2.6-flash-free | Code review |
| coder | opencode/glm-5.3-flash-free | Implementation |
| pentest-agent | opencode/minimax-m3.1-flash-free | Strix pentesting |

---

## MCP Servers (13)

| Server | Type | Status |
|---|---|---|
| pexels | local (npx) | configured |
| playwright | local (npx) | configured |
| filesystem | local (npx) | configured |
| context7 | remote | configured |
| sentry | remote (OAuth) | configured |
| github | docker (OAuth) | configured |
| brave-search | local (npx) | disabled (no key) |
| semgrep | local (CLI) | configured |
| snyk | local (CLI) | configured |
| exa | local (npx) | disabled (no key) |
| magicui | local (npx) | configured |
| claude-mem | local (CLI) | configured |
| artemis | local (uv) | configured |

---

## Skills (50+)

### Built-in (OpenCode)
accessibility, browser, build-dashboard, code-review, data-visualization, diagnosing-bugs, frontend-design, performance-optimization, playwright-best-practices, report, universal-erp-flow, verification-before-completion, web-design-guidelines, xlsx-manipulation.

### Joe Skills (custom)
- multi-agent-harness — parallel/context persistence guide
- multi-agent-collaboration — collaborative execution patterns
- opencode-models-guide — free/paid models + connection
- goal-management — big/small goals + auto-review
- auto-review — review before closing goal
- agent-reach — web/social scraping CLI
- free-llm-apis — free LLM providers list
- artemis-mobile — Android automation MCP

### Anthropic Skills (20)
academy-guide, algorithmic-art, brand-guidelines, canvas-design, claude-api, discernment-nudge, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing, xlsx.

### Video Skills (8)
business-short-form-reels, depth-ui-reel, educational-youtube-editor, personal-broll-library, personal-short-form-reels, ranking-format, tutorial-videos, youtube-clips.

---

## Multi-Agent Collaboration

### Patterns
1. **Parallel Review** — 2-3 agents on same task (reviewer + security + ui).
2. **Discuss → Refine → Execute** — planner + frontend + backend discuss, then coder implements.
3. **Divide & Conquer** — frontend UI + backend API + security review in parallel.
4. **Review Loop** — coder → reviewer → coder → reviewer until clean.

### Usage Examples
> "Run reviewer + security-auditor + ui-designer in parallel on this change, then synthesize."

> "Have planner, frontend-dev, backend-dev discuss and implement a login page together."

---

## Environment Variables
- `PEXELS_API_KEY` (Pexels)
- `GITHUB_PERSONAL_ACCESS_TOKEN` (GitHub MCP) — or OAuth
- `BRAVE_API_KEY` (Brave Search) — optional
- `EXA_API_KEY` (Exa) — optional
- `LLM_API_KEY` (Strix)
- `STRIX_LLM` (Strix model)
- `GEMINI_API_KEY` / `GOOGLE_API_KEY` (Artemis)
- `OPEN_ROUTER_API_KEY` (Artemis/OpenRouter)

---

## Dependencies
- Python 3.12 (Strix, Artemis)
- Python 3.11 (agent-reach, video skills)
- Node.js >=20
- Bun (claude-mem)
- uv (Artemis)
- ffmpeg (video)
- scrcpy (Artemis video recording)
- Docker (Strix, GitHub MCP OAuth)
- Android device/emulator (Artemis)

---

## Troubleshooting

### MCP server not connecting
- Run `/mcps` in OpenCode.
- Check `opencode mcp list`.
- Restart OpenCode.

### Agent not found
- Ensure agents are in `~/.config/opencode/agents/`.
- Restart OpenCode.

### Skill not loading
- Ensure skill has `SKILL.md` with `description` in frontmatter.
- Check permissions: `skill` action in `permissions`.

### Installer fails
- Run `python installer.py` directly.
- Check Python version (3.11+).
- Install missing deps manually.

---

## Future Skills
- **Security:** OWASP checklist, SAST rules, dependency scanning.
- **Testing:** Jest, Vitest, Cypress, Playwright advanced.
- **DevOps:** Docker, CI/CD, Kubernetes, Terraform.
- **Data:** SQL, analytics, ETL, dbt.
- **Docs:** API docs, README, changelog, OpenAPI.
- **Mobile:** iOS testing, Flutter, React Native.
- **Design:** Figma, shadcn, Tailwind, design tokens.
- **AI/ML:** RAG, embeddings, fine-tuning.

---

## License
MIT (for Joe Skills bundle). Individual tools have their own licenses.