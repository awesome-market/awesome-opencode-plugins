# @juanbenjumea/pi-provider-usage-fetcher

Shared **provider usage** library for Pi extensions, agentq, and other tooling.

Despite the name (historical), this package covers more than OpenCode Go:

| Provider | Auth | Source |
|---|---|---|
| **OpenCode Go** | API key (same as chat) | `GET https://opencode.ai/zen/go/v1/usage` |
| **Claude** | macOS keychain, `auth.json`, explicit apiKey | `GET https://api.anthropic.com/api/oauth/usage` |
| **Codex** | `auth.json`, `~/.codex/auth.json`, explicit apiKey | `GET https://chatgpt.com/backend-api/wham/usage` |
| **ClinePass** | `CLINE_API_KEY`, `auth.json`, explicit apiKey | `api.cline.bot/api/v1/*` |
| **Umans** | `UMANS_API_KEY`, `auth.json`, explicit apiKey | `GET https://api.code.umans.ai/v1/usage` |
| **Copilot** | `auth.json` (`github-copilot`), explicit apiKey | `GET https://api.github.com/copilot_internal/user` |
| **Gemini** | `auth.json`, `~/.gemini/oauth_creds.json`, explicit apiKey | `POST https://cloudcode-pa.googleapis.com/v1internal:retrieveUserQuota` |
| **Kimi Coding** | `KIMI_API_KEY`, `auth.json`, explicit apiKey | `GET https://api.kimi.com/coding/v1/usages` |
| **Synthetic** | `SYNTHETIC_API_KEY`, `auth.json`, explicit apiKey | `GET https://api.synthetic.new/v2/quotas` |
| **z.ai / GLM** | Region-specific environment key, `auth.json`, explicit apiKey | `GET {api.z.ai or open.bigmodel.cn}/api/monitor/usage/quota/limit` |
| **Grok / SuperGrok** | `GROK_OAUTH_TOKEN`, `GROK_ACCESS_TOKEN`, `auth.json` (`grok`), or `~/.grok/auth.json` | Grok CLI billing proxy (`cli-chat-proxy.grok.com/v1/billing?format=credits`) |
| **Mistral** | API key (`auth.json`, `MISTRAL_API_KEY`), or `quota-sessions.json` (`mistral.cookie`) | `GET https://api.mistral.ai/v1/billing/budget` |
| **Cursor** | `quota-sessions.json`, env, CodexBar, Cursor app DB | `cursor.com/api/usage-summary` |
| **CommandCode** | `quota-sessions.json`, env, CodexBar | `api.commandcode.ai/internal/billing/*` |
| **Openference** | API key from caller, `OPENFERENCE_API_KEY`, or `auth.json` | `GET https://openference.com/api/user/me` |

Legacy OpenCode Go dashboard cookie scraping remains as a fallback when no API key is configured.

Grok reports **subscription credits**, not xAI API spend. Its quota adapter follows the Grok CLI billing route observed in CodexBar; this is a private CLI endpoint and may change. It does not use xAI inference API keys or xAI Management API spend endpoints.

## Install

```bash
npm install @juanbenjumea/pi-provider-usage-fetcher
```

Monorepo consumers: `"@juanbenjumea/pi-provider-usage-fetcher": "file:../opencode-go-usage"`.

## Unified Dispatch

```ts
import { detectProvider, fetchProviderUsage, fetchAllProviderUsage } from "@juanbenjumea/pi-provider-usage-fetcher";

// Automatically detects alias ("anthropic", "github-copilot", "opencode", etc.)
const canonical = detectProvider("anthropic"); // "claude"

// Fetches and normalizes quota snapshot across any supported provider
const snapshot = await fetchProviderUsage("anthropic", { apiKey: "..." });
// { provider: "Claude", windows: [ { label: "5h", usedPercent: 45, resetsIn: "1h30m" }, ... ], fetchedAt }

// Or collect several providers concurrently; unknown providers are omitted.
const snapshots = await fetchAllProviderUsage(["anthropic", "openai-codex", "cursor"]);
```

## OpenCode Go (API-first)

```ts
import { fetchUsageApi } from "@juanbenjumea/pi-provider-usage-fetcher";

const usage = await fetchUsageApi(process.env.OPENCODE_GO_KEY!);
// { rolling, weekly, monthly, error? }
```

