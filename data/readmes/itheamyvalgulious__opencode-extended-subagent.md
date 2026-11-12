# opencode-extended-subagent

[![License: GPL-3.0](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](./LICENSE)
[![OpenCode v2](https://img.shields.io/badge/OpenCode-v2-black)](https://opencode.ai)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178c6)](https://www.typescriptlang.org)

Subagent orchestration for **OpenCode v2**. The native subagent tool runs child sessions; this plugin adds the
orchestration layer around them: an explicit spawn contract, batched fan-out, feedback groups that wake the parent
exactly once, agent-to-agent messaging behind a consent gate, persistent timers, restart recovery, and a live sidebar
with recursive cost.

English | [简体中文](./README.zh-CN.md)

## Highlights

- **Explicit `spawn`** — `name`, `model`, `variant`, `group` (and optionally `agent`) are required and recorded, so the
  mesh always knows who a subagent is, what it runs on and which batch it belongs to.
- **`swarm` fan-out** — one prompt template + N items; each item replaces `{{fill}}` and becomes `name-1..N` in the same
  feedback group.
- **Feedback groups** — when every member of a group reaches a terminal state (`idle` / `error` / `interrupted` /
  `stopped`), the parent is woken once with the full status list. A later `agent_send` / `broadcast` re-arms the group.
- **Agent mesh** — list, read, message, interrupt and stop any agent; subagents can proactively report to their parent.
- **Consent-gated peer messaging** — subagent↔subagent messages are refused until the main agent enables them, and the
  main agent may only do that with the user's explicit consent.
- **Persistent timers** — `set_timer` wakes the owning session once after N seconds; timers survive server restarts.
- **Live sidebar** — status glyph, name, model, group, per-agent cost and recursive cost; click a row to open the
  subagent's session, click `✕` to force-stop it.
- **Restart recovery** — the mesh registry and timers are persisted, then reconciled once after a restart.
- **No build step** — the plugin host loads the TypeScript sources directly; the only runtime peers are the OpenTUI /
  Solid packages already provided by OpenCode.

## Requirements

- OpenCode v2 with plugin + TUI sidebar support. Built against `@opencode/plugin` 2.0.18 and tested with OpenCode 2.2.3;
  preview APIs can change between OpenCode releases.
- A subagent-capable OpenCode agent (the default is `general`; override per spawn with `agent`).

## Installation

### From GitHub (recommended)

```bash
opencode plugin add github:itheamyvalgulious/opencode-extended-subagent
opencode reload
```

### From a local clone

```bash
git clone https://github.com/itheamyvalgulious/opencode-extended-subagent.git \
  ~/.config/opencode/plugins/opencode-extended-subagent
```

```jsonc
// ~/.config/opencode/opencode.json
{
  "plugins": ["/home/you/.config/opencode/plugins/opencode-extended-subagent"]
}
```

The TUI sidebar is loaded automatically through the package's `./tui` export — there is no separate install step.

## Quick start

Ask the main agent for a batch, for example:

> Refactor the auth, API and database modules in parallel. Use a high-reasoning model for each and tell me once all
> three are done.

The agent then uses the plugin tools:

```text
spawn(prompt: "Refactor src/auth ...", name: "auth-refactor",
      model: "anthropic/claude-sonnet-4-5", variant: "high", group: "refactors")

spawn(prompt: "Refactor src/api ...",  name: "api-refactor",
      model: "anthropic/claude-sonnet-4-5", variant: "high", group: "refactors")

spawn(prompt: "Refactor src/db ...",   name: "db-refactor",
      model: "anthropic/claude-sonnet-4-5", variant: "high", group: "refactors")
```

All three share the group `refactors`. The parent sleeps until the whole group is finished, then receives one
notification. Use `agent_read("auth-refactor", tail: 10)` to inspect what a member did.

Fan-out with a template:

```text
swarm(prompt: "Audit {{fill}} for injection and authorization bugs. Report findings only; do not edit files.",
      items: ["src/auth.ts", "src/api/", "src/db.ts"],
      name: "audit",
      model: "anthropic/claude-sonnet-4-5",
      variant: "medium",
      group: "security-audit")
```

This creates `audit-1`, `audit-2`, `audit-3` in the same group.

## Tools

| Tool | Arguments | Description |
| --- | --- | --- |
| `spawn` | `prompt`, `name`, `model`, `variant`, `group`, `agent?` | Create one subagent. `name` must be unique in the mesh; `model` is `provider/model-id`; `variant` must be supported by that model; `agent` defaults to `general`. |
| `swarm` | `prompt`, `items`, `name`, `model`, `variant`, `group`, `agent?` | Create `items.length` subagents. Every `{{fill}}` in `prompt` is replaced by an item; members are named `name-1..N`. |
| `broadcast` | `group`, `text` | Send one message to every member of a group. Re-arms the group's completion notification. |
| `agent_list` | — | List every agent in the mesh (root + subagents) with live status, plus active timers and peer-messaging state. Use it for discovery, **not** for polling. |
| `agent_read` | `target`, `tail?`, `limit?` | Read an agent's recent conversation. `target` is a subagent name/id, or `parent` / `main` / `self` from inside a subagent. |
| `agent_send` | `target`, `text` | Message any agent. Main → subagent: queued while busy, starts it when idle. Subagent → `parent`: proactive report. Subagent → peer: gated by `allow_peer_messaging`. |
| `agent_interrupt` | `target` | Interrupt the current turn; the subagent stays alive with its full context. |
| `agent_stop` | `target` | Force-stop a subagent (terminal state; the session is kept). |
| `allow_peer_messaging` | `enabled`, `group?` | Main-agent-only gate for subagent↔subagent messaging. Omit `group` to affect all groups. Only call with explicit user consent. |
| `mesh_models` | — | List available models with their supported variants, plus subagent-capable agents. No API calls, no token usage. |
| `set_timer` | `time`, `message` | Wake the calling session once after `time` seconds. Persisted and rebuilt after a server restart. |

The plugin also injects orchestration rules into the system prompt of every main session and mesh rules into every
subagent session, so agents know the group semantics, the no-polling rule and the consent gate without extra setup.

## Sidebar

The `sidebar.content` slot shows:

- one row per subagent: status glyph, name, model, group, recursive cost;
- a header with the agent count, total cost and peer-messaging state;
- **click a row** to open that subagent's session;
- **click `✕`** on a row to force-stop that subagent.

Status glyphs: `○` starting, `●` running, `↻` retrying, `✓` idle/done, `⚠` error, `✕` interrupted, `■` stopped.

## How it works

| File | Role |
| --- | --- |
| `index.ts` | Server plugin: tools, RPC handlers, system-prompt hook, mesh registry, timers, restart reconciliation. |
| `tui.ts` | TUI plugin: sidebar view and RPC client. |
| `rpc.ts` | Shared RPC contract (`extended-subagent`). |

- **Sessions**: `spawn` creates a real child session with `parentID`, the requested agent/model/variant, and then sends
  the initial prompt. Subagent sessions therefore stay out of the root session picker in the TUI and web UI.
- **Registry**: the mesh is persisted under the `mesh.registry.v1` storage key. `spawn` persists before broadcasting an
  `updated` event, so the sidebar never shows a half-created agent.
- **Multiple plugin instances**: the host loads one plugin instance per location, and each holds its own in-memory mesh.
  RPC `list`/`stop` read the shared storage registry and merge live state from the serving instance, so the sidebar can
  route to any instance.
- **Cost**: per-agent cost comes from the session record; recursive cost adds all descendants. The sidebar total sums the
  visible tree.

## Consent gate for peer messaging

Two independent locks:

1. **Prompt layer** — the injected rules tell agents that peer messaging needs the main agent's permission, and that the
   main agent may only enable it after the user explicitly agrees.
2. **Technical layer** — a subagent sending to a peer is rejected unless `allow_peer_messaging(true, group?)` was called
   on the same mesh root. Subagent → parent reports are never blocked.

## Restart recovery

- **Timers** are stored with their fire time. After a restart they are rebuilt with the remaining delay, in chunks for
  very long delays; a timer that expired while the server was down fires once at startup. The id sequence continues from
  the highest persisted id.
- **Agents** are persisted together with their group state and initial prompt. After startup the plugin reconciles once:
  - terminal agents (`idle` / `error` / `interrupted` / `stopped`) are left untouched — a user interrupt is not undone;
  - agents whose session was deleted are removed from the mesh;
  - agents that never received their first prompt get the initial prompt again;
  - agents that were busy are compared on token/cost progress. Progress means the work actually finished → `idle`; zero
    progress means the restart killed it → the original instruction is re-sent and the agent stays `busy`.
- Reconciliation runs once. Normal events keep flowing during recovery; the first terminal event wins, so no duplicate
  completion notification is sent.

## Notes and limitations

- Native `task`/`subagent` tools are not part of the mesh: they have no name/model/variant/group, no sidebar entry and no
  group wake-up. Use `spawn`/`swarm` when you want orchestration.
- Because mesh sessions carry `parentID`, the TUI and web root session pickers hide them; open them from the sidebar.
  The raw `GET /api/session` endpoint still returns every session, including children. Sessions created before 1.1.0 have
  no `parentID` and may still appear in the root list.
- `model` must match an available model and `variant` must be one the model supports; call `mesh_models()` first.
- Group completion requires a terminal state. An agent waiting forever keeps the group (and the parent) waiting.
- The plugin does not sandbox subagents: each one runs with the permissions of its OpenCode agent.
- A subagent can only message agents in its own mesh; cross-mesh messaging is rejected.
- The sidebar needs the TUI. The server-side tools still work without it, but there is no UI then.

## Development

```bash
npm install
npm run typecheck   # tsc --noEmit
```

There is no build step — the plugin host consumes `index.ts`, `tui.ts` and `rpc.ts` directly. To develop against a local
checkout, point the plugin config at this directory and run `opencode reload`.

## License

GPL-3.0-only. See [LICENSE](./LICENSE).
