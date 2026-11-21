# opencode-web-plugin

`opencode-web-plugin` is an OpenCode v2 plugin that exposes two directly callable tools:

- `web.search` searches the public web through the first configured search provider.
- `web.fetch` extracts readable content from an HTTP or HTTPS URL through the first configured fetch provider.

The plugin uses provider REST APIs directly, has no provider SDK dependencies, never performs a native webpage fetch, and does not include a browser, crawler, cache, or telemetry.

> OpenCode v2's Plugin API is currently beta. This package targets the current `@opencode-ai/plugin@next` API.

## Providers

| Provider | Search | Fetch | Environment |
|---|---:|---:|---|
| Tavily | ✓ | ✓ | `TAVILY_API_KEY` |
| Exa | ✓ | ✓ | `EXA_API_KEY` |
| Brave Search | ✓ | — | `BRAVE_SEARCH_API_KEY` |
| Serper | ✓ | — | `SERPER_API_KEY` |
| Jina | ✓ | ✓ | `JINA_API_KEY` |

Jina is considered configured only when `JINA_API_KEY` is present, including for Reader requests.

## Installation

Set at least one provider API key:

```bash
export TAVILY_API_KEY=tvly-xxx
```

Then add the package to `opencode.json` or `opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["opencode-web-plugin"]
}
```

OpenCode will register `web.search` and `web.fetch` as direct, non-CodeMode tools. API keys are resolved only when a tool executes, so the plugin still loads when no keys are present or when only one capability is configured.

For local development, build the package and reference its absolute directory or a relative path from the configuration file:

```jsonc
{
  "plugins": ["/absolute/path/to/opencode-web-plugin"]
}
```

## Provider selection

The default order is:

```text
search: tavily → exa → brave → serper → jina
fetch:  jina → tavily → exa
```

Selection skips providers that do not support the requested capability or whose configured environment variable is absent. Once a provider is selected, an authentication failure, rate limit, timeout, network failure, or upstream error is returned immediately. Runtime failures never trigger another provider, preventing unexpected requests and billing.

Examples:

- With only `EXA_API_KEY`, both tools use Exa.
- With only `BRAVE_SEARCH_API_KEY`, `web.search` works and `web.fetch` reports `CONFIG_ERROR` when called.
- With `TAVILY_API_KEY` but no `JINA_API_KEY`, `web.fetch` uses Tavily Extract.

## Configuration

All options are optional. These are the effective defaults:

```jsonc
{
  "plugins": [
    {
      "package": "opencode-web-plugin",
      "options": {
        "search": {
          "providerOrder": ["tavily", "exa", "brave", "serper", "jina"],
          "maxResults": 5,
          "timeoutMs": 15000
        },
        "fetch": {
          "providerOrder": ["jina", "tavily", "exa"],
          "maxChars": 50000,
          "timeoutMs": 30000
        },
        "providers": {
          "tavily": { "apiKeyEnv": "TAVILY_API_KEY" },
          "exa": { "apiKeyEnv": "EXA_API_KEY" },
          "brave": { "apiKeyEnv": "BRAVE_SEARCH_API_KEY" },
          "serper": { "apiKeyEnv": "SERPER_API_KEY" },
          "jina": { "apiKeyEnv": "JINA_API_KEY", "region": "global" }
        }
      }
    }
  ]
}
```

To change an environment variable name without putting the secret in OpenCode configuration:

```jsonc
{
  "plugins": [
    {
      "package": "opencode-web-plugin",
      "options": {
        "providers": {
          "exa": { "apiKeyEnv": "MY_EXA_API_KEY" }
        }
      }
    }
  ]
}
```

The plugin will read `process.env.MY_EXA_API_KEY` at tool execution time. Never place the actual key in `opencode.json`.

To use Jina's Reader and Search endpoints optimized for access from mainland China:

```jsonc
{
  "plugins": [
    {
      "package": "opencode-web-plugin",
      "options": {
        "providers": {
          "jina": { "region": "cn" }
        }
      }
    }
  ]
}
```

