<div align="center">

# opencode-router

**Per-turn model routing for OpenCode V2 and Kilo.**

A small model running on your machine picks the right model for every turn — so a
one-line question doesn't cost frontier tokens, and a hard refactor doesn't run on
a model that will fail it.

[![npm](https://img.shields.io/npm/v/@231self/opencode-router?color=3b82f6&label=npm)](https://www.npmjs.com/package/@231self/opencode-router)
[![ci](https://github.com/231self/opencode-router/actions/workflows/ci.yml/badge.svg)](https://github.com/231self/opencode-router/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-Apache--2.0-22c55e)](LICENSE)
[![node](https://img.shields.io/badge/node-%E2%89%A522-111827)](https://nodejs.org)

</div>

> **Status: v0.2.3.** Routing, the context optimiser, subagent policy, the TUI
> `/router` surface, per-turn timing, the CLI, and the Kilo shim are implemented
> and tested. Design of record:
> [`docs/specs/2026-11-15-opencode-omlx-router-design.md`](docs/specs/2026-11-15-opencode-omlx-router-design.md).

## Why

A coding agent makes you pick one model for a whole session. A one-line question
then costs frontier-model tokens, while a hard refactor on a small model burns
retries. This plugin routes **each turn** to the model that fits it, from a pool
you control.

It ports the transferable ideas from
[`pi-smart-router`](https://github.com/beettlle/pi-smart-router) — turn envelope,
deterministic triage, context-fit gate, cache-aware pinning, loop escalation,
decision logging — and drops the heavy machinery (HyDRA/ONNX embeddings,
benchmark calibration, virtual cost, planning delegate).

The pool can mix cloud models with local oMLX or llama.cpp models. Loopback
providers are priced at zero, so a capable local model can take routine turns
while cloud models handle the hard ones.

## Quick start

```sh
# 1. install
opencode plugin add @231self/opencode-router

# 2. choose the models the router may pick from
opencode-model-router config set pool.source list
opencode-model-router config set pool.models '["deepseek/deepseek-flash","deepseek/deepseek-v4-pro"]'

# 3. make sure a small judge model is served locally
opencode-model-router judge probe

# 4. talk normally; inspect the first decisions
opencode-model-router status
opencode-model-router history 5
```

In the TUI, `/router` opens the full menu, `/router explain` shows why the last
turn picked its model, and `/router debug` prints the diagnostic bundle.

## Documentation

- [Architecture](docs/architecture.md) — adapter, WASM core, turn flow, subagents, pinning, optimiser.
- [WASM protocol](docs/protocol.md) — ABI, request/response JSON, need-judge flow, optimiser plans.
- [Configuration reference](docs/configuration.md) — every key, defaults, examples.
- [Troubleshooting](docs/troubleshooting.md) — symptoms, evidence, reset.
- [Building and releasing](docs/releasing.md) — build, pack, publish, tag, consumer install.
- [Benchmarks](docs/benchmarks/) — routing/cost suites and the live quality eval.
- [Design spec](docs/specs/2026-11-15-opencode-omlx-router-design.md) and
  [implementation plan](docs/plans/2026-11-15-implementation.md).
- [Development notes](docs/development.md) — probe results, verification, limits.

## Requirements

| Requirement | Notes |
|---|---|
| [OpenCode](https://opencode.ai) ≥ 2.3 | First-class; V2 plugin API |
| [Kilo CLI](https://kilo.ai) ≥ 7.6.2 | Best-effort mode; see [Kilo limitations](#kilo-limitations) |
| [oMLX](https://github.com/jundot/omlx) or [llama.cpp](https://github.com/ggml-org/llama.cpp) | Local OpenAI-compatible server; oMLX defaults to `http://127.0.0.1:1234/v1`, `llama-server` to `:8080` |
| A small judge model | e.g. a ~4B instruct model; oMLX, llama.cpp, or any OpenAI-compatible server; see [Choose a judge](#choose-a-judge) |
| Node/Bun | Provided by OpenCode and Kilo; nothing extra to install |

No Rust toolchain is needed to install a released package. Building from source
requires Rust with the `wasm32-unknown-unknown` target.

## Install

Release/build details: [docs/releasing.md](docs/releasing.md).

### OpenCode V2

```sh
opencode plugin add @231self/opencode-router
```

```jsonc
// ~/.config/opencode/opencode.jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["@231self/opencode-router"]
}
```

### Kilo

```sh
kilo plugin @231self/opencode-router
```

```jsonc
// ~/.config/kilo/kilo.jsonc or project kilo.jsonc
{
  "$schema": "https://app.kilo.ai/config.json",
  "plugin": ["@231self/opencode-router"]
}
```

### From a checkout (development)

```sh
git clone https://github.com/231self/opencode-router
cd opencode-router
bun install
bun run build:wasm       # needs Rust with wasm32-unknown-unknown
```

Then point the host at the checkout:

```jsonc
// OpenCode
{ "plugins": ["/absolute/path/to/opencode-router"] }
```

```jsonc
// Kilo
{ "plugin": ["/absolute/path/to/opencode-router/src/index.js"] }
```

Kilo applies a decision at the next request boundary; see
[Kilo limitations](#kilo-limitations).

The CLI installs as `opencode-model-router`. `omlx-router` remains an alias.
Config, state, plugin IDs, and `OMLX_ROUTER_*` env vars keep their historical
names, so existing setups keep working.

## How it works

Three layers: a plain-JS adapter for the host, a Rust decision engine compiled to
WebAssembly, and a short JSON-verdict call to a small local model.

```text
prompt hook
  ├─ envelope: cheap Rust heuristics → signals + complexity hint
  ├─ short-circuit? (trivial · forced pin · escalation · empty pool)
  ├─ judge: 4B local model → JSON verdict        [5 s budget]
  ├─ reconcile: judge + deterministic floor (judge can raise, never lower)
  ├─ gates → score → pin → chosen model
  └─ session.switchModel(...) + write pin + decision record
context hook (same turn)
  ├─ optimiser: token estimate → prune plan → afterTokens
  └─ afterTokens feeds the next routing decision
telemetry (after the turn)
  └─ turns.jsonl: routing/judge/core/switch time, tokens, cost
```

The routing brain is deterministic, has no I/O, and is unit-tested on its own.
The only model call the plugin makes for a decision is the short verdict prompt
to the judge endpoint you configure (localhost by default). If it is slow or
down, deterministic heuristics take over and routing continues.

### The judge

A classifier, not a chat model. It is asked one question per turn, and sees only:

- the turn truncated to 1,200 characters,
- token counts, image count, and tool-failure count,
- the deterministic signals (code, error, planning, review),
- the candidate table — context, tools, vision, price, local flag.

It never sees the transcript, file contents, or tool output.

| Input | Value |
|---|---|
| Temperature | `0` |
| Max tokens | `220` |
| Format | `response_format: json_object`, one repair retry |
| Timeout | `judge.timeoutMs` (default 5 s) |

It returns:

```json
{"task":"edit","complexity":2,"needsTools":true,"needsVision":false,
 "contextNeed":"small","reasoningNeed":"medium","confidence":0.8}
```

**The judge is a floor-adder.** `reconcile` lets it raise complexity, reasoning,
or context need, but never lower what the deterministic signals already proved.
That is why a 4B that under-classifies a multi-file refactor cannot cause an
under-route. `confidence` is recorded but does not steer selection. On timeout,
HTTP, or parse failure the heuristic verdict is used, the decision log records
`used: false`, and the turn continues.

### Signals and complexity

Before any judge call, the envelope computes word-boundary-aware markers:

| Signal | Trigger |
|---|---|
| `code` | code fences, source extensions, `cargo`/`bun`/`npm`/`git` |
| `agentic` | implement, fix, refactor, migrate, debug, add, run, test, … |
| `error_trace` | panic, traceback, exception, `error:`, exit code, … |
| `planning` | plan, design, architect, approach, trade-off, spec |
| `review` | review, audit, critique, security, look for bugs |
| `trivial` | short, no signals, small prompt and context |
| `multi_file` | ≥ 3 code files, or 2 across files |
| `large_context` | estimated input over 60k tokens |
| `repeated_failures` | 3+ consecutive identical tool failures |

Complexity starts at 1 and adds a point per signal (clamped to 5), with planning
and review floored at 3. Trivial turns skip the judge entirely.

### Scoring

1. **Gates.** Deprecated models, context fit (`input ≤ context × 0.9`), minimum
   context, required tools, and required vision are hard filters.
2. **Required quality.** Complexity maps to 0.25 / 0.40 / 0.55 / 0.75 / 0.90,
   plus 0.10 for high reasoning and 0.05 for planning or review, then the
   agent's quality floor.
3. **Quality estimate.** 45% price percentile, 25% parameter-size heuristic,
   15% context percentile, 15% reasoning support. Overrides win; free local
   models default to 0.35.
4. **Expected cost.** Input plus expected output at the model's context tier,
   with a cache-read discount (`pin.cacheHitRatio`, default 0.8).
5. **Policy weights.**

| Policy | Cost | Quality | Latency | Use when |
|---|---:|---:|---:|---|
| `cost` (default) | 0.6 | 0.3 | 0.1 | Cheapest model that clears the bar |
| `quality` | 0.1 | 0.8 | 0.1 | Quality matters more than spend |
| `latency` | 0.2 | 0.2 | 0.6 | Interactive work; favours local and flash tiers |

Changing the policy clears pins so the next turn is scored from scratch.

### Custom weights

Override any preset, and optionally vary the blend by turn class:

```jsonc
{
  "policy": "cost",
  "policyWeights": { "cost": 0.6, "quality": 0.35, "latency": 0.05 },
  "policyByClass": {
    "planning": { "cost": 0.1, "quality": 0.8, "latency": 0.1 },
    "review":   { "cost": 0.1, "quality": 0.8, "latency": 0.1 },
    "trivial":  { "cost": 0.85, "quality": 0.1, "latency": 0.05 }
  }
}
```

Turn classes are `trivial`, `routine`, `agentic`, `planning`, `review`, and
`tool_continuation`. A class override wins over `policyWeights`; omitted fields
inherit. `/router policy custom` prints the active weights and the config path.
Weights change which model wins a turn; pin thresholds decide whether the router
switches at all.

### Pinning

Provider prompt caches are per model and per provider. A switch pays one full
prefill, so routing alone would thrash the cache. The pin is the counterweight.

| Mode | Behaviour |
|---|---|
| `cache` | Keep the incumbent to reuse its cache; switch only on hard breaks |
| `balanced` (default) | Keep unless a challenger wins by `pin.switchThreshold` (0.12) |
| `switch` | Take the best every turn, with cold-cache scoring |

Even in `cache` or `balanced`, a pin is released by:

- idle TTL (`pin.idleTtlMs`, 5 min),
- a complexity jump of two or more,
- pin age (`pin.maxAgeMs`, 30 min) or pinned turns (`pin.maxTurns`, 8),
- an incumbent costing over `pin.costSwitchRatio` (4×) the cheapest **adequate**
  challenger,
- a flip-flop guard (`pin.flipFlopTurns`, 3),
- a gate failure, context overflow, compaction, policy change, or user override.

Picking a model yourself (`/model`) becomes a forced pin until you run
`/router auto`, the session compacts, or the model disappears.

### Provider failover

A 429, 5xx, timeout, auth, billing, or quota failure blocks the model for the
session — 5 min for rate limits, 1 min for server errors, 5 min for auth and
billing. Auth, payment, and quota failures block the whole provider; rate limits
and server errors block the one model. The pin is cleared and the next candidate
from the last decision is queued. OpenCode's `model.resolve` hook swaps it in on
the retry; if the host never retries, the next turn routes around the blocked
model. 400-class request errors are not treated as provider failures.

The pool needs a second provider or model for a switch to happen. `/router
pins` shows per-session blocks and pins, `/router debug` shows the active blocks,
and `failover.enabled: false` restores plain host behaviour.

### Context optimiser

When the assembled request fits, **nothing is changed** — cache-safe by
construction. When it does not fit, the optimiser works in order and stops as
soon as the request fits:

1. Deduplicate identical tool outputs, keeping the newest.
2. Truncate outputs above `optimiser.maxToolTokens` (2,000) to 60% head + 40%
   tail, with a marker.
3. Stub older tool outputs, largest first, keeping the last
   `keepRecentToolOutputs` (3).

System instructions, user text, the first user message, recent turns, and error
outputs are protected. If pruning cannot fit the request, the optimiser reports
`overflow`, clears the pin, and lets OpenCode compact; the next turn routes to a
model with a larger window. Compaction, title, and transient generation requests
are never pruned or routed.

### The three caches

These are unrelated and worth keeping apart:

| Cache | Scope | Invalidation |
|---|---|---|
| Provider prompt cache | Per model/provider; Anthropic markers, OpenAI prefix, oMLX KV | Not portable across models; the pin protects it |
| Judge verdict cache | In-process LRU, 128 entries, 10 min | Prompt fingerprint, agent, policy, pool, context tokens |
| Host catalog | OpenCode refreshes models.dev (~15 min) and exposes it live | Plugin caches the catalog for 2 s, `/models` for 60 s |

Pricing comes from the host catalog, so it follows models.dev automatically.
Local models have no catalog price; set
`providers.<id>.models.<id>.cost` if you want the cost policy to weigh them.

### Subagents

Subagents route independently, with their own pins, so an `explore` subagent can
run cheap and fast while the parent stays on a strong model. Detection is via the
child session's `parentID`; the agent identity comes from the session metadata.

Resolution order:

1. An explicit model configured on the agent (respected as a forced pin unless
   `subagents.overrideExplicitModel` is `true`).
2. `subagents.agents[agentID]`.
3. `subagents.default`.
4. The global policy.

The shipped defaults: `explore` is latency-first with 128k minimum context,
`general` is cost-first with a 0.55 floor, and `review`/`plan` are quality-first
with high floors. Loop escalation is per session, so a failing subagent escalates
itself without dragging the parent. On a score tie, a child prefers the parent's
model to reuse its cache.

## Choose the pool

The **pool** is the set of models the router may choose from. By default it uses
your host favorites. You can instead name the models explicitly:

```sh
opencode-model-router config set pool.source list
opencode-model-router config set pool.models '["deepseek/deepseek-flash","deepseek/deepseek-v4-pro"]'
opencode-model-router config set pool.minContext 32000
```

Or edit `~/.config/omlx-router/config.json`:

```jsonc
{
  "pool": {
    "source": "list",
    "models": [
      "deepseek/deepseek-flash",
      "deepseek/deepseek-v4-pro"
    ],
    "requireTools": true,
    "minContext": 32000
  }
}
```

| Source | Behaviour |
|---|---|
| `favorites` | Models favorited in OpenCode/Kilo (default). Empty favorites mean **no pool**; routing pauses rather than silently using every model |
| `list` | Exactly `pool.models` (use `provider/model#variant` for a variant) |
| `available` | Every eligible chat model the host advertises (explicit opt-in) |

An empty `favorites` pool does **not** fall back to all models. That prevents
zero-cost or unintended models from being selected without your opt-in; set
`source: "available"` if that is what you want. An unknown source selects
nothing and reports a warning. The TUI tells you when the pool is empty: at
startup and in `/router status` it points to `/router pool`, which offers
**Use my favorites**, **Enter an explicit list**, or **Use all available**.

`pool.include` / `pool.exclude` add or drop globs after the source; `maxModels`
caps the judge's candidate table; `requireTools` and `minContext` are hard
filters. `/router pool` (or `opencode-model-router pool`) shows the resolved pool, the
config path, and the exact commands to change it.

If model names do not contain parameter sizes (for example `deepseek-flash`
and `deepseek-v4-pro`), set explicit quality scores so the quality floor can
distinguish them:

```jsonc
{
  "quality": {
    "overrides": {
      "deepseek/deepseek-flash": 0.55,
      "deepseek/deepseek-v4-pro": 0.8
    }
  }
}
```

Quality is `0..1`; the router uses it with complexity/reasoning requirements.
Without overrides it falls back to price, context, name-size, and reasoning
heuristics.

## Choose a judge

The judge is a small instruct model served by a local OpenAI-compatible server
(oMLX, llama.cpp, or similar). It answers one short JSON
question per turn: how complex is this turn, does it need tools/vision/long
context, how much reasoning, and how confident is it.

A ~4B model is the sweet spot: fast enough for a per-turn hop, reliable enough
for structured output. Recommended: a Qwen3-4B-class MLX instruct model, pulled
through the oMLX app's model browser. A 1.7B-class model works for coarse
classification; a 27B model works but adds real prefill cost to every turn.

The plugin defaults to `judge.model: "auto"`, which picks the smallest model the
`/v1/models` endpoint advertises. Set it explicitly if you run several small
models:

```json
{ "judge": { "model": "Qwen3-4B-Instruct-2507-4bit" } }
```

### Pull the judge from the plugin (with consent)

The plugin can ask oMLX to download the recommended judge. It **never downloads
without an explicit confirmation**: you see the repository, parameter count,
download size, license, and source first.

```text
/router judge                 # offers the download when no suitable judge exists
/router judge pull [repo]     # explicit pull, same confirmation
/router judge status          # progress
/router judge cancel [task]   # cancel an active download
```

```sh
opencode-model-router judge pull              # prints the summary, asks y/N
opencode-model-router judge pull --yes        # skips only the prompt
opencode-model-router judge pull mlx-community/Some-Other-4B
opencode-model-router judge status
opencode-model-router judge cancel
```

The download uses oMLX's own admin API and its Hugging Face downloader, so the
model lands in oMLX's model directory and is discovered when complete. It needs
the oMLX **main** API key (sub-keys cannot administer downloads):

```jsonc
{
  "judge": {
    "provision": {
      "adminApiKey": "{env:OMLX_ADMIN_API_KEY}",
      "readSettingsKey": true,
      "repo": "mlx-community/Qwen3-4B-Instruct-2507-4bit"
    }
  }
}
```

If `adminApiKey` is unset, the plugin falls back to `auth.api_key` in
`~/.omlx/settings.json` when `readSettingsKey` is true. The key is only used for
the local admin login, never logged, and the session cookie stays in memory.
Non-MLX repositories are rejected unless `allowNonMlx` is set.

Verify with:

```text
/router judge
```

This prints the selected model, a sample verdict, and the round-trip latency.

### Using llama.cpp or another server

The verdict path is plain OpenAI-compatible: `GET /v1/models` and
`POST /v1/chat/completions`, an optional Bearer key, and `response_format` with a
fallback for servers that reject it. Point `judge.baseURL` at any such server.

```sh
llama-server -m Qwen3-4B-Instruct-2507-Q4_K_M.gguf --port 8080
```

```jsonc
{
  "judge": {
    "baseURL": "http://127.0.0.1:8080/v1",
    "model": "auto",                    // or the alias llama-server reports
    "provision": { "backend": "none" }  // optional; auto-detected anyway
  }
}
```

The download helper (`judge pull`, `judge status`, `judge cancel`) uses the oMLX
admin API. On any other endpoint the plugin detects that and prints the setup
recipe instead of failing. Routing, pinning, the optimiser, and timing are
backend-agnostic.

## Route to local models

Add the server as an OpenAI-compatible provider in the host, then include its
models in the pool. oMLX on `:1234` and llama.cpp on `:8080` both work:

```jsonc
"providers": {
  "omlx": {
    "package": "@opencode/ai/providers/openai-compatible",
    "settings": { "baseURL": "http://127.0.0.1:1234/v1" },
    "models": {
      "Qwen3.8-27B-MLX-4bit": { "capabilities": { "tools": true } }
    }
  }
}
```

The router detects loopback providers, prices them at zero
(`pool.localCostZero`), and gives them a size-based quality: under 3B 0.35,
3–8B 0.45, 8–30B 0.55, 30B+ 0.72. An 8k-token routine edit no longer counts as
hard work, so a local 27B can take those turns. Oversized local models still
lose to cloud models when the turn requires more; set `quality.overrides` when
you have a real measurement.

## Quality scores

Quality comes from two public datasets by default, with no API key:

1. **Epoch AI** — SWE-bench Verified or MirrorCode when the model is tracked,
   otherwise the Epoch Capabilities Index (ECI).
2. **LMArena** — the Code Arena (`webdev`) leaderboard.

Both are fetched from public endpoints, normalised into the same 0.35–0.97
band, and cached for 24 hours at `~/.local/state/omlx-router/quality.json`.
Source priority is configurable. `quality.overrides` always win; unmatched
models keep the heuristic or the local size tier.

```jsonc
{
  "quality": {
    "source": "auto",                    // auto | epoch | lmarena | manual
    "sources": ["epoch", "lmarena"],     // first match wins
    "refreshHours": 24
  }
}
```

```sh
opencode-model-router quality refresh     # fetch now
opencode-model-router quality status      # per-source counts and age
```

In the TUI: `/router quality` and `/router quality refresh`. `/router pool`
shows the score and its source for each model.

Set `"quality": { "source": "manual" }` to turn the fetch off. Epoch AI data is
[CC-BY](https://epoch.ai/benchmarks/use-this-data); LMArena is
[CC-BY-4.0](https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset).
Attribution to both is kept here.

## Pricing

A model's price is read from the host catalog first, then from public price
tables when the catalog has none. OpenCode reports `cost: []` for some providers
and all-zero prices for others; those used to show as `$0`, and a partially
reported price used to zero out the missing field. Missing prices now read as
`unknown`, and the router fills real gaps from:

1. **models.dev** — the same catalogue OpenCode reads, flat per-million prices.
2. **LiteLLM** — per-token costs converted to per million.

Neither needs an access token. Only missing or zero fields are filled, so
first-party billing still wins when the host reports it. The merged table is
cached for 24 hours at `~/.local/state/omlx-router/pricing.json`.

```jsonc
{
  "pricing": {
    "source": "modelsdev",                  // modelsdev | off
    "sources": ["modelsdev", "litellm"],    // first source wins per model
    "refreshHours": 24
  }
}
```

```sh
opencode-model-router pricing refresh
opencode-model-router pricing anthropic/claude-opus-5-5
```

In the TUI: `/router pricing` lists each pool model with its source, and
`/router pricing refresh` refetches. Local models are marked free regardless of
the table.

## Benchmarks

Modelled costs from published per-million-token prices, decisions from the real
WASM core with recorded verdicts, and an 80% cache-read assumption on repeated
turns. These measure routing and cost, not answer quality.

| Scenario | Short session (10 turns, 7k–34k) | Long session (24 turns, 12k–208k) |
|---|---:|---:|
| Router balanced | $0.444 (-50%) · 10/10 | $4.212 (-37%) · 24/24 |
| Router switch | $0.409 (-54%) · 10/10 | $4.190 (-38%) · 24/24 |
| Always frontier | $0.893 · 10/10 | $6.723 · 24/24 |
| Static complexity tiers | $0.690 (-23%) · 10/10 | $8.020 (+19%) · 24/24 |
| Fixed cheap model | $0.027 · 6/10 | $0.252 · 14/24 |

The short session favours `switch`; the long session favours `cache` or
`balanced`, because repeated cold prefills at 200k cost more than keeping the
incumbent cached. The router pool in both suites includes a local 27B and 4B at
zero cost.

Full method and caveats:
[short session](docs/benchmarks/2026-11-17-routing.md) ·
[long session](docs/benchmarks/2026-11-17-routing-long.md) ·
[live quality eval](docs/benchmarks/2026-11-17-quality.md).

The live eval runs eight small coding tasks through fixed models with
deterministic checks. All three models pass 8/8; the suite is at its ceiling, so
it does not yet separate cheap from frontier models.

## Configuration

One file is the source of truth: `~/.config/omlx-router/config.json`. Plugin
options in `opencode.jsonc` / Kilo config are read **once** to seed the file when
it does not exist; afterwards the file wins, so manual edits and the TUI picker
always behave predictably. `/router status` warns if the two drift.

Full example: [`config.example.json`](config.example.json).

```jsonc
{
  "enabled": true,
  "policy": "cost",                       // cost | quality | latency
  "policyWeights": null,                  // {cost, quality, latency} overrides
  "policyByClass": {},                    // e.g. planning: {quality: 0.8}

  "pool": {
    "source": "favorites",                // favorites | list | available
    "models": [],                         // used when source = list
    "include": [],                        // glob patterns, force-add
    "exclude": [],                        // glob patterns, drop
    "maxModels": 8,                       // judge table size
    "requireTools": true,
    "minContext": 32000,
    "localCostZero": true              // loopback providers cost 0
  },

  "judge": {
    "enabled": true,
    "baseURL": "http://127.0.0.1:1234/v1",
    "model": "auto",                      // or an explicit judge model id
    "apiKey": "{env:OMLX_API_KEY}",       // the server may not require one
    "timeoutMs": 5000,
    "cacheTtlMs": 600000,
    "cacheSize": 128,
    "provision": {
      "enabled": true,
      "backend": "auto",
      "repo": "mlx-community/Qwen3-4B-Instruct-2507-4bit",
      "adminApiKey": "{env:OMLX_ADMIN_API_KEY}",
      "readSettingsKey": true,
      "allowNonMlx": false
    }
  },

  "pin": {
    "mode": "balanced",                   // cache | balanced | switch
    "switchThreshold": 0.12,
    "idleTtlMs": 300000,
    "maxAgeMs": 1800000,
    "maxTurns": 8,
    "costSwitchRatio": 4.0,
    "flipFlopTurns": 3,
    "cacheHitRatio": 0.8
  },

  "optimiser": {
    "enabled": true,
    "reserveOutputTokens": 8192,
    "safetyTokens": 1024,
    "maxToolTokens": 2000,
    "keepRecentToolOutputs": 3,
    "keepRecentTurns": 2
  },

  "limits": {
    "shortfallTolerance": 0.2,
    "allowLocalForComplexity": 2,
    "expectedOutputTokens": 1200,
    "contextFitRatio": 0.9
  },

  "quality": {
    "overrides": {},                      // {"provider/model": 0.0..1.0} wins
    "source": "auto",                     // auto | epoch | lmarena | manual
    "sources": ["epoch", "lmarena"],      // first match wins
    "refreshHours": 24
  },
  "latency": { "overrides": {}, "localProviders": [] },

  "subagents": {
    "enabled": true,
    "overrideExplicitModel": false,
    "default": { "policy": "cost", "qualityFloor": 0.0 },
    "agents": {
      "explore": { "policy": "latency", "qualityFloor": 0.45, "minContext": 128000 },
      "general": { "policy": "cost",    "qualityFloor": 0.55 },
      "review":  { "policy": "quality", "qualityFloor": 0.75 },
      "plan":    { "policy": "quality", "qualityFloor": 0.8 }
    }
  },

  "telemetry": { "enabled": true },

  "failover": {
    "enabled": true,                      // route around provider failures
    "cooldownMs": 300000,                 // 429 cooldown
    "serverCooldownMs": 60000,            // 5xx / timeout cooldown
    "authCooldownMs": 1800000,            // 401/403 cooldown
    "redirectTtlMs": 60000,               // how long a queued redirect stays valid
    "retryDelayMs": 1000                  // delay when the host would not retry
  },

  "debug": false
}
```

Models without tool support, deprecated models, and models that cannot fit the
turn are excluded automatically. Local models (loopback providers) are never
chosen above complexity 2 unless you raise `limits.allowLocalForComplexity` or set
a quality override.

Model quality is a documented heuristic (price percentile, parameter size,
context size, reasoning support), not a benchmark. Zero-cost local models get a
default quality of 0.35. If the heuristic misjudges a model you use, override it:

```json
{
  "quality": { "overrides": { "omlx/Qwen3.8-27B-MLX-4bit": 0.72 } },
  "latency": { "overrides": { "openai/gpt-6.1-sol": 1400 } }
}
```

## Commands

The `/router` surface runs in the **OpenCode TUI** (the plugin's TUI part), so
status and settings never cost a model turn. The same actions are available in
the CLI for headless `opencode run`/`serve`, OpenCode Desktop, and Kilo.

| Command | Purpose |
|---|---|
| `/router` | Navigable action menu: status, policy, pool, timing, history, judge, pin, toggles |
| `/router status` | Compact status: state, judge, pins, timing, last decision |
| `/router version` | Router version, host, core ABI, and config path |
| `/router debug` | Diagnostics: paths, config digest, judge, pool, last decision, timing |
| `/router on` / `/router off` | Enable or disable routing |
| `/router policy` | Interactive picker for `cost` / `quality` / `latency`, or custom weights; clears pins |
| `/router pin-mode` | Interactive picker for `cache` / `balanced` / `switch` |
| `/router pool` | Interactive pool setup: favorites, explicit list, or all available; shows context, cost, and quality per model |
| `/router pricing [refresh]` | Input, output, and cache-read prices per pool model, with the price source |
| `/router pins [clear]` | Sessions with automatic routing state; list or clear |
| `/router history [n]` | Recent decisions, including subagents and judge/route time |
| `/router timing [n]` | Local judge vs remote model vs tool time per turn |
| `/router explain` | Readable why: chosen model, policy, verdict, top scores, and per-turn costs |
| `/router pin` / `/router auto` | Force or release a model pin for this session |
| `/router judge` | Probe the judge: model, latency, sample verdict |
| `/router subagents on\|off` | Toggle subagent routing |

Commands that take optional parameters print a `usage:` line naming them, and
an unknown parameter is rejected with the allowed values rather than ignored.

Menu items have descriptions and are navigable with the arrow keys, Enter, and
Esc. A palette entry, **"OpenCode Router: settings"**, opens the same menu without
typing a command. When routing changes the model, the plugin refreshes the
session and shows a short `model → …` toast; the host footer follows the
session model.

### CLI

Works in any host, including Kilo, headless OpenCode, and CI:

```sh
opencode-model-router status
opencode-model-router version [--json]
opencode-model-router debug [--json]
opencode-model-router doctor
opencode-model-router pool
opencode-model-router pricing [refresh|provider/model]
opencode-model-router history 20
opencode-model-router timing 20
opencode-model-router config get policy
opencode-model-router config set policy quality
```

`version` prints the bare version for scripts; `version --json` adds the package
name, ABI, host, and wasm path. `debug` is read-only and never prints secrets.

## Kilo limitations

Kilo 7.6.2 uses the V1 plugin API, which has no per-request model hook. The shim
switches the session model at the next request boundary; a decision therefore
applies to the following turn, and the decision log records
`applied: "boundary"`. If Kilo's model-switching API is unavailable to plugins,
the shim reports `kilo: unsupported` and stays out of the way rather than
pretending to route. Kilo has no `/router` command and no TUI settings dialog;
use the `opencode-model-router` CLI and `config.json`.

## Privacy

- Decision and turn records store **no prompt, message, or tool-output text** —
  only signals, model ids, scores, timings, token counts, cost, and a hashed
  session id.
- The only text that leaves the machine is the truncated turn summary in the
  judge request, sent to the `judge.baseURL` you configure (localhost by
  default).
- When quality scores are enabled, the plugin fetches public datasets from
  Epoch AI and Hugging Face (LMArena). Those requests contain no prompts,
  files, or local paths; set `quality.source` to `manual` to disable them.
- API keys are read from your config/env and never logged. The oMLX admin key
  may be read from the local `~/.omlx/settings.json` (when allowed) solely for
  the local download login.
- `opencode-model-router debug` prints a secret-free config digest, never key values.
- State is local: `~/.local/state/omlx-router/<host>/`.

## Troubleshooting

| Symptom | Check |
|---|---|
| Routing does nothing | `/router status`: enabled? pool empty? judge errors? |
| Judge timeouts | `/router judge`; raise `judge.timeoutMs`, use a smaller judge model |
| Wrong model chosen | `/router explain`; adjust `quality.overrides`, policy, or pool |
| Model switching visibly lags | Kilo boundary behaviour, or a host that rejects the switch; check the decision log |
| Context overflow | The optimiser reports `overflow`; raise the pool's context floor or reduce `reserveOutputTokens` |
| Config ignored | The file wins after first run; check `~/.config/omlx-router/config.json` and the drift warning in status |
| Prices look stale | The host refreshes models.dev on its own schedule; `/router pool` reads the live catalog |

When in doubt, run `/router debug` (TUI) or `opencode-model-router debug` (CLI) and include
its output in a bug report. It contains no prompt text and no credentials.

## Development

```sh
bun install
bun run build:wasm     # cargo build --target wasm32-unknown-unknown --release
bun test               # adapter + WASM bridge tests
bun run test:rust      # cargo test
bun run check          # fmt, clippy, tests, size gate
bun run test:e2e       # live prompt tests against OpenCode + Kilo (needs a local judge)
bun run test:e2e:live  # one prompt through the real local judge
bun run judge:calibrate # real judge verdicts + latency across six cases
bun run routing:eval    # real judge routing vs a ground-truth oracle
bun run bench           # deterministic routing/cost benchmark
bun run bench:long      # the same at 12k–208k context
bun run quality:eval    # live task-quality eval (spends provider tokens)
```

The prompt tests start real OpenCode/Kilo sessions, inject a deterministic
judge, and assert both the decision record and the model each host actually
used. See [tests/e2e/README.md](tests/e2e/README.md).

The repository uses [jj](https://github.com/jj-vcs/jj) on top of git
(colocated). Conventional commits, `main` is the release bookmark.

Layout:

```text
core/            Rust decision engine (no I/O), compiled to dist/core.wasm
src/             plain-JS host adapters, judge client, state, commands
src/tui.js       OpenCode TUI /router command + palette (plain JS)
bin/             CLI (opencode-model-router, alias omlx-router)
tests/           Bun tests and fixtures
docs/            design spec and deeper docs
```

## License

Apache-2.0. See [LICENSE](LICENSE).
