# opencode-delete

Delete the session you are in from [OpenCode](https://opencode.ai), like `/delete` in Codex CLI.

OpenCode 2 has no command for deleting the current session. The only way is `/sessions`, then `ctrl+d` twice on the session. `/delete` does it from the session itself, after a confirmation that starts on Cancel.

```text
 Delete session                                                          esc

 "Fix the login redirect" and its 2 subagent sessions will be permanently
 deleted.

 The session is running and will be stopped first.

                                                                Cancel  Delete
```

## Features

- **Asks first, and starts on Cancel.** Pressing `enter` right after `/delete` closes the dialog and deletes nothing. To delete, move to Delete with `←` / `→` or `tab`, then press `enter`.
- **The whole conversation.** Deletes the session, its subagent sessions, and any background shells they left running.
- **Stops what is running.** If the session or one of its subagents is still working, it is stopped first. The dialog says so.
- **Quiet.** OpenCode takes you out of the deleted session on its own. The plugin only speaks up if something goes wrong.
- **Nothing to configure.**

## Requirements

OpenCode 2. Tested with OpenCode 2.2.5. OpenCode 1 is not supported.

## Install

To install it along with opencode-lodestar and opencode-ask, use [opencode-kit](https://github.com/dhkimxx/opencode-kit). It also removes copies left over from earlier installs:

```sh
curl -fsSL https://raw.githubusercontent.com/dhkimxx/opencode-kit/main/install.sh | bash
```

To install only this plugin:

```sh
opencode plugin add github:dhkimxx/opencode-delete
```

This installs the plugin and adds it to your `cli.json`. If OpenCode is already running, restart it.

To install a specific release, add its tag:

```sh
opencode plugin add github:dhkimxx/opencode-delete#v0.1.0
```

Update or remove the plugin with the same name you installed it with:

```sh
opencode plugin update github:dhkimxx/opencode-delete
opencode plugin remove github:dhkimxx/opencode-delete
```

To get a newer version, use `opencode plugin update`. Removing the plugin and adding it again reuses the copy OpenCode downloaded before.

<details>
<summary>Manual install</summary>

Clone the repository into your global OpenCode plugins folder. OpenCode loads it automatically.

```sh
git clone https://github.com/dhkimxx/opencode-delete ~/.config/opencode/plugins/opencode-delete
```

To update, run `git pull` in that folder.

</details>

## Usage

| To do this                 | Do this                                                          |
| -------------------------- | ---------------------------------------------------------------- |
| Delete the current session | `/delete`, or **Delete session** in the command palette (`ctrl+p`) |
| Choose Delete              | `←` / `→` or `tab`, then `enter`                                 |
| Cancel                     | `enter` (it starts on Cancel), `esc`, or `ctrl+c`                |

`/delete` is only offered on a session screen.

## How it works

- OpenCode does the deleting. The plugin asks it to remove the top session of the conversation, which takes the session's messages and every subagent session below it.
- Before that, the plugin interrupts whatever is running and waits for it to go idle, for up to 10 seconds. It also removes the background shells the conversation left running.
- Forks are separate sessions, so they stay. So does what OpenCode keeps outside a session, such as your prompt history and file snapshots.
- If OpenCode ships its own `/delete`, or another plugin already provides one, this plugin steps aside.

## Development

You need [Bun](https://bun.sh).

```sh
git clone https://github.com/dhkimxx/opencode-delete
cd opencode-delete
bun install
bun run check
```

`bun run check` type-checks the code, runs the tests, and builds `dist/tui.js`. To try your changes, point OpenCode at your clone in `~/.config/opencode/cli.json`, then restart OpenCode:

```json
{
  "plugins": ["/path/to/opencode-delete"]
}
```

`python3 scripts/smoke.py` opens a real OpenCode TUI with your clone in a pseudo-terminal, runs Delete session and checks that cancelling keeps the session and Delete removes it, with no model called. It needs `pip install pyte`. CI runs it on every push with the OpenCode version in the README, and every Monday with the newest OpenCode, opening an issue when that fails.

`dist/` is committed on purpose. OpenCode only compiles plugin JSX outside `node_modules`, so GitHub and npm installs need the built JavaScript. Run `bun run bundle` and commit `dist/` with your change. CI fails if `dist/` is out of date.

Don't add `build`, `prepare`, `prepack`, or install scripts to `package.json`. npm runs an extra install step for GitHub packages that have them, and that step fails inside OpenCode.

Releases are described in [RELEASING.md](RELEASING.md).

## License

[MIT](LICENSE)
