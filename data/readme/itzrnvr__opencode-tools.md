# opencode-tools

A small collection of focused plugins for [OpenCode V2](https://opencode.ai/v2).

## Plugins

| Plugin | Commands | What it does |
| --- | --- | --- |
| [`clean-defeatist`](./clean-defeatist) | `/clean-defeatist`, `/clean-defeatist-compact` | Reframes a session in success-oriented language, optionally followed by a compaction. |
| [`turn-surgeon`](./turn-surgeon) | `/turns`, `/turns-quick`, `/turns-restore` | Turn editor: visually delete or edit individual turns — a single reply, one tool call, ranges, everything from a point on. |

## Install

Clone the repo:

```sh
git clone https://github.com/itzrnvr/opencode-tools.git
```

Add the plugin directory to the `plugins` array in `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "plugins": [
    {
      "package": "/absolute/path/to/opencode-tools/clean-defeatist"
    }
  ]
}
```

Or copy/symlink the plugin directory into `.opencode/plugins/` (plugins there are loaded automatically).

Restart the OpenCode service after changing the config:

```sh
opencode service restart
```

## License

MIT
