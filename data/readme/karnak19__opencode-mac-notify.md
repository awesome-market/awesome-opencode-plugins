# opencode-mac-notify

macOS notifications for OpenCode that work in the TUI, in headless runs and through the API.

## Install

```sh
opencode plugin add github:Karnak19/opencode-mac-notify
```

The command installs the plugin from this repository and adds it to your global `opencode.json`:

```json
{
  "plugins": ["github:Karnak19/opencode-mac-notify"]
}
```

The key is `plugins` on OpenCode v2. On v1 it is `plugin`.

Restart OpenCode afterwards — plugins are loaded at startup.

### Manual install

To vendor the source instead, clone it into your plugins directory:

```sh
git clone https://github.com/Karnak19/opencode-mac-notify.git ~/.config/opencode/plugins/opencode-mac-notify
```

then point `opencode.json` at the clone:

```json
{
  "plugins": ["file:///Users/VOTRE_NOM/.config/opencode/plugins/opencode-mac-notify"]
}
```

The path must be **absolute** and prefixed with `file:///` — `~` and relative paths do not resolve. It points at the cloned directory, whose `package.json` exposes `plugin.mjs`.

Zero dependencies, nothing to build.

## Why not the built-in setting

`attention.notifications` in `~/.config/opencode/cli.json` only writes an OSC escape sequence to the TUI's stdout. Two consequences:

- You need a terminal. Headless runs and API-driven sessions get nothing.
- The terminal must be blurred — a focused terminal swallows the escape sequence.

This plugin calls `osascript` directly, so the notification is emitted by macOS no matter what drives the session.

## What it does

| Event | Notification |
| --- | --- |
| `session.idle` | Title of the finished session. Root sessions only, subagents are ignored. |
| `permission.asked` | Permission requested, with the message. |
| `session.execution.failed` | Execution error. |

## Requirements

- macOS
- `osascript` (ships with the system)
- OpenCode v2

## Avoid double notifications

If `attention.notifications` is `true` in `~/.config/opencode/cli.json`, the TUI may also send its OSC notification when the terminal is blurred — one from the plugin, one from the TUI. Disable the built-in one:

```json
{
  "notifications": false,
  "sound": true
}
```

Keep `"sound": true` if you still want the terminal bell from the TUI; otherwise let the plugin handle the sound.

## Troubleshooting

- The notification is posted by the app that launched OpenCode (Terminal, Warp, iTerm, …). Check that this app is allowed in System Settings → Notifications.
- Focus / Do Not Disturb must be off, or notifications are silenced at the system level.
- Subagents do not notify on purpose. Only the root session announces itself.
- The sound is `Ping`. Change it in `plugin.mjs` (`DEFAULT_SOUND`) or pass a `sound` option to `createPlugin`.

## License

MIT
