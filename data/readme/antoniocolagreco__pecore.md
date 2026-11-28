# <PE/CORE>

<PE/CORE> (Product Engineering Core) is a desktop software factory. It runs jobs made of agent, command and human steps on your repositories, with the coding agents you already use (Claude Code first) and your own subscriptions.

Status: in development. The design is in [docs/design.md](docs/design.md) and the UI in [docs/ui-design.md](docs/ui-design.md). Install and first-run instructions come with the first release.

## Build from source

Requirements: Linux, Node.js 22 or later, pnpm, git.

```sh
pnpm install
pnpm test
pnpm typecheck
pnpm lint
```

Tests run under Electron's Node, so `better-sqlite3` is built once, for Electron.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
