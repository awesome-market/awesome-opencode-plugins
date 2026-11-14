# Strategy MCP

[![npm version](https://img.shields.io/npm/v/strategy-mcp.svg)](https://www.npmjs.com/package/strategy-mcp)
[![npm downloads](https://img.shields.io/npm/dm/strategy-mcp.svg)](https://www.npmjs.com/package/strategy-mcp)
[![license](https://img.shields.io/npm/l/strategy-mcp.svg)](https://github.com/Ritterbeckaj/strategy-mcp/blob/main/LICENSE)
[![node](https://img.shields.io/node/v/strategy-mcp.svg)](https://www.npmjs.com/package/strategy-mcp)

```bash
npx -y strategy-mcp
```

Deterministic strategic-planning frameworks as a local MCP server. Runs anywhere
Node 18+ runs, makes **zero network calls**, and needs **no API keys**.

Four tools are free and MIT-licensed in this repo. Eight more (twelve total) ship
as [StrategyBrain Pro](#strategybrain-pro).

```
swot_analysis   marketing_mix   lean_canvas   decision_matrix     ← free (this repo)
```

## Free tools (MIT)

| Tool | What it actually returns |
|---|---|
| `swot_analysis` | S/W/O/T, then **S-O / W-O / S-T / W-T cross-mapping** and 3–5 offensive + defensive actions. Not just the four quadrants. |
| `marketing_mix` | The 4Ps — product, price, place, promotion — plus the one-line pitch that connects them. |
| `lean_canvas` | One-page business model: problem → segments → UVP → solution → channels → revenue → costs → metrics → unfair advantage. |
| `decision_matrix` | Options scored against weighted criteria, ranked, with the margin between winner and runner-up. |

Every tool is a pure function of its input. Same input, same output, no model
call, no drift between runs, nothing sent anywhere.

## Install

**Requirements:** Node 18 or newer. Nothing to clone, no absolute paths.

The server is on npm, so `npx` fetches and runs it:

```bash
npx -y strategy-mcp
```

That speaks MCP over stdio and waits for a client. Or install it once, globally:

```bash
npm install -g strategy-mcp
strategy-mcp
```

Prefer the source? Same four tools:

```bash
git clone https://github.com/Ritterbeckaj/strategy-mcp.git
cd strategy-mcp && npm install
```

### OpenCode

`~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "servers": {
      "strategy": {
        "type": "local",
        "command": ["npx", "-y", "strategy-mcp@latest"]
      }
    }
  }
}
```

Installed globally instead? `"command": ["strategy-mcp"]`.

### Claude Code

```bash
claude mcp add strategy -- npx -y strategy-mcp@latest
```

### Claude Desktop / Cursor

Claude Desktop — `claude_desktop_config.json`
(macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`).
Cursor — `~/.cursor/mcp.json`. Same shape:

```json
{
  "mcpServers": {
    "strategy": {
      "command": "npx",
      "args": ["-y", "strategy-mcp@latest"]
    }
  }
}
```

Building from a local clone instead? Point `command` at `node` and `args` at the
absolute path of `index.js`.

Restart the client. The four tools appear as `swot_analysis`, `marketing_mix`,
`lean_canvas`, `decision_matrix`.

Then just ask:

> "Run a SWOT on my print-on-demand merch line and tell me which threat actually kills it."

## Or use the hosted servers (no install)

The same tools — plus FactCheck and LeadGen — run as remote MCP endpoints over
Streamable HTTP. Useful when you can't install anything locally:

| Server | Endpoint | Tools |
|---|---|---|
| StrategyBrain | `https://strategybrain-mcp.factcheck-mcp-worker.workers.dev/mcp` | 12 |
| FactCheck | `https://factcheck-mcp.factcheck-mcp-worker.workers.dev/mcp` | 7 (6 + `get_usage`) |
| LeadGen | `https://leadgen-mcp.factcheck-mcp-worker.workers.dev/mcp` | 6 |

Header on every request:

```
x-api-key: oc_trial_5a4900841684ff7d265ba3028bcb1fcc
```

That's a **shared public demo key: 100 calls/day across all users**. Fine for
testing whether it works in your client. If you need a real quota, buy a pack
and you get your own key.

## What touches the network

READMEs in this category tend to say "fully offline" and stop there. Enumerated
instead:

| Pack | Tools | Network |
|---|---|---|
| StrategyBrain (free 4 here + Pro's 8) | 12 | **none** |
| Monetize MCP | 8 | **none** |
| FactCheck MCP | 6 | 4 tools → Wikipedia, Semantic Scholar, optional Google Fact Check. `cross_verify` and `anti_hallucination_protocol` are local. |
| LeadGen MCP | 6 | 2 tools → DuckDuckGo, plus the page you point it at. `qualify_lead`, `save_lead`, `list_leads`, `draft_outreach` are local. |

**26 of the 32 tools on sale make zero network calls.** Six do, and they call
free, keyless, read-only public endpoints — no account, no billing, nothing
written. `GOOGLE_FACTCHECK_API_KEY` is optional; without it the server degrades
to Wikipedia + Semantic Scholar. When a network call fails, the tool returns
`UNVERIFIED` rather than inventing a result.

## The other packs

One page with everything: **<https://ritterbeckaj.github.io/mcp-packs/>**

Same design as what you just installed — no model calls, no keys, deterministic
output. Each is a drop-in MCP server.

| Pack | Tools | Price |
|---|---|---|
| [**StrategyBrain Pro**](https://ritterbeck.gumroad.com/l/strategybrain-pro) — Porter's Five Forces, PESTLE, Ansoff, Jobs-to-be-Done, TAM/SAM/SOM, OKRs, roadmap, brainstorm | 8 | $12 |
| [**FactCheck MCP**](https://ritterbeck.gumroad.com/l/factcheck-mcp) — claim verification, source fetching, citation checks, anti-hallucination protocol | 6 | $12 |
| [**LeadGen MCP**](https://ritterbeck.gumroad.com/l/leadgen-mcp) — find leads, extract from a page, qualify, save, draft outreach | 6 | $12 |
| [**Monetize MCP**](https://ritterbeck.gumroad.com/l/monetize-mcp) — pricing, packaging, offer ladders | 8 | $0+ |

Each pack is $29 with a 30-minute setup call, and there's a 30-day refund if it
isn't useful. Start with **[Monetize MCP at $0+](https://ritterbeck.gumroad.com/l/monetize-mcp)**
if you want to test the install before paying for anything.

All four packs together — 32 tools:
**[The MCP Toolkit](https://ritterbeck.gumroad.com/mcp-bundle)** ($29, or $79 with setup).

## Why open-core

The four tools here are the ones that survive being used on their own. The Pro
pack funds maintenance and the next batch. If the free tools earn it, buy Pro.
If they don't, you've lost nothing but a `npm install`.

## Publishing your own

MIT — fork it, rename it in `package.json` and in the `McpServer` constructor,
`npm publish`. If you fork, pick your own package name: `strategy-mcp` is taken
(as of v0.2.0, by this project).

## License

MIT — see [LICENSE](LICENSE). The Pro tools are proprietary and are not in this
repository.
