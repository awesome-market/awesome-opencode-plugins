# @joaogsbarbosa/opencode-9router

OpenCode plugin provider for [9Router](https://github.com/decolua/9router) — FREE AI Router & Token Saver. 40+ providers, 100+ models.

Registers 9Router as a custom provider in OpenCode with auto-discovery of models.

> **Dual V1 + V2 support.** This package ships a single entrypoint that works on both **OpenCode V1** (via the V1 `server` hook, OpenCode `1.18.29`+) and **OpenCode V2** (via the V2 `Plugin.define({ id, setup })` API). The discovery core is shared; only the plugin entrypoint differs. No separate package is needed.

## Quick Start

> **Automated:** run `npx @joaogsbarbosa/opencode-9router-installer` for the
> interactive installer, or add the plugin manually below.

### OpenCode V1

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["@joaogsbarbosa/opencode-9router@latest"]
}
```

1. Add the plugin to `opencode.json`
2. Restart OpenCode
3. `/models` → select a 9Router model

### OpenCode V2

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["@joaogsbarbosa/opencode-9router@latest"]
}
```

Or with plugin options (object form):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "@joaogsbarbosa/opencode-9router@latest",
      "options": {
        "baseURL": "http://localhost:20128",
        "apiKey": "{env:ROUTER_API_KEY}",
        "cache": true,
        "cacheTTL": 10800000,
        "discoveryTimeout": 30000
      }
    }
  ]
}
```

The plugin will auto-discover models from `http://localhost:20128` (default).

## Features

- **Auto-discover models** — Models from 9Router are automatically detected on startup
- **Smart caching** — Discovery results cached for 3 hours (configurable) for instant subsequent loads
- **Stale fallback** — If the backend is unreachable, returns cached models instead of failing
- **Configurable timeout** — Adjustable discovery timeout (default 30s) for slow backends
- **Dynamic model list** — All models from 9Router are available, including custom combos
- **Combo multimodal defaults** — Combo models (`owned_by: "combo"`) that expose no capability info are forced to accept text/image/audio input with tool calling, reasoning, 256K context, 128K output, and `low`/`medium`/`high`/`xhigh`/`max`/`minimal`/`thinking` variants
- **Catalog thinking modes (V2)** — Reasoning variants from exact provider/model matches in models.dev, preserving configured overrides and combo variants
- **OpenAI-compatible** — Uses `@ai-sdk/openai-compatible` (V1) / `@opencode/ai/providers/openai-compatible` (V2)
- **Type-safe** — Uses the `config` hook (V1) / provider transforms (V2) for provider registration that conforms to the OpenCode config schema

### Catalog thinking modes (V2)

Raw models expose effort and toggle variants from models.dev `reasoning_options`. Efforts use `reasoningEffort`; toggles use 9Router's `enable_thinking` body field and clear inherited effort with `reasoningEffort: null` in variant settings so it cannot override the toggle. The adapter omits the cleared effort from the request. Native OpenCode configuration merges variants by ID: settings/body fields you supply win, while unspecified catalog fields remain; an empty configured variants array does not remove catalog variants. Unknown controls and numeric budgets are omitted. Leaving the variant unselected preserves upstream defaults. These controls remain subject to 9Router's downstream effort rewriting and toggle handling.

