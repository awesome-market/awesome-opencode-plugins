# auto-model-switcher

Automatic model failover for OpenCode — a local, OpenAI-compatible proxy that routes every request to the **best available model** and, when a provider trips a rate limit, runs out of quota, returns a 5xx, times out, or rejects the prompt for exceeding context length, **switches to the next model automatically** without you noticing or retrying manually.

```
┌──────────┐   /v1/chat/completions   ┌─────────────────────┐
│ opencode │ ───────────────────────> │  switcher (local)   │
│ (AI SDK) │                          │  :8790              │
└──────────┘                          │  model="auto"       │
                                      │                     │
                                      │  ┌─ google  ──────┐ │
                                      │  │ gemini-2.5-flash│ │
                                      │  └───────────────-─┘ │
                                      │  ┌─ openrouter ────┐ │
                                      │  │ nemotron...:free │ │
                                      │  └────────────────-┘ │
                                      │  ┌─ groq ─────────┐ │
                                      │  │ gpt-oss-120b   │ │
                                      │  └───────────────-─┘ │
                                      └─────────────────────┘
```

## Why

OpenCode needs a model with a **very large context window** and reliable availability. No single free provider reliably covers both. The switcher:

- **Bundles 15 free models** across Google, OpenRouter, NVIDIA, Groq and Cerebras, all with context windows ≥ 128K and most with **≥ 1M context**.
- Picks the **best model per request** using a weighted priority score (context window, capability quality, availability, rate limits, latency, free-tier generosity).
- **Fails over automatically** on `429/402`, quota exhaustion, `5xx`, timeouts and context-length errors.
- **Never retries in a tight loop** — skips options that are cooling down and returns a clear error when everything is exhausted.
- Reuses credentials you already have: environment variables **or** the OpenCode `auth.json`, so models you already `/connect`ed in OpenCode work with **zero extra setup**.

## Quick start

> Two ways to run it: the **`switchr` CLI** (interactive setup, run from any
> directory — recommended) or **direct `npm start`** (from the project folder).

### With the `switchr` CLI (recommended)

