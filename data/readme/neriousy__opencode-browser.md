# @neriousy/opencode-browser

An embedded browser workspace for the OpenCode V2 TUI. It runs one hidden Electron runtime in the background, renders
the selected page directly into the terminal, and lets the user and an agent operate the same live browser tabs.

There is no separate Electron window. The address bar, navigation controls, loading state, and tab strip are OpenTUI
UI inside OpenCode. Rendering is provided by
[`opentui-browser`](https://github.com/neriousy/opentui-browser), whose terminal-browser direction is inspired by
[`zenbu-labs/terminal-browser`](https://github.com/zenbu-labs/terminal-browser).

## What it provides

- Real interactive pages with keyboard, paste, mouse, wheel, hover, links, and forms.
- Multiple browser tabs sharing one Electron runtime and profile.
- Responsive viewports that follow OpenCode and terminal resizes.
- Hidden background tabs that stay alive while only the selected page is presented.
- Automatic OpenCode registration for browser lifecycle tools and Chrome DevTools MCP.
- Scoped Effect lifecycle, bounded recovery, and cleanup for Electron, pages, MCP servers, and the OpenTUI surface.

## Requirements

- OpenCode V2 `0.0.0-next-16650` or a newer compatible `@next` build, launched as `opencode2`.
- A local Kitty-capable terminal. Ghostty is the primary tested terminal.
- Node.js 22.12 or newer for the controller and Chrome DevTools MCP subprocesses.
- Bun 1.3 or newer only when developing this repository.

The OpenCode TUI, OpenCode server, Electron runtime, and terminal must run on the same machine. Remote
`opencode attach` sessions, tmux, and screen are not supported by the current image transport.

The OpenCode V2 plugin API is still beta. This release is tested against `0.0.0-next-16650`; upgrade OpenCode and
this plugin together if that API changes.

## Install OpenCode V2

Install the current V2 prerelease and allow its package install script:

```sh
npm install -g @opencode-ai/cli@next --allow-scripts='@opencode-ai/cli'
opencode2 --version
```

If npm previously installed the CLI without its platform binary:

```sh
npm rebuild -g @opencode-ai/cli --allow-scripts='@opencode-ai/cli'
```

## Configure the plugin

OpenCode V2 reads `~/.config/opencode/cli.json`, or `$OPENCODE_CONFIG_DIR/cli.json` when that environment variable
is set. Add the published TUI plugin:

```json
{
  "tabs": {
    "enabled": true,
    "scope": "global"
  },
  "mouse": true,
  "plugins": [
    {
      "package": "@neriousy/opencode-browser@latest",
      "options": {
        "url": "https://example.com"
      }
    }
  ]
}
```

For reproducible installations, replace `@latest` with an exact package version. If no options are needed, the
short form also works:

```json
{
  "plugins": ["@neriousy/opencode-browser@latest"]
}
```

OpenCode resolves the package's `./tui` export. There is no separate plugin file, MCP configuration, Electron
window, Chrome installation, or browser-server setup.

Electron is a package dependency. If its install script did not provision the platform binary, first activation runs
Electron's installer asynchronously in a bounded worker and validates the result before starting the browser. That
first activation can take longer and needs either a cached binary or network access.

Restart `opencode2` after changing the package or its options.

## Use

`/browser` reveals the currently selected browser tab when one exists; it does not create another tab. When the browser
is empty, it creates the local **New tab** page on demand. `/browser https://example.com` reuses the selected tab and
starts navigation only after its terminal surface has the final viewport. Use
`/browser-new` or `/browser-new https://example.com` when you explicitly want an additional tab. Both commands are
available from the slash-command picker and command palette.

| Action                      | Keyboard or UI                                           |
| --------------------------- | -------------------------------------------------------- |
| Focus the address           | `Ctrl-L` / `Cmd-L`                                       |
| New browser tab             | `/browser-new [url]`, `Ctrl-T` / `Cmd-T`, or `+`         |
| Close selected browser tab  | `Ctrl-W` / `Cmd-W`, or the tab's `×`                     |
| Next / previous browser tab | `Ctrl-Tab` / `Ctrl-Shift-Tab`                            |
| Reload or stop loading      | `Ctrl-R` / `Cmd-R`, or the toolbar button                |
| Back / forward              | `Cmd-[` / `Cmd-]`, or `Alt-Left` / `Alt-Right`           |
| Reset an unresponsive page  | `Ctrl-Shift-R` / `Cmd-Shift-R`                           |
| Return to OpenCode          | `Ctrl-Shift-B`, a session tab, or **Return to OpenCode** |

While the address field is focused, `Escape` restores the live page URL. `Ctrl-W` keeps its normal word-deletion
behavior there; `Cmd-W` still closes the page.

Returning to OpenCode hides the browser without closing Electron or its pages, so reopening is fast. **Remove browser
tabs from strip** also hides every browser page item while keeping the runtime ready; `/browser` restores them.
Closing the final tracked page closes the browser workspace and leaves no hidden replacement target. The Electron
runtime stays ready; the next explicit `/browser`, `open`, or `new_tab` operation creates the next page. A plain
`/browser` creates the local welcome page on demand and presents it as **New tab** with an empty address instead of
exposing its internal data URL.

Popup windows are deliberately denied. Use `+` or the controller's `new_tab` tool when a new tracked page is
required.

## Options

| Option                   | Purpose                                                                         |
| ------------------------ | ------------------------------------------------------------------------------- |
| `url`                    | Initial HTTP(S) URL and default new-tab page. Defaults to a local welcome page. |
| `electronExecutablePath` | Explicit Electron executable. Normally resolved from the package dependency.    |
| `userDataDirectory`      | Dedicated persistent profile for cookies, logins, history, and cache.           |
| `frameRate`              | Active Electron paint ceiling from 1 to 240 fps. Defaults to 30.                |
| `nodeCommand`            | Node.js executable used for both local MCP subprocesses.                        |

Without `userDataDirectory`, each Browser Generation uses a private temporary profile that is deleted during cleanup.
Only use a directory dedicated to this plugin; do not share it with another running Electron process.

## Agent access

The plugin automatically registers two local MCP servers:

| MCP server                  | Responsibility                                                                        |
| --------------------------- | ------------------------------------------------------------------------------------- |
| `opencode-browser-control`  | Navigate, create, list, select, and close tracked browser tabs in the background.     |
| `opencode-browser-devtools` | Inspect and operate the same live Electron pages through `chrome-devtools-mcp@1.6.0`. |

The control server exposes six tools: `open`, `new_tab`, `list_tabs`, `select_tab`, `close_tab`, and `status`. Agent
operations never select the Browser workspace. They can add a browser item to the terminal tab strip and update its
loading state, but OpenCode stays active until the user runs `/browser` or selects that browser tab.

For reliable agent automation:

1. Use `open` for an ordinary single-page request; it reuses the selected tab in the background, including the initial
   welcome tab.
2. Use `new_tab` only when the user requests an additional tab or the task must keep multiple pages open concurrently;
   the new page is also created and selected in the background.
3. Read its stable logical `tabId`, current CDP `targetId`, URL, and title.
4. Call Chrome DevTools MCP `list_pages` and match the live page by URL/title.
5. Use Chrome DevTools MCP's numeric `pageId` for page-scoped DevTools operations.

`tabId`, `targetId`, and Chrome DevTools MCP's `pageId` are different identities:

- `tabId` belongs to the plugin and survives replacement of an unresponsive page.
- `targetId` belongs to the current Electron `webContents` and changes when that page is replaced.
- `pageId` belongs to the current Chrome DevTools MCP process and must be obtained from `list_pages`.

Use the controller for `new_tab` and `close_tab`; creating page lifecycle through DevTools would bypass the Browser
Session and leave the terminal tab strip stale. Give `new_tab` a caller-generated `requestId` and reuse it when
retrying the same timed-out call.

The plugin launches the installed Chrome DevTools MCP entry with Node.js. It does not use `npx`, download an MCP
package during activation, discover system Chrome, or create a second browser runtime.

DevTools screenshots default to WebP at quality 80 and are bounded to 640×640 during capture. The bound keeps even an
explicit PNG capture below Chrome DevTools MCP's inline-image threshold, so screenshot results remain typed image
attachments that OpenCode can render in the session feed instead of opaque temporary-file messages.

If the plugin becomes active during an existing agent turn, begin a new turn so OpenCode can refresh its MCP tool
catalog.

## How it works

One Browser Generation owns one hidden Electron Managed Browser Runtime. Every browser tab is a long-lived Shared
Browser Page inside that runtime. Only the selected visible page owns an active Presentation:

```text
OpenCode Host UI
  -> selected Shared Browser Page
    -> Electron offscreen paint
      -> raw RGBA file
        -> Kitty image in the terminal
```

Background pages remain available to the user and agent, idle their offscreen paint rate at 1 fps, and do not send
frames to Kitty. Changing terminal geometry updates the selected page viewport and placement without stretching a stale
frame. Explicit foreground URL commands wait for that viewport and Presentation to be ready before navigation; agent
navigation remains immediate and offscreen.

OpenCode V2 currently exposes session tabs rather than arbitrary native plugin tabs. The plugin therefore renders a
composite strip in the global app slot: OpenCode sessions and logical browser pages remain independently owned, while
the current OpenCode route stays mounted underneath the browser workspace.

If a page Presentation fails, the plugin retries it and can replace only that Shared Browser Page. If Electron
disconnects, it retires the Browser Generation, launches a clean replacement, and refreshes the DevTools endpoint
without replacing the stable controller or MCP names.

Contributor-level lifecycle, identity, and Effect boundaries are documented in
[`CONTEXT.md`](https://github.com/neriousy/opencode-browser/blob/main/CONTEXT.md).

## Resource use

Electron's fixed main, GPU, network-service, profile, and DevTools cost is paid once per Browser Generation. Each
additional tab adds a page renderer; only the selected visible page pays active Presentation cost.

On Apple M5/macOS with a 960×600 animated page:

| State                                  | Electron memory |          Electron CPU | Bun + Electron memory |
| -------------------------------------- | --------------: | --------------------: | --------------------: |
| Hidden/no Presentation, 1 fps idle cap |     223–225 MiB | 0.25–0.6% of one core |           276–278 MiB |
| Active Presentation, 30 fps            |     227–232 MiB |    26–29% of one core |           281–283 MiB |

This short measurement covers the real bitmap-to-RGBA-file path but excludes Ghostty's image storage and a full
OpenCode host baseline. Real websites, video, WebGL, extra tabs, viewport size, and terminal image storage can use more.

Raw frame traffic scales with `width × height × 4 × frameRate`. At 30 fps, 960×600 is about 66 MiB/s and
1920×1080 is about 237 MiB/s. Raising the rate to 60 doubles those upper bounds. Lower `frameRate` first when reducing
active CPU or file traffic.

## Troubleshooting and limitations

- **No browser appears:** run `/browser`, then check OpenCode's **Plugins** view for an activation error.
- **First activation is slow:** Electron may be provisioning its platform binary after lifecycle scripts were skipped.
- **Blank surface:** use a direct local Kitty-capable terminal and OpenCode's alternate-screen renderer; multiplexers
  and remote attachment are unsupported.
- **Input goes to OpenCode:** click the page or use `/browser` to focus the Browser Surface; `Ctrl-L` intentionally
  focuses the address field.
- **MCP registration fails:** remove or rename pre-existing servers called `opencode-browser-control` or
  `opencode-browser-devtools`. The plugin will not overwrite them.
- **Duplicate plugin behavior:** configure the package once. Do not combine `cli.json` registration with a local
  auto-discovered copy.

Page-created popup windows, browser permission prompts, remote rendering, and terminal multiplexers are not supported.

## Cleanup and security

Hiding the workspace keeps Electron ready. Deactivating the plugin from OpenCode's **Plugins** view—or removing it from
`cli.json` and restarting—removes the app slot and both MCP registrations, closes the authenticated controller, and
closes Electron.

Electron's DevTools server and the controller bind only to loopback. The controller requires a random bearer token
passed only to its stdio sidecar, bounds request bodies and concurrent work, and accepts only HTTP(S) navigation.
Treat the configured persistent browser profile as sensitive because an attached DevTools agent can inspect its cookies
and storage.

## Local development

```sh
git clone https://github.com/neriousy/opencode-browser.git
cd opencode-browser
bun install
bun run check
bun run test:packed
bun run test:mcp
```

To load a checkout, build it and point `plugins` at its exported file:

```json
{
  "plugins": [
    {
      "package": "/absolute/path/to/opencode-browser/dist/tui.js",
      "options": {
        "url": "https://example.com"
      }
    }
  ]
}
```

Launch `opencode2` from the project you want the agent to operate on. Do not also place the plugin under
`.opencode/plugins/tui`, because local auto-discovery would load it a second time.

`bun run test:packed` uses a sibling `../opencode` checkout by default. Set
`OPENCODE_REPO=/absolute/path/to/opencode` when that checkout is elsewhere. `bun run test:mcp` launches the real
Electron runtime and directly installed Chrome DevTools MCP.

Release verification:

```sh
bun run check
bun run test:packed
bun run test:mcp
```

Publishing is tag-driven through `.github/workflows/publish.yml`. Set the package version, push `main`, then push the
matching `v<version>` tag. GitHub reruns `check` and `test:packed` before publishing through npm trusted publishing.
