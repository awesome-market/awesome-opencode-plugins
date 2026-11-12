<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/opencode.svg" width="100" alt="opencode logo" />
  <h1>OpenCode Developer Workflow Pack</h1>
  <p>A reusable, <strong>profile-based</strong> <a href="https://opencode.ai">OpenCode</a> configuration from HumbleBee AI. Each profile is a small engineering team scoped to one kind of work — only the commands, skills, agents, and MCP servers that profile actually needs.</p>
</div>

---

## Install

One command, run **inside the project you want to set up**. It fetches just that profile and leaves no installer artifacts behind:

```bash
curl -fsSL https://raw.githubusercontent.com/humblebeeai/opencode/main/install.sh | bash -s -- <profile>
```

```bash
# frontend project
curl -fsSL https://raw.githubusercontent.com/humblebeeai/opencode/main/install.sh | bash -s -- frontend

# omit the profile for fullstack (everything)
curl -fsSL https://raw.githubusercontent.com/humblebeeai/opencode/main/install.sh | bash
```

Profiles: `frontend` `backend` `infra` `fullstack` `fastapi` `nextjs` `python-sdk` `docs` `docker`.

It drops the profile's `.opencode/`, `opencode.json`, `AGENTS.md`, `.env.example`, and `.ignore` into the current directory — backing up an existing `.opencode/` and never clobbering an existing `opencode.json`/`AGENTS.md` — then you run `opencode`. The download goes to a temp dir that's cleaned up on exit, so nothing but the profile is left behind.

Overrides (env vars): `OPENCODE_PACK_REF` (branch/tag, default `main`), `OPENCODE_PACK_TARGET` (default: current dir), `OPENCODE_PACK_PROFILE`.

## Why profiles

OpenCode discovers every command in `.opencode/commands/` and can't hide them through config. So instead of one bloated setup where a frontend engineer sees Docker, Nginx, and database commands, the pack ships **self-contained profiles** — each its own `.opencode/`, `opencode.json`, and docs. You install the profile that matches your work and get a lean, focused toolset.

| Profile     | Commands                                                                   | Skills                                   | MCP servers              |
| ----------- | ------------------------------------------------------------------------- | ---------------------------------------- | ------------------------ |
| `frontend`  | architect, frontend, test, review, refactor, commit, docs                 | frontend, testing                        | context7, playwright     |
| `backend`   | architect, backend, security, test, review, refactor, commit, docs        | backend, security, testing               | context7, postgres       |
| `infra`     | architect, docker, compose, nginx, github-actions, deploy, deploy-check, security, test, review, refactor, commit, docs | docker, compose, nginx, github-actions, deployment, security, testing | context7, github         |
| `fullstack` | everything (all 16 commands)                                              | all                                      | context7, playwright, github, postgres, linear |

Every profile includes the shared core — `architect`, `test`, `review`, `refactor`, `commit`, `docs` — plus the matching read-only analyzer subagents. `security` is in backend/infra/fullstack; `linear` lives only in fullstack.

### Framework profiles

Narrower specializations that layer HumbleBee's framework conventions (as a loadable skill) on top of a domain base. The skills also ship in `fullstack`.

| Profile      | Based on            | Convention skill          | Notes                                                       |
| ------------ | ------------------- | ------------------------- | ---------------------------------------------------------- |
| `fastapi`    | backend             | `frameworks/fastapi`      | scaffolds from `rest-fastapi-template` / `-orm-template`    |
| `nextjs`     | frontend            | `frameworks/nextjs`       | Next.js App Router + shadcn/ui                              |
| `python-sdk` | backend (lean)      | `frameworks/python-sdk`   | scaffolds from `module-python-template`                     |
| `docs`       | docs + core         | `frameworks/docs-mkdocs`  | scaffolds from `docs-mkdocs-template`                       |
| `docker`     | docker + compose    | `infra/docker` (enriched) | ships `reference.Dockerfile` + `docker-entrypoint.sh`; conventions enforced by the docker-build analyzer |

