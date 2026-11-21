# Refract

Bootstrap greenfield or existing projects with provider-neutral instructions and native capability parity for Claude Code, Codex, OpenCode, and OhMyPi (omp). Pi remains selectable but is deprecated. Integrations and privileged behavior remain opt-in.

## How it works

Both project types converge on the same managed, validated, ownership-tracked state:

```mermaid
flowchart LR
  N["New project → refract init"] --> P
  E["Existing project → refract retrofit"] --> P
  P["Dry-run plan + preview<br/>nothing is written yet"] --> V["Deterministic validation<br/>syntax · tokens · ADRs · portable core"] --> H["Human applies<br/>staged apply · rollback-safe"] --> M["Managed state<br/>.refract/ manifest · file hashes"]
  M -. "re-run later: idempotent,<br/>unmanaged files never overwritten" .-> P
```

## Use with an agent

Point your coding agent at this repository and let it drive the bootstrap; the agent previews but never applies.

1. The agent runs bounded inspection and a dry-run preview:

   ```bash
   refract inspect --target /path/to/project

   refract retrofit \
     --agent-guided \
     --agent-intent /outside/project/intent.json \
     --dry-run \
     --plan-format json \
     --target /path/to/project
   ```

2. The agent stops and shows the plan identifier. You apply in your own interactive terminal:

   ```bash
   refract retrofit \
     --agent-guided \
     --agent-intent /outside/project/intent.json \
     --expected-plan PLAN_SHA256 \
     --target /path/to/project
   ```

After bootstrap, the generated `AGENTS.md`, progressive-disclosure docs, deterministic validators, and the project-scoped `refract` skill steer the agent through the development process. See the [agent-guided protocol](docs/AGENT_GUIDED.md) for roles, trust boundaries, and plan integrity.

### Copy-paste prompt

Install Refract once (`pip install /path/to/refract`), then paste this into your agent from your project root:

```text
Add Refract to this project in advisory mode. You may inspect and preview, but you
must never modify project files, stage, commit, or apply anything — the human applies.

1. If the `refract` CLI is unavailable, clone
   https://github.com/BlasterSystems/refract and `pip install <checkout>`.

2. Bounded, read-only inspection (JSON evidence only; do not add --include-snippets):

   refract inspect --target .

3. From the evidence, write a strict proposal to /tmp/refract-intent.json (outside
   this repo). Only these fields are accepted; anything else is rejected:

   {
     "schema": "refract-intent/v1",
     "project": {
       "name": "<from evidence>",
       "description": "<from evidence>",
       "build_command": "<from evidence or null>",
       "test_command": "<from evidence or null>",
       "run_command": null,
       "ticket_prefix": null
     },
     "features": {
       "platforms": ["<harnesses this project uses>"],
       "mcp": false,
       "agents": false,
       "github": false,
       "scheduled_audit": false,
       "hooks": false
     }
   }

   Valid platforms: claude, codex, pi, opencode, omp. Leave every privileged
   feature false and ask me before enabling any. Never include credentials, file
   contents, or fields outside the schema. Do not read .env, key files, or other
   known secret locations.

4. Deterministic dry-run preview (writes only to stdout):

   refract retrofit --agent-guided --agent-intent /tmp/refract-intent.json \
     --dry-run --plan-format json --target .

5. STOP. Report the plan identifier and every planned operation. Flag any update
   or removal of an existing file for exact diff review in my terminal, plus any
   conflicts (unmanaged files are never overwritten). Do not apply.

6. Wait for me. I will apply in my own interactive terminal:

   refract retrofit --agent-guided --agent-intent /tmp/refract-intent.json \
     --expected-plan <PLAN_SHA256> --target .
```

## Supported harnesses

First-class adapters render each capability (permissions, skill invocation, subagents, MCP, deterministic agent hooks) in the platform's native format (ADR-0010):

- Claude Code (`CLAUDE.md`, `.claude/settings.json`, `.claude/skills`, `.claude/agents/`, `.mcp.json`)
- OpenAI Codex (`AGENTS.md`, `.agents/skills`, `.codex/config.toml`, `.codex/hooks.json`, `.codex/agents/`)
- OpenCode (`AGENTS.md`, `.agents/skills`, `opencode.json`, `.opencode/commands|agents|plugins`)
- OhMyPi (omp) (`AGENTS.md`, `.agents/skills`, `.omp/settings.json`, `.omp/RULES.md`, `.omp/agents/`, `.omp/mcp.json`, `.omp/hooks/`)
- Pi Coding Agent: deprecated; portable core only (`AGENTS.md`, `.agents/skills`)

