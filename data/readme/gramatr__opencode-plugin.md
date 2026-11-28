<p align="center">
  <img alt="grāmatr" src="https://gramatr.com/brand/g-dark-sq.png" width="128" height="128">
</p>

# @gramatr/opencode-plugin

grāmatr lifecycle plugin for [OpenCode](https://opencode.ai). Maps OpenCode's
plugin events (`session.created`, `message.updated`, `tool.execute.before`,
`session.idle`, `session.compacted`) to grāmatr hooks — pre-classifying every
prompt through the remote MCP server at `api.gramatr.com/mcp`, restoring
session continuity on start, and enforcing git-gate hard rules before
destructive shell commands run. Same intelligent context engineering layer
used across Claude Code, ChatGPT, Cursor, Codex, and Gemini.

## What you get

- **Cheaper, faster prompts.** A multi-head classification pipeline pre-routes
  each request and replaces the tens-of-thousands-token system prompt you'd
  otherwise hand-maintain. The effect compounds the longer you work.
- **Consistent behavior across sessions.** The same contract — directives plus
  quality gates — runs on every prompt, so your AI acts the same on session
  200 as on session 1.
- **Continuity across tools.** A session you start in OpenCode resumes
  cleanly in Claude Code, Cursor, or the web — the handoff is persisted by
  the same backend.
- **Auditable safety rails.** Per-prompt hard gates (e.g. `git push --force`
  to `main` is blocked locally before the tool runs).

## Install

Add both entries to your `opencode.json`:

```json
{
  "mcp": {
    "gramatr": {
      "type": "remote",
      "url": "https://api.gramatr.com/mcp",
      "enabled": true
    }
  },
  "plugin": [
    "@gramatr/opencode-plugin"
  ]
}
```

OpenCode will fetch the package from npm on next start. No global install
required.

## Authentication

The remote MCP connector authenticates via OAuth 2.0 Device Authorization
Grant ([RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628)). On first
connect, OpenCode prompts you to visit a short URL and paste a user code —
the same flow used in SSH, WSL, and CI environments where a browser
redirect can't reach the client. Tokens are stored by OpenCode's MCP
client; the plugin never handles raw credentials.

If you don't have a grāmatr account yet, sign up at
[gramatr.com](https://gramatr.com).

## How it works

```
OpenCode
   │
   ├── plugin: @gramatr/opencode-plugin  ──┐
   │                                       │ lifecycle events
   │                                       │ (session.created, message.updated, …)
   │                                       ▼
   └── mcp.gramatr (remote, OAuth) ──► api.gramatr.com/mcp
                                       (route_request, load_handoff,
                                        save_reflection, …)
```

The plugin is a thin connector: every grāmatr hook is invoked against the
already-connected remote MCP server declared in the `mcp` block — there is
no local binary, no `execSync`, no shell-out. Guidance from the server is
injected into the active session as a `noReply` system message so the model
sees it before formulating its next response.

When OpenCode's plugin API exposes a typed `client.callTool()`, the
connector will switch to direct MCP tool invocation and drop the
prompt-injection path.

## Requirements

- OpenCode with `@opencode-ai/plugin` ≥ 1.0.0
- Node.js ≥ 22
- Network access to `https://api.gramatr.com/mcp`

## Links

- Docs: [gramatr.com/docs](https://gramatr.com/docs)
- OpenCode plugin reference: [opencode.ai/docs/plugins](https://opencode.ai/docs/plugins/)
- Source manifest: [`contracts/mcp/opencode-plugin-manifest.yaml`](https://github.com/gramatr/gramatr/blob/main/contracts/mcp/opencode-plugin-manifest.yaml)
- Privacy: [gramatr.com/privacy](https://gramatr.com/privacy/)
- Terms: [gramatr.com/terms](https://gramatr.com/terms/)
- Support: [support@gramatr.com](mailto:support@gramatr.com)

## License

See [LICENSE](LICENSE) in this package.