Install the CLI once, then `switchr` is available from any terminal. See
[Installation](#installation) for all the ways to install it.

#### 1. Configure providers and keys

```bash
switchr setup
```

No key prompts needed — the switcher **auto-detects** what OpenCode is already
signed in to and registers only those providers/models. It:

- scans your local OpenCode `auth.json` (what `/connect` writes) plus any
  `*_API_KEY` environment variables,
- lists every provider with its live credential status (`opencode-auth:...`,
  `env:...`, or `no credentials`),
- writes an OpenCode config that contains **only models you can actually call**.

If nothing is configured yet, log in to your providers in OpenCode first
(`/connect`) or set the relevant `*_API_KEY` env vars, then re-run.

#### 2. Start the proxy

```bash
switchr start
```

`switchr start` injects the keys you saved in `setup`, remembers your config
scope choice, writes the OpenCode config if needed, and runs the proxy on
`http://127.0.0.1:8790` (Ctrl+C to stop).

#### 3. Use it in OpenCode

Restart OpenCode, run `/models`, and pick **`modelswitcher/auto`**.

### Without the CLI

```bash
npm install
npm start
```

In a second terminal:

```bash
# check it's alive
curl http://127.0.0.1:8790/healthz

# list models
curl http://127.0.0.1:8790/v1/models

# generate the OpenCode config that registers this as a provider
npm run generate-opencode-config
```

Then in OpenCode: `/models` → pick **`modelswitcher/auto`**.

> The `auto` model ID invokes the automatic failover router. Individual models
> from the registry (e.g. `modelswitcher/gemini-2.5-flash`) are also selectable
> for when you want to force a specific model.

## Installation

The package is publish-ready for npm. Any of these installs the `switchr`
command globally:

| Method | Command |
| --- | --- |
| **npm registry** (after publish) | `npm install -g auto-model-switcher` |
| **GitHub** | `npm install -g github:PrateekDahiya/openCodeAutoModelSwtcher` |
| **Local folder** | `npm install -g D:\path\to\autoModelSwitcher` |
| **Local link** (dev, live-reloads edits) | `cd D:\path\to\autoModelSwitcher && npm link` |
| **Run without installing** | `npx auto-model-switcher` (or `npx --yes github:PrateekDahiya/openCodeAutoModelSwtcher`) |
| **Clone + run** | `npm install && npm start` |

Requirements: **Node.js ≥ 18**. No runtime dependencies.

After installing, verify:

```bash
switchr help
switchr models
```

> Publishing: `npm publish` deploys the CLI to the npm registry so
> `npm install -g auto-model-switcher` works for anyone. Until then, the
> GitHub / folder / `npx` methods above are equivalent.

## CLI reference

```
switchr help                     show usage
switchr setup                    auto-detect OpenCode logins, write config
switchr start                    ensure config, then run the proxy server
switchr config                   (re)generate the OpenCode config (choose scope)
switchr detect                   show which providers/models are usable on this machine
switchr models                   list models in the auto pool / all selectable
switchr file                     show where credentials & settings are stored
```

Global options:

| Option | Applies to | Meaning |
| --- | --- | --- |
| `--scope global\|package\|none` | `start`, `config` | Where to write the OpenCode config |
| `--port <n>` | `start`, `config` | Override port (default `8790`) |
| `--host <h>` | `start`, `config` | Override host (default `127.0.0.1`) |

Examples:

```bash
switchr setup                                  # auto-detect logins and configure
switchr start                                  # start proxy, ask scope on first run
switchr start --scope package --port 9000      # project-local config on :9000
switchr config --scope global                  # update config everywhere
switchr detect
switchr models
switchr file
```

### Auto-detection (`switchr detect` / `switchr setup`)

The generated config and the auto pool are **discovered from your machine**, not
a fixed catalog:

- Providers are considered usable when OpenCode's `auth.json` holds a credential
  for them (API key or unexpired OAuth) **or** a matching `*_API_KEY` env var is set.
- `auth.json` **wins** over env vars — the switcher uses exactly the credentials
  OpenCode itself is signed in with, so a stale env var can't shadow a live login.
- Only models from usable providers are written into the OpenCode config, so
  the picker lists models you can actually call.
- `switchr detect` prints the full inventory: every provider with its credential
  source, plus all usable models with their context windows.

### Where keys & settings live

| Item | Location |
| --- | --- |
| API keys | `~/.switchr/credentials.json` (defaults to `SWITCHR_HOME` if set) |
| Saved config scope etc. | `~/.switchr/settings.json` |
| OpenCode config (global) | `~/.config/opencode/opencode.json(c)` |
| OpenCode config (package) | `<current dir>/.opencode/opencode.json` |

Keys are stored in your user home only — never inside the project — and are
injected into the proxy as environment variables at launch.

### The `switchr config` scopes

- **package** — writes `.opencode/opencode.json` in the current directory;
  applies when you run OpenCode inside that project.
- **global** — writes `~/.config/opencode/opencode.json(c)`; applies to every
  project.
- **none** — skips writing the OpenCode config entirely (proxy-only usage).

The choice is remembered in `~/.switchr/settings.json`; re-run
`switchr config --scope <x>` anytime to change it.

## How the `auto` router works

For every request with `model: "auto"`:

1. **Estimate input tokens** from the request body (deliberately over-estimates for safety).
2. **Order candidates** by priority (configurable weights, preferred list first).
3. **Skip** models that are: cooling down from a recent failure, missing credentials, or excluded. Models **too small for the full conversation are not skipped outright** — the conversation is first **compacted** to fit that model (see below).
4. **Try the best candidate**; on success mark it healthy and stream the response straight through.
5. On a **transient** failure (`429/402/quota/5xx/timeout/context-length`) record the failure, put the model on an **escalating cooldown** (default 60s → 5m → 15m → 1h, honoring `Retry-After`), and try the next candidate.
6. **Non-transient** errors (bad request, auth failure, content filter) are returned to the user **unchanged** — the switcher does not silently re-route those. A `404` (model not on that provider) **is** routed to the next candidate instead of crashing.
7. When all candidates fail (or the failover cap is hit), return a clear error with the full failover trail (`x-failover-count`, error `details.failoverLog`). No infinite retry.

### Context compaction

When a conversation outgrows a candidate model's context window, the switcher
**compacts it instead of failing** (set `compactOnSmallContext: false` to keep the
old skip-if-too-small behavior):

- System messages (instructions) are always preserved.
- The **most recent** messages are kept; the oldest are dropped until the
  request fits the model's input budget.
- This happens automatically for **every** candidate: a request that fits the
  biggest model but not a smaller fallback gets compacted when the router fails
  over to that smaller model.
- Direct requests to a specific model whose context is exceeded are compacted
  too, instead of being sent oversized.
- Compaction is lossy (older turns are discarded) and logged; responses carry
  an `x-context-compacted: true` header when it happened.

Explicit, non-`auto` model requests never fail over — they return the provider's result (or a structured error) verbatim, but failures still feed the health store so future `auto` requests route around that model.

## Configuration

Copy `config.default.json` to `config.json` and edit, or override with `AUTO_*` env vars.

| Setting | Default | Env var |
| --- | --- | --- |
| `host` / `port` | `127.0.0.1:8790` | `AUTO_HOST` / `AUTO_PORT` |
| `apiKey` | (off) | `AUTO_API_KEY` (used when OpenCode can't be IP-trusted) |
| `logLevel` | `info` | `AUTO_LOG_LEVEL` (`debug|info|warn|error|silent`) |
| `modelRequestTimeoutMs` | `60000` | `AUTO_MODEL_REQUEST_TIMEOUT_MS` |
| `requestTimeoutMs` | `180000` | `AUTO_REQUEST_TIMEOUT_MS` |
| `connectTimeoutMs` | `15000` | `AUTO_CONNECT_TIMEOUT_MS` |
| `retryDelayMs` | `200` | `AUTO_RETRY_DELAY_MS` (backoff between retries of the same model) |
| `maxFailoverCandidates` | `12` | `AUTO_MAX_FAILOVER_CANDIDATES` |
| `maxRetriesPerModel` | `3` | `AUTO_MAX_RETRIES_PER_MODEL` (retries on same model before failing over; `0` = off) |
| `cooldownsSeconds` | `[60,300,900,3600]` | `AUTO_COOLDOWNS_SECONDS` (`"[10,60,300]"` or `"10,60,300"`) |
| `cooldownContextOverrideSeconds` | `900` | `AUTO_COOLDOWN_CONTEXT_OVERRIDE_SECONDS` |
| `stateFile` | `state.json` | `AUTO_STATE_FILE` |
| `contextSafetyMarginTokens` | `8000` | `AUTO_CONTEXT_SAFETY_MARGIN_TOKENS` |
| `minContextRatio` | `0.95` | `AUTO_MIN_CONTEXT_RATIO` |
| `allowPaidModelsInAuto` | `false` | `AUTO_ALLOW_PAID_MODELS_IN_AUTO` |
| `autoPool` | `free` | `AUTO_AUTO_POOL` (`free`|`paid`) |
| `excludedModels` / `preferredModels` | `[]` | `AUTO_EXCLUDED_MODELS` / `AUTO_PREFERRED_MODELS` (comma lists) |
| `compactOnSmallContext` | `true` | `AUTO_COMPACT_ON_SMALL_CONTEXT` (compact vs skip when a model's context is too small) |
| `streamIdleTimeoutMs` | `30000` | `AUTO_STREAM_IDLE_TIMEOUT_MS` (abort an upstream that stops producing tokens; `0` = off) |
| `maxRetriesPerModel` | `3` | `AUTO_MAX_RETRIES_PER_MODEL` (retry the same model N times on transient failure before failing over; `0` = off) |
| `priorityWeights` | see below | `AUTO_PRIORITY_WEIGHTS` (JSON) |

Default priority weights (`context:30, quality:25, availability:15, rateLimit:15, latency:5, freeTierGenerosity:10`). Every model also carries its own `quality`, `availability`, `rateLimit`, `latency` heuristics, editable in the registry.

## Credentials

Credentials are resolved per provider, in order:

1. **OpenCode's auth store** (`~/.local/share/opencode/auth.json`) — the same
   store `/connect` writes to. API keys and unexpired OAuth access tokens are
   reused automatically, so models you already authenticated in OpenCode work
   in the switcher with zero extra setup. This is checked **first** so the
   switcher uses exactly (and only) what OpenCode is signed in with.
2. **Environment variables** declared on the provider (e.g. `GEMINI_API_KEY`,
   `OPENROUTER_API_KEY`, `GROQ_API_KEY`, `CEREBRAS_API_KEY`, `NVIDIA_API_KEY`) —
   used when OpenCode has no stored credential for that provider.
3. **The `switchr` credential store** (`~/.switchr/credentials.json`, kept for
   legacy setups from earlier versions) — the CLI injects these as environment
   variables when it launches the proxy.

Secrets are never written to disk by the proxy itself and never printed (keys are masked in logs and `/healthz` reports only *sources*, not values). The `switchr` CLI stores keys only in your user home (`~/.switchr/`), never inside the project.

## Models

The bundled registry (`models.default.json`) is **data-driven** — add/remove models and providers without touching any code. Copy it to `models.json` to customize; the loader prefers `models.json` over the bundled default.

### Auto pool (free tier)

| Model | Name | Context | Max out | Tier | Provider |
| --- | --- | --- | --- | --- | --- |
| `gemini-2.5-flash` | Gemini 2.5 Flash | 1024K | 64K | free | Google AI Studio (Gemini) |
| `gemini-2.5-flash-lite` | Gemini 2.5 Flash-Lite | 1024K | 64K | free | Google AI Studio (Gemini) |
| `gemini-2.0-flash` | Gemini 2.0 Flash | 1024K | 8K | free | Google AI Studio (Gemini) |
| `gemini-3-flash-preview` | Gemini 3 Flash (Preview) | 1024K | 64K | free | Google AI Studio (Gemini) |
| `gemini-3.1-flash-lite-preview` | Gemini 3.1 Flash-Lite (Preview) | 1024K | 64K | free | Google AI Studio (Gemini) |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | Nemotron 3 Ultra 550B (free) | 977K | 125K | free | OpenRouter |
| `nvidia/nemotron-3.5-lightning:free` | Nemotron 3.5 Lightning (free) | 977K | 32K | free | OpenRouter |
| `dots-studio/dots-3-note-preview:free` | Dots3 Note Preview (free) | 500K | 16K | free | OpenRouter |
| `thinkingmachines/inkling` | Inkling (NVIDIA free catalog) | 1024K | 128K | free | NVIDIA NIM (build.nvidia.com) |
| `z-ai/glm-5.2` | GLM-5.2 (NVIDIA free catalog) | 977K | 128K | free | NVIDIA NIM (build.nvidia.com) |
| `minimaxai/minimax-m3` | MiniMax-M3 (NVIDIA free catalog) | 977K | 16K | free | NVIDIA NIM (build.nvidia.com) |
| `nvidia/nemotron-3-ultra-550b-a55b` | Nemotron 3 Ultra 550B (NVIDIA free catalog) | 977K | 64K | free | NVIDIA NIM (build.nvidia.com) |
| `nvidia/nemotron-3.5-lightning-30b-a3b` | Nemotron 3.5 Lightning 30B (NVIDIA free catalog) | 256K | 256K | free | NVIDIA NIM (build.nvidia.com) |
| `nvidia/nemotron-3-nano-30b-a3b` | Nemotron 3 Nano 30B (NVIDIA free catalog) | 128K | 128K | free | NVIDIA NIM (build.nvidia.com) |
| `minimaxai/minimax-m2.7` | MiniMax-M2.7 (NVIDIA free catalog) | 200K | 128K | free | NVIDIA NIM (build.nvidia.com) |
| `openai/gpt-oss-120b` | GPT-OSS 120B (Groq free tier) | 128K | 32K | free | Groq |
| `llama-3.3-70b-versatile` | Llama 3.3 70B Versatile (Groq free tier) | 128K | 32K | free | Groq |
| `gpt-oss-120b` | GPT-OSS 120B (Cerebras) | 128K | 32K | free | Cerebras |
| `meta-llama/llama-3.3-70b-instruct:free` | Llama 3.3 70B (free) | 128K | 32K | free | OpenRouter |
| `google/gemma-4-31b-it:free` | Gemma 4 31B (free) | 256K | 128K | free | OpenRouter |

### Paid pool (disabled in `auto` unless `allowPaidModelsInAuto: true`)

| Model | Name | Context | Max out | Tier | Provider |
| --- | --- | --- | --- | --- | --- |
| `gemini-2.5-pro` | Gemini 2.5 Pro (paid) | 1024K | 64K | paid | Google AI Studio (Gemini) |
| `openai/gpt-5.4` | GPT-5.4 (via OpenRouter) | 1025K | 125K | paid | OpenRouter |
| `zai-org/glm-5.2` | GLM-5.2 (via OpenRouter) | 1024K | 128K | paid | OpenRouter |
| `moonshotai/kimi-k3` | Kimi K3 (via OpenRouter) | 1024K | 128K | paid | OpenRouter |
| `meta-llama/llama-4-scout` | Llama 4 Scout (via OpenRouter) | 1280K | 16K | paid | OpenRouter |
| `deepseek/deepseek-v4-pro` | DeepSeek V4 Pro (via OpenRouter) | 1024K | 32K | paid | OpenRouter |
| `kimi-k2-turbo` | Kimi K2 Turbo (Moonshot) | 250K | 8K | paid | Moonshot AI (Kimi) |

Context windows, prices and rate limits were verified against [models.dev](https://models.dev) (the registry OpenCode uses for its own limits) and provider docs in August 2026. Note that rate limits genuinely vary by account and change often; the cooldown + failover machinery is designed to absorb that uncertainty.

## API

- `POST /v1/chat/completions` — OpenAI-compatible; `model: "auto"` routes automatically. Supports both `stream: true` (SSE passthrough) and non-streaming.
- `GET /v1/models` — registry models plus the virtual `auto` entry, with context/output limits.
- `GET /healthz` — providers, credential status (no secrets), cooldowns, candidate counts.
- `OPTIONS` — CORS preflight (`Access-Control-Allow-Origin: *`).

Response headers: `x-model-used`, `x-failover-count`, `x-context-compacted` (when the conversation was trimmed to fit), `x-request-id`.

## Operational notes

- **Cooldown state** is persisted (`state.json`) so a restart doesn't immediately re-try a repeatedly failing model. Clear it by deleting the file.
- **Streaming**: once a model starts streaming it is committed — failover decisions happen before the first upstream byte goes to the client. If a provider fails mid-stream, the client sees a truncated stream; the error is logged and the model is cooled down for the *next* request.
- **Timeout**: an upstream that hangs is aborted after `modelRequestTimeoutMs`; the router treats it as a retryable failure and moves on.
- Shuts down cleanly on `SIGINT`/`SIGTERM` (flushes state).

## Project layout

```
bin/
  switchr.js    CLI entry point (setup / start / config / models / file)
src/
  auth.js       credential resolution (opencode auth.json -> env -> switchr store)
  classifier.js classify failures (rate limit / quota / context / 5xx / auth)
  config.js     config load + env overrides
  discover.js   provider credential status, usable-model discovery for config/CLI
  health.js     per-model cooldown state, escalating, persisted
  logger.js     leveled logger (console + file), key masking
  registry.js   model/provider data, validation, priority scoring
  router.js     the failover engine
  server.js     HTTP server (OpenAI-compatible endpoints)
  tokens.js     conservative token estimation
  upstream.js   OpenAI-compatible client (streaming + non-streaming)
  opencode-config.js  shared OpenCode provider-config builder (CLI + script)
  cli/          switchr CLI internals (prompts, credentials store, injection)
scripts/
  generate-opencode-config.js  thin wrapper around opencode-config.js
test/          node:test suite
```

## Development

```bash
npm test                  # node --test test/*.test.js
npm run dev               # restart on file changes
node bin/switchr.js help  # run the CLI without installing
```

## License

MIT