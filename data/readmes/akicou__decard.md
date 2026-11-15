# decard

A cross-agent **skill + slash command** that finds and removes card-based UI
container components — shadcn/MUI/Bootstrap/Vuetify/Ant/Chakra `Card`, elevated
"box" panels, bordered-and-shadowed wrappers — and flattens them into
`section` + heading + divider layouts. It also prevents reaching for card
containers when building new UI.

Flattening is **not** "remove every border": tables, divided lists, code blocks
and inputs keep their structural frames. Only the decorative box that gift-wraps
a heading + prose gets cut, and a grid of identical cards collapses into one
divided list.

## Repo layout

```
skills/decard/SKILL.md      # the skill (Agent Skills standard)
skills.sh.json              # skills.sh repo grouping
.claude/commands/decard.md  # Claude Code  ->  /decard
.opencode/commands/decard.md# OpenCode     ->  /decard
.pi/prompts/decard.md       # pi           ->  /decard   (also /skill:decard)
```

The full rule set, flatten recipe and search patterns live in
[`skills/decard/SKILL.md`](./skills/decard/SKILL.md).

## Install

### skills.sh

This repo follows the [skills.sh](https://www.skills.sh) layout
(`skills/<name>/SKILL.md` + `skills.sh.json`). Point the skills.sh tooling /
registry at `github.com/Akicou/decard`; the `decard` skill appears under the
**UI cleanup** group.

### Claude Code

```bash
git clone https://github.com/Akicou/decard.git /tmp/decard
# Skill (auto-loads on relevant requests):
mkdir -p ~/.claude/skills
cp -r /tmp/decard/skills/decard ~/.claude/skills/decard
# Slash command  ->  /decard
mkdir -p ~/.claude/commands
cp /tmp/decard/.claude/commands/decard.md ~/.claude/commands/decard.md
```

> `cp` won't create the target folder — the `mkdir -p` lines matter. On PowerShell
> use `New-Item -ItemType Directory -Force <dir>` (mkdir's `-p` is implied by `-Force`).

### pi (pi.dev)

```bash
# Skill  ->  /skill:decard
mkdir -p ~/.pi/agent/skills
cp -r /tmp/decard/skills/decard ~/.pi/agent/skills/decard
# Prompt template  ->  /decard
mkdir -p ~/.pi/agent/prompts
cp /tmp/decard/.pi/prompts/decard.md ~/.pi/agent/prompts/decard.md
```

### OpenCode

```bash
# Command  ->  /decard   (global; or use ./.opencode/commands/ per-project)
mkdir -p ~/.config/opencode/commands
cp /tmp/decard/.opencode/commands/decard.md ~/.config/opencode/commands/decard.md
```

### Other agents (Cursor, Cline, …)

Any agent that runs a markdown prompt can use the same body — copy the contents
of [`.claude/commands/decard.md`](./.claude/commands/decard.md) into that tool's
command/rule format.

## Use

Trigger it in any project:

- `/decard` — flatten cards in the current diff (or the whole UI)
- `/decard src/pages/Settings.tsx` — target a path
- `/decard audit` — just list the card containers, don't edit
- or plain language: "remove the cards", "this is too boxy", "de-overlay the UI"

## License

MIT — see [`LICENSE`](./LICENSE).
