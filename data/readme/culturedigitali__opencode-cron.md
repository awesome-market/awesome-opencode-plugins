<p align="center">
  <a href="https://culturedigitali.github.io/opencode-cron/">
    <img src="assets/social-preview.png" alt="opencode-cron: Intelligent AI Agent Scheduler for OpenCode" width="100%" style="border-radius: 12px; max-width: 860px; border: 1px solid #2a2a2a;" />
  </a>
</p>

<p align="center">
  <a href="https://culturedigitali.github.io/opencode-cron/">
    <img src="assets/icon.png" alt="opencode-cron logo" width="96" height="96" style="border-radius: 22px;" />
  </a>
</p>

# ⏰ opencode-cron: Intelligent AI Agent Scheduler for OpenCode + Mission Control Web GUI

> **ChatGPT introduced Scheduled Tasks. OpenCode was missing them. opencode-cron brings them to life: supercharged with persistent markdown memory, session binding, and a real-time Mission Control Web GUI.**

> 🌐 **Visit the launch site:** [culturedigitali.github.io/opencode-cron](https://culturedigitali.github.io/opencode-cron/) (available in 10 languages).

Tell OpenCode **“watch competitor releases every 15 minutes”** or **“re-check CI flaky tests every hour”** and it continues autonomously in the exact same chat session. Even after context compact. Even when your terminal or TUI is closed.

[![npm version](https://img.shields.io/npm/v/@culturedigitali/opencode-cron?style=flat-square&color=blue)](https://www.npmjs.com/package/@culturedigitali/opencode-cron)
[![npm downloads](https://img.shields.io/npm/dm/@culturedigitali/opencode-cron?style=flat-square&color=emerald)](https://www.npmjs.com/package/@culturedigitali/opencode-cron)
[![license](https://img.shields.io/npm/l/@culturedigitali/opencode-cron?style=flat-square)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/CultureDigitali/opencode-cron/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/CultureDigitali/opencode-cron/actions/workflows/ci.yml)
[![Bun](https://img.shields.io/badge/bun-%3E%3D1.1-black?style=flat-square&logo=bun)](https://bun.sh)
[![Node](https://img.shields.io/badge/node-%3E%3D20-339933?style=flat-square&logo=node.js&logoColor=white)](https://nodejs.org)
[![i18n](https://img.shields.io/badge/i18n-10%20Languages-indigo?style=flat-square)](http://localhost:4488)
[![GitHub stars](https://img.shields.io/github/stars/CultureDigitali/opencode-cron?style=social)](https://github.com/CultureDigitali/opencode-cron/stargazers)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink?style=flat-square&logo=github-sponsors)](https://github.com/sponsors/CultureDigitali)

---

### 🖥️ Real-Time Mission Control Web GUI

<p align="center">
  <a href="https://culturedigitali.github.io/opencode-cron/">
    <img src="assets/gui-demo.gif" alt="opencode-cron Mission Control Web GUI demo" width="100%" style="max-width: 860px; border-radius: 8px; border: 1px solid #333333;" />
  </a>
</p>
<p align="center">
  <em>Mission Control Web GUI: live worker pool monitoring, 1-click burst mode, interactive DAG pipeline modal, and real-time execution streaming.</em><br>
  ▶️ <a href="assets/gui-demo.mp4"><strong>Watch Web GUI HD Demo (MP4)</strong></a> &bull; 🌐 <a href="https://culturedigitali.github.io/opencode-cron/"><strong>Visit Launch Site</strong></a>
</p>

### ⚡ Autonomous Terminal Daemon Walkthrough

<p align="center">
  <a href="https://culturedigitali.github.io/opencode-cron/">
    <img src="assets/demo.gif" alt="opencode-cron live autonomous terminal execution demo" width="100%" style="max-width: 860px; border-radius: 8px; border: 1px solid #333333;" />
  </a>
</p>
<p align="center">
  <em>Autonomous CLI daemon walkthrough: launchd setup, session binding, DAG chain, and live daemon execution.</em><br>
  ▶️ <a href="assets/demo.mp4"><strong>Watch Terminal Daemon HD Demo (MP4)</strong></a> &bull; 🌐 <a href="https://culturedigitali.github.io/opencode-cron/"><strong>Visit Launch Site</strong></a>
</p>

---

### ⭐ If this saves you open tabs, background scripts, and burned tokens, consider starring the repo and sponsoring the project! It helps AI engineers discover true agent scheduling.

---

## 🚀 Why opencode-cron?

Traditional cron is **blind**: it runs an isolated shell script, forgets previous executions, loses conversational context, and can burn hundreds of dollars in looping API tokens.

**opencode-cron is an intelligent AI Agent Scheduler:**

* 🔄 **Same Conversation, Every Tick:** It re-prompts the **same `sessionID`** with full conversation history, not a detached CLI call.
* 🧠 **Persistent Markdown Memory:** Survives context compaction, restarts, and reboots. Tracks `seenHashes` to prevent repetitive notifications.
* 🖥️ **Mission Control Web GUI:** Sleek dark-mode dashboard at `http://localhost:4488` with live SQLite chat streaming, active job monitors, and instant controls.
* 🪟 **Cross-Platform Desktop App & System Tray:** Native installable packages for **macOS (.dmg)**, **Windows (.exe)**, and **Linux (.AppImage, .deb)** with a live system tray icon showing real-time OpenCode connection and active cron status.
* ⚡ **1-Click "Imposta Cron" Binding:** Bind an automated recurring schedule directly to any conversation session with visual schedule previews.
* 📊 **Execution Timeline & Diagnostics (`/runs`):** Real-time visibility into every tick: duration, status, exit codes, trigger source, and error logs.
* ⚡ **Smart Adaptive Schedule & Burst Mode:** Dynamically accelerates into high-frequency cadence (e.g. 1m) upon activity/discoveries and backs off to idle (e.g. 30m) when quiet, conserving LLM tokens while reacting instantly. Includes 1-click 15m Burst trigger in the GUI and `cron_burst` Code Mode tool.
* 🔗 **Multi-Job Pipeline & DAG Workflows:** Chain tasks with `onSuccess` / `onFailure` triggers, memory propagation, and cycle prevention.
* 📡 **Inbound Webhooks & HTTP Trigger Receiver:** External event triggers with HMAC SHA-256 signatures (GitHub, GitLab, CI/CD).
* ⚡ **Priority Concurrency & Worker Pool:** Parallel bounded worker slots (1 to 10) with priority queue sorting (`high`, `normal`, `low`).
* 🛡️ **Dead Letter Queue (DLQ) & Failure Circuit Breaker:** Automatic quarantine after failures with canary probe recovery.
* 🏷️ **Job Tags & Multi-Criteria Live Filtering:** Instant search, dynamic categories, tag pills, and matching counters.
* 📈 **Real-Time Execution Metrics & Prometheus Exporter:** Latency KPIs (`avg`, `min`, `max`, `p95`) and scraping at `/api/metrics/prometheus`.
* 🔔 **Multi-Channel Alerting:** Instant notifications via Slack, Discord, or custom HTTP webhooks with anti-spam cooldowns.
* 📋 **Job Template & Blueprint Engine:** 6 built-in blueprints with 1-click apply and custom ID validation.
* 💾 **Point-in-Time Snapshot & Backup/Restore Engine:** Instant backup bundles with SHA-256 verification and auto-pruning.
* ⏱️ **Execution Timeout Watchdog:** Terminate hung ticks (minimum 5,000ms floor) across headless daemons and in-process plugins.
* 🧹 **Run History Retention Policy:** Auto-prune by age, run count, or total history size.
* 🌐 **Timezone-Aware Scheduling & Cron Aliases:** Full IANA timezone support and macros (`@hourly`, `@daily`, `@weekly`, etc.).
* 🚦 **Pre-Flight Guards & Condition Checks:** Verify HTTP status or shell commands before spending tokens on ticks.
* 🔐 **Secret & Credential Redaction Engine:** Sanitize AI keys, Bearer tokens, private keys, and webhook secrets from logs and history.
* 🛡️ **Autonomous Background Daemon:** Keeps running overnight with your TUI or terminal closed via native `launchd`, `systemd`, or `schtasks`.

---

## ⚡ Plain Cron vs. opencode-cron

| Feature | Plain Cron / Bash Loops | opencode-cron |
|---|---|---|
| **Session Awareness** | ❌ Spawns blind one-off shells | ✅ **Re-prompts same session ID** with full context |
| **Context Compact Safe** | ❌ Wiped out on conversation compact | ✅ **Compaction hook re-injects memory file** |
| **Deduplication** | ❌ Repeats same alerts every tick | ✅ **`seenHashes` dedup prevents repeat alerts** |
| **Loop / Token Protection** | ❌ Can loop infinitely, burning tokens | ✅ **60s min, 5-fail circuit breaker, `maxRuns`, timeout guard** |
| **User Interface** | ❌ Terminal only / crontab file | ✅ **Web GUI Mission Control (`localhost:4488`) + Desktop Tray** |
| **Observability** | ❌ Grepping obscure syslog files | ✅ **Dedicated `/runs` Timeline + Prometheus Exporter** |
| **Pipelines & DAG** | ❌ Fragile custom shell piping | ✅ **Native `onSuccess` / `onFailure` DAG with cycle checks** |
| **External Triggers** | ❌ Custom listening scripts required | ✅ **Authenticated Webhooks (`/api/webhook/:id`)** |
| **Multi-Language** | ❌ English only / none | ✅ **10 languages with interactive onboarding tour** |

---

## 🎨 Brand Identity & Design System

<p align="center">
  <a href="https://culturedigitali.github.io/opencode-cron/">
    <img src="assets/brand-identity.png" alt="opencode-cron Brand Identity and Design Guidelines Spec Board" width="100%" style="max-width: 960px; border-radius: 8px; border: 1px solid #333333;" />
  </a>
</p>

The `opencode-cron` visual system unites **astronomical chronometry** (precision dials, concentric orbits) with **autonomous agent intelligence** (hexagonal neural core).
* **Obsidian Carbon (`#191919`):** Deep terminal foundation and high-contrast surfaces.
* **Deep Teal (`#0c7866`):** Primary brand accent, symbolizing deliberate execution and reliability.
* **Electric Cyan (`#14b8a6`):** Active telemetry, burst triggers, and live status indicators.
* **Warm Bone White (`#f4f4f0`):** High-readability editorial typography and vector linework.

---

## ⏱️ 30-Second Quickstart

### 1. Add Plugin to OpenCode
Add `@culturedigitali/opencode-cron` to your `opencode.json`:
```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["@culturedigitali/opencode-cron"]
}
```

### 2. Launch Mission Control Web GUI
Start the dashboard in one command:
```bash
npx @culturedigitali/opencode-cron gui
# Or if working in this repo:
bun run gui
```
Open **`http://localhost:4488`** in your browser. You get full access to:
- **Mission Control (`/`)**: View jobs, inspect SQLite sessions, trigger test ticks, edit memory, view metrics, and apply templates.
- **Execution History (`/runs`)**: Live timeline of successes, failures, execution latencies, and retention pruning.
- **Interactive Guide (`/instructions`)**: 8-chapter visual documentation + interactive onboarding tour.

### 3. Schedule Your First Job
You can create jobs in two simple ways:

* **Via the Web GUI:** Open any session in Mission Control and click **`⚡ Imposta Cron`**. Choose your schedule (`5m`, `30m`, `cron: 0 9 * * *`), set optional duration (`maxRuns`), type your prompt, and save.
* **Via OpenCode Chat:**
  ```
  /cron-add -> "Controlla le novità AI ogni 15m e salva i risultati"
  ```

### 4. Enable Background Execution (TUI Closed)
Keep tasks running autonomously overnight:
```bash
npx @culturedigitali/opencode-cron os-install
```
* **macOS:** Installs `ai.opencode.cron` launchd daemon (`~/Library/LaunchAgents/`).
* **Linux:** Generates systemd service + timer (`systemctl --user`).
* **Windows:** Configures Task Scheduler via `schtasks`.

---

## 📸 Explore the Features

### 🖥️ Mission Control Web Dashboard (`localhost:4488`)
Manage your entire AI automation fleet in one place:
- **Active Cron Matrix:** Live counters, last tick results, next execution countdowns, and quick pause/resume toggles.
- **SQLite Session Streamer:** Read active and archived chats in real time with auto-refresh and diff highlight.
- **Markdown Memory Studio:** Directly view and edit `.opencode/cron/memory/<id>.md` to steer agent memory without touching terminal files.

### ⚡ 1-Click "Imposta Cron" Session Modal
Never write complex cron strings by hand again:
- **Preset Buttons:** Quick intervals (`5m`, `15m`, `30m`, `1h`, `daily`).
- **Visual Schedule Explainer:** Translates expressions into natural human language and previews the next 3 scheduled run timestamps in real time.
- **Finite vs Infinite Runs:** Set `0` for perpetual automation, or specify `N` (e.g. `5` runs) to automatically mark the job completed once finished.

### 📊 Execution Timeline & Diagnostics (`/runs`)
Full observability into your background workers:
- **Live Status Badges:** Success (`200 OK`), Failed (`ERR`), Skipped, or In-Flight.
- **Detailed Metrics:** Exact runtime duration (e.g. `1240ms`), exit codes, trigger origin (launchd daemon vs manual test).
- **Collapsible Error Traces:** Inspect stack traces, HTTP errors, and model timeouts with one click.
- **Summary Cards & Filters:** Real-time counters for Total Runs, Success Rate %, and Active Jobs.

### 📈 Prometheus Exporter & Performance Metrics
Export production telemetry to your observability stack:
- **Scrape Endpoint:** `GET /api/metrics/prometheus` outputs standard Prometheus metrics.
- **KPI Metrics Modal:** Inspect average latency, p95 execution latency, min/max runtime, and total ticks per job.

### 🔔 Multi-Channel Alerting & Webhooks
Receive immediate alerts when jobs fail or recover:
- **Supported Channels:** Slack incoming webhooks, Discord webhooks, or custom HTTP endpoints.
- **Anti-Spam Throttling:** Configurable cooldowns prevent notification storms during repetitive outages.

### 📋 Job Template & Blueprint Engine
Instantiate battle-tested agent automations with a single click:
- **Repository Janitor:** Automated git cleanup, stale branch tracking, and test integrity.
- **Daily Standup Assistant:** Summarizes yesterday's git commits and PRs into concise morning updates.
- **Flaky CI Watchdog:** Monitors test suites, identifies flaky tests, and files targeted reports.
- **Documentation Sync:** Verifies README code snippets and documentation links against code changes.
- **Security & Dependency Auditor:** Scans for CVEs, outdated packages, and exposed secrets.
- **Production Health Probe:** Verifies HTTP endpoints and triggers alerts on degradation.

### 💾 Point-in-Time Backup & Restore Engine
Protect your automation configurations:
- **Full Snapshot Bundles:** Archives all job definitions and persistent memories into timestamped bundles.
- **Cryptographic Verification:** SHA-256 integrity checks ensure backups cannot be tampered with.
- **Anti Path-Traversal:** Strict validation prevents cross-platform archive extraction attacks.

### 🌍 Universal 10-Language i18n Suite
Localized experience with zero-latency client-side switching:
- 🇬🇧 English · 🇮🇹 Italiano · 🇪🇸 Español · 🇫🇷 Français · 🇩🇪 Deutsch
- 🇵🇹 Português · 🇨🇳 中文 · 🇯🇵 日本語 · 🇷🇺 Русский · 🇸🇦 العربية (Full RTL support)

### 🪟 Native Desktop App & System Tray Monitor (macOS, Windows, Linux)
Run OpenCode Cron as an elegant, native desktop application that lives quietly in your system tray / menu bar:
* **Live System Tray / Menu Bar Icon:**
  - Dynamic status indicator (🟢 Connected / 🔴 Disconnected) with OpenCode daemon heartbeat.
  - **Live Cron Matrix Submenu:** Hover over the tray icon to see all active cronjobs, their frequencies, and exact countdowns to the next execution.
  - **1-Click Quick Actions:** Run due jobs immediately, reload rotated desktop sidecar credentials, or open the external browser.
  - **Run on Startup:** Built-in auto-start toggle ensures your automations resume seamlessly across system reboots.
* **Frameless Dark Architecture:** Designed with sleek macOS `hiddenInset` traffic lights, ultra-clean `#030712` dark styling, and automatic **minimize-to-tray on window close**.
* **Cross-Platform Installers:**
  - **macOS:** Universal `.dmg` installer & `.zip` (Apple Silicon & Intel).
  - **Windows:** NSIS Installer `.exe` & standalone Portable `.exe`.
  - **Linux:** Standalone `.AppImage` & Debian package `.deb`.

---

## 🛠️ Complete Tool Reference (18 Native Tools)

Agents equipped with `@culturedigitali/opencode-cron` have access to 18 native tools:

| Tool | Purpose | Key Parameters |
|---|---|---|
| `cron_add` | Create recurring scheduled task bound to current session | `title`, `every` (e.g. `5m`) or `cron` (e.g. `*/15 * * * *`), `systemPrompt`, `followupPrompt`, `maxRuns`, `catchUp`, `priority`, `pipeline`, `webhook`, `category`, `tags`, `timeoutMs`, `guard` |
| `cron_list` | List all active and paused jobs for the project | *None* |
| `cron_get` | Inspect detailed job state and metadata | `id` |
| `cron_pause` | Temporarily pause automated execution | `id` |
| `cron_resume` | Resume scheduled execution | `id` |
| `cron_remove` | Delete job and clean up persistent memory | `id` |
| `cron_run_now` | Trigger immediate test tick without waiting | `id` |
| `cron_burst` | Trigger high-frequency Burst Mode for rapid monitoring | `id`, `durationMinutes` |
| `cron_priority` | Inspect or update execution priority level (`high`, `normal`, `low`) | `id`, `priority` (optional) |
| `cron_queue` | View active worker slots, in-flight tasks, and priority queue status | *None* |
| `cron_dlq` | Manage Dead Letter Queue quarantined jobs and circuit breaker state | `action` (`list`, `get`, `retry`, `resolve`, `clear`), `jobId` |
| `cron_pipeline` | Inspect Multi-Job Pipeline DAG workflows, dependencies, and execution triggers | `id` (optional) |
| `cron_webhook` | Manage inbound HTTP Webhook trigger endpoint and authorization token | `id`, `action` (`get`, `enable`, `disable`, `rotate-token`), `secret`, `rateLimitSeconds`, `passPayload` |
| `cron_memory_read` | Read persistent markdown memory for job | `id` |
| `cron_memory_save` | Persist findings, update facts, append `seenHashes` | `id`, `fattiChiave`, `nuoviVisti`, `lastRunSummary`, `domandeAperte` |
| `cron_metrics` | View latency KPIs, p95 latencies, success rates, and Prometheus metrics | `id` (optional) |
| `cron_template` | List blueprints or instantiate a job from a production template | `action` (`list`, `apply`), `templateId`, `targetId` |
| `cron_backup` | Create snapshot or restore jobs and memory from backup bundle | `action` (`create`, `list`, `restore`), `backupId` |

### Chat Slash Commands
- `/cron-add`: Interactive wizard to schedule a new task.
- `/cron-list`: Inspect all jobs and upcoming execution times.
- `/cron-manage`: Pause, resume, or delete a job.
- `/cron-gui`: View dashboard status and quick-launch the Web GUI.
- `/cron-refresh`: Re-synchronize rotated desktop app sidecar credentials.

---

## 🏗️ Architecture: How It Works

```
                                  ┌─────────────────────────────┐
                                  │   OpenCode Chat / Web GUI   │
                                  └──────────────┬──────────────┘
                                                 │
                                                 ▼
                                     .opencode/cron/jobs.json
                                     .opencode/cron/memory/<id>.md
                                                 │
                     ┌───────────────────────────┴───────────────────────────┐
                     │                                                       │
          [ TUI Open: In-Process ]                                [ TUI Closed: OS Daemon ]
                     │                                                       │
         Scheduler Timer (scheduler.ts)                         launchd / systemd / schtasks (60s)
                     │                                                       │
                     ▼                                                       ▼
        ctx.session.prompt({ sessionID })                       opencode-cron check --dir <project>
                     │                                                       │
                     └───────────────────────────┬───────────────────────────┘
                                                 │
                                                 ▼
                                 OpenCode Session Server (HTTP/CLI)
                                                 │
                                  [ Every Tick Injects: ]
                                  1. Frozen System Objective
                                  2. Persistent Memory Markdown
                                  3. Mandatory 3-Question Self-Check
                                  4. Followup Prompt + cron_memory_save
```

### Context Compaction Preservation
When an AI chat reaches token limits, OpenCode triggers compaction. Normal prompt state is compressed or discarded.
**opencode-cron hooks into `ctx.session.hook("compaction")`** to re-inject `.opencode/cron/memory/<id>.md` directly into the compaction summary. Your agent retains 100% of its learned state, discovered URLs, and deduplication hashes.

---

## 🛡️ Production Guardrails & Reliability

Designed for production workstations and autonomous background operations:
* **Minimum 60s Interval:** Prevents runaway recursive loops and excessive API charges.
* **Atomic Concurrency Locks:** `.lock` files prevent duplicate ticks if a previous execution is still running (`skipIfRunning: true`).
* **Circuit Breaker Auto-Pause:** If an agent fails 5 consecutive times, the job auto-quarantines into the Dead Letter Queue.
* **Execution Timeout Watchdog:** Terminate hung ticks (minimum 5,000ms floor) across daemons and plugins.
* **Pre-Flight Guards:** Skip ticks when health checks fail, preventing wasted LLM credits.
* **Secret Redaction:** Strip sensitive keys and tokens from logs, run history, and notifications.
* **Self-Check Before Action:** Every tick prompt enforces a 3-question self-audit before making edits or API calls.

---

## 🔒 Security & Desktop Credentials Rotation

The OpenCode desktop app rotates internal sidecar credentials on every restart. opencode-cron handles this automatically:
1. Credentials are saved to `~/.config/opencode-cron/credentials` with strict `0600` permissions.
2. If credentials expire after a desktop app restart, simply run:
   ```bash
   node ./dist/bin/run.js refresh-creds
   ```
   *(Or trigger `/cron-refresh` in chat).*
3. **Zero Secrets in Git:** Job definitions and persistent memories live in `.opencode/cron/`, which is gitignored by default. Never commit sensitive API tokens to prompt text. See [`SECURITY.md`](SECURITY.md).

---

## 🎨 Brand Identity & Design System

The visual identity of **opencode-cron** was crafted with Gemini Pro & Nano Banana, reflecting precision timekeeping and autonomous agentic engineering.

<p align="center">
  <a href="assets/brand-identity.png">
    <img src="assets/brand-identity.png" alt="opencode-cron Brand Identity Board and Guidelines" width="100%" style="border-radius: 10px; max-width: 860px; border: 1px solid #2a2a2a;" />
  </a>
</p>

### 🌌 Visual Philosophy & Symbolism
* **The Precision Astrolabe & Chronometer Outer Ring:** Honors mechanical timepieces and astronomical astrolabes (inspired by Regiomontanus' 1462 astrolabe in The Met collection) — celebrating cyclical, deterministic cadence.
* **The Neural Agent Nucleus:** The glowing hexagonal core represents autonomous OpenCode agents executing reliably at each scheduled interval.
* **Tagline:** *"Agents run on time."*

### 🎨 Color Palette Tokens
| Token Name | Hex Code | RGB | Role / Usage |
|---|---|---|---|
| **Obsidian Carbon** | `#191919` | `rgb(25, 25, 25)` | Primary canvas, terminal background, dark-mode surfaces |
| **Deep Astrolabe Teal** | `#0c7866` | `rgb(12, 120, 102)` | Primary brand accent, borders, badges, deep status indicators |
| **Electric Cyan Core** | `#14b8a6` | `rgb(20, 184, 166)` | Active tick pulses, glowing agent nucleus, focus states |
| **Bone White** | `#f4f4f0` | `rgb(244, 244, 240)` | High-contrast typography, astrolabe gears, foreground text |
| **Warning Amber** | `#f59e0b` | `rgb(245, 158, 11)` | Cooldowns, canary warnings, burst mode triggers |
| **Quarantine Red** | `#ef4444` | `rgb(239, 68, 68)` | Circuit breaker open, DLQ alerts |

### 🔤 Typography & Brand Guidelines
* **Display / Editorial:** Gambarino (Warm serif with geometric precision) & Inter Display
* **Body / Interface:** General Sans & Inter
* **Code / Terminal:** JetBrains Mono
* **Iconography:** Utilitarian, thin-line geometric vector strokes with 2px borders and 8px/12px corner radii.

### 📦 Asset Directory
* **Master Logo (1024x1024 PNG):** [`assets/logo.png`](assets/logo.png)
* **Transparent Original:** [`assets/logo-transparent.png`](assets/logo-transparent.png)
* **Dark Mode Two-Tone:** [`assets/logo-dark.png`](assets/logo-dark.png)
* **Vector Master (SVG):** [`assets/logo.svg`](assets/logo.svg)
* **App Icon (512x512 PNG):** [`assets/icon.png`](assets/icon.png)
* **Brand Guidelines Board:** [`assets/brand-identity.png`](assets/brand-identity.png)
* **GitHub Social Preview (1024x572):** [`assets/social-preview.png`](assets/social-preview.png)

---

## ❤️ Sponsor & Support OpenCode Cron

OpenCode Cron is developed and maintained by [Culture Digitali](https://github.com/CultureDigitali) as free, open-source infrastructure for the AI agent ecosystem.

If OpenCode Cron saves your team engineering hours, automates mission-critical tasks, or protects your token budget:
- **[Sponsor on GitHub](https://github.com/sponsors/CultureDigitali)** to support ongoing maintenance and enterprise features.
- **Star the repository** on GitHub to help other agentic engineers find us.
- Contact us at **`contact@culturedigitali.com`** for custom integrations, enterprise SLA, or dedicated deployment support.

---

## 🤝 Contributing

Contributions are welcomed!
1. Clone the repository: `git clone https://github.com/CultureDigitali/opencode-cron.git`
2. Install dependencies: `bun install`
3. Run tests and typecheck:
   ```bash
   bun test && bun run typecheck && bun run build
   ```
4. Read our [Contributing Guide](CONTRIBUTING.md) and submit a pull request!

---

## 📄 License

MIT © [Culture Digitali](https://github.com/CultureDigitali) and contributors.
See [LICENSE](LICENSE) for details.
