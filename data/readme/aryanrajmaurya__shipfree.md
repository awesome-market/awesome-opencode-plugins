<p align="center">
  <b>shipfree</b><br>
  <i>Deploy an AI service for $0 — with limits that are verified, not remembered.</i>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <a href="https://github.com/AryanRajMaurya/shipfree"><img src="https://img.shields.io/badge/limits-82%20checked%20against%20upstream-success.svg" alt="Limits verified"></a>
  <a href="https://github.com/AryanRajMaurya/shipfree"><img src="https://img.shields.io/badge/skill-Agent%20Skills-informational.svg" alt="Agent Skill"></a>
</p>

---

## The problem

Everyone wants to put an AI service online. Almost nobody wants to pay for
it. So they read a blog post, copy a scaffold, deploy it, and two weeks later
it starts returning `Error 1027` or silently stops writing.

**A free tier is not a smaller paid tier. It is a different shape.** The
numbers that decide whether your deployment stays free are scattered across
half a dozen pricing pages, they are phrased in ways that mislead, and they
change without warning.

Three that matter more than you would expect:

| | Free tier | The trap |
| --- | --- | --- |
| **Cloudflare Workers CPU** | **10 ms** per invocation | Wall clock is not CPU time. Waiting on a socket is free; parsing a 2 MB JSON body is not. |
| **Cloudflare Durable Objects CPU** | **30 seconds** per request | 3,000x more. Everything stateful or realtime goes here, not in a Worker. |
| **Cloudflare Queues consumer CPU** | **5 minutes** | Anything heavy belongs in a queue, not in the request path. |

## What this is

An **Agent Skill** that teaches any AI coding agent how to deploy an AI
service on a free tier — and does it with the real numbers.

It ships one repository with the skill installed for **every major AI
harness**, so the same guidance works in Claude Code, Codex, Cursor,
Copilot, opencode, Kimi, Grok, Devin, Cline, Kiro, OpenClaw and Pi.

## What makes it different

**The limits in this skill are checked by CI against the upstream
documentation.** Not summarised from a blog post. Not written from memory.

`limits.json` is the single source of truth. A harness fetches the platform's
own documentation source, extracts the limit tables, and compares every
asserted value. If a limit changes upstream, the build fails and prints the
upstream text next to the value that is now wrong.

```
$ python harness/check_limits.py
  ok  workers           requests_per_day
  ok  workers           cpu_time_per_invocation
  ok  durable_objects  cpu_per_request
  ok  d1                queries_per_worker_invocation
  ...
82 checks, 0 need attention
```

That is the whole point. A stale limit is worse than no limit, because it
produces a broken deployment that looks correct.

The skill's tables are *generated* from `limits.json`, so the prose and the
verified data cannot drift apart.

## Install

<details open>
<summary><b>Claude Code</b></summary>

```bash
/plugin marketplace add AryanRajMaurya/shipfree
/plugin install shipfree@shipfree
```
</details>

<details>
<summary><b>Codex</b></summary>

Add the plugin from this repository's `.codex-plugin/plugin.json`, or copy
`.agents/skills/shipfree/` into your Codex skills directory.
</details>

<details>
<summary><b>opencode</b></summary>

```bash
git clone https://github.com/AryanRajMaurya/shipfree ~/.config/opencode/shipfree
```

The skill is discovered from `.opencode/skills/shipfree/`, and
`/shipfree` runs it as a command.
</details>

<details>
<summary><b>Cursor</b></summary>

Copy `.cursor/rules/shipfree.mdc` into `.cursor/rules/` in your project, or
`.cursor-plugin/` for the plugin manifest.
</details>

<details>
<summary><b>GitHub Copilot</b></summary>

Copy `.github/copilot-instructions.md` into `.github/` in your repository.
</details>

<details>
<summary><b>Any other harness</b></summary>

The canonical skill is `.agents/skills/shipfree/SKILL.md`. It follows the
open Agent Skills format: YAML frontmatter with `name`, `description` and
`license`, then Markdown. Copy it wherever your harness looks for skills.
</details>

## What you get

- **A decision matrix** for choosing a free platform, and an explanation of
  why Cloudflare Workers wins for almost every AI workload.
- **The limits that actually bite**, with the architecture that fits inside
  them — the 10 ms CPU rule and how to stream around it, Durable Objects
  for state and WebSockets, D1's 50-query budget, KV's write ceiling, R2's
  free egress, Queues' 5-minute consumer budget.
- **A ten-step workflow** from "here is my idea" to a deployed, authenticated,
  rate-limited, monitored service that is still free.
- **Ten traps** that account for most free-tier failures, including
  buffering a streaming response and putting an API key in the frontend.
- **Working templates** — a streaming proxy and a full agent API.

## Templates

```bash
git clone https://github.com/AryanRajMaurya/shipfree
cd shipfree/templates/streaming-proxy
npm install
npx wrangler secret put GEMINI_API_KEY
npx wrangler deploy
```

- **`templates/streaming-proxy/`** — a Worker that streams a model response
  and enforces a shared token.
- **`templates/agent-api/`** — Worker + D1 + a Durable Object session +
  a queue consumer. The full stack for a realtime agent.

## Using it

Ask your agent to deploy something and it will reach for the skill:

> Deploy a chat API that streams from Gemini, stores conversations in D1,
> and stays on the free tier.

Or run it directly:

```
/shipfree deploy a RAG endpoint over PDFs on R2, free tier
```

## Keeping it honest

The limits are verified on every push and on a scheduled weekly run. When
upstream changes, the workflow opens an issue with the drift so it gets
fixed rather than rotting.

If you find a stale number, do not edit the table by hand:

```bash
python harness/fetch_limits.py --refresh   # pull upstream
python harness/check_limits.py              # report drift
python harness/render_skill.py              # regenerate the tables
```

Open a pull request. The checker will confirm your new value against
upstream before it merges.

## Contributing

Contributions are very welcome, and the easiest useful contribution is the
one that matters most: **a limit that changed upstream.** If you notice a
drift the CI has not caught, open an issue with the upstream text.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
