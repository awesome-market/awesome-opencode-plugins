# Signoff

> You own what ships.

A team-focused OpenCode plugin that packages custom agents, Engineering
Cookbook rules, and `@dietrichgebert/ponytail`. It helps developers turn
feature intent into a shared, reviewable plan, then delegate bounded work with
clear approval and verification points.

## What It Provides

- `orchestrator`, `delivery`, and `refactor` agents for a developer-led feature
  workflow.
- A standalone `reviewer` agent backed by Open Code Review.
- A standalone `documentation` agent that discovers, creates, and audits
  technical documentation, with the `docs-conventions`, `docs-audit`,
  `docs-c4`, `docs-adr`, `docs-sequence`, `docs-class`, `docs-uml`, and
  `docs-erd` skills. It uses Mermaid in Markdown by default and Archify for
  complex diagrams.
- Bundled CLIs: Open Code Review (`ocr`) and [CodeGraph](https://github.com/colbymchenry/codegraph)
  (`codegraph`), available in agent shells without a global install, plus
  CodeGraph's MCP server and a `/codegraph-init` command.
- Vendored third-party skills: `open-code-review-delegate`, `grill-me`,
  `grilling`, `cyclomatic-complexity`, and `archify`.
- The `author-engineering-rules` skill, which interviews you and writes
  engineering rules for your own project.
- Engineering rules as Markdown, shipped as a catalogue under `plugin/rules/`.
  They are opt-in: `/rules-install` copies selected stacks into the project's
  `.opencode/rules/`, and the `author-engineering-rules` skill writes new ones.
  Active rules are served to agents by the `rules_for` tool and validated by
  `rules_check`.
- An `/ocr-rules` command that writes the project's installed rules into the repository's
  Open Code Review rule file.
- Ponytail's skills and commands, without a separate ponytail plugin entry.
- Discovery of bundled skills and skills installed under project-local
  `.agents/skills` directories.

The plugin registers bundled `plugin/skills/<id>/SKILL.md` files, composes the
bundled ponytail plugin, and installs agent Markdown files. OpenCode's plugin
API does not create agents directly, so the plugin copies those files into an
OpenCode agents directory. `orchestrator`, `reviewer`, and `documentation` are
primary agents; `delivery` and `refactor` are subagents.

### Engineering Rules

The team's engineering and coding conventions live as Markdown rules, not
inside skills, so every agent can reach them. The plugin bundles a catalogue
under `plugin/rules/<stack>/`; a project uses rules only once they are under
`.opencode/rules/<stack>/`, with the same layout:

```text
.opencode/rules/nestjs/
  README.md          # stack guide; frontmatter: description, detect, review-marker
  architecture/      # decision records
  engineering-rules/ # detailed rules by topic
  checks/            # short checklists bound to file globs, also used for OCR
```

Two ways to get rules into a project:

- **Install the bundled rules.** `/rules-install` lists the stacks (NestJS,
  Vue), previews the files, and copies the selected ones after confirmation.
  Existing files that differ are kept unless you confirm `overwrite`.
- **Write your own.** Ask an agent to use the `author-engineering-rules`
  skill: it interviews you theme by theme, collects examples and references,
  and writes a stack under `.opencode/rules/`. The `rules_check` tool validates
  it.

The plugin adds a short index of the installed stacks to every session and
registers a `rules_for` tool. Given the files an agent plans to change or
review, it returns, for each stack whose `detect` dependencies appear in the
nearest `package.json`, the first check whose `globs` match, plus the cookbook
sources to read. Delivery and Refactor call it; Delivery records the applied
check IDs in the spec's `## Rules` section.

Installed files are the project's own: edit them, add a stack (for example
`.opencode/rules/project/checks/`), and commit them. A stack without `detect`
applies to every file. Rules live under `.opencode/` rather than `.agents/`
because the Orchestrator keeps `.agents/` local and ignored.

A check is a short Markdown file:

```markdown
---
title: NestJS controller (transport boundary).
globs: ["**/*.controller.ts"]
sources: [engineering-rules/design/001-business-oriented-api-design.md]
---
- Keep handlers thin: ...
```

Checks are matched in file-name order, like OCR's first-match rule, so put
specific globs before broad ones. Globs must be lowercase: OCR lowercases file
paths before matching, and `rules_for` does the same.

## Developer-Led Workflow

The developer remains the pilot: you decide what the feature should do, provide
technical direction, approve its scope, and judge whether the result is right.
The agents help make sure everyone understands what is being created before
implementation begins, then work within the boundaries you approve. This is
structured assistance for developers who know how to build the feature, not a
replacement for their expertise or judgment.

1. **Orchestrator** clarifies requirements, proposes small features, and waits
   for your approval before starting each one.
2. **Delivery** writes a decision-complete spec with acceptance and edge-case
   criteria. It asks for explicit approval of that spec, then implements and
   tests only the approved plan.
3. **Refactor** checks the implementation against the approved criteria,
   fixes directly related issues, and reports any remaining gaps.
