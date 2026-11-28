# social-media

<p align="right"><b>🇬🇧 English</b> | <a href="README.tr.md">🇹🇷 Türkçe</a></p>

A local, file-based workspace for planning and running social media marketing for one or more brands/products. Everything — brand info, personas, ideas, monthly plans, generated visuals — lives as plain `.md`, `.json` and image files on your disk. A small web **panel** shows them, lets you edit them, and refreshes live when files change. Optional **Claude Code agents and skills** can fill the files for you.

No database, no account, no cloud. The panel only listens on `127.0.0.1`.

> The panel UI and the built-in templates are in **Turkish**. The file formats, folder layout and code are language-neutral; you can translate the templates in `panel/templates/` to any language.

## Features

- **Multi-project.** Each brand/product is a folder under `projects/`. Create one from the panel with a single click.
- **Brand information pack (33 files).** A ready-made set of templates in 7 folders (identity, brand, visual identity, audience, competition, strategy, measurement). Each file has a priority (P1–P3), a status (`bos` / `taslak` / `tamam` / `uygulanmaz`), a source, and an "open questions" checklist.
- **Readiness tracking.** Per-folder and overall completion percentage, a "ready to plan" check (all P1 files at least a draft), stale P1 files (older than 90 days), and a list of every open question across the pack.
- **Personas.** Create, edit and delete audience personas in the panel (card view and "team desk" view, 50 pixel-art avatars, filters by segment / skepticism / platform). Saved to `personas.json`.
- **Plan & drafts.** Monthly plan (`plan.md`), post drafts (`drafts.json`) and persona-based scores (`scores.json`) shown in a calendar-style tab.
- **Ideas board.** One markdown file per idea, created from the panel.
- **Gallery.** Browse images and videos (reference material and generated output), with range streaming for video.
- **Brand card.** Accent colour and fonts are extracted automatically from your colour palette / typography files.
- **Full-text search + command palette** (`Ctrl/Cmd + K`), in-memory, typo tolerant.
- **Built-in editor** for markdown/JSON/YAML with conflict detection (if a file changed on disk, you are warned instead of overwriting).
- **Live refresh.** Edit a file anywhere (your editor, git, Claude Code) and the panel updates; unsaved text in an open editor is never overwritten.
- **Claude Code integration (optional).** 6 sub-agents and 7 skills for filling the brand pack, writing posts, planning a month, auditing content and generating images/video with [fal](https://fal.ai).

## Quick start

Requirements: **Node.js ≥ 20** and npm. Git, if you want to clone.

```bash
git clone <this-repo-url> social-media
cd social-media/panel
npm install
npm run dev          # panel: http://127.0.0.1:5177
```

Open `http://127.0.0.1:5177`, click **Yeni proje** (new project), type a brand name, and start filling the files.

Want to look around with sample data first?

```bash
npm run seed                    # copies the fictional sample project `ornek-kahve` into panel/.demo (never overwrites)
npm run dev -- --root .demo     # open the panel on the sample data
```

### Everyday use (single port)

```bash
npm run build        # once, and again after pulling UI changes
npm start            # http://127.0.0.1:4177
```

## Does the panel really create and edit files?

Yes. Every action in the panel is a file operation inside `projects/<project>/`:

| In the panel | What happens on disk |
|---|---|
| **New project** | Creates `projects/<slug>/` with the 33 template `.md` files, `personas.json` (`[]`), `learnings.md` and empty `fikirler/ plan/ gorseller/ performans/` |
| **Add missing files** | Copies only the templates the project doesn't have yet; never overwrites |
| **Create / edit / delete a persona** | Rewrites `personas.json` (2-space indent) |
| **Edit a markdown file** | Writes that `.md` file; updates `son_guncelleme` in the frontmatter |
| **Change a file's status** | Patches the frontmatter only, body untouched |
| **New idea** | Creates `fikirler/<name>.md` |
| **New file / folder** (Files tab) | Creates it (`.md`, `.json`, `.yaml` only) |

Writes are atomic (temp file + rename). You can equally edit all of these files in VS Code, with git, or with Claude Code — the panel picks the change up instantly.

## Project layout

```
social-media/
├─ panel/                 # the web panel (Vite + React SPA, Hono file API)
├─ projects/              # YOUR DATA — git-ignored, one folder per brand
│  └─ my-brand/
│     ├─ 00-kunye/ … 06-olcum/    # the brand information pack (markdown)
│     ├─ personas.json
│     ├─ learnings.md
│     ├─ fikirler/                 # ideas, one .md each
│     ├─ plan/YYYY-MM/{plan.md, drafts.json, scores.json}
│     ├─ gorseller/{referans/, YYYY-MM/}
│     └─ performans/
├─ shared/marka-bilgi-paketi.md   # source list of the 33-file pack
├─ .claude/               # optional Claude Code agents + skills
├─ CLAUDE.md              # rules for Claude Code in this folder
└─ README.md / README.tr.md
```

`projects/` is git-ignored on purpose: your brand data stays private and the repo stays clean. If you want to version your own content, run `git init` inside `projects/` (or keep it in a separate private repo).

## File formats

**Markdown frontmatter** (all optional; broken/missing frontmatter still opens)

```yaml
---
baslik: Ses tonu          # title
oncelik: P1               # P1 | P2 | P3
durum: taslak             # bos | taslak | tamam | uygulanmaz
kaynak: brand-guide.pdf   # where the information came from
son_guncelleme: 2026-11-02
---
```

Body sections used by the panel: `## Neden önemli`, `## Doldurulacaklar`, `## Cevaplanması gereken sorular` (items `- [ ]` are open questions, `- [x]` answered).

Readiness: `tamam` = 1, `taslak` = 0.5, `bos` = 0, `uygulanmaz` is excluded.

**`personas.json`** — array; only `id` is required

```json
[
  {
    "id": "brand-01", "ad": "Selin", "yas": 29, "meslek": "…",
    "hedef_segment": "b2c", "platformlar": ["instagram", "x"],
    "dijital_alışkanlık": "…", "satin_alma_tutumu": "…",
    "supheci_mi": true, "dikkat_suresi": "kisa",
    "tetikleyiciler": ["…"], "itici_seyler": ["…"],
    "ses_tonu": "…", "avatar": 17
  }
]
```

**`plan/YYYY-MM/drafts.json`** — array of `{ id, tarih, platform, format, kanca, metin?, durum?, persona_ids? }`.
**`scores.json`** — `{ "<draftId>": { "genel": 7, "personalar": { "<personaId>": 8 } } }` (array forms are accepted too).

Full API and rules: [`panel/CONTRACT.md`](panel/CONTRACT.md) · panel details: [`panel/README.md`](panel/README.md).

## Using Claude Code (optional)

The panel works without any AI. If you use [Claude Code](https://claude.com/claude-code), open the `social-media/` folder in it and the agents/skills in `.claude/` become available:

| Skill | Purpose |
|---|---|
| `marka-paketi-doldur` | Fill the brand pack from your docs/repo, honestly (no invented facts) |
| `aylik-plan-uret` | Produce `plan.md` + `drafts.json` for a month |
| `gonderi-yaz` | Write a single post |
| `icerik-denetle` | Pre-publish checklist (tone, claims, legal) |
| `referans-ice-aktar` | Import your first images/videos as brand references |
| `fal-gorsel-uret` / `fal-video-uret` | Generate images/videos with fal |

Agents: `sosyal-medya-stratejisti`, `icerik-yazari`, `gorsel-uretim-yonetmeni`, `marka-denetcisi` (review only), `arastirmaci`, `paket-doldurucu`.

Rules baked in (see `CLAUDE.md`): no invented numbers/customers/prices — unknown things stay as open questions; a file is `tamam` only after your approval or a verified source.

**Image/video generation** needs a fal key in the `FAL_KEY` environment variable. Never put it in a file that gets committed (`.env*` is git-ignored).

## Configuration

| Setting | How |
|---|---|
| Projects folder | `--root <dir>` or env `PANEL_ROOT` (default `<repo>/projects`) |
| Port | env `PANEL_PORT` (default `4177`; dev UI uses `5177`) |

## Security

- Binds to `127.0.0.1` only; requests with a foreign `Host`/`Origin` are rejected (DNS-rebinding / CSRF guard).
- Path traversal, symlink escapes, `.env*`, `.git`, `node_modules` and `panel/` are never read or listed. Writes are limited to `.md .json .yaml .yml`.
- Don't expose the panel to a network (no authentication).

## Development

```bash
cd panel
npm test            # node:test unit + API tests
npm run avatars     # regenerate avatars (output is deterministic)
```

To add a template file: write it under `panel/templates/marka-paketi/<folder>/`, register it in `_manifest.json`, add a row to `shared/marka-bilgi-paketi.md` (the test suite checks consistency), then use **Add missing files** in existing projects.

## Credits

Avatars: [DiceBear](https://www.dicebear.com) pixel-art (design CC0 1.0, code MIT). Pixel font: Pixelify Sans (SIL OFL). Built with Vite, React, Hono, chokidar, MiniSearch, gray-matter, Zod.

## License

No license file has been added yet. Until the owner adds one, all rights are reserved.
