# opencode-exa-parallel

An [OpenCode 2](https://opencode.ai/v2/docs/) web search provider that searches with Exa and falls back to Parallel.

It registers one provider, `exa-parallel`, for OpenCode's built-in `websearch` tool. Each search goes to OpenCode's native `exa` provider first. Parallel is only called when Exa:

- throws an error (including HTTP 429 rate limits and authentication failures),
- takes longer than the timeout (20 seconds by default), or
- returns no usable results (no result with an `http(s)` URL and a title or content).

There are no extra tools, MCP servers, or dependencies. Both searches run through OpenCode's own `exa` and `parallel` providers, so they use whatever credentials you've already set up for those.

## Install

Pick one.

**Single file.** Copy `exa-parallel.js` into your global plugins directory. OpenCode loads every plugin there automatically:

```sh
mkdir -p ~/.config/opencode/plugins
curl -fsSL https://raw.githubusercontent.com/lemon07r/opencode-exa-parallel/main/exa-parallel.js \
  -o ~/.config/opencode/plugins/exa-parallel.js
```

**Plugin list.** Add the repository to `plugins` in `~/.config/opencode/opencode.json(c)`:

```jsonc
{
  "plugins": ["github:lemon07r/opencode-exa-parallel"],
}
```

Then select the provider in the same file:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "websearch": {
    "provider": "exa-parallel",
  },
}
```

The plugin never sets itself as the default, so a project's `websearch` setting still overrides your global choice.

Restart OpenCode's background service so it picks up the plugin:

```sh
opencode service restart
```

## Credentials

Set up Exa and Parallel the same way you would for OpenCode's native providers: run `/connect` in the TUI, or set `EXA_API_KEY` and `PARALLEL_API_KEY` in the environment the OpenCode server runs in.

## Behavior

| Exa outcome | Result |
| --- | --- |
| Usable results | Exa results; Parallel is not called |
| Error, HTTP 429, timeout, or no usable results | Parallel results |
| Search cancelled | Cancellation is passed through; Parallel is not called |
| Exa and Parallel both fail | One error naming both causes, with API keys redacted |

If Parallel succeeds with zero results, the search returns an empty list (OpenCode reports "No search results found").

## Options

Options are only available when the plugin is loaded through the `plugins` list:

```jsonc
{
  "plugins": [
    {
      "package": "github:lemon07r/opencode-exa-parallel",
      "options": {
        "timeoutMs": 15000,
      },
    },
  ],
}
```

| Option | Default | Description |
| --- | --- | --- |
| `timeoutMs` | `20000` | Time limit for each provider attempt, in milliseconds. OpenCode's native providers also stop after 25 seconds. |
| `primary` | `"exa"` | Provider tried first. |
| `fallback` | `"parallel"` | Provider tried when the first one fails. |

## Development

```sh
npm test
```

The tests use Node's built-in test runner and a fake plugin context, so they need no network access or API keys.

## License

[MIT](LICENSE)
