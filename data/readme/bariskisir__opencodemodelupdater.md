# OpenCode Model Updater

[![npm version](https://img.shields.io/npm/v/opencode-model-updater.svg)](https://www.npmjs.com/package/opencode-model-updater)

CLI tool that automatically fetches and updates [OpenCode](https://opencode.ai) configuration with the latest models from supported providers.

New models added to provider APIs can take time to appear in [models.dev](https://models.dev/model-schema.json). This tool automatically syncs all available models from your chosen providers and updates `opencode.json` instantly—enabling you to use any model immediately without waiting.

## Features

- Automatically updates all available models from 24 OpenAI-compatible providers
- Updates or creates `~/.config/opencode/opencode.json` with latest model data
- Supports Windows, Linux, and macOS
- Preserves existing provider configurations during updates
- Creates automatic timestamped backups before each update
- Removes auto-generated provider entries from config with `--remove`

## Usage

```bash
npx opencode-model-updater [options]
```

### Options

| Option | Default | Description |
|---|---|---|
| `--provider <name>` | `all` | Specific provider(s) to update (comma-separated names or `all`) |
| `--remove [names]` | | Remove auto-generated provider entries (comma-separated names, or omit to remove all) |
| `--version` | | Display version number |
| `--help` | | Show help message |
| `--list` | | List all available providers |

### Supported Providers

| Provider | Description |
|---|---|
| `openrouter` | [OpenRouter](https://openrouter.ai) - Access 600+ LLMs through a single API |
| `aihubmix` | [AIHubMix](https://aihubmix.com) - Multi-provider model gateway with 600+ models |
| `ollamacloud` | [Ollama Cloud](https://ollama.com) - Run open-source models on your own cloud |
| `nvidia` | [Nvidia](https://api.nvidia.com) - Nvidia NIM models |
| `abacus` | [Abacus](https://abacus.ai) - Abacus AI models |
| `novita-ai` | [Novita AI](https://novita.ai) - Fast and affordable AI inference |
| `chutes` | [Chutes AI](https://chutes.ai) - AI model infrastructure |
| `cortecs` | [Cortecs AI](https://cortecs.ai) - AI inference platform |
| `moark` | [Moark](https://moark.ai) - AI model marketplace |
| `helicone` | [Helicone](https://helicone.ai) - AI observability and model gateway |
| `huggingface` | [Hugging Face](https://huggingface.co) - Open AI model hub |
| `fastrouter` | [FastRouter](https://fastrouter.ai) - Fast AI routing |
| `inception` | [Inception Labs](https://inceptionlabs.ai) - AI inference |
| `zenmux` | [Zenmux](https://zenmux.ai) - AI model multiplexing |
| `ovhcloud` | [OVH Cloud](https://ovhcloud.ai) - Cloud AI inference |
| `synthetic` | [Synthetic AI](https://synthetic.ai) - AI model services |
| `nano-gpt` | [NanoGPT](https://nano-gpt.com) - Lightweight GPT models |
| `requesty` | [Requesty](https://requesty.ai) - AI request routing |
| `friendli` | [Friendli](https://friendli.ai) - AI inference engine |
| `io-net` | [IO.NET](https://io.net) - Distributed GPU computing |
| `modelscope` | [ModelScope](https://modelscope.cn) - AI model hub (China) |
| `poe` | [Poe](https://poe.com) - AI chatbot platform |
| `opencode-zen` | [OpenCode Zen](https://opencode.ai/zen) - OpenCode Zen AI |
| `deep-infra` | [Deep Infra](https://deepinfra.com) - AI model hosting |

### Examples

Update configuration with all providers:

```bash
npx opencode-model-updater
```

Update only OpenRouter provider:

```bash
npx opencode-model-updater --provider openrouter
```

Update only AIHubMix provider:

```bash
npx opencode-model-updater --provider aihubmix
```

Update multiple specific providers:

```bash
npx opencode-model-updater --provider openrouter,aihubmix
```

List all available providers:

```bash
npx opencode-model-updater --list
```

Remove all auto-generated provider entries from config:

```bash
npx opencode-model-updater --remove
```

Remove specific auto-generated providers from config:

```bash
npx opencode-model-updater --remove openrouter,aihubmix
```

## Generated Config Example

The tool creates provider entries in your OpenCode configuration with all available models:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "your-existing-provider": { "..." : "preserved" },
    "openrouter-auto-generated": {
      "name": "OpenRouter Auto Generated",
      "options": {
        "baseURL": "https://openrouter.ai/api/v1",
        "apiKey": "your-api-key"
      },
      "models": {
        "openai/gpt-4o": { "name": "GPT-4o" },
        "anthropic/claude-sonnet-4": { "name": "Claude Sonnet 4" }
      }
    }
  }
}
```

## License

[MIT](LICENSE)
