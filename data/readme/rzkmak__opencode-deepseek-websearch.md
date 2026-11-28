# opencode-deepseek-websearch

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A DeepSeek search provider for **OpenCode v2**'s built-in `websearch` tool. Search requests go to DeepSeek's search API at `POST https://api.deepseek.com/v1/tools/search` and reuse the DeepSeek key already connected in OpenCode.

Built against the **2.0.32** plugin API. OpenCode v1 is not supported.

## Features

- Automatic retries with exponential backoff + jitter on transient failures (HTTP 408/425/429, 5xx, network errors, timeouts), configurable 0–5 attempts
- TTL cache for identical queries (5 minutes by default) so repeats don't hit the API again
- Optional full page content via `need_content`, with per-result truncation
- Result enrichment: site name, publish date, and authority tier folded into `content`
- Quality filters: `minScore` (rerank score) and `minAuthority` (0–4 authority tier)
- Configurable result count (1–50), timeout, endpoint (proxy support), and explicit API key
- Query whitespace normalization, URL deduplication, and tolerant response decoding
- Structured logging per search
- Zero runtime dependencies — OpenCode supplies `effect` and the plugin API at runtime

## Installation

**Option 1 — install from GitHub** (recommended):

```
opencode plugin add github:rzkmak/opencode-deepseek-websearch#v0.1.0
```

The command appends the spec to `plugins` in your global `opencode.json`. Adding it by hand works the same way:

```jsonc
{
  "plugins": ["github:rzkmak/opencode-deepseek-websearch#v0.1.0"]
}
```

**Option 2 — local copy**: clone or copy this folder into your project's `.opencode/plugins/` (or `~/.config/opencode/plugins/` for all projects) and OpenCode loads it automatically:

```
git clone https://github.com/rzkmak/opencode-deepseek-websearch ~/.config/opencode/plugins/opencode-deepseek-websearch
```

After either option, **restart OpenCode**. To upgrade a GitHub install, change the tag. Pick one option only — installing both registers duplicate plugins.

## API key

The plugin reads the key from OpenCode's `deepseek` integration, which the DeepSeek model provider also uses. If you already run DeepSeek models in OpenCode, search uses that key with no extra setup. Otherwise connect one:

- `/connect` in the TUI → pick DeepSeek, or
- `opencode auth login deepseek`, or
- set `DEEPSEEK_API_KEY` in your environment, or
- set the plugin's `apiKey` option (see below).

Without any of these, every search fails with a clear error explaining the options above.

## Configuration

Options go in the object form of the plugin entry. All options are optional:

```jsonc
{
  "websearch": { "provider": "deepseek" },
  "plugins": [
    {
      "package": "github:rzkmak/opencode-deepseek-websearch#v0.1.0",
      "options": {
        "count": 10,
        "needContent": false,
        "contentMaxLength": 8000,
        "timeoutSeconds": 25,
        "retries": 2,
        "enrichContent": true,
        "minScore": 0,
        "minAuthority": -1,
        "localization": "",
        "apiKey": "",
        "baseUrl": "https://api.deepseek.com/v1/tools/search",
        "cacheTtlSeconds": 300,
        "cacheMaxEntries": 256
      }
    }
  ]
}
```

| Option | Default | Description |
| --- | --- | --- |
| `count` | `8` | Results per search, 1–50 (DeepSeek's limit). |
| `needContent` | `false` | Ask DeepSeek for full page content. Result `content` then prefers the page text, falling back to the summary/snippet. Costs more. |
| `contentMaxLength` | `8000` | Truncate each result's `content` to this many characters, with an explicit `…[truncated]` marker. `0` disables truncation. |
| `timeoutSeconds` | `25` | Per-request timeout, 5–120. |
| `retries` | `2` | Automatic retries (0–5) for transient failures: transport errors, HTTP 408/425/429, 5xx, and timeouts. Backoff is exponential with jitter, capped at 8 s. Auth and bad-request errors fail immediately. |
| `enrichContent` | `true` | Prepend a short source line to `content`, e.g. `[Example • 2026-01-15 • authoritative source]`, built from DeepSeek's `site_name`, `date`, and `authority` fields. |
| `minScore` | `0` | Drop results whose DeepSeek `rerank_score` (0–3, ≥1.5 is high quality) is below this. |
| `minAuthority` | `-1` | Drop results whose `authority` tier (0–4, `-1` unknown) is below this. Results without an authority tier always pass. |
| `localization` | `""` | IP address passed to DeepSeek to localize results. |
| `apiKey` | — | Explicit API key. When unset, falls back to OpenCode's `deepseek` integration / `DEEPSEEK_API_KEY`. |
| `baseUrl` | DeepSeek endpoint | Override to route through a compatible proxy. |
| `cacheTtlSeconds` | `300` | How long identical queries (same query/count/needContent/localization) are served from an in-memory cache. `0` disables. |
| `cacheMaxEntries` | `256` | LRU cap on cached queries. |

### Choosing the provider

Set DeepSeek in `opencode.json`:

```jsonc
{ "websearch": { "provider": "deepseek" } }
```

Without this setting, OpenCode asks which provider to use the first time the `websearch` tool runs; pick DeepSeek under "Choose another provider". With `"provider": "random"`, DeepSeek joins the pool OpenCode picks from.

## What a search sends and returns

Each call sends the whitespace-normalized query with your configured `count`, `need_content`, and `localization`. DeepSeek accepts 1–128 Unicode characters; a longer query fails locally with a clear error and no request goes out.

Response mapping:

| DeepSeek field | OpenCode result field |
| --- | --- |
| `url` | `url` |
| `title` | `title`, left out when empty |
| `content` (when `needContent`), else `summary`, else `snippet` | `content`, after enrichment and truncation |
| `date` | `time.published` in epoch milliseconds, left out when missing or unparseable |

Results are deduplicated by URL and filtered by `minScore`/`minAuthority` before returning.

Retries preserve native HTTP error values, so in `random` mode a final 429 still puts DeepSeek on cooldown through OpenCode's built-in handling.

## Development

```
npm install
npm run typecheck   # strict type check
npm test            # smoke test: mock server, retry/backoff, mapping, cache
```

`effect` and `@opencode/plugin` are dev/peer dependencies for type checking. At runtime OpenCode supplies its own copies of both and never loads them from a plugin's `node_modules`.

The request and response shapes follow DeepSeek's [search API reference](https://api-docs.deepseek.com/api/search/). OpenCode documents the plugin API in [OpenCode v2 plugins](https://dev.opencode.ai/v2/docs/build/plugins/).

## License

[MIT](LICENSE)
