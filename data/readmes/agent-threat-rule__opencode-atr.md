# opencode-atr

An [OpenCode](https://opencode.ai) plugin that checks tool calls before they run and tool output before the model reads it against [Agent Threat Rules](https://github.com/Agent-Threat-Rule/agent-threat-rules) (ATR), MIT-licensed detection rules for attacks on AI agents: prompt injection in fetched pages and files, commands that open a shell to another host, attempts to read or send credentials. Matching runs locally in the ATR engine, which loads once per OpenCode process: no network calls and no API key.

## Install

Add it to your OpenCode config (`opencode.json`):

```json
{
  "plugin": ["opencode-atr"]
}
```

OpenCode installs npm plugins with Bun at startup.

## What it does

| Hook | What is checked | When a rule in the blocking lane matches at high or critical severity |
|---|---|---|
| `tool.execute.before` | tool name and arguments | the call throws and does not run; the error names the rules |
| `tool.execute.after` | the tool output | the output is replaced with a notice naming the rules, so the model never reads it |

Every match, blocking or not, is written to OpenCode's log. The plugin runs the ATR engine without a model judge or a reporter, so it makes no network requests of its own.

## Lanes and blocking

ATR rules carry a maturity, and a lane selects which ones run: `enforce` (stable rules), `alert` (stable and test) and `hunt` (all rules except draft and deprecated ones).

- `lane` (default `alert`) chooses the rules that are evaluated.
- `blockLane` (default `enforce`) chooses the rules that can block. `none` records only. It cannot be wider than `lane`.

The default blocks only on stable rules, and that lane is narrow. In our tests it withheld a fetched page telling the model to send `~/.ssh/id_rsa` to a webhook, but let a reverse-shell command run. `blockLane: "alert"` blocked both. The alert lane also blocks ordinary content: of 1,500 benign texts sampled from ATR's benign corpus and checked as tool output with ATR 4.3.0, it blocked 102 (6.8%); the enforce lane blocked none. `node scripts/measure-benign.mjs <agent-threat-rules checkout>` reproduces this. Start with `"blockLane": "none"`, look at what your sessions produce, then choose.

Settings live in `~/.config/opencode/atr.json`:

```json
{ "lane": "alert", "blockLane": "none" }
```

A project can add `.opencode/atr.json`, but it can only make checking stricter than your own settings, never weaker, so a repository you open cannot turn blocking off. If the project's `blockLane` is wider than your `lane`, `lane` is widened to match, and an unreadable project file is ignored.

## License

MIT
