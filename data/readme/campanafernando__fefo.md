# FEFO

**Flow Execution via Federated Ontology.**

FEFO is a whitelabel workspace for OpenCode that federates independent Git
repositories into one context. It keeps each repository's history, dependencies,
and tests, while giving the agent one routing layer, one knowledge vault, one
MCP gateway, and one set of modular subagents.

OpenCode is the canonical harness. FEFO also generates adapters for Claude Code,
Cursor, and GitHub Copilot from the same source, so a team can use different
harnesses without forking the instructions.

> FEFO is the template and reference implementation. The OpenCode plugin is the
> lightweight runtime for an existing workspace, and `opencode-zshell` exposes
> the same commands from zsh.

## Why

Most agent workspaces fail in one of two ways:

1. **One giant repository** — every instruction, skill, and agent lives in one
   place, and unrelated projects leak into each other.
2. **One agent per repository** — context, contracts, and conventions drift
   because no layer owns the federation.

FEFO keeps repositories independent and makes the federation explicit:

- `AGENTS.md` is the routing contract.
- `.fefo/workspace.json` is the source of truth.
- `docs/vault/` is the durable knowledge graph.
- `codegraph-<repo>` MCP servers give each repository its own index.
- `.opencode/agents/` is a modular agent base.
- Generated adapters keep Claude, Cursor, and Copilot aligned.

## Quick start

Requirements: Git, Python 3.10+, OpenCode 2.2.7+, and the CodeGraph CLI on
`PATH` for indexing (optional but recommended).

```sh
git clone https://github.com/campanafernando/FEFO.git my-workspace
cd my-workspace

# Register the repositories that will join the federation.
./bin/fefo init --name "My Workspace" \
  --repo ../api \
  --repo ../web
```

Or interactively:

```sh
./bin/fefo init
```

Then open OpenCode at the workspace root:

```sh
opencode
```

The generated entry point is the `fefo` agent. From there:

```text
/fefo-add ../worker --role data
/fefo-index
/fefo-status
/fefo-doctor
```

## What FEFO generates

| File | Purpose |
|---|---|
| `.fefo/workspace.json` | Source of truth: repos, roles, stacks, MCP servers, model |
| `opencode.json` | OpenCode model, agents, references, permissions, MCP gateway |
| `.mcp.json` | Claude Code MCP configuration |
| `.claude/` | Claude agents, skills, commands, settings |
| `CLAUDE.md` | Claude entry point that imports `AGENTS.md` |
| `.cursor/rules/fefo.mdc` | Cursor project rule |
| `.github/copilot-instructions.md` | GitHub Copilot instructions |
| `AGENTS.md` | Generated routing contract and repository table |
| `AGENTS.local.md` | User-owned local instructions; never overwritten |
| `docs/vault/` | Knowledge vault, federation snapshot, per-repo notes |
| `codegraph/README.md` | Index and MCP guidance |

Generated files are replaced by `./bin/fefo sync`. Put user-owned text in
`AGENTS.local.md` and `docs/vault/`.

## Repository roles

| Role | Use when |
|---|---|
| `api` | Django, DRF, FastAPI, Flask, or another HTTP backend |
| `web` | Next.js, React, or another web client |
| `mobile` | Flutter or a native mobile client |
| `data` | ETL, analytics, warehouse, or data quality |
| `infra` | Containers, CI/CD, deployment, or operations |
| `legacy` | Legacy systems and compatibility bridges |
| `integration` | External APIs, webhooks, or scrapers |
| `docs` | Documentation-only repository |
| `service` | Shared service or library |
| `library` | Reusable package |
| `orchestrator` | Another holding repository |

FEFO detects Django, FastAPI, Flask, Next.js, React, Flutter, docs, and
infrastructure stacks. Override detection with `--stack`, `--role`, `--test`,
`--lint`, and `--build`.

## MCP gateway

CodeGraph is the default. FEFO creates one local server per repository:

```jsonc
{
  "mcp": {
    "servers": {
      "codegraph-api": {
        "type": "local",
        "command": ["codegraph", "serve", "--mcp", "--path", "../api"]
      }
    }
  }
}
```

Add another MCP without editing JSON:

