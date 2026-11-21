# opencode-telegram-notify

Telegram notifications for [opencode](https://opencode.ai) — get pinged when the agent finishes a turn, needs permission, hits an error, or asks a question. Reply from your phone to continue the session, approve/reject permissions via inline buttons.

- One plugin, zero runtime dependencies (plain `fetch`, no `telegraf` needed)
- Two-way: Telegram → opencode via long-polling `getUpdates`
- Long messages (>4000 chars) auto-upload as `.md` file
- Fail-silent: missing token/chat, network errors, timeouts never break opencode
- Debounced `busy → idle`, delayed permission (auto-accept suppresses), subagent spam filter

## Quick install

```bash
git clone <this-repo> && cd opencode-telegram-notify
./install.sh
# prompts for bot token + chat ID, builds, verifies the token,
# writes the plugin entry to ~/.config/opencode/opencode.jsonc,
# and sends a test message. Then restart opencode.
```

Non-interactive / other targets:

```bash
./install.sh --token 123456:ABC... --chat-id 145264105
./install.sh --project-dir /path/to/project   # project-local instead of global
./install.sh --help
```

## Triggers

| Event | Telegram |
|---|---|
| `session.status` busy→idle / `session.idle` | ✅ waiting for input + last assistant text |
| `permission.updated` / `permission.asked` | 🔐 permission + Allow once / Always / Reject buttons |
| `tool.execute.before` on `ask`/`question`/`confirm`, `question.asked` | ❓ question ping |
| `session.error` | ❌ error text |
| `permission.replied` | cancels pending notification |

## 1. Create a bot

1. In Telegram: `@BotFather` → `/newbot` → copy token (`123456:ABC-...`)
2. DM your bot anything, then:
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getUpdates
   # read chat.id → your chat ID
   ```
3. Groups: `/mybots` → Group Privacy OFF, add bot, send message, re-read `getUpdates`.

## 2. Install

```bash
cd opencode-telegram-notify
npm install
npm run build
```

Add to `opencode.json` (project) or `~/.config/opencode/opencode.json` (global):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    ["file:///abs/path/opencode-telegram-notify/dist/index.js", {
      "botToken": "123456:ABC-DEF...",
      "chatId": "145264105"
    }]
  ]
}
```

Or env-only (no options):

```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-..."
export TELEGRAM_CHAT_ID="145264105"
# opencode.json: "plugin": ["file:///abs/path/opencode-telegram-notify/dist/index.js"]
```

Options override env vars. Full shape — see `opencode.json.example`.

> Restart opencode after changing config — plugins load at startup.

## 3. Use

- Work normally. When opencode idles / asks permission / asks a question → Telegram message with `[session: name]`.
- **Reply** to a notification to send text back into that session.
- Tap **Allow once / Always / Reject** on permission messages.
- Commands in Telegram DM: `/telegram-pause`, `/telegram-resume`, `/telegram-status`.
- Same via TUI: run `telegram-pause` / `telegram-resume` (intercepted, never reach LLM).

## 4. Config reference

| Option | Env fallback | Default |
|---|---|---|
| `botToken` | `TELEGRAM_BOT_TOKEN` | required |
| `chatId` (`recipientChatId`) | `TELEGRAM_CHAT_ID` | required |
| `message` | — | `opencode agent is waiting for your input` |
| `enabled` | `TELEGRAM_ENABLED` | `true` |
| `debug` | `TELEGRAM_DEBUG=1` | `false` → logs `/tmp/opencode-telegram-debug.log` |
| `ignoreSubagents` | — | `true` |
| `notifyOn: {idle, error, permission, question}` | — | all `true` |

## 5. Dev

```bash
npm run typecheck
npm run build
npm test
```

Test without Telegram: set `debug: true`, watch `/tmp/opencode-telegram-debug.log` for `event: ...` lines.
