# motionframe-edit

One agent skill for editing video, animating motion graphics, and designing interfaces —
made by merging eighteen existing skill repositories rather than inventing a nineteenth.

[![ci](https://github.com/jamescai-md/motionframe-edit/actions/workflows/ci.yml/badge.svg)](https://github.com/jamescai-md/motionframe-edit/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-2ea44f.svg)](LICENSE)

Each of those eighteen repos is good at one thing and wrong about another: one cuts
beautifully but needs a paid transcription API, one has the strictest correctness rules and
only covers talking heads, one bans gradients while another builds everything from them. Left
alone, an agent given all of them at once gives contradictory advice.

This repository reads them together, decides the disagreements in writing, and keeps the
source material next to the decision so you can check it.

## Install

```bash
git clone https://github.com/jamescai-md/motionframe-edit.git
cd motionframe-edit
./install.sh
```

`install.sh` detects which agents you have and links the skills into place. To target one
explicitly, or a tool it does not recognise:

| Agent | Install |
|---|---|
| Claude Code | `./install.sh --target claude` |
| ChatGPT / Codex | `./install.sh --target codex` |
| Gemini CLI | `gemini extensions link .` |
| Antigravity | `./install.sh --target antigravity` |
| OpenCode | `./install.sh --target opencode` |
| Cursor, Windsurf, Zed, Aider, Hermes | `./install.sh --dir <your skills directory>` |

Every platform reads the same `AGENTS.md` and `skills/`, with thin adapters per tool so they
cannot drift. [docs/platforms.md](docs/platforms.md) has the details.

## The skills

| Skill | Ask for it when |
|---|---|
| [motionframe-edit](skills/motionframe-edit/SKILL.md) | you are not sure which of the others applies — it routes, and it settles conflicts between them |
| [edit-supervisor](skills/edit-supervisor/SKILL.md) | you have footage and want a finished piece: cutting, captions, grade, mix, delivery |
| [motion-director](skills/motion-director/SKILL.md) | something has to move: launch films, lower thirds, transitions, beat sheets |
| [design-director](skills/design-director/SKILL.md) | pages, interfaces, decks, posters, brand systems |
| [ui-motion](skills/ui-motion/SKILL.md) | interface animation feels wrong, or you need to know whether it should animate at all |
| [gatekeeper](skills/gatekeeper/SKILL.md) | before calling something done — measures the render instead of trusting it |
| [taste-memory](skills/taste-memory/SKILL.md) | you keep correcting the same thing and want it remembered |

They are read on demand, not all at once: a captioning job loads the caption rules and nothing
from the design system.

## What it is built from

All eighteen sources are in [library/](library/), each with its upstream URL, licence, pinned
commit and what it is bad at. That is 1,824 files and 13.4 MB of the sources' own text —
copied verbatim where the licence allows it, which is what makes the merge checkable instead
of a claim.

Four of them do not permit redistribution and are here on the maintainer's stated permission;
each of those folders records the basis in `PERMISSION.md`. The MIT licence at the root covers
this project's own writing only — see [NOTICE](NOTICE) for exactly what it does not cover,
including Remotion's company-size threshold and hypit's commercial conditions.

This is not a fork, and the copies are not the product. A GitHub fork maps one repository to
one repository, which cannot hold eighteen; the sources are here as reference material so the
merge in `skills/` can be checked rather than trusted. Credit is per source in
[ATTRIBUTION.md](ATTRIBUTION.md), and the rule-by-rule map is
[docs/absorption.md](docs/absorption.md).

## Requirements

Python 3.10 or newer, and `ffmpeg` on the PATH. Transcription uses `whisper.cpp` or
`faster-whisper` if you have either; everything else works without it.

No API keys, no accounts, no credits, no telemetry. `python3 tools/mfe.py doctor` reports what
is installed and the command to install what is missing.

## Documentation

| | |
|---|---|
| [docs/platforms.md](docs/platforms.md) | how each agent loads the skills |
| [docs/architecture.md](docs/architecture.md) | what the skills decide and what the tools measure |
| [docs/absorption.md](docs/absorption.md) | which rule in `skills/` came from which source |
| [docs/plan.md](docs/plan.md) | what is unfinished or weak, stated plainly |
| [CHANGELOG.md](CHANGELOG.md) | what changed, and when |
| [examples/selftest](examples/selftest/) | a real 13.6 s render and the gate report that measured it |
| [CONTRIBUTING.md](CONTRIBUTING.md) | how to add a rule or a source |

## Licence

MIT for this project's own work — see [LICENSE](LICENSE) and [NOTICE](NOTICE) for the
scope, since the copied sources keep their own terms.
