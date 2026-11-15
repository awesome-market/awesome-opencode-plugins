# opencode-azure-entra-auth

[English](README.md) | [한국어](README_KO.md)

Keyless Microsoft Entra ID (Azure AD) authentication for [opencode](https://opencode.ai). This plugin authenticates Azure model endpoints with Azure CLI tokens instead of API keys, so no secret is ever written to disk. It works with any OpenAI-compatible Azure endpoint, and is verified against Azure AI Foundry and Azure Databricks model serving.

## Why

opencode stores provider API keys in `~/.local/share/opencode/auth.json` by default. In enterprise environments this is often undesirable, and some Azure resources disable key-based authentication entirely (`disableLocalAuth`). In those cases authentication must go through Microsoft Entra ID with role-based access control.

This plugin reuses your existing Azure CLI sign-in. It obtains a short-lived Entra token through `az account get-access-token`, injects it into every model request as a bearer token, caches the token in memory, and refreshes it shortly before expiry. No API key is stored, and access is governed by the RBAC roles assigned to your identity.

## Why Azure Databricks for Anthropic models

Azure offers Anthropic Claude models in more than one place, and the access path matters.

Azure AI Foundry serves Claude as a direct model, but it is billed through the Azure Marketplace. In subscriptions or regions where Marketplace purchases are restricted (for example tenants without Marketplace access, or regions where the offer is not available), the Foundry path to Claude is effectively blocked. Azure Databricks serves the same Claude family through its Foundation Model APIs without going through the Marketplace, so it remains usable where the Foundry Marketplace path is not.

This is why the examples pair the two providers: Foundry for GPT and other models, and Databricks for the Claude family as a Marketplace-independent route. The two paths are not identical in shape. Databricks serves Claude through an OpenAI-compatible interface (`/serving-endpoints`), whereas Foundry serves Claude through the Anthropic Messages API (`/anthropic/v1/messages`), not an OpenAI-compatible one. Both are still authenticated with Entra tokens, but they use different token resources and different opencode provider packages.

### Using Foundry direct Claude instead of Databricks

If your subscription has unrestricted Marketplace access, you can serve Claude from Foundry directly. According to the [Microsoft Learn documentation](https://learn.microsoft.com/azure/ai-foundry/foundry-models/how-to/use-foundry-models-claude), this path supports keyless Entra ID authentication, but differs from the GPT setup in two ways:

- **Token resource (audience):** `https://ai.azure.com` (not `https://cognitiveservices.azure.com`).
- **Endpoint and API:** base URL `https://<resource-name>.services.ai.azure.com/anthropic`, using the Anthropic Messages API rather than OpenAI Chat Completions. In opencode this means an Anthropic-style provider, not `@ai-sdk/openai-compatible`.

To use this path, add the provider to the plugin's `DEFAULT_PROVIDERS` map with `resource: "https://ai.azure.com"`, and configure the opencode provider against the `/anthropic` endpoint.

> **Not verified end to end.** This Foundry direct Claude configuration follows the Microsoft Learn documentation, but it was not run against a live deployment, because the subscription used for development has Marketplace billing disabled (which is the reason for the Databricks route in the first place). The Databricks and GPT paths in this README were verified against live endpoints; the Foundry direct Claude path is documentation-based only.

## How it works

The plugin installs a `fetch` wrapper on each configured provider at startup. The wrapper performs three tasks.

1. It attaches `Authorization: Bearer <token>` to every request, using the Entra token for that provider.
2. It caches the token and refreshes it five minutes before expiry, so long sessions never stall. The Azure CLI refreshes the underlying token silently, so unattended runs continue without intervention.
3. When the server returns 401 or 403, it forces a token refresh and retries the request once, which covers clock skew and early revocation.

Token injection is implemented as a `fetch` wrapper rather than a header hook because the wrapper can inspect the response status and retry on 401. The provider id is read from the runtime `input.provider.id` path.

## Requirements

1. Azure CLI installed and signed in. Use `az login` for interactive sessions, or `az login --service-principal ...` / a Managed Identity for unattended runs.
2. RBAC permission on the target resource.
   - Azure AI Foundry (AI Services): `Cognitive Services User`
   - Azure Databricks: workspace access with `CAN_USE` on the serving endpoint
3. A deployed model. Foundry needs a model deployment, Databricks needs a serving endpoint in the `READY` state.

## Install

This plugin is distributed as a local opencode plugin; it is not published to npm. opencode auto-loads any `.js`/`.ts` file placed in `~/.config/opencode/plugins/`, and because the only non-runtime dependency (`@opencode-ai/plugin`) is imported as a type and erased at runtime, the TypeScript source runs directly with no build step.

1. Copy `src/index.ts` from this repository into your plugins directory, for example `~/.config/opencode/plugins/azure-entra-auth.ts`.
2. Open the copied file and fill in the `DEFAULT_PROVIDERS` map near the top with your providers. Each key is an opencode provider id, and `resource` is the Azure AD token resource (audience) for that provider.

```ts
const DEFAULT_PROVIDERS: Record<string, ProviderAuthConfig> = {
  foundry: { resource: "https://cognitiveservices.azure.com", reasoningParamFix: true },
  databricks: { resource: "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d" },
}
```

The Databricks value `2ff814a6-3304-4ab8-85cb-cd0e6f879c1d` is the fixed global first-party application id for Azure Databricks, the same across every tenant. Unlike Foundry, whose token resource is an endpoint-style URL (`https://cognitiveservices.azure.com`), the Databricks token audience is this application id; both are valid `--resource` values for `az account get-access-token`. Set `reasoningParamFix: true` for a provider that serves Azure GPT-5 reasoning models (see [Configuration fields](#configuration-fields)).

## Configure providers

Register the providers themselves in `~/.config/opencode/opencode.json`. Both use the OpenAI-compatible interface, so they connect through `@ai-sdk/openai-compatible`. The `apiKey` field takes a dummy value; it is required for SDK initialization but is never used, since the plugin overrides the authorization header.

```jsonc
{
  "provider": {
    "foundry": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Azure AI Foundry (Entra)",
      "options": {
        "baseURL": "https://<resource-name>.cognitiveservices.azure.com/openai/v1",
        "apiKey": "entra-via-plugin"
      },
      "models": {
        "<deployment-name>": { "name": "GPT (Foundry)" }
      }
    },
    "databricks": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Azure Databricks (Entra)",
      "options": {
        "baseURL": "https://<workspace-name>.azuredatabricks.net/serving-endpoints",
        "apiKey": "entra-via-plugin"
      },
      "models": {
        "<serving-endpoint-name>": { "name": "Claude (Databricks)" }
      }
    }
  }
}
```

The baseURL path differs by provider. Foundry appends `/openai/v1` to the resource endpoint, and the model id is the deployment name. Databricks appends `/serving-endpoints` to the workspace host, and the model id is the serving endpoint name. A full example is in [examples/opencode.json](examples/opencode.json).

For Foundry open-weight models served through the Azure AI Model Inference endpoint, use the host form `https://<resource-name>.services.ai.azure.com/models` and add the provider to the plugin's `providers` map with the same `https://cognitiveservices.azure.com` resource.

### Foundry direct Claude (documentation-based, not verified)

To use Foundry's direct Claude instead of (or alongside) Databricks, add a separate provider for the Anthropic Messages endpoint. Add it to the plugin's `DEFAULT_PROVIDERS` with the `https://ai.azure.com` resource, and register it in `opencode.json` with an Anthropic-style provider package against the `/anthropic` endpoint:

```jsonc
{
  "provider": {
    "foundry-claude": {
      "npm": "@ai-sdk/anthropic",
      "name": "Azure AI Foundry Claude (Entra)",
      "options": {
        "baseURL": "https://<resource-name>.services.ai.azure.com/anthropic",
        "apiKey": "entra-via-plugin"
      },
      "models": {
        "<claude-deployment-name>": { "name": "Claude (Foundry)" }
      }
    }
  }
}
```

```ts
const DEFAULT_PROVIDERS: Record<string, ProviderAuthConfig> = {
  "foundry-claude": { resource: "https://ai.azure.com" },
}
```

As noted above, this path is based on the Microsoft Learn documentation and was not run against a live deployment. The exact opencode provider package and option names for the Anthropic-on-Azure endpoint may need adjustment in your environment.

## Configuration fields

Set these in the `DEFAULT_PROVIDERS` map inside the plugin file.

| Field | Type | Description |
| :--- | :--- | :--- |
| `<provider-id>` | key | An opencode provider id that matches a provider in your `opencode.json`. |
| `<provider-id>.resource` | `string` | Azure AD token resource (audience) for that provider. |
| `<provider-id>.reasoningParamFix` | `boolean` | Optional. Normalizes sampling params for Azure reasoning models that reject `max_tokens` and require temperature=1 (for example GPT-5.x on Foundry). Defaults to false. |

To override the Azure CLI executable (default `az`), edit the `azCommand` default in the plugin file.

## Token expiry and long-running sessions

Entra authentication has two kinds of expiry, and they behave differently.

The first is the AAD access token, which lives for roughly 60 to 90 minutes. The plugin refreshes it five minutes before expiry, and the Azure CLI renews the underlying token silently, so continuous sessions keep working without any user action. If a token is invalidated earlier than expected and the server returns 401 or 403, the plugin forces a refresh and retries once.

The second is the Azure CLI sign-in itself. When the refresh token expires, MFA is required again, or the token is revoked, `az account get-access-token` fails. The plugin then raises a clear message asking you to re-authenticate, and the request fails. In an interactive environment, running `az login` again restores it immediately.

For unattended operation, interactive `az login` is not suitable, so use one of the following. A service principal with a certificate (`az login --service-principal -u <appId> --tenant <tenantId> -p <cert.pem>`) renews tokens non-interactively; assign the service principal the appropriate RBAC role on the resource. A Managed Identity, when running on an Azure VM or container, lets the CLI obtain tokens through the instance metadata service with no credential management at all.

## Troubleshooting

- `Unauthorized` or `Credential was not sent`: the plugin did not load, or the RBAC role is missing. Run opencode with `--print-logs --log-level INFO` and confirm the plugin loaded and the provider id is correct.
- `'max_tokens' is not supported`: an Azure GPT-5 reasoning model rejected `max_tokens`. Set `reasoningParamFix: true` for that provider.
- Token fails to refresh: the Azure CLI sign-in expired. Run `az login` again, or switch to a service principal or Managed Identity for unattended runs.

## Development

The plugin runs directly from `src/index.ts` as a local plugin, so no build is required to use it. To type-check or produce a compiled `dist/` build:

```bash
bun install
bun run typecheck
bun run build
```

## License

MIT. See [LICENSE](LICENSE).
