# burrow 🦊

[![CI](https://github.com/RedFoxxo/burrow/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/RedFoxxo/burrow/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/RedFoxxo/burrow)](https://github.com/RedFoxxo/burrow/releases/latest)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-io.github.RedFoxxo%2Fburrow-blue)](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.RedFoxxo/burrow)
[![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](#install)
[![License: MIT](https://img.shields.io/github/license/RedFoxxo/burrow)](LICENSE)

[![burrow MCP server](https://glama.ai/mcp/servers/RedFoxxo/burrow/badges/card.svg)](https://glama.ai/mcp/servers/RedFoxxo/burrow)

An MCP server for [LeafWiki](https://github.com/perber/leafwiki): AI assistants
read, search, write and organize wiki pages. It signs in with your own LeafWiki
account, so every change shows up under your name, and it never overwrites a
change someone else made since your last read.

Tested against LeafWiki **v0.14.2**. Releases are listed in
[CHANGELOG.md](CHANGELOG.md).

burrow is one small executable: no Node.js or other runtime, about 8 MB of
memory while it runs.

## Requirements

- Linux (x64 or arm64), macOS (Apple silicon or Intel) or Windows (x64)
- A LeafWiki account that signs in with a username and password alone (no
  two-factor codes). A viewer account can only use the `read_` tools; changing
  pages needs an editor or admin.

## Install

Linux and macOS:

```sh
curl -fsSL https://raw.githubusercontent.com/RedFoxxo/burrow/main/install.sh | sh
```

Windows, in PowerShell:

```powershell
irm https://raw.githubusercontent.com/RedFoxxo/burrow/main/install.ps1 | iex
```

The script downloads the file for your system from the
[latest release](https://github.com/RedFoxxo/burrow/releases/latest), checks
it against the release's `SHA256SUMS`, and installs it as `burrow` in
`~/.local/bin` (Windows: `%LOCALAPPDATA%\Programs\burrow`). If that folder is
not on your `PATH` yet, it adds it: to `~/.profile` (and `~/.zprofile` on
macOS), or to your user `PATH` on Windows. Log out and back in on Linux and
macOS, or open a new terminal on Windows, then check with `burrow --version`.

Run the same line again to update. Settings go to the script: `BURROW_VERSION`
installs a given release, `BURROW_INSTALL_DIR` uses another folder, and
`BURROW_NO_MODIFY_PATH=1` leaves your `PATH` alone, e.g.
`curl -fsSL …/install.sh | BURROW_VERSION=2.0.0 sh`, or in PowerShell
`$env:BURROW_VERSION = '2.0.0'` before `irm … | iex`.

### Claude Desktop

Download `burrow.mcpb` from the
[latest release](https://github.com/RedFoxxo/burrow/releases/latest) and open
it, or drag it into **Settings → Extensions**. Claude Desktop asks for the wiki
URL, your username and your password (kept in the system's secure storage), and
runs burrow from the bundle; nothing else to install. burrow is also listed in
the [MCP Registry](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.RedFoxxo/burrow)
as `io.github.RedFoxxo/burrow`.

### By hand

Download the file for your system from the latest release into a folder on your
`PATH`, rename it to `burrow` (`burrow.exe` on Windows), and on Linux and macOS
make it executable (`chmod +x burrow`). On macOS, a file downloaded with a
browser needs `xattr -d com.apple.quarantine burrow` once before it starts.

| System | File |
|---|---|
| Linux x64 | `burrow-linux-x64` |
| Linux arm64 | `burrow-linux-arm64` |
| macOS, Apple silicon | `burrow-macos-arm64` |
| macOS, Intel | `burrow-macos-x64` |
| Windows x64, also Windows on ARM | `burrow-windows-x64.exe` |

To build from source instead (needs Rust):
`cargo install --git https://github.com/RedFoxxo/burrow --tag v2.0.3 --locked`.
Or as a container image: `docker build -t burrow .` in a clone, then start it
with `docker run -i --rm -e LEAFWIKI_URL -e LEAFWIKI_USERNAME -e LEAFWIKI_PASSWORD burrow`.

**Coming from 1.x?** burrow 1.x ran through `npx` from the npm package
`@redfoxxo/burrow`, which gets no new versions. Install burrow as above, then
change your client's `"command": "npx", "args": ["-y", "@redfoxxo/burrow@1"]`
to `"command": "burrow"`. Tools, settings and permission rules stay the same.

## Setup

burrow reads its settings from environment variables, which your MCP client
passes to it:

| Variable | Required | Purpose |
|---|---|---|
| `LEAFWIKI_URL` | yes | Wiki root, e.g. `https://wiki.example.com` (a base path like `/wiki` is fine, no `/api`). `https` only, except for `localhost`, `127.0.0.1` and `[::1]` |
| `LEAFWIKI_USERNAME` | when the wiki has sign-in | Your LeafWiki username or email |
| `LEAFWIKI_PASSWORD` | when the wiki has sign-in | Its password. Never logged |
| `BURROW_READ_ONLY` | no | `true` registers only the `read_` tools (default `false`) |

Keep the password out of config files: export `LEAFWIKI_USERNAME` and
`LEAFWIKI_PASSWORD` in your shell profile and let the client pass them
through, as the examples below do.

burrow signs in on the first tool call and keeps the session alive the way the
web app does. It sends your password and session cookies only to
`LEAFWIKI_URL` and never follows a redirect. If LeafWiki rejects the password,
burrow stops trying until it is restarted, so it cannot lock your account
(LeafWiki locks it for 15 minutes after 5 failed sign-ins).

### Claude Code

Register the server once for all your projects. `${LEAFWIKI_USERNAME}` and
`${LEAFWIKI_PASSWORD}` are read from your environment when the server starts,
so the password is not stored in the config:

```sh
claude mcp add-json burrow --scope user '{
  "type": "stdio",
  "command": "burrow",
  "env": {
    "LEAFWIKI_URL": "https://wiki.example.com",
    "LEAFWIKI_USERNAME": "${LEAFWIKI_USERNAME}",
    "LEAFWIKI_PASSWORD": "${LEAFWIKI_PASSWORD}"
  }
}'
```

Then add the permission rules to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": ["mcp__burrow__read_*"],
    "ask": ["mcp__burrow__write_*", "mcp__burrow__delete_*"]
  }
}
```

Claude Code names MCP tools `mcp__<server>__<tool>`, so the server name must be
`burrow` for these rules to match. Check the connection with
`claude mcp get burrow`, or `/mcp` inside a session.

### opencode

Add the server and the permission rules to `opencode.json` (global:
`~/.config/opencode/opencode.json`):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "burrow": {
        "type": "local",
        "command": ["burrow"],
        "environment": {
          "LEAFWIKI_URL": "https://wiki.example.com",
          "LEAFWIKI_USERNAME": "{env:LEAFWIKI_USERNAME}",
          "LEAFWIKI_PASSWORD": "{env:LEAFWIKI_PASSWORD}"
        }
      }
    }
  },
  "permissions": [
    { "action": "burrow_read_*", "resource": "*", "effect": "allow" },
    { "action": "burrow_write_*", "resource": "*", "effect": "ask" },
    { "action": "burrow_delete_*", "resource": "*", "effect": "ask" }
  ]
}
```

opencode names MCP tools `<server>_<tool>`, so the server name must be `burrow`
for these rules to match (`read_page` becomes `burrow_read_page`). Restart
opencode after changing the file; `opencode mcp list` shows whether it connected.

### Other MCP clients

Any client that starts local (stdio) servers works. Most accept an
`mcpServers` block like this one (Claude Desktop, Cursor, ...):

```json
{
  "mcpServers": {
    "burrow": {
      "command": "burrow",
      "env": {
        "LEAFWIKI_URL": "https://wiki.example.com",
        "LEAFWIKI_USERNAME": "your-username",
        "LEAFWIKI_PASSWORD": "your-password"
      }
    }
  }
}
```

If the client can't find `burrow` (some desktop apps don't see your shell's
`PATH`), give the full path to the file instead, e.g.
`"C:\\Users\\you\\AppData\\Local\\Programs\\burrow\\burrow.exe"` on Windows.
Then map the three tool-name prefixes below to the client's permission system.

## Tools

### Permission tiers

Every tool name starts with its tier, so one rule per tier covers all tools,
including ones added in later versions. Read tools are also marked read-only in
the MCP tool annotations, and delete tools destructive.

| Prefix | What it does | Suggested rule |
|---|---|---|
| `read_` | Reads only | allow |
| `write_` | Creates, changes, moves and copies pages and files | ask |
| `delete_` | Deletes pages and files | ask |

39 tools, about 5,100 tokens of tool definitions; `BURROW_READ_ONLY=true`
leaves the 20 read tools, about 2,200. Pages are named by id or by path
(`docs/runbooks/deploy`).

- read: `read_wiki`, `read_tree`, `read_page`, `read_lookup_path`,
  `read_find_title`, `read_search`, `read_search_status`, `read_tags`,
  `read_pages_by_tags`, `read_properties`, `read_pages_by_property`,
  `read_links`, `read_broken_links` (admins only), `read_revisions`,
  `read_revision`, `read_compare_revisions`, `read_favorites`, `read_assets`,
  `read_slug`, `read_refactor_preview`
- write: `write_create_page`, `write_ensure_path`, `write_update_page`,
  `write_edit_text`, `write_append`, `write_tags`, `write_properties`,
  `write_move`, `write_sort`, `write_pin`, `write_favorite`, `write_convert`,
  `write_copy`, `write_refactor`, `write_restore_revision`,
  `write_upload_asset`, `write_rename_asset`
- delete: `delete_page`, `delete_asset`

### Rules the server enforces

- **No lost updates.** `write_update_page`, `write_edit_text`, `write_refactor`
  and `delete_page` need the `version` from your last read. If someone changed
  the page since, nothing is sent and the answer says who changed it. The other
  write tools change the latest version, and only the part they name: tags,
  properties and appended text merge with what is there.
- **No surprise deletes.** `delete_page` refuses a page with children unless
  `recursive: true`.
- **No local files.** `write_upload_asset` takes base64 data (a `data:` URL is
  fine); burrow never reads your disk.

## Limitations

- Accounts with two-factor codes (TOTP) can't sign in through burrow. LeafWiki's
  API keys are still experimental and not supported yet.
- Revision history and link refactoring are LeafWiki options
  (`--enable-revision`, `--enable-link-refactor`); `read_wiki` says which are
  on. Without them, the revision and refactor tools fail.
- `write_move` and `write_rename_asset` don't rewrite links to the old
  location; `write_refactor` does, for pages.
- Admin screens (users, backups, snapshots, branding, API keys, import) are
  left out on purpose.

## Development

Building from source, running the tests and releasing are described in
[DEVELOPMENT.md](DEVELOPMENT.md).

## License

[MIT](LICENSE)
