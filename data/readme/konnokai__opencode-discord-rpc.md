# opencode-discord-rpc

Discord Rich Presence plugin for [OpenCode](https://opencode.ai) - Show your AI-assisted coding activity in Discord!

![Discord Rich Presence Preview](https://img.shields.io/npm/v/@konnokai/opencode-discord-rpc?style=flat-square&color=5865F2)

## Features

- Shows your current AI model being used (GPT-4, Claude, etc.)
- Displays session duration (elapsed time)
- Shows activity status (Coding/Idle/Thinking)
- Clickable button to visit OpenCode.ai
- Auto-reconnects if Discord restarts
- Zero configuration needed

## Installation

OpenCode v2 plugin. Add it to the `plugins` array in your `opencode.json(c)`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["@konnokai/opencode-discord-rpc"]
}
```

For global installation, add it to `~/.config/opencode/opencode.json`. A local
checkout also works:

```json
{
  "plugins": ["E:/repos/opencode-discord-rpc"]
}
```

Options go in the object form:

```json
{
  "plugins": [
    {
      "package": "@konnokai/opencode-discord-rpc",
      "options": { "clientId": "1234567890", "maxRetries": 0 }
    }
  ]
}
```

OpenCode reloads plugins when the config changes, so no restart is needed.

## How It Works

The plugin subscribes to the OpenCode event stream and updates Discord as the
session moves:

- **Coding...** - a tool is executing or a session started working
- **Thinking...** - the model is generating or reading a tool result
- **Waiting for input...** - the turn finished, a permission or form is open
- **Idle** - no session has run yet

Subagent sessions and parallel sessions are tracked separately, so a finished
subagent does not flip the presence to idle while the main session is still
busy.

## Rich Presence Display

```
┌─────────────────────────────────────────┐
│ [OpenCode Logo]                         │
│                                         │
│ Using gpt-4o                            │
│ Coding...                               │
│ 01:23:45 elapsed                        │
│                                         │
│ [ Visit OpenCode.ai ]                   │
└─────────────────────────────────────────┘
```

## Configuration

The plugin works out of the box with no configuration needed. Each option also
reads the matching environment variable, and the plugin option wins.

| Option | Environment variable | Description | Default |
|--------|----------------------|-------------|---------|
| `enabled` | `OPENCODE_DISCORD_ENABLED` | Set to `false` (or `"false"`) to disable | `true` |
| `clientId` | `OPENCODE_DISCORD_CLIENT_ID` | Use your own Discord Application | Built-in |
| `retryInterval` | `OPENCODE_DISCORD_RETRY_INTERVAL` | Base reconnect interval (ms) | `15000` |
| `maxRetries` | `OPENCODE_DISCORD_MAX_RETRIES` | Max reconnect attempts, `0` = forever | `0` |

Reconnect delay grows with each attempt and caps at 60 seconds, so starting
OpenCode before Discord is fine. `retryInterval` below 1000 is ignored.

OpenCode runs one plugin instance per location in the same process; the
Discord connection is shared between them, and the first setup's options win
until the plugin reloads.

## Requirements

- OpenCode v2.3 or newer
- Discord Desktop App (must be running)

## Troubleshooting

### Rich Presence not showing

1. **Make sure Discord is running** - The desktop app must be open
2. **Check Activity Status is enabled** - In Discord Settings > Activity Privacy, ensure "Display current activity as a status message" is ON
3. **Restart OpenCode** - The plugin connects on startup

### Connection errors in logs

The plugin will automatically retry if Discord isn't available. Common messages:

- `"Discord is not running or not accessible"` - Discord desktop app is closed; the plugin keeps retrying
- `"Event stream failed, reconnecting"` - the OpenCode event stream dropped and the plugin resubscribed

## Privacy

This plugin does **not** display:
- Your project name or path
- File names or contents
- Any code or conversation content

It only shows:
- The AI model being used
- Your activity status
- How long the session has been active

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

```bash
# Clone the repository
git clone https://github.com/konnokai/opencode-discord-rpc.git
cd opencode-discord-rpc

# Install dependencies
npm install

# Build
npm run build

# Smoke test (plugin shape and setup lifecycle)
npm test

# Watch mode for development
npm run dev
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

- Built for [OpenCode](https://opencode.ai)
- Uses [@xhayper/discord-rpc](https://github.com/xhayper/discord-rpc) for Discord IPC communication
