# OpenCode Go Usage — DeepSeek Harness plugin

A small DeepSeek Harness (dsh) UI plugin that shows your **OpenCode Go** allowance right under the chat composer:
the rolling 5-hour window, the weekly window, and the monthly window, as percentages with progress bars.

```
OpenCode Go   5h ▮▮░░░░░░  2%   Week ▮▮▮░░░░  6%   Month ▮▮░░░░░  3%   Usage details   ↻
```

## Features

- Compact row in the composer dock: `OpenCode Go · 5h 2% · Week 6% · Month 3% · Usage details · ↻`
- Hover a meter to see when that window resets; meters turn amber at 80% and red when the limit is reached
- "Usage details" opens the matching page in the OpenCode Console
- Refreshes every 60 seconds; the `↻` button refreshes on demand
- After a reboot it notices the local OpenCode service is down and starts it again automatically (up to two attempts, ~8 s of polling)
- English and Chinese UI, following the app language

## Requirements

1. **DeepSeek Harness** with plugin bundle support (this plugin is a standard `dsh.bundle` package).
2. **OpenCode v2 CLI** — the plugin reads usage from the local OpenCode service that the v2 CLI ships:
   ```bash
   npm install -g @opencode/cli@2.2.5
   ```
   The plugin only needs the *service*; if you already run `opencode serve --service` yourself, the CLI
   does not have to be installed next to the plugin.
3. **One-time sign-in** to the OpenCode Console workspace that owns your Go plan:
   ```bash
   opencode auth login      # choose: OpenCode Console → OpenCode Console account
   ```
   This stores the credential in the OpenCode data directory; the plugin never sees it. It only talks to the
   local service over HTTP with the password from `service.json`.

## Install

1. Clone this repository somewhere stable, e.g. `~/dsh-plugins/opencode-go-usage`:
   ```bash
   git clone https://github.com/niantian2/dsh-opencode-go-usage.git
   ```
2. Install the folder as a bundle in your DSH profile. From the Harness Web UI, ask the agent to install the
   bundle directory, or use the plugin manager's *install bundle* action with the absolute folder path:
   ```
   install_bundle target=/absolute/path/to/dsh-opencode-go-usage
   ```
3. Reload the Web UI. The row appears under the composer in any session.

If the automatic start cannot find the CLI, point the plugin at it:

```bash
OPENCODE_CLI_PATH=/absolute/path/to/opencode
```

(windows: `%USERPROFILE%\...\node_modules\@opencode\cli\bin\opencode.exe`)

## How it works

- **Host half** (`index.js`) registers a same-origin route `GET /plugins/opencode-go-usage/usage`.
  It reads `~/.local/state/opencode/service.json` for the service URL/password, calls
  `GET /api/experimental/usage/limits` with HTTP Basic auth (`opencode:<password>`), and caches the
  snapshot for 30 seconds. Query flags: `?refresh=1` bypasses the cache, `?start=1` may spawn
  `opencode serve --service` when the service is not answering.
- **Client half** (`client.js`) registers a cell in the `conversation.composer.dock` slot and polls the
  route. It never sees the service password.

The response is the official one:

```json
{
  "data": {
    "workspace": { "id": "org_...", "name": "Personal", "usageURL": "https://opencode.ai/console/..." },
    "go": {
      "rolling": { "percent": 2, "limited": false, "resetsAt": 1793779082000 },
      "weekly":  { "percent": 6, "limited": false, "resetsAt": 1794182400000 },
      "monthly": { "percent": 3, "limited": false, "resetsAt": 1796283956000 }
    },
    "budgets": []
  }
}
```

Percentages are the share of the Go plan's monthly dollar allowance already spent in each window
(the 5-hour window is capped at 20% of the monthly allowance, the week at 50%, the month at 100%).

## Notes

- Everything is local: the plugin talks to `127.0.0.1` only. No telemetry, no remote calls from the browser.
- The service password is read on the host side from `service.json` and used for a loopback request; it is
  never serialized into the snapshot returned to the browser.
- This is an unofficial community plugin and is not affiliated with OpenCode.

## License

MIT — see [LICENSE](LICENSE).
