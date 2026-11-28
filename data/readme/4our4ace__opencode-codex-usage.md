# OpenCode Codex Usage

> **Unofficial community plugin:** This project is not affiliated with,
> endorsed by, or maintained by the OpenCode team.

See your ChatGPT/Codex usage limits directly in OpenCode's sidebar. The plugin
uses native V1 and V2 sidebar entrypoints.

![Usage sidebar](imgs/sidebar.png)

## Install

Copy and paste this command:

```bash
curl -fsSL https://raw.githubusercontent.com/4our4ace/opencode-codex-usage/v0.2.2/install.sh | bash
```

The installer safely adds the V1 sidebar plugin and, when `opencode2` is
installed, the V2 sidebar entrypoint. It keeps other settings and plugins,
backs up changed configuration, and installs the diagnostic command. It does
not edit shell profiles. If `~/.local/bin` is not on your `PATH`, run the
command as `~/.local/bin/opencode-chatgpt-usage` or add that directory to
`PATH` yourself.

**Requirements:** `bash`, `curl`, and one of `python3`, `node`, or `bun` for
safe JSON editing. JSONC/comments or malformed/unsupported configuration is
never rewritten; the installer prints a precise manual fallback instead.

Restart OpenCode after installation. On first use, open the command palette
and choose **Refresh Codex usage** if the panel is not immediately populated.

## OpenCode 2

OpenCode 2 uses a different TUI plugin API. When `opencode2` is installed, the
installer adds a native V2 sidebar panel. The V2 panel reads existing OpenCode
or plugin-private credentials; use `opencode2 auth login` to sign in when
needed.

## What to expect

OpenCode OAuth is reused automatically when its OpenAI login is available. You
can instead use the plugin’s own ChatGPT login, or explicitly enable read-only
Codex authentication. OpenCode and Codex credential stores are never written or
refreshed by this plugin.

Usage refreshes at startup when credentials exist, every five minutes, after a
completed OpenAI/Codex session becomes idle, and manually with `/codex-usage`.
Click or focus the **Codex usage** heading and press Enter or Space to collapse
or expand the panel.

On every refresh, the plugin asks any active provider auth resolver for the
current session credentials before falling back to OpenCode's OAuth store. This
optional protocol lets account-management plugins expose their live selection
without making Codex Usage depend on a specific plugin or cache its credentials.

![Expanded usage panel](imgs/oc_usage.png)

![Collapsed usage panel](imgs/usage_collapsed.png)

## Diagnostic command

The installer places `opencode-chatgpt-usage` in `${XDG_BIN_HOME:-~/.local/bin}`.
It prints only the plan and real usage limits:

```bash
opencode-chatgpt-usage --source opencode
# also supported: --source plugin or --source codex
```

## Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/4our4ace/opencode-codex-usage/v0.2.2/uninstall.sh | bash
```

This removes only the exact plugin entry, its managed files, and its managed
diagnostic wrapper/module. Restart OpenCode afterward.

If automatic editing is declined for a JSONC or malformed TUI config, use the
printed `file://` URL to add only that plugin entry to the top-level `plugin`
array, then restart OpenCode.

## Security & privacy

Credentials remain local. The plugin makes network requests only to OpenAI
authentication and ChatGPT usage endpoints; it sends no telemetry or analytics.
When selected or available, it reads OpenCode’s OAuth store, its plugin-private
auth file, and optionally `~/.codex/auth.json` read-only. Plugin-private
credentials are stored and refreshed locally; OpenCode and Codex credentials are
never written or refreshed. The ChatGPT WHAM endpoint and OAuth protocol are
undocumented and may change.
