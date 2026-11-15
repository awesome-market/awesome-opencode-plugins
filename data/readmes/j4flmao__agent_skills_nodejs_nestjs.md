# Agent Skills — Node.js (TypeScript) & NestJS

A curated, production-ready set of **Agent Skills** that teach an AI coding agent
how to write, review, and refactor backend code in **Node.js + TypeScript** and
**NestJS** following strict OOP, strong typing, design-pattern, and decoupling
rules.

The skills are written so that any AI agent can read them and immediately:

- understand the **architecture** the codebase must follow,
- generate code that is **OOP-first**, **generic-typed** (`Type<T>`), and
  **decoupled** (low coupling, high cohesion),
- apply the right **design pattern** for the problem at hand,
- separate **business logic** from transport, persistence, and infrastructure,
- be safe to use in both **development** and **production**.

---

## Quick start

1. Drop the `.agents/` folder into your project root (or copy individual skills
   into `~/.config/agents/skills/`).
2. Open the project with any agent that supports the Agent Skills protocol.
3. Ask the agent to load a skill, e.g.
   *"Load the `designing-oop-typescript` skill and refactor `user.service.ts`."*

## Phases

```diagram
╭───────────────────────────────╮
│ Phase 0 — Rule base / meta    │  conventions every skill must obey
╰──────────────┬────────────────╯
               ▼
╭───────────────────────────────╮
│ Phase 1 — Node.js + TypeScript│  OOP, generics, patterns, decoupling
╰──────────────┬────────────────╯
               ▼
╭───────────────────────────────╮
│ Phase 2 — NestJS              │  modules, DTOs, guards, persistence
╰───────────────────────────────╯
```

## Skill index

### Phase 0 — Rule base
- `_conventions` — how each skill in this pack is structured and consumed.

### Phase 1 — Node.js + TypeScript
- `nodejs-typescript-foundation` — tsconfig, lint, package layout, scripts.
- `designing-oop-typescript` — classes, encapsulation, SOLID in TS.
- `typing-generic-responses` — `ApiResponse<T>`, `Result<T,E>`, `Paginated<T>`.
- `applying-design-patterns` — creational, structural, behavioral patterns.
- `decoupling-with-di` — interfaces, DI container, ports & adapters.
- `separating-business-logic` — domain / application / infrastructure layers.
- `handling-errors-typescript` — typed error hierarchy, never swallow errors.
- `structuring-project-layout` — folders, barrels, module boundaries.
- `testing-typescript-services` — unit, integration, contract testing.
- `managing-configuration` — env validation, schema, secrets.
- `logging-and-observability` — structured logs, traces, metrics.
- `securing-nodejs-apps` — input validation, headers, auth basics.

### Phase 2 — NestJS
- `architecting-nestjs-modules` — feature modules, dependency boundaries.
- `building-nestjs-controllers` — thin controllers, DTOs, versioning.
- `designing-nestjs-services` — application services, no framework leak.
- `validating-nestjs-dtos` — class-validator + class-transformer.
- `using-nestjs-pipes-guards-interceptors` — cross-cutting concerns.
- `handling-nestjs-exceptions` — exception filters, HTTP mapping.
- `persisting-data-with-typeorm` — repository pattern, transactions.
- `testing-nestjs-applications` — Test module, e2e with Supertest.
- `deploying-nestjs-production` — config, health, graceful shutdown.

## License

MIT.