```sh
./bin/fefo mcp add docs --local -- npx -y @modelcontextprotocol/server-filesystem ./docs
./bin/fefo mcp add sentry --remote https://mcp.sentry.dev/mcp
./bin/fefo mcp list
./bin/fefo mcp remove docs
```

Local MCPs are mirrored to Claude Code. Remote MCPs with `{file:...}` or
`{env:...}` credentials stay OpenCode-only by default; see
[`docs/harnesses.md`](docs/harnesses.md).

## Agent base

FEFO ships a modular base, not a monolith:

- **Orchestration:** `fefo`, `backend`, `frontend`
- **Backend layers:** `model`, `service`, `selector`, `serializer`, `migration`, `test`, `lint`
- **Data:** `database`, `data`
- **Web layers:** `form`, `table`, `api-layer`, `design`, `i18n`
- **Cross-cutting:** `cross-stack`, `architect`, `security`, `infra`, `legacy`, `integration`
- **Extension:** `specialist` template

No agent hardcodes a model. Agents inherit the session model. See
[`docs/agents.md`](docs/agents.md) for the full catalog and routing.

## Knowledge vault

`docs/vault/` is the durable knowledge graph:

- `00-INDEX.md` — entry point
- `federation.md` — generated snapshot of the workspace
- `repos/<name>.md` — generated repository facts + user-owned domain notes
- `decisions.md` — durable decisions

The vault is for knowledge that cannot be derived from symbols: product rules,
contracts, provenance, source hierarchies, and decisions. CodeGraph is for code.

## Harnesses

OpenCode is canonical. FEFO derives the rest:

| Harness | Entry point |
|---|---|
| OpenCode | `opencode.json`, `.opencode/agents`, `.opencode/commands`, `.agents/skills` |
| Claude Code | `.mcp.json`, `.claude/`, `CLAUDE.md` |
| Cursor | `.cursor/rules/fefo.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |

See [`docs/harnesses.md`](docs/harnesses.md) for the adapter contract and
limitations.

## Provider recommendation

FEFO does not require a provider. Choose the provider and model your account
supports in `opencode.json` or through the OpenCode model picker.

Our recommendation for FEFO workspaces is **OpenCode Go** with
**`deepseek-v4.1-flash`**. It has strong tool use, low latency, predictable cost,
and a free Zen variant for experiments. Change it in `.fefo/workspace.json`:

```sh
# edit provider.model, then:
./bin/fefo sync
```

Agents never pin a model, so switching providers is a workspace-level decision.

## Ecosystem

| Project | Use it when |
|---|---|
| **FEFO** (this repository) | You want the reference template, agents, vault, and CLI |
| **`opencode-fefo` plugin** | You want FEFO commands inside an existing OpenCode workspace ([repo](https://github.com/campanafernando/opencode-fefo)) |
| **`opencode-zshell`** | You want zsh helpers that call the plugin and OpenCode ([repo](https://github.com/campanafernando/opencode-zshell)) |

## CLI

```sh
./bin/fefo init                 # create the workspace manifest
./bin/fefo add <path>           # add or update a repository
./bin/fefo remove <name>        # remove a repository
./bin/fefo sync                 # regenerate config and harness adapters
./bin/fefo index [name...]      # refresh CodeGraph indexes
./bin/fefo status               # repository and index overview
./bin/fefo doctor               # validate the workspace
./bin/fefo mcp add|remove|list  # manage additional MCP servers
```

Run `./bin/fefo <command> --help` for flags.

## Design principles

1. **Federate, do not merge.** Repositories keep their own Git history and
   delivery pipeline.
2. **One source of truth.** The manifest drives every generated adapter.
3. **CodeGraph first for code, vault for knowledge.**
4. **Contract first across repositories.**
5. **Modular agents, inherited model.**
6. **No silent destructive actions.** Git history changes require authorization.
7. **Generated files are disposable; local instructions are not.**

## Roadmap

See [`docs/roadmap.md`](docs/roadmap.md). The next increments are the
`opencode-fefo` plugin, the `opencode-zshell` integration, vault graph export,
and a workspace bootstrap path for users who do not want to clone the template.

## License

MIT. See [`LICENSE`](LICENSE).