`src/reasoning.ts` translates provider IDs using a subset of 9Router's [`PROVIDER_ALIASES`](https://github.com/decolua/9router/blob/89ffac5a2c8108449c432afd1ad6531578fa81cd/src/lib/modelCatalog/sync.js#L22-L40) at commit `89ffac5a2c8108449c432afd1ad6531578fa81cd` (`hunyuan` is omitted). The additional `gh` prefix comes from that revision's [GitHub provider registry](https://github.com/decolua/9router/blob/89ffac5a2c8108449c432afd1ad6531578fa81cd/open-sse/providers/registry/github.js#L1-L5). These aliases translate identities, not reasoning levels; controls still require an exact full model ID within the matched provider. Alias identity does not guarantee capability parity across authentication modes, notably Kimi's OAuth and API-key routes.

## OpenCode V2

OpenCode V2 replaces the V1 `plugin` config key with `plugins` and the single-function plugin shape with `Plugin.define({ id, setup })`. This package handles both — the same published entrypoint is loaded by V1 and V2.

### Configure (V2)

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["@joaogsbarbosa/opencode-9router@latest"]
}
```

For a local checkout, keep the directory path in the V2 `plugins` list:

```jsonc
{
  "plugins": ["/absolute/path/to/opencode-9router"]
}
```

The local directory must expose a root `server` entrypoint; this repository provides `server.js` for that purpose. The V1 configuration key remains `plugin` and can continue to use the published package name as shown above.

Plugin options use the object form (`{ "package": ..., "options": { ... } }`) and are read from `ctx.options`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "@joaogsbarbosa/opencode-9router@latest",
      "options": {
        "baseURL": "http://localhost:20128",
        "apiKey": "{env:ROUTER_API_KEY}",
        "cache": true,
        "cacheTTL": 10800000,
        "discoveryTimeout": 30000
      }
    }
  ]
}
```

### Providers (V2)

In V2, providers are declared under the `providers` key. Each 9router-family provider uses the OpenAI-compatible runtime package and carries the endpoint in `settings.baseURL`. The plugin discovers models for every provider whose ID starts with `9router` and fills in the model list.

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["@joaogsbarbosa/opencode-9router@latest"],
  "providers": {
    "9router": {
      "name": "9Router",
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": {
        "baseURL": "http://localhost:20128/v1",
        "apiKey": "{env:ROUTER_API_KEY}"
      }
    },
    "9router-remote": {
      "name": "Remote 9Router",
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": {
        "baseURL": "https://your-9router-endpoint.example.com/v1"
      }
    }
  }
}
```

If no 9router-family provider exists, the plugin registers a default `9router` provider pointing at `http://localhost:20128`. A background refresh re-discovers models and calls `ctx.provider.reload()` every 5 minutes; the discovery interval is cleaned up when the plugin unloads.

### Dual V1 + V2 entrypoint

The default export exposes both implementations:

```ts
import { Plugin } from "@opencode/plugin"
import { NineRouterPlugin } from "./plugin.js"   // V1
import { nineRouterV2 } from "./v2.js"           // V2

const v2 = Plugin.define(nineRouterV2)
export default { id: v2.id, setup: v2.setup, server: NineRouterPlugin }
export { NineRouterPlugin }
```

V2 reads `id`/`setup`; V1 (1.18.29+) reads `server`. The named `NineRouterPlugin` export is kept for older V1 consumers. For local development, the repository also includes a root `server.js` bridge because OpenCode resolves an absolute plugin directory through its `server` entrypoint. The published package exposes the same entry through the `./server` export.

## Installation

### From npm (recommended)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["@joaogsbarbosa/opencode-9router@latest"]
}
```

No need to define a provider manually — the plugin registers it automatically. On
OpenCode V1, use the legacy `plugin` key as shown in the Quick Start above.

### Automated install (npx)

A separate installer package ships the interactive setup. It uses
`jsonc-parser` to edit the `plugins` array and the matching `providers` entry,
preserving comments and formatting elsewhere in the file. It targets the V2
`plugins` key; on OpenCode V1, add the package to the legacy `plugin` key
manually (see Quick Start).

**Run with npx:**

```bash
npx @joaogsbarbosa/opencode-9router-installer
```

The interactive menu shows the current installation status (including the
effective base URL, API key, cache and timeouts) before asking what to do.

**Flags:** `--project` edits the project config instead of the global config. It
uses `./opencode.jsonc` by default, or an existing `./opencode.json` or
`.opencode/opencode.json(c)`.

**Prompts:** base URL (default `http://localhost:20128`), API key (optional),
cache (default `Y`), cache TTL in ms (default `10800000`, 3 h), discovery
timeout in ms (default `30000`). The install/configure option reads the current
values from the plugin options, or from a `providers` entry whose ID starts with
`9router` (its `settings.baseURL`/`settings.apiKey`) when one exists. The values
are pre-filled at the cursor, so pressing Enter keeps them. The connection
(`{baseURL}/v1/models`) is verified before saving.

