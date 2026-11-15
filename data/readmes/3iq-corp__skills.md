# 3iQ Skills Hub

A [GitHub-backed skills hub](https://github.com/anthropics/skills) for
[3iQ Corp](https://3iq.io) — a Toronto-based institutional digital-asset
manager. This repo hosts the skills we install into [OpenCode][opencode],
[OpenWork][openwork], and [Claude][claude] to keep everything on brand.

[opencode]: https://opencode.ai
[openwork]: https://differentai.com
[claude]: https://claude.com

## Structure

```
├── anthropic/                    # Curated skills from Anthropic (auto-synced weekly)
│   ├── algorithmic-art/
│   ├── brand-guidelines/
│   ├── canvas-design/
│   ├── claude-api/
│   ├── doc-coauthoring/
│   ├── docx/
│   ├── frontend-design/
│   ├── internal-comms/
│   ├── mcp-builder/
│   ├── pdf/
│   ├── pptx/
│   ├── skill-creator/
│   ├── slack-gif-creator/
│   ├── theme-factory/
│   ├── web-artifacts-builder/
│   ├── webapp-testing/
│   └── xlsx/
├── 3iq/                          # 3iQ proprietary skills
│   ├── 3iq-brand/
│   └── make-it-matter-brand/
├── anthropic-skills.json         # Config: which Anthropic skills to track
├── setup.sh                      # macOS/Linux installer
├── setup.ps1                     # Windows installer
└── .github/workflows/
    └── sync-anthropic.yml        # Weekly auto-sync from Anthropic
```

## Skills

### 3iQ Custom

| Skill | Description |
|---|---|
| [`3iq-brand`](./3iq/3iq-brand/) | Full 3iQ brand system — palette, typography, gradients, logo rules, voice, JSX components |
| [`make-it-matter-brand`](./3iq/make-it-matter-brand/) | Make It Matter brand system |

### Anthropic (curated)

All 17 skills from [`anthropics/skills`](https://github.com/anthropics/skills),
kept in sync via a weekly GitHub Action. Edit [`anthropic-skills.json`](./anthropic-skills.json)
to add or remove skills from the tracked list.

---

## Installing

### Quick Start

```bash
# Clone the repo
git clone https://github.com/3iQ-Corp/skills.git
cd skills

# macOS / Linux
./setup.sh

# Windows (PowerShell — run as Admin or enable Developer Mode)
.\setup.ps1
```

The setup scripts create symlinks from this repo into your OpenCode skills
directory, so `git pull` keeps everything current.

### Skills Directories by OS

| OS | Path |
|---|---|
| macOS | `~/.config/opencode/skills/` |
| Linux | `~/.config/opencode/skills/` (or `$XDG_CONFIG_HOME/opencode/skills/`) |
| Windows | `%APPDATA%\opencode\skills\` |

### OpenWork Hub

1. Open workspace settings → **Available from Hub**
2. Click **Add git repo** → enter `3iQ-Corp/skills@main`
3. Click **Refresh hub** — you'll see all skills listed
4. Click a skill → **Install** on the worker you want

### Zip Install (no git, no admin)

1. Download: **https://github.com/3iQ-Corp/skills/archive/refs/heads/main.zip**
2. Extract and copy skill folders from `anthropic/` and `3iq/` into your skills directory (see table above)

### Updating

```bash
cd /path/to/skills && git pull
```

Symlinks stay valid — new skills need another `./setup.sh` run.

---

## Managing Anthropic Skills

### Add a skill

1. Add the skill name to the `skills` array in `anthropic-skills.json`
2. Run the sync Action manually (Actions tab → "Sync Anthropic Skills" → "Run workflow")
3. Merge the resulting PR
4. Team members: `git pull`

### Remove a skill

1. Remove the skill name from `anthropic-skills.json`
2. Delete the folder from `anthropic/`
3. Commit and push
4. Team members: `git pull` and re-run setup to clean up the symlink

### How auto-sync works

A GitHub Action runs every Monday at 9:00 AM UTC. It:

1. Reads `anthropic-skills.json` for the tracked skill list
2. Fetches the latest from [`anthropics/skills`](https://github.com/anthropics/skills)
3. Diffs against what's in `anthropic/`
4. Opens a PR if anything changed — you review before merging

---

## Adding 3iQ Custom Skills

1. Create a new folder under `3iq/` with a `SKILL.md` file
2. Commit and push
3. Team members: `git pull` + re-run setup if new

---

## Troubleshooting

**Skill doesn't trigger.** Check the skill folder contains `SKILL.md`
directly (not nested) and is properly symlinked into your skills directory.

**Windows: symlink creation fails.** Enable Developer Mode in Windows
Settings, or run PowerShell as Administrator. Alternatively, use the zip
install method.

**Old references to `3iQ-Corp/design-system`.** This repo was renamed in
April 2026. GitHub auto-redirects, but update your remote:

```sh
git remote set-url origin https://github.com/3iQ-Corp/skills.git
```

---

## Sources

All 3iQ brand content is derived from:

- **GitHub** — this repo (formerly `3iQ-Corp/design-system`)
- **Live site** — [3iq.io](https://3iq.io) — upstream source for colors, type, and spacing

Nothing is invented. If you find a decision that doesn't trace back to
one of those sources, flag it.

## License

3iQ skills are for internal 3iQ Corp use. Licensed fonts
(`3iq/3iq-brand/fonts/`) are covered by their respective EULAs and must
not be redistributed outside 3iQ. Anthropic skills are subject to their
[upstream license](https://github.com/anthropics/skills).