## Cursor / CommandCode

```ts
import { fetchCursorUsage } from "@juanbenjumea/pi-provider-usage-fetcher/cursor.ts";
import { fetchCommandCodeUsage } from "@juanbenjumea/pi-provider-usage-fetcher/commandcode.ts";
import { fetchOpenferenceUsage } from "@juanbenjumea/pi-provider-usage-fetcher/openference.ts";

// Footer labels (Plan / Auto / API)
await fetchCursorUsage();

// agentq labels (total / auto-composer / api-models)
await fetchCursorUsage({ labelStyle: "agentq" });

await fetchCommandCodeUsage();

// Uses the dashboard profile endpoint (openference.com/api/user/me), which the
// inference API key authenticates via Bearer. window = usage.windowQuotaUsed /
// plan.requestsPerWindow, week = usage.weekQuotaUsed / plan.requestsPerWeek.
const openference = await fetchOpenferenceUsage(process.env.OPENFERENCE_API_KEY);
```

Auth resolution order: provider-specific explicit key → environment variable → `auth.json` credential. For Cursor and CommandCode cookies, the existing order is `quota-sessions.json` → env vars → legacy `auth.json` cookies → CodexBar manual cookies → (Cursor only) desktop app token. Mistral prefers its API key and falls back to `quota-sessions.json`.

## Mistral

Mistral reports the monthly allowances as percentages, not as an API spend report:

```ts
import { fetchMistralUsage } from "@juanbenjumea/pi-provider-usage-fetcher/mistral.ts";

const snapshot = await fetchMistralUsage();
// { provider: "Mistral", windows: [
//     { label: "Month", usedPercent: 40, resetsAt, resetsIn, resetDescription: "\u20ac20.00 / \u20ac50.00 \u00b7 \u20ac30.00 left" },
//     { label: "Vibe", usedPercent: 12.5, resetsAt, resetsIn, resetDescription: "..." },
//   ], fetchedAt }
```

`Month` is the API allowance (`api_budget`) and `Vibe` is the Vibe Code allowance (`vibe_budget`). Each window carries the allowance's own reset date and a used / total / remaining description. When Mistral reports no allowance for the account the fetcher returns `windows: []` with `error: "allowance-not-exposed"`; it never invents a 0% window.

### With an API key (preferred)

The API key comes from `options.apiKey`, then `MISTRAL_API_KEY`, then the `mistral` entry in `auth.json`. It reads:

- `GET https://api.mistral.ai/v1/billing/budget` — `api_budget` and `vibe_budget`, each with `usage_percentage`, `initial_budget`, `currency`, `reset_at`

### With a browser session (fallback)

If no API key is configured, or the key is rejected, the fetcher reads the same budgets out of the admin subscription page with the browser session. Configure it in the pi agent dir (`~/.pi/agent/quota-sessions.json`, or the file named by `PI_QUOTA_SESSIONS_FILE`):

```json
{
  "mistral": {
    "cookie": "<Cookie header copied from an authenticated admin.mistral.ai request>"
  }
}
```

Copy the whole `Cookie` request header from the browser devtools on `https://admin.mistral.ai/`, not a single cookie. The value is a credential: it is only ever sent as a request header, and is never logged or returned in a snapshot or error.

- `GET https://admin.mistral.ai/subscription` — the page embeds `budget: { api_budget, vibe_budget }` in its React Server Component flight data

`admin.mistral.ai` is behind Cloudflare, so the request presents a browser user agent to match the `cf_clearance` cookie; a challenge response is reported as an error rather than bypassed. An expired session is answered with a redirect to `auth.mistral.ai` and is reported as `HTTP 401`.

Background and source links for both paths: [`docs/mistral-usage-research.md`](docs/mistral-usage-research.md).

## Consumers

- `@juanbenjumea/pi-dynamic-footer` — subscription quota bars
- `@juanbenjumea/pi-multi-opencode-go` — failover usage polling
- **agentq** — `data/quota.json` collector

## Package rename

This package is published as `@juanbenjumea/pi-provider-usage-fetcher`. Existing consumers of the former `@juanbenjumea/opencode-go-usage` npm package must switch their dependency and imports when adopting this package; the old package identity remains separate.
