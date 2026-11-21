# Opencode-Serper

[![CI](https://github.com/Jarvvski/opencode-serper/actions/workflows/ci.yml/badge.svg)](https://github.com/Jarvvski/opencode-serper/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

Serper web search and scraping for [OpenCode](https://opencode.ai). Registers
[Serper](https://serper.dev) as a `websearch` provider — so the built-in search
tool, and every agent that already uses it, search through Serper — and adds a
namespace of `serper.*` tools for the rest of Serper's endpoints.

**Status:** `0.1.0`, pre-1.0. Installed from Git; not yet published to npm.

## Quickstart

```sh
opencode plugin add github:Jarvvski/opencode-serper
```

Restart OpenCode, then run `/connect`, choose **Serper**, and paste your API key.
Serper is now the default web search provider: ask for current information and
the built-in `websearch` tool uses it.

That is the whole setup. Agents can additionally call the `serper.*` tools
(`news`, `scholar`, `places`, `images`, `autocomplete`, `scrape`) in Code Mode.

Installing the plugin makes Serper the default search provider. To keep another
provider and use only the `serper.*` tools, pass `options: { "setDefault": false }`
— see [configuration](docs/configuration.md#web-search-provider).

Full walkthrough, every tool, and troubleshooting:
**[docs/usage.md](docs/usage.md)**.

## Documentation

- [Usage](docs/usage.md) — install, connect, search, every tool, examples.
- [Configuration](docs/configuration.md) — key resolution, options, env, permissions.
- [Architecture](docs/architecture.md) — how the plugin registers and maps results.
- [ADRs](docs/adr/) — design decisions.
- [Changelog](CHANGELOG.md) — what has landed.

## Contributing

Project conventions and agent guidance live in [AGENTS.md](AGENTS.md)
([CLAUDE.md](CLAUDE.md) is a symlink to it).

## License

MIT. See [LICENSE](LICENSE).
