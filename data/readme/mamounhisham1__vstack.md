# vstack

Personal skill collection. Every skill ID starts with `v-` and ships with a matching slash command.

[![Live site](https://img.shields.io/badge/site-live-brightgreen)](https://MamounHisham1.github.io/vstack/)
[![Pages deploy](https://github.com/MamounHisham1/vstack/actions/workflows/pages.yml/badge.svg)](https://github.com/MamounHisham1/vstack/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![skills.sh](https://skills.sh/b/MamounHisham1/vstack)](https://skills.sh/MamounHisham1/vstack)

## Demo

Live site: https://MamounHisham1.github.io/vstack/

One-click install page: https://MamounHisham1.github.io/vstack/install.html

## Install as plugin (one install, all skills)

In a Claude Code session (v2.1.275+):

```text
/plugin install vstack --marketplace MamounHisham1/vstack
```

Or from the shell:

```bash
claude plugin marketplace add MamounHisham1/vstack
claude plugin install vstack@vstack
```

This installs the `vstack` plugin with every `v-` skill. Skills run namespaced, e.g. `/vstack:v-build`.

## Install via skills CLI (per-agent)

```bash
npx skills add MamounHisham1/vstack --skill v-skill-creator -y
```

Install a specific skill:

```bash
npx skills add MamounHisham1/vstack --skill <skill-id> -y
```

Install everything:

```bash
npx skills add MamounHisham1/vstack --skill '*' -y
```

The `skills` CLI remembers your last selected agents and reuses them on the next install.

## Layout

```text
skills/<skill-id>/SKILL.md          # canonical skill (skills.sh + agents)
.opencode/commands/<skill-id>.md    # OpenCode slash command /<skill-id>
.claude-plugin/plugin.json          # Claude Code plugin manifest (one plugin, all skills)
.claude-plugin/marketplace.json     # marketplace catalog for `claude plugin marketplace add`
docs/                               # live site (https://MamounHisham1.github.io/vstack/)
scripts/                            # site build helpers
.github/workflows/pages.yml         # GitHub Pages deploy
```

## Skills

- `v-skill-creator` — create a new `v-` skill in this repo, publish it, and install it. Run `/v-skill-creator`. Install: `npx skills add MamounHisham1/vstack --skill v-skill-creator -y`
- `v-copy-me` — extract how you work from the session and create or update `v-` skills. Run `/v-copy-me`. Install: `npx skills add MamounHisham1/vstack --skill v-copy-me -y`
- `v-build` — build features with parallel subagents: decomposes big features into slices, fans out batches, ships as reviewed PRs, merges + syncs. Run `/v-build`. Install: `npx skills add MamounHisham1/vstack --skill v-build -y`
- `v-fill-me` — catch up on uncommitted, untracked, unpushed, and recently pushed work across repo and worktrees. Run `/v-fill-me`. Install: `npx skills add MamounHisham1/vstack --skill v-fill-me -y`
- `v-humanize` — rewrite long or technical AI output into plain human-readable language. Run `/v-humanize`. Install: `npx skills add MamounHisham1/vstack --skill v-humanize -y`
