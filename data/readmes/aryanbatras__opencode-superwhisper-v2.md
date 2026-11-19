# OpenCode Superwhisper V2

OpenCode V2 plugin for [Superwhisper](https://superwhisper.com) voice notifications and hands-free replies.

The original [`@superwhisper/opencode`](https://www.npmjs.com/package/@superwhisper/opencode) plugin is built for OpenCode V1 and fails to load in OpenCode V2. This is a local-first V2 port of that plugin.

> Unofficial community port. Not affiliated with Superwhisper or OpenCode. Based on the MIT-licensed `@superwhisper/opencode` 1.0.8 source.

## Requirements

- [OpenCode](https://opencode.ai) 2.0 or newer
- [Superwhisper](https://superwhisper.com) for macOS
- Node.js 20 or newer

## Install

Clone into your OpenCode plugins directory:

```bash
git clone https://github.com/aryanbatras/opencode-superwhisper-v2.git \
  ~/.config/opencode/plugins/superwhisper
```

OpenCode discovers plugin package directories in `~/.config/opencode/plugins/` automatically. Restart OpenCode after cloning.

If you clone somewhere else, add the directory to `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["/absolute/path/to/opencode-superwhisper-v2"]
}
```

Local plugin paths must point to a directory, not a single file.

Verify the plugin loaded:

```bash
opencode plugin list
```

You should see:

```text
superwhisper   local   /Users/<you>/.config/opencode/plugins/superwhisper
```

## What it does

- Sends a Superwhisper notification when an OpenCode turn completes.
- Reads your spoken reply and injects it as the next prompt.
- Sends error notifications when an execution fails.
- Sends permission requests with voice approval options.
- Supports per-session bypass permissions.
- Registers `superwhisper_toggle` to enable or disable voice notifications for the current session.
- Includes project, branch, and session title in notification metadata.
- Skips subagent sessions.
- Drops stale notifications when you interact with OpenCode directly.

## How it works

```text
You speak -> OpenCode works -> plugin notifies Superwhisper -> you speak back -> loop
```

1. OpenCode emits `session.idle`.
2. The plugin reads the completed assistant text.
3. The plugin writes the message to `/tmp/superwhisper-agent/`.
4. The plugin writes an `agent-update` payload to the Superwhisper inbox and opens `superwhisper://agent-wake` when needed.
5. Superwhisper shows the notification and records your reply.
6. Superwhisper writes the response file.
7. The plugin polls the response file and sends the text back with `ctx.session.prompt`.

## Permissions

Permission notifications offer these voice choices:

| Choice | OpenCode decision |
| --- | --- |
| Allow | `once` |
| Always Allow | `always` |
| Bypass permissions for this session | `once`, then auto-allow later requests |
| Deny | `reject` |

Bypass mode writes a marker to `/tmp/superwhisper-agent/<sessionID>-bypass-perms`. Later permission requests in that session are allowed automatically.

## Toggle per session

Ask OpenCode to disable or enable voice notifications. The plugin exposes the `superwhisper_toggle` tool with `action: "enable" | "disable"`.

## Configuration

Environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `SUPERWHISPER_DEBUG` | off | Write debug logs to `/tmp/superwhisper-agent/debug.log` |
| `SUPERWHISPER_SCHEME` | auto-detected | Override the deeplink scheme |
| `SUPERWHISPER_DIR` | `/tmp/superwhisper-agent` | Override the message directory |
| `SUPERWHISPER_POLL_INTERVAL_MS` | `1000` | Response poll interval |
| `SUPERWHISPER_POLL_TIMEOUT_MS` | `1800000` | Response poll timeout |

The plugin uses `superwhisper-debug://` when it detects a Superwhisper debug build under `DerivedData`. Otherwise it uses `superwhisper://`.

## V2 differences from the V1 plugin

- Reads `event.data` instead of `event.properties`.
- Reads assistant text from `message.content` parts instead of `message.parts`.
- Replies to permissions with `ctx.permission.reply({ sessionID, requestID, decision })`.
- Registers tools with `ctx.tool.transform`.
- Watches `session.execution.failed` instead of `session.error`.
- Ignores idle events whose outcome is `failed` or `interrupted`, avoiding duplicate notifications.

## Limitations

OpenCode V2 removed the V1 `question.asked` event, and the V2 plugin context has no API for replying to `form.created` forms. Question/form prompts are not answered by this plugin. Completion, error, and permission flows are supported.

## Troubleshooting

Check that OpenCode loaded the plugin:

```bash
opencode plugin list
grep -i superwhisper ~/.local/share/opencode/log/opencode.log | tail
```

Check the Superwhisper inbox:

```bash
ls -la ~/Library/Application\ Support/superwhisper/agent/inbox
```

Run with debug logging:

```bash
SUPERWHISPER_DEBUG=1 opencode
tail -f /tmp/superwhisper-agent/debug.log
```

## Development

No dependencies. Tests use Node's built-in test runner.

```bash
npm test
```

The integration test simulates the V2 event stream, completion reply, permission reply, and failed-idle filtering.

## License

MIT. See [LICENSE](LICENSE).
