# opencode-permission-notify

Approval prompts from OpenCode, as a native macOS floating panel in the top-right
corner of your screen — with **Allow once / Always / Reject** buttons, so you never
have to switch back to the OpenCode window to answer.

- **Non-activating** — the panel is an `NSWindowStyleMaskNonactivatingPanel`; clicking a button does not bring OpenCode forward or interrupt what you are doing
- **Quiet when it should be** — if OpenCode is already frontmost, nothing pops up
- **Never lost** — answers are written back immediately; after 5 minutes the panel closes and hands the request back to the in-window prompt
- **No dependencies** — no terminal-notifier, no notification permission; the helper binary ships with the package

## Install

```jsonc
// ~/.config/opencode/opencode.jsonc
{
  "plugins": ["opencode-permission-notify"]
}
```

Or point at a local checkout while developing:

```jsonc
{
  "plugins": ["/absolute/path/to/permission-notify"]
}
```

On first load the bundled universal binary (arm64 + x86_64) is extracted to
`~/Library/Application Support/opencode/permission-notify/bin/notify-request`.

**Requirements**: macOS, OpenCode V2 (desktop or TUI — the plugin runs in the
server).

## How it works

```
OpenCode server emits permission.asked
   ↓  the plugin filters by location (only the instance owning the session's
      directory handles it)
notify-request:
   OpenCode is frontmost → exit quietly
   otherwise draw a panel in the top-right corner and wait for a click
   ↓  stdout: index of the chosen button
ctx.permission.reply({ sessionID, requestID, decision })
```

The three buttons map to the `once` / `always` / `reject` decisions.

## Configuration

| Environment variable | Description |
| --- | --- |
| `PERMISSION_NOTIFY_HELPER` | Override the helper path (rarely needed) |

Log file: `~/Library/Application Support/opencode/permission-notify/notify.log`

## Build from source

Requires Xcode Command Line Tools:

```sh
./build.sh          # builds bin/notify-request (universal)
```

## Limitations

- macOS only
- Panels stack by request (up to five slots); many simultaneous requests overlap slightly
- Rejections do not carry feedback text yet (OpenCode supports reject-with-reason; this only sends `reject`)

## License

MIT

---

## 中文说明

把 OpenCode 的授权请求变成屏幕右上角的 macOS 原生浮窗，带「允许一次 / 总是允许 / 拒绝」
三个按钮，不抢焦点、不用切回窗口；OpenCode 已在前台时不弹。通用二进制助手随包分发。

安装：在 `~/.config/opencode/opencode.jsonc` 的 `plugins` 中加 `"opencode-permission-notify"`。
仅支持 macOS + OpenCode V2。
