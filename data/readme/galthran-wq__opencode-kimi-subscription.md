# opencode-kimi-subscription

Use your Kimi Code subscription in OpenCode 2.

**TL;DR:** install, run `/connect`, pick **Kimi Code (subscription)**, approve in the browser, choose a Kimi model. Run `/kimi-usage` to check your quota.

## Install

Requires OpenCode 2.2.5+.

```sh
opencode plugin add github:galthran-wq/opencode-kimi-subscription
```

Or from a local checkout:

```sh
git clone https://github.com/galthran-wq/opencode-kimi-subscription ~/.config/opencode/plugins/kimi-subscription
cd ~/.config/opencode/plugins/kimi-subscription
npm install --ignore-scripts
```

Then add the absolute path to `~/.config/opencode/opencode.json`:

```json
{
  "plugins": ["/home/you/.config/opencode/plugins/kimi-subscription"]
}
```

## Usage

Sign in:

```
/connect → Kimi Code (subscription) → Sign in with Kimi (subscription)
```

or from the shell:

```sh
opencode auth login kimi-code --method device
```

Pick a model with `/models`:

| Model | Context |
| --- | --- |
| `k3` | 1M |
| `kimi-for-coding` | 256K |
| `kimi-for-coding-highspeed` | 256K |

The live list comes from Kimi's `/models` endpoint after sign-in and is cached for 6 hours.

Check quota:

```
/kimi-usage
```

```
Kimi subscription usage

5-hour limit
  Used: 12%
  Remaining: 88%
  Resets: 2026-11-14T15:00:00Z

Weekly limit
  Used: 41%
  Remaining: 59%
  Resets: 2026-11-17T00:00:00Z
```

This does not start a model turn and costs no tokens.

## What it does

- Kimi device-code OAuth; OpenCode Core exclusively refreshes, rotates, and persists credentials
- On a 401/403, resolves the current Core credential once more and retries only if its access token changed
- Credentials are always resolved for the active Core account, so switching accounts never reuses an old token
- `temperature` is pinned to `1`, the only value Kimi Code accepts

## Development

```sh
npm install --ignore-scripts
npm run typecheck
npm test
```

Tests mock every Kimi endpoint and never touch real credentials.

## Credits

Port of [t94j0/opencode-kimi-subscription](https://github.com/t94j0/opencode-kimi-subscription) to the OpenCode 2 plugin API.

## License

MIT
