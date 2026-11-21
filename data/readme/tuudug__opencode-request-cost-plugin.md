# opencode-request-cost-plugin

OpenCode TUI plugin that adds the USD cost to the prompt status line after each model request.

It listens for OpenCode `step-finish` events, calculates cost from the active model price and token usage, then renders it persistently in the prompt status area:

```text
▣  Plan · GPT-5.5 Fast · 3.3s - 0.03$
```

## Install

```bash
bun add opencode-request-cost-plugin
```

Or with npm:

```bash
npm install opencode-request-cost-plugin
```

## Configure OpenCode

Add the plugin to `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-request-cost-plugin"]
}
```

Restart OpenCode after editing config. Plugins are loaded at startup.

## Options

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    [
      "opencode-request-cost-plugin",
      {
        "decimals": 2,
        "includeModel": false,
        "prefix": " - ",
        "showTokens": false,
        "source": "auto",
        "suffix": ""
      }
    ]
  ]
}
```

| Option | Default | Description |
|---|---:|---|
| `decimals` | `2` | Number of decimal places in `x.xx$`. |
| `includeModel` | `false` | Include `provider/model` after the cost. Usually unnecessary because OpenCode already shows the model in the status line. |
| `prefix` | ` - ` | Text inserted before the cost. |
| `showTokens` | `false` | Include input/output token counts. |
| `source` | `auto` | `auto`, `calculated`, or `opencode`. |
| `suffix` | `` | Text inserted after the cost. |

`source: "auto"` calculates from the model price when available and falls back to OpenCode's emitted cost if provider-specific billing differs.

This is a TUI plugin, not a toast/dialog plugin. It uses OpenCode's `session_prompt_right` slot.

## Development

```bash
bun install
bun run typecheck
bun run build
```

Before publishing:

```bash
bun run prepublishOnly
npm publish
```

## License

MIT
