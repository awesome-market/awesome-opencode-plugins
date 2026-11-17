# opencode-todo-progress

[npm](https://www.npmjs.com/package/opencode-todo-progress) · [source](https://github.com/satas20/opencode-todo-progress)

A persistent todo progress bar for the [opencode](https://opencode.ai) TUI.

Shows a compact `▓▓▓▓▓▓▓▓░░ 3/10 · current task` indicator on the right side of
the session prompt's agent/model row, next to the model name. It updates live as
todos are created/completed, and hides entirely when there are no todos.

```
┌─ opencode session ────────────────────────────────────┐
│ ...                                                   │
│                                                       │
│ > _                                                   │
│ Claude · sonnet 4    ▓▓▓▓▓▓▓▓░░ 3/4 · testing plugin  │
│ @ agents / commands          esc interrupt  12k 0.04  │
└───────────────────────────────────────────────────────┘
```

- Fill color is **warning** (amber) while in progress, **success** (green) when
  all todos are done.
- Cancelled todos are excluded from the counts.

## Install

### Recommended (npm)

```sh
opencode plugin opencode-todo-progress
```

This installs the package via Bun, detects the TUI entrypoint, and adds it to
your `tui.json` automatically. Add `-g` to install globally
(`~/.config/opencode/tui.json`).

Or add it manually:

```jsonc
// ~/.config/opencode/tui.json
{
  "$schema": "https://opencode.ai/tui.json",
  "plugin": ["opencode-todo-progress"]
}
```

opencode auto-installs npm plugins at startup.

### Local file (no build needed)

opencode transpiles `.tsx` plugins on the fly, so you can point `tui.json`
straight at the source file:

```jsonc
{
  "plugin": ["/absolute/path/to/opencode-todo-progress/src/index.tsx"]
}
```

## Develop

```sh
bun install      # dev deps (solid-js, @opencode-ai/plugin, @opentui/solid, tsc)
bun run build    # emit dist/index.js + dist/index.d.ts (for npm publish)
bun run typecheck
```

Publishing: `npm publish` (the `prepublishOnly` script runs the build
automatically).

## Requirements

- opencode >= 1.17 (TUI plugin API, `@opencode-ai/plugin/tui`)

## License

MIT
