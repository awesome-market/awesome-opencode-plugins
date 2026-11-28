# Agentry for OpenCode

Agentry brings QuickAgents into your agent host. Search a registry, read a QuickAgent's capability contract, scan findings and signature, install it, and run it in Agentry's sandboxed runner with a preview you approve first. Build your own QuickAgent, validate it, get an AI Review and test it before you publish. The plugin drives the Agentry CLI on your computer; the CLI keeps your sign-in and enforces each QuickAgent's contract.

## Install

```sh
opencode plugin add github:blaktron/agentry-plugin-opencode
```

This needs OpenCode v2. The plugin adds the `agentry` MCP server and the
`agentry` skill while it is enabled; a server or skill you configured under the
same name is kept. For the slash commands, copy the files in `commands/` into
`.opencode/commands/` (or `~/.config/opencode/commands/`).

## Requirements

- The Agentry CLI 0.6.63 or newer on `PATH`. Install it from https://secureagentry.net/download.
- Node 24 or newer on `PATH`.
- Docker, for runs on this computer.

Signing in stays in your terminal (`agentry login`). Documentation: https://docs.secureagentry.net/agentry/mcp/.
Privacy: https://secureagentry.net/privacy.
