# opencode-anthropic-auth-community

> Community-maintained Anthropic Claude Pro/Max OAuth plugin for [opencode](https://github.com/anomalyco/opencode).

The official `opencode-anthropic-auth` package was removed from npm following a legal request from Anthropic. This is a community fork to keep the functionality alive.

> **Disclaimer:** Using this plugin may violate Anthropic's Terms of Service. Use at your own risk.

---

## Installation

Add the plugin to your `opencode.json`:

```json
{
  "plugin": ["@thehugeman/opencode-anthropic-auth-community@latest"]
}
```

That's it. No custom binary, no fork of opencode — works with the standard installed `opencode` CLI.

---

## Usage

1. Run `opencode`
2. Go to **Providers** → **Login** → **Anthropic**
3. Select **Claude Pro/Max**
4. A browser URL will open — authorize it, then paste the code back into the terminal
5. Done — your Claude Pro/Max subscription is now used by opencode at no extra API cost

---

## Optional: Full system prompt

If you're on opencode `>= 1.2.27`, you can add the original Anthropic session prompt by creating an `anthropic-prompt.txt` file in your opencode plugins directory:

```
~/.config/opencode/plugins/anthropic-prompt.txt
```

Contents from the [original prompt](https://github.com/anomalyco/opencode/blob/8e09e8c6121f03244a1f25281b506a90bcb355d7/packages/opencode/src/session/prompt/anthropic-20250930.txt).

---

## How it works

The plugin intercepts Anthropic API requests and:
- Handles OAuth PKCE flow via `claude.ai`
- Injects the required `oauth-2025-04-20` beta header
- Handles token refresh automatically
- Prefixes tool names with `mcp_` (required by the OAuth API path)
- Strips the prefix back from streaming responses
- Computes the required billing header

---

## Contributing

PRs welcome. If the plugin breaks (Anthropic can change their OAuth flow at any time), open an issue or submit a fix.

---

## License

MIT
