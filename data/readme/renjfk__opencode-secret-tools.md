[![CI](https://github.com/renjfk/opencode-secret-tools/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/renjfk/opencode-secret-tools/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![npm](https://img.shields.io/npm/v/@renjfk/opencode-secret-tools)](https://www.npmjs.com/package/@renjfk/opencode-secret-tools)
[![Downloads](https://img.shields.io/npm/dm/@renjfk/opencode-secret-tools)](https://www.npmjs.com/package/@renjfk/opencode-secret-tools)

# opencode-secret-tools

Configurable secret bridge for [OpenCode](https://opencode.ai/).

Provides `list_secrets`, `get_secret`, and `clear_secret` tools that shell out
to any CLI-based secret store. Loaded secrets are injected into shell commands
through a `shell.create.before` hook, and a `tool.execute.after` hook redacts
their values from all subsequent tool outputs before they reach the LLM.

## Install

Add to `~/.config/opencode/opencode.json` (this is a server plugin, so the
TUI-side `cli.json` cannot load it):

```json
{
  "plugins": [{ "package": "@renjfk/opencode-secret-tools" }]
}
```

### Refresh cached plugin after updates

If OpenCode keeps using an older published version of the plugin after an
update, clear the cached package and restart OpenCode:

```bash
rm -rf ~/.cache/opencode/packages/@renjfk/
```

## Configuration

```json
{
  "plugins": [
    {
      "package": "@renjfk/opencode-secret-tools",
      "options": {
        "folder": "Secrets",
        "listCmd": ["rbw", "list", "--fields", "name,folder"],
        "getCmd": ["rbw", "get", "--folder", "Secrets", "{name}"]
      }
    }
  ]
}
```

### Options

| Option    | Required | Description                                                                               |
| --------- | -------- | ----------------------------------------------------------------------------------------- |
| `listCmd` | Yes      | Command returning secret names. One per line, or TSV `name\tfolder` when `folder` is set. |
| `getCmd`  | Yes      | Command returning the secret value. `{name}` is replaced at runtime.                      |
| `folder`  | No       | Filter `listCmd` output to this folder. If omitted, every line is treated as a name.      |

## Tools

- `list_secrets({})` — run `listCmd`, parse and filter, return names. Prompts according to your `list_secrets` permission rule (resource: the configured folder, else `*`).
- `get_secret({ name })` — run `getCmd` with `{name}` replaced, load the value for shell commands, track it for redaction. Prompts according to your `get_secret` permission rule (resource: the secret name).
- `clear_secret({ name })` — stop injecting the secret and stop tracking it.

## How it works

1. User configures `listCmd` and `getCmd` for their vault CLI (e.g. `rbw`, `op`, `gopass`).
2. `list_secrets` runs `listCmd`, parses the output (optionally filtering by folder), and returns names.
3. `get_secret` runs `getCmd` with `{name}` replaced, stores the value in a per-plugin-instance map (one per project/location, so secrets never cross projects), and tracks it for redaction. Both `get_secret` and `list_secrets` call `permission.assert` first, so `ask` and resource-scoped permission rules work.
4. A `shell.create.before` hook injects every loaded secret into the environment of each shell command, so `bash`/`shell` tools can use `$NAME`. Values are never written to the shared server's `process.env`.
5. `tool.execute.after` replaces tracked values with `[REDACTED: {name}]` in `content` (string or array) and `metadata` of all tools except `list_secrets`.
6. `clear_secret` removes the value from the injection map and stops tracking.
7. Values shorter than 4 characters are not redacted to avoid false positives.

## Redaction in action

Below is a real-world example showing the redaction mechanism at work. Even though the secret is injected into the subprocess environment and can be referenced in commands, its plaintext value never appears in any tool output visible to the LLM or user.

![Redaction demo](screenshots/redaction-demo.png)

## Contributing

opencode-secret-tools is open to contributions and ideas!

### Issue conventions

**Format:** `type: brief description`

- `feat:` new features or functionality
- `fix:` bug fixes
- `enhance:` improvements to existing features
- `chore:` maintenance tasks, dependencies, cleanup
- `docs:` documentation updates
- `build:` build system, CI/CD changes

### Development

```bash
npm run test         # node --test
npm run check        # lint + fmt
npm run lint         # oxlint
npm run fmt          # oxfmt --check
npm run fmt:fix      # oxfmt --write
```

### Test local plugin in OpenCode

To test unpublished changes in the OpenCode TUI, point the config at the local
repo path, not the npm package name:

```json
{
  "plugins": [{ "package": "/Users/your-user/opencode-secret-tools/index.js" }]
}
```

### Release process

Manual releases via opencode; see [RELEASE_PROCESS.md](RELEASE_PROCESS.md).

## License

This project is licensed under the [MIT License](LICENSE).
