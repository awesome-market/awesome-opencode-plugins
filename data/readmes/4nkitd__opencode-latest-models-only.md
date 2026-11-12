# opencode-latest-models-only

[![Check](https://github.com/4nkitd/opencode-latest-models-only/actions/workflows/check.yml/badge.svg)](https://github.com/4nkitd/opencode-latest-models-only/actions/workflows/check.yml)

OpenCode V2 plugin that hides models released more than 3 months ago, toggled with a single command:

```
/toggle-old-models
```

## How it works

- Release dates come from OpenCode's own model registry (`Model.Info.time.released`), which mirrors models.dev `release_date`. No network calls, no cache, works offline.
- When enabled, a `ctx.model.transform` removes every active model released before the rolling 3-calendar-month cutoff.
- Custom or self-hosted providers without catalog release data report `released: 0` and are never touched.
- Protected from removal: models explicitly listed in the global config (`~/.config/opencode/opencode.json(c)`, including top-level `model` refs) and the location's effective default model. If a config file exists but cannot be read or parsed, the filter fails open for that rebuild (models stay visible) and a warning is logged.
- Models already disabled by configuration or another plugin are left alone.

## Usage

Run the command in any session:

```
/toggle-old-models
```

It flips the filter and posts a report (count, providers, protected old models), for example:

```
Old-models filter ON (cutoff 2026-07-04). Hid 32 of 108 visible models. Providers: github-copilot 17, xai 9, opencode-go 3, openai 3. Kept 2 old models (config-pinned or default): opencode/nemotron-3-ultra-free, opencode/big-pickle. Run /toggle-old-models again to restore.
```

The command reloads the model registry of the current location, so the effect is immediate — no restart. The filter only changes the visible list; your configured defaults are protected, but a model already selected in a running session is not (see Limits).

The report is sent as a synthetic session message. OpenCode delivers these to the session agent, so the agent may acknowledge it (and speak it, if the session uses text-to-speech).

State file: `~/.config/opencode/latest-models-only.json`

```json
{
  "enabled": false,
  "updatedAt": "2026-10-04T00:00:00.000Z"
}
```

The filter starts OFF. Toggle it on when you want a clean, fresh-only model list.

## Install

Pick one of the two methods.

As an OpenCode plugin package, straight from GitHub:

```sh
opencode plugin add github:4nkitd/opencode-latest-models-only
```

Or copy the single file into the global plugin directory:

```sh
cp index.ts ~/.config/opencode/plugins/latest-models-only.ts
opencode plugin list
```

The plugin is a single dependency-free TypeScript file; the runtime needs nothing besides Node built-ins.

## Requirements

- OpenCode v2 (tested with 2.0.22)
- For development: Bun >= 1.3 and Node >= 20

## Development

```sh
bun install
bun run check   # tsc --noEmit + bun test
```

## Limits

- Only the global config is scanned for pins; project-level `opencode.json` pins are not (the location's effective default model is still protected).
- A model actively selected in a running session is not protected: if it is older than the cutoff and not pinned, it can be hidden, and that session may ask you to pick another model.
- Toggling reloads the registry of the location where the command runs. Other locations apply the new state on their next registry rebuild.
- The cutoff is computed in local time (calendar months, clamped to month length); release dates are UTC-midnight timestamps.

## License

MIT
