# FelOps Backend

FelOps is being built to let businesses configure workspace agents, connect
their tools, and serve customers across channels. The planned AI Service chooses
actions; the Backend stores the rules and the planned embedded MCP module
enforces them.

This repository currently implements an Express API scaffold with
`GET /api/v1/health`, runtime configuration, and a users schema. Product flows
in the design documents are planned; no MCP code exists yet. AI Service
implementation lives in the separate `FelOps-platform/felops-ai` repository.

## Documentation

Start at [docs/README.md](docs/README.md) for the project constitution, reading
order, and documentation ownership. It links the current
[architecture](docs/architecture.md), [database design](docs/database.md), and
[delivery workflow](docs/delivery.md).

- [API setup](api/README.md): local commands, environment requirements, and the
  Apidog contract handoff.
- [Contributor onboarding](docs/onboarding/agent-onboarding.md) and the
  [coding-agent workflow](docs/onboarding/agent-workflow.md): where contributors
  and coding agents start.
- [Repository rules](AGENTS.md) and [verified metadata](agent-metadata.md):
  shared instructions, repository boundaries, and evidence of implemented
  behavior.

Edit architecture and database design in their canonical files above. Work
records under `docs/work/` link to those files and describe the change; they do
not hold separate pieces of the current architecture or schema.

## Local development

Run from the repository root:

```bash
npm ci --prefix api --ignore-scripts
npm run lint --prefix api
npm run typecheck --prefix api
npm run build --prefix api
bash bin/check-agent-workflow.sh
bash bin/check-opencode-config.sh
```

Server startup and the existing health test require Infisical bootstrap
credentials. Follow [API setup](api/README.md) for the secure environment setup
and test limitations. The root is not an npm workspace.
