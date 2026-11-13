# opencode-command-hotkeys

[Русский](README.ru.md)

Configurable hotkeys for OpenCode commands, with a Goal pause/resume toggle.

- Bind server commands to keys you choose.
- Pause or resume the current Goal with one key.
- Run actions without replacing or sending your draft.

## Compatibility

OpenCode 2.2.5 TUI. Building from source requires Node.js >=22.18.0 and npm.

## Installation

Install the package in a dedicated directory:

```sh
mkdir -p "$HOME/.local/share/opencode-command-hotkeys-install"
cd "$HOME/.local/share/opencode-command-hotkeys-install"
npm install --ignore-scripts opencode-command-hotkeys@0.1.1
```

In `cli.json`, use the absolute path to the installed package directory, ending in `node_modules/opencode-command-hotkeys`.

For a source checkout, run these commands and use the checkout directory instead:

```sh
npm ci --ignore-scripts
npm run build
```

## Configuration

Add an entry to your existing `plugins` list. Replace the example path with the package directory, not a JavaScript file.

```json
{
  "plugins": [
    {
      "package": "/absolute/path/opencode-command-hotkeys",
      "options": {
        "bindings": [
          {
            "id": "review-changes",
            "key": "ctrl+alt+r",
            "title": "Review against main",
            "command": "review",
            "text": "main"
          },
          {
            "id": "goal-toggle",
            "key": "f4",
            "title": "Pause / resume Goal",
            "action": "goal-toggle"
          }
        ]
      }
    }
  ]
}
```

No keys are bound by default. The example assigns Ctrl+Alt+R to the built-in `review` command to compare the current branch with `main`, passed in `text`; replace `main` with your desired base branch. F4 pauses or resumes the current Goal. Actions also appear in the command palette.

## Behavior

Actions target the current session. Keyboard shortcuts are inactive while a dialog is open, and drafts are not sent or replaced.

`goal-toggle` pauses an active Goal and resumes a paused one. If there is no Goal or it is complete, nothing happens. It never creates a new Goal.

Pausing a Goal suspends its automatic continuation. It is not Escape and does not stop an ongoing response.

Repeated calls of the same binding in the same session are ignored while its request is pending. Other bindings and sessions remain independent.

## More

- [Configuration reference](docs/configuration.md)
- [Testing](docs/verification.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Releasing](docs/releasing.md)
- [Changelog](CHANGELOG.md)

## License

[MIT](LICENSE), copyright 2026 Mikhail Belyakov
