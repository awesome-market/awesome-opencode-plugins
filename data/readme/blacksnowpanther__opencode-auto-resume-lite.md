# opencode-auto-resume-lite

A minimal, dependency-free **auto-resume watchdog** for [OpenCode](https://opencode.ai) **V2**.

When a model stalls mid-response — a dropped stream, a silent provider timeout, a rate-limit, a hung tool call — OpenCode just sits there until you type "continue" yourself. This plugin watches sessions and resumes them automatically, **and keeps trying indefinitely** instead of giving up after a fixed number of attempts.

- **No subscriptions, no accounts, no telemetry**
- **Single file of TypeScript**, MIT licensed
- **No runtime dependencies** beyond `@opencode/plugin`
- **Never permanently gives up** — per-burst budget with a growing cooldown
- **Tunable** down to a few seconds

## Install

Clone the repo somewhere permanent:

```sh
git clone https://github.com/BlackSnowPanther/opencode-auto-resume-lite.git
cd opencode-auto-resume-lite
npm install
npm run build
```

Then reference the local package in `opencode.jsonc` (project) or `~/.config/opencode/opencode.jsonc` (global):

```jsonc
{
  "plugins": [
    {
      "package": "file:///absolute/path/to/opencode-auto-resume-lite",
      "options": {
        "stallMs": 120000,
        "maxNudges": 4,
        "cooldownMs": 60000,
        "maxCooldownMs": 1800000,
        "failureGraceMs": 3000,
        "debug": false
      }
    }
  ]
}
```

All options are optional; the defaults above are what ship.

## Options

| Option | Type | Default | Description |
|---|---|---|---|
| `stallMs` | number | `120000` | How long a session may be `busy` with no activity before it is treated as stalled. |
| `checkEveryMs` | number | `8000` | How often the watchdog re-checks its per-session state. |
| `maxNudges` | number | `4` | Resume attempts allowed in one burst before a cooldown. Resets on any clean turn. |
| `baseDelayMs` | number | `2500` | First resume delay; doubles per attempt within a burst. |
| `maxDelayMs` | number | `45000` | Cap on the per-attempt resume delay. |
| `cooldownMs` | number | `60000` | First cooldown after a burst is used up. Doubles each burst. |
| `maxCooldownMs` | number | `1800000` | Cap on the cooldown (30 min). |
| `failureGraceMs` | number | `3000` | Wait after a terminal failure before nudging, so OpenCode's own retry can settle. |
| `interruptGraceMs` | number | `1500` | Wait after a stall-interrupt before sending the continue prompt. |
| `startTimeoutMs` | number | `20000` | If an accepted resume prompt produces no execution in this window, try again. |
| `maxToolRunMs` | number | `3600000` | A tool running longer than this no longer blocks recovery. |
| `maxRecoveryAgeMs` | number | `21600000` | Stop auto-recovering a session idle after failure longer than this (6 h). |
| `forgetAfterMs` | number | `1800000` | Drop idle, healthy sessions from memory after this long. |
| `nudgeText` | string | see below | Text sent to resume the session. |
| `logFile` | string | — | Append a recovery log to this path (keep it **outside** any watched config folder). |
| `debug` | boolean | `false` | Log every event and decision to the console. |

Default nudge text:

```
Your previous response was interrupted by a timeout or stall. Continue exactly where you left off and finish the task. Do not restart or repeat work that is already done.
```

## How it works

1. **Retry hook** — timeout-like provider errors (`rate limit`, `gateway`, `overloaded`, `socket hang up`, `408/499/504`, …) are made retryable inside OpenCode, while permanent errors (`400/401/403/404/422`, bad key, unknown model, context length) are left alone.
2. **Failure recovery** — on a terminal `session.execution.failed` that looks timeout-like, the plugin waits `failureGraceMs` and then sends the nudge, unless the session already resumed itself. A provider `retryAfterMs` is honored as a cooldown.
3. **Stall recovery** — a session that stays `busy` with no activity for `stallMs`, with no tool or permission pending, is interrupted and nudged.
4. **Per-burst budget, never permanent** — after `maxNudges` attempts without a clean turn, the plugin enters a cooldown (`cooldownMs`, doubling up to `maxCooldownMs`) and then **tries again, forever**. A successful turn or a genuine user turn resets the burst.
5. A resume prompt is only counted when it is actually delivered; a `session.prompt` that throws does not burn an attempt. The plugin re-checks `time.busy` vs `time.idle` before and after the delay so it never double-prompts a session that recovered on its own.

The event stream reconnects automatically with backoff, tool tracking has a TTL so a hung tool can't block recovery, and a process-global singleton prevents double-nudging if the plugin is loaded twice.

## Tuning

For near-instant recovery:

```jsonc
"options": { "stallMs": 15000, "checkEveryMs": 2000 }
```

Tips:

- Keep your provider timeouts **longer** than `stallMs` so the plugin can nudge before the transport gives up.
- If your model legitimately pauses for long reasoning stretches, raise `stallMs` instead of disabling the plugin.
- Set `logFile` (outside any watched config folder) and read it to watch bursts and cooldowns, e.g. `resuming … (attempt 2/4, burst 1)`.

## Development

```sh
npm install
npm run build     # emits dist/index.js + dist/index.d.ts
npm run dev       # watch mode
```

`dist/` is committed so the plugin works straight from a clone without a build step.

## License

MIT © BlackSnowPanther