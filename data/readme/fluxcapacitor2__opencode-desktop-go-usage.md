# OpenCode Go usage

Shows your OpenCode Go usage in the OpenCode Desktop tab bar as a small badge.

![Go usage tooltip under the top tab bar](docs/top-tabs.png)

- Displays the current monthly usage as a percentage and a circular progress ring
- Hover shows current monthly, weekly, and 5-hour usage, usage per day, the projected
  usage at the end of the subscription term, and the monthly reset date
- Refreshes every 10 minutes
- Supports both the horizontal and vertical tab layouts

## Install

```sh
mkdir -p ~/.config/opencode/plugins
cd ~/.config/opencode/plugins
git clone https://github.com/FluxCapacitor2/opencode-desktop-go-usage
cd opencode-desktop-go-usage
bun install
bun run build
```

OpenCode Desktop loads plugins from `~/.config/opencode/plugins/` automatically. If
you want to install it somewhere else, add it to `~/.config/opencode/opencode.json`:

```jsonc
{
  "plugins": ["/path/to/opencode-desktop-go-usage"],
}
```

The desktop app reloads the plugin when the package changes. If the badge does not
appear, restart OpenCode Desktop.

## Update

```sh
cd ~/.config/opencode/plugins/opencode-desktop-go-usage
git pull
bun install
bun run build
```

## Development

```sh
bun run watch     # rebuild gui-experimental.cjs on change
bun run typecheck # type-check without building
```

## Data source

The badge uses `ctx.client.usage.limits()`, the app's usage endpoint for the current signed-in
OpenCode Console workspace. It doesn't touch user credentials directly.