Restrictive permission policies are opt-in (`--permissions`). refract writes only inside the target project and refuses home directories or folders that group several repositories (`--allow-unscoped-target` overrides).

See the [platform support matrix](docs/PLATFORM_SUPPORT.md) for verified versions and support levels.

## Agentic workflow skills

Every generated project ships a portable, provider-neutral skill chain (ADR-0011), invocable by name on each supported agent:

| Stage | Skills |
|---|---|
| Plan before code | `research` (evidence-grounded plan in `tasks/`; tickets only after approval), `confidence-check` |
| Build one ticket | `implement` (task file, branch, tests, validation, pull request; never deploys) |
| Quality gates | `security-check`, `quality-review`, `commit` (conventional commit plus a living `docs/branches/` document) |
| Ship | `deploy-dev`, `deploy-prd`, `hotfix`: tag-driven, explicit-request-only, and inactive until `docs/DEPLOYMENT.md` is configured |

The skills contain no project keys, hosts, languages, or tracker APIs. Project specifics live in project-owned seeds (`docs/DEPLOYMENT.md`, `docs/DEVELOPMENT_PROCESS.md`, `tasks/task-template.md`), which refract never overwrites after you edit them.

## Quick start

Requires Python 3.11+.

Clone or download this repository, then run from its checkout:

```bash
cd refract
python3 -m pip install -e .

# Preview an all-platform project without writing files
refract init --platform all --dry-run --yes --target /path/to/project

# Initialize a minimal omp project
refract init --platform omp --yes --target /path/to/project

# Add the portable core and selected adapters to an existing project
refract retrofit --platform claude,codex,opencode,omp \
  --dry-run --yes --target /path/to/project

# Inspect bounded evidence without changing the project
refract inspect --target /path/to/project

# Validate generated configuration
refract validate --target /path/to/project
```

The repository-local entry point works without installation:

```bash
scripts/refract.sh init --platform all --dry-run --yes --target /path/to/project
```

## Optional features

```text
--mcp              Native MCP configuration where supported
--agents           Specialized-agent definitions where supported
--github           GitHub documentation-check workflow
--scheduled-audit  Weekly docs-check schedule; implies --github
--hooks            Git hooks without changing Git configuration
--answers FILE     Confirmed project and feature answers as JSON
--agent-guided     LLM-advisory preview with separate human apply
--agent-intent FILE Strict unverified proposal for agent-guided mode
--expected-plan ID Integrity check for interactive human apply
--plan-format json Machine-readable plan
--remove-obsolete  Explicitly remove obsolete manifest-owned files
```

See the [answers-file reference](docs/ANSWERS.md) for trusted-caller JSON and the [agent-guided protocol](docs/AGENT_GUIDED.md) for bounded inspection, typed proposals, preview, and trusted-terminal handoff. Unmanaged files are never overwritten; start with `--dry-run` when retrofitting.

## Documentation: load progressively

Read only what the current task requires:

1. **Start here:** [documentation index](docs/README.md)
2. **Contributing:** [development process](docs/DEVELOPMENT_PROCESS.md)
3. **Architecture:** [architecture overview](docs/ARCHITECTURE.md), then the [ADR index](docs/adr/README.md) before individual decisions
4. **Platform details:** [support matrix](docs/PLATFORM_SUPPORT.md)
5. **Generated files:** [exact all-feature output](docs/GENERATED_OUTPUT.md)
6. **Releases:** [Semantic Versioning and Git tags](docs/RELEASING.md)
7. **Knowledge strategy:** [LLM Wiki evaluation and pilot plan](docs/LLM_WIKI_EVALUATION.md)

## Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m refract validate --target .
```

## Credits

- [Cloudflare security-audit-skill](https://github.com/cloudflare/security-audit-skill) — the optional security-audit integration ([ADR-0006](docs/adr/0006-opt-in-security-audit-skill.md)) documents and orchestrates this MIT-licensed skill. The skill itself is installed on demand and remains the work of its authors.
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) and [emiliosheinz/agent-skills](https://github.com/emiliosheinz/agent-skills) — the optional task-breakdown and ticket-creation integrations ([ADR-0007](docs/adr/0007-install-on-demand-task-breakdown-skills.md)) document these MIT-licensed skills, installed on demand.
- [vercel-labs/skills](https://github.com/vercel-labs/skills) — the open skills CLI that the documented `npx skills add` install flows for both integrations run on.
- [gitleaks](https://github.com/gitleaks/gitleaks) — optional staged-change credential scan in the generated Git pre-commit hook.

## License

Apache-2.0 — see [LICENSE](LICENSE).
