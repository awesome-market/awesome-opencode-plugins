# opencode-daily

[![npm version](https://img.shields.io/npm/v/opencode-daily.svg)](https://www.npmjs.com/package/opencode-daily)
[![license](https://img.shields.io/npm/l/opencode-daily.svg)](./LICENSE)

An [OpenCode](https://opencode.ai) plugin that solves two common problems with a
single install:

1. **The model never knows the current date.** OpenCode puts `Today's date` in a
   cached system block, and long-running or resumed sessions get stuck on stale
   information. This plugin injects a **fresh local date/time into every user
   message** (cache-safe), so the model always knows the real day.
2. **No per-day record of what was done (Scrum).** It adds a `/standup` command
   and a `daily_log` tool that keep a log per day at
   `.opencode/daily/YYYY-MM-DD.md`.

## Why a plugin

- **Model-agnostic:** it does not rely on the model following instructions.
- **Cache-safe:** it only touches the user message, never the cached system prefix.
- **One-line install** and zero runtime dependencies.

## Install

Add it to your `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-daily"]
}
```

Restart OpenCode. That's it — dates are injected automatically.

## Configuration

Pass options using the tuple form:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    ["opencode-daily", {
      "timezone": "America/Bogota",
      "format": "iso",
      "dailyDir": ".opencode/daily"
    }]
  ]
}
```

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `timezone` | `string` | system | IANA time zone (e.g. `Europe/Madrid`). Invalid values fall back to the system zone. |
| `format` | `"iso" \| "locale" \| "custom"` | `"iso"` | How the injected date is rendered. |
| `customFormat` | `string` | `"YYYY-MM-DD HH:mm:ss"` | Token format used when `format` is `"custom"`. Supports `YYYY YY MM DD HH mm ss dddd Z z`. |
| `locale` | `string` | system | Locale used by the `locale` format (e.g. `es-CO`). |
| `includeTime` | `boolean` | `true` | Include the time, not just the date. |
| `includeInEveryMessage` | `boolean` | `true` | Inject on every user message. |
| `onlyOnDateChange` | `boolean` | `false` | Inject only when the day changes within a session. |
| `prefix` | `string` | `"[Local date/time: "` | Text placed before the date. |
| `suffix` | `string` | `"]"` | Text placed after the date. |
| `dailyDir` | `string` | `".opencode/daily"` | Folder for the daily logs, relative to the project root. |
| `enableCommand` | `boolean` | `true` | Register the `/standup` command. |
| `enableTool` | `boolean` | `true` | Register the `daily_log` tool. |

Every option can also be provided through the environment:
`OPENCODE_DAILY_TIMEZONE`, `OPENCODE_DAILY_FORMAT`, `OPENCODE_DAILY_CUSTOM_FORMAT`,
`OPENCODE_DAILY_LOCALE`, `OPENCODE_DAILY_INCLUDE_TIME`,
`OPENCODE_DAILY_INCLUDE_EVERY_MESSAGE`, `OPENCODE_DAILY_ONLY_ON_DATE_CHANGE`,
`OPENCODE_DAILY_PREFIX`, `OPENCODE_DAILY_SUFFIX`, `OPENCODE_DAILY_DIR`,
`OPENCODE_DAILY_ENABLE_COMMAND`, `OPENCODE_DAILY_ENABLE_TOOL`.

## Usage

### `/standup`

Generate today's stand-up and append it to the daily log:

```
/standup focused on the plugin release
```

### `daily_log` tool

The model can call it directly:

- `action: "read"` — read today's log.
- `action: "append"`, `section: "done" | "doing" | "blocker" | "note"`, `text: "..."` — add an entry.

## How it works

- **Date injection** uses the `chat.message` hook and prepends the formatted date
  to the first text part of each user message. It is idempotent (it won't inject
  twice) and never modifies the cached system prompt.
- **`/standup`** is registered through the plugin `config` hook.
- **`daily_log`** is a custom tool that reads and writes Markdown files under
  `dailyDir`, one file per day.

If a specific OpenCode version does not allow plugins to register commands, the
`daily_log` tool still works, and you can create the command manually:

```markdown
---
description: Generate today's Scrum stand-up summary and append it to the daily log.
---

Run a Scrum daily stand-up for today following the instructions in the opencode-daily README.
```

## Programmatic API

```ts
import { formatTime, resolveOptions, appendDailyLog } from "opencode-daily/utils"

const options = resolveOptions({ timezone: "America/Bogota" })
const now = formatTime(options)
console.log(now.formatted)
```

## Compatibility

- OpenCode `>= 1.0.0` (`@opencode-ai/plugin` peer dependency).
- Node `>= 18`. Works on Windows, macOS and Linux.

## License

[MIT](./LICENSE)
