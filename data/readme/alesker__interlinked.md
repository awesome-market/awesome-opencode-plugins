# Interlinked

![](https://static.wikia.nocookie.net/bladerunner/images/2/24/BR2049_baseline_test.jpg)

## Within cells interlinked

This setup targets [OpenCode](https://github.com/anomalyco/opencode) and is managed with [GNU Stow](https://www.gnu.org/software/stow/).

```
stow .
```


## Within cells interlinked

### Agents

#### Primary agents
- Rubber-Duck :duck:
- Plan <sup>[Built-in]</sup>
- Build <sup>[Built-in]</sup>
- Review 
- `Pair-Programmer` :ghost:

#### Sub-agents
- general <sup>[Built-in]</sup>
- explore <sup>[Built-in]</sup>
- prompt-editor
- spell-scribe :ghost:
- tech-skill-smith

## Within cells interlinked

### Skills

- technical-research
- bug-triage
- technical-implementation
- change-inspection
- github-ops
- obsidian
- `go-code`
- `go-specs-code`
- `shell-code`

#### Third-party skills

Third-party skills are declared in [`skills.json`](skills.json) and are installed with `gh skill install` (using `gh skill bundle` alias).

`gh skill bundle` alias requires `gh`, Bash, and `jq`.

Import it:

```sh
gh alias import .gh/aliases.yml
```

Use it:

```sh
gh skill bundle --file skills.json --dir "$HOME/.agents/skills"
```

## Within cells interlinked

### Commands

- onboard-agents

## Within cells interlinked

### MCP Tools

- linear

## Within cells interlinked

### Plugins

- shell-env <sup>[Local]</sup>
- spell-library <sup>[Local]</sup>
- obsidian-library <sup>[Local]</sup>

## Within cells interlinked

### Claude Code

> [!WARNING] **Deprecated:** `interlink-claude` is not maintained for the native OpenCode V2 configuration right now.

OpenCode is the source of truth, but it's possible to derive a user-level [Claude Code](https://code.claude.com/docs/en/overview) setup from it.

```sh
./interlink-claude
```

This command
- generates Claude-native agents under `~/.claude/agents`
- links the canonical skills into `~/.claude/skills`
- adds a managed import block to `~/.claude/CLAUDE.md`

It owns only files recorded in `~/.claude/.interlink-claude-manifest` (existing Claude configuration is preserved, and name collisions fail without overwriting anything).
A symlinked `CLAUDE.md` is also left untouched and reported as a conflict.

Skill edits are reflected immediately through symlinks.
Run the command again after changing agents or moving the checkout.
Use `./interlink-claude --check` to report drift and conflicts without changing files.
Both modes list every translation with status indicators: `✅` in sync, `➕` missing or created, `🔄` content or link drift, `✨` updated, `🔗` relinked, `🗑️` stale, `⚠️` warning or configuration drift, and `❌` failure.

Agent translation preserves scalar `allow`, `ask`, or `deny` values for `edit`, `bash`, and `webfetch`.
Granular forms of those permissions are retained for OpenCode but cannot be enforced by the current Claude translator; translation emits a warning and relies on the generated agent prompt instead.


## Within cells interlinked

> *What a day, hmmm?*

![](https://static.wikia.nocookie.net/bladerunner/images/7/7d/Joi_and_K.jpg)
