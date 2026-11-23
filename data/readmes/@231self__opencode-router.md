# opencode-router

Per-turn model routing and context management for **OpenCode V2** and
**Kilo** — a workspace of three packages sharing one pricing brain, one
security gate, and one staged release pipeline.

| Package | Role |
|---|---|
| [`@231self/opencode-router`](packages/router) | Routes each turn to the best model from your pool (small local judge + deterministic floor), with pins, failover, subagent policy, a TUI `/router` surface, and a CLI. |
| [`@231self/opencode-compaction`](packages/compaction) | Context management: the context optimiser, a priced compact/keep/delegate advisory (`/ctx`), and `/ctx here`. |
| [`@231self/opencode-shared`](packages/shared) | Shared runtime: cache-aware pricing/measurement, config/state host adapters, Kilo shim, model-ref semantics. Zero dependencies. |

```sh
opencode plugin add @231self/opencode-router
opencode plugin add @231self/opencode-compaction
```

- User docs: [`packages/router/README.md`](packages/router/README.md)
- Architecture: [`docs/architecture.md`](docs/architecture.md)
- Benchmarks: [`docs/benchmarks/`](docs/benchmarks) (routing reports regenerated
  for 0.3.0; live compaction tolerance run still pending)
- Research: [`docs/paper/draft.md`](docs/paper/draft.md) — cache-aware
  compaction economics
- Releasing: [`docs/releasing.md`](docs/releasing.md) (CI stages over npm
  trusted publishing; a maintainer approves with 2FA)
- Designs: [`docs/specs/`](docs/specs), [`docs/superpowers/`](docs/superpowers)

Licensed Apache-2.0.
