# opencode-ast-grep

[![CI](https://github.com/donbowman/opencode-ast-grep/actions/workflows/ci.yml/badge.svg)](https://github.com/donbowman/opencode-ast-grep/actions/workflows/ci.yml)

An [OpenCode](https://opencode.ai) v2 plugin that exposes
[ast-grep](https://ast-grep.github.io/) structural search and rewrite as two
first-class tools, so the agent reaches for syntax-aware tooling when the task
is about the *shape* of code instead of plain text.

| Tool | What it does |
|---|---|
| `ast_grep_search` | Finds code by AST pattern: calls with arguments, JSX, declarations, nesting, missing guards. Returns compact `file:line:column` matches. |
| `ast_grep_edit` | Multi-file structural rewrite that preserves surrounding formatting. Dry-run diff by default; `apply=true` writes. |

## Why a plugin

Tool registration puts ast-grep at the same decision level as
`grep`/`read`/`edit`. A line in `AGENTS.md` competes with whatever tool the
model already reaches for; a registered tool with a trigger-shaped description
is chosen when the task is structural. The tools validate arguments, run the
local `ast-grep` binary directly (never through a shell), ask the CLI for
compact JSON, and fail soft with a readable message.

## Requirements

- OpenCode v2
- `ast-grep` 0.40+ on `PATH` (`pip install ast-grep-cli`,
  `npm i -g @ast-grep/cli`, `cargo install ast-grep --locked`, or
  `brew install ast-grep`)

## Install

### Copy into the plugins directory (no config needed)

```sh
mkdir -p ~/.config/opencode/plugins/ast-grep
cp index.ts ~/.config/opencode/plugins/ast-grep/
```

OpenCode v2 auto-discovers plugin directories under
`~/.config/opencode/plugins/`. The file watcher picks the new file up; if it
does not, run `opencode service restart`. No `opencode.jsonc` change is
required. The plugin has **no runtime dependencies** — `index.ts` is executed
by the host as-is.

### Point config at the clone

```jsonc
// ~/.config/opencode/opencode.jsonc
{
  "plugins": ["/absolute/path/to/opencode-ast-grep"]
}
```

### Verify it loaded

```sh
opencode plugin list       # should list: ast-grep  local  .../ast-grep/index.ts
```

Then ask for something structural, for example "find every `console.log` call
with its arguments" or "rename all `oldApi(...)` calls to `newApi(...)` under
`src`".

## Usage

`ast_grep_search`:

```jsonc
// pattern is code with metavariables: $A one node, $$$ many, $_ no capture
{ "pattern": "console.log($$$ARGS)", "lang": "ts", "paths": ["src"] }
{ "pattern": "$A && $A()", "globs": ["!**/node_modules/**"], "limit": 50 }
```

`ast_grep_edit`:

```jsonc
// 1) preview: returns a diff, writes nothing (default)
{ "pattern": "console.log($$$ARGS)", "rewrite": "logger.info($$$ARGS)", "lang": "ts" }

// 2) apply
{ "pattern": "console.log($$$ARGS)", "rewrite": "logger.info($$$ARGS)", "lang": "ts", "apply": true }
```

Both tools accept `lang`, `paths`, `globs` and `strictness`
(`cst` | `smart` | `ast` | `relaxed` | `signature` | `template`). Search also
accepts `context` (lines around each match) and `limit`; edit also accepts
`apply`.

Pattern notes:

- Patterns are code, not regex. A `run` pattern matches a whole AST node, so
  `std::env::var($X)` does not match a bare `env::var($X)`; try both forms.
- `$$$` absorbs any number of nodes; useful for argument lists and bodies.
- Zero matches is a normal result (reported as such), not an error.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `AST_GREP_BIN` | auto-detected | Path to the `ast-grep` binary. When unset, `ast-grep` then `sg` are probed; the `sg` fallback verifies it really is ast-grep (Linux also ships `sg` as setgroups(1)). |

Timeouts are fixed (20s search, 30s edit) and output is truncated at ~50k
characters so a huge match set cannot flood the context.

## Development

```sh
npm install
npm test          # typecheck + smoke test (needs ast-grep on PATH or AST_GREP_BIN)
npm run typecheck # tsc --noEmit
npm run smoke     # node test/smoke.ts
```

The smoke test loads the plugin through a mock OpenCode host and exercises both
tools against a temporary fixture: registration, structured search results,
zero-match handling, argument validation, dry-run diffs and apply semantics.

## Related

- ast-grep docs: <https://ast-grep.github.io/> (patterns, rules, rewrite)
- The ast-grep skill for agents: <https://github.com/ast-grep/claude-skill>

## License

MIT — see [LICENSE](LICENSE).
