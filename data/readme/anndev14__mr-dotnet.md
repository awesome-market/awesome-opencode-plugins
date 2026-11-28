# Mr. Dotnet

**A model-agnostic .NET/C# agent for OpenCode V2.**  
It adapts to modular monoliths, layered CRUD apps, legacy databases and background workers — without imposing an architecture on the repository.

[Español](README.es.md) · [MIT License](LICENSE)

## Why

Most .NET "AI agents" assume a clean architecture, a single database provider and a fresh codebase. Real repositories rarely look like that.

Mr. Dotnet starts with recon:

- What is the archetype?
- How is the database owned and mapped?
- What are the conventions, target framework and error contract?
- What can be changed safely?

Then it makes the smallest correct change.

## Features

- **Adaptive:** modular monolith, layered CRUD, legacy layered CRUD, Minimal API, Dapper, workers/Quartz.
- **Legacy-safe:** treats an immutable database as a contract; no migrations, renames or "normalization" unless explicitly authorized.
- **No architecture imposition:** keeps `ApiResponse`, generic repositories, controllers or `ProblemDetails` if that is what the repo already uses.
- **Model-agnostic:** no `model:` in the agent; it uses the model selected in OpenCode.
- **Skills on demand:** architecture, error handling, testing and PostgreSQL RLS are loaded only when relevant.
- **Cautious permissions:** destructive git, EF Core and NuGet commands ask first.

## Requirements

- [OpenCode V2](https://opencode.ai/v2/docs/) (tested on 2.0.x).
- A model with tool calling for edits and shell commands. Chat-only models can answer but cannot modify files.
- Recommended context: 32k+; 64k+ for large repositories.
- Optional: [Context7 MCP](https://context7.com/) for current library documentation.

## Install

### Global (all projects)

```bash
git clone https://github.com/Anndev14/mr-dotnet.git
cd mr-dotnet
./install.sh
```

This copies:

```text
~/.config/opencode/agents/mr-dotnet.md
~/.config/opencode/skills/<skill>/SKILL.md
```

If a file already exists, the installer skips it. Use `--force` to overwrite (a timestamped backup is created).

### Project-local (recommended for teams)

```bash
./install.sh --project /path/to/your/repo
```

This copies the agent and skills into:

```text
<repo>/.opencode/agents/mr-dotnet.md
<repo>/.opencode/skills/<skill>/SKILL.md
```

Commit `.opencode/` so everyone on the team gets the same agent and skills.

### Manual

Copy `agents/mr-dotnet.md` to your global or project `.opencode/agents/` directory, and each directory under `skills/` to the matching `.opencode/skills/` directory.

### Verify

```bash
opencode debug agents
```

Look for `mr-dotnet` in the list. In the TUI, open the agent picker and select **Mr. Dotnet**.

## Usage

```bash
opencode run --agent mr-dotnet "review this controller"
opencode run --agent mr-dotnet -m <provider/model> "add a health endpoint"
```

The agent does not pin a model, so `-m` (or the model selected in the TUI) decides. List configured models with:

```bash
opencode models
```

To make it the default primary agent for new sessions:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "mr-dotnet"
}
```

Changing the default agent does not change the model of existing sessions.

## What it does

| Archetype | Signals | Behaviour |
|---|---|---|
| Modular monolith | `src/Modules/*`, `SharedKernel`, `*.Contracts` | Follows module boundaries and existing CQRS/Result patterns. |
| Layered CRUD | `Controllers/`, `Services/`, `Repositories/` | Fits the existing layers; no forced CQRS. |
| Legacy layered CRUD | `API` + `Core` + `Infrastructure`, `IGenericRepository<>`, Specifications | Keeps the existing structure and error envelope. |
| Minimal API | `MapGroup`, endpoints in `Program.cs` | Extends the existing endpoint style. |
| Dapper / raw SQL | SQL strings, `IDbConnection` | Parameterized queries; respects the schema. |
| Worker / background | `BackgroundService`, `IHostedService`, Quartz `IJob` | Treats it as a worker, not an API. |

## Included skills

| Skill | Use |
|---|---|
| `dotnet-backend-architecture` | Modules, CQRS, EF Core patterns, Outbox, multi-tenancy, auth. Only when the project already follows it or the user asks. |
| `dotnet-error-handling` | `Result`/`Error`, `ProblemDetails`, validation and exception mapping. |
| `dotnet-testing` | Unit, integration, API and architecture tests. |
| `postgres-rls` | PostgreSQL Row-Level Security. |
| `context7-mcp` | Optional current documentation for libraries and frameworks. Falls back to lockfiles and official docs. |

## Model compatibility

The agent is model-agnostic by design:

- No `model:` in the frontmatter.
- No provider-specific prompt tricks or request overrides.
- Skills are loaded on demand, so the base prompt stays small.
- The system prompt is in English; the agent replies in the user's language.

Smoke-tested with `opencode/deepseek-v4.1-flash-free` and `flint-40b-free`. See [docs/models.md](docs/models.md) for the matrix and known caveats.

## Customization

- Edit `agents/mr-dotnet.md` to change the system prompt.
- Add a skill under `skills/<id>/SKILL.md`; run `bash scripts/validate.sh`.
- Keep the agent free of `model:` if you want it to remain model-agnostic.
- Project conventions belong in the repository's `AGENTS.md`, not in this global agent.

## Troubleshooting

**The agent does not appear.**  
Check that the file is at `~/.config/opencode/agents/mr-dotnet.md` or `<repo>/.opencode/agents/mr-dotnet.md`. Run `opencode debug agents`.

**A skill does not load.**  
Check that the directory is `skills/<id>/SKILL.md` and that the ID matches the directory name. Run `bash scripts/validate.sh`.

**The model does not edit files.**  
Use a model with tool calling. Chat-only models can explain but cannot run tools.

**Context7 is not configured.**  
The agent falls back to `dotnet list package`, lockfiles and official documentation. See `examples/opencode.jsonc` for an optional MCP setup.

## Repository layout

```text
agents/mr-dotnet.md      # the agent
skills/                  # on-demand skills
install.sh               # global/project installer
uninstall.sh             # removes the installed agent and skills
scripts/validate.sh      # repository checks
docs/                    # model matrix and archetypes
examples/                # config and smoke tests
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep personal paths, secrets and project-specific rules out of the repository.

## License

MIT © 2026 anndev. See [LICENSE](LICENSE).

---

Not affiliated with Microsoft. .NET is a trademark of Microsoft.
