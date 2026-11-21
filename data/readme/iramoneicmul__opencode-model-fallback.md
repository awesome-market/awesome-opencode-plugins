# opencode-model-fallback

> 🇬🇧 English · [Version française](README.fr.md)

Automatic model failover for [opencode](https://opencode.ai): keep the **free tier** as the default
model, fall back to your **paid subscription** when the free provider returns a quota error or is
unavailable, and go back to the free tier **as soon as its quota resets**.

> `opencode.json` has no fallback field. `model` and `small_model` are single strings, and unknown keys
> make opencode refuse to start. This plugin fills that gap: opencode is told to load a plugin, and the
> plugin owns the model chain.

> **Version note.** This repository ships the **V1** plugin (`plugin/model-fallback.ts`, `config` /
> `event` / `chat.message` hooks, opencode 1.18+). opencode 2.x replaced that API with `Plugin.define`,
> a session `prompt` hook and an event stream; the author's machine runs that **V2** variant from
> `~/.config/opencode/lib/model-fallback/index.ts`. The manual-choice fix described below is **ported
> to both variants**: the `chat.message` hook of the V1 plugin in this repository and the `prompt`
> hook of the V2 variant in service.

```
opencode/big-pickle (free)   →   opencode-go/qwen3.8-flash   →   opencode-go/qwen3.8-max
        ↑ default                    ↑ first fallback              ↑ last resort
   retried first on
   every new attempt
```

---

## Features

1. **Free first, always.** The first model of the chain is the default, for both `model` and
   `small_model` (titles, summaries, compaction).
2. **Instant failover.** When a request fails with a quota / rate-limit / overload / network error, the
   failed turn is replayed automatically on the next model of the chain.
3. **Automatic return.** Every subsequent attempt tries the free model again. As soon as a request
   succeeds on the free model, the chain resets to its default — including across restarts.
4. **Resilient across restarts.** The active fallback is persisted, so quitting and relaunching opencode
   while the free tier is exhausted starts you on the fallback instead of throwing an error.
5. **No false positives.** Output-length errors, user aborts and plain auth failures do **not** trigger a
   switch. There is no background polling of the free endpoint.
6. **No secrets in the plugin.** The plugin never reads or writes API keys; it only reads the model
   chosen by opencode and replays turns.
7. **Manual model choices are respected.** Switching model by hand in the TUI is no longer cancelled
   on the next turn: the forced retry on the free model is paused as long as you stay on your choice,
   and resumes only after a real failure (see [Manual model choice respected](#manual-model-choice-respected-fix)).

---

## Requirements

- opencode **1.18+** (uses the `chat.message` and `event` plugin hooks and `session.prompt` with a
  `model` override)
- A model provider that can return quota errors, e.g. OpenCode Zen free tier + an OpenCode GO
  subscription. Any chain of `provider/model` ids works.
- Node 22+/Bun only if you want to run the test suite (no build step: the plugin is a single `.ts` file
  loaded directly by opencode).

---

## Installation

**1. Copy the plugin** into a directory that opencode can load. Do **not** put it in
`~/.config/opencode/plugin/` if you also declare it in `opencode.json`: that folder is auto-discovered,
and a file present in both places is loaded twice (duplicate hooks).

```bash
mkdir -p ~/.config/opencode/lib
curl -fsSL https://raw.githubusercontent.com/iramoneicmul/opencode-model-fallback/main/plugin/model-fallback.ts \
  -o ~/.config/opencode/lib/model-fallback.ts
```

**2. Declare it in `~/.config/opencode/opencode.json`** using the tuple form so you can pass options:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/big-pickle",
  "small_model": "opencode/big-pickle",
  "plugin": [
    [
      "file:///home/you/.config/opencode/lib/model-fallback.ts",
      {
        "chain": [
          "opencode/big-pickle",
          "opencode-go/qwen3.8-flash",
          "opencode-go/qwen3.8-max"
        ],
        "switchBackInSession": true,
        "freeRetryCooldownMs": 45000,
        "verbose": true
      }
    ]
  ]
}
```

> Use an **absolute** `file://` path. On a different username, change `/home/you` accordingly.

**3. Restart opencode.** The configuration is read once at startup; a running session keeps the model
it already resolved.

### Option: no options needed

If you are happy with the default chain, drop the file in `~/.config/opencode/plugin/` (or
`~/.config/opencode/plugins/`) and it is auto-discovered — no `plugin` entry required. You then lose the
ability to customise the chain, so the tuple form is recommended.

---

## Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `chain` | `string[]` | `["opencode/big-pickle", "opencode-go/qwen3.8-flash", "opencode-go/qwen3.8-max"]` | Ordered list of `provider/model` ids. First = default, last = last resort. |
| `maxChain` | `number` | length of `chain` | Truncate the chain (useful to ignore the last entries). |
| `switchBackInSession` | `boolean` | `true` | Retry the first model on the next turn even when the session is already on a fallback. |
| `freeRetryCooldownMs` | `number` | `45000` | Minimum delay between two attempts on the free model (anti-storm). |
| `stateFile` | `string` | `~/.local/state/opencode/model-fallback.json` | State file location (mostly for tests). |
| `verbose` | `boolean` | `true` | Write decisions to the log file. |

`config.model` and `config.small_model` are overwritten by the plugin at startup with the currently
active model. `small_model` is only set if you did not define one.

---

## How it works

The plugin registers three hooks.

### `config` — startup

```
cfg.model       = chain[state.activeIndex]   # 0 = free, otherwise the fallback remembered from last run
cfg.small_model = chain[0]                   # only if not already defined
```

This is what makes a restart "remember" an exhausted free tier.

### `event` — errors and successes

`message.updated` events carry the failing assistant message (`providerID`, `modelID`, `error`) and
`session.error` carries session-level provider errors. A failure is *fallback-worthy* when the error name
is not in the ignore list and one of these patterns matches `data.message`, `data.responseBody` or
`data.statusCode`:

- **quota / rate limit** — `rate limit`, `429`, `too many requests`, `quota`, `insufficient_quota`,
  `usage limit`, `limit reached|exceeded`, `exceeded your`, `billing`
- **unavailable** — `overloaded`, `502|503|504|529`, `service unavailable`, `temporarily unavailable`,
  `no available model|provider|capacity`, `capacity`, `upstream`
- **network** — `timeout`, `timed out`, `ECONNRESET`, `socket hang up`, `ETIMEDOUT`, `network error`,
  `fetch failed`

Ignored on purpose: `MessageOutputLengthError` (answer too long — not a quota problem),
`MessageAbortedError` (user cancellation) and `ProviderAuthError` whose message mentions neither quota
nor billing (a bad key should not burn paid tokens).

On a fallback-worthy error, the plugin:

1. identifies the failing model from the assistant message (falling back to the last known model),
2. moves to the **next** index in the chain (or gives up cleanly if the chain is exhausted),
3. persists the state,
4. re-reads the last user message via `client.session.messages` and replays it on the fallback model via
   `client.session.prompt({ body: { model: { providerID, modelID }, parts } })`.

A `handled` set keyed by `sessionID + messageID + index` prevents a turn from being escalated twice to
the same model.

When an assistant message **succeeds** on `chain[0]`, the plugin resets `activeIndex`/`since` to `0`:
the free quota is considered restored.

### `chat.message` — free-first retry

```
if state.since == 0                      → no failover ever happened: do nothing (manual choice respected)
if the session has a manual choice       → nothing: the user's pick wins (see the fix below)
if the turn already targets chain[0]     → nothing to do
if now - lastFreeAttemptAt < cooldown   → wait (anti-storm)
otherwise                                → client.session.abort() then replay the turn on chain[0]
```

This is the literal implementation of *"the next attempt retries the first model"*, and it is also how
the plugin learns that the quota window rolled over. In the V2 variant the equivalent is the
`ctx.session.hook("prompt")` hook, augmented with manual-choice detection (see
[Manual model choice respected](#manual-model-choice-respected-fix)).

### State machine

```
        ┌────────────────────────────┐
        │ index 0 : FREE MODEL       │  ← initial and resting state
        └─────────────┬──────────────┘
                      │ quota / 5xx / network error
                      ▼
        ┌────────────────────────────┐
        │ index 1 : first fallback   │  activeIndex=1, since=ts, switches++
        └─────────────┬──────────────┘
                      │ same error
                      ▼
        ┌────────────────────────────┐
        │ index 2 : last resort      │
        └─────────────┬──────────────┘
                      │ error → "chain exhausted", give up (failing model stays visible)
     ┌────────────────┴─────────────────────┐
     │                                      │
     │ success on chain[0], or               │ next turn, free model retried
     │ next turn retried on chain[0] and OK  │ and answering
     ▼                                      ▼
   index 0 (default)                     index 0
```

---

## Manual model choice respected (fix)

### The bug

With `switchBackInSession: true`, the prompt hook forced a return to `chain[0]` **on every turn**
as soon as a failover episode was active (`state.since != 0`):

1. the user picks `opencode/space-bunny-free` in the TUI model selector;
2. they send their message;
3. the hook sees `since != 0` and a model != `chain[0]` → `session.switchModel()` back to
   `opencode/big-pickle`;
4. the TUI shows Big Pickle again, as if the choice had never been made.

Worse: `since` is only reset by a **success on `chain[0]`**. As long as Big Pickle had not succeeded
a turn, the episode stayed open and **every** manual choice was cancelled, even when the chosen model
answered perfectly. The log then looped:

```
10:06:26 retentative sur le modele gratuit opencode/big-pickle
10:12:56 retentative sur le modele gratuit opencode/big-pickle
10:14:28 retentative sur le modele gratuit opencode/big-pickle
```

### How the fix works

The plugin now distinguishes **two ways** of changing model:

| Origin of the change | Effect |
| --- | --- |
| The plugin itself (`replay`, free-first retry) | Nothing changes: the forced retry stays armed |
| The user (TUI selector, `/model`) | The forced retry is **suspended for that session** |

Three in-memory structures (per session, not persisted) carry the logic — in **both** plugin
variants (`plugin/model-fallback.ts` and `~/.config/opencode/lib/model-fallback/index.ts`):

```ts
const observed = new Map<string, string>()   // last model seen for the session
const manualChoice = new Set<string>()       // sessions with a manual choice active
const selfSwitch = new Map<string, string>() // last plugin-driven switch, to tell it apart
```

`noteSelfSwitch(sessionID, id)` records a plugin-driven switch: it sets `observed` + `selfSwitch`
and **clears** `manualChoice` (automatic failover takes back control).

On every turn, the hook compares the session's actual model:

```ts
// forced set   → we were waiting for OUR switch: a different model means the user changed it
// forced unset → compare with the last observed model: a difference means a manual choice
```

Then, before the forced-retry logic:

```ts
if (manualChoice.has(sessionID)) return   // the user chose: touch nothing
```

### Lifecycle of a manual choice

```
 manual pick (UI)       quota/5xx failure on that model       success on chain[0]
       │                           │                               │
       ▼                           ▼                               ▼
 manualChoice = true  →  escalate(): manualChoice       →  manualChoice cleared
 retry suspended            cleared + failover to chain[i+1]   (state reset to zero)
```

- **Activation**: detected when the next prompt is admitted (the TUI fires no hook on selector change
  alone).
- **Release 1 — failure**: an escalation (`session.step.failed` / `session.execution.failed` in V2,
  `message.updated` / `session.error` in V1, with a quota reason) clears `manualChoice`: failover takes
  back control, including replaying the turn.
- **Release 2 — back to the free model**: if the user re-selects `chain[0]` themselves,
  `manualChoice` is cleared (normal state restored).
- **Release 3 — plugin-driven switch**: every `replay` / free-first retry goes through
  `noteSelfSwitch`, which clears `manualChoice`.

Log lines (in `model-fallback.log`):

```
manual choice opencode/space-bunny-free -> forced retry on opencode/big-pickle suspended (until next failure)   # V1
choix manuel opencode/space-bunny-free -> retour force opencode/big-pickle suspendu (jusqu'au prochain echec)  # V2
```

### What the fix does not change

- **Restarts**: the startup hook (`config` in V1, `ctx.model.transform` in V2) still applies
  `chain[activeIndex]` as the default → a new session starts on the remembered fallback. A manual
  choice only lasts for the current session (the markers live in memory).
- **Automatic escalation**: if Space Bunny Free returns a `Rate limit exceeded`, the turn is still
  replayed on the next chain entry — you never get stuck on a failing model.
- **`switchBackInSession: false`** remains the blunt option: it disables the forced retry outright,
  with no pause mechanism.

### Verification

```bash
# editing the plugin is enough: the opencode watcher reloads it (see "loading plugin" in opencode.log)
tail -f ~/.local/state/opencode/model-fallback.log

# in the TUI: switch model, send a message, check the selector still shows your pick
# and no "retentative" line appears
```

---

## Why the plugin does not probe the free endpoint

An earlier version polled `https://opencode.ai/zen/v1/chat/completions` to know whether the free quota
had reset. OpenCode Zen rejects it:

```json
{"type":"error","error":{"type":"FreeTierError",
 "message":"OpenCode's free tier can only be used from within OpenCode"}}
```

The free tier only serves requests made by opencode itself. So the plugin does **no** polling and no
request spoofing: quota recovery is detected from opencode's own signals (a success on the free model)
and free-tier availability is tested simply by trying again on the next turn. Cost: zero, and no false
positives.

---

## State and logs

| Path | Content |
| --- | --- |
| `~/.local/state/opencode/model-fallback.json` | `currentIndex`, `activeIndex`, `since`, `lastReason`, `lastFreeAttemptAt`, `lastFreeSuccessAt`, `switches` |
| `~/.local/state/opencode/model-fallback.log` | one line per decision (startup model, failover, replay, quota restored) |

```bash
cat ~/.local/state/opencode/model-fallback.json   # current state
tail -20 ~/.local/state/opencode/model-fallback.log

# force a return to the free model
echo '{"currentIndex":0,"activeIndex":0,"since":0,"lastReason":"","lastFreeAttemptAt":0,"lastFreeSuccessAt":0,"switches":0}' \
  > ~/.local/state/opencode/model-fallback.json
```

`auth.json` is never touched: authentication stays entirely under opencode's control.

---

## Testing

The suite simulates the opencode client (no network, temporary state file):

```bash
npm test
# or
node --experimental-strip-types test/model-fallback.test.mjs
# test another copy of the plugin
node --experimental-strip-types test/model-fallback.test.mjs /path/to/model-fallback.ts
```

24 assertions: default model, `small_model` handling, quota escalation, 503 escalation, chain
exhaustion, restart remembering the fallback, free-first retry, quota-restored reset, manual choice
respected, custom chain, the anti-loop guard, and the full lifecycle of a manual choice during a
failover episode (respected, still in effect next turn, lifted by a failure, forced retry armed
again).

---

## Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| Nothing happens on quota errors | Check `plugin` is declared in the **global** config, then restart opencode; check `~/.local/state/opencode/model-fallback.log` exists |
| The model reverts to the free tier after a manual switch | **Fixed** (V1 and V2): a manual choice pauses the forced retry. If it persists, look for a `manual choice … suspended` (V1) or `choix manuel … suspendu` (V2) line in the log, and check the loaded plugin is `lib/model-fallback/index.ts` |
| It switches to a paid model although the free tier works | The error matched a quota pattern; inspect `lastReason` in the state file |
| The free model is used but the UI still shows a paid model | The UI model selection is applied per turn; the plugin replays the turn on the free model, the next turn may need one more retry |
| Duplicate user message in the transcript | Replayed parts are sent with `synthetic: true`; some opencode versions still display them |
| Subagent (`task` tool) failures do not switch models | Sub-agent errors usually surface as tool errors, not assistant errors |
| Plugin does not load after editing | `opencode.log` (`~/.local/share/opencode/log/`) contains the load error; the config is only read at startup |

---

## Known limitations

1. A config change requires a restart; running sessions keep their resolved model.
2. Switchover is per turn: requests already in flight are not migrated, the next turn is replayed.
3. Sub-agents may not trigger a switch (see troubleshooting).
4. The plugin does not know the free tier's reset window, by design: it simply prefers the free model on
   every attempt.
5. The state file is not process-safe; with several opencode windows the last writer wins. Harmless: it
   only decides which model a *new* session starts on.
6. The manual-choice markers (`manualChoice`, `observed`, `selfSwitch`) live **in memory**: they do not
   survive a plugin reload nor a new session. A manual choice also does not prevent escalation when the
   chosen model itself hits a quota error.

---

## Security

- The plugin contains no credentials and makes no network call of its own.
- It never reads or writes `~/.local/share/opencode/auth.json`.
- Replayed user text is sent to the *same* session on another provider — if your fallback provider is a
  different vendor than your free provider, the text of that turn is sent to it. Pick your chain
  accordingly.

---

## License

MIT — see [LICENSE](LICENSE). Contributions welcome (open an issue or a PR).
