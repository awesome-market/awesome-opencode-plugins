# opencode-yourstatus

[![npm version](https://img.shields.io/npm/v/opencode-yourstatus.svg)](https://www.npmjs.com/package/opencode-yourstatus)
[![npm downloads](https://img.shields.io/npm/dt/opencode-yourstatus)](https://www.npmjs.com/package/opencode-yourstatus)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An [OpenCode](https://opencode.ai) TUI plugin that shows quota for the account selected in the current session directly in the right sidebar.

Based on [opencode-mystatus](https://github.com/vbgate/opencode-mystatus), with Google Antigravity support removed and xAI (SuperGrok) support added.

[简体中文](./README.zh-CN.md)

## Features

- Persistent quota display in OpenCode's right sidebar
- Follows the provider/model selected by the current session
- Reuses per-model quota cache while switching models
- Force-refreshes the response model after every completed response
- No slash command or model tool
- Remaining-quota meters and reset countdowns
- Chinese and English output
- API keys are masked when displayed

## Supported Providers

| Provider       | Account type            | Quota source                             |
| -------------- | ----------------------- | ---------------------------------------- |
| OpenAI         | Plus / Team / Pro OAuth | OpenCode `auth.json`                     |
| Zhipu AI       | Coding Plan API key     | OpenCode `auth.json`                     |
| Z.ai           | Coding Plan API key     | OpenCode `auth.json`                     |
| xAI            | SuperGrok OAuth         | OpenCode `auth.json`                     |
| GitHub Copilot | Individual / Business   | OpenCode `auth.json` or quota PAT config |

## Requirements

- OpenCode 1.18.0 or later
- Node.js 18 or later for local development
- A terminal wide enough for OpenCode's sidebar, or manually enable the sidebar from the command palette

## Install

Add the plugin to `~/.config/opencode/tui.json`:

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "plugin": ["opencode-yourstatus"]
}
```

Then fully quit and restart OpenCode. TUI plugins are loaded only during startup.

The plugin belongs in `tui.json`, not the `plugin` array in `opencode.json`. It does not register `/yourstatus` or an AI-callable tool.

### Custom auth path

OpenCode's standard auth path is detected automatically. To override it:

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "plugin": [["opencode-yourstatus", { "authPath": "/custom/path/auth.json" }]]
}
```

Custom auth files are read-only. The plugin never rotates provider credentials; OpenCode's own provider integration remains responsible for OAuth token refresh.

### Upgrade from 1.x

1. Remove `opencode-yourstatus` from the `plugin` array in `opencode.json`.
2. Remove the custom `yourstatus` command from `opencode.json` or the command directory.
3. Add `opencode-yourstatus` to the `plugin` array in `tui.json` as shown above.
4. Restart OpenCode.

## Usage

No plugin command is required. Select a supported model and the right sidebar follows it immediately. Previously fetched quota is shown from an in-memory per-model cache; a model without cached data is queried once.

The plugin force-refreshes and updates that cache when a model response finishes and the session becomes idle.

For unsupported providers, the sidebar shows a short unsupported message instead of querying every configured account.

## xAI Setup

The xAI integration displays the SuperGrok credit window and reset countdown returned by Grok. Sign in through OpenCode's built-in xAI Grok OAuth flow, then use an xAI model in the session.

xAI API keys cannot query SuperGrok subscription quota. The sidebar reports this limitation instead of making a misleading balance estimate.

## GitHub Copilot Setup

If OpenCode's Copilot OAuth token cannot access quota data, create `~/.config/opencode/copilot-quota-token.json` with a fine-grained GitHub PAT that has read-only `Plan` permission:

```json
{
  "token": "github_pat_xxx",
  "username": "your-github-username",
  "tier": "pro"
}
```

Valid tiers are `free`, `pro`, `pro+`, `business`, and `enterprise`.

## Security

The plugin reads provider credentials without modifying them and does not persist quota responses. OpenCode's own provider integrations remain responsible for OAuth token refresh.

Network requests are limited to provider quota endpoints:

- `https://chatgpt.com/backend-api/wham/usage`
- `https://bigmodel.cn/api/monitor/usage/quota/limit`
- `https://api.z.ai/api/monitor/usage/quota/limit`
- `https://grok.com/grok_api_v2.GrokBuildBilling/GetGrokCreditsConfig`
- `https://cli-chat-proxy.grok.com/v1/user`
- GitHub's official API endpoints used by the Copilot integration

## Development

```bash
npm install
npm run typecheck
npm run lint
npm test
```


## Credits

Forked and modified from [opencode-mystatus](https://github.com/vbgate/opencode-mystatus) by [vbgate](https://github.com/vbgate). Changes relative to upstream:

- Removed Google Antigravity support
- Added xAI (SuperGrok OAuth) quota display

## License

MIT
