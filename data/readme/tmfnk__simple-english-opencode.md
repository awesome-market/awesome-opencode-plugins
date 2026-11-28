# Simple English for OpenCode

An OpenCode skill that rewrites verbose, AI-sounding prose into plain English.

Use it on marketing copy, docs, blog posts, specs, and AI-generated text. It keeps the discipline from [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) (short sentences, active voice, fixed vocabulary), but it is not a full ASD-STE100 compliance tool. It's a practical rewrite skill for real writing work.

## What it does

- Rewrites into short, plain, active sentences (max 20 words for steps, 25 for explanations)
- Cuts AI padding: filler transitions, empty intensifiers, fake structure, synonym rotation
- Locks vocabulary (one word, one meaning)
- Leaves code, identifiers, and quoted errors alone
- Returns the same three blocks every time: rewrite, cuts, and before/after stats

## Why use it

Most writing tools stop at flagging problems. This one rewrites the text into a cleaner version you can use.

It is built for cases where the draft is technically fine but still feels bloated, vague, or LLM-written:

- landing pages that sound like brochure copy
- docs that bury the point
- blog intros that take too long to start
- specs full of soft language and filler
- AI drafts that need a human, direct voice

## Modes

| Mode              | Say                                               | Result                                         |
| ----------------- | ------------------------------------------------- | ---------------------------------------------- |
| Rewrite (default) | "rewrite", "simplify", "de-slop", "plain English" | Simple English + Cuts + Stats                  |
| Check             | "check", "audit", "review only"                   | Findings table + Stats                         |
| Shorter           | "make it shorter"                                 | Same as rewrite, aim for about 30% fewer words |

Optional genre hint: `marketing`, `docs`, `blog`, or `spec`.

## Install

OpenCode loads skills from project and global directories.

### Global (recommended)

Clone the repo, then symlink the skill into your OpenCode skills directory:

```bash
git clone https://github.com/TMFNK/Simple-English-OpenCode.git
mkdir -p ~/.config/opencode/skills
ln -s "$(pwd)/Simple-English-OpenCode/skills/simple-english-opencode" \
  ~/.config/opencode/skills/simple-english-opencode
```

If you already have the repo elsewhere on disk, point the symlink at that path instead.

Or copy the skill directory:

```bash
cp -r skills/simple-english-opencode ~/.config/opencode/skills/simple-english-opencode
```

### Project-local

```bash
mkdir -p .opencode/skills
ln -s /path/to/simple-english-opencode/skills/simple-english-opencode \
  .opencode/skills/simple-english-opencode
```

OpenCode also picks up `.claude/skills/` and `.agents/skills/`. Start a new session after install. The agent should list `simple-english-opencode` in the `skill` tool.

## Usage

Ask for a rewrite the way you normally would:

- "Rewrite this landing page in simple English."
- "De-slop this README."
- "Check this spec for filler and passive voice."
- "Make this blog intro shorter."
- "Marketing pass on this paragraph."

Optional genre hints:

- `marketing`
- `docs`
- `blog`
- `spec`

### Real-world examples

- See `examples/popular-page-before-after.md` for a before/after rewrite from Shopify's enterprise page.
- See `examples/technical-docs-before-after.md` for a before/after rewrite from GitHub's technical docs.

### Example

**Input:**

> The decision was made by the committee to utilize a more robust framework that would facilitate better outcomes for all stakeholders involved in the process.

**Output:**

```markdown
## Simple English

The committee chose a stronger framework.

## Cuts

| Before                                 | After               | Why                   |
| -------------------------------------- | ------------------- | --------------------- |
| The decision was made by the committee | The committee chose | active voice          |
| utilize / robust / facilitate…         | stronger framework  | empty claim + padding |

## Stats

|                      | Before | After |
| -------------------- | ------ | ----- |
| Words                | 26     | 6     |
| Sentences            | 1      | 1     |
| Avg words / sentence | 26     | 6     |
| Passive voice        | 1      | 0     |
```

## Layout

```text
simple-english-opencode/
├── README.md
├── LICENSE
├── .gitignore
└── skills/
    └── simple-english-opencode/
        ├── SKILL.md
        └── references/
            ├── checklist.md
            ├── substitutions.md
            └── genres.md
```

## Credits

- Maintained by [TMFNK](https://github.com/TMFNK)
- Sentence and vocabulary rules lean on [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish)

## License

[MIT](./LICENSE)
