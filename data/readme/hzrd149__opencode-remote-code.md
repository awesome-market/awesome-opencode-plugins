# Remote Code

[中文](README.zh-CN.md)

Use OpenCode to work on a remote machine over SSH. The plugin redirects `shell`,
`glob`, `grep`, `read`, `write`, `edit`, and `patch` to the remote target. Commands
run over SSH; file tools use SFTP. No remote agent installation is required.

**Install once in your global OpenCode config, then use `/remote connect` to switch
the current session to SSH.** Other sessions stay local; `/remote disconnect`
switches the session back to local tools.

## Requirements

- OpenCode 2.2.7+ (V2 instruction-source metadata is required), compatible with the `@opencode/plugin` version in [package.json](package.json).
- Node.js 20+ for the plugin's Node runtime and tests.
- A remote SSH server with SFTP and a POSIX shell, or OpenSSH for Windows with
  PowerShell 5.1/7. No remote Node.js, Python, Git, or ripgrep is needed.

## Quick start: install globally, connect per session

### 1. Build the plugin

The scoped npm package is not published yet. Build a local checkout using the pnpm
version pinned in `package.json`:

```sh
git clone https://github.com/hzrd149/opencode-remote-code.git
cd opencode-remote-code
pnpm install --frozen-lockfile
pnpm run build
```

### 2. Enable it globally

