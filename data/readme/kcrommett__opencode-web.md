> **DEPRECATED:** This project has been archived and is no longer maintained.
> Use the replacement project: [shuvcode](https://github.com/Latitudes-Dev/shuvcode) | [shuv.ai](https://shuv.ai)

> **Note:** This is an independent, community-maintained project created by
> fans of OpenCode. It is not affiliated with SST Corp. or the official
> OpenCode project. For the official OpenCode CLI, visit [opencode.ai](https://opencode.ai).

<p align="center">
  <a href="https://opencode.ai">
    <picture>
      <source srcset="assets/logo-ornate-dark.svg" media="(prefers-color-scheme: dark)">
      <source srcset="assets/logo-ornate-light.svg" media="(prefers-color-scheme: light)">
      <img src="assets/logo-ornate-light.svg" alt="OpenCode logo">
    </picture>
  </a>
  <br>
  (web)
</p>

<p align="center">OC Web - the browser interface for OpenCode sessions.</p>

<p align="center">
  <a href="https://www.npmjs.com/package/opencode-web"><img alt="npm" src="https://img.shields.io/npm/v/opencode-web?style=flat-square" /></a>
  <a href="https://github.com/kcrommett/opencode-web/actions/workflows/release.yml"><img alt="Release" src="https://img.shields.io/github/actions/workflow/status/kcrommett/opencode-web/release.yml?style=flat-square&label=release" /></a>
</p>

OC Web is a TanStack Start, React, and Bun app for managing OpenCode Server
sessions from a browser. It provides mobile-friendly session continuation, live
SSE timelines, command execution output, file preview, theme switching, and
OpenCode model/agent controls.

## Quick Start

```bash
# Latest stable release
bunx opencode-web@latest

# Dev release
bunx opencode-web@dev
```

Then open [http://localhost:3000](http://localhost:3000).

Other install paths:

```bash
bun add -g opencode-web
opencode-web

npm install -g opencode-web
opencode-web

curl -sSL https://raw.githubusercontent.com/kcrommett/opencode-web/main/install.sh | bash
```

Use `--external-server <url>` to connect to an existing OpenCode Server:

```bash
opencode-web --external-server http://10.0.0.200:4096 --host 0.0.0.0 -p 8080
```

Full CLI options, environment variables, and Windows notes are in
[Usage](docs/USAGE.md).

## Screenshots

### Mobile-first responsive design

![Mobile welcome screen](docs/screenshots/IMG_7456.jpg)
![Mobile session with token usage](docs/screenshots/IMG_7457.jpg)

### Session continuation and live timeline

![New session walkthrough](docs/screenshots/session-new.png)
![Session timeline with history](docs/screenshots/session-history.png)

### Command deck, model picker, and file preview

![Agent picker modal](docs/screenshots/picker-session.png)
![Model picker details](docs/screenshots/picker-model.png)
![File browser with syntax highlighting](docs/screenshots/file-browser.png)

### Mobile command execution and theme gallery

![Command execution output](docs/screenshots/IMG_7458.jpg)
![OpenCode theme](docs/screenshots/theme-opencode.png)
![Dracula theme](docs/screenshots/theme-dracula.png)
![Tokyo Night theme](docs/screenshots/theme-tokyonight.png)

More screenshots are in [`docs/screenshots/`](docs/screenshots/).

## Features

- Browser access to OpenCode sessions without installing a separate desktop UI.
- Real-time monitoring through Server-Sent Events.
- Mobile-first PWA layout for phones, tablets, and second screens.
- Keyboard-driven leader key navigation.
- Session continuation with history, context, and active task state.
- Shell command output panels with copy support.
- Model, theme, agent, MCP, and LSP status surfaces.
- File browser with markdown, syntax-highlighted text, and image previews.

## Architecture

- TanStack Start and React Router provide hybrid SSR/CSR routing.
- `server.ts` serves the production bundle and proxies OpenCode API traffic.
- `src/lib/` wraps the OpenCode HTTP API and shared client behavior.
- `src/app/_components/` contains message renderers, command controls, pickers,
  dialogs, and UI primitives.

Browser access to the OpenCode server must go through the web app. The frontend
does not directly connect to the OpenCode API; requests flow through `/api/*`
proxy endpoints for compatibility with external server configurations.

## Local Development

```bash
bun install
bun run dev
bun run build
bun run lint
bun x tsc --noEmit
```

The app listens on [http://localhost:3000](http://localhost:3000) by default.
Set `OPENCODE_SERVER_URL` or pass `--external-server` to point at an existing
OpenCode Server. Development, build, release-channel, and project-structure
details are in [Development](docs/DEVELOPMENT.md).

## Deployment and Security

OC Web is designed for local development and does not include built-in
authentication. Do not expose it directly to the internet. Use Cloudflare
Access, a VPN, or an authenticated reverse proxy for remote access.

Production serving, reverse proxy notes, Windows build troubleshooting, and
environment migration guidance are in [Deployment](docs/DEPLOYMENT.md).

## Documentation

| Topic                                               | Link                                                                       |
| --------------------------------------------------- | -------------------------------------------------------------------------- |
| Usage, CLI flags, and environment variables         | [docs/USAGE.md](docs/USAGE.md)                                             |
| Production, Windows, reverse proxies, and migration | [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)                                   |
| Development workflow and project structure          | [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)                                 |
| Configuration samples                               | [docs/config-samples/](docs/config-samples/)                               |
| API endpoints                                       | [docs/API-ENDPOINTS-DOCUMENTATION.md](docs/API-ENDPOINTS-DOCUMENTATION.md) |
| SSE events                                          | [docs/SSE-EVENTS-DOCUMENTATION.md](docs/SSE-EVENTS-DOCUMENTATION.md)       |
| MCP status usage                                    | [docs/MCP_STATUS_USAGE.md](docs/MCP_STATUS_USAGE.md)                       |

## Contributing

Follow [AGENTS.md](AGENTS.md). Before opening a PR, run lint and typecheck,
describe UI-visible changes, and flag server-function updates.