The default `"global"` region uses `r.jina.ai` and `s.jina.ai`. The `"cn"` region uses the API-compatible `r.jinaai.cn` and `s.jinaai.cn` endpoints. API keys and authentication are unchanged.

To restrict both capabilities to Exa:

```jsonc
{
  "plugins": [
    {
      "package": "opencode-web-plugin",
      "options": {
        "search": { "providerOrder": ["exa"] },
        "fetch": { "providerOrder": ["exa"] }
      }
    }
  ]
}
```

## Tool contracts

### `web.search`

Input:

```ts
interface WebSearchInput {
  query: string
  maxResults?: number // 1–20; defaults to configured search.maxResults
}
```

Structured output:

```ts
interface WebSearchOutput {
  provider: string
  results: Array<{
    rank: number
    title: string
    url: string
    snippet: string
    publishedAt?: string
  }>
}
```

Every snippet is capped at 1,500 characters. `maxResults` is an upper bound; Jina Search may return at most its fixed result count.

### `web.fetch`

Input:

```ts
interface WebFetchInput {
  url: string // http:// or https:// only
  maxChars?: number // 1,000–100,000; defaults to configured fetch.maxChars
}
```

Structured output:

```ts
interface WebFetchOutput {
  provider: string
  url: string
  title?: string
  author?: string
  publishedAt?: string
  content: string
  truncated: boolean
}
```

Content is always locally capped after provider normalization, even when the provider supports its own limit.

## Safety and errors

Model-visible output clearly labels search results and fetched pages as untrusted external content. Page text is data, never plugin configuration or instructions. The plugin does not follow links found in returned content.

Errors use one of these stable codes:

```text
CONFIG_ERROR
INVALID_INPUT
INVALID_URL
TIMEOUT
AUTH_ERROR
RATE_LIMITED
UPSTREAM_ERROR
PARSE_ERROR
```

Provider response bodies, request headers, and API keys are never embedded in normalized errors.

## Development

Requires Bun and Node.js 20 or newer:

```bash
bun install
bun run typecheck
bun test
bun run build
```

Tests mock `fetch`; they do not access the internet and do not require real provider keys.

## Releasing

Releases must be created from a clean, up-to-date `main` branch. Install and
authenticate the GitHub CLI before the first release:

```bash
gh auth login
```

Choose the appropriate semantic-version increment and run one command:

```bash
bun run release:patch # 0.1.0 -> 0.1.1
bun run release:minor # 0.1.0 -> 0.2.0
bun run release:major # 0.1.0 -> 1.0.0
```

The release command runs all checks, updates `package.json`, creates a version
commit and `vX.Y.Z` tag, atomically pushes both, and creates a GitHub Release.
GitHub generates the release title and notes from changes since the nearest
previous tag. Publishing the GitHub Release triggers the npm publish workflow.

If GitHub Release creation fails after the push succeeds, the script prints a
`gh release create` command that resumes the final step without bumping the
version again.

## Provider API mappings

- Tavily Search: `maxResults` → `max_results`; `content` → `snippet`.
- Tavily Extract: one URL in `urls`; `raw_content` → `content`.
- Exa Search: `maxResults` → `numResults`; `contents.highlights` → joined snippet.
- Exa Contents: URL in `ids`; `text.maxCharacters` receives the requested limit.
- Brave Search: `maxResults` → `count`; `description` → `snippet`.
- Serper: only `organic` results are normalized and locally sliced.
- Jina Search: JSON mode via `s.jina.ai`; full result content is reduced to a bounded snippet.
- Jina Reader: JSON mode via `r.jina.ai`; response timestamps are not assumed to be publication dates.

## Known limitations

- There is no native HTML fetch or parsing fallback.
- There is no runtime provider failover or retry.
- Jina anonymous Reader access is intentionally not used.
- Provider metadata absent from the upstream response remains absent; the plugin does not infer dates, authors, or titles.
- Provider APIs and the OpenCode v2 Plugin API can change; adapters may need updates as beta contracts evolve.
