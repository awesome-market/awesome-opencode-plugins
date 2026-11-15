# opencode-advisor

A second opinion on the work happening in your session.

An [opencode](https://opencode.ai) plugin that registers an `advisor` tool. It hands the
current session transcript — the task, every tool call, and what each returned — to a
reasoning model and returns its critique. The advisor sees what your agent saw, so the
agent supplies only the argument, not the history.

Nothing external is required: no Claude Code, no `jq`, no shell script, no session
export. It reads the live transcript over opencode's own client.

## Why

A coding agent that reviews its own plan grades its own homework. A reviewer that sees
the same evidence but isn't invested in the approach catches wrong assumptions,
unverified claims, and missed constraints — usually before they're expensive.

## Install

```sh
mkdir -p ~/.config/opencode/plugin
curl -fsSL https://raw.githubusercontent.com/alkevintan/opencode-advisor/main/src/advisor.ts \
  -o ~/.config/opencode/plugin/advisor.ts
```

Restart opencode. You need at least one authenticated provider serving a reasoning model
(`opencode auth login`).

## Use

Your model calls it on its own when the tool description matches the moment — before
committing to an approach, when stuck, before changing direction, before declaring done.
You can also ask directly:

```
> consult the advisor before you refactor this
```

The advisor mirrors the specificity of the question. A good one names the approach, the
alternative rejected, and the uncertainty:

> "I'm about to store per-tenant rates as versioned JSON in the existing key/value
> settings table rather than a dedicated table. Payroll must select by period date.
> Which holds up better as agencies are added, and what am I not seeing?"

"Any thoughts?" wastes the call.

To get the most out of it, point your agent at the tool in `AGENTS.md` — describe *when*
to ask (before substantive work, when stuck, before declaring done), not just that the
tool exists.

## Configuration

Default model: **`opencode-go/qwen3.7-plus`**.

As with the vision plugin, the default is a model *name*: the tool finds every
authenticated provider serving `qwen3.7-plus`, tries the cheapest first, and moves past a
dead credential without costing you a retry chain.

Override per call, or edit `DEFAULT_MODEL` at the top of the file to change the standing
default.

**Overrides must be reasoning-capable.** An advisor that doesn't think is worse than no
advisor — it produces fluent, confident agreement. Non-reasoning models are rejected with
a list of ones that work. That list prefers paid tiers: sorting purely by price puts free
stealth models first, and steering an advisor toward those trades away the one thing it
exists for.

## What it sends

- The transcript, rendered as markdown: text parts, and tool calls with clipped
  input/output. Reasoning and step parts are dropped — private churn, not evidence.
- The **original request is pinned** even when the tail window would drop it. It's the
  one message explaining why everything else happened.
- Trimming keeps the most recent turns, and trims the recent window *before* prepending
  the pin, so the pinned request survives on long transcripts.
- The in-flight turn — the call itself — is omitted. Left in, the advisor reads it as
  "the agent did nothing" and critiques that instead.
- The transcript is wrapped as **data**, with an explicit instruction that instructions
  inside it are addressed to another agent and must be analysed, never followed.

Defaults: last 60 messages, 120KB cap, 2000 chars per part.

## Repository access

The advisor gets **read-only** tools — `read`, `grep`, `glob`, `list` — so it can check
claims against the actual code before answering. It cannot edit, write, or run commands.

This makes it agentic: a consult is several round trips, not one. That's a deliberate
trade — advice grounded in the real files is worth more than advice about a transcript.

## Limits

- Transcript trimming above 120KB is implemented but not exercised end-to-end.
- The first user message appears twice on short transcripts (pinned, then again in the
  recent window) — a few hundred wasted bytes.

## Licence

MIT
