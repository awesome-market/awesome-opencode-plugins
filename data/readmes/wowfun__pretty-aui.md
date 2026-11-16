# pretty-aui

English | [简体中文](README.zh-CN.md)

A minimal, composable Agent Client Protocol chat UI for React and static sites.
It ships a framework-neutral controller, one React presentation, and a
standalone Shadow DOM mount of that same presentation. The package is
pre-release and may make breaking changes before 1.0.

![An ACP chat showing an agent task and its response in pretty-aui](https://raw.githubusercontent.com/wowfun/pretty-aui/v0.1.0-rc.1/tests/e2e/visual.spec.ts-snapshots/agent-inline-light-chromium-linux.png)

## Install

Install the current release candidate in a React application:

```sh
npm install pretty-aui@rc react react-dom
# or
pnpm add pretty-aui@rc react react-dom
```

For a static site or Python web app, [export the standalone browser files](#static-sites).

The published package supports Node.js `^22.22.2`, `^24.15.0`, or `>=26.0.0`,
matching the server-safe sanitizer used by the React entry. The copied
standalone bundle runs in the browser and has no Node.js runtime dependency.

## React

```tsx
import { Chat, createWebSocketConnector } from "pretty-aui/react";
import "pretty-aui/styles.css";

export function Assistant() {
  return (
    <Chat
      surface="inline"
      colorScheme="system"
      options={{
        connector: createWebSocketConnector("wss://example.com/acp"),
        session: { cwd: "/workspace/project" },
      }}
    />
  );
}
```

`Chat` includes the header, transcript, interactions, and composer. For custom
assembly and tool rendering, see [Composition](docs/composition.md). For visual
rules, stable data attributes, and CSS variables, see the
[Design system](docs/design-system.md).

The root `pretty-aui` entry is framework-neutral. React and React DOM are
optional package features used only by `pretty-aui/react`; the bundled
standalone entry does not resolve either peer.

## Static sites

Install the package as a development dependency and export its standalone
bundle to your static assets directory. Keep the bundled licenses with it.

```sh
npm install -D pretty-aui@rc
npm exec -- pretty-aui vendor assets/pretty-aui

# pnpm
pnpm add -D pretty-aui@rc
pnpm exec pretty-aui vendor assets/pretty-aui
```

Append `--check` to verify a checked-in copy. See the
[vendor command contract](docs/distribution.md#vendoring-standalone).

```html
<div id="assistant"></div>

<script type="module">
  import {
    mountChat,
    createWebSocketConnector,
  } from "/assets/pretty-aui/pretty-aui.js";

  const mounted = mountChat(document.querySelector("#assistant"), {
    options: {
      connector: createWebSocketConnector("wss://example.com/acp"),
      session: { cwd: "/workspace/project" },
    },
    surface: "sidebar",
    colorScheme: "system",
  });

  await mounted.ready;
</script>
```

ACP v1 is the default. Passing `options` creates a controller owned by the
mount; pass `controller` instead to borrow an existing controller. The two
modes are mutually exclusive. `styleNonce` nonces the package style element for
a strict host CSP. `setDraft()` and `focusComposer()` provide host integration
without Shadow DOM traversal. Call `mounted.unmount()` for deterministic
cleanup; the standalone mount also unmounts itself if its connected host is
removed from the document.

Browsers need an authenticated HTTP or WebSocket ACP gateway. Production
gateways should use their host application's authenticated channel. The local
OpenCode bridge in this repository is a development-only tool with a
short-lived per-process token injected into its loopback-served page and carried
as a WebSocket subprotocol, loopback TCP and browser-Origin checks, and bounded
connections. It does not print or place the token in a page URL.

## Composer integration

The full-width `+` menu groups images, Agent commands, host actions and the
optional ContextProvider add action. Set `placement: "shortcut"` on a host
`composerActions` entry to show it above the editor. Its `children` supply the
grouped choices. Choosing an action appends editable text to the draft.
Commands preserve body text and images.

Use `controller.setDraft`, `appendDraft`, `addDraftImages` and `sendDraft` after a
session is ready. `getSnapshot().draft` projects text, images, revision, preparation
lock and recoverable submissions. Standalone `setDraft` uses the same owner;
React renders updates asynchronously. Drafts survive same-controller reconnect
and session selection, with no browser-storage persistence. See
[composition](docs/composition.md#composer-actions) and the
[ownership contract](docs/architecture.md#composer-ownership-and-delivery).

Built-in connectors accept `maxMessageBytes` when a gateway advertises a budget.
The same decoded JSON UTF-8 limit applies to both transport directions and
controller preflight; its default is 2 MiB. Image intake retains original bytes
and may refuse an image even if its wire message would fit. Provider limitations
remain separate from these local bounds.

## Local development

Repository development uses the Node.js version pinned in `.node-version`
(26.3.1 or newer) and pnpm 10.34. Install dependencies and start the React
example:

```sh
pnpm install
pnpm dev
```

The page uses a deterministic ACP fixture by default, so it does not need an
agent service or credentials. It is a single Composer context playground:
selectable context is editable before a turn and disclosed in the transcript
after submission. The renderer adapts to the width of its host container. The
theme controls preserve the `thoughtDelay`, `subagentDelay`, and
`usage=extreme` diagnostics in the page URL.

Run the repository checks before submitting a change:

```sh
pnpm check
pnpm test:e2e
```

`pnpm test:e2e` is the Chromium browser gate; reviewed screenshot baselines run
only with Chromium on Linux. Firefox and WebKit are non-blocking compatibility
signals and can be run explicitly with `pnpm test:e2e:compat`; they skip
`visual.spec.ts`.

Run `pnpm build` after changing `src/`. The build writes the distributable files
to `dist/`.

To open the React example with a real local OpenCode session, install the
OpenCode CLI and run:

```sh
pnpm dev:opencode
```

This starts Vite and the localhost bridge, injects a short-lived random bridge
token into the served development page, then opens the live page in your
default browser. The same Composer context playground is used, while the page
source is fixed to OpenCode for that run. It does not print the token, put it in
browser history, or send a prompt. The bridge refuses non-loopback binds and TCP
peers; an explicit origin allowlist permits only the additional browser page
origins named by the developer. The bridge token is not inherited by the
spawned OpenCode process.

## License

MIT
