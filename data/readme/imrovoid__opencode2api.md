<div align="center">

<img src="assets/images/OpenCode2API_Banner.webp" alt="OpenCode2API Banner" width="100%">

# OpenCode2API-Proxy

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![npm version](https://img.shields.io/npm/v/opencode2api-proxy.svg?logo=npm&logoColor=white)](https://www.npmjs.com/package/opencode2api-proxy)
[![CI](https://github.com/IMROVOID/OpenCode2API/actions/workflows/test.yml/badge.svg)](https://github.com/IMROVOID/OpenCode2API/actions/workflows/test.yml)
[![Node.js Version](https://img.shields.io/badge/Node.js-%3E%3D26.0.0-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-7.0.2-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers-F38020?logo=cloudflare&logoColor=white)](https://workers.cloudflare.com/)
[![OpenCode](https://img.shields.io/badge/OpenCode-FF6900?logo=opencode&logoColor=white)](https://opencode.ai/)
[![OpenAI Compatible](https://img.shields.io/badge/OpenAI-Compatible-412991?logo=openai&logoColor=white)](https://platform.openai.com/docs/api-reference)

<p align="center">
  OpenCode Zen and Go to a universal OpenAI, Responses and Anthropic compatible API router. Serve <b>Zen</b> and <b>Go</b> models from one endpoint with <b>protocol conversion, streaming, key rotation, rich model attributes, and a built-in control WebUI with AI Chat and one-click self-updating</b>.
</p>

<p align="center">
  <b><a href="README.md">English</a></b> • <b><a href="README_ZH.md">简体中文 (Simplified Chinese)</a></b> • <b><a href="README_FA.md">فارسی (Persian)</a></b> • <b><a href="https://opencode2api.rovoid.tech">Website</a></b> • <b><a href="https://opencode2api.rovoid.tech/docs">Documentation</a></b>
</p>

[Overview](#what-is-opencode2api-proxy) • [Why OpenCode2API?](#why-opencode2api) • [Features](#key-features) • [Quick Start](#quick-start) • [Models](#model-catalog--aliases) • [Clients](#client-integration) • [Architecture](#architecture--structure) • [Guides](#advanced-guides) • [Disclaimer](#disclaimer--legal-notice) • [References](#references--acknowledgements) • [License](#license)

</div>

## Table of Contents

- [What is OpenCode2API-Proxy?](#what-is-opencode2api-proxy)
- [Why OpenCode2API?](#why-opencode2api)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
  - [Method 1: Local Daemon & npm](#method-1-local-daemon--npm)
  - [Method 2: Built Release](#method-2-built-release)
  - [Method 3: Cloudflare Workers (Serverless)](#method-3-cloudflare-workers-serverless)
  - [Method 4: Docker & Self-Hosted (Coolify / Dokploy / Zeabur)](#method-4-docker--self-hosted-coolify--dokploy--zeabur)
- [Model Catalog & Aliases](#model-catalog--aliases)
- [Client Integration](#client-integration)
- [Architecture & Structure](#architecture--structure)
- [Advanced Guides](#advanced-guides)
  - [WebUI Control Panel & AI Chat Suite](#webui-control-panel--ai-chat-suite)
  - [Automatic Update System](#automatic-update-system)
  - [Protocol Conversion](#protocol-conversion)
  - [Key Rotation & Failure Handling](#key-rotation--failure-handling)
  - [Unlimited Lane & Dual-Lane Architecture](#unlimited-lane--dual-lane-architecture)
  - [Environment Variables](#environment-variables)
- [Development & Testing](#development--testing)
  - [Continuous Integration (CI)](#continuous-integration-ci)
  - [Building & Publishing Releases](#building--publishing-releases)
- [Disclaimer & Legal Notice](#disclaimer--legal-notice)
- [References & Acknowledgements](#references--acknowledgements)
- [License](#license)

## What is OpenCode2API-Proxy?

[OpenCode](https://opencode.ai/) serves its **Zen** and **Go** model families behind two different wire shapes. The Zen lane expects the OpenCode 1.x request format, the Go lane the OpenCode 2.x CLI format, and neither is directly consumable by the OpenAI-compatible clients developers actually use.

**OpenCode2API-Proxy** bridges that gap:

1. It discovers the models OpenCode publishes, per tier, and learns each model's **native protocol** and **rich attributes** (context windows, limits, modalities, capabilities) from OpenCode's own capability catalog.
2. It serves a single endpoint that speaks **OpenAI Chat Completions**, **OpenAI Responses** and **Anthropic Messages** at the same time, converting a request from the client's protocol to the upstream's and converting the answer back.
3. It rotates across several upstream keys, cools down the ones that fail, and falls back from the anonymous lane to the authenticated tiers.
4. It ships an advanced **control WebUI & AI Chat Suite** with System, Dark, and Light themes on every deployment method, featuring streaming chat inference, IDE-style document previews, 30-day stateless sessions, and a one-click Cloudflare Worker self-updater.

> **Note**: The Go lane requires an active OpenCode Go subscription and a workspace in the Global region. The free tier is served from the official OpenCode client only, so it needs that client's TLS fingerprint. See [Disclaimer & Legal Notice](#disclaimer--legal-notice).

> **Reference**: Inspired by and referencing the original [jasonxu114514/opencode2api](https://github.com/jasonxu114514/opencode2api) repository.

## Why OpenCode2API?

If you are looking to plug OpenCode Zen and Go models into **Cursor, Claude Code, Cline, Roo Code, or OpenWebUI**, here is how `IMROVOID/OpenCode2API` compares to standard wrappers and forks:

| Feature / Pain Point | Basic CLI Wrappers & Competing Repos | `IMROVOID/OpenCode2API` |
| --- | --- | --- |
| **Protocol Coverage** | OpenAI `/v1/chat/completions` only | **Triple Protocol:** Native OpenAI Chat, `/v1/responses` (reasoning/streams), and native **Anthropic `/v1/messages`** |
| **Runtime Footprint** | Requires global Node.js + OpenCode CLI subprocess | Single self-contained binary, 1-command Docker / npm, or zero-local-dependency Cloudflare Worker bundle |
| **Rate Limits & 429s** | Dies when anonymous IP quota hits | Automatic proxy/key pooling, exponential cooldown circuit breakers, DoH IPv6 edge pool rotation, and Kilo tier failover |
| **Tool Calling & Streaming** | Often breaks on SSE or tool schemas | Full native tool-call translation, structured reasoning tokens, and first-event SSE timeout protection |
| **Context Window Preservation** | Truncates to 200k/256k | Auto-detects and preserves full **1,000,000 token context windows** without down-tiering |
| **Control Plane** | None (headless terminal logs) | Full-featured Control WebUI & AI Chat Suite with Light/Dark themes, file preview, metrics, and one-click self-updating |

## Key Features

- **Three Protocols, One Endpoint**: `/v1/chat/completions`, `/v1/responses` and `/v1/messages` all accept the same request body and answer in the protocol the client asked for.
- **Three Deployment Methods**:
  - **Local Daemon & npm**: Run globally via npm (`npm install -g opencode2api-proxy`), run directly with `npx`, or run from a cloned repository with a local API endpoint on `127.0.0.1:8080` and control WebUI on `127.0.0.1:8081`.
  - **Built Release**: Cross-platform ZIP archives for Linux, Windows and macOS on x64 and arm64, each with an example configuration.
  - **Cloudflare Worker**: A standalone bundle with no Node built-ins, full control WebUI, and self-healing rotation.
- **Advanced WebUI & AI Chat Suite**:
  - **Interactive AI Chat Panel**: Real-time SSE streaming inference, tool call execution visualization, live process indicator, message jump navigation, timeline groups, and search highlighting.
  - **In-Place Markdown Composer**: Rich-text composer with custom formatting context menu and custom modal hyperlink overlay (zero browser alert popups).
  - **File Preview Panel**: Responsive split-pane and mobile overlay preview panel for text, Markdown, HTML, CSV, and PDF documents with segmented Preview / IDE raw mode, line numbers gutter, and download menu.
  - **Draft & Staging Persistence**: Unsent messages, conversation preview panel states, and media staging persist in `localStorage` across reloads with edge gradient fades.
  - **Theme Switcher**: System (default), Dark, and Light mode switcher with upward combobox menu, SVG icons, greyscale OKLCH tokens, and `localStorage` persistence.
  - **Instant Skeleton Loading**: Instant route skeleton states and smooth horizontal sliding sidebar collapse animation.
  - **Interactive Monitor & Charts**: Real-time request counters, latency tracking, uptime scales (days/weeks/months/years), and SVG charts.
- **Automatic Update Checker & One-Click Cloudflare Worker Updater**:
  - Checks GitHub Releases and npm registry on a 15-minute cache with in-panel release notes preview.
  - One-click remote update for Cloudflare Workers using a scoped Cloudflare API token (`workers:write`).
  - Automatic update commands for Node.js git repos (`git pull --ff-only && npm run build`) and npm global installs.
- **Robust 30-Day Stateless Sessions & Persistence**:
  - HMAC-SHA256 signed stateless session tokens in HTTP-only cookies (`opencode2api_session`) surviving Worker cold-starts.
  - Server state sidecar persistence (`.opencode2api-state.json`) for local daemon sessions, metrics, and logs.
  - SPA routing with history navigation, preserving custom paths (`WEBUI_PATH` / `ADMIN_PATH`) without reload logout.
- **Model Catalog Discovery & Rich Attributes**:
  - Discovers models on Zen and Go tiers and learns native protocols, context window lengths, token limits, and input/output modalities.
  - Exposes detailed descriptors on both daemon and Worker `/v1/models` endpoints.
  - Preserves 1M context windows without down-tiering in free equivalents.
- **Protocol-Native Routing**: A request is sent in the upstream's own protocol, so no conversion happens on the hot path unless the client asked for a different one.
- **Key Rotation & Cooldown**: A 401, 403 or 429 rotates to the next key of the tier; the failing key is cooled down with an exponential backoff, and a non-retryable 4xx leaves the tier immediately.
- **Dual-Lane Self-Healing & Quota Bypass**:
  - **OpenCode Unlimited Lane**: Discovers live Cloudflare `AAAA` edge pools via DoH (`1.1.1.1/dns-query`), steers Worker subrequests with `cf.resolveOverride`, rotates device/session/project identities on `QuotaExceeded` / `429` walls (up to 8 hops), and blacklists burned `/64` prefixes.
  - **Kilo Free Gateway Failover**: Seamless secondary fallback to high-throughput free models without quotas, automatically rotating past 400 `context_length_exceeded`, 401, 403, and 404 errors while prioritizing 1M models.
- **Full SSE Streaming**: Reasoning deltas, tool call arguments and the usage report survive the trip, and a non-streaming client gets the same answer collapsed back into one document.
- **Complete Vector Branding Suite**: Parametric SVG logo marks, favicons, Apple touch icons, PWA icons, 1200x630 banner, and full OpenGraph/Twitter SEO metadata.
- **Modern Toolchains & Quality**:
  - Built with **TypeScript 7.0.2** and **Node.js 26 LTS**.
  - **277 automated unit & integration tests** across 85 test suites.
- **Standalone Public Website & Documentation Portal**:
  - Accessible at [opencode2api.rovoid.tech](https://opencode2api.rovoid.tech).
  - Visible Grid aesthetic with responsive interactive dot grid, fluid cursor, and full dark/light theme toggle.
  - Interactive Cloudflare Worker automated deployer with live subdomain and URL reporting.
  - Comprehensive documentation portal with instant search, keyboard shortcuts (`Ctrl+K`), and live code snippets.
- **Safe & Resource-Bounded**:
  - 32 MB request body limit and 64 MB response body limit.
  - Client disconnect cancellation through `AbortSignal`.
  - An upstream timeout that ends a stalled request instead of hanging it.
  - Secrets masked out of every log line and every WebUI view.

## Quick Start

### Method 1: Local Daemon & npm

#### Step 1: Get an API Key

Create a key in the [OpenCode Console](https://opencode.ai/) and copy it. You need a key for the **Zen** tier, the **Go** tier, or both.

#### Step 2: Install or Run

Choose one of three ways to run:

**Option A: Global npm Installation**

```bash
npm install -g opencode2api-proxy
```

The package ships the CLI bundle, the standalone Cloudflare Worker bundle (`worker/worker.js`), and the example configuration.

**Option B: Direct execution via npx (no install)**

```bash
npx opencode2api-proxy start
```

**Option C: Clone from GitHub & build from source**

```bash
git clone https://github.com/IMROVOID/OpenCode2API.git
cd OpenCode2API
npm install
npm run build
node dist/cli.js start
```

#### Step 3: Configure

Copy the example configuration and edit it:

```bash
cp config.example.json config.json
```

```json
{
  "listen": "127.0.0.1:8080",
  "server_keys": ["sk-your-local-key"],
  "zen_keys": ["sk-your-zen-key"],
  "go_keys": ["sk-your-go-key"],
  "webui": {
    "enabled": true,
    "listen": "127.0.0.1:8081",
    "username": "admin",
    "password": "change-this-admin-password"
  }
}
```

`server_keys` are the keys your clients authenticate with. `zen_keys` and `go_keys` are the keys OpenCode issued you.

Alternatively, provide keys directly via a `.env` file in your working directory without editing JSON:

```env
API_KEY=sk-your-local-key
OPENCODE_ZEN_KEYS=sk-your-zen-key
OPENCODE_GO_KEYS=sk-your-go-key
```

#### Step 4: Start the Router

```bash
opencode2api-proxy start
```

Or specify a custom port and key:

```bash
opencode2api-proxy start --port 8080 --key sk-my-secret-key
```

Your local endpoint is available at `http://127.0.0.1:8080/v1`, and the control WebUI at `http://127.0.0.1:8081`.

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-your-local-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4.1-flash","messages":[{"role":"user","content":"Hello"}]}'
```

### Method 2: Built Release

Prebuilt archives for every supported platform are attached to each release.

#### Step 1: Download

Grab the archive that matches your platform from the [releases page](https://github.com/IMROVOID/OpenCode2API/releases):

| Target | File |
|---|---|
| Linux x64 | `opencode2api-proxy-v1.2.0-linux-x64.zip` |
| Linux arm64 | `opencode2api-proxy-v1.2.0-linux-arm64.zip` |
| Windows x64 | `opencode2api-proxy-v1.2.0-win-x64.zip` |
| Windows arm64 | `opencode2api-proxy-v1.2.0-win-arm64.zip` |
| macOS (Intel) | `opencode2api-proxy-v1.2.0-macos-x64.zip` |
| macOS (Apple Silicon) | `opencode2api-proxy-v1.2.0-macos-arm64.zip` |

#### Step 2: Extract and configure

```bash
unzip opencode2api-proxy-v1.2.0-linux-x64.zip -d opencode2api-proxy
cd opencode2api-proxy
mv config.example.json config.json
```

Each archive ships a **separate example configuration** named `config.example.json`, so the proxy never overwrites a configuration you already wrote. Rename it to `config.json` and fill in your keys.

#### Step 3: Run

```bash
node opencode2api-proxy.js
```

On Windows:

```powershell
node opencode2api-proxy.js
```

The archive runs on any system with **Node.js 26 or newer**. Install it from [nodejs.org](https://nodejs.org/) if you do not have it.

### Method 3: Cloudflare Workers (Serverless)

Deploy a 24/7 serverless gateway without keeping your computer running.

#### Step 1: Copy the Code

Open [`worker/worker.js`](./worker/worker.js) and copy the entire file contents.

#### Step 2: Create Worker in Cloudflare Dashboard

1. Log into the [Cloudflare Dashboard](https://dash.cloudflare.com).
2. Go to **Workers & Pages** -> **Create application** -> **Create Worker**.
3. Set name to `opencode2api-proxy` and click **Deploy**.
4. Click **Edit code**, select all existing code, delete it, and paste the copied contents of `worker/worker.js`.
5. Click **Deploy** in the top right.

#### Step 3: Add Variables & Secrets

In your Worker, go to **Settings** -> **Variables and Secrets** and configure as needed:

| Variable | Type | Default | Description |
|---|---|---|---|
| `ADMIN_USERNAME` | Text / Secret | `admin` | Username for the control WebUI |
| `ADMIN_PASSWORD` / `WEBUI_PASSWORD` | Secret | `admin` | Password for the control WebUI (change from default in production!) |
| `WEBUI_PATH` / `ADMIN_PATH` | Text | `/` | Web path where the control panel is served (e.g. `/admin`). When customized, `/` returns API health JSON. |
| `WEBUI_ENABLED` | Text | `true` | Set to `false` to completely disable the control WebUI |
| `API_KEY` | Secret | *(None)* | Client bearer authorization key (e.g. `sk-local-key`). Required if clients must authenticate. |
| `OPENCODE_ZEN_KEYS` | Secret | *(None)* | Your OpenCode Zen key(s). Multiple keys separated by commas. |
| `OPENCODE_GO_KEYS` | Secret | *(None)* | Your OpenCode Go key(s). Multiple keys separated by commas. |
| `CF_API_TOKEN` | Secret | *(None)* | Cloudflare API token with `Workers Scripts: Edit` permission for one-click in-panel updates |
| `CF_ACCOUNT_ID` | Text | *(Auto-discovered)* | Optional Cloudflare Account ID for updates (auto-discovered if token has access to one account) |
| `CF_WORKER_NAME` | Text | *(Inferred)* | Optional Worker script name (inferred from `*.workers.dev` subdomain or defaults to `opencode2api-proxy`) |
| `KILO_API_KEY` | Secret | *(None)* | Kilo Free Gateway key for zero-quota fallback |
| `KILO_API_BASE` | Text | `https://api.kilo.ai/v1` | Kilo API base URL |
| `UPSTREAM_ZEN` | Text | `https://opencode.ai/zen` | Zen upstream base URL |
| `UPSTREAM_GO` | Text | `https://opencode.ai/zen/go` | Go upstream base URL |
| `UPSTREAM_ANONYMOUS` | Text | `https://opencode.ai/inference` | Anonymous free upstream base URL |

Click **Save and deploy**.

#### Worker Control Panel

The built-in control panel provides a comprehensive management dashboard:

- **Access URL**: By default, navigate to `https://opencode2api-proxy.<your-subdomain>.workers.dev/` (or custom path like `/admin` if `WEBUI_PATH` is set).
- **Default Username**: `admin`
- **Default Password**: `admin`
- **30-Day Stateless Sessions**: HMAC-SHA256 signed tokens stored in secure HTTP-only cookies (`opencode2api_session`) that survive Worker cold starts and restarts.
- **Custom Path SPA Routing**: When `WEBUI_PATH="/admin"` is configured:
  - `GET /` serves `{ "name": "OpenCode2API", "status": "ok", "version": "1.2.0" }` (custom admin path remains private)
  - `GET /admin` serves the full interactive dashboard with seamless client-side SPA routing
  - All API routes (`/v1/chat/completions`, etc.) continue serving client requests cleanly
- **Interactive AI Chat Suite**: Real-time SSE streaming, tool call visualization, rich Markdown formatting, and split-pane file preview.
- **Theme Switcher**: Instant switching between System, Dark, and Light themes with persistent state.
- **One-Click Self-Updater**: Check for new releases and update the remote Worker deployment script directly from WebUI Settings with a scoped Cloudflare API token.

Your Cloudflare Worker API URL:

```
https://opencode2api-proxy.<your-subdomain>.workers.dev/v1
```

### Method 4: Docker & Self-Hosted (Coolify / Dokploy / Zeabur)

Deploy anywhere in 30 seconds with Docker or modern PaaS control panels.

#### Single Command Run

```bash
docker run -d \
  --name opencode2api \
  -p 8080:8080 -p 8081:8081 \
  -e OPENCODE_ZEN_KEYS="your-zen-key" \
  -e OPENCODE_GO_KEYS="your-go-key" \
  -e ADMIN_USERNAME="admin" \
  -e ADMIN_PASSWORD="your-secure-password" \
  --restart unless-stopped \
  node:26-alpine npx -y opencode2api-proxy start
```

#### Docker Compose (`docker-compose.yml`)

```yaml
services:
  opencode2api:
    image: node:26-alpine
    container_name: opencode2api
    command: npx -y opencode2api-proxy start
    ports:
      - "8080:8080"
      - "8081:8081"
    environment:
      - OPENCODE_ZEN_KEYS=your-zen-key
      - OPENCODE_GO_KEYS=your-go-key
      - ADMIN_USERNAME=admin
      - ADMIN_PASSWORD=your-secure-password
      - API_KEY=sk-your-client-key # Optional bearer token for clients
    restart: unless-stopped
```

## Model Catalog & Aliases

The router discovers the models OpenCode publishes on each tier, learns each model's native protocol from OpenCode's capability catalog, and auto-detects **rich attributes** (context window lengths, token limits, input/output modalities, and capabilities). Full **1M context windows** are preserved without down-tiering in free equivalents. You always request a **model id**, and the router picks the lane and the protocol.

| Requested model | Lane | Notes |
|---|---|---|
| `deepseek-v4.1-flash` | Zen or Go | Served by the tier that advertises it. |
| `glm-5.3` | Zen or Go | Served by the tier that advertises it. |
| `grok-4.6` | Zen or Go | Served by the tier that advertises it. |
| `kimi-k3` | Zen or Go | Served by the tier that advertises it. |
| `qwen3.8-max` | Zen or Go | Served by the tier that advertises it. |
| `claude-haiku-5-5` | Zen or Go | Native protocol is Anthropic Messages. |
| `*free` | Anonymous | Served on the anonymous lane when it is enabled. |

`GET /v1/models` lists everything the router can serve on both local daemon and Cloudflare Worker, including native protocols, context window limits, input/output modalities, and capabilities:

```bash
curl http://127.0.0.1:8080/v1/models -H "Authorization: Bearer sk-your-local-key"
```

## Client Integration

<details open>
<summary><b>Cursor & Windsurf IDE</b></summary>

Use OpenCode Zen & Go models inside Cursor as your primary coding and agent model:

1. Open **Cursor Settings** (`Ctrl+,` or `Cmd+,`) -> **Models**.
2. Under **OpenAI API Key**, toggle custom API key and click **Override OpenAI Base URL**.
3. Set URL and Key:
   - **Base URL**: `http://127.0.0.1:8080/v1` (or your Cloudflare Worker URL `https://your-worker.workers.dev/v1`)
   - **API Key**: `sk-your-local-key` (or dummy string if `API_KEY` is not set)
4. Add model IDs: `deepseek-v4.1-flash`, `glm-5.3`, `kimi-k3`, `qwen3.8-max`, `claude-haiku-5-5`.
5. Enable them in the model dropdown to code with full tool calling and streaming.

</details>

<details open>
<summary><b>Claude Code CLI</b></summary>

Point Anthropic's official terminal coding agent (`claude`) at your OpenCode router via native `/v1/messages`:

```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:8080"
export ANTHROPIC_AUTH_TOKEN="sk-your-local-key"
export ANTHROPIC_MODEL="claude-haiku-5-5" # or deepseek-v4.1-flash / glm-5.3
claude
```

</details>

<details open>
<summary><b>Cline, Roo Code & Continue.dev</b></summary>

In VS Code extension settings, select **OpenAI Compatible** or **Anthropic Compatible**:

```json
{
  "apiProvider": "openai",
  "openaiApiBase": "http://127.0.0.1:8080/v1",
  "openaiApiKey": "sk-your-local-key",
  "openaiModelId": "deepseek-v4.1-flash",
  "contextWindow": 1000000
}
```

*Note: OpenCode2API preserves full 1M context windows without truncation or forced down-tiering.*

</details>

<details>
<summary><b>OpenWebUI, LibreChat & SillyTavern</b></summary>

Configure as a custom OpenAI-compatible provider. The gateway serves dynamic model listings with rich attributes via `/v1/models`:

```bash
OPENAI_API_BASE_URL="http://127.0.0.1:8080/v1"
OPENAI_API_KEY="sk-your-local-key"
```

</details>

<details>
<summary><b>Python SDKs (OpenAI & Anthropic)</b></summary>

**OpenAI Python SDK:**
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="sk-your-local-key",
)

response = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": "Write a binary search in Python."}],
    stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta.content or "", end="")
```

**Anthropic Python SDK:**
```python
from anthropic import Anthropic

client = Anthropic(
    base_url="http://127.0.0.1:8080",
    api_key="sk-your-local-key",
)

message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain SSE streaming."}],
)
print(message.content[0].text)
```

</details>

<details>
<summary><b>Codex CLI</b></summary>

```toml
# ~/.codex/config.toml
model = "deepseek-v4.1-flash"
model_provider = "opencode2api"

[model_providers.opencode2api]
name = "OpenCode2API"
base_url = "http://127.0.0.1:8080/v1"
env_key = "OPENCODE2API_KEY"
wire_api = "responses"
```

</details>

<details>
<summary><b>OpenCode CLI</b></summary>

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "opencode2api": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "http://127.0.0.1:8080/v1",
        "apiKey": "sk-your-local-key"
      },
      "models": {
        "deepseek-v4.1-flash": { "name": "DeepSeek v4.1 Flash" }
      }
    }
  },
  "model": "opencode2api/deepseek-v4.1-flash"
}
```

</details>

<details>
<summary><b>Cherry Studio / LobeChat / NextChat</b></summary>

Add a custom OpenAI provider:

| Field | Value |
|---|---|
| API address | `http://127.0.0.1:8080/v1` |
| API key | `sk-your-local-key` |
| Model | `deepseek-v4.1-flash` |

</details>

<details>
<summary><b>Any OpenAI-compatible client</b></summary>

Point the client at `http://127.0.0.1:8080/v1` and use `sk-your-local-key` as the API key. Every OpenAI-compatible client works, because the router speaks the client's protocol.

</details>

## Architecture & Structure

```
OpenCode2API-Proxy/
├── assets/images/                # Vector logo suite, favicons, touch icons, and 1200x630 banner
├── src/
│   ├── types/
│   │   ├── config.ts             # Configuration, tier, protocol and log-level contracts
│   │   └── inference.ts          # The protocol-neutral bridge model
│   ├── config/
│   │   ├── defaults.ts           # Default configuration and the SOTA model list
│   │   ├── env-keys.ts           # Environment variable and .env parsing with auto-tier classification
│   │   ├── version.ts            # Semantic version and release configuration
│   │   ├── schema.ts             # The strict configuration schema
│   │   ├── normalize.ts          # The single validation point
│   │   ├── secrets.ts            # Masking, fingerprinting and redaction
│   │   └── store.ts              # Atomic configuration persistence
│   ├── protocol/
│   │   ├── identity.ts           # Session, message and project id derivation
│   │   ├── sha256.ts             # Portable SHA-256 for the Worker bundle
│   │   ├── decode-request.ts     # Client body -> bridge model
│   │   ├── encode-request.ts     # Bridge model -> upstream body
│   │   ├── response.ts           # Upstream body -> client body
│   │   ├── stream-parser.ts      # Upstream SSE -> bridge events
│   │   ├── stream-encoder.ts     # Bridge events -> client SSE
│   │   ├── collapse.ts           # SSE stream -> one response document
│   │   ├── tools.ts              # The v1 read gate and the v2 core tool gate
│   │   └── lanes.ts              # The v1 and v2 upstream lanes
│   ├── proxy/
│   │   ├── model-catalog.ts      # The discovered models and the routing rules
│   │   ├── model-discovery.ts    # The listings and the capability catalog
│   │   ├── model-metadata.ts     # Rich attribute normalization, context detection & capability parser
│   │   ├── catalog-refresh.ts    # The refresh timer
│   │   ├── attempt-runner.ts     # The key rotation and the cooldown
│   │   ├── request-shaping.ts    # The per-lane request shaping
│   │   └── delivery.ts           # The response relay and the conversion
│   ├── auth/
│   │   └── key-pool.ts           # The key pool with its cooldown
│   ├── unlimited/
│   │   ├── lane.ts               # DoH AAAA edge pool, /64 normalization & identity rotation
│   │   ├── guard.ts              # Quota-wall detector, /64 blacklist & self-healing hop loop
│   │   ├── doctor.ts             # Cloudflare egress verifier & health diagnostics
│   │   └── index.ts              # Public unlimited module exports
│   ├── update/
│   │   └── checker.ts            # GitHub Releases & npm registry update checker with SemVer comparator
│   ├── server/
│   │   ├── dispatcher.ts         # Route matching, CORS and client authentication
│   │   ├── gateway.ts            # The runtime that owns the pools and the catalog
│   │   ├── routes.ts             # Public API routes (/v1/*, /v1/unlimited/*, /healthz)
│   │   ├── completion-handler.ts # The core completion flow
│   │   ├── state-store.ts        # Atomic server state sidecar persistence (.opencode2api-state.json)
│   │   └── admin/                # Modular admin routes: config, key, update, upstream-key, views, session
│   ├── telemetry/
│   │   ├── metrics.ts            # The request counters, the latency and the usage
│   │   ├── log-broker.ts         # The log ring and the live subscribers
│   │   └── logger.ts             # The structured logger
│   ├── webui/
│   │   ├── document.ts           # Self-contained HTML with SEO/OpenGraph and theme mounts
│   │   ├── theme.ts              # OKLCH tokens for System, Dark, and Light themes
│   │   ├── script-chat-*.ts      # AI Chat composer, markdown, file preview, search, and state
│   │   ├── script-theme.ts       # Theme switcher controller and localStorage persistence
│   │   ├── script-update.ts      # Auto-update checker and Cloudflare Worker updater UI
│   │   ├── script-skeleton.ts    # Instant skeleton loading states across routes and panels
│   │   └── styles-*.ts           # Modular stylesheets adhering strictly to <=300 line ceiling
│   ├── cli/
│   │   ├── index.ts              # The CLI entrypoint
│   │   └── commands/start.ts     # The daemon command
│   └── worker/
│       ├── index.ts              # The Cloudflare Workers fetch entrypoint
│       ├── admin-update.ts       # Cloudflare Worker self-updater handlers
│       ├── cf-api.ts             # Cloudflare Client API for token verification and script deployment
│       ├── session.ts            # 30-day HMAC-SHA256 stateless session engine
│       ├── models.ts             # Enriched Worker /v1/models route with capabilities & context windows
│       └── unlimited.ts          # Worker self-healing guard, hop & doctor handlers
├── worker/
│   └── worker.js                 # Standalone Cloudflare Worker bundle (680.8 KB)
├── dist/
│   └── cli.js                    # Standalone Node.js CLI executable bundle (777.5 KB)
├── tests/                        # 266 automated unit & integration tests across 78 test suites
├── scripts/
│   ├── build.ts                  # The esbuild build pipeline
│   ├── build-release.ts          # The cross-platform archive builder
│   └── zip.ts                    # The dependency-free ZIP writer
├── .github/
│   └── workflows/
│       ├── test.yml              # The CI workflow with skip flags
│       └── release.yml           # The manual multi-OS draft release workflow
├── config.example.json
└── package.json
```

## Advanced Guides

### WebUI Control Panel & AI Chat Suite

The built-in WebUI provides a complete control plane and interactive AI Chat suite across all deployment environments (Local Daemon, Built Release, and Cloudflare Worker):

1. **Interactive AI Chat Panel**:
   - **Streaming Inference**: Real-time SSE token streaming, multi-turn message history, and live generation process indicators.
   - **Tool Call Visualization**: Live indicators showing upstream tool invocation and arguments execution.
   - **Navigation & Search**: Middle-left message jumping track, chronological timeline grouping, message jump navigation, and in-chat keyword search with highlight markers.
   - **Rich Markdown Rendering**: Code blocks with syntax styling and one-click copy, tables, checklists, callouts, and KaTeX math formatting.
2. **In-Place Markdown Composer**:
   - In-place rich-text editing with custom formatting context menu (clear formatting, headings, bold, code).
   - Custom modal hyperlink dialog preventing disruptive browser `window.prompt` popups.
3. **Split-Pane File Preview Panel**:
   - Responsive split-pane and mobile overlay preview for text, Markdown, HTML, CSV, and PDF documents.
   - Segmented toggle between rendered preview and raw IDE code mode with a line-number gutter.
   - Download options menu for direct file exports.
4. **Draft & Staging State Persistence**:
   - Unsent message drafts, conversation preview panel states, and staged file uploads persist in `localStorage` across page reloads.
   - Masked linear gradient edge fades for staged preview chips.
5. **Theme Switcher**:
   - Instant switcher supporting **System** (default auto-detection), **Dark**, and **Light** modes via an upward combobox menu in the sidebar footer.
   - Complete greyscale OKLCH light tokens applied across all cards, tables, popovers, and composer elements, with instant zero-flash loading.
6. **Instant Navigation & Monitoring**:
   - Instant skeleton loading placeholders across routes and views for smooth transitions.
   - Animated horizontal slide collapse toggle on sidebar navigation.
   - SVG metrics charts tracking request volume, token consumption, latency distribution, and multi-unit uptime format (days, weeks, months, years).

### Automatic Update System

OpenCode2API-Proxy includes an integrated update management pipeline that detects new releases and enables zero-downtime updates:

1. **Update Checker (`/api/update/check`)**:
   - Queries GitHub Releases for the latest version tag, falling back to the npm registry.
   - Caches results for 15 minutes to respect rate limits, with on-demand force-refresh support.
   - Displays new version notifications, release notes, and release asset listings directly within the WebUI Settings view.
2. **One-Click Cloudflare Worker Updater (`/api/update/apply`)**:
   - Deploys the latest pre-tested `worker/worker.js` bundle directly to your Cloudflare account without requiring Git, Wrangler, or command-line tools.
   - **Requirements**: A scoped Cloudflare API token with `Workers Scripts: Edit` permission (`CF_API_TOKEN`).
   - Automatically validates token status via Cloudflare API (`/user/tokens/verify`), auto-discovers your Account ID, and identifies the target Worker script name.
3. **Local Daemon Update Automation**:
   - **Git Clones**: Runs `git pull --ff-only && npm run build` and notifies the administrator to restart.
   - **Global npm**: Executes `npm install -g opencode2api-proxy@latest`.
   - **Release Archives**: Direct link to download the latest multi-arch binary archive from GitHub Releases.

### Protocol Conversion

The router sends a request in the **upstream's own protocol** and only converts when the client asked for a different one.

| Client endpoint | Upstream lane | What happens |
|---|---|---|
| `/v1/chat/completions` | v1 (Zen) | The body is sent as Chat Completions, with a `read` tool guaranteed. |
| `/v1/chat/completions` | v2 (Go) | The body is sent as Chat Completions, with the five core tools guaranteed. |
| `/v1/responses` | any | The body is sent as Responses, and the answer is converted back. |
| `/v1/messages` | any | The body is sent as Anthropic Messages, and the answer is converted back. |

A request to a different protocol than the upstream's is decoded into the bridge model, re-encoded for the upstream, and the answer is converted back on the way out. The same protocol on both sides is passed through untouched, so the common case costs nothing.

**The v1 read gate.** The v1 free tier requires a tool named `read`. A client tool that reads files (`read_file`, `ReadFile`, `read-text-file` and similar) is renamed to `read` on the wire, and the original name is restored in the answer.

**The v2 core tool gate.** The v2 free tier requires the five core tools `shell`, `edit`, `glob`, `grep` and `read`, and compares their description and parameter schema against the official CLI. The genuine definitions ship with the router, so a client that declares its own tools keeps them and the missing core tools are added.

### Key Rotation & Failure Handling

Put several keys in `zen_keys` or `go_keys` and the router distributes the requests across them.

1. **Round-robin**: Each request starts on a different key.
2. **Failure detection**: A 401, 403 or 429 rotates to the next key of the tier.
3. **Cooldown**: The failing key is held back with an exponential backoff, up to eight times the base cooldown. A longer `Retry-After` is honored in full.
4. **Immediate exit**: Any other 4xx is deterministic, so the router leaves the tier at once instead of burning the other keys.
5. **Tier fallback**: When the first tier is exhausted, the next tier in the prefer order takes over.
6. **Anonymous first**: A free model starts on the anonymous lane when `anonymous` is enabled, and falls back to the authenticated tiers when the anonymous lane rejects it.

### Unlimited Lane & Dual-Lane Architecture

OpenCode enforces strict rate limits and device quotas on free-tier inference (`[429]: Free usage limit reached`). OpenCode2API provides a dual-lane architecture to maintain high availability:

```text
Incoming Client Request
       │
       ▼
 ┌──────────────┐
 │ Quota Check  │
 └──────┬───────┘
        │
        ├────────────────────────────────────────────────┐
        ▼ (Lane A)                                       ▼ (Lane B)
 ┌───────────────────────────────┐              ┌─────────────────────────────────┐
 │ OpenCode v2.2.5 Direct Lane   │              │ Kilo Free Gateway Failover      │
 ├───────────────────────────────┤              ├─────────────────────────────────┤
 │ • Live DoH Cloudflare AAAA    │              │ • Zero-quota free tier models   │
 │ • cf.resolveOverride routing  │ ──(Quota ──► │ • Automatic secondary fallback  │
 │ • /64 block blacklist (200)   │    Wall)     │ • KILO_API_KEY / KILO_API_BASE  │
 │ • Clean device ID generation  │              └─────────────────────────────────┘
 │ • Auto-hop (up to 8 attempts) │
 └───────────────────────────────┘
```

1. **OpenCode v2.2.5 Direct Lane (`zen-lane` & `zen-guard`)**:
   - **Live DoH Edge Pool**: Resolves live `AAAA` records for `opencode.ai` via Cloudflare DNS-over-HTTPS (`1.1.1.1/dns-query`), falling back to verified Cloudflare IPv6 edge literals (`2606:4700:10::ac42:ad95`, `2606:4700:10::ac42:ad96`, `2606:4700:10::6814:2011`). On Cloudflare Workers, subrequests are steered directly via `cf.resolveOverride`.
   - **Self-Healing Auto-Hop**: When an upstream request hits a `429`, `403 FreeTierError`, or body containing `QuotaExceeded` / `Free usage limit reached`, the guard normalizes the edge to its `/64` prefix, blacklists it, generates a fresh device identity (`ses_`, `msg_`, 40-hex `project`, 32-hex `machineId`), and retries with a new edge (up to `8` hops transparently).
   - **Oldest-Block Recycling**: Blacklists up to 200 `/64` blocks. If all edges are blacklisted, it recycles the oldest block to prevent starvation.
2. **Kilo Free Gateway Failover**:
   - If direct OpenCode lanes are saturated or repeatedly blocked, configure `KILO_API_KEY` to enable instant fallback to high-throughput free models without quota limits.
3. **Diagnostic & Hop Endpoints**:
   - `GET /v1/unlimited/doctor` — Inspects outbound IPv6 `/64` egress, active edge and session identity, hop count, and blacklist telemetry.
   - `POST /v1/unlimited/hop` — Manually rotates to a fresh `/64` edge and identity immediately.

```bash
# Check unlimited lane & guard health
curl http://127.0.0.1:8080/v1/unlimited/doctor \
  -H "Authorization: Bearer sk-your-local-key"

# Manually hop to a fresh edge and device/session identity
curl -X POST http://127.0.0.1:8080/v1/unlimited/hop \
  -H "Authorization: Bearer sk-your-local-key"
```

### Environment Variables

Both the local daemon and Cloudflare Worker support environment variables. The local daemon automatically loads `.env` from the current working directory:

| Variable | Target | Default | Description |
|---|---|---|---|
| `OPENCODE2API_CONFIG` | Local | `./config.json` | Path to local JSON configuration file |
| `API_KEY` / `API_KEYS` | Both | *(None)* | Client authorization bearer token(s), comma-separated. Also accepts `OPENCODE2API_SERVER_KEY` or `SERVER_KEYS`. |
| `OPENCODE_ZEN_KEYS` | Both | *(None)* | Upstream OpenCode Zen keys, comma-separated. Also accepts `ZEN_KEYS` or `ZEN_KEY`. |
| `OPENCODE_GO_KEYS` | Both | *(None)* | Upstream OpenCode Go keys, comma-separated. Also accepts `GO_KEYS` or `GO_KEY`. |
| `OPENCODE_KEYS` | Both | *(None)* | Generic OpenCode keys, automatically classified into Zen or Go based on key prefix/content. |
| `ADMIN_USERNAME` | Both | `admin` | Username for the control WebUI |
| `ADMIN_PASSWORD` / `WEBUI_PASSWORD` | Both | `admin` | Password for the control WebUI (change from default in production!) |
| `WEBUI_PATH` / `ADMIN_PATH` | Both | `/` | Web path where the control panel is served (e.g. `/admin`). When set, `/` returns health JSON. |
| `WEBUI_ENABLED` | Both | `true` | Set to `false` to completely disable the control WebUI |
| `SESSION_TTL_MINUTES` | Both | `43200` | Admin session cookie lifetime in minutes (default 30 days = 43,200 min) |
| `CF_API_TOKEN` | Worker | *(None)* | Scoped Cloudflare API token (`Workers Scripts: Edit`) for one-click Worker in-panel updates |
| `CF_ACCOUNT_ID` | Worker | *(Auto)* | Cloudflare Account ID (auto-discovered if token has access to one account) |
| `CF_WORKER_NAME` | Worker | *(Inferred)* | Cloudflare Worker script name (inferred from subdomain or defaults to `opencode2api-proxy`) |
| `KILO_API_KEY` | Both | *(None)* | Kilo Free Gateway API key for secondary quota failover |
| `KILO_API_BASE` | Both | `https://api.kilo.ai/v1` | Kilo Free Gateway base API URL |
| `UPSTREAM_ZEN` | Both | `https://opencode.ai/zen` | Zen upstream base URL |
| `UPSTREAM_GO` | Both | `https://opencode.ai/zen/go` | Go upstream base URL |
| `UPSTREAM_ANONYMOUS` | Both | `https://opencode.ai/inference` | Anonymous free upstream base URL |

## Development & Testing

<!-- AUTO-GENERATED:SCRIPTS -->
| Command | Description |
|---|---|
| `npm run typecheck` | Run TypeScript compiler type checking (`tsc --noEmit`) |
| `npm test` | Run automated unit and integration test suite (`tsx --test tests/**/*.test.ts`) |
| `npm run build` | Bundle standalone CLI (`dist/cli.js`) and Cloudflare Worker (`worker/worker.js`) |
| `npm run verify:worker` | Verify `worker/worker.js` in a Cloudflare Workers global-scope sandbox and run handler smoke tests |
| `npm run build:release` | Build cross-platform release ZIP archives into `release/` |
| `npm run prepublishOnly` | Run typecheck, tests, bundle build, and Worker verification before publishing |
| `npm start` | Start the local proxy daemon directly from TypeScript source |
<!-- /AUTO-GENERATED:SCRIPTS -->

Run typecheck:

```bash
npm run typecheck
```

Run the automated test suite:

```bash
npm test
```

Build the standalone bundles:

```bash
npm run build
```

### Continuous Integration (CI)

Every commit and pull request runs automated verification through the [Test & Verify](.github/workflows/test.yml) GitHub Actions workflow (Node.js 26 LTS and TypeScript 7):

- **Typecheck**: `npm run typecheck`
- **Unit & Integration Tests**: `npm test` (266 automated tests across 78 suites)
- **Bundle Verification**: `npm run build`, plus a check that the Worker bundle carries no Node built-in.

#### Skipping Automated Tests

To skip the test suite on specific commits (e.g. for docs updates, asset additions, or fast iterations while still verifying types and builds), include any of the following tags in the commit message:

- `[skip test]` or `[skip tests]`
- `[skip-test]` or `[skip-tests]`

When triggered manually via **Actions** -> **Run workflow**, check the **Skip running automated tests** input option.

### Building & Publishing Releases

The [Release workflow](.github/workflows/release.yml) builds multi-arch platform binaries and the standalone Cloudflare Worker bundle, publishing them as a **Draft Release** on GitHub.

#### Trigger Options

1. **Manual Trigger (`workflow_dispatch`)**:
   - Go to **Actions** -> **Release** -> **Run workflow**.
   - **Tag**: Release tag (defaults to `v` + `version` from `package.json`, e.g. `v1.2.0`).
   - **Draft**: Create as Draft release (defaults to `true`). Uncheck when ready to publish publicly.
   - **Overwrite**: If a release or tag with this name already exists, delete and recreate it (defaults to `true`).
   - **Custom Release Notes**: Optional markdown text to use as release notes. Leave empty to use GitHub's auto-generated release notes.
   - **Skip tests**: Check to bypass test execution during release packaging.
2. **Automatic Trigger via Commit Flag**:
   - Push a commit to `master` containing `[release]`, `[draft-release]`, or `[release-draft]` in the commit message.
   - Automatically builds and publishes a Draft release for the current `package.json` version.

#### Release Assets

Each release attaches:
- 6 platform ZIP archives: `linux-x64`, `linux-arm64`, `win-x64`, `win-arm64`, `macos-x64`, `macos-arm64`.
- Standalone Cloudflare Worker script: `worker.js` (evaluated and pre-tested).

To build the release archives locally:

```bash
npm run build
npm run build:release
```

The archives land in `release/`.

## Disclaimer & Legal Notice

> **IMPORTANT**: Please read this notice carefully before using or deploying OpenCode2API-Proxy.

1. **Educational & Research Purposes Only**: This project is developed and distributed exclusively for personal educational, research, and non-commercial API interoperability testing purposes.
2. **Upstream Terms of Service**: Routing requests to OpenCode's Zen, Go or free tier through a third-party client may violate OpenCode's Terms of Service. The free tier explicitly restricts access to the official OpenCode client, and the Go tier requires a paid subscription. OpenCode may rate-limit, revoke keys, or suspend accounts that use the upstream outside its own client.
3. **No Warranty & No Guarantee**: The author and contributors make no claims, promises, or guarantees regarding the safety, status, or longevity of your OpenCode account or subscription. This software is provided "AS IS", without warranty of any kind, express or implied.
4. **Assumption of Risk**: You assume full and sole responsibility for any outcomes or damages resulting from using this software, including but not limited to account termination, loss of API access, or data loss. Use strictly at your own risk.
5. **Trademark Attribution**: All product names, logos, and brands (such as "OpenCode", "OpenAI", "Anthropic") are trademarks or registered trademarks of their respective owners. OpenCode2API-Proxy is an independent open-source project and is neither affiliated with, maintained by, nor endorsed by any of them.

## References & Acknowledgements

- [jasonxu114514/opencode2api](https://github.com/jasonxu114514/opencode2api) — Original reference repository for OpenCode API proxying and reverse engineering.
- [ElectronBreach/opencode-unlimited-usage](https://github.com/ElectronBreach/opencode-unlimited-usage) — Reference implementation for `AAAA` edge pool rotation, `/64` prefix blacklisting, and self-healing quota-wall recovery.

## License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. See the [LICENSE](./LICENSE) file for details.
