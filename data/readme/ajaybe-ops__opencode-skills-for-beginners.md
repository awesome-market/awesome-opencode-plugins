<p align="center">
  <img src="assets/banner.svg" alt="OpenCode Skills for Beginners" width="100%">
</p>

<h1 align="center">OpenCode Skills for Beginners</h1>

<p align="center">
  Learn what skills are, install your first one, actually use it, and write your own — without reading a spec first.
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-7dd3fc"></a>
  <a href="https://opencode.ai/docs/skills/"><img alt="OpenCode 2" src="https://img.shields.io/badge/OpenCode-2.x-a78bfa"></a>
  <img alt="Beginner friendly" src="https://img.shields.io/badge/level-beginner-f472b6">
  <img alt="No build step" src="https://img.shields.io/badge/setup-none%20needed-2dd4bf">
</p>

<p align="center">
  <b>New here?</b> Start at <a href="#-quickstart-your-first-skill-in-4-steps">Quickstart</a> ·
  <b>Stuck?</b> Jump to <a href="docs/09-troubleshooting.md">Troubleshooting</a> ·
  <b>Writing one?</b> Copy <a href="examples/hello-skill/">examples/hello-skill</a>
</p>

---

## What is a skill, really?

A skill is **a folder with a `SKILL.md` file inside it**. That file teaches your agent a repeatable workflow. Nothing is compiled, installed from a registry, or restarted.

```text
.opencode/skills/hello-skill/
└── SKILL.md
```

```markdown
---
name: Hello Skill
description: Use when the user asks for a friendly greeting or a demo of skills
---

# Hello Skill

1. Greet the user by name.
2. Explain in one sentence that you loaded this skill from `SKILL.md`.
```

The magic is in the **`description`**: OpenCode shows the agent only skill names and descriptions, every step. When your request matches one, the agent loads that skill's full instructions — and only then. That is why 400 installed skills do not blow up your context window.

> [!TIP]
> Think of a skill as a **playbook on a shelf**. The agent reads the spine (the description) all day, and pulls the book down (the `SKILL.md` body) only when the task calls for it.

**A skill is not:** an MCP server, a plugin, an agent, or a slash command. See [skills vs. agents vs. commands](docs/08-skills-vs-agents-vs-commands.md).

---

## 🚀 Quickstart: your first skill in 4 steps

### 1. Make sure OpenCode is installed

```bash
opencode --version
```

If that fails, install it from the official docs — <https://opencode.ai/docs/>. The quickest routes:

```bash
# macOS / Linux
curl -fsSL https://opencode.ai/v2/install | bash
# or via npm
npm install -g @opencode/cli
```

