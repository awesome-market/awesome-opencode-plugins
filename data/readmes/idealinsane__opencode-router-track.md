# @idealinsane/opencode-router-track

An experimental OpenCode plugin that reads model metadata returned by OpenRouter Free Models Router and displays it in the OpenCode terminal user interface (TUI) sidebar.

## Installation

Install the public package from npmjs.org. No npm login or GitHub personal access token (PAT) is required.

```sh
npm install @idealinsane/opencode-router-track
```

The package with the same name on GitHub Packages (`npm.pkg.github.com`) is hosted on a separate registry and requires GitHub authentication to install. This repository publishes to npmjs.org by default.

## How it works

- **Server entry point:** `dist/index.js` (default export). Uses the `http.response` hook to read model metadata from server-sent events (SSE) or JSON responses to free-model requests.
- **TUI entry point:** `dist/tui.jsx` (default export). Displays the most recently collected model information in the sidebar's `Free Models Router` section.
- **Local state:** `$HOME/.local/share/opencode/plugins/opencode-router-track/resolved.json`.

Register the server and TUI entry points separately with the plugin loader supported by your OpenCode version. Installing the npm package alone does not activate the plugin.

## Compatibility and limitations

- The development dependency is `@opencode/plugin@2.1.2`. The plugin uses the V2 plugin API; compatibility with other versions is not guaranteed.
- If a response contains no model metadata, the plugin cannot determine the selected model. Displayed values come from response or message metadata and are not independently verified provider information.
- The state file is shared across sessions. When multiple sessions are active, the sidebar may show a value from an earlier request or another session.
- A successful build is not proof of correct behavior inside OpenCode. This repository does not yet include automated OpenCode integration tests.

## Build from source

```sh
git clone https://github.com/idealinsane/opencode-router-track.git
cd opencode-router-track
npm ci
npm run build
npm pack --dry-run
```

Build output is written to `dist/`. Generated build files are not committed to the repository.

## License

MIT, as declared in `package.json`.
