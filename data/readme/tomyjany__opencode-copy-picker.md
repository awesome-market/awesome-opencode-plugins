# opencode-copy-picker

Copy exactly the part you need from the latest OpenCode assistant reply: the whole reply, a Markdown section, or one fenced code block.

## Preview

![Copy picker running inside an OpenCode session](assets/copy-picker-in-opencode.png)

![Copy picker dialog with whole-reply and code-block choices](assets/copy-picker-dialog.png)

## Features

- `/copy-part` opens an OpenCode-native picker.
- `Ctrl+Y` opens the same picker by default.
- Code blocks are copied without their Markdown fences.
- Normal terminals use native clipboard commands with OSC52 fallback.
- Sandboxes can use a configurable, write-only HTTP clipboard bridge.
- The plugin never reads the clipboard.

## Install

Install globally from npm:

```bash
opencode plugin --global opencode-copy-picker
```

For local development, build the repository and add the bundle to `~/.config/opencode/tui.json`:

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "plugin": ["/absolute/path/to/opencode-copy-picker/dist/tui.js"]
}
```

## Configuration

Plugin options use the tuple form supported by `tui.json`:

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "plugin": [
    [
      "opencode-copy-picker",
      {
        "keybind": "ctrl+y",
        "clipboard": { "transport": "auto" }
      }
    ]
  ]
}
```

Set `keybind` to `false` to keep `/copy-part` without registering a shortcut.

### Docker sbx

The plugin can send selected text to a host-side, write-only endpoint:

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "plugin": [
    [
      "/home/agent/.config/opencode-omniroute/plugins/copy-picker/dist/tui.js",
      {
        "clipboard": {
          "transport": "http",
          "url": "http://host.docker.internal:20129/__sbx_clipboard"
        }
      }
    ]
  ]
}
```

The HTTP request is `POST` with `Content-Type: application/json` and body `{ "text": "..." }`. An optional `tokenEnv` setting adds `Authorization: Bearer ...` using the named environment variable.

## Development

```bash
corepack enable
pnpm install
pnpm check
```

## Security

Only text explicitly selected in the picker is passed to the configured clipboard transport. HTTP transport URLs are opt-in. Tokens are read from the configured environment variable and never included in the request body or error messages.

## License

MIT