Windows: package managers are not supported — use the [standalone CLI zip](https://opencode.ai/docs/) or the [desktop app](https://opencode.ai/docs/). Full matrix in [docs/02-install-opencode.md](docs/02-install-opencode.md).

### 2. Create the folder

Skills live in one of two places. Pick **project** for this walkthrough — it keeps the example self-contained.

```bash
# macOS / Linux
mkdir -p .opencode/skills/hello-skill
```

```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force .opencode\skills\hello-skill
```

### 3. Paste the skill

Save this as `.opencode/skills/hello-skill/SKILL.md`:

```markdown
---
name: Hello Skill
description: Use when the user asks for a friendly greeting or a demo of how skills work
---

# Hello Skill

1. Greet the user by name.
2. Say which skill file you loaded.
3. Ask one short follow-up question.
```

### 4. Start a **new** session and ask for it

```bash
opencode
```

```text
Load the hello-skill skill and show me what it does.
```

> [!IMPORTANT]
> Skills are discovered **when a session starts**. A session that was already open will not see a folder you just created. Start a fresh one.

If the agent greets you and names the file, you are done — you just installed and ran a skill. 🎉

---

## 📚 What's in this repo

| Path | What you get |
| --- | --- |
| **[docs/01-what-is-a-skill.md](docs/01-what-is-a-skill.md)** | The mental model, file layout, and why loading is on-demand |
| **[docs/02-install-opencode.md](docs/02-install-opencode.md)** | Getting OpenCode running on macOS, Linux, or Windows |
| **[docs/03-install-a-skill.md](docs/03-install-a-skill.md)** | Four ways to install: CLI, zip, catalog URL, or by hand |
| **[docs/04-use-a-skill.md](docs/04-use-a-skill.md)** | Auto-invocation vs. `@skill-id`, and how to verify it loaded |
| **[docs/05-write-your-first-skill.md](docs/05-write-your-first-skill.md)** | Frontmatter, descriptions that trigger, and body structure |
| **[docs/06-global-vs-project.md](docs/06-global-vs-project.md)** | Which scope to use, plus how precedence and overrides work |
| **[docs/07-load-from-url.md](docs/07-load-from-url.md)** | Loading a whole web catalog in `opencode.json` (OpenCode 2) |
| **[docs/08-skills-vs-agents-vs-commands.md](docs/08-skills-vs-agents-vs-commands.md)** | Stop guessing which primitive you need |
| **[docs/09-troubleshooting.md](docs/09-troubleshooting.md)** | "It's not loading" — the six-cause checklist |
| **[docs/10-glossary.md](docs/10-glossary.md)** | Every term in one page |
| **[CHEATSHEET.md](CHEATSHEET.md)** | One-page reference for the impatient |
| **[labs/](labs/)** | Three graded exercises with solutions |
| **[examples/](examples/)** | Real, working skills you can copy |
| **[scripts/validate-skills.mjs](scripts/validate-skills.mjs)** | Lint your skills before you commit them |

**Suggested path:** docs 01 → 04, do Lab 1 and Lab 2, then docs 05 → 06 and Lab 3. That is about an hour.

---

## 🗂️ Where skills live

| Scope | Path | Visible to |
| --- | --- | --- |
| **Global** | `~/.config/opencode/skills/<id>/SKILL.md` | Every project on your machine |
| **Project** | `.opencode/skills/<id>/SKILL.md` | Everyone in that repo |
| Compat (global) | `~/.claude/skills/`, `~/.agents/skills/` | Every project — Claude Code skills work unchanged |
| Compat (project) | `.claude/skills/`, `.agents/skills/` | Everyone in that repo |
| **Catalog** | A URL in the `skills` array of `opencode.json` | Whatever you configure |

On Windows, `~/.config` means `C:\Users\<you>\.config`, so a global skill lands at:

```text
C:\Users\<you>\.config\opencode\skills\hello-skill\SKILL.md
```

Either layout is valid inside a source folder:

```text
skills/
├── review.md              ← flat file, id = "review"
└── git-release/
    └── SKILL.md           ← directory form, id = "git-release" (recommended)
```

Directory form is recommended because scripts and reference files can sit beside `SKILL.md`:

```text
git-release/
├── SKILL.md
├── references/
│   └── release-policy.md
└── scripts/
    └── changelog.ts
```

---

## ⚡ Using a skill

**Let the agent decide.** Just describe the task; matching skills are advertised automatically:

```text
Review my last commit and suggest a better message.
```

**Or force it.** Mention the ID with an `@`:

```text
@git-release draft the release notes for v1.4.0
```

The ID comes from the **path**, not the frontmatter `name`:

| File | ID |
| --- | --- |
| `.opencode/skills/git-release/SKILL.md` | `git-release` |
| `.opencode/skills/teams/release/SKILL.md` | `release` |
| `.opencode/skills/review.md` | `review` |

IDs are **case-sensitive** and should be lowercase kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`).

---

## ✍️ Writing a skill that actually fires

The whole trick is a `description` that says **when**, not just **what**:

```markdown
---
name: Git Commits
description: Use when writing, reviewing, or fixing git commit messages and pull request descriptions
---
```

| Weak | Strong |
| --- | --- |
| `description: Git helper` | `description: Use when writing or fixing git commit messages` |
| `description: Spreadsheets` | `description: Use when creating, editing, or analyzing .xlsx files from data` |

Then structure the body so a model can follow it:

```markdown
# Git Commits

## When to use
The user asks for a commit message, or a commit is about to be created.

## Workflow
1. Run `git diff --staged` and read the actual change.
2. Classify it: feat, fix, docs, refactor, test, chore.
3. Write `<type>(<scope>): <imperative summary>` in 72 characters or less.
4. Show the message and wait for approval before committing.

## Rules
- Never invent a scope that is not in the diff.
- One logical change per commit.
```

Full walkthrough: [docs/05-write-your-first-skill.md](docs/05-write-your-first-skill.md).

---

## 📦 Install skills from opencodeskills.dev

[opencodeskills.dev](https://opencodeskills.dev/) is an independent, community-run directory with 491 free MIT-licensed skills in 18 categories. Three ways in:

**CLI chooser** (needs Node 20.12+):

```bash
curl -fsSL https://opencodeskills.dev/install.sh | sh
```

```powershell
# Windows PowerShell
irm https://opencodeskills.dev/cli.mjs -OutFile "$env:TEMP\opencode-skills.mjs"; node "$env:TEMP\opencode-skills.mjs"
```

**Named installs, no prompts:**

```bash
# two skills, globally
curl -fsSL https://opencodeskills.dev/install.sh | sh -s -- install xlsx pdf-handling

# into this repo's .opencode/skills/
curl -fsSL https://opencodeskills.dev/install.sh | sh -s -- install --project git-commits

# one whole category
curl -fsSL https://opencodeskills.dev/install.sh | sh -s -- install --category recommended --all
```

**Or point OpenCode at the catalog** (OpenCode 2 — nothing copied to disk). Add to `opencode.json`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["https://opencodeskills.dev/catalog/documentation/"]
}
```

Details and caveats: [docs/07-load-from-url.md](docs/07-load-from-url.md).

> [!NOTE]
> OpenCode Skills is **not** affiliated with OpenCode or its maintainers. It is a community directory. The official reference is <https://opencode.ai/docs/skills/>.

---

## 🧪 Try the bundled examples

This repo ships three working skills. Point OpenCode at the `examples/` folder instead of copying anything:

```jsonc
// opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["./examples"]
}
```

| Skill | What it demonstrates |
| --- | --- |
| [`hello-skill`](examples/hello-skill/) | Smallest possible skill; ideal first test |
| [`commit-message-writer`](examples/commit-message-writer/) | A real workflow with a `references/` cheatsheet |
| [`pr-review-checklist`](examples/pr-review-checklist/) | Step-by-step procedure with stop-and-ask gates |

Validate any skill folder — yours or one you downloaded:

```bash
node scripts/validate-skills.mjs
```

---

## 🔧 It's not loading

Work down this list; it catches nearly every case:

1. **Filename** — must be exactly `SKILL.md` (case matters on Linux/macOS), or a root-level `*.md`.
2. **Depth** — `SKILL.md` may sit at the source root or in a folder below it, but not inside another skill folder.
3. **Fresh session** — skills are discovered at session start.
4. **Description** — no `description`, no advertisement to the model.
5. **ID mismatch** — `@release`, not `@Git Release`.
6. **Shadowing** — a later source (project beats global) defines the same ID and wins.

Full checklist with fixes: [docs/09-troubleshooting.md](docs/09-troubleshooting.md).

---

## ❓ FAQ

<details>
<summary><b>Do I need Node or a package manager?</b></summary>

No. A skill is a Markdown file in a folder. Node is only needed for the opencodeskills.dev installer or this repo's validator.
</details>

<details>
<summary><b>Do Claude Code skills work?</b></summary>

Yes. OpenCode reads `~/.claude/skills/` and `.claude/skills/` (and the `.agents/` equivalents) alongside its own folders.
</details>

<details>
<summary><b>Will 50 installed skills slow my agent down?</b></summary>

Not much. Only names and descriptions are listed at each step; bodies load on demand. Still, prune what you do not use — descriptions compete for attention.
</details>

<details>
<summary><b>How do I stop a skill from auto-triggering?</b></summary>

Hide it from the model but keep it loadable:

```yaml
metadata:
  opencode/autoinvoke: false
```
</details>

<details>
<summary><b>Can I share skills with my team?</b></summary>

Commit `.opencode/skills/` to the repo. Everyone who clones it gets the same skills, with no setup step.
</details>

<details>
<summary><b>How do I delete a skill?</b></summary>

Delete its folder. Do not delete the parent `skills/` directory unless you mean to remove every skill beside it.
</details>

---

## 🤝 Contributing

Corrections, clearer explanations, and new beginner examples are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first — it is short, and the CI check is one command.

## 📄 License

[MIT](LICENSE). Use it, fork it, teach with it.

<p align="center">
  <sub>Built for people who just want their agent to stop forgetting the same thing twice.</sub>
</p>