**Menu:**

- Option 1 — `install` when not installed, `configure` when already installed.
  Installs the plugin or changes the current configuration.
- Option 2 — `uninstall` removes the plugin entry and cache.
- Option 0 — `quit` exits.

**What it writes:**

```json
{
  "package": "@joaogsbarbosa/opencode-9router@latest",
  "options": {
    "baseURL": "...",
    "apiKey": "...",
    "cache": true,
    "cacheTTL": 10800000,
    "discoveryTimeout": 30000
  }
}
```

`apiKey` is omitted when left empty. If the plugin options contain a
`providers` array, the matching entry is updated in place. If the config already
has a `providers` entry for `9router` (or another ID starting with `9router`), the
installer also updates that entry's `settings.baseURL` and `settings.apiKey`,
since V2 prefers the provider settings over the plugin options. OpenCode installs
the package and its dependencies automatically. The uninstall option removes the
config entry and the plugin cache (`~/.cache/opencode-9router`, or
`$XDG_CACHE_HOME/opencode-9router`); a `providers` entry for `9router` is left
untouched. Requires Node 18+.

### Multiple Providers

Add one or more 9Router-family providers with custom options:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["@joaogsbarbosa/opencode-9router@latest"],
  "provider": {
    "9router": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Your Provider",
      "options": {
        "baseURL": "https://your-9router-endpoint.example.com/v1",
        "apiKey": "{env:ROUTER_API_KEY}",
        "cache": true,
        "cacheTTL": 10800000,
        "discoveryTimeout": 60000
      }
    },
    "9router-local": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Local Router",
      "options": {
        "baseURL": "http://127.0.0.1:20128/v1",
        "apiKey": "sk-...",
        "cache": true,
        "discoveryTimeout": 60000
      }
    }
  }
}
```

Each provider key must start with `9router`. The `npm` must be `@ai-sdk/openai-compatible`. The `name` is a display label shown in OpenCode.

> **Never commit real API keys.** Replace the `baseURL`/`apiKey` above with your own endpoint and a placeholder such as `{env:ROUTER_API_KEY}` (or a dummy value like `sk-...`). Real keys belong in environment variables, not in `opencode.json` or this README.

### With Environment Variable

```json
{
  "provider": {
    "9router": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Remote 9Router",
      "options": {
        "baseURL": "https://example.com/v1",
        "apiKey": "{env:ROUTER_API_KEY}",
        "cache": true,
        "discoveryTimeout": 30000
      }
    }
  }
}
```

```bash
export ROUTER_API_KEY=your-api-key-here
opencode
```

## Provider Options

| Option                | Type      | Default     | Description                                            |
| --------------------- | --------- | ----------- | ------------------------------------------------------ |
| `baseURL`               | `string`    | `http://localhost:20128` | 9Router API endpoint                                   |
| `apiKey`                | `string`    | —           | API key (if required by backend)                       |
| `cache`                 | `boolean`   | `true`      | Cache discovery results to `~/.cache/opencode-9router/` |
| `cacheTTL`              | `number`    | `10800000` (3h) | Cache TTL in milliseconds                           |
| `discoveryTimeout`      | `number`    | `30000` (30s)  | Timeout for `/v1/models` request in milliseconds     |

### Example with cache and timeout tuning

```json
{
  "provider": {
    "9router": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Local Router",
      "options": {
        "baseURL": "http://localhost:20128",
        "cache": true,
        "discoveryTimeout": 60000
      }
    },
    "9router-remote": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Remote API",
      "options": {
        "baseURL": "https://your-9router-endpoint.example.com/v1",
        "apiKey": "{env:ROUTER_API_KEY}",
        "cacheTTL": 3600000
      }
    }
  }
}
```

### Disable cache

```json
{
  "provider": {
    "9router": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Local Router",
      "options": {
        "baseURL": "http://localhost:20128",
        "apiKey": "sk-...",
        "cache": false,
        "discoveryTimeout": 30000
      }
    }
  }
}
```

