# opencode-typescript

[![Build](https://github.com/app/opencode-typescript/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/app/opencode-typescript/actions/workflows/build.yml)
[![Last build](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fapp%2Fopencode-typescript%2Fstatus%2Fstatus.json)](https://github.com/app/opencode-typescript/actions/workflows/build.yml)

A container image that runs [OpenCode](https://opencode.ai) for TypeScript
development. Nothing to install: one run command from your project directory
and the agent is working — the TUI opens inside the container.

## Quick start

From the project directory you want the agent to work in:

Podman:

```bash
podman run -it --rm --userns=keep-id:uid=1000,gid=1000 \
  -v "$PWD:/home/opencode/projects/$(basename "$PWD")" \
  -v opencode-state-$(id -un):/home/opencode/.local \
  --detach-keys="ctrl-],ctrl-q" \
  ghcr.io/app/opencode-typescript:latest
```

Docker (the same, with `--user` instead of `--userns`):

```bash
docker run -it --rm --user "$(id -u):$(id -g)" \
  -v "$PWD:/home/opencode/projects/$(basename "$PWD")" \
  -v opencode-state-$(id -un):/home/opencode/.local \
  --detach-keys="ctrl-],ctrl-q" \
  ghcr.io/app/opencode-typescript:latest
```

State (sessions, connected accounts) is kept in the per-user volume
`opencode-state-<user>`, so users of a shared machine do not share it. The
TUI opens on OpenCode's free built-in model — start typing, no key needed.
For other models, connect OpenRouter with the TUI's `/connect` command and
pick a model in the model picker. See [Installation](docs/installation.md).

## The image

- **Rolling latest.** GitHub Actions builds and publishes the image to GHCR on
  every push and on a schedule, always with the current upstream OpenCode and
  Node LTS versions. Tags: `latest`,
  `oc-<opencode-version>-node<node-version>`, `<YYYYMMDD>` — see
  [Updating](docs/updating.md).
- **TypeScript toolchain.** Current Node LTS via mise, TypeScript and the
  TypeScript language server, Prettier, pnpm/yarn, git and the usual agent
  tooling — see [Toolchain](docs/toolchain.md).
- **Non-root.** The agent never runs as root: on Podman it is the image's
  uid 1000 mapped onto your host user, on Docker your host UID, with a
  restricted sudo policy.

## Three kinds of users

- A human in the TUI — the image default, as in the quick start above.
- A human in the web UI — server mode plus the pairing flow.
- An external agent — server mode plus the HTTP API (Basic auth, username
  `opencode`).

Server mode is an explicit command
(`opencode serve --hostname 0.0.0.0 --port 4096`); see
[Usage](docs/usage.md) and [Access](docs/api.md). Running OpenCode in
Kubernetes: [Kubernetes](docs/kubernetes.md).

## Security and secrets

OpenCode runs unprivileged (uid 1000 mapped onto your host user on Podman,
your host UID on Docker) with a restricted sudo policy, so treat the
container as the security boundary. Secrets live only on the host or on the
`opencode-state-<user>` volume: the runtime env file, the calling environment, a
Kubernetes Secret, or a connected account. Nothing secret is baked into the
image; it ships a documented `.env.example` template, and a built-in agent
skill offers to copy it into the working folder when runtime variables are
missing. See [Security notes](docs/security.md).

## Documentation

| Document                                   | Contents                                                          |
| ------------------------------------------ | ----------------------------------------------------------------- |
| [Installation](docs/installation.md)       | Requirements, the first run, more models, the optional launcher   |
| [Usage](docs/usage.md)                     | Running the container, mounts, passing secrets, command overrides |
| [Access](docs/api.md)                      | TUI, web UI and the HTTP API for agents, Basic auth, OpenAPI      |
| [Kubernetes](docs/kubernetes.md)           | Deployment, Service and Secret examples for server mode           |
| [Toolchain](docs/toolchain.md)             | Installed tools, Node.js and mise, installing extra packages      |
| [Architecture](docs/architecture.md)       | Repository layout, the image, the GitHub Actions pipeline         |
| [Updating](docs/updating.md)               | How versions are resolved and how image releases work             |
| [Security notes](docs/security.md)         | Trust model and secret handling                                   |
| [Troubleshooting](docs/troubleshooting.md) | Common errors and fixes                                           |
