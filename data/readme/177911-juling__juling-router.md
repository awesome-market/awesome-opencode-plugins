<p align="center">
  <img src="docs/icon.png" alt="Juling Router app icon" width="128" />
</p>

<h1 align="center">Juling Router</h1>

<p align="center"><strong>One desktop window to install, launch and re-point every AI coding tool — with one shared model catalog.</strong></p>

<p align="center">
Juling Router is an open-source desktop control center for AI tools and LLM providers. It installs and launches 20+ AI CLIs and desktop agents, writes each tool's native config when you switch models, keeps ChatGPT / Codex CLI / Claude Code accounts with live quota in one place, runs a local OpenAI- and Anthropic-compatible endpoint with automatic failover, and can serve local models. Windows, macOS and Linux. Tauri + Rust.
</p>

<p align="center">
  <a href="https://github.com/177911-juling/Juling-Router/releases">
    <img src="https://img.shields.io/github/v/release/177911-juling/Juling-Router?style=flat-square&color=D97757" alt="Latest release" />
  </a>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue?style=flat-square" alt="Windows, macOS and Linux" />
  <img src="https://img.shields.io/badge/stack-Tauri%20%2B%20Rust-orange?style=flat-square" alt="Tauri + Rust" />
  <img src="https://img.shields.io/github/license/177911-juling/Juling-Router?style=flat-square" alt="Apache-2.0 license" />
  <img src="https://img.shields.io/github/stars/177911-juling/Juling-Router?style=flat-square" alt="GitHub stars" />
</p>

<p align="center">
  <a href="https://www.177911.com">API Token Trading Platform</a> ·
  <a href="https://github.com/177911-juling/Juling-Router/releases/latest">Download</a> ·
  <a href="README.zh-CN.md">中文 README</a>
</p>

