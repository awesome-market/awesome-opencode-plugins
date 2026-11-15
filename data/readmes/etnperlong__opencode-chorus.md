<div align="center">

<img src="images/banner.webp" alt="opencode-chorus" width="100%" />

# opencode-chorus

> The [Chorus](https://github.com/Chorus-AIDLC/Chorus) integration plugin for [OpenCode](https://opencode.ai)

[![Version](https://img.shields.io/badge/Version-v0.16.4-blue?style=for-the-badge&logo=npm&logoColor=white)](https://www.npmjs.com/package/opencode-chorus)
[![License](https://img.shields.io/badge/License-AGPL--3.0-blue?style=for-the-badge&logo=open-source-initiative&logoColor=white)](./LICENSE)
[![With & For OpenCode](https://img.shields.io/badge/With_%26_For-OpenCode-000000?style=for-the-badge&labelColor=555555&logo=data:image/svg%2bxml;base64,PHN2ZyB3aWR0aD0nMjQwJyBoZWlnaHQ9JzMwMCcgdmlld0JveD0nMCAwIDI0MCAzMDAnIGZpbGw9J25vbmUnIHhtbG5zPSdodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2Zyc+PGcgY2xpcC1wYXRoPSd1cmwoI2NsaXAwXzE0MDFfODYyODMpJz48bWFzayBpZD0nbWFzazBfMTQwMV84NjI4Mycgc3R5bGU9J21hc2stdHlwZTpsdW1pbmFuY2UnIG1hc2tVbml0cz0ndXNlclNwYWNlT25Vc2UnIHg9JzAnIHk9JzAnIHdpZHRoPScyNDAnIGhlaWdodD0nMzAwJz48cGF0aCBkPSdNMjQwIDBIMFYzMDBIMjQwVjBaJyBmaWxsPSd3aGl0ZScvPjwvbWFzaz48ZyBtYXNrPSd1cmwoI21hc2swXzE0MDFfODYyODMpJz48cGF0aCBkPSdNMTgwIDI0MEg2MFYxMjBIMTgwVjI0MFonIGZpbGw9JyM0QjQ2NDYnLz48cGF0aCBkPSdNMTgwIDYwSDYwVjI0MEgxODBWNjBaTTI0MCAzMDBIMFYwSDI0MFYzMDBaJyBmaWxsPScjRjFFQ0VDJy8+PC9nPjwvZz48ZGVmcz48Y2xpcFBhdGggaWQ9J2NsaXAwXzE0MDFfODYyODMnPjxyZWN0IHdpZHRoPScyNDAnIGhlaWdodD0nMzAwJyBmaWxsPSd3aGl0ZScvPjwvY2xpcFBhdGg+PC9kZWZzPjwvc3ZnPg==&logoColor=white)](https://opencode.ai)

</div>

---

## What Is This?

[**Chorus**](https://github.com/Chorus-AIDLC/Chorus) is an agent harness for AI-Human collaboration, inspired by the [AI-Driven Development Lifecycle (AI-DLC)](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/) methodology. It coordinates Ideas, Proposals, Tasks, review gates, notifications, and multi-agent handoffs from requirements to delivery.

**opencode-chorus** is the community-maintained OpenCode integration. It loads Chorus workflow skills, exposes a lazy stateless MCP bridge, injects bounded runtime context, routes notifications, and automates three independent reviewer gates without pretending OpenCode sub-agent events are Chorus AgentSession lifecycle events.

## Features

| Category | Components | Description |
|---|---|---|
| **Runtime Hooks** | State Management, Lazy MCP Bridge, Context Injection, Notification Coordination | Activates Chorus on first bridge use, refreshes identity and tool context, injects bounded project guidance, and routes notifications. |
| **Review Agents** | Proposal Reviewer, Task Reviewer, Code Reviewer | Automatically dispatches read-only Proposal, Task, and aggregate Idea code reviews with structured verdicts. |
| **Workflow Skills** | 11 bundled skills synchronized with Chorus v0.16.4 | `chorus`, `chorus-brainstorm`, `chorus-docs`, `chorus-idea`, `chorus-openspec`, `chorus-orchestrate`, `chorus-proposal`, `chorus-develop`, `chorus-quick-dev`, `chorus-review`, `chorus-yolo` |

> [!NOTE]
> A local or online Chorus instance must be running and accessible to use this plugin. See [Chorus Quick Start](https://github.com/Chorus-AIDLC/Chorus#quick-start) to get one running.

For detailed component descriptions, see [docs/COMPONENTS.md](./docs/COMPONENTS.md).

## Quick Start

> [!TIP]
> This plugin is already included in the [Chorus upstream onboarding flow](https://github.com/Chorus-AIDLC/Chorus#connect-ai-agents). If you followed the Chorus setup guide for OpenCode, you can skip to step 2.

### 1. Install the Plugin

Add `opencode-chorus` to your OpenCode config file (usually `~/.config/opencode/opencode.json`):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-chorus"]
}
```

### 2. Configure Credentials

Create a `chorus.json` in your OpenCode config directory (`~/.config/opencode/chorus.json`) with the minimal configuration:

```json
{
  "chorusUrl": "http://localhost:8637",
  "apiKey": "your-chorus-api-key"
}
```

Or use environment variables:

```bash
export CHORUS_URL="http://localhost:8637"
export CHORUS_API_KEY="your-chorus-api-key"
```

### 3. Restart OpenCode

After installing and configuring, restart OpenCode. You will see the bundled Chorus skills in your workspace. Load the `chorus` skill to get started.

The plugin does not connect during OpenCode startup. It registers the four bridge tools immediately. First use refreshes Chorus identity/context, fetches the permission-filtered tool index through a request-scoped MCP client, starts notification listening, and enables prompt context injection. Every MCP list or execute operation opens and closes its own authenticated connection because Chorus `/api/mcp` is stateless.

For all configuration options (environment variables, `chorus.json` fields, state storage, observability settings), see [docs/CONFIGURATION.md](./docs/CONFIGURATION.md).

## Documentation

| Document | Description |
|---|---|
| [Configuration](./docs/CONFIGURATION.md) | Full configuration reference — env vars, `chorus.json`, state storage, observability |
| [Components](./docs/COMPONENTS.md) | Detailed descriptions of lifecycle hooks, review agents, and workflow skills |
| [Changelog](./docs/CHANGELOG.md) | Release history and migration notes |

## License

[AGPL-3.0](./LICENSE)
