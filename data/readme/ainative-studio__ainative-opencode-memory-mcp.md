# ainative-opencode-memory-mcp

**Persistent memory for [OpenCode](https://opencode.ai) agents.** OpenCode is stateless — it forgets everything between sessions. This MCP server gives your OpenCode coding agent **long-term memory** powered by [AINative ZeroDB](https://ainative.studio/opencode?utm_source=npm&utm_medium=mcp&utm_campaign=opencode-memory): store a codebase's decisions, conventions, and gotchas once, and recall them in every future session.

## Why

OpenCode restarts with a blank slate every time. Your agent re-learns your architecture, re-asks the same questions, re-makes the same mistakes. With this MCP, it remembers:

- Architecture & design decisions
- Naming conventions and code style
- Gotchas, workarounds, and "don't touch X" rules
- User/team preferences

## Install

```bash
npm install -g ainative-opencode-memory-mcp
```

## Setup (OpenCode)

1. **Get a free API key** → [ainative.studio/signup](https://ainative.studio/signup?utm_source=npm&utm_medium=mcp&utm_campaign=opencode-memory) (Hobbyist $5/mo, 7-day free trial).
2. Add to your OpenCode MCP config (`opencode.json` / MCP settings):

```json
{
  "mcpServers": {
    "ainative-memory": {
      "command": "npx",
      "args": ["-y", "ainative-opencode-memory-mcp"],
      "env": { "AINATIVE_API_KEY": "your-key-here" }
    }
  }
}
```

## Tools

| Tool | What it does |
|------|--------------|
| `opencode_store_memory` | Remember a fact/decision/snippet (optional tags) |
| `opencode_search_memory` | Semantic search over everything remembered |
| `opencode_recall_context` | Reload relevant memories at the start of a task |
| `opencode_memory_stats` | How many memories are stored |
| `opencode_clear_memory` | Wipe memories (optionally by tag) |

## Example

At the start of a session, have your agent call `opencode_recall_context` with the file/task you're working on — it reloads what it knew. As you work, `opencode_store_memory` captures new decisions. Next session, it all comes back.

## Environment

| Var | Default | Notes |
|-----|---------|-------|
| `AINATIVE_API_KEY` | — | **Required.** Free at ainative.studio |
| `OPENCODE_MEMORY_NAMESPACE` | `opencode` | Isolate memories per project |
| `AINATIVE_API_URL` | `https://api.ainative.studio` | Override for self-host |

---

Built by [AINative Studio](https://ainative.studio/opencode?utm_source=npm&utm_medium=mcp&utm_campaign=opencode-memory) — the AI-native dev platform with 65+ models, one OpenAI-compatible endpoint, and persistent agent memory. MIT licensed.
