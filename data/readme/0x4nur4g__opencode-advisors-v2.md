# opencode-advisors-v2

Native OpenCode V2 advisor/watchdog plugin. Attaches passive reviewer personas to an OpenCode session. Each reviewer observes completed primary-agent model steps, independently checks for mistakes or drift, and emits at most one concise note (nit / concern / blocker).

## Install

**Git (recommended):**

```jsonc
// ~/.config/opencode/opencode.json (or project opencode.json)
{
  "plugins": [
    {
      "package": "github:0x4nur4g/opencode-advisors-v2",
      "options": {
        "enabled": true,
        "defaultModel": "anthropic/claude-sonnet-4-5#medium",
        "advisors": [
          { "name": "Skeptic", "instructions": "Challenge assumptions..." }
        ]
      }
    }
  ]
}
```

Works on any machine with git access; pin a commit with `github:0x4nur4g/opencode-advisors-v2#<commit>` (or track the default branch with `github:0x4nur4g/opencode-advisors-v2#main`).

**Local checkout:**

```bash
bun install          # dev dependencies only
```

```jsonc
{
  "plugins": [
    { "package": "/absolute/path/to/opencode-advisors-v2", "options": { "enabled": true } }
  ]
}
```

This minimal form activates the built-in Skeptic advisor bound to the configured default model (see Configuration).

The plugin loads from TypeScript source with no build step: the OpenCode
directory loader resolves the repo-root `index.ts` (a 3-line re-export of
`src/index.ts`), with `package.json` beside it as the loader requires. The
`exports` field points tooling and import consumers at the same root
`index.ts`; `bun run bundle` remains available as optional local tooling.

The plugin is **disabled unless `enabled: true`** is set. There is no implicit activation from a sidecar config file.

## Compatibility

OpenCode v2 line only — v1 is not supported.

Status: **experimental** (v0.1.0). The plugin is written against the v2 plugin
API; plugin loading is live-verified on opencode v2.0.5 (serve probe,
2026-09-17), and the raw `{ id, setup }` object-export contract it uses has
been verified from the beta line (beta-18286) through v2.0.5. Some host
surfaces the plugin relies on (agent transform on plugin-defined agents, the
session context hook) are not live-verified on every runtime build — pin a
commit for stability.

## Configuration

Key options (the full option set is defined in `src/options.ts`):

| Key | Default | Notes |
|---|---|---|
| `enabled` | `false` | Must be `true` to activate |
| `defaultModel` | — | `provider/model#variant` |
| `advisors` | built-in `Skeptic` | Array of persona definitions; omitted key → built-in default; explicit array (incl. `[]`) replaces it entirely |
| `review.mode` | `"async"` | `"async"` or `"sync"` |
| `review.maxParallel` | `3` | `1..8` |
| `review.timeoutMs` | `30000` | `1000..120000` |
| `delivery.immuneTurns` | `3` | `0..20` |
| `delivery.wakeOnTerminalBlocker` | `true` | Blocker on an idle-terminal session wakes it with the note; `false` queues instead |
| `delivery.hardInterruptBlockers` | `false` | Experimental opt-in. Blocker on a RUNNING session: interrupt the in-flight turn, then wake the stopped session with the note. The host documents no deadline/cancellation guarantee for `ctx.session.interrupt`; the bare call can stall review processing |

Out-of-range values are rejected with a path-specific error, not silently clamped.

When the `advisors` key is omitted and the plugin is enabled, one built-in
advisor — **Skeptic** — is registered automatically, bound to `defaultModel`
and marked `[builtin]` in `advisor-status` output. An explicit `advisors`
array always replaces the default entirely (it is never merged), and an
explicit empty array (`[]`) registers no advisors at all — a deliberate
opt-out.

## Reviews and Controls

Reviews are fully automated and passive: session hooks observe context, updates
queue inside the runtime, thresholds drain the queue, and advisory notes are
delivered as synthetic session messages (`ctx.session.synthetic`). No tool call
or manual trigger is involved.

