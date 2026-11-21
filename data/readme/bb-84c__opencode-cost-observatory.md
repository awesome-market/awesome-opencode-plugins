# OpenCode Cost Observatory

Cost Observatory gives OpenCode users a local analytics view of token spend, model mix, and pricing coverage.
It keeps data on your machine while helping you understand where AI coding costs come from.

## Status and scope

- This repository is a source-only GitHub release.
- Current support target is Windows + PowerShell 7+.
- The tool reads a local OpenCode database and builds a local analytics database for dashboard use.
- Launcher integration with `opencode --usage` is optional and user-managed.

## Prerequisites

- Node 22+
- npm
- PowerShell 7+
- A local OpenCode installation with a readable OpenCode SQLite database

## Install dependencies

```powershell
npm ci
```

## Configuration

Create runtime config with either of these files:

- copy `.env.example` to `.env`
- or copy `dashboard.config.example.json` to `dashboard.config.json`

After copying, edit the file so `OPENCODE_DB_PATH` / `opencodeDbPath` point at your local OpenCode SQLite database.

The observatory uses two local stores:

- `ANALYTICS_DB_PATH` / `analyticsDbPath` for rebuildable analytics cache data
- `PRICING_DB_PATH` / `pricingDbPath` for durable pricing registry data

If the analytics DB is deleted, usage/session rollups can be rebuilt from the raw OpenCode DB. If the pricing DB is deleted, current pricing rows must be restored or re-seeded.

Use an absolute path for `PRICING_DB_PATH` / `pricingDbPath` when overriding the default. Values copied from `.env` or `dashboard.config.json` are not shell-expanded, so write `C:/Users/<your-user>/.local/share/opencode-cost-observatory/pricing.db` instead of `%USERPROFILE%/...`.

Pricing recovery precedence at backend startup is:

1. keep an existing durable pricing registry when active rows are present
2. otherwise migrate active legacy pricing rows from the analytics database
3. otherwise insert the built-in current effective pricing seed rows

Config precedence is:

1. process environment variables
2. `.env`
3. `dashboard.config.json`

For localhost auth, provide either:

- `DASHBOARD_TOKEN`
- or `DASHBOARD_TOKEN_FILE`

## Run the backend

```powershell
pwsh -File .\bootstrap.ps1 start
```

## Check backend status

```powershell
pwsh -File .\bootstrap.ps1 status
```

## Stop backend

```powershell
pwsh -File .\bootstrap.ps1 stop
```

## Run the frontend

```powershell
npm run dev
```

The default frontend URL is `http://127.0.0.1:41778`.

The browser UI is served separately from the backend during development.

## Build

```powershell
npm run build
```

Note: the current build only emits the client bundle.

## Typecheck

```powershell
npm run check
```

## Optional `opencode --usage` integration

This repository does **not** install or manage your personal `opencode` launcher.

If you want `opencode --usage` to start the observatory, create and maintain your own launcher file at a path appropriate for your local OpenCode installation, for example:

`C:\Users\<your-user>\.config\opencode\bin\opencode.cmd`

Minimal example:

```cmd
@echo off
if /I "%~1"=="--usage" (
  pwsh -NoProfile -NoLogo -File "<path-to-this-repo>\scripts\opencode-usage.ps1"
  exit /b %ERRORLEVEL%
)
call "<path-to-real-opencode.cmd>" %*
exit /b %ERRORLEVEL%
```

That launcher is outside the managed surface of this repo.

## Incremental usage sync and uploads

Raw OpenCode access is read-only. The first sync builds the analytics facts and
records a raw message rowid cursor in `sync_state`. Subsequent cycles seek new
rowids, reread a 1,024-rowid overlap, and look up unfinished assistant messages
by their primary keys. Messages without a positive `time.completed` remain in
`raw_sync_pending` until completion or deletion, regardless of their age.
Projects and sessions are read in full each cycle.

`SYNC_FULL_RECONCILE_INTERVAL_MS` sets the reconciliation interval (default
`86400000`, or 24 hours). A full pass also runs for missing/invalid cursors,
source identity/schema changes, cursor rollback, or a missing cursor anchor.
It repairs deleted facts and arbitrary edits to older completed messages.
Those repairs can lag by the reconciliation interval plus one sync cycle;
open-message updates normally arrive in the next cycle. Unchanged facts are
not rewritten or requeued during reconciliation.

Uploads use a durable `usage_upload_outbox`, not creation time, so late token
and cost updates are resent. Only the exact revisions accepted by ingest are
acknowledged. Concurrent changes stay queued, failed requests remain retryable,
and equal creation timestamps cannot skip rows at a batch boundary. The old
time watermark remains for status compatibility but no longer selects facts.
Local sync/uploader opens upgrade existing databases and queue historical facts
once to repair earlier missed updates. Server bootstrap and ingest do not create
pending/outbox tables or install their triggers. Expect one local historical replay.

The ingest request JSON format is unchanged. Successful ingest responses advertise
`factUpsert: "all-fields"`. The uploader stops without acknowledging revisions if
this capability is absent, including on an otherwise successful HTTP response.
Deploy upgraded ingest before restarting the uploader; older ingest code only
updates cost, not token counts. Raw deletions are reconciled locally only: the
existing ingest protocol has no deletion/tombstone operation.

Read-only upload validation and optional comparison with an online-safe VPS DB copy:

```powershell
node --import tsx uploader/ingest-preflight.ts --local <local-analytics-copy.db>
node --import tsx uploader/ingest-preflight.ts --local <local-analytics-copy.db> --vps <vps-analytics-copy.db>
```

Preflight shares the HTTP endpoint's validators, including JSON serialization of
non-finite numbers. It reports invalid message/session counts and invalid fields.
With `--vps`, it also reports differing/shared/local-only/VPS-only rows for both
tables and each token/cost aggregate delta (local minus VPS). Non-finite usage
values are counted and excluded from comparison sums. Both DBs open read-only;
preflight performs no migration, repair, upload or backup.

The Windows uploader is separate from `bootstrap.ps1` (the local dashboard):

```powershell
pwsh -NoProfile -File .\uploader.ps1 status
pwsh -NoProfile -File .\uploader.ps1 stop
pwsh -NoProfile -File .\uploader.ps1 start
pwsh -NoProfile -File .\uploader.ps1 logs
```

## Privacy and local data

- `.run/` contains local runtime state, logs, auth tokens, and the rebuildable analytics cache.
- The durable pricing registry lives outside `.run/` by default.
- Do not commit `.run/`, local databases, or local tokens.
- Browser auth is localhost-only and token-based.
