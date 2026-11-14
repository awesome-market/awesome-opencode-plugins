# opcup

Interactive CLI to scaffold an `.opencode/` folder with frameworks, MCP tools, and skills for any project.

Works in new or existing repos.

## Quick Start

```sh
npx opcup
```

Run it in any project directory — it prompts you to select frameworks, MCP tools, and skills.

A `.opencode/` folder is generated automatically.

## What You Get

```
.opencode/
├── opencode.json       # plugins + MCP config
├── package.json        # dependencies (when a framework is selected)
├── .gitignore          # bun.lock(b), node_modules, package-lock.json, tokens/
├── .npmrc              # package-lock=false
├── commands/           # 36 Svelte + 3 generic skills
├── docs/               # bundled Svelte + example documentation
└── tokens/             # MCP token placeholders (when an MCP is selected)
```

OpenCode picks these up automatically.

No manual setup needed.

## Available Options

| Category           | Options                                                                  |
| ------------------ | ------------------------------------------------------------------------ |
| **Frameworks**     | Svelte 5 / SvelteKit 3 — `@sveltejs/opencode` plugin + 36 skills         |
| **MCP Tools**      | Sanity (mcp.sanity.io)                                                   |
| **Generic Skills** | Pure Commit (auto-group commits), Env Safety (secrets), Docs Conventions |

## Generic Skills