> This GitHub repository is one of several distribution channels and the public issue tracker. Product pages, announcements and commercial inquiries: [Juling, a large-model compute trading platform](https://www.177911.com).

---

## Why this exists

AI work is scattered by design. Claude Code, Codex CLI, Cursor, ChatGPT Desktop and the rest each keep their own config file, their own login and their own quota screen. Setting up a new machine means repeating everything, and a provider outage means editing half a dozen files one by one.

Juling Router pulls that apart into a single desktop surface: one catalog of providers and models, one place to install and launch the apps, one switch for accounts and models, and one local endpoint that keeps going when a provider does not.

## At a glance

| What you get | Why it matters |
| --- | --- |
| **AI app manager** | Install, update and launch 20+ coding CLIs and desktop agents; Juling Router knows where each one lives and how it stores settings |
| **Shared model catalog** | OpenAI-compatible APIs, Anthropic, Gemini, DeepSeek and router/relay providers configured once, then reused by every supported tool |
| **Model switching** | Pick a model in the catalog and Juling Router rewrites the tool's native config (`~/.claude`, `~/.codex`, `~/.grok/config.toml`, `~/.kimi-code/config.toml` and more) — no manual TOML/JSON editing |
| **Account center** | Multiple ChatGPT, Codex CLI and Claude Code accounts, browser sign-in, plan and quota display, refresh and deletion |
| **Auto Router** | A local OpenAI Chat Completions + Anthropic Messages endpoint that tries models in your order and fails over on rate limits or outages |
| **Local LLMs** | Hardware-aware runtime selection, model download and a one-click start — all on your own machine |
| **Extras** | Voice input, a chat assistant, AI news briefs, a usage dashboard, community plugins and a token pet |

## Run your AI stack from one window

The App Manager is the home screen. It detects what is installed, offers one-click install for the rest, and launches apps without hunting for shortcuts. Every supported tool is driven through the same model catalog, so the workflow is always the same: pick a provider, pick a model, launch, switch.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/desktop-en-dark.png">
  <img alt="Juling Router App Manager with the app store" src="docs/screenshots/desktop-en-light.png" width="100%">
</picture>

Coding CLIs such as **Claude Code**, **Codex CLI**, **Grok Build**, **Kimi CLI**, **Qwen Code**, **Aider**, **OpenCode**, **MiMo Code**, **Kilo Code**, **ZCode**, **OpenClaw**, **Pi** and **Vibe-Trading** are handled at their native config level. Desktop apps including **Claude Desktop** (3P profile), **ChatGPT Desktop**, **Kimi Desktop**, **OpenCode Desktop**, **OpenScience** and **WorkBuddy** are supported too.

## One model catalog, every tool

Model Nexus is the single source of truth. Add OpenAI, Anthropic, Gemini, DeepSeek, compatible third-party APIs, API relays or local models, test latency before committing, then point any supported tool at that entry. Change the provider or the key once — every tool that uses it follows.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/model-en-dark.png">
  <img alt="Juling Router Model Nexus" src="docs/screenshots/model-en-light.png" width="100%">
</picture>

API keys are encrypted at rest with AES-256-GCM and bound to the machine; they never leave your computer.

## Switch accounts, watch quota

Save several accounts for the tools that rotate sessions, then choose which one a launch should use:

- **ChatGPT Desktop and Codex CLI** — add OpenAI accounts through browser sign-in; both read the shared local Codex account, so the selected account applies to both.
- **Claude Code** — browser authorization, then launch with the chosen account; plan, remaining 5-hour and 7-day quota, and reset countdowns are shown when the provider exposes them.
- **Quota panel** — refresh usage, spot exhausted accounts and remove saved ones without leaving the app.

Account switching changes logins; Auto Router below is about model endpoints. Pick whichever fits the task, and use a third-party model when you prefer an API provider.

## A local endpoint that survives provider failures

Auto Router puts up to 20 of your configured models behind one local API. Drag the cards into priority order; requests try the first model, then fall back automatically when a model is rate-limited, out of quota or temporarily unavailable. Cooldowns end, and routing resumes from the top.

- **One endpoint, two protocols** — OpenAI Chat Completions and Anthropic Messages, including clients such as Claude Code.
- **Explicit priority** — the order you set is the order used, not a price- or task-based guess.
- **No key re-entry** — reuse models already configured in Model Nexus.

For ChatGPT Desktop and Codex CLI third-party models, use account switching or a Responses-compatible provider directly; Auto Router does not expose the Responses API.

## Models that never leave your machine

The Local page detects your hardware, picks a suitable runtime, downloads a quantized model and starts a server in one flow. Everything runs locally; nothing is uploaded to a hosted provider.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/localllm-en-dark.png">
  <img alt="Juling Router local model marketplace" src="docs/screenshots/localllm-en-light.png" width="100%">
</picture>

## More than a launcher

- **Voice input** — speech-to-text with text polishing, plus selection translate and ask once the enhancement is enabled.
- **Assistant** — a chat-driven setup and troubleshooting agent with quick commands and SSH server management.
- **AI Brief** — a daily digest of AI news, pulled into the same app.
- **AI Career** — a dashboard of sessions, messages and token usage across your coding tools.
- **Plugin Hub (developer preview)** — install reviewed community plugins, themes and text processors from GitHub, GitCode/CNB or a local directory.
- **Token Pet** — a small companion that grows as you use AI.

<table>
  <tr>
    <td align="center" width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/agent-en-dark.png">
        <img alt="Juling Router Assistant" src="docs/screenshots/agent-en-light.png" width="100%">
      </picture>
      <br><sub>Assistant</sub>
    </td>
    <td align="center" width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/career-en-dark.png">
        <img alt="Juling Router AI Career dashboard" src="docs/screenshots/career-en-light.png" width="100%">
      </picture>
      <br><sub>AI Career</sub>
    </td>
  </tr>
</table>

## Supported tools

**Install and switch models in one click** — the tool's own config is rewritten for you.

Coding CLIs: Claude Code · Codex CLI (OpenAI) · Grok Build (xAI) · Kimi CLI (Moonshot) · Qwen Code · Aider · OpenCode · MiMo Code (Xiaomi) · Kilo Code · ZCode (Z.AI) · OpenClaw · Pi · Vibe-Trading

Desktop apps: Claude Desktop (3P profile) · ChatGPT Desktop · Kimi Desktop · OpenCode Desktop · OpenScience · WorkBuddy (Tencent CodeBuddy)

**Install and launch, model selection stays with the app**

Hermes Desktop · Claude Science · Cursor · VS Code · Gemini Desktop · Coffee CLI

## Install

**Windows** (PowerShell)

```powershell
irm https://www.177911.com/install.ps1 | iex
```

**macOS / Linux**

```sh
curl -fsSL https://www.177911.com/install.sh | sh
```

The script detects the OS, downloads the matching build and skips the download when you are already current.

Prefer a manual download? Grab the latest package:

| Platform | Asset |
| --- | --- |
| Windows x64 | `JulingRouter_<ver>_Windows_x64-setup.exe` |
| macOS (Apple Silicon) | `JulingRouter_<ver>_macOS_arm64.dmg` |
| Linux x64 · Debian/Ubuntu | `JulingRouter_<ver>_Linux_x64.deb` |
| Linux arm64 · Debian/Ubuntu | `JulingRouter_<ver>_Linux_arm64.deb` |
| Linux x64 · Fedora/RHEL | `JulingRouter_<ver>_Linux_x64.rpm` |
| Linux arm64 · Fedora/RHEL | `JulingRouter_<ver>_Linux_arm64.rpm` |

Releases: <https://github.com/177911-juling/Juling-Router/releases/latest>

## Build from source

Requirements: Node.js 22+, Rust 1.93 (see `rust-toolchain.toml`), and the usual Tauri platform prerequisites (MSVC + WebView2 on Windows, Xcode command-line tools on macOS, WebKitGTK on Linux).

```sh
git clone https://github.com/177911-juling/Juling-Router.git
cd Juling-Router
npm install
npm run dev     # Tauri dev window
npm run build   # production bundles
```

Quality gates used by CI:

```sh
npm run format:check && npm run typecheck && npm run lint && npm test
cd src-tauri && cargo fmt --check && cargo clippy --all-targets --all-features -- -D warnings && cargo test
```

## FAQ

**Is Juling Router a proxy or a VPN?**
No. It is a desktop manager: it writes the config files that AI tools already read, and optionally exposes a local OpenAI/Anthropic-compatible endpoint on your machine. Nothing is tunneled to a remote service.

**How do I switch models for Claude Code or Codex CLI?**
Add the provider once in Model Nexus, then choose that entry for the tool. Juling Router rewrites the tool's native config, so no manual TOML or JSON editing is needed.

**Where are my API keys and accounts stored?**
Locally. Model API keys are encrypted with AES-256-GCM using a machine-bound key; account data stays in the app's own directory and is never uploaded.

**Does Auto Router rotate my accounts?**
No — it rotates **model endpoints**. Use the Account Center to switch ChatGPT, Codex CLI or Claude Code logins.

**Can I point it at a self-hosted or third-party OpenAI-compatible API?**
Yes. Any OpenAI- or Anthropic-compatible endpoint can be added as a model, including local servers.

**Which platforms are supported?**
Windows x64, macOS on Apple Silicon, and Linux x64/arm64 as Debian or RPM packages.

## Developer

<table>
  <tr>
    <td width="150" align="center">
      <img src="docs/sponsors/juling-api.png" width="92" alt="Juling API Market" />
    </td>
    <td>
      <a href="https://www.177911.com"><strong>Juling API Market</strong></a> — API Token trading platform for large-model compute<br/>
      No lock-in to any single API site — compare the whole market. More models, more vendors, never out of stock, available, affordable, reliable and guaranteed.
    </td>
  </tr>
</table>

## License and brand

The source code of **Juling Router v1.0.0** is released under the [Apache License 2.0](LICENSE). Fork it, audit it, build on it. [NOTICE](NOTICE) explains attribution.

The **brand and trade dress** are separate from the code license. The name **Juling Router**, its logo, and the distinctive combination of the app's user-facing surfaces are common-law marks of 177911-juling; descriptive feature labels such as _Model Nexus_ / _模型中心_ are protected only as part of that trade dress. Forks may keep the branding with honest upstream credit ("Juling Router Community Edition by X"), or rebrand entirely while keeping the NOTICE attribution. Commercial SaaS or app-store products branded "Juling Router" need permission, and the code must not be presented as an original from-scratch work. See [TRADEMARKS.md](TRADEMARKS.md) for the exact policy.

---

<p align="center">
  Built by the Juling Router Team<br>
  <sub>⭐ <a href="https://github.com/177911-juling/Juling-Router">Star the repository</a> · <a href="README.zh-CN.md">中文文档</a> · <a href="https://www.177911.com">API Token Trading Platform</a></sub>
</p>
