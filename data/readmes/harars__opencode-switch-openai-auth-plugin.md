# opencode-switch-openai-auth-plugin

Switch saved OpenAI OAuth accounts from OpenCode with one command:

```text
/switch
```

Version 0.3 adds an OpenCode 2 adapter. On 2.x, `/switch` selects accounts from OpenCode's native account manager; the plugin never reads or copies their tokens. The existing 1.x workflow remains available.

## Compatibility

| Host | Workflow | Live validation |
| --- | --- | --- |
| OpenCode 2.0.32–2.2.x | Native credential IDs and built-in account management | 2.0.32 and 2.2.0 on Linux |
| OpenCode 1.18.33–1.19.x | Legacy saved snapshots and native auth writes | 1.19.4 on Linux; previous 0.2 validation on 1.19.0 |

V2 uses the host's dialogs and keymap without importing OpenTUI or Solid at runtime. V1 uses the host's OpenTUI 0.4.5 / Solid 1.9.12. macOS/Windows and real browser/device authorization still need account/platform testing. Intermediate 2.x releases are covered by the declared API range, not individually exercised binaries.

## Installation

This checkout contains version 0.3.0. Building or packing it does not publish a registry release. To use the updated adapter now:

```bash
bun install --frozen-lockfile
bun run build
```

For **OpenCode 2**, merge this into `$XDG_CONFIG_HOME/opencode/cli.json` (default `~/.config/opencode/cli.json`, or `OPENCODE_CONFIG_DIR/cli.json` when overridden):

```json
{
  "plugins": ["/absolute/path/to/switch-auth-plugin"]
}
```

Use the built **directory**, including its root `tui.js` for 2.0.32 compatibility. In 2.2.0, local directories with package exports resolve through those exports; both routes load the same entry. A standalone `dist/entry.js` URL is not a V2 directory target. Keep your other plugin entries. Remove the old `/switch` entry to avoid duplicate registration. V1's `tui.json` uses a different schema; see Development below. Production configuration is not changed by the build or tests.

After a 0.3.0 registry release, V2 can install it with `opencode plugin add @harars/opencode-switch-openai-auth-plugin@0.3.0`.

## Usage

On **OpenCode 2**, `/switch` lists native OpenAI connections, labels the current account, and disables accounts that need sign-in. Select an account to activate its native credential ID. The plugin rechecks native state after selection so changes from another window are taken into account. **Add or manage accounts** opens native `/connect`; choose OpenAI to sign in, rename, or remove accounts. Environment-provided connections can take priority; the plugin checks the resulting active connection before reporting success.

V2 owns token storage, refresh, OAuth and provider reload. The plugin does not call `credential.list` (which exposes secrets), write `auth.json`, dispose the whole instance, or reuse the legacy saved store. An operation cancelled before selection or completed after plugin unload cannot start another switch. A native activation already sent cannot be undone by closing the UI. The V2 adapter uses the connected server's public API; V1's local-filesystem and writable-project requirements do not apply.

**Upgrading from 1.x:** OpenCode's own migration imports legacy active auth once; it does not import this plugin's saved account history. Old `auth-switch/accounts.json` and its backups are retained. Add any missing accounts through native `/connect`; the adapter deliberately does not copy old refresh tokens into the new schema.

On **OpenCode 1.x**, open `/switch` and select an action:

- **Sign in with OpenAI** uses OpenCode's native browser/device OAuth flow. Successful login changes the active OpenAI account and saves it.
- **Select an account** switches native OpenAI credentials, captures the outgoing account's latest tokens, and refreshes OpenCode.
- **Remove saved account** removes that saved record after confirmation. It keeps the active login intact.

The picker displays email, plan, workspace and the current account. An expired access token is retained: OpenCode can refresh it when used.

Switching and login query all session statuses in the current OpenCode instance and wait for busy/retrying responses to finish. Credentials are shared with other local OpenCode instances, so avoid switching while another window is generating a response.

Press **Escape** to close a dialog. **Ctrl+y** copies the authorization link or device code without intercepting normal authorization-code input. Closing a dialog cancels further plugin actions, including switches waiting for the store lock and pending native requests. A credential write or OAuth callback already accepted by OpenCode may still change the native login.

If a native write succeeds but refreshing OpenCode fails, the plugin reports the partial success and asks you to restart. A saved-account history error is also reported separately from the actual credential switch.

## V1 storage and upgrade

The following storage and migration rules apply only to the V1 adapter. It requires a directly launched local TUI, a writable project for a temporary filesystem check, and no `OPENCODE_AUTH_CONTENT` override. V1 `attach` is unsupported because its API cannot read remote credentials.

The store is separate from OpenCode's active `auth.json`:

```text
$XDG_DATA_HOME/opencode/auth-switch/accounts.json
```

Without `XDG_DATA_HOME`, OpenCode's XDG resolver defaults to `~/.local/share/opencode` on all platforms. The plugin uses the same resolver. `OPENCODE_TEST_HOME` does not independently redirect the data directory.

On first access to a v1 store:

1. The plugin creates a private, byte-for-byte `accounts.v1-backup.<id>.json`.
2. It migrates to v2 stable record IDs and deduplicates only accounts with matching user/workspace identity.
3. Invalid legacy records remain recoverable in the backup. Expired tokens are retained.

If the new directory has no store, the plugin can import the old macOS `Library/Application Support` or Windows `LOCALAPPDATA` / `APPDATA` store. Multiple legacy candidates require manual selection; originals are not deleted.

A malformed, empty, or unsupported-version store is preserved and blocks writes. Back up the current files before restoring a known-good copy. Never edit the store while OpenCode instances are using it. Migration backups contain credentials too.

Unix directories/files are restricted to `0700` / `0600`. Windows uses the directory's inherited ACLs; chmod is not an ACL guarantee. Writes use a cross-process lock, same-directory temporary file, synchronization, and atomic replacement. Stale locks from a crashed process are reclaimed automatically.

This plugin manages OpenCode OAuth credentials. It does not manage Codex CLI credentials or share token refresh ownership with Codex.

## Development

```bash
bun install --frozen-lockfile
bun run check
```

The check runs type checking, behavioral tests, OpenTUI rendering tests, and the build. Tests use fake credentials and temporary directories.

For a **V1** local source entry, add to your project's `.opencode/tui.json`:

```json
{
  "plugin": ["file:///absolute/path/to/switch-auth-plugin/src/entry.ts"],
  "plugin_enabled": { "harars.switch-auth": true }
}
```

With `tmux` and the relevant host binary installed, run:

```bash
bun run test:live /absolute/path/to/opencode-1.x
bun run test:live:v2 /absolute/path/to/opencode-2.x
```

V1 opens source, built, and unpacked-package TUI sessions. V2 opens built-directory and unpacked-package sessions against a separate localhost server. Both use isolated XDG directories and fake credentials and preserve unrelated providers. V2 also verifies a selection after another client's switch, native management handoff and that legacy files remain untouched. Only test screens are captured. These are not separate registry installs and do not perform real OAuth or model requests.

V2 source review: [opencode2_review_2026-10-28.md](opencode2_review_2026-10-28.md). Previous V1/Codex review: [latest_source_review_2026-10-12.md](latest_source_review_2026-10-12.md).

See [DESIGN.md](DESIGN.md) for the current storage and lifecycle contract and [CHANGELOG.md](CHANGELOG.md) for changes.
