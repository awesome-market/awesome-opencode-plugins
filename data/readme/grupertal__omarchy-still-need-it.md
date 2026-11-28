# omarchy-still-need-it

**Omarchy 4.5 ships half your hacks and will fight with some of the rest. Find out which before you update.**

![The report sorts your customizations into dev branch, RC, totally yours and conflicts, then zooms into a keybinding clash](assets/demo.gif)

<sub>[Watch the 22-second video](assets/omarchy-still-need-it.mp4)</sub>

An agent skill for [Omarchy](https://omarchy.org).
Over time you add plugins, hooks, scripts, keybindings, hypr tweaks, theme templates, `/etc` fixes and patched packages.
Then Omarchy ships the same thing.
This skill checks every customization against upstream, so you end up with the cleanest up-to-date system that still keeps the customizations that are really yours.

## Quick start

```bash
git clone https://github.com/GruperTal/omarchy-still-need-it.git ~/.claude/skills/omarchy-still-need-it
```

Then run `/omarchy-still-need-it` in Claude Code, or just ask *"do I still need my Omarchy customizations?"*

It changes nothing until you pick what to clean up, and it backs up every file before touching it.
Other agents that read `SKILL.md` work too: clone it wherever your agent loads skills from.

## What you get

A report in your terminal, also saved as `report-<date>-<time>.md`.
Here's an excerpt from a real run, Omarchy 4.0.6 against 4.5:

**Conflicts (new upstream will clash with yours)**

| Yours | Clashes with (upstream) | Ships in | Fix |
|---|---|---|---|
| `SUPER + M` → Spotifast | New default `SUPER + M`: minimize the window to the dock. Hyprland fires both. | v4.5.0-rc3 | `hl.unbind("SUPER + M")` before your bind |
| `SUPER + W` → a "Close Chrome?" confirmation | New second close chord `SUPER + Q` (#7767) closes directly and skips it | v4.5.0-rc1 | Point `SUPER + Q` at the same script |
| `compose:ralt`: Right Alt is the compose key | Voxtype push-to-talk holds Right Alt | v4.5.0-rc3 | Move compose, or keep push-to-talk on F9 |

**Exists in an RC (comes with the next version)**

| Your customization | Upstream equivalent | Ships in | Covers | Action |
|---|---|---|---|---|
| Hand-installed `omasnap` + screenshot key overrides | Omasnap becomes a default package (#9446) | v4.5.0-rc1 | Fully | Install the package now; drop the overrides at 4.5 |
| Workspace planner in a monitor plugin | Each monitor gets its own block of workspaces (#15655) | v4.5.0-rc1 | Partly: fixed blocks of ten | Turn the plugin's workspace planning off at 4.5 |

The full report also has **Exists on the dev branch** (merged, no release date yet), **Totally custom** (keep it, with any open PR noted) and numbered **Recommendations**.

## How it works

1. `scan.py` takes a read-only inventory of your customizations.
2. It cross-references each one with upstream Omarchy since your installed version: new files, commits (tagged with the release that ships them), release notes, new default keybindings and packages.
3. The agent checks every lead against upstream source, so every verdict comes with its receipt: the commit, PR or release.
4. It asks which items to clean up, backs up each file, and disables things before deleting them.

The scanner also runs on its own and writes the evidence you can read yourself:

```bash
python3 scan.py             # prints the path of ~/.cache/omarchy-still-need-it/evidence.md
python3 scan.py --selftest
```

It needs Python 3, git and pacman, all of which an Omarchy machine already has.
`gh` is optional; the agent uses it to look up open PRs.

## Upstream

Proposed for Omarchy as an optional post-update skill: [omacom/omarchy#17429](https://github.com/omacom/omarchy/discussions/17429). Join the discussion there.

## License

MIT
