# opencode-brave-websearch

[![npm version](https://img.shields.io/npm/v/opencode-brave-websearch)](https://www.npmjs.com/package/opencode-brave-websearch)

An OpenCode v2 plugin that registers [Brave Search API](https://brave.com/search/api/) as a websearch provider.

This project is part of [alexandru/agents-config](https://github.com/alexandru/agents-config). See it in use in my [OpenCode configuration](https://github.com/alexandru/opencode-config).

## Configuration

Set `BRAVE_SEARCH_API_KEY` in the OpenCode process environment. Add the package to `opencode.jsonc`:

```jsonc
{
  "websearch": { "provider": "brave" },
  "plugins": ["opencode-brave-websearch"],
}
```

See [development.md](docs/development.md) for local tests and publishing.
