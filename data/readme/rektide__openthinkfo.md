# openthinkfo

OpenCode V2 Effect plugin for model provenance: it records model-selection
changes in the session before the user prompt associated with each change, and
retitles forks that diverge onto a different model.

```text
[model: openai/gpt-5.6-sol#high]

Write the initial implementation.

[model-switched from="openai/gpt-5.6-sol#high" to="zai/glm-5.3#max"]

Review the implementation Sol wrote.
```

The records are synthetic messages. OpenCode persists them, displays them as
session notices, and includes them as user-role messages in later model
context. The system prompt is never modified.

## Model records

The plugin runs in `session.hook("prompt")`:

1. Read the session's selected model and compare it with the model stored for
   that session in plugin storage.
2. If it changed, admit a synthetic record with the prompt's delivery mode and
   `resume: false`.
3. Return from the hook. OpenCode then admits the original prompt behind the
   synthetic and wakes execution normally.

For steering input, OpenCode promotes both messages in admission order, so the
model sees the change record immediately before the user's instruction. For
queued input, OpenCode promotes one queued item at a time, so the model record
gets its own step before the user's queued prompt.

`resume: false` delays execution; it does not suppress it. The original prompt
performs the wake only after both inputs have their durable inbox order.

Hook runs are serialized per session (each prompt awaits the previous run's
fiber), so overlapping prompts admit their records in order. A failed record
admission dies to the host without updating storage — the next prompt retries.

## Session context readout

The plugin also registers `tools.openthinkfo.session_context` and appends the same
readout to existing model-change records. It distinguishes lagging provider-reported
context from session-lifetime totals, uses the reporting model's context limit, and
returns unknown when compaction/revert scope cannot support a measurement. It does
not compact sessions or add threshold alerts.

See the [maintained context guide](/doc/session-context/README.md) for invocation,
scope, loading, and verification limits.

## Fork retitles

Absorbed from openforkmark (now retired). On the firehose, `session.forked`
snapshots the parent's at-fork model into plugin storage; on
`session.model.selected` the fork's new model is compared against that
snapshot. When they differ the title gains the model; when they match again it
is removed:

```text
Debug the parser (fork #1)              ->  Debug the parser (fork #1, glm-5.3#max)
Debug the parser (fork #1, glm-5.3#max) ->  Debug the parser (fork #1)
```

The model is the short `id#variant` form (`glm-5.3#max`). Titles without a
fork marker (custom-retitled, or untitled-at-fork and later auto-titled) gain
a bare marker instead: `my title (fork, glm-5.3#max)`.

If storage misses (server restarted between fork and switch, or the fork
predates this plugin), the handler recovers the baseline from the durable
`Session.Info.fork` field and the parent's current model. The firehose filter
drops every other event after one string comparison; `switchModel` dedupes
no-op switches, so both observed events are rare.

## Data retained

- **Plugin storage** (server-persisted, plugin-scoped):
  - `session-model/<sessionID>` → the most recently recorded
    `{ providerID, id, variant? }` for that session.
  - `fork/<sessionID>` → `{ parentModel? }`, the parent's at-fork model —
    the baseline fork divergence is measured against.
  Neither is ever pruned; `ctx.storage` exposes `remove`/`scan`, so cleanup
  on `session.deleted` is possible future work.
- **Transcript records**: the synthetic messages above with metadata
  `{ source: "openthinkfo", model, context }`, including the context measurement or
  its unknown/unavailable status. They are ordinary session messages and
  inherit the session's retention.
- **Reads, not retained**: session info (title, model, `fork` lineage) is
  fetched per event and never stored beyond the snapshots above.

## Install

Reference the plugin directory from `opencode.jsonc` (server config):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["file:///home/me/src/openthinkfo/src/plugin"]
}
```

Dependencies (`@opencode/plugin`, `@opencode/schema`, `effect`) resolve
from the plugin's own `node_modules`; install with `pnpm install`.

## Development

```sh
pnpm test
pnpm check
pnpm fix
```

## Scope

- Model changes are observed when a user prompt is admitted. If a session has
  no selected model in `Session.Info`, the plugin leaves the prompt unchanged.
- Untitled forks are never retitled (there is no title to extend); upstream's
  own title generator may title them later without a fork marker.
- Upstream's fork numbering comes from the title chain
  (`X (fork #1)` → `X (fork #1) (fork #1)` on fork-of-fork). A model-annotated
  marker breaks upstream's increment match, so a fork of a marked fork starts
  a fresh `(fork #1)`; this plugin then annotates the innermost marker.
- Model comparison includes provider, id, and variant; a variant-only change
  (e.g. `glm-5.3#max` → `glm-5.3#high`) counts as a divergence.
- Subagent (agent-mode child) sessions are a non-issue, not a watched case:
  they never emit `session.forked`, their spawn model rides
  `session.created`, and the only upstream path that switches a child's model
  is continuing it with a different configured agent — rare, and dropped by
  the `info.fork` guard that covers plain sessions before any storage read.
