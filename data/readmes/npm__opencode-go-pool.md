# opencode-go-pool

Multi-account pool, quota monitor and local usage ledger for **OpenCode Go**, inside OpenCode CLI and OpenCode Desktop.

![Go pool usage in OpenCode CLI and Desktop](https://raw.githubusercontent.com/den1251/opencode-go-pool/main/docs/screenshots/overview.png)

*Screenshots use example data.*

## Install

```bash
opencode plugin add opencode-go-pool
```

Restart OpenCode after installing. That is the whole installation.

This is a plugin, not a separate app or command-line tool. It adds no `opencode-go-pool` binary and no global npm package. The server, TUI and Desktop parts ship together in the same package.

Requires OpenCode 2.x. The Desktop panel requires an OpenCode Desktop build with GUI plugin support.

## Open the usage view

### OpenCode CLI/TUI

Run `/go-pool` in a session, or open the command palette and choose **Go pool usage**.

The dialog shows account quotas, today and month totals, and per-model requests, tokens, list cost and Go plan usage.

### OpenCode Desktop

Open the session panel **+** menu and choose **Open Go pool usage**, or type `/go-pool` in the composer.

![Open Go pool usage in the Desktop session panel menu](https://raw.githubusercontent.com/den1251/opencode-go-pool/main/docs/screenshots/desktop-menu-icon.png)

The **Go Pool** side panel shows the same data and has a **Refresh** button. It is on demand: there is no footer text or composer pill, and no background polling.

## What it does

- Rotates between OpenCode Go accounts in a persistent order: one account is used until its Go allowance is drained, then the next.
- Reads the account-level usage percentage from OpenCode's Go API: `GET https://opencode.ai/zen/go/v1/usage` (`rolling` / `weekly` / `monthly`, each with `status`, `percent`, `resetsAt`).
- Tracks local tokens and cost per person, per account and per model. Usage is stored only on the machine where the plugin runs.
- Shows account quota and local usage in the OpenCode CLI and Desktop.
- Shows every model separately, with requests, input/output tokens, list cost and Go plan usage.

## What is exact

| Measurement | Exact? | Source |
|---|---|---|
| Account quota used (5h / week / month) | Yes | Go usage API |
| Tokens used by this OpenCode installation | Yes | `usage.opencode.tokens` in the HTTP response, with `session.step.ended` as fallback |
| Exact list cost for a request | Yes | `usage.opencode.list_cost` |
| Exact amount charged | Yes | `usage.cost` (`0` inside a Go allowance) |
| Go plan allowance consumed | Yes | `usage.opencode.allowance` |
| Billing source | Yes | `usage.opencode.billing_source` |
| Cost for a response with no `opencode` block | Estimate | model catalog price × tokens |

The plugin reads the raw response body for every successful `opencode-go` request. It handles a plain JSON body and a streaming SSE body, taking the final usage object. For a stream, this does not delay the response: the original body is returned to OpenCode and a clone is parsed in the background.

When the exact `opencode.list_cost` is present, it is used as the entry's `cost`, and `estimated` is `false`. The catalog estimate is only a fallback for responses that do not report OpenCode-specific usage.

`opencode.allowance` is the plan-dollar amount the request counted toward the Go limit. Summing it per machine gives that machine's exact consumed share for captured requests. The account-wide `/usage` percentages remain the authoritative account total.

## Accounts

The plugin does not ask for or store keys itself. It discovers credentials already known to OpenCode:

- `opencode-go` API-key connections, and
- `opencode` Console OAuth connections (the normal OpenCode Console login used for Go).

Add accounts with OpenCode's own UI or CLI:

```bash
opencode auth login opencode-go
```

In Desktop, use the provider's **Add account** flow. The plugin notices new credentials through `credential.updated` / `integration.updated` and begins using them without a restart.

Accounts with the same Console workspace (`orgID`) are treated as one account, because the Go allowance is workspace-wide. Different workspaces and different API keys are separate accounts.

The first usable account in the persistent order is active. New accounts are discovered newest-first, so the account currently active in OpenCode is preferred on first run. When the active account reaches 100% in any window (or Go returns `429`), the next usable account is selected and persisted automatically.

## Configuration

Plugin options are passed through the OpenCode config entry:

```jsonc
{
  "plugins": [
    {
      "package": "opencode-go-pool",
      "options": {
        "switchAtPercent": 100,
        "refreshSeconds": 60,
        "dashboard": false,
        "dashboardPort": 0
      }
    }
  ]
}
```

| Option | Default | Meaning |
|---|---|---|
| `switchAtPercent` | `100` | Switch when any window reaches this used percentage |
| `refreshSeconds` | `60` | Quota cache lifetime |
| `dashboard` | `false` | Start the optional local dashboard |
| `dashboardPort` | `0` | Dashboard port; `0` chooses a free port |
| `dataDir` | native per-OS directory | Local state directory |
| `requestTimeoutMs` | `5000` | Quota request timeout |
| `debug` | `false` | Also print log lines to stderr |
| `usageURL` | official Go usage URL | Override for tests |
| `upstream` | `https://opencode.ai` | Override for tests |

The optional dashboard binds to `127.0.0.1` and is read-only except for **Refresh quota** and **Clear all local usage**. Its URL and token are written to `dashboard.json` in the data directory.

## Local data

This is a per-PC ledger. There is no account splitting, user profile or upload. All usage files stay in the local data directory.

The data directory is native per OS:

| OS | Default |
|---|---|
| Linux | `~/.local/share/opencode-go-pool/` (or `$XDG_DATA_HOME/opencode-go-pool/`) |
| macOS | `~/Library/Application Support/opencode-go-pool/` |
| Windows | `%APPDATA%\opencode-go-pool\` |

Set `OPENCODE_GO_POOL_DIR` or the `dataDir` option to override it.

```
status.json       current snapshot (accounts, quota, aggregates)
accounts.json     persistent account order and active account
quota.json        last quota response per account
cooldown.json     429 cooldowns
events/           one JSON file per usage event
machine.json      stable machine ID
dashboard.json    dashboard URL/token/pid
plugin.log        plugin log
switches.json     recent account switches
```

All files are created with owner-only permissions. Events older than 120 days are pruned at startup. Clearing local usage never changes the account's Go quota.

## How it works

1. `session.hook("http.request")` runs for `opencode-go` requests. It selects an account, rewrites `Authorization` (and the org header for Console accounts), and stores a replayable request template.
2. `session.hook("http.response")` returns every successful response unchanged, but clones its body and parses the final usage object. For a `429` it marks the account, selects the next one, retries the same request, and captures the retry response's usage on the successful account. If every account fails, it returns a `429` with a clear message.
3. Quota is refreshed on demand: before a request when the cached snapshot is older than `refreshSeconds`, and after a successful response. There is no background quota polling loop.
4. `session.step.ended` supplies the step boundary and a fallback `cost` / `tokens`. The raw response provides the exact `list_cost`, `allowance`, `billing_source` and billed tokens. The event itself does not carry a model, so the model and account come from the matching HTTP request context, shared across plugin instances by data directory.
5. The raw response is matched to the step by session, request kind and model. A global claim ensures one event is written once even when OpenCode activates several plugin locations.
6. A response whose raw cost fields are absent falls back to OpenCode's reported cost, then to the model catalog estimate.

## Usage accounting

Each completed step writes one JSON file to `events/`, named `<UTC day>__<event ID>.json`:

```json
{
  "id": "evt_...",
  "ts": 1794322562184,
  "day": "2026-11-10",
  "machineID": "mch_...",
  "accountID": "cred_...",
  "accountLabel": "Personal",
  "providerID": "opencode-go",
  "model": "deepseek-v4.1-flash",
  "modelName": "DeepSeek V4.1 Flash 1017",
  "cost": 0.00412,
  "listCost": 0.00412,
  "allowance": 0.003,
  "charged": 0,
  "billingSource": "go",
  "metering": "response",
  "estimated": false,
  "tokens": {
    "input": 17300,
    "output": 3,
    "reasoning": 0,
    "cacheRead": 0,
    "cacheWrite": 0
  },
  "sessionID": "ses_..."
}
```

Token meanings follow OpenCode's `TokenUsage.Info`:

| Field | Meaning |
|---|---|
| `input` | non-cached input tokens |
| `output` | visible output tokens |
| `reasoning` | reasoning tokens, reported separately from visible output |
| `cacheRead` | prompt-cache read tokens |
| `cacheWrite` | prompt-cache write tokens |

The total token count is the sum of all five. The panel shows only `input in / output out`; the event files contain the complete breakdown.

Cost fallback order:

1. exact `listCost`
2. positive `charged`
3. catalog estimate

The catalog estimate is:

```
input × inputPrice
+ (output + reasoning) × outputPrice
+ cacheRead × cacheReadPrice
+ cacheWrite × cacheWritePrice
```

Prices are USD per million tokens from the `opencode-go` model catalog. The pricing tier is selected by the request context size (`input + cacheRead + cacheWrite`). The entry is marked `estimated: true` only when this fallback is used.

Aggregation scans the event files for the requested UTC day or month prefix, then sums cost, list cost, allowance and all five token counters per account and model. `status.json` is only a derived snapshot; the event files are the source of truth.

Known limits on OpenCode 2.2.6:

- Only successful `session.step.ended` events are recorded. `session.step.failed` is ignored.
- `session.usage.recorded` is not exposed by 2.2.6, so title, compaction and generate calls are not in the ledger.
- Day and month buckets are UTC, not the machine's local timezone.

## Update

```bash
opencode plugin check opencode-go-pool
opencode plugin update opencode-go-pool
```

Restart OpenCode after updating.

## Install from source

```bash
git clone https://github.com/den1251/opencode-go-pool.git
cd opencode-go-pool
bun install
bun run build
```

Point OpenCode at the checkout while developing:

```jsonc
{
  "plugins": ["/absolute/path/to/opencode-go-pool"]
}
```

A configured absolute directory works; an auto-discovered `~/.config/opencode/plugin` symlink does not provide the HTTP hooks on OpenCode 2.2.6.

## Publishing

For maintainers:

1. Bump `version` in `package.json`.
2. Run `bun run typecheck` and `bun test`.
3. Run `bun run build`.
4. Check the package contents with `npm pack --dry-run`.
5. Log in to npm and confirm the account:

```bash
npm login
npm whoami
```

6. Publish with 2FA. A direct publish prompts for the 2FA challenge:

```bash
npm publish
```

Non-interactive, with a current one-time code:

```bash
npm publish --otp=123456
```

If npm cannot complete your security-key challenge, use staged publishing:

```bash
npm stage publish
npm stage list
npm stage approve <stage-id>
```

You can also approve the staged version in the browser on npmjs.com under **Staged Packages**.

For automated releases, configure trusted publishing (OIDC) instead of a bypass-2FA token.

`publishConfig.access` is already `public`.

After publishing:

```bash
npm view opencode-go-pool version
opencode plugin update opencode-go-pool
```

Restart OpenCode to load the new plugin version. If the OpenCode config points at a local checkout, replace that path with `opencode-go-pool` before updating.

## License

MIT. See [LICENSE](LICENSE).