| Skill                                                                                                      | Description                                                                    |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [`purecommit.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/purecommit.md) | Auto-group changed files by topic into logical commits                         |
| [`env.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/env.md)               | Environment variable safety — never expose secrets in terminal output          |
| [`docs.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/docs.md)             | Writing documentation guidelines — numbered headings, Why/What/How code blocks |

## Svelte Skills

When Svelte is selected, 36 command files are generated covering the full Svelte 5 + SvelteKit 3 API:

| Skill                                                                                                                                                             | Topics                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [`svelte.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/svelte.md)                                                         | Runes, routing, data loading, forms, SvelteKit              |
| [`explicit-env-vars.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/001-explicit-env-vars/explicit-env-vars.md)             | `$app/env/private`, `$app/env/public`, `src/env.ts`         |
| [`attach.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/002-attach/attach.md)                                              | `{@attach ...}` — modern replacement for `use:action`       |
| [`function-bindings.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/003-function-bindings/function-bindings.md)             | `bind:value={get, set}` — function bindings                 |
| [`parallel-loading.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/004-parallel-loading/parallel-loading.md)                | Data loading, invalidation, `getRequestEvent`               |
| [`error-handling.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/005-error-handling/error-handling.md)                      | `handleError` kinds (`app`/`framework`/`validation`/`unknown`), `App.Error` |
| [`loading-states.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/006-loading-states/loading-states.md)                      | `$effect.pending()`, `settled()`, `tick()`                  |
| [`reactive-classes.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/007-reactive-classes/reactive-classes.md)                | `SvelteMap`, `SvelteSet`, `SvelteURL`, `MediaQuery`         |
| [`hydratable-imperative.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/008-hydratable-imperative/hydratable-imperative.md) | `hydratable()`, `mount()`, `hydrate()`, `fork()`            |
| [`images.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/009-images/images.md)                                              | `@sveltejs/enhanced-img`, CDN images, LCP best practices    |
| [`context-state.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/010-context-state/context-state.md)                         | `createContext()`, snapshots, `{#key}` blocks               |
| [`motion-transitions.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/011-motion-transitions/motion-transitions.md)          | `Spring`, `Tween`, 8 built-in transitions, easing           |
| [`template-styling.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/012-template-styling/template-styling.md)                | Declaration tags, svelte:\* elements, scoped/global styles  |
| [`typescript-svelte.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/013-typescript-svelte/typescript-svelte.md)             | Generic `$props`, `Component`/`ComponentProps` types        |
| [`remote-fns-advanced.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/014-remote-fns-advanced/remote-fns-advanced.md)       | `query.batch`, `query.live`, single-flight mutations        |
| [`platform.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/015-platform/platform.md)                                        | Accessibility, icons, auth, service workers, observability  |
| [`async-svelte.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/016-async-svelte/async-svelte.md)                            | `await` in components, synchronized updates, `$state.eager` |
| [`remote-functions.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/017-remote-functions/remote-functions.md)                | Full remote functions: query, form, command, prerender      |
| [`testing.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/018-testing/testing.md)                                           | Vitest, Playwright, `mount()`, `flushSync()`                |
| [`custom-elements.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/019-custom-elements/custom-elements.md)                   | Web components, `$host`, shadow modes                       |
| [`performance.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/020-performance/performance.md)                               | Waterfalls, preloading, optimization                        |
| [`packaging.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/021-packaging/packaging.md)                                     | `@sveltejs/package`, exports map, TypeScript                |
| [`adapters.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/022-adapters/adapters.md)                                        | Node, Cloudflare, Netlify, Vercel deployment                |
| [`glossary.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/023-glossary/glossary.md)                                        | CSR, SSR, SSG, hydration, ISR, edge                         |
| [`debugging.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/024-debugging/debugging.md)                                     | VS Code, Chrome DevTools breakpoints                        |
| [`compiler-errors.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/025-compiler-errors/compiler-errors.md)                   | Complete error code reference                               |
| [`runtime-errors.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/026-runtime-errors/runtime-errors.md)                      | All runtime errors and warnings                             |
| [`type-defs.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/027-type-defs/type-defs.md)                                     | Full SvelteKit 3 TypeScript API reference (`@sveltejs/kit/*`, `$app/*`) |
| [`faq.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/028-faq/faq.md)                                                       | Svelte + SvelteKit troubleshooting                          |
| [`compiler-warnings.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/029-compiler-warnings/compiler-warnings.md)             | A11y checks, CSS warnings, deprecated features              |
| [`svelte-5-migration.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/030-svelte-5-migration/svelte-5-migration.md)          | Upgrade guide: Svelte 4 → 5                                 |
| [`browser-support.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/031-browser-support/browser-support.md)                   | Minimum browser versions                                    |
| [`svelte-events.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/032-svelte-events/svelte-events.md)                         | `on()` from `svelte/events` for event delegation            |
| [`svelte-easing.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/033-svelte-easing/svelte-easing.md)                         | 30 easing functions for custom transitions                  |
| [`migrating-to-sveltekit-3.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/034-migrating-to-sveltekit-3/migrating-to-sveltekit-3.md) | SvelteKit 2 → 3 migration — deps, config, API moves         |
| [`svelte-all.md`](https://github.com/robots4life/opencode-setup/blob/main/template/commands/svelte/svelte-all.md)                                                 | Meta-command — loads the other 35 files at once             |

Use `/svelte` in OpenCode for quick reference, or `/svelte-all` to load the complete knowledge base.

## Merge and Overwrite

If `.opencode/` already exists, you can choose how to proceed:

| Mode          | Behavior                                                                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Merge**     | Adds missing commands, docs, and token placeholders, and merges plugins, MCP configs, and dependencies. Existing entries are never overwritten. Safe for adding to a configured project. |
| **Overwrite** | Wipes `commands/` and `docs/`, then regenerates everything from your new selection. `tokens/` is removed only when no MCP is selected; existing token files are otherwise preserved. |

In Overwrite mode, `opencode.json` and `package.json` are regenerated from your selection, so stale plugins and MCP configs are removed (if no framework is selected, no `package.json` is written). Merge mode only adds missing entries.

## Requirements

- Node.js 20+
- Generated SvelteKit 3 skills target Node.js 22.17+

## Development

```sh
npm test              # run the test suite (node:test)
npm run test:coverage # same, with a coverage report
npm run check         # format check, lint, pack validation, and tests
```

## License

MIT © robots4life
