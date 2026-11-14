# opencode-context-usage

A tiny `/context` command for [OpenCode](https://opencode.ai) that shows what is filling your session's context window: system prompt, built-in tools, each MCP server, skills, AGENTS.md / instructions and messages, with token estimates.

- One file, ~7.5 KB
- No dependencies, no network calls, no file reads, nothing written to disk (in-memory only)
- Requires **OpenCode 2.2.5+** (uses the v2 plugin API: `context` session hook, `command.transform`, `session.synthetic`)

## Screenshot

![/context in the OpenCode TUI](docs/screenshot.png)

## Sample output

From a test session (mock model, one demo MCP server with 5 tools, one project skill):

```
Context usage (estimate) · agent build, model mock/mock

  System prompt .................................   538
    base / agent prompt .........................   444
    environment .................................    86
    date ........................................     8

  Tools (built-in) ..............................  4.5k
    codemode: opencode ..........................  1.2k
    subagent ....................................   663
    edit ........................................   374
    shell .......................................   370
    question ....................................   348
    execute .....................................   289
    grep ........................................   267
    read ........................................   235
    …6 more .....................................   758

  MCP ...........................................   163
    demo (5 tools) ..............................   163

  AGENTS.md / instructions ......................    24
    ~/my-app/AGENTS.md .........................    24

  Skills ........................................   352
    opencode ....................................   139
    (guidance) ..................................   111
    report ......................................    66
    demo-skill ..................................    36

  Messages ......................................     2
    user text ...................................     2

  MCP servers: demo=connected

  Fixed baseline 5.6k · Thread 2 · Total 5.6k  (chars/4 estimate, not billed tokens)
```

## Install

```sh
mkdir -p ~/.config/opencode/plugins
curl -fsSL https://raw.githubusercontent.com/crisesarmiento/opencode-context-usage/main/context-usage.js \
  -o ~/.config/opencode/plugins/context-usage.js
```

Or just copy `context-usage.js` into `~/.config/opencode/plugins/`. OpenCode auto-discovers global plugins there; if it doesn't pick it up, run `opencode service restart`.

Uninstall: delete the file.

## Usage

1. Send at least one message in the session (the plugin captures the request OpenCode sends to the model).
2. Run `/context`.

## How it works

The plugin listens to the `context` session hook, keeps the last request per session in memory (capped at 50 sessions), and on `/context` splits it into categories:

- **System prompt** parts, by their instruction keys (`core/environment`, `core/date`, ...)
- **Tools**: each tool definition; MCP tools are attributed to their server by name prefix
- **Code Mode catalog**: split per namespace; namespaces that match an MCP server count as MCP
- **AGENTS.md / instructions**: split per source file
- **Skills**: one entry per available skill, plus the skill guidance
- **Messages**: by role and part type

## Limitations (honest list)

- **Estimates, not billed tokens.** ~4 chars/token for ASCII, denser for non-ASCII. Real tokenizers differ per model.
- **Tiny token cost per run.** The TUI shows a synthetic note by its description, so the report goes there; the model only receives one short line ("[/context report shown to the user; no action needed]", ~15 tokens) on the next turn.
- **TUI checked in a headless terminal** (OpenCode 2.2.5 in tmux, see screenshot), not on every terminal/theme. Desktop/web clients were not tested.
- **Code Mode MCP detail.** In OpenCode 2.2.5, MCP tools can arrive as a "Code Mode tool catalog" update inside the messages instead of as direct tools. The plugin parses that and credits them to the MCP server, but this depends on OpenCode's current text format and may break on future versions.
- **In memory only.** After restarting OpenCode, send one message before `/context` has data.
- Tested with a mock provider and a demo MCP server, not with every real provider/MCP.

## Credits

Inspired by [jasonwaleryszak/opencode-context](https://github.com/jasonwaleryszak/opencode-context) (MIT): the idea of capturing the `context` session hook and splitting system parts by their instruction keys comes from there. This is an independent, much smaller rewrite.

## License

MIT, see [LICENSE](LICENSE).
