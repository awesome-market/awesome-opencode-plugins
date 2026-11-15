# opencode-ollama-multi-auth

[![npm version](https://img.shields.io/npm/v/opencode-ollama-multi-auth)](https://www.npmjs.com/package/opencode-ollama-multi-auth)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

OpenCode plugin for Ollama Cloud with multiple API keys and automatic failover. Never run out of API quota!

## Features

- **Multiple API Keys** - Add unlimited API keys from different Ollama Cloud accounts
- **Automatic Failover** - Automatically rotates to next key when current one fails (401, 403, 429)
- **Auto Recovery** - Re-enables failed keys after configurable fail window (default: 5 hours)
- **Dynamic Model Discovery** - Automatically discovers all available Ollama Cloud models (no manual model config needed)
- **TUI Notifications** - Toast notifications for key rotations, recovery, and exhaustion
- **Key Management Tools** - Built-in tools to list, switch, and reset API keys on the fly

## Installation

```bash
npm install -g opencode-ollama-multi-auth
```

## Configuration

Add the plugin to your `~/.config/opencode/opencode.json`:

```json
{
  "model": "ollama-multi/kimi-k3",
  "provider": {
    "ollama-multi": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "https://ollama.com/v1"
      }
    }
  },
  "plugin": [
    ["opencode-ollama-multi-auth", {
      "ollamaMultiAuth": {
        "keys": [
          "your-ollama-api-key-1",
          "your-ollama-api-key-2",
          "your-ollama-api-key-3"
        ]
      }
    }]
  ]
}
```

> Models are **auto-discovered** from Ollama Cloud — no need to list them manually.

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `keys` | string[] | [] | Array of API keys to rotate through |
| `failWindowMs` | number | 18000000 | Time in ms before retrying a failed key (default: 5 hours) |
| `notifications` | boolean | true | Show TUI toast notifications on key rotation, recovery, and errors |
| `autoDiscoverModels` | boolean | true | Automatically discover all available Ollama Cloud models (set to false to configure models manually) |
| `providerId` | string | "ollama-multi" | Provider ID to manage (for custom providers) |

## Environment Variables

You can also set keys via environment variables:

```bash
export OLLAMA_API_KEY="your-first-key"
export OLLAMA_API_KEY_1="your-second-key"
export OLLAMA_API_KEY_2="your-third-key"
```

Keys from environment variables are merged with config keys.

## How It Works

```
Request 1: Using Key #1 ✅ Success
Request 2: Using Key #1 ❌ Rate limited (429)
           ↓ Automatic rotation
Request 2: Using Key #2 ✅ Success
...
```

The plugin intercepts API requests and:
1. Uses the first available key from your list
2. Detects auth errors (401, 403, 429)
3. Marks failed key and rotates to next available key
4. Re-enables failed keys after the fail window expires

## State Files

The plugin manages these files automatically:
- `~/.local/share/opencode/auth.json` - Current active key
- `~/.opencode/ollama-keys-state.json` - Key failure history with timestamps

## Key Management Tools

The plugin registers tools you can invoke during a session:

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_ollama_keys` | List all keys with status (active, healthy, failed with recovery time) | none |
| `switch_ollama_key` | Manually switch to a specific key by index | `index` (1-based key index) |
| `reset_ollama_keys` | Clear failed status — optionally for a specific key | `index` (optional, resets all if omitted) |

## Testing

The plugin includes a mock server for testing key rotation:

```bash
cd node_modules/opencode-ollama-multi-auth
node scripts/mock-server.js
```

Then configure a test provider in opencode.json pointing to `http://127.0.0.1:11435/v1` with test keys.

## Available Models

All Ollama Cloud models are **auto-discovered** by default (cached for 15 minutes). Run `/models` in the TUI to see the full list.

To manually configure models instead, set `autoDiscoverModels: false` and add them to your provider config:

```json
"models": {
  "kimi-k3": { "id": "kimi-k3", "name": "Kimi K3" },
  "gemma4:31b": { "id": "gemma4:31b", "name": "Gemma 4 31B" }
}
```

## License

MIT License