Add this entry to `plugins` in **`~/.config/opencode/opencode.jsonc`** (or
`$XDG_CONFIG_HOME/opencode/opencode.jsonc` when set). Use the absolute path to your
built checkout and keep your other configuration entries:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "/absolute/path/to/opencode-remote-code",
      "options": { "runtime": true }
    }
  ]
}
```

This makes `/remote` available across projects. Sessions start with local tools;
no SSH connection is opened until you connect. Leave `ssh`, `host`, and `activateIn`
out of this global runtime configuration. OpenCode reloads configuration changes
automatically; use `/reload` if needed.

### 3. Switch the current session to SSH

Open OpenCode in your usual project directory, or use an existing session. Enter:

```text
/remote connect server.example
/remote status
```

Once connected, file and shell tools in **this session** operate on the remote
machine. The username defaults to your local OS user (on the OpenCode service
host), and the working directory defaults to the remote login home, resolved
over SFTP. Other sessions are unaffected. To select a user and project explicitly:

```text
/remote disconnect
/remote connect alice@server.example --workdir /srv/project --key ~/.ssh/id_ed25519
```

To return to local tools:

```text
/remote disconnect
```

To change SSH targets, disconnect first, then run `/remote connect` with the new
target. For a Windows target, use a path such as `C:/Users/alice/project`.
Omit `--key` to use an SSH agent available to the OpenCode service, or supply
`--agent-socket` explicitly. Passwords must use the runtime RPC, not command text.
See [connection arguments](docs/usage.md#connection-arguments) for all supported flags.

Once published, `@hzrd149/opencode-remote-code` can replace the local `package`
path in the same global configuration; keep `"options": { "runtime": true }`.

## Important behavior

### Connect from the terminal

With the global runtime configuration above, you can also connect before opening
the OpenCode UI:

```sh
node /absolute/path/to/opencode-remote-code/dist/cli-main.js alice@server.example --workdir /srv/project
```

The installed executable is `remote-opencode`. It captures the terminal's
`SSH_AUTH_SOCK`, creates a stable local session directory, connects through typed
RPC, and attaches to that session. No model call is needed to connect.
In-session controls are `/remote status`, `/remote disconnect`, and
`/remote connect alice@server.example --workdir /srv/project`.
Host-only connections such as `/remote connect server.example` or
`/remote connect 192.168.1.20` default to your local OS username and the remote
login home (resolved over SFTP). Quote paths with spaces:
`/remote connect alice@host --workdir '/path with spaces'`.
Use `--port 2222`, `--user alice`, `--agent-socket /path/to/agent`, or `--key /path/to/key`
as needed. The CLI accepts the same target options (`--agent-socket` overrides its
calling terminal's `SSH_AUTH_SOCK`); the slash command uses the service's configured
authentication unless explicitly overridden. IPv6 may be bare or bracketed
(`alice@[::1]`); specify ports separately with `--port`, never `host:port`.
Arguments support quotes and backslash escapes, with no shell evaluation or
variable expansion. `/remote connect --help` shows usage. The previous JSON target
form remains supported; passwords must use RPC rather than slash-command text.
Connections are session-specific; interrupted or failed remote sessions block
file/shell tools until reconnect or explicit disconnect. Passwords use RPC,
not slash-command text. Remote subagent delegation is disabled.

- **Runtime mode switches one session at a time.** For a fixed target instead,
  omit `runtime` and configure `ssh`/`host` in plugin options. In that mode,
  `activateIn` restricts activation to matching local session directories;
  without it, the configured target is active everywhere. See [configuration](docs/configuration.md).
- `workdir` is a **remote** path. It defaults to the SSH user's home; relative
  paths and `~` resolve there. Windows absolute paths need a drive letter, such
  as `C:/Users/me/project`.
- Authentication uses `key`, `password`, or a local SSH agent (`agentSocket`,
  otherwise the service's `SSH_AUTH_SOCK`), in that order. Agent forwarding is disabled.
  The `ssh` string is parsed, not
  executed, and does not provide full OpenSSH command-line behavior.
- Remote files are mirrored locally as needed. There is no remote LSP, and
  SFTP searches can be slower than running ripgrep on the server.
- Runtime sessions have isolated mirrors; fixed-target sessions share them.
  Avoid concurrent edits to the same remote files. Currently,
  `patch` delete hunks empty files rather than remove them; use `shell` to delete.

## Documentation

### Remote instructions

OpenCode's model prompts, custom agents, skills, Code Mode, MCP guidance and session
instruction entries are preserved. The plugin replaces `core/environment` with remote
OS/shell/workspace details and `core/instructions` with the remote root `AGENTS.md`,
read once at setup. This replaces the entire discovered-file source, including local
global/configured instruction files; use custom agent instructions for shared policies.
Nested remote instruction discovery is not automatic. Generate/compaction requests
receive the same edits when they contain these sources; title prompts are untouched.
Stored history is unchanged, so old local instruction updates can remain in the transcript;
the remote context explicitly distinguishes them. No model prompt templates are bundled.

- [Configuration](docs/configuration.md): options, SSH syntax, paths, search limits.
- [Usage and troubleshooting](docs/usage.md): launchers, installation, tool behavior,
  and limitations.
- [Test harness](test/README.md): test commands, coverage, and platform requirements.
- [Changelog](CHANGELOG.md): changes since the fork and release notes for npm.

## Development

Use `nvm use` for the default development Node version and the pnpm version in
`package.json`. From the repository root:

```sh
pnpm install --frozen-lockfile
pnpm run build
pnpm run lint
MOCK_SSH_BASH=/bin/bash pnpm test --dialect=posix
```

Tests use Node + `tsx`; Windows integration tests need Windows and PowerShell.
See the [test guide](test/README.md) for platform requirements and runner options.

Run `pnpm dev` to build the plugin and open an interactive OpenCode session with
the local build and runtime connections enabled. OpenCode must be on `PATH`.
The launcher uses a private server (`--standalone`) and an ignored local session
directory at `tmp_test_artifacts/dev`; your usual providers and credentials remain
available. Inside the session, connect to a remote:

```text
/remote connect alice@server.example --workdir /srv/project
```

Use your terminal's SSH agent, or add `--key ~/.ssh/id_ed25519` to the connection
arguments. Check `/remote status` to confirm the connection. Development launcher
arguments match the `remote-opencode` CLI and connect before opening the TUI:

```sh
pnpm dev alice@server.example --workdir /srv/project --port 2222 --key ~/.ssh/id_ed25519
pnpm dev --help
```

All CLI options, including `--user` and `--session`, are supported. Target-specific
development sessions live beneath `tmp_test_artifacts/dev` and use a private
server that stops when the TUI exits. Use a development session ID with `--session`.
After source changes, exit and rerun `pnpm dev` to load a fresh build.
`pnpm dev:watch` runs only the TypeScript compiler in watch mode.

## Attribution and license

Forked from [vibed-this/opencode-remote-code](https://github.com/vibed-this/opencode-remote-code),
which forked [zz6zz666's original OpenCode V1 plugin](https://github.com/zz6zz666/opencode-remote-code).
Published package name: `@hzrd149/opencode-remote-code`. License: MIT.
