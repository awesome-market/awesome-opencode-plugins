# opencode-register-provider

🌟 Interactive CLI tool to register OpenAI-compatible providers to OpenCode.ai with auto-fetch models from `/v1/models` endpoint.

[![npm version](https://badge.fury.io/js/opencode-register-provider.svg)](https://badge.fury.io/js/opencode-register-provider)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features ✨

- 🎯 **Interactive prompts** - guided setup for provider configuration
- 🔍 **Auto-fetch models** - automatically fetch model list from `/v1/models` endpoint
- ✅ **Flexible selection** - select specific models, ranges, or all
- 📦 **Auto-configure** - generates `opencode.jsonc` automatically
- 🔐 **Configuration** - API keys are stored in `opencode.jsonc` configuration file
- 🚀 **Zero manual editing** - no need to touch config files manually

## Installation

```bash
npm install -g opencode-register-provider
```

## Usage

Simply run:

```bash
opencode-register-provider
```

The tool will guide you through an interactive setup process.

## Interactive Flow

The script will ask you:

1. **Provider ID** - unique identifier (kebab-case, e.g., `openrouter`, `together-ai`)
2. **Provider display name** - name shown in the UI
3. **Base URL** - API endpoint (e.g., `https://openrouter.ai/api/v1`)
4. **API Key** - authentication key from the provider
5. **Model selection** - choose models from the fetched list:
   - Comma-separated: `1,3,5,7`
   - Range: `1-10`
   - All: `all`
6. **Model naming** - bulk naming or custom per-model
7. **Confirmation** - review config before saving

## Example Session

```
🌟 OpenCode.ai - OpenAI-Compatible Provider Registration

Provider ID (lowercase, kebab-case): openrouter
Provider display name (default "openrouter"): OpenRouter
Base URL: https://openrouter.ai/api/v1
API Key: sk-or-v1-…xxxx

🔍 Fetching models from provider...

✅ Found 127 models

Available models:
  [1] anthropic/claude-3.5-sonnet
  [2] openai/gpt-4-turbo
  [3] meta-llama/llama-3.1-70b-instruct
  ...

Select models (comma-separated, range, or "all"): 1-5

📦 Selected 5 model(s)

Use same display name format for all? (y/n): y

📂 Config file: /home/user/project/opencode.jsonc

📝 Configuration to be applied:
...

Apply this configuration? (y/n): y

🚀 Saving configuration...

✅ Provider registered successfully!

💡 Next steps:
1. Run OpenCode in your project directory: opencode
2. Select a model with: /models
3. Look for models from "OpenRouter"
```

## Prerequisites

- Node.js >= 14.0.0
- OpenCode.ai installed and initialized in your project (`opencode init`)

## Config Structure

This tool generates configuration following the [OpenCode.ai provider specification](https://opencode.ai/docs/providers):

### opencode.jsonc (Project or Global Config)

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "custom-provider-id": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Provider Display Name",
      "options": {
        "baseURL": "https://api.provider.com/v1"
      },
      "models": {
        "model-id-1": {
          "name": "Model 1 Display Name"
        }
      }
    }
  }
}
```

## Compatible Providers

This tool is compatible with **any provider following the OpenAI API specification** that provides a `/v1/models` endpoint:

### ✅ Tested & Verified

- OpenRouter
- Together AI
- Fireworks AI
- DeepInfra
- Anyscale
- Perplexity API
- OpenAI (official)
- Groq
- Replicate

### ✅ Self-Hosted / Local

- LocalAI
- vLLM
- Text Generation WebUI
- Ollama (with OpenAI compatibility layer)
- LM Studio
- Jan
- Atomic Chat

### ✅ Enterprise / Custom

- Azure OpenAI (custom endpoint)
- AWS Bedrock (via proxy)
- GCP Vertex AI (via proxy)
- Custom internal APIs

## Config File Priority

OpenCode searches for config files with the following priority:

1. `./opencode.jsonc` (current directory - **recommended**, highest priority)
2. `./opencode.json` (current directory - backward compatibility)
3. `~/.config/opencode/opencode.jsonc` (global config)
4. `~/.config/opencode/opencode.json` (global config - backward compatibility)

The tool automatically detects and updates existing configs, or throws an error if no config file is found.

## Troubleshooting

### ❌ Error: Failed to fetch models

**Possible causes:**
- Base URL incorrect or missing `/v1` path
- API key invalid or expired
- Network connectivity issues
- Provider endpoint down

**Solutions:**
- Verify base URL format: `https://api.provider.com/v1`
- Test API key with curl:
  ```bash
  curl -H "Authorization: Bearer YOUR_KEY" https://api.provider.com/v1/models
  ```
- Check provider documentation for correct endpoint

### ❌ No OpenCode config file found

The tool requires an existing `opencode.jsonc` or `opencode.json` file. Run:

```bash
opencode init
```

in your project directory to create one.

### ❌ Models not showing in OpenCode

**Solutions:**
- Verify config saved correctly: `cat opencode.jsonc`
- Restart OpenCode terminal
- Run `/models` command in OpenCode TUI

## Security Notes

- ⚠️ **Do not commit** `opencode.jsonc` - it now contains your API keys directly. Ensure it is added to your `.gitignore`.

## Examples: Popular Providers

### OpenRouter

```
Provider ID: openrouter
Base URL: https://openrouter.ai/api/v1
API Key: sk-or-v1-…
```

### Together AI

```
Provider ID: together-ai
Base URL: https://api.together.xyz/v1
API Key: …
```

### Groq

```
Provider ID: groq
Base URL: https://api.groq.com/openai/v1
API Key: gsk_…
```

### LocalAI (Self-hosted)

```
Provider ID: localai
Base URL: http://localhost:8080/v1
API Key: (leave blank or dummy key if auth disabled)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT © [Fahmi Amaru](https://github.com/me-fahmi)

## Related Links

- [OpenCode.ai Documentation](https://opencode.ai/docs)
- [OpenCode.ai Providers Guide](https://opencode.ai/docs/providers)
- [Models.dev - Provider Directory](https://models.dev)
- [AI SDK Documentation](https://ai-sdk.dev/)

---

**Built for:** OpenCode.ai  
**Compatible with:** Any OpenAI-compatible API endpoint