## Usage

### Select a model

```
/models
  → Find the 9Router provider
  → Pick any model (e.g., kr/claude-sonnet-4.5, cc/claude-opus-4-7)
```

## Model Prefixes

| Prefix | Provider | Tier |
|--------|----------|------|
| `cc/` | Claude Code | Subscription |
| `cx/` | Codex | Subscription |
| `gh/` | GitHub Copilot | Subscription |
| `cu/` | Cursor IDE | Subscription |
| `kr/` | Kiro AI | **FREE** |
| `oc/` | OpenCode Free | **FREE** |
| `vertex/` | Vertex AI | $300 credits |
| `glm/` | GLM | $0.6/1M |
| `minimax/` | MiniMax | $0.2/1M |
| `kimi/` | Kimi | $9/mo flat |
| `openrouter/` | OpenRouter | API key |
| `deepseek/` | DeepSeek | API key |
| `groq/` | Groq | API key |

## How It Works

```
opencode.json "plugin": ["@joaogsbarbosa/opencode-9router@latest"]
  ↓
Plugin loads at startup detects 9Router-family providers in config
  ↓
For each provider:
  1. Check local cache (~/.cache/opencode-9router/discovery-*.json)
     └─ Fresh cache (≤3h) → return cached models instantly
  2. If cache miss/stale:
     └─ GET {baseURL}/v1/models with 30s timeout (configurable)
     └─ If OK → register live models + save to cache
     └─ If fail → fallback to stale cache (if exists), else skip
  ↓
config hook creates/updates provider with discovered models
  ↓
Provider appears in /models
```

### Cache storage

Cache files are stored at `~/.cache/opencode-9router/discovery-{base64url}.json`, one per unique `baseURL`. The cache directory also stores the models.dev capability catalog (`models-dev.json`).

## Development

```bash
git clone https://github.com/joaogsbarbosa/opencode-9router
cd opencode-9router
npm install
npm install --prefix installer
npm run build
node installer/install.mjs   # run the installer locally
```

### Test

```bash
node test-minimal.mjs
opencode models 9router --print-logs
```

### Validate after publish

After publishing to npm, verify the plugin works end-to-end:

```bash
opencode models 9router-local --print-logs --log-level DEBUG
```

This runs model discovery against the published package with full debug logging to confirm caching, timeout, and capability resolution are working correctly.

### Publish

Plugin:

```bash
npm login
npm version patch  # or minor, major
npm publish --access public
git push --follow-tags
```

Installer (separate package):

```bash
cd installer
npm version patch  # or minor, major
npm publish --access public
```

## Files

```
opencode-9router/
  src/
    index.ts          # Dual V1 + V2 package entry
    plugin.ts         # V1 plugin entry (provider registration + config hook)
    v2.ts             # V2 plugin entry (Plugin.define + provider transform)
    v2-map.ts         # V1 ModelConfig → V2 Model.Info mapping
    discovery.ts      # Model discovery pipeline
    capabilities.ts   # Capability resolution (catalog + per-model API)
    cache.ts          # Discovery + models.dev cache
    reasoning.ts      # Catalog reasoning options (effort + toggle) from models.dev
    types.ts          # Shared types
    utils.ts          # Shared helpers
    constants.ts      # Models, defaults, prefixes
  dist/               # Compiled output (generated)
  installer/
    install.mjs       # Interactive installer (separate npx package)
    package.json      # Installer package config
    README.md         # Installer usage
  package.json        # npm package config
  tsconfig.json       # TypeScript config
  README.md           # This file
  LICENSE             # MIT
```

## Links

- [npm package](https://www.npmjs.com/package/@joaogsbarbosa/opencode-9router)
- [OpenCode Plugin Docs](https://opencode.ai/docs/plugins/)
- [OpenCode Custom Provider](https://opencode.ai/docs/providers/#custom-provider)
- [9Router GitHub](https://github.com/decolua/9router)
- [9Router Website](https://9router.com)
