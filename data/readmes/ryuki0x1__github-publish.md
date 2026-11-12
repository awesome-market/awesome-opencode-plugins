# 🚀 github-publish

> Publish any project to GitHub with a polished, SEO-optimized README — no more rewriting the same "publish it on github" checklist every session.

[![OpenCode Skill](https://img.shields.io/badge/OpenCode-Skill-blue?logo=github)](https://github.com/Ryuki0x1/github-publish)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Ryuki0x1/github-publish/pulls)

---

## ✨ What it does

This OpenCode skill turns your repeatable GitHub publishing routine into one command. Instead of restating screenshot rules, SEO keywords, and tag lists every time, just say:

> **"publish it on github do the necessary with readme screenshots and tags"**

The skill handles everything:

| 🧭 Step | What happens |
|---------|--------------|
| **1. Screenshots** | Captures **UI-only** screenshots via `readme-screenshots` — no desktop or background noise |
| **2. Demo background** | Adds a placeholder hero image or GIF when you have no real demo video |
| **3. SEO README** | Writes a keyword-rich README: title, one-line pitch, badges, features, install, usage, license |
| **4. Discovery tags** | Adds 5–10 GitHub topics/tags + repository description so your repo surfaces in search |
| **5. Publish** | Commits, pushes to `main`, and optionally creates a repo/tag/release via `gh` CLI |

---

## 📋 Prerequisites

Install these before using the skill:

| 🛠️ Tool | Why |
|---------|-----|
| [`readme-screenshots`](https://github.com/Ryuki0x1/readme-screenshots) | Takes the UI-only screenshots for your README |
| `git` | Commits and pushes your code |
| `gh` (GitHub CLI) | Optional — auto-creates the repo, adds topics, and makes a release |

> Not using `readme-screenshots`? The skill falls back to manual screenshots.<br>
> Not using `gh`? Create the repo manually on GitHub.com and push via git.

---

## 📦 Installation

Clone this repo into your OpenCode skills folder:

```bash
git clone https://github.com/Ryuki0x1/github-publish.git ~/.agents/skills/github-publish
```

Folder structure after install:

```
~/.agents/skills/github-publish/
├── SKILL.md      # the agent instructions (the actual skill)
├── README.md     # this file (human-facing docs)
└── LICENSE       # MIT license
```

---

## ⚡ Quick start

In any project folder you want to ship:

1. Run the skill: **"publish it on github do the necessary with readme screenshots and tags"**
2. Follow the prompts — it captures screenshots, writes the README, and pushes to GitHub.
3. Confirm the output checklist below.

---

## ✅ Output checklist

Before you finish, make sure:

- [ ] 📸 UI-only screenshots saved (no background noise)
- [ ] 🎨 Fake/demo background visual present (`docs/demo.gif` or `assets/hero.png`)
- [ ] 🔍 README follows the SEO structure (title, pitch, keywords, badges, features, install, usage, license)
- [ ] 🏷️ Repository description set on GitHub
- [ ] 🏷️ Topics/tags added (5–10)
- [ ] 📦 Code committed and pushed to `main`
- [ ] 🏷️ Release/tag created (optional)

---

## 📝 Example README the skill generates

```markdown
# My Project

A keyword-rich one-line pitch under 60 characters.

Short description with discovery keywords.

![Demo](./docs/demo.gif)

## Badges

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

- Feature 1
- Feature 2

## Installation

```bash
git clone https://github.com/user/repo.git
```

## Usage

```bash
# usage example
```

## Screenshots

![UI screenshot](./docs/screenshots/dashboard.png)

## License

[MIT](LICENSE)
```

---

## 🔖 Topics on this repo

opencode-skill · github-publish · readme-screenshots · seo · readme · agent-skill · publish-to-github · opencode

> Topics are managed in GitHub repo settings and show up as search tags on the repo page.

---

## 📄 License

[MIT License](LICENSE)

---

## 🤝 Contributing

PRs welcome! Open an issue to suggest improvements to the README template, topic list, or publish steps.
