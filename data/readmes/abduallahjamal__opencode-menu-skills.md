<div align="center">

<img src="assets/banner.svg" alt="opencode-menu-skills — 8 Arabic RTL menu production skills + /menu" width="100%">

<br>

**Eight [OpenCode](https://opencode.ai) Agent Skills + `/menu` command for producing *print-ready, zero-drift Arabic RTL café & restaurant menus* — separating photography from live HTML/CSS typography and 300-DPI booklet production.**

[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e.svg?style=flat-square)](LICENSE)
[![OpenCode](https://img.shields.io/badge/OpenCode-Skills-38bdf8.svg?style=flat-square)](https://opencode.ai/docs/skills/)
[![Skills](https://img.shields.io/badge/skills-8-818cf8.svg?style=flat-square)](#-the-eight-skills)
[![Command](https://img.shields.io/badge/command-%2Fmenu-a78bfa.svg?style=flat-square)](#-end-to-end-production-pipeline)
[![RTL](https://img.shields.io/badge/Arabic-RTL-a78bfa.svg?style=flat-square)](#-the-idea-in-one-line)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-d97757.svg?style=flat-square)](#-one-standard-three-agents)
[![Codex](https://img.shields.io/badge/Codex%20CLI-compatible-10a37f.svg?style=flat-square)](#-one-standard-three-agents)
[![CI](https://img.shields.io/github/actions/workflow/status/abduallahJamal/opencode-menu-skills/validate.yml?branch=main&style=flat-square&label=CI&color=0ea5a4)](.github/workflows/validate.yml)
[![Docs](https://img.shields.io/badge/docs-English%20%2B%20العربية-0f172a.svg?style=flat-square)](#-usage)

**🌐 English** · **[العربية](README.ar.md)**

</div>

---

## 📌 The idea in one line

Asking an AI image generator to draw an Arabic menu directly produces **garbled Arabic letters, hallucinated prices, and uneditable layouts**. **Menu (`opencode-menu-skills`)** enforces a studio-grade separation of concerns: **verified JSON item/price schema → strictly text-free AI food photography → real Arabic RTL typography in A4 HTML/CSS → 300-DPI Chromium rendering → page-by-page visual QA & saddle-stitch print packaging**.

| | Naive AI Menu Generation | With `opencode-menu-skills` (`/menu`) |
|---|---|---|
| **Arabic text** | Melted/broken letters baked into raster images | Crisp, local `@font-face` **Arabic RTL** typography in HTML/CSS |
| **Prices & items** | Hallucinated numbers, missing or duplicated items | Validated **single JSON source of truth** (`validate_menu_data.py`) |
| **Photography** | Cluttered fake text and watermarks inside images | Art-directed **zero-text food & venue photography** + QA rubric |
| **Print geometry** | Random aspect ratios, blurry exports | Exact A4 `1240×1754` CSS px rendered `@2x` → **`2480×3508` (300 DPI)** |
| **Quality control** | Delivered with clipped footers & overflow | Automated DOM audit (`audit_html.py`) + **visual page-by-page QA** |
| **Press handoff** | Odd page counts rejected by print shops | Saddle-stitch **multiples of 4 (`4n`)**, TOC, back cover & print PDF/ZIP |

---

## 🧩 The eight skills

### 🍽️ `menu` — Master Orchestrator & `/menu` Command
Coordinates the full pipeline from raw client items and logo to final print-ready PDF and 300-DPI page exports — enforcing zero hallucinated data, strict separation between photography and text, and mandatory visual sign-off.

### 🗂️ `menu-data-architect` — Canonical JSON Schema & Price Integrity
Normalizes categories, item names, multi-size variants, and featured repeats into a single validated JSON file — bundled with `scripts/validate_menu_data.py`, `assets/menu-data.template.json`, and a complete 67-item reference dataset (`assets/sample-menu-data.example.json`).

### 🎨 `brand-asset-prep` — Logo, Palette & Local Arabic Fonts
Inspects logo resolution/transparency, produces clean circular/transparent crops (`scripts/crop_logo_circle.py`, `scripts/inspect_assets.py`), extracts brand color tokens, and downloads offline Arabic font families (`scripts/download_google_fonts.py`).

### 📸 `cafe-image-art-director` — Zero-Text Food & Venue Photography
Crafts cohesive art-direction prompts for hero covers and category headers (`references/prompt-library.md`) with strict negative constraints against embedded text/logos, backed by `references/image-qa-rubric.md`.

### 📐 `arabic-rtl-menu-designer` — A4 RTL HTML/CSS Design Systems
Builds print-locked A4 pages (`1240×1754` CSS px) with complete `:root` CSS custom-property palettes (Cream Classic, Dark Luxury,Editorial Daylight), dotted price leaders, badges, and starter template `assets/menu-page-template.html`.

### 🖥️ `playwright-menu-renderer` — 300-DPI Chromium Export Engine
Renders multi-page HTML menus via headless Chromium at `device_scale_factor=2` (`2480×3508` px PNG/JPG) plus unified print PDF and press archive (`scripts/render_menu.py`).

### 🔍 `visual-menu-qa` — DOM & Visual Page-by-Page QA
Detects text overflow, footer collisions, broken images, and price-count mismatches programmatically (`scripts/audit_html.py`) alongside a structured visual inspection checklist (`references/qa-checklist.md`).

### 📖 `booklet-print-producer` — Saddle-Stitch Booklet & Press Handoff
Converts arbitrary page counts into press-ready multiples of 4 (`4, 8, 12, 16`), adds table-of-contents and back-cover layouts, verifies PDF page counts (`scripts/verify_pdf.py`), and packages final deliverables (`scripts/package_outputs.py`).

---

## 🔄 End-to-end production pipeline

```text
Raw Items + Logo
   │
   ▼
1. menu-data-architect      → Validated menu-data.json (exact item & price counts)
   │
   ├─► 2. brand-asset-prep       → Clean logo + brand palette + local Arabic fonts
   └─► 3. cafe-image-art-director→ Text-free hero & category food photography
   │
   ▼
4. arabic-rtl-menu-designer → Self-contained A4 RTL HTML/CSS pages (1240×1754 px)
   │
   ▼
5. playwright-menu-renderer → 2480×3508 (300-DPI) PNG/JPG pages + print PDF
   │
   ▼
6. visual-menu-qa           → Zero clipping, zero overflow, 100% price parity
   │
   ▼
7. booklet-print-producer   → 4n booklet pagination + verified press ZIP/PDF
```

---

## 🧩 One standard, three agents

Built on the open [Agent Skills specification](https://agentskills.io/specification) — every skill directory (including its bundled `scripts/`, `assets/`, and `references/`) works seamlessly across OpenCode, Claude Code, and Codex CLI:

| Agent | Project path | Global path | Invocation |
|---|---|---|---|
| **OpenCode** | `.opencode/skills/` + `.opencode/commands/` | `~/.config/opencode/` | `/menu` or `use skill menu` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | `/menu`, `/arabic-rtl-menu-designer`, … |
| **Codex CLI** | `.agents/skills/` | `~/.agents/skills/` | `$menu` or `/skills` |

`.opencode/skills/` is the **single source of truth**; `.claude/skills/` and `.agents/skills/` are generated and verified via recursive SHA-256 manifests:

```bash
./scripts/sync-platforms.sh          # sync all 8 full skill directories to .claude/ and .agents/
./scripts/sync-platforms.sh --check  # fail on any file drift (enforced in GitHub Actions CI)
```

---

## 🚀 Installation

### Option 1 — Multi-agent installer (recommended)

```bash
git clone https://github.com/abduallahJamal/opencode-menu-skills.git
cd opencode-menu-skills

# Global install for OpenCode + Claude Code + Codex CLI
./install.sh --all --global

# Or install into a specific menu project
./install.sh --all --project /path/to/your-menu-project
```

Windows PowerShell is also supported via `.\install.ps1 global` or `.\install.ps1 project C:\path\to\project`.

### Option 2 — Python runtime dependencies (for rendering & PDF verification)

```bash
python -m pip install playwright pillow pypdf pyyaml
python -m playwright install chromium
```

### Option 3 — Optional OpenCode skill permissions

Merge [`opencode.example.json`](opencode.example.json) into your project's `opencode.json` to pre-authorize all 8 menu skills without overwriting existing project settings.

---

## 🧪 Usage

Open your menu workspace in OpenCode and run:

```text
/menu
Create an 8-page A4 print-ready Arabic RTL café menu using the attached logo and item list.
Keep every item name and price exact, generate text-free category photography, render 300-DPI
pages + print PDF, and verify every page visually before delivery.
```

See ready-to-copy prompts for individual stages in **[English Usage Examples](docs/usage-examples.en.md)** and **[أمثلة الاستخدام بالعربية](docs/usage-examples.md)**.

---

## 📁 Repository structure

```text
opencode-menu-skills/
├── .opencode/
│   ├── commands/menu.md                           # /menu slash command
│   └── skills/                                    # canonical source of truth (8 skills + scripts/assets)
│       ├── menu/                                  # master orchestrator + case study & checklist
│       ├── menu-data-architect/                   # JSON validator + template & 67-item sample JSON
│       ├── brand-asset-prep/                      # logo crop/inspect + Google Fonts downloader
│       ├── cafe-image-art-director/               # prompt library + photography QA rubric
│       ├── arabic-rtl-menu-designer/              # A4 RTL HTML template + 3 CSS design systems
│       ├── playwright-menu-renderer/              # 300-DPI Chromium renderer (PNG/JPG/PDF/ZIP)
│       ├── visual-menu-qa/                        # automated HTML overflow auditor + QA checklist
│       └── booklet-print-producer/                # 4n booklet playbook + PDF verifier & packager
├── .claude/skills/                                # generated → Claude Code
├── .agents/skills/                                # generated → Codex CLI / Cursor / Gemini
├── docs/                                          # bilingual prompt examples (EN + AR)
├── assets/banner.svg                              # repository header banner
├── scripts/
│   ├── sync-platforms.sh                          # recursive multi-agent sync + SHA-256 drift check
│   ├── validate.py                                # Python CI validator (frontmatter + scripts + docs)
│   └── publish.sh                                 # GitHub publishing helper
├── opencode.example.json                          # optional OpenCode skill permission snippet
├── install.sh / install.ps1                       # Linux/macOS & Windows installers
├── AGENTS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

---

## 🤝 Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Before submitting a pull request, run:

```bash
bash -n install.sh scripts/*.sh
./scripts/sync-platforms.sh --check
python3 scripts/validate.py
```

---

## 📜 License

Released under the [MIT License](LICENSE).
