# opencode-qwen-auth

[![npm version](https://img.shields.io/npm/v/opencode-qwen-auth)](https://www.npmjs.com/package/opencode-qwen-auth)
[![npm downloads](https://img.shields.io/npm/dm/opencode-qwen-auth)](https://www.npmjs.com/package/opencode-qwen-auth)
[![license](https://img.shields.io/npm/l/opencode-qwen-auth)](./LICENSE)

> **Alpha software.** This plugin is early-stage and may have rough edges. Bug reports and feedback are welcome — please [open an issue](https://github.com/bad-noodles/opencode-qwen-auth/issues).

OpenCode plugin that authenticates with Qwen via OAuth — use your free [Qwen Code](https://qwen.ai) account instead of a paid API key.

> **Caution:** This plugin relies on the same OAuth flow as the official Qwen Code CLI. Alibaba could restrict third-party access at any time. Use at your own discretion.

## Prerequisites

- A free account at [qwen.ai](https://qwen.ai) (the same one used by the `qwen` CLI)
- No API key required

## Free Quota

The Qwen Code account provides a generous free quota for the `qwen3-coder-plus` model. Exact limits may vary by account.

## Setup

1. Add the plugin to your `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-qwen-auth"],
  "provider": {
    "qwen": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Qwen",
      "options": {
        "apiKey": "oauth"
      },
      "models": {
        "qwen3-coder-plus": {
          "name": "Qwen3 Coder Plus",
          "tool_call": true,
          "limit": { "context": 1000000, "output": 65536 }
        }
      }
    }
  }
}
```

2. Log in:

```sh
opencode auth login
```

Select **Qwen** as the provider, then **Login with Qwen account**. Your browser will open automatically — approve the request and you're done.

3. Select the model in OpenCode: `qwen / qwen3-coder-plus`

## How it works

The plugin implements the same device code + PKCE OAuth flow used by the official `qwen` CLI. On each API request it:

- Injects the Bearer token (auto-refreshed before expiry)
- Sets the `X-DashScope-AuthType: qwen-oauth` header required by the backend
- Resolves the base URL dynamically from the `resource_url` field in the token response
- Injects a system message if the request lacks one (required to access Qwen Code quota — see [`REVERSE_ENGINEERING.md`](./REVERSE_ENGINEERING.md))
- Retries token refresh with exponential backoff on transient failures
- Coordinates refresh token rotation across multiple concurrent opencode sessions via a sidecar file (`~/.local/share/opencode/qwen-refresh.json`)

## Updating

OpenCode does not auto-update plugins. To get the latest version:

```sh
rm -rf ~/.cache/opencode/node_modules/opencode-qwen-auth
opencode
```

## Troubleshooting

### "Refresh token expired or invalid. Please re-authenticate"

Your session has expired. Log in again:

```sh
opencode auth login
```

Select **Qwen** → **Login with Qwen account**.

### Getting a 429 / `insufficient_quota` error

This usually means the system message injection is not working. Ensure you are using the latest version of the plugin (see [Updating](#updating)).

### The browser didn't open during login

The URL is always shown in the terminal as a fallback — copy and paste it into your browser manually.

### The error only appears in one of several open opencode windows

This is a known cross-process token rotation issue. Closing and reopening the affected window usually resolves it. If it persists, re-authenticate as above.

## FAQ

**Does this work without a paid Qwen account?**
Yes. A free account at [qwen.ai](https://qwen.ai) is all you need.

**Is my API key or password stored anywhere?**
No. The plugin uses OAuth — only short-lived access tokens and refresh tokens are stored by OpenCode in `~/.local/share/opencode/auth.json`. Your password never touches this plugin.

**Which models are supported?**
`qwen3-coder-plus` is the recommended model and is confirmed to work. Other model IDs may return errors — see [`REVERSE_ENGINEERING.md`](./REVERSE_ENGINEERING.md) for details.

**Will this break if Alibaba updates the Qwen CLI?**
Possibly. The plugin reverse-engineers the OAuth flow used by the official `qwen` CLI. If Alibaba changes the flow or revokes third-party client IDs, the plugin will stop working until updated.

**Can I use this alongside a DashScope API key?**
Yes. The plugin also exposes an "Enter DashScope API Key manually" option in the auth flow.

## Reporting issues

Run the diagnostic script and include the output in your bug report:

```sh
curl -fsSL https://raw.githubusercontent.com/bad-noodles/opencode-qwen-auth/main/diagnose.sh | sh
```

Then [open an issue](https://github.com/bad-noodles/opencode-qwen-auth/issues/new?template=bug_report.md). See [CONTRIBUTING.md](./CONTRIBUTING.md) for more details.

## Local development

```sh
git clone https://github.com/bad-noodles/opencode-qwen-auth.git
```

Then point your config at the local path:

```json
{
  "plugin": ["file:///absolute/path/to/opencode-qwen-auth"]
}
```
