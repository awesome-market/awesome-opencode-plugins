# OpenCode Usage Tracker

View provider account quotas, reset times, plans, and credits in OpenCode with `/usage`.

## Install

```sh
opencode plugin add opencode-usage-tracker
```

## Usage

1. Connect a supported provider with `/connect`.
2. Run `/usage` or select **Usage** in the command palette.
3. Choose a provider or **All Providers** when multiple providers are available.

- Press `h` in **All Providers** to show or hide providers with only errors.
- Press `Esc` to close.
- Reopen `/usage` to refresh the data.

Bars show **used** quota, not remaining quota. Reset timestamps use **UTC+8**.

## Supported providers

- Codex / ChatGPT
- Anthropic / Claude
- GitHub Copilot
- MiniMax Coding Plan
- Kimi for Coding
- Z.AI Coding Plan

Available data depends on your account and provider. Codex and Claude require
subscription OAuth connections; API keys do not expose their subscription quotas.
This is an account-quota viewer, not a session token counter or billing dashboard.

## Screenshot

![Historical Usage Tracker dialog showing Codex and GitHub Copilot quotas](docs/images/sample.png)

Historical provider-card layout; current usage bars and colors differ.

## License

MIT
