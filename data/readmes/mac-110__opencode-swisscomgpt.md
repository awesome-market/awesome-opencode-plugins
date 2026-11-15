# opencode-swisscomgpt

SwisscomGPT provider for [OpenCode](https://github.com/anomalyco/opencode) - Access GPT-3.5, GPT-4, and GPT-5 via Swisscom's internal AI platform.

## Features

- 🚀 Access to GPT-5 and other models via Swisscom's GPU cluster
- 🔐 JWT-based authentication via gpt.swisscom.com
- 🔄 Full streaming support (SSE)
- 🛠️ Easy integration with OpenCode

## Installation

### From npm (when published)

```bash
npm install opencode-swisscomgpt
# or
bun add opencode-swisscomgpt
```

### From local source

```bash
# Clone and build
git clone https://github.com/mac-110/opencode-swisscomgpt.git
cd opencode-swisscomgpt
bun install
bun run build

# Install in OpenCode's config directory
cd ~/.config/opencode
bun add /path/to/opencode-swisscomgpt
```

## Prerequisites

You need a Swisscom employee account to use this provider.

### Getting your JWT Token

1. Log in to [gpt.swisscom.com](https://gpt.swisscom.com)
2. Open Browser DevTools (F12)
3. Go to the **Network** tab
4. Reload the page or make any request
5. Find a fetch request and look at the **Headers** tab
6. Copy the token from the `Authorization: Bearer <token>` header

## Configuration

### 1. Set Environment Variable

```bash
export SWISSCOMGPT_API_KEY="your-jwt-token"

# Or add to ~/.zshrc / ~/.bashrc for persistence
echo 'export SWISSCOMGPT_API_KEY="your-jwt-token"' >> ~/.zshrc
```

### 2. OpenCode Config

Add the provider to your `~/.config/opencode/opencode.json`:

```json
{
  "provider": {
    "swisscomgpt": {
      "npm": "opencode-swisscomgpt",
      "env": ["SWISSCOMGPT_API_KEY"],
      "options": {
        "baseURL": "https://api.rastro.icp.swisscom.com"
      },
      "models": {
        "gpt-5": {
          "name": "GPT-5",
          "id": "gpt-5",
          "attachment": true,
          "tool_call": true,
          "temperature": true,
          "cost": { "input": 0, "output": 0 },
          "limit": { "context": 128000, "output": 16384 },
          "modalities": { "input": ["text"], "output": ["text"] }
        },
        "gpt-5-instant": {
          "name": "GPT-5 Instant",
          "id": "gpt-5-instant",
          "attachment": true,
          "tool_call": true,
          "temperature": true,
          "cost": { "input": 0, "output": 0 },
          "limit": { "context": 128000, "output": 16384 },
          "modalities": { "input": ["text"], "output": ["text"] }
        },
        "gpt-5-thinking": {
          "name": "GPT-5 Thinking",
          "id": "gpt-5-thinking",
          "reasoning": true,
          "attachment": true,
          "tool_call": true,
          "temperature": true,
          "cost": { "input": 0, "output": 0 },
          "limit": { "context": 128000, "output": 32768 },
          "modalities": { "input": ["text"], "output": ["text"] }
        },
        "gpt-4-turbo": {
          "name": "GPT-4 Turbo",
          "id": "gpt-4-turbo",
          "attachment": true,
          "tool_call": true,
          "temperature": true,
          "cost": { "input": 0, "output": 0 },
          "limit": { "context": 128000, "output": 4096 },
          "modalities": { "input": ["text"], "output": ["text"] }
        }
      }
    }
  },
  "model": "swisscomgpt/gpt-5",
  "small_model": "swisscomgpt/gpt-4-turbo"
}
```

> **Important:** OpenCode requires explicit model definitions in the `models` object. Each model you want to use must be defined with its capabilities and limits.

### Model Configuration Reference

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name in OpenCode |
| `id` | string | API model identifier |
| `tool_call` | boolean | Supports function calling |
| `reasoning` | boolean | Model has reasoning/thinking capability |
| `attachment` | boolean | Supports file attachments |
| `temperature` | boolean | Supports temperature parameter |
| `cost.input` | number | Cost per 1M input tokens (USD) |
| `cost.output` | number | Cost per 1M output tokens (USD) |
| `limit.context` | number | Max context window size |
| `limit.output` | number | Max output tokens |
| `modalities.input` | array | Supported input types: `text`, `image`, `audio` |
| `modalities.output` | array | Supported output types: `text`, `image`, `audio` |

## Available Models

### GPT-5 Models
| Model ID | Description |
|----------|-------------|
| `gpt-5` | Default GPT-5 model |
| `gpt-5-instant` | ⚡ Fastest replies, no deep thought |
| `gpt-5-thinking-mini` | 💡 Light, efficient reasoning |
| `gpt-5-thinking` | 🧠 Slower, more detailed reasoning |

### GPT-4 Models (Legacy)
| Model ID | Description |
|----------|-------------|
| `gpt-4o` | Great for general tasks |
| `gpt-4o-mini` | Faster for simple tasks |
| `gpt-4-turbo` | High performance |
| `gpt-4.1` | Optimized for coding |

### Reasoning Models
| Model ID | Description |
|----------|-------------|
| `o3` | Advanced reasoning model |
| `o3-mini` | Fast reasoning model |

### Claude
| Model ID | Description |
|----------|-------------|
| `claude-3.5-sonnet` | Great for creative writing and code |

### Swiss Models 🇨🇭
| Model ID | Description |
|----------|-------------|
| `apertus` | Swiss-trained open model |
| `llama-4-scout` | Large context model |

## Usage with OpenCode

```bash
# Verify models are available
opencode models swisscomgpt

# Start OpenCode (uses configured default model)
opencode

# Switch model in session
/model swisscomgpt/gpt-5-thinking
```

## Programmatic Usage

You can also use this provider directly in your code:

```typescript
import { createSwisscomGPT } from 'opencode-swisscomgpt';
import { generateText } from 'ai';

const swisscomgpt = createSwisscomGPT({
  apiKey: process.env.SWISSCOMGPT_API_KEY!,
});

const { text } = await generateText({
  model: swisscomgpt('gpt-5'),
  prompt: 'Explain quantum computing in simple terms.',
});

console.log(text);
```

### With Streaming

```typescript
import { createSwisscomGPT } from 'opencode-swisscomgpt';
import { streamText } from 'ai';

const swisscomgpt = createSwisscomGPT({
  apiKey: process.env.SWISSCOMGPT_API_KEY!,
});

const result = await streamText({
  model: swisscomgpt('gpt-5'),
  prompt: 'Write a short story about AI.',
});

for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
```

## API Reference

### `createSwisscomGPT(config)`

Creates a SwisscomGPT provider instance compatible with Vercel AI SDK.

#### Config Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiKey` | `string` | required | JWT Bearer token from gpt.swisscom.com |
| `baseURL` | `string` | `https://api.rastro.icp.swisscom.com` | API base URL |
| `threadId` | `string` | auto-generated | UUID for conversation continuity |
| `policy` | `string` | `SKIP` | API policy parameter |

## How It Works

This provider wraps `@ai-sdk/openai-compatible` and transforms requests for SwisscomGPT's API:

1. **URL Transformation**: `/v1/chat/completions` → `/v2/chat/completions/{threadId}?policy=SKIP`
2. **Authentication**: Uses JWT Bearer token in Authorization header
3. **Thread ID**: Auto-generates UUID per request for conversation tracking

## Troubleshooting

### "Provider not found: swisscomgpt"

1. Make sure the package is installed in `~/.config/opencode/node_modules/`
2. Verify your `opencode.json` has explicit model definitions
3. Check that the package is built (`dist/` folder exists)

### Token Expired

JWT tokens from gpt.swisscom.com expire after ~24h. Get a fresh token from the browser.

### Network Errors

Make sure you're connected to the Swisscom network (VPN if remote).

## Security Notes

- Never commit your JWT token to version control
- Use environment variables for the API key
- Tokens are tied to your personal Swisscom account

## Contributing

Contributions welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

## License

MIT © Swisscom / Alexander Schäfer

---

Made with ❤️ for Swisscom developers
