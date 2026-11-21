# sm-ailib 

Cross-client **MCP (Model Context Protocol) server + local skill bundle** for text-only AI models.

Adds three capabilities with near-zero token overhead:

1. **Persistent memory** — `@sm-ailib_save <content>` / `@sm-ailib_recall <query>`.
2. **Zero-cost image generation** — `@sm_ailib_img <prompt>` via Pollinations AI, saved locally.
3. **Granular token-budget modes** — `@sm_ailib_0` … `@sm_ailib_5` (Lazy → Minimal Senior Dev → Standard → Max Reasoning → Max Audit).

## Layout

```
sm-ailib/
  server.js            MCP server (Node + @modelcontextprotocol/sdk, stdio)
  plugin/server.js     OpenCode server plugin: enforces per-mode maxTokens + system rules
  skill/SKILL.md       Skill: triggers, modes, token rules, image rule
  config/opencode.mcp.jsonc   OpenCode MCP server snippet
  config/claude_desktop_config.json Claude Desktop MCP snippet
  install.mjs          Installer: merges MCP/plugin config, installs skill + plugin, writes Claude config
  test/                MCP client test harness
```

## Run

```sh
npm install
node server.js
```

## Tools

| Tool | Purpose |
|---|---|
| `sm_ailib_save` | Persist content into `<SM_AILIB_HOME>/memory.json`. |
| `sm_ailib_recall` | Recall entries (`query`, `limit`) from memory. |
| `sm_ailib_img` | Generate via `https://image.pollinations.ai/prompt/<prompt>` → save to `<SM_AILIB_HOME>/images/`. |
| `sm_ailib_level` | Get/set mode 0–5; returns `maxTokens` + `rules`. |

## OpenCode

- MCP: `opencode.json` → `mcp.servers."sm-ailib"` (local, stdio, env `SM_AILIB_HOME`).
- Plugin: `./plugins/sm-ailib` → enforces `session.hook("context")` maxTokens/system per mode.
- Skill: `~/.agents/skills/sm-ailib/SKILL.md`.

## Claude Desktop / Claude Code

- MCP: `claude_desktop_config.json` → `mcpServers."sm-ailib"` (local stdio, node + server.js).

## Modes summary

- `@sm_ailib_0` Strict Lazy — 256 tokens, one sentence.
- `@sm_ailib_1`/`@sm_ailib_2` Minimal Senior Dev — 2048/4096 tokens, direct code edits, no fluff.
- `@sm_ailib_3` Standard — 8192 tokens.
- `@sm_ailib_4` Maximum Reasoning — 16384 tokens.
- `@sm_ailib_5` Maximum Audit — 32768 tokens, full reasoning + audit.

## Limits

- Memory keeps the last 200 entries.
- Image generation depends on Pollinations AI availability.
- Token enforcement on Anthropic-style providers uses semantic `maxTokens`; providers without support may need the user's own wiring.