Advisory notes post with an explicit `delivery` mode. `queue` deliveries
promote FIFO at the end of the next drain (one head promotes when the drain
would otherwise end), so a queued advisory enters the transcript and the
outbound model context of the successor turn, ordered after pending user
turns; `steer` promotes at the next safe provider-turn boundary. An
independent `resume` wake policy is selected by the severity/state matrix —
the host default is never relied on. A failed post is retained as bounded
post-only retry state and re-posted on later session events (no regeneration,
FIFO: one attempt at emission plus at most 3 bounded retries — 4 total post
attempts — before abandonment). Emission dedupe state commits only after
durable admission, so a lost post never silently suppresses the note. See
[Attention parity and blocker interruption](#attention-parity-and-blocker-interruption-product-requirement-2026-09-24)
for the full severity/state matrix and the blocker interrupt flow.

Advisor sessions are created with the advisor's configured model bound
explicitly at session creation (per-advisor override, else the plugin
default) — hosts otherwise resolve a session's run model from the
session/config default, which would leak the primary model into advisor runs.

The only user-facing controls are two administrative commands:

| Command | Effect |
|---|---|
| `advisor-status` | Reads in-memory runtime state for the current session and posts a bounded status notification (status, queue depth, per-advisor model, health, metrics). |
| `advisor-reset` | Clears the current session's advisor state (buffers, queue, dedupe, cooldown) and posts a deterministic confirmation. |

Both run directly in the plugin process: they read or mutate in-memory state and
post a notification-style message with `resume:false`, so it appears in the
session inbox without scheduling any model execution — invoking either command
performs zero primary-model generation. They stay silent when invoked without a
session (headless runs). There are no model-callable advisor tools and no manual
review command.

## Attention parity and blocker interruption (product requirement 2026-09-24)

**Requirement:** every advisor note must be at least as visible/attended as a
normal chat message to the session it reviews — never a lower-priority,
invisible inbox artifact. Blockers may additionally interrupt the running
target session, experimental and opt-in (see below).

### Delivery matrix

| State | nit | concern | blocker |
|---|---|---|---|
| Running | steer | steer | steer (interrupt-then-wake when `hardInterruptBlockers: true`) |
| Idle terminal | resume | resume | resume when `wakeOnTerminalBlocker`; else queue |
| Idle incomplete | resume | resume | resume |
| User interrupted | queue | queue | queue |
| Cooldown | steer/resume by state | steer/resume by state | steer/resume by state |

- `steer` = admitted at the next safe provider-turn boundary; the note keeps
  its synthetic advisor provenance and does not impersonate a user or system
  message — the host picks the boundary, which is not necessarily the same
  scheduling or authority as a normal user message. A `queue` delivery
  promotes behind pending user turns, which live observation on 2026-09-24
  confirmed is strictly lower ordering.
- `resume` = wake the idle session so the note becomes the next turn's input
  (one drain, exactly one successor provider turn).
- Only user-interrupted sessions queue; an idle-terminal blocker with an
  explicit `delivery.wakeOnTerminalBlocker: false` also queues — every other
  note steers or resumes by state, cooldown included.
- Blocker + running + `delivery.hardInterruptBlockers: true` (experimental,
  default `false`): the plugin calls `ctx.session.interrupt` first and then
  posts the note with `resume: true` (interrupt FIRST, note SECOND). When the
  call resolves, the interrupted turn ends and the note wakes the session as
  the next turn's input — one successor turn. The reverse order is forbidden: a
  note posted before the interrupt stays inbox-only indefinitely (silent loss),
  observed in the 2026-09-24 single-file host-ordering probe on opencode
  v2.0.15, which covers only the resolved path. The host documents no
  AbortSignal/deadline/cancellation guarantee for this RPC: the call is a bare
  await and can stall review processing.

### Interrupt loss, as the user sees it

The in-flight turn is aborted: unsettled tool calls fail with
`Tool execution interrupted`, partial assistant text is retained, the execution
outcome is `interrupted`, and then the resumed turn attends the note. The
interrupt fires `session.execution.interrupted` with `reason: "user"` — from the
host's perspective it is indistinguishable from a user stop, and the plugin
treats it the same way (further steers are suppressed until the next execution
start; the armed cooldown bounds the next interrupt).

### Authority boundary

Notes travel only through `ctx.session.synthetic`: the transcript types them as
synthetic messages with the advisor's XML attribution in the body
(`<advisory advisor="..." severity="...">`). The plugin never writes
system/developer authority, never injects a `session.prompt` user message, and
never impersonates user consent.

### Residual non-parity (accepted, by design)

Only user-interrupted sessions deliberately stay `queue` (plus the explicit
`delivery.wakeOnTerminalBlocker: false` case for idle-terminal blockers):

- **User interrupted** — after the user stops a turn, advisories must not
  restart it. This is a user-preserved safeguard.

Cooldown is not a delivery exception: it arms only after a resolved opt-in hard
interrupt and suppresses repeated hard INTERRUPTS only. Notes keep their
state-appropriate steer/resume during cooldown. Queued notes are not lost: they
promote on the next actionable turn instead of waking the session.

### Rate and cost

Each wake is one successor provider turn (≈ 1 model request) plus the reviewer
generation that produced the note. A hard interrupt resolved in ≈ 10 ms in the
single v2.0.15 host-ordering probe (2026-09-24) — a dated observation of the
resolved path, not a general latency ceiling (the call has no host deadline).

Loop bounding:

- the cooldown (`immuneTurns`, default 3) arms only after a resolved opt-in hard
  interrupt and decrements on step ends; it suppresses repeated hard INTERRUPTS
  only — notes are never queued or demoted by it;
- severity-escalation dedupe is bounded (4096 entries) and suppresses identical
  notes; only an escalated severity re-emits. Paraphrased notes are not deduped
  and can wake again;
- the noise filter drops low-signal notes, reviewers see their own prior notes
  (`priorAdvice`), and repeated reviewer failure halts the advisor;
- the interrupt path additionally requires blocker + running + a steered
  non-user-interrupted row + no active cooldown, so the interrupt ceiling is ≈ 1
  per cooldown window per session.

Honest limit: **there is no hard per-session reviewer/wake/spend cap.** The
exact-note dedupe bound above is the only repeat suppression; paraphrased notes
can wake again, and the model unit price is unknown, so spend is not
quantified.

### Historical backlog (not retroactive)

This change affects only NEW emissions. Already-parked inbox notes (~10-12
across 14 sessions as of 2026-09-24) are NOT auto-drained: there is no polling,
no scheduler, no timers. They promote only if their session naturally runs
again.

### Scope

The mechanism is session-level and identical for worker/lead/orchestrator
target sessions: the plugin reviews any session in the registered directory and
posts to THAT session. There is no automatic cross-session parent broadcast in
the host — a completed child's wake is attended in the child's own transcript;
parent-side visibility is outside this plugin.

### Testable acceptance criteria

- fake blocker control (running session, `hardInterruptBlockers: true`):
  `session.interrupt` fired, the note is in the transcript, and the resumed
  turn contains a model ACK;
- fake concern and nit controls (running session): no interrupt; nit still
  steers at a boundary;
- idle-terminal concern/nit: the session wakes and the note is the next turn's
  input;
- user-interrupt control: no interrupt, no wake (queued);
- repeated identical note: deduped, no second interrupt;
- completed-child wake: attended in the child's own transcript.

## Bundle

```bash
bun run bundle   # optional local tooling: dist/index.js
bun run typecheck
bun test
```

The script is named `bundle`, not `build`: lifecycle-named scripts (`build`, `prepare`, `preinstall`, `postinstall`, `install`, `prepack`) trigger the host's git-dependency preparation path during Git-hosted plugin installation, which is not lifecycle-safe; `bundle` avoids it.

## API Exports

```ts
import plugin, { parseOptions, AdvisorRuntime } from "opencode-advisors-v2"
```

The root `index.ts` re-exports all three from `src/index.ts`.

- `default` — the plugin object `{ id: "opencode.advisors", setup }`; this is what the loader registers
- `parseOptions(raw)` — strict validation; throws on unknown keys, out-of-range values, malformed model refs
- `AdvisorRuntime` — runtime class for lifecycle, event consumption, and status (embedding/advanced use)

### Deferred

- `followPrimary: true` is accepted in config but advisors using it are skipped until model-specific session reuse is proven.
- `WATCHDOG.yml` roster discovery (`src/roster.ts`) is implemented but not wired into the runtime (Phase 2).

### Advisor tool capabilities

Every advisor gets the read-only investigation tools `read`, `glob`, and
`grep` as agent capabilities. `bash`, `edit`, `write`, and all mutating tools
stay denied. Passive reviews do not invoke tools; a tool-capable review loop
remains deferred.

Network tools are opt-in per advisor:

```jsonc
{ "name": "Researcher", "network": true }
```

`network` defaults to `false`. The advisor reviews untrusted transcript
content; with network egress, injected instructions in that content can
steer it to exfiltrate file secrets via fetch URLs or search queries
(bounded tool input/result values are now included — full reviewer
visibility — with best-effort credential-value redaction applied to the
whole transcript before dispatch). Opt in only if you
accept that risk. Networked advisors get a policy addendum restricting
what they may place into queries and URLs.

The passive review path is tool-free. It uses `ctx.session.generate()` with an
explicit no-tools instruction because advisor agents may still advertise read
tools. Read-only permissions remain registered for advisor agents, but passive
reviews do not invoke them.

## Privacy

A cross-provider advisor means your transcript data reaches another provider. Reviewer transcripts include bounded (2000-char) tool input and output values for every step — full session visibility by design (USER DIRECTIVE 2026-09-24: "reviewer sees everything"; this reverses the fail-closed exclusion shipped in `10b0abb`). `redactSecrets` still masks recognized credential VALUES before dispatch (API keys, tokens, env-var assignments, URL userinfo, and Basic credentials in curl `-u`/`--user` argv and `Authorization: Basic` headers), binary content is still skipped, advisory self-exclusion (loop prevention) is unchanged, and the plugin does not log full prompts by default. Redaction is pattern-based and best-effort: unrecognized credential shapes are NOT masked, and Basic header values below 8 characters are not redacted.

## Known Limitation

Advisor sessions are created as root sessions because the exposed V2 plugin `create` omits `parentID` and `title`. Deterministic session IDs prevent unbounded duplication. Upstream child-session support is the intended fix.

## License

MIT — see [LICENSE](LICENSE).