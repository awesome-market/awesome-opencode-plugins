# opencode-session-stats

A TUI plugin for OpenCode that shows how many LLM requests you made today and
how that rate compares to the day so far.

## What it shows

- **Sidebar**: `LLM today  N · M/h`.
- **Composer**: the same line above the prompt.

The count comes from OpenCode's own session statistics, aggregated from local
midnight across every session, and refreshes every 10 seconds.

## Install

Add the plugin to the `plugins` array in `~/.config/opencode/cli.json`:

```json
{
  "plugins": ["opencode-session-stats@0.1.0"]
}
```

## Requirements

- OpenCode 2.2 or newer.
- No configuration and no credentials.

Servers that do not expose the experimental stats endpoint simply show
nothing.

## Development

```sh
git clone https://github.com/Kovami/opencode-session-stats.git
cd opencode-session-stats
npm install
npm run check
```

To run a local checkout in OpenCode, point `cli.json` at the folder instead of
the npm name:

```json
{
  "plugins": [
    { "package": "/absolute/path/to/opencode-session-stats" }
  ]
}
```

## Troubleshooting

- Nothing appears: make sure the plugin is listed in `~/.config/opencode/cli.json`
  (the CLI configuration), not in `opencode.json`.
- OpenCode 2.2 or newer is required. After saving the config, check
  `~/.local/share/opencode/log/opencode.log` for `plugin` lines.
- If the line is missing on an older server, the experimental stats endpoint is
  unavailable; the plugin stays silent instead of showing an error.

## License

MIT