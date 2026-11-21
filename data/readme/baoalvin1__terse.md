# terse

**Short answers. No filler.** A skill that caps every LLM response to its minimum useful length — answer first, lists over prose, code explained in three lines, links when they help.

## What it does

Stops a coding agent from padding its answers. Under `terse`, every reply is allocated a small budget: 5 sentences of prose max, 5-item lists, only the changed lines of code, up to 2 helpful links. Preamble, recaps, and "Hope this helps!" get cut before they're sent.

| Before | After |
|---|---|
| "Great question! Let me think about this. Your setup has a few moving pieces..." | "Run `npm install`, then edit `src/auth.ts:42`." |

## How it works

- **Budget, not target.** A hard ceiling per reply; no obligation to fill it.
- **Lead is the answer.** The deliverable comes first, always.
- **Code questions, three lines.** What it does, how (`file:line`), what breaks — plus up to 2 docs links.
- **Diagnostics, not alarm.** Errors state where, why, and the fix.
- **Bends for danger.** Destruction (`rm -rf`, force push, migrations) still triggers a confirmation prompt.
- **Stays on.** Mode persists for the whole session until you say "stop terse mode".

## Install

Point any opencode project at this skill, or copy it locally:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": { "paths": ["/path/to/terse/skills"] }
}
```

Or copy the folder globally:

```bash
cp -r skills/terse ~/.config/opencode/skill/terse
```

Restart opencode, then invoke with `/terse`.

### Pi (pi.dev)

Pi uses the same Agent Skills standard, so this skill works there unchanged. Install the repo as a Pi package (`skills/` is auto-discovered):

```bash
pi install git:github.com/baoalvin1/terse
```

Or copy the skill folder:

```bash
mkdir -p ~/.pi/agent/skills && cp -r skills/terse ~/.pi/agent/skills/terse
```

Then invoke with `/skill:terse`. Note: Pi loads skills on demand, so for always-on terseness append the skill body to `~/.pi/agent/AGENTS.md` (loaded every session):

```bash
cat skills/terse/SKILL.md >> ~/.pi/agent/AGENTS.md
```

## Usage

```
/terse
```

Mode applies to every response for the rest of the session. Turn it off with `stop terse mode` or `normal mode`.

## Files

```
skills/terse/SKILL.md   # the skill
opencode.json            # registers the skill path
```

## License

MIT