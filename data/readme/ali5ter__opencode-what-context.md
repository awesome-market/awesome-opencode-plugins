# opencode-what-context

A plugin for [OpenCode](https://opencode.ai) that shows what was sent to the model, request by
request.

## What it does

Every time OpenCode calls a model, the plugin records what went out. Agent-loop calls carry the
assembled context — system instructions by source, tool schemas, and conversation; every call
also carries the wire body size and the provider's reported usage. In the TUI the records render
as a [dsh-context](https://github.com/bowenliang123/dsh-context)-style panel: a context-window
gauge, a request history, a per-request composition bar, and a token trend.

## Install

```sh
opencode plugin add github:ali5ter/opencode-what-context
```

The package is installed from the Git repository on first start, so restart OpenCode afterwards.

## Usage

Open the panel in the TUI with the `/context` command or the `<leader>v` keybinding. Use `j`/`k`
to move through the request history, `f` to toggle fullscreen, and `q` to close.

## Why

OpenCode persists per-message token and cost totals in its SQLite session database, but not the
served request body. A community `/context` plugin —
[`opencode-context-usage`](https://github.com/angeloper86/opencode-context-usage) by angeloper86 —
answers *how many*: token totals by category, cache hit rate, cost, including delegated subagents.
Nothing answers *what*: the served request body is not persisted, so the composition of the
context (system instructions, tool schemas, conversation) stays invisible. This plugin closes
that gap through the [plugin API](https://opencode.ai/docs/plugins/) session hooks.

## License

MIT — see [LICENSE](LICENSE).
