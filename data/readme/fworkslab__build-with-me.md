<div align="center">

# build-with-me

### A SKILL FOR CODING AGENTS

![OpenCode skill](https://img.shields.io/badge/OpenCode-skill-51418d?label=package)
![License](https://img.shields.io/badge/license-CC%20BY--NC--ND%204.0-lightgrey?label=license)

**Turns work you did with a human into a build-along tutorial.**

A skill for coding agents. It turns work you and a human just did together into a
tutorial a beginner can follow from an empty folder to a working program.

Product page: [fworkslab.github.io/other/build-with-me](https://fworkslab.github.io/other/build-with-me/index.en.html)

[Русский](README.ru.md)

</div>

---

> Write a "build along with me" tutorial — volumes, chapters, every element
> explained, every line written out live with its reason and its consequence,
> and both the errors that actually happened and the ones you are about to hit.

## The problem it solves

Most generated documentation explains finished code. The finished code cannot
tell you that the build failed twice because a file was locked, that the obvious
approach was wrong, that three attempts were tried before one worked. That
information exists only in the history of the work.

This skill keeps the mistakes. A step looks like this:

> **Why we write this.** Electron has no window until the app reports that it
> finished booting, and `whenReady` is that report. Anything visual has to wait
> for it.
>
> **What we are writing.** Three things. The import brings in the two Electron
> pieces we need. `whenReady().then` schedules work for after boot.
> `BrowserWindow` creates the window, and we hold it in a variable.
>
> **What happens if we leave it out.** Without the import, `app` is undefined
> and the app dies on startup. Create the window before `whenReady` and we get
> `ERR_ELECTRON_BEFORE_READY` and an immediate exit. Drop the `const win` and the
> window flashes for a fraction of a second and disappears.

---

## What comes out

- **An opening that says what is being built and why**, before any detail
- **A contents listing** of volumes, chapters and elements
- **Every element answered three times**: what it is, why it exists, what breaks
  without it — concretely, not "it is required"
- **Code written out live in prose**, not tabulated. For every block: why we
  write this, what we are writing, what it costs the program to omit it
- **Two kinds of errors kept apart**: the ones that actually happened, quoted
  verbatim, and the ones a reader starting from a different machine is about to
  hit
- **Abandoned approaches**, recorded so the reader does not spend the same hour

### Structure

```
Volume      a major part of the program: a platform, a runtime, a subsystem
  Chapter   a phase with a checkable outcome: "the build produces a signed APK"
    Element a file, an asset, an object, a layer — what breaks without it
      Step  the action, written out, with its reason and its consequence
```

Volumes are used when a program has more than about three major parts. Smaller
programs read better with chapters alone.

---

## Install

```bash
npx skills add <owner>/<repo>@build-with-me -g -y
```

The skill lands in `~/.agents/skills/build-with-me/SKILL.md` — that directory
is read by every agent, OpenCode included.

To put it into OpenCode's own directory instead:

```bash
npx skills add <owner>/<repo>@build-with-me -a opencode -g -y
```

Then the skill lands in `~/.config/opencode/skills/build-with-me/SKILL.md`.

Or copy it yourself — a skill is one file with a YAML header:

```
~/.agents/skills/build-with-me/SKILL.md
```

---

## Two languages on purpose

The body is written in English, because that keeps it compact. The `description`
in the header is bilingual, so the skill still triggers when the request arrives
in Russian: it matches requests such as "собери вместе со мной", "напиши
туториал", "опиши как мы это делали", "разбери программу по элементам".

The tutorial that comes out is written in whatever language the reader needs.

---

## It is not only for code

The structure survives when the project is not a program. Only the vocabulary
changes — the element is whatever the reader will come back to when something is
broken, and a step is any action named exactly enough to repeat.

| Project | An element is | A step is |
|---|---|---|
| Program | a file | code |
| Game on an engine | an asset, an actor, a Blueprint, a level | a tool call, a console command, a menu path with its value |
| Blender | a collection, a modifier, a bone, a keyframe | an exact operation with its setting |
| Maya, Houdini, ZBrush, Substance | a node, a subtool, an anchor point, a channel set | an exact parameter change |
| Spreadsheet, analysis | a sheet, a named range, a formula, a pivot, a chart | the formula, written with its cell addresses |
| Document | a heading level, a section, a style | applying the named style |
| Deck | a slide, the master it inherits from | the layout change, with its values |
| Drawing | a layer, a pass, a palette | a stroke with tool, size, angle, colour |
| Raster image | a layer, an adjustment, a mask, a smart object | the operation and its parameters, plus the export settings |

Node graphs count as code. A Blueprint graph, a material graph or a procedural
graph is code in a visual language, so it gets the same three questions per
block — and it gets printed as text, since a screenshot is not an explanation.

Three things the non-code sections insist on, because that is where this medium
actually fails:

- **Counts are read, not estimated.** File totals, resolutions, layer counts,
  pivot ranges — if the number appears in the tutorial it came out of the file.
  An invented "roughly two thousand lines" teaches the reader a wrong mental
  model of their own project.
- **A spreadsheet is a program nobody version-controls.** So formulas get their
  cell addresses, ranges get absolute references, and the origin of every input
  figure is named.
- **The output size is decided before the resolution**, and a colour profile is
  named wherever a colour value appears. Most of the rest of raster work follows
  from those two.

For any 3D project the tutorial also covers the handoff into the engine: unit
scale on import, LODs, naming collisions, and a lit check inside the engine
rather than only in the authoring tool, because that is where most 3D problems
survive the export unnoticed.

---

## What it will not do

- **Pad a small project.** Elements are counted from the machine before any chapter
  is planned, so a folder holding one file gets one chapter — not two volumes, a
  contents tree, and eight hundred lines. Where two rules of the skill pull opposite
  ways (explain everything, against stop when unsure) the shorter document wins.
  Without that rule the skill is only usable on projects big enough to absorb it,
  which is backwards: the small ones are where padding shows. A tutorial is not
  evidence that the agent worked hard.
- **Invent a past error.** If a step went cleanly, it says so. A tutorial with
  manufactured problems teaches the reader to expect failures that never occur
  and hides the ones that did.
- **Invent a history of troubles it never saw.** Given a repository someone else
  built, the structure, the reasoning and the predicted failures all still work
  because they are deduced from the files. What actually went wrong, and what was
  tried and dropped, does not — and the tutorial says plainly which parts are
  reconstructed from the code rather than from the build.

---

## Two questions it always asks first

1. **Scope** — a session often covers more than one program.
2. **Start state** — what the reader already has installed, and on which machine.

A third is about output format, and it scans what the machine can actually
convert to before offering anything: `pandoc`, LibreOffice, or libraries such as
`docx`, `pdfkit`, `python-docx`, `reportlab`. It never offers a format it cannot
produce, and it weights what the reader can open over what is easiest to
generate.

---

## Licence

CC BY-NC-ND 4.0. You may read this material, copy it and share it as long as you do
not modify it, do not sell it, and credit F Works. Publishing a modified version is
not permitted. Full text is in [LICENSE](LICENSE).