# @argabor/caveman-opencode-plugin

Caveman communication mode plugin for [opencode](https://opencode.ai). Adapts [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) into hook-based plugin.

> Fork of [`caveman-opencode-plugin`](https://www.npmjs.com/package/caveman-opencode-plugin) by dantesCode, adding **OpenCode V2 support** (dual-generation export). Published under the `@argabor` scope.

## Installation

```bash
# Global install
opencode plugin @argabor/caveman-opencode-plugin@latest --global

# Or local install
opencode plugin @argabor/caveman-opencode-plugin@latest
```

**NPM:** https://www.npmjs.com/package/@argabor/caveman-opencode-plugin

Add to `opencode.json`.

OpenCode V1:

```json
{
  "plugin": ["@argabor/caveman-opencode-plugin"]
}
```

OpenCode V2:

```json
{
  "plugins": ["@argabor/caveman-opencode-plugin"]
}
```

## OpenCode V2 support

This package is dual-generation: one default export provides both implementations.

- V1 calls `server()` — requires OpenCode `>= 1.18.29` for the object entrypoint.
- V2 reads `id` + `setup()` and ignores `server()`.

The V2 half uses the V2 domain APIs:

- `ctx.session.hook("context", ...)` replaces the V1 `experimental.chat.system.transform` hook for system-prompt injection.
- `ctx.command.transform(...)` replaces the V1 `config` + `command.execute.before` pair for the `/caveman*` commands.

`caveman.json` is read from the same locations on both generations (project root, then `$XDG_CONFIG_HOME/opencode/`).

> On V1 hosts `>= 1.17.10` an embedded V2 core may also invoke `setup()` in a
> registration-only pass, which can add extra `[v2]` log lines. It does not
> change V1 behavior.

## Setup

Run the interactive setup script:

```bash
# Download and run
curl -fsSL https://raw.githubusercontent.com/argabor/caveman-opencode-plugin/main/setup.sh | bash

# Or clone and run locally
curl -O https://raw.githubusercontent.com/argabor/caveman-opencode-plugin/main/setup.sh
bash setup.sh
```

Or create `caveman.json` manually:

```bash
# Project-level config (recommended)
echo '{"enabled":true,"defaultMode":"full","features":{"caveman":true,"commit":true,"review":true}}' > caveman.json

# Or global config in ~/.config/opencode/
mkdir -p ~/.config/opencode
echo '{"enabled":true,"defaultMode":"full","features":{"caveman":true,"commit":true,"review":true}}' > ~/.config/opencode/caveman.json
```

## Upstream

Behavior mirrors [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) methodology. See [UPSTREAM.md](UPSTREAM.md) for reference and intentional differences.

## Configuration

`caveman.json` example:

```json
{
  "enabled": true,
  "defaultMode": "full",
  "features": {
    "caveman": true,
    "commit": true,
    "review": true
  }
}
```

- `enabled` — master switch
- `defaultMode` — mode on session start (`lite`, `full`, `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`, `off`)
- `features` — toggle individual features:
  - `caveman` — enable caveman communication mode
  - `commit` — enable `/caveman-commit` command
  - `review` — enable `/caveman-review` command

### Config file locations

Plugin looks for `caveman.json` in this order:

1. `./caveman.json` (project root)
2. `$XDG_CONFIG_HOME/opencode/caveman.json` (global, defaults to `~/.config/opencode/caveman.json`)

Both files are merged per key, so a global `defaultMode` is kept unless the project file sets its own. The project file takes precedence over global for the keys it contains.

## Commands

| Command | Description |
|---------|-------------|
| `/caveman <mode>` | Switch caveman mode |
| `/caveman-commit <diff>` | Generate conventional commit message |
| `/caveman-review <code>` | One-line code review |

## Modes

| Mode | Description |
|------|-------------|
| `lite` | Light compression, keep some filler |
| `full` | Full caveman rules (default) |
| `ultra` | Maximum brevity |
| `wenyan-lite` | Lite in classical Chinese style |
| `wenyan-full` | Full classical Chinese style |
| `wenyan-ultra` | Ultra classical Chinese style |
| `off` / `normal` | Disable caveman |

## Companion Plugin

For context compression, pair with [@tarquinen/opencode-dcp](https://github.com/Opencode-DCP/opencode-dynamic-context-pruning).

## License

MIT
