# @mac110/opencode-openai-compatible

OpenAI-compatible provider plugin for [OpenCode](https://opencode.ai) — connect any OpenAI-compatible API endpoint such as kiro-gateway, LiteLLM, LocalAI, Ollama, and more.

## Installation

Add to `~/.config/opencode/package.json`:

```json
{
  "dependencies": {
    "@mac110/opencode-openai-compatible": "latest"
  }
}
```

Then install:

```bash
cd ~/.config/opencode && bun install
```

## Configuration

Add the provider to `~/.config/opencode/config.json`.

### API Key via environment variable (recommended)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "myprovider": {
      "npm": "@mac110/opencode-openai-compatible",
      "env": ["MY_API_KEY"],
      "options": {
        "baseURL": "http://localhost:8888/v1"
      },
      "models": { ... }
    }
  }
}
```

```bash
export MY_API_KEY="your-api-key"
```

### API Key directly in config

You can also put the API key directly in `options.apiKey` — useful for local gateways where security is not a concern:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "myprovider": {
      "npm": "@mac110/opencode-openai-compatible",
      "options": {
        "baseURL": "http://localhost:8888/v1",
        "apiKey": "your-api-key"
      },
      "models": { ... }
    }
  }
}
```

## Example: kiro-gateway (full model list)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "kiro": {
      "npm": "@mac110/opencode-openai-compatible",
      "options": {
        "baseURL": "http://192.168.1.100:8888/v1",
        "apiKey": "your-kiro-gateway-token"
      },
      "models": {
        "auto": {
          "id": "auto",
          "name": "Auto",
          "modalities": { "input": ["text", "image"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 0, "output": 0 },
          "limit": { "context": 200000, "output": 8192 }
        },
        "claude-opus-4.6": {
          "id": "claude-opus-4.6",
          "name": "Claude Opus 4.6",
          "modalities": { "input": ["text", "image"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 15, "output": 75 },
          "limit": { "context": 200000, "output": 32000 }
        },
        "claude-sonnet-4.6": {
          "id": "claude-sonnet-4.6",
          "name": "Claude Sonnet 4.6",
          "modalities": { "input": ["text", "image"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 3, "output": 15 },
          "limit": { "context": 200000, "output": 16000 }
        },
        "claude-opus-4.5": {
          "id": "claude-opus-4.5",
          "name": "Claude Opus 4.5",
          "modalities": { "input": ["text", "image"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 15, "output": 75 },
          "limit": { "context": 200000, "output": 32000 }
        },
        "claude-sonnet-4.5": {
          "id": "claude-sonnet-4.5",
          "name": "Claude Sonnet 4.5",
          "modalities": { "input": ["text", "image"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 3, "output": 15 },
          "limit": { "context": 200000, "output": 16000 }
        },
        "claude-sonnet-4": {
          "id": "claude-sonnet-4",
          "name": "Claude Sonnet 4",
          "modalities": { "input": ["text", "image"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 3, "output": 15 },
          "limit": { "context": 200000, "output": 16000 }
        },
        "claude-haiku-4.5": {
          "id": "claude-haiku-4.5",
          "name": "Claude Haiku 4.5",
          "modalities": { "input": ["text", "image"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 0.8, "output": 4 },
          "limit": { "context": 200000, "output": 8192 }
        },
        "deepseek-3.2": {
          "id": "deepseek-3.2",
          "name": "DeepSeek 3.2",
          "modalities": { "input": ["text"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 0, "output": 0 },
          "limit": { "context": 128000, "output": 8192 }
        },
        "minimax-m2.5": {
          "id": "minimax-m2.5",
          "name": "MiniMax M2.5",
          "modalities": { "input": ["text"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 0, "output": 0 },
          "limit": { "context": 128000, "output": 8192 }
        },
        "minimax-m2.1": {
          "id": "minimax-m2.1",
          "name": "MiniMax M2.1",
          "modalities": { "input": ["text"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 0, "output": 0 },
          "limit": { "context": 128000, "output": 8192 }
        },
        "qwen3-coder-next": {
          "id": "qwen3-coder-next",
          "name": "Qwen3 Coder Next",
          "modalities": { "input": ["text"], "output": ["text"] },
          "temperature": true,
          "tool_call": true,
          "cost": { "input": 0, "output": 0 },
          "limit": { "context": 128000, "output": 8192 }
        }
      }
    }
  },
  "model": "kiro/claude-opus-4.6",
  "small_model": "kiro/claude-haiku-4.5"
}
```

## Example: Ollama

```json
{
  "provider": {
    "ollama": {
      "npm": "@mac110/opencode-openai-compatible",
      "options": {
        "baseURL": "http://localhost:11434/v1",
        "apiKey": "ollama"
      },
      "models": {
        "llama3": {
          "id": "llama3",
          "name": "Llama 3",
          "modalities": { "input": ["text"], "output": ["text"] },
          "temperature": true,
          "tool_call": false,
          "cost": { "input": 0, "output": 0 },
          "limit": { "context": 8192, "output": 4096 }
        }
      }
    }
  }
}
```

## Model fields reference

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Model ID sent to the API |
| `name` | string | Display name in OpenCode |
| `modalities.input` | array | `"text"`, `"image"`, `"audio"`, `"video"`, `"pdf"` |
| `modalities.output` | array | `"text"`, `"image"`, `"audio"` |
| `temperature` | boolean | Whether temperature control is supported |
| `tool_call` | boolean | Whether tool/function calling is supported |
| `cost.input` | number | Cost per million input tokens (USD) |
| `cost.output` | number | Cost per million output tokens (USD) |
| `limit.context` | number | Max context window (tokens) |
| `limit.output` | number | Max output tokens |

## License

MIT