4. **Orchestrator** archives the spec, lists the feature's changed files, and
   strongly recommends that you review and commit them, with a suggested
   message. Committing stays your decision.

No agent stages, commits, or pushes. `NEEDS_ATTENTION` records a gap or
divergence; after implementation starts, it does not automatically skip review
or archiving. The workflow pauses when approval is missing, and before a new
feature when uncommitted changes remain, so you can commit them first.

## Code Review

The `reviewer` agent is standalone and is not part of the Orchestrator
workflow. Run `/review`, optionally naming a branch range or commit, to switch
the session to it and start a review, or switch to `reviewer` yourself. It is
the only agent that runs OCR: the other agents are told to send review
requests to `/review` instead of calling `ocr` themselves. It uses
[Open Code Review](https://github.com/alibaba/open-code-review)
in delegation mode: `ocr` selects files and resolves review rules, and the
OpenCode model performs the review, so no OCR API key is required. The agent
reports findings with file coverage, proposes a fix plan, and asks before
applying any fix. It never stages or commits.

Prerequisite: Git 2.41 or later, required by OCR. The `ocr` CLI and the
`open-code-review-delegate` skill ship with the plugin.

### Team Review Rules

OCR reads its rules from `<repo>/.opencodereview/rule.json`. Run `/ocr-rules`
in a repository to install the team checks there:

1. It lists the rule stacks and their checks.
2. You select the stacks the project needs and, for each, the application
   directory (the repository root by default); globs are prefixed with it so
   stacks in different directories do not shadow each other.
3. It previews the merged file, with warnings for existing catch-all entries
   that would shadow the team rules, and writes it only after confirmation.

Existing entries, `include`, and `exclude` are kept and stay first, so project
rules keep priority. Team entries are identified by their `[<marker>]` prefix
and replaced on each run, so rerun `/ocr-rules` after updating the plugin.
Entries set `merge_system_rule: true` to keep OCR's built-in language rules.
Commit the file to share the rules, including with CI, and run `/review` to
review with them.

## Bundled Tools

`@alibaba-group/open-code-review` and `@colbymchenry/codegraph` are npm
dependencies of the plugin; npm installs their self-contained build for the
current platform, so neither needs Node.js at runtime. The plugin writes `ocr`
and `codegraph` launchers to `~/.cache/opencode-signoff/bin`
(`$XDG_CACHE_HOME` or `%LOCALAPPDATA%` when set) and prepends that directory to
`PATH` for every shell command an agent runs.

### CodeGraph

CodeGraph indexes the project into a local knowledge graph (`.codegraph/`)
that agents query instead of grepping and reading files one by one. The plugin
registers CodeGraph's MCP server (`codegraph_explore`) itself, so
`codegraph install` is not needed and no agent configuration or `AGENTS.md` is
modified. Telemetry is always disabled (`CODEGRAPH_TELEMETRY=0`).

Each project is indexed once; the index then syncs automatically:

- `/codegraph-init` builds the index for the current project.
- The `orchestrator` checks for the index with the `codegraph_init` tool and
  offers to build it before its first feature.

The plugin does not change `.gitignore`; decide yourself whether to commit
`.codegraph/` or other generated folders such as `.archify/`.

## Install

Install globally to make the plugin available across projects:

```sh
opencode plugin add @thomasrumas/signoff
```

For one project, add the package and choose where its agents should be
installed in that project's OpenCode config:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "@thomasrumas/signoff",
      "options": { "agents": "project" }
    }
  ]
}
```

Restart OpenCode or start a new session after installation so the plugin can
register its skills and agents.

### Agent Installation

The default is `global`. On macOS/Linux, agents install into
`~/.config/opencode/agents/` unless `XDG_CONFIG_HOME` is set, in which case the
target is `$XDG_CONFIG_HOME/opencode/agents/`. On Windows, `%APPDATA%` is used
when `XDG_CONFIG_HOME` is unset. Choose another mode with the plugin's `agents`
option:

- `"global"` (default): install agents for use across projects.
- `"project"`: install into `<project>/.opencode/agents/`.
- `"none"`: do not install agents automatically.

At each startup, the plugin installs missing agents and overwrites installed
ones that differ from the bundled version, so a new plugin version always
replaces them. Local edits to these files are lost; to customize an agent,
copy it under another name. The plugin reloads agents after it installs or
updates files. Uninstalling the plugin does not remove agents already
installed.

## Skills

The plugin discovers project-local `.agents/skills` directories as well as the
package's bundled `plugin/skills/` directory. For example, install a skill in the
project with the skills CLI:

```sh
npx -y skills@latest add vercel-labs/agent-skills -a opencode
```

Restart OpenCode or start a new session after adding skills so the plugin can
rescan them. Project-local `.agents/skills` skills are discovered at runtime
and override bundled skills with the same ID; they are not automatically
included in the published package. The plugin does
not import user-global `~/.agents/skills` or `~/.config/opencode/skills`.
Skills intended to ship with the package must be tracked under `plugin/skills/<id>/`.

### Vendored Skills

Third-party skills are copied into `plugin/skills/` at pinned commits, with their
licenses and an `UPSTREAM.json` recording the source:

| Skill | Source | License |
| --- | --- | --- |
| `open-code-review-delegate` | alibaba/open-code-review | Apache-2.0 |
| `grill-me`, `grilling` | mattpocock/skills | MIT |
| `cyclomatic-complexity` | saurabhkumar8112/cyclomatic-complexity-skill | Apache-2.0 |
| `archify` | tt-a1i/archify (rendered `examples/*.html` excluded) | Apache-2.0 |

To update them, change the pinned commits in `plugin/scripts/vendor-skills.ts`
and run `npm --prefix plugin run skills:vendor`.

### Agent Skill References

`ponytail-review` is provided by the bundled ponytail plugin. Do not add
`@dietrichgebert/ponytail` separately; that would register its skills, commands,
and hooks twice. The `grill-me` and `cyclomatic-complexity` skills referenced by
the agents are vendored in this package.

The agents' legacy `skills:` fields do not restrict which skills are available.
To restrict skill access, configure ordered `permissions` rules for the `skill`
action; the last matching rule wins, so put the deny rule first:

```yaml
permissions:
  - { action: skill, resource: "*", effect: deny }
  - { action: skill, resource: "grill-me", effect: allow }
```

## Local Development

This repository contains two independent npm packages: the plugin in `plugin/`
and the VitePress site in `documentation/`. From the repository root, install
and check them with:

```sh
npm ci --prefix plugin
npm --prefix plugin run typecheck
npm --prefix plugin test
npm --prefix plugin run rules:check

npm ci --prefix documentation
npm --prefix documentation run docs:dev
npm --prefix documentation run docs:build
```

The documentation catalogue reads its rules from `plugin/rules/`. To test the
local plugin, start OpenCode from `plugin/` so `opencode.jsonc` loads `./src`:

```sh
cd plugin
opencode
```

After editing `plugin/rules/<stack>/`, validate the rules with
`npm --prefix plugin run rules:check`. To restart the OpenCode service and
inspect registered skills or agents:

```sh
opencode service restart
opencode api get /api/skill
opencode api get /api/agent
```

To install agents only in the development project, use an options object in
`plugin/opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "./src",
      "options": { "agents": "project" }
    }
  ]
}
```

## Continuous Integration

The `CI` workflow runs on every pull request:

- **Plugin** installs `plugin/` dependencies, typechecks, runs the tests, and
  validates the bundled rules.
- **Documentation** installs `documentation/` dependencies and builds the
  VitePress site with the `/signoff` base path used by the project Pages site.

## Publish

The npm package includes `src/`, `rules/`, `skills/`, and `agents/`. Add any
skills you intend to ship under `plugin/skills/`.

The package pins `@dietrichgebert/ponytail` as a dependency and installs its
agents on startup, so consumers do not need to install ponytail separately or
manually copy the bundled agent files.

Releases are automated with [semantic-release](https://semantic-release.org/).
On every push to `main`, the `Release` workflow runs the plugin checks. When
the push contains a releasable commit, it:

- publishes `@thomasrumas/signoff` to npm,
- creates the GitHub release and its notes,
- commits the new version in `plugin/package.json` and
  `plugin/package-lock.json` back to `main`.

The first release is `1.0.0`: semantic-release starts there when the repository
has no release tag. The first push to `main` must include at least one
releasable commit, for example `feat: initial release`. Later versions follow
the commit messages:

| Commit | Release |
| --- | --- |
| `fix: ...` | patch (`1.0.1`) |
| `feat: ...` | minor (`1.1.0`) |
| `feat!: ...` or `BREAKING CHANGE: ...` | major (`2.0.0`) |

`chore:`, `docs:`, `test:`, and other non-release types do not create a
version. If you squash-merge pull requests, the pull request title becomes the
commit message, so write it in the same format.

To publish manually, for example to recover from a failed release, run
`npm publish --access public` from `plugin/`, then install it with
`opencode plugin add @thomasrumas/signoff`.

### One-time repository setup

- Configure a trusted publisher for `@thomasrumas/signoff` on npmjs.com:
  GitHub Actions, repository `ThomasRumas/signoff`, workflow `release.yml`, with
  `npm publish` allowed. Publishing uses OIDC and needs no `NPM_TOKEN` secret.
- Protect `main` and require the `CI` workflow checks before merging.
- If `main` is protected, allow GitHub Actions to push the release commit, or
  remove `@semantic-release/git` from `release.config.mjs` and keep versions
  only in git tags and npm.

## Documentation deployment

The `Deploy documentation` workflow builds and deploys the VitePress site on
every push to `main`. It derives VitePress's base path from the GitHub Pages
metadata, so it works for both project sites and custom domains. The site is
available at `https://thomasrumas.github.io/signoff/` unless a custom domain is
configured.

In Settings > Pages, set the build and deployment source to **GitHub Actions**.
