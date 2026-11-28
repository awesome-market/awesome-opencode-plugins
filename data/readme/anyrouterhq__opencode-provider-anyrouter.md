# opencode-provider-anyrouter

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Official [AnyRouter](https://anyrouter.dev) provider for
[OpenCode](https://opencode.ai). One `sk-ar-v1-` key reaches every model in the
catalog, with routing and failover handled by AnyRouter.

The only valid AnyRouter domain is `https://anyrouter.dev` (short link
`https://anyr.dev` for social posts). Any other domain using the AnyRouter name
is not affiliated with this project.

## Install

Add the provider to `~/.config/opencode/opencode.json` (all projects) or
`./opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "anyrouter": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "AnyRouter",
      "options": {
        "baseURL": "https://anyrouter.dev/api/v1",
        "apiKey": "{env:ANYROUTER_API_KEY}"
      }
    }
  }
}
```

Then export your key and start OpenCode:

```bash
export ANYROUTER_API_KEY="sk-ar-v1-..."
opencode
```

Pick a model with `/models`, or pass one directly. Model ids are `provider/model`
from the catalog, for example `anyrouter/free` for the best free model at that
moment.

## Verify the config

```bash
npm install
npm test
```

The test fails if the base URL is not `https://anyrouter.dev/api/v1`, so a
forked config cannot silently point at another host.

## Notes

- Free models are `$0` per token on Go and up, with no daily cap. The Free plan
  gets a 5-request trial.
- Bring-your-own-key routes through your own provider keys at `$0` markup.
- The Anthropic Messages endpoint, for tools that speak it, is
  `https://anyrouter.dev/api`.
