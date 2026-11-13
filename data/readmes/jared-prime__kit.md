[![Build](https://github.com/Jared-Prime/kit/actions/workflows/buildx.yaml/badge.svg)](https://github.com/Jared-Prime/kit/actions/workflows/buildx.yaml)
[![release](https://github.com/Jared-Prime/kit/actions/workflows/release.yml/badge.svg)](https://github.com/Jared-Prime/kit/actions/workflows/release.yml)

A collection of Docker Sandbox Kit (v3) workflows and mixins.

## Quickstart

Each harness — Claude Code, Codex, and opencode — publishes as a single, ready-to-run OCI image, so you don't need to compose kits by hand to get started:

```shell
sbx run 'ghcr.io/jared-prime/kit/sandbox/anthropic:latest'
```

```shell
sbx run 'ghcr.io/jared-prime/kit/sandbox/openai:latest'
```

```shell
sbx run 'ghcr.io/jared-prime/kit/sandbox/anomaly:latest'
```

| harness     | image                                       |
|-------------|---------------------------------------------|
| Claude Code | `ghcr.io/jared-prime/kit/sandbox/anthropic` |
| Codex       | `ghcr.io/jared-prime/kit/sandbox/openai`    |
| opencode    | `ghcr.io/jared-prime/kit/sandbox/anomaly`   |

## Images and Tags

Every image is built for `linux/amd64` and `linux/arm64`, scanned with Trivy, and published by the [build](.github/workflows/build.yaml) and [release](.github/workflows/release.yml) workflows.

Images are published under `ghcr.io/jared-prime/` with these tags:

| image                                         | contents                                  | tags                              | published          |
| --------------------------------------------- | ----------------------------------------- | --------------------------------- | ------------------ |
| `kit/sandbox/anthropic`, `openai`, `anomaly`  | the ready-to-run harness (use these)      | `<sha>`, `<version>` and `latest` | on release         |
| `kit/workload/anthropic`, `openai`, `anomaly` | the workload kit for each harness         | `<sha>` and `latest`              | every `main` build |
| `kit/skills`                                  | the agent skills mixin (add with `--kit`) | `<sha>` and `latest`              | every `main` build |
| `kit/playwright`                              | the Playwright mixin (add with `--kit`)   | `<sha>` and `latest`              | every `main` build |
| `kit`                                         | the shared tools only                     | `<sha>` and `latest`              | every `main` build |

`<sha>` is the full commit SHA and `<version>` is the release version without a `v` prefix, for example `3.0.0`.
The ready-to-run `kit/sandbox/*` images compose a workload with the `kit/skills` and `kit/playwright` mixins.
Merging to `main` publishes the intermediate images (`kit`, `kit/skills`, `kit/playwright`, `kit/workload/*`). When release-please cuts a release, the release workflow builds the sandbox images from that commit's intermediate images and tags them `<sha>`, `<version>` and `latest`.

## Development

Use the local directory while developing and testing

```shell
sbx run './anthropic' \
  --kit './skills' \
  --kit './playwright'
```

### The `tools` build arg

Each workload kit and the `playwright` mixin build on the shared tools image through a `tools` build arg, which defaults to `ghcr.io/jared-prime/kit:latest`.
CI always passes `tools=<registry>/kit:<sha>`, and the release sandbox references the workload images built for that same SHA, so a release is pinned to its matching tools build.
A manual build that omits `--build-arg tools=...` resolves `kit:latest`, the most recent `main` build, which can differ from what CI would build (and only exists once `main` has pushed it).
To reproduce a specific build, pass the commit explicitly; the `just workload` recipe does this with the current commit:

```shell
docker buildx build -f anthropic/anthropic.yaml \
  --build-arg tools=ghcr.io/jared-prime/kit:<commit> ./anthropic
```

## Skills

Load individual skills to share among agents

```shell
sbx agents add jared-prime/kit --skill guided-review
```

## Playwright

The `playwright` mixin adds `playwright-cli` and a headless Chromium so agents can browse and test web pages:

```shell
sbx run './anthropic' --kit './playwright'
```

- The browser is Alpine's system Chromium (from the upstream Alpine `community` repository), preconfigured through `PLAYWRIGHT_MCP_*` environment variables.
  Playwright's bundled browsers are glibc builds and do not run on this Alpine image, so do not run `playwright-cli install` to download browsers.
- The browser only loads hosts the sandbox network policy allows.
  A blocked host answers `403 Forbidden` with an `Approval required for <host>:443` message; review pending requests on the host with `sbx policy approval ls`.
- The sandbox proxy intercepts TLS. At agent start, an entrypoint hook imports the proxy CA into Chromium's NSS database (`~/.pki/nssdb`), because Chromium ignores `SSL_CERT_FILE`.
- The mixin also installs the `playwright-cli` agent skill.

## Credentials

The Claude Code and Codex workloads declare an optional host credential.
When bound, the token stays on the host; the sandbox only sees sentinels, and the proxy substitutes the real token.
Sandboxes created afterwards start signed in.

| harness     | token on the host                                        | token in the sandbox only                                                            |
|-------------|----------------------------------------------------------|--------------------------------------------------------------------------------------|
| Claude Code | `/login` once; the proxy captures it                     | decline the `anthropic` credential prompt, then `/login` per sandbox                 |
| Codex       | `sbx secret set -g openai --oauth` (browser on the host) | decline the `openai` credential prompt, then `codex login --device-auth` per sandbox |
| opencode    | not supported                                            | LM Studio takes no login; for OpenCode Zen, sign in per sandbox                      |

To keep a token in the sandbox only, also leave the service unset on the host (`sbx secret ls`).
If you approved the credential before, remove its entry from `~/.config/sbx/credentials.yaml`.
Each harness README shows how to check which token the sandbox holds.

OpenCode Zen models (e.g. `opencode/big-pickle`) need a Zen API key.
`sbx` has no service for it, so the key can only live in the sandbox:
sign in with opencode's login, choose OpenCode Zen, and paste the key in each new sandbox.

All three workloads read the GitHub MCP server's token from the host

```shell
sbx secret set github
```

## Network Policies

A Docker Sandbox applies network access control at two layers:

1. the kit `network-policy` capability declaration
2. the global policy active on the host running `sbx`

One of three presets declare the host policy:

- **open**: all outbound traffic allowed without restriction
- **balanced**: a baseline allowlist covers common development tooling
- **closed**: no baseline allowlist; only kit or user-declared allow rules permitted

A **balanced** policy ships by default.

Allow policies are additive; deny policies are blocking.

### Organization Management

An organization with a paid subscription manages [governance permissions](https://docs.docker.com/ai/sandboxes/governance/access-controls/organization/).
When active, the managed policy replaces the local `sbx` policy entirely.
A kit's `network-policy.allow` declarations and any local machine policies will no longer evaluate.
