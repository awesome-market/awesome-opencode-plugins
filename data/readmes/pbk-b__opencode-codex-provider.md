# @zmide/opencode-codex-provider

[中文文档](./README.zh-CN.md)

A production-focused bridge for users who work across both `opencode` and Codex app-server.

It gives you a cleaner integration path between `opencode` and `ai-sdk-provider-codex-cli`, including:

- Provider option field mismatch (for example `reasoningEffort` / `reasoningSummary`)
- Tool name mismatch (`exec` vs `bash`)
- Inconsistent historical `tool-result` shapes during session resume
- Repeated approvals inside the workspace

## When to use

- You primarily operate in `opencode` but depend on Codex app-server models
- You want Codex integration through a published npm package without local wrapper maintenance
- You need fewer runtime surprises in tool calls, session resume, and workspace approvals

[![asciicast](https://asciinema.org/a/I8Gb8M5iMjXV7Glo.svg)](https://asciinema.org/a/I8Gb8M5iMjXV7Glo)

## Install

```bash
npm install @zmide/opencode-codex-provider
```

## Minimal config (recommended)

Point both `provider` and `plugin` to the same npm package:

```jsonc
{
  "plugin": ["@zmide/opencode-codex-provider"],
  "model": "codex-app-server/gpt-5.3-codex",
  "provider": {
    "codex-app-server": {
      "name": "Codex App Server",
      "npm": "@zmide/opencode-codex-provider",
      "models": {
        "gpt-5.3-codex": {
          "name": "gpt-5.3-codex",
          "options": {
            "approvalPolicy": "on-request",
            "sandboxPolicy": "workspace-write",
            "threadMode": "stateless",
            "minCodexVersion": "0.105.0",
            "effort": "medium",
            "codexPath": "/absolute/path/to/codex",
            "configOverrides": {
              "example_provider": "example-provider",
              "example_provider_feature_flag": false
            }
          }
        }
      }
    }
  }
}
```

Notes:

- Keep `plugin[]` and `provider.codex-app-server.npm` the same package.
- Set `model` to `provider-id/model-id`, and keep the entry under `provider.codex-app-server.models` keyed by the unprefixed model id.
- Replace `codexPath` and `configOverrides` with values for your environment.

## Quick verification

Verify Codex CLI first:

```bash
codex exec --ephemeral --skip-git-repo-check -m gpt-5.3-codex "Reply with exactly: same-model-ok"
```

Then verify `opencode` with the same prompt:

```bash
opencode run -m codex-app-server/gpt-5.3-codex "Reply with exactly: same-model-ok"
```


## What this package does

- Rewrites compatibility fields under `providerOptions["codex-app-server"]`
- Removes unsupported provider options before sending to base provider
- Normalizes tool names from `exec` to `bash` for generated and streaming outputs
- Normalizes provider-executed `tool-result` payloads
- Injects workspace-aware approval handlers
- Exports an `opencode` plugin to repair malformed historical tool parts

## Approval behavior (default)

- Command approvals are `acceptForSession` when `cwd` is inside the current workspace
- File-change approvals are `acceptForSession` when `grantRoot` is inside the current workspace
- Network approvals are `decline`
- Execution policy amendments are `decline`
- If your custom approval handlers return a decision, that decision wins

## More docs

- [Architecture](./docs/architecture.md)
- [Troubleshooting](./docs/troubleshooting.md)

## Development (maintainers)

```bash
npm run validate
```

This runs format, lint, typecheck, test coverage, and build.