The `docker` skill encodes the required Dockerfile conventions — `# syntax` directive, version-pinned base, multi-stage builds, BuildKit cache/bind mounts, non-root user (with root→user drop in the entrypoint), and `docker-entrypoint.sh` that `exec`s under `tini`. Compose: `compose.yml` (not `docker-compose.yml`) and no fixed `container_name`.

## Requirements

- [OpenCode](https://opencode.ai): `npm install -g opencode-ai`
- A model configured in OpenCode. The pack is **provider-agnostic** — it pins no model, so every agent and command uses your configured default (Anthropic, OpenAI, any provider). Set one by running `opencode` and picking a model.

## Environment & MCP servers

After installing, from your project root:

```bash
cp .env.example .env
```

If the project already has a `.env` or `.env.example`, the installer doesn't overwrite them — it **appends** this profile's variables under a labeled `# --- opencode pack: <profile> profile ---` block, skipping any key you've already set (so real values in `.env` are never touched).

`context7` (live library docs) is enabled in every profile and needs no credentials. The rest are scoped per profile and only need setup when you use them:

| Server       | In profiles            | Default      | Needs                          |
| ------------ | ---------------------- | ------------ | ------------------------------ |
| `context7`   | all                    | **enabled**  | nothing                        |
| `playwright` | frontend, fullstack    | **enabled**  | nothing (downloads a browser)  |
| `postgres`   | backend, fullstack     | disabled     | `DATABASE_URL`                 |
| `github`     | infra, fullstack       | disabled     | `GITHUB_TOKEN`                 |
| `linear`     | fullstack              | disabled     | Linear OAuth (backs `/linear`) |

Credentialed servers ship disabled so a fresh install never errors. Flip `"enabled": true` in `opencode.json` and add the env var to enable one.

## Permissions

`bash` runs under a pattern allow-list (the same in every profile): read-only inspection, version checks, linters/formatters, and test runners run without a prompt; state-changing git and unrecognized commands prompt; destructive commands (`rm -rf`, `sudo`, `git push --force`, …) are denied. Subagents are fully read-only. Details and the full list are in each profile's `AGENTS.md` and `opencode.json` → `permission.bash`.

## Customizing & extending

Every profile under `profiles/` is **self-contained and edited directly** — there's no build step. `fullstack` is the complete set; the others are scoped subsets of it.

- **Change a profile** — edit its files under `profiles/<name>/.opencode/`, its `profiles/<name>/opencode.json`, or its `profiles/<name>/AGENTS.md`.
- **Change something shared** (a core agent, a skill, the bash allow-list) — apply it to each profile that includes it; `fullstack` is the reference for the full set.
- **Add a profile** — copy the closest existing one and trim it:

  ```bash
  cp -R profiles/backend profiles/fastapi
  # then trim .opencode/ to what you need, adjust opencode.json (MCPs, default_agent),
  # and update AGENTS.md to match
  ```

Keep each profile's `AGENTS.md` command/agent/skill list in sync with the files actually in its `.opencode/`. To try a profile from a clone without installing: `cd profiles/<name> && opencode`.

## Repo structure

```
.
├── README.md
├── install.sh                 # the curl-pipe installer
└── profiles/                  # the deliverable — one self-contained config per profile
    ├── fullstack/             # the complete set (all commands, agents, skills, MCPs)
    │   ├── .opencode/{agents,commands,skills}/
    │   ├── opencode.json
    │   ├── AGENTS.md
    │   ├── .env.example
    │   └── .ignore
    ├── frontend/              # frontend
    ├── backend/               # backend
    ├── infra/                 # docker / compose / nginx / ci / deploy
    ├── fastapi/               # backend + FastAPI conventions
    ├── nextjs/                # frontend + Next.js/shadcn conventions
    ├── python-sdk/            # Python library + conventions
    ├── docs/                  # MkDocs documentation
    └── docker/                # Dockerfile + Compose conventions
```

## License

MIT
