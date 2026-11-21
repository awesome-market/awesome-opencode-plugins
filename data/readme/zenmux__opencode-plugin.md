# ZenMux OAuth for OpenCode

Use [ZenMux](https://zenmux.ai) models in [OpenCode](https://opencode.ai) with OAuth 2.0 Authorization Code + PKCE. The plugin adds browser login, automatic refresh-token rotation, dynamic model discovery, and an offline model cache.

## Install

Add the npm package to your OpenCode configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["@zenmux/opencode-oauth"]
}
```

Then sign in:

```bash
opencode auth login -p zenmux -m "ZenMux OAuth (PKCE)"
```

You can also run `/connect` inside OpenCode, select **ZenMux**, and choose **ZenMux OAuth (PKCE)**. After authorization, run `/models` and select a `zenmux` model.

## How it works

- Production uses one bundled native public OAuth client ID. Public clients do not contain a client secret.
- Authorization uses PKCE with `S256` and an ephemeral loopback callback on `127.0.0.1`; after validation, the callback renders `https://zenmux.ai/platform/oauth-completed?client=opencode` in a full-screen iframe.
- OpenCode stores the access and refresh tokens in its own credential store.
- The plugin refreshes access tokens shortly before expiry, persists the rotated token pair, and injects the access token as a Bearer token.
- The model catalog is mapped per model to Anthropic Messages, OpenAI Responses, or Chat Completions according to the endpoint adapters advertised by ZenMux.
- The last non-empty model catalog is cached at `~/.cache/opencode/zenmux/models.json`. A failed or empty refresh does not overwrite a valid cache.

The package requests only these scopes:

- `inference:invoke`
- `offline_access`

## Configuration

Production works without additional configuration. These environment variables are available for development and self-hosted testing:

| Variable | Default | Purpose |
| --- | --- | --- |
| `ZENMUX_OAUTH_ORIGIN` | `https://zenmux.ai` | OAuth authorization server origin |
| `ZENMUX_API_BASE_URL` | `https://zenmux.ai/api/v1` | OpenAI-compatible API base URL |
| `ZENMUX_ANTHROPIC_BASE_URL` | `https://zenmux.ai/api/anthropic/v1` | Anthropic-compatible API base URL |
| `ZENMUX_MODEL_CATALOG_URL` | `https://zenmux.ai/api/frontend/model/available/list` | Rich model catalog URL |
| `ZENMUX_OAUTH_CLIENT_ID` | bundled for production | Override the public client ID |

Non-production origins register a native public client on first use and cache its client ID in the OpenCode configuration directory. Existing production client-ID caches remain supported so previously issued refresh tokens continue to work.

## Development

```bash
npm test
npm pack --dry-run
```

To load the source as a project-local plugin while developing, create `.opencode/plugins/zenmux-oauth.js` containing:

```js
export { ZenMuxOAuthPlugin } from "../../index.mjs"
```

## Compatibility

This release targets the stable OpenCode V1 plugin API. OpenCode V2 currently uses a separate beta plugin API and requires a dedicated entry point.

## License

MIT
