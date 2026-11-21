# OpenCode plugins

Small terminal UI plugins for [OpenCode V2](https://opencode.ai/v2/docs/).

[![Checks](https://github.com/mxfp0/opencode-plugins/actions/workflows/checks.yml/badge.svg)](https://github.com/mxfp0/opencode-plugins/actions/workflows/checks.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-83d996)](LICENSE)

## Plugins

| Plugin | What it does |
| --- | --- |
| [Skill status](plugins/skill-status) | Shows loaded skills in a collapsible sidebar section, even at low verbosity. |

<img src="docs/skill-status.svg" alt="Preview of the Skills sidebar section with green dots beside loaded skill names" width="600">

## Install

Requires OpenCode V2. Tested with **2.0.31**.

Clone this repository:

```sh
git clone https://github.com/mxfp0/opencode-plugins.git
```

Add the plugin folder's absolute path to the `plugins` array in `~/.config/opencode/cli.json`. Keep any existing entries:

```json
{
  "plugins": [
    "/absolute/path/to/opencode-plugins/plugins/skill-status"
  ]
}
```

Restart OpenCode. The **Skills** section appears in the right sidebar. Click its heading to collapse or expand it.

OpenCode supplies the runtime dependencies. No build or dependency installation is needed to use the plugin.

To update, run `git pull` in the cloned repository and restart OpenCode.

## Develop

Use [Bun](https://bun.sh/) 1.3.14:

```sh
bun install
bun run typecheck
bun run test
```

Each plugin lives in `plugins/<name>/` with its own package manifest and README. See [Contributing](CONTRIBUTING.md) to add one.

## License

[MIT](LICENSE)
