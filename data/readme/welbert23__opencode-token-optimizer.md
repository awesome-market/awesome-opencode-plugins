# OpenCode Token Optimizer

Project-level configuration to reduce token consumption in OpenCode.

## Folder Structure

```
opencode agent/
│
├── opencode.json                     # Main config — compaction, limits, plugin, agents
├── package.json                      # npm package (for opencode-token-optimizer)
├── package-lock.json
├── README.md
│
├── .opencode/
│   ├── agents/
│   │   └── quick.md                  # Subagent for trivial/quick tasks
│   │
│   ├── skills/
│   │   └── token-saver/
│   │       └── SKILL.md              # Skill with token-saving strategies
│   │
│   └── token-optimizer.json          # opencode-token-optimizer plugin config
│
└── node_modules/
    └── opencode-token-optimizer/     # Installed plugin
```

## How Token Limiting Works

Source: `overflow.ts` (opencode core)

### Compaction Trigger Formula

```
usable = limit.input - reserved

With limit.input set:
  usable = limit.input - reserved
  If reserved = 8000, input = 25000:
    usable = 25000 - 8000 = 17,000 tokens

Without limit.input (default):
  usable = context - maxOutputTokens
  If context = 200000, maxOutput = 32000:
    usable = 200000 - 32000 = 168,000 tokens
```

Compaction triggers when `current_tokens >= usable`.

### UI Percentage Formula

```
percent = current_tokens / usable * 100
```

## Token Reduction Comparison

| Level | `input` | `reserved` | Usable | vs Default (168K) | Messages before compaction |
|-------|---------|------------|--------|-------------------|---------------------------|
| Default (no limit) | — | 20K | ~168K | — | ~10-15 messages |
| Light | 150K | 8K | 142K | ~15% reduction | ~8-12 messages |
| Medium | 80K | 8K | 72K | ~57% reduction | ~4-6 messages |
| Aggressive | 40K | 8K | 32K | ~81% reduction | ~2-3 messages |
| **Ultra (current)** | **25K** | **8K** | **17K** | **~90% reduction** | **~1-2 messages** |

## Configuration Files

### `opencode.json` — Main Config

| Setting | Value | Effect |
|---------|-------|--------|
| `compaction.auto` | `true` | Enable automatic compaction |
| `compaction.prune` | `true` | Remove old tool outputs |
| `compaction.reserved` | `8000` | Buffer before compaction (default: 20K) |
| `tool_output.max_lines` | `100` | Limit tool output lines |
| `tool_output.max_bytes` | `4096` | Limit tool output size |

Model limits applied to all 50 OpenCode Zen models:
- **Free models**: `input: 25000`, `output: 8K-16K`
- **GPT models**: `input: 25000`, `output: 16K-32K`
- **Claude models**: `input: 25000`, `output: 16K`
- **Gemini models**: `input: 25000`, `output: 16K`
- **Others (DeepSeek, GLM, MiniMax, Kimi, Qwen, Grok)**: `input: 25000`, `output: 16K`

### `.opencode/agents/quick.md` — Quick Task Agent

Subagent for trivial tasks (typos, renames, version bumps). Limited permissions (`edit: allow`, `bash: deny`) with a focused prompt to save context.

### `.opencode/skills/token-saver/SKILL.md` — Token Saver Skill

Auto-loaded skill providing token-saving strategies whenever the user asks about reducing tokens.

### `token-optimizer.json` — Plugin Config

6 optimization patterns (all enabled):
1. **Precise Task Prompts** — better subagent delegation
2. **Anti-Duplication Guard** — prevent repeated work
3. **Single-Concern Validation** — one task at a time
4. **Quick Category Routing** — trivial tasks to cheap model
5. **Pre-Computation Guidance** — resolve paths before spawning agents
6. **Cut Explore Agent** — use direct tools instead

## Usage

1. Restart OpenCode after editing any config file
2. For trivial tasks, use: `task(agent="quick", ...)`
3. To change the token limit level, edit `limit.input` in `opencode.json`:
   - Ultra: 25000 | Aggressive: 40000 | Medium: 80000 | Light: 150000

## Compatibility

- Covers all 50 OpenCode Zen models
- Works with the `opencode` provider (`opencode/model-id`)
