<div align="center">

# Taste Engine

**The design skill that starts with your taste, not the model's defaults.**

A portable, open-source Agent Skill for building distinctive, accessible frontends with user-selected visual styles, anti-slop quality gates, SEO guidance, and purposeful motion.

<p align="center">
  <img src="./assets/banner.webp" alt="Taste Engine — Design systems for AI agents, routed by taste" width="100%" />
</p>

<p align="center">
  <video src="./assets/intro.mp4" poster="./assets/intro-poster.webp" controls="controls" width="100%">
    <a href="./assets/intro.mp4">
      <img src="./assets/intro-poster.webp" alt="Watch Taste Engine Walkthrough Video" width="100%" />
      <br />
      ▶ <b>Watch Intro Video Walkthrough (1 min)</b>
    </a>
  </video>
</p>

[![License: MIT](https://img.shields.io/badge/license-MIT-111111.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.13.1-4F46E5.svg)](CHANGELOG.md)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-111111.svg)](https://agentskills.io/)

[Live Showcase](https://kennedys0.github.io/taste-engine/) · [Installation](#install) · [CLI Setup](#enable-global-taste-engine-cli-command) · [How it works](#how-it-works) · [Styles](#style-library) · [Quality principles](#quality-without-a-house-style) · [Contributing](#contributing)

</div>

## Aesthetic fidelity, not aesthetic labels

The chosen style must be unmistakable in the finished UI. Every style pack in Taste Engine enforces a screenshot-level **Material Fidelity Gate** and provides production-ready CSS reference recipes:

- **Claymorphism:** Volumetric dual inner shadows (highlight + form shadow), soft tinted drop shadows, and sunken relief wells. [Read pack](skills/taste-engine/styles/claymorphism.md) · [CSS recipe](skills/taste-engine/examples/claymorphism/sculpted-surfaces.css) · [Visual QA](skills/taste-engine/tests/claymorphism-visual.md)

- **Frutiger Aero:** Optimistic mid-2000s nature-tech technological vision featuring glossy horizon sheens, aqua/ocean/leaf light fields, and soft dimensional depth. Consolidates three native expressions: **Classic Aero** (default, vibrant aqua gloss), **Aero Glass** (frosted crystalline transparency, preserves Glassmorphism affordances), and **Aero Tactile** (convex physical buttons, preserves Skeuomorphism affordances). [Read pack](skills/taste-engine/styles/frutiger-aero.md) · [CSS recipe](skills/taste-engine/examples/frutiger-aero/glossy-surfaces.css) · [Visual QA](skills/taste-engine/tests/frutiger-aero-visual.md)

- **Brutalism (Raw & Bento):** Raw structural scaffolding, square corners, stark monochrome contrast, and immediate state flips. Features two native layout variants: **Raw** (exposed composition, deliberate visual tension) and **Bento** (modular grid composition with asymmetric panel spans while maintaining strict brutalist materials). [Read pack](skills/taste-engine/styles/brutalism.md) · [CSS recipe](skills/taste-engine/examples/brutalism/raw-surfaces.css)

- **Neo-brutalism:** 2.5px solid black borders, unblurred hard offset shadows, and mechanical press displacement. [Read pack](skills/taste-engine/styles/neo-brutalism.md) · [CSS recipe](skills/taste-engine/examples/neo-brutalism/pop-surfaces.css)

- **Minimalism & Data Cockpit:** Active intentional negative space, mathematical type calibration, hairline dividers, scannable tabular figures (`tabular-nums`), and high-density operational data cockpits (`⌘K`, floating docks, lateral inspectors). [Read pack](skills/taste-engine/styles/minimalism.md) · [CSS recipe](skills/taste-engine/examples/minimalism/clean-surfaces.css)

- **Swiss / Editorial:** Dramatic scale contrast (up to 72px headlines), 12-column grid, structural hairline rules, and section indexes. [Read pack](skills/taste-engine/styles/swiss-editorial.md) · [CSS recipe](skills/taste-engine/examples/swiss-editorial/grid-typography.css)

- **Retro-Terminal:** Authentic CRT phosphor glow, static scanlines, bracketed ASCII frames, and monospace CLI prompts. [Read pack](skills/taste-engine/styles/retro-terminal.md) · [CSS recipe](skills/taste-engine/examples/retro-terminal/crt-console.css)

- **Retro Pixel:** 8-bit and 16-bit pixel illustrations, stepped bevel borders, classic desktop window chrome, arcade orange/teal accents, and integer pixel press displacement. [Read pack](skills/taste-engine/styles/retro-pixel.md) · [CSS recipe](skills/taste-engine/examples/retro-pixel/pixel-surfaces.css) · [Visual QA](skills/taste-engine/tests/retro-pixel-visual.md)

- **Art Deco:** Architectural geometric precision, stepped chevron silhouettes, symmetrical framing, and flat metallic finishes (Antique Gold `#B89B5E`, Muted Brass `#B69A68`, Bronze `#A98462`). Features three expressions: **Modern Deco** (default, generous whitespace), **Classic Deco** (monumental obsidian drama), and **Minimal Deco** (quiet burgundy & bronze). [Read pack](skills/taste-engine/styles/art-deco.md) · [CSS recipe](skills/taste-engine/examples/art-deco/geometric-surfaces.css) · [Visual QA](skills/taste-engine/tests/art-deco-visual.md)

- **Y2K Futurism:** Late-1990s and early-2000s cyber-optimism, polished liquid chrome sheens, iridescent spectral highlights, and chamfered geometric framing. Features three expressions: **Chrome** (default, polished liquid silver), **Holographic** (restrained iridescent spectral accents), and **Retro Tech** (early web cybernetics and modular console framing). [Read pack](skills/taste-engine/styles/y2k-futurism.md) · [CSS recipe](skills/taste-engine/examples/y2k-futurism/metallic-surfaces.css) · [Visual QA](skills/taste-engine/tests/y2k-futurism-visual.md)

## Why Taste Engine?

Most AI-generated interfaces look familiar because the agent chooses a visual direction without asking. Taste Engine changes the order of operations: **discover the user's preference, load exactly the relevant design guidance, implement, and review.**

**No house aesthetic. No default purple gradient. No mandatory framework.** Claymorphism, brutalism, minimalism, swiss-editorial, and other canonical styles are equal first-class choices; legacy `glassmorphism`/`skeuomorphism` requests resolve to Frutiger Aero variants.

## Install

### Recommended: Agent Skills CLI

Requires Node.js and access to GitHub. The repository exposes a standard `skills/taste-engine/SKILL.md` package, so the portable [`skills` CLI](https://github.com/vercel-labs/skills) can discover and install it.

```bash
# Interactive: select an agent and installation scope

npx skills add kennedys0/taste-engine --skill taste-engine

# Install globally for Claude Code

npx skills add kennedys0/taste-engine --skill taste-engine -a claude-code -g -y

# Install globally for Codex

npx skills add kennedys0/taste-engine --skill taste-engine -a codex -g -y

# Install for Antigravity

npx skills add kennedys0/taste-engine --skill taste-engine -a antigravity -g -y

# Install for the Antigravity CLI

npx skills add kennedys0/taste-engine --skill taste-engine -a antigravity-cli -g -y
```

**Antigravity IDE note:** The `skills` CLI may install to a backward-compatible Antigravity path. For the exact current Antigravity IDE global location (`~/.gemini/config/skills/`), use the native installer below. See [the official Antigravity locations](https://antigravity.google/docs/skills).

### Native CLI: exact agent paths, no dependencies

Clone the repository and run the bundled Node.js CLI (Node 20+):

```bash
git clone https://github.com/kennedys0/taste-engine.git

cd taste-engine

# Preview all 10 styles interactively in your browser with live Dark/Light mode toggle

node bin/taste-engine.mjs gallery

# Exact Antigravity IDE global location

node bin/taste-engine.mjs install --agent antigravity --global

# All supported agents in the current project

node bin/taste-engine.mjs install --agent all --project

# Check an installation

node bin/taste-engine.mjs doctor --agent antigravity --global

# Uninstall an installation

node bin/taste-engine.mjs uninstall --agent antigravity --global
```

The installer supports `antigravity`, `antigravity-cli` (alias `agy`), `claude-code` (alias `claude`), `codex`, `cursor`, `cline`, `roo-code` (alias `roo`), `windsurf`, `copilot`, or `all`. It supports `--dry-run`, backs up an existing Taste Engine directory to `.taste-engine-backups/` outside the skills folder before replacing it, and refuses to overwrite or delete an unrelated skill directory. See [INSTALL.md](INSTALL.md) for paths and update options.

### Enable global `taste-engine` CLI command

To run `taste-engine` anywhere in your terminal, create a symlink to the Node CLI or use `npm link`:

```bash
# Option 1: Symlink the Node CLI
mkdir -p ~/.local/bin
ln -sf /path/to/taste-engine/bin/taste-engine.mjs ~/.local/bin/taste-engine
chmod +x ~/.local/bin/taste-engine

# Option 2: npm link from repository root
npm link
```

- `taste-engine -v` — check CLI version (use `taste-engine doctor` to inspect installed skill versions).
- `taste-engine update` — automatically download and apply the latest release from GitHub.
- `taste-engine update --agent <name|all> [--global|--project]` — update a specific agent or all installed targets (e.g. `taste-engine update --agent claude-code --global`).

> **Publication status:** installation commands work after the source files in this repository are published. The presence of a GitHub repository alone does not imply a working skill package or a release asset.

### Tailwind CSS & shadcn/ui Presets

Taste Engine includes official **Tailwind CSS presets** and **shadcn/ui theme variable overrides** across all 10 archetypes (with native layout variants):

```bash
# Preview available presets (alias: taste-engine --preset)

taste-engine preset

# Scaffold Tailwind preset & shadcn themes directly into your project (alias: taste-engine --init)

taste-engine init

# Scaffold into a custom directory, preview with dry-run, or force overwrite

taste-engine init ./src --dry-run
taste-engine --init ./src
taste-engine init --force
```

In your `tailwind.config.js`:

```javascript
module.exports = {

  presets: [require('./taste-presets/tailwind/tailwind.preset.js')],

  content: ['./src/**/*.{js,ts,jsx,tsx}'],

};
```

Read the [Tailwind CSS & shadcn/ui Integration Guide](skills/taste-engine/references/tailwind-shadcn.md) for full component recipes (`.taste-clay-card`, `.taste-aero-card`, `.taste-y2k-card`, `.taste-neo-btn`, etc.).

## How it works

| Your request | Taste Engine behavior |
| --- | --- |
| “Build a portfolio website.” | Ask one question: which visual style? Pause before writing UI code. |
| “Build a Frutiger Aero portfolio.” | Load Frutiger Aero pack immediately. |
| “Build a Y2K Futurism landing page.” | Load Y2K Futurism pack immediately. |
| “Fix the mobile navbar in this project.” | Preserve the existing design system; do not repeat the style question. |
| “Audit the SEO of my website.” | Run the SEO guidance only; do not introduce a style picker. |

The agent's host controls automatic skill discovery. Taste Engine provides a precise `name`/`description` trigger, but does not claim guaranteed invocation across all agents or IDE versions.

<details>

<summary><strong>Example style question</strong></summary>

> Before I start designing, which direction would you prefer: Claymorphism, Frutiger Aero, Brutalism, Neo-brutalism, Minimalism, Swiss/Editorial, Retro Terminal, Retro Pixel, Art Deco, Y2K Futurism, or something custom? You can also share a reference image.

</details>

## Style library

| Style | Visual character | Companion recipe |
| --- | --- | --- |
| **Claymorphism** | Sculpted, tactile surfaces, dual inner-shadow volumetric depth, and soft dimensional presence | [`examples/claymorphism/`](skills/taste-engine/examples/claymorphism/sculpted-surfaces.css) |
| **Frutiger Aero** | Optimistic mid-2000s nature-tech vision, glossy horizon sheens, aqua/ocean/leaf light fields, and soft dimensional depth (Classic, Glass, Tactile) | [`examples/frutiger-aero/`](skills/taste-engine/examples/frutiger-aero/glossy-surfaces.css) |
| **Brutalism** | Direct typography, raw structural scaffolding, intentionally hard edges, and monochrome contrast. Features **Raw** and **Bento** layout variants | [`examples/brutalism/`](skills/taste-engine/examples/brutalism/raw-surfaces.css) |
| **Neo-brutalism** | Playful contrast, 2.5px solid black borders, hard unblurred offset shadows, and press displacement | [`examples/neo-brutalism/`](skills/taste-engine/examples/neo-brutalism/pop-surfaces.css) |
| **Minimalism** | Purposeful restraint, active intentional negative space, mathematical type hierarchy, and high-density operational data cockpits | [`examples/minimalism/`](skills/taste-engine/examples/minimalism/clean-surfaces.css) |
| **Swiss / Editorial** | Typographic rhythm, 12-column grids, dramatic scale contrast, and structural hairline rules | [`examples/swiss-editorial/`](skills/taste-engine/examples/swiss-editorial/grid-typography.css) |
| **Retro Terminal** | Console-inspired phosphor glow, static scanlines, ASCII frames, and monospace CLI prompts | [`examples/retro-terminal/`](skills/taste-engine/examples/retro-terminal/crt-console.css) |
| **Retro Pixel** | Nostalgic 8-bit/16-bit computing, desktop window chrome, stepped pixel bevels, and arcade accents | [`examples/retro-pixel/`](skills/taste-engine/examples/retro-pixel/pixel-surfaces.css) |
| **Art Deco** | Architectural geometric elegance, stepped chevrons, fluted panels, and antique gold/brass finishes (Modern, Classic, Minimal) | [`examples/art-deco/`](skills/taste-engine/examples/art-deco/geometric-surfaces.css) |
| **Y2K Futurism** | Polished liquid chrome finishes, iridescent reflections, chamfered framing, and speculative cyber-optimism (Chrome, Holographic, Retro Tech) | [`examples/y2k-futurism/`](skills/taste-engine/examples/y2k-futurism/metallic-surfaces.css) |

### Frutiger Aero Consolidation & Backward Compatibility

Glassmorphism and Skeuomorphism are consolidated into **Frutiger Aero** as native expressions:
- **Classic Aero (`variant: "classic"`, default):** Bright aqua-inspired palette, glossy dimensional controls, nature-tech balance, and optimistic compositions.
- **Aero Glass (`variant: "glass"`):** Frosted crystalline panels, layered transparency, controlled background blur, and soft luminous borders. Preserves core Glassmorphism design principles.
- **Aero Tactile (`variant: "tactile"`):** Physical material cues, tactile button surfaces, convincing highlights and shadows, and realistic surface depth. Preserves core Skeuomorphism design principles.

**Backward Compatibility:** Requests specifying `style: "glassmorphism"` or `style: "skeuomorphism"` automatically resolve to `style: "frutiger-aero"` with `variant: "glass"` or `variant: "tactile"`. Existing configurations continue working seamlessly.

### Y2K Futurism Specification

Y2K Futurism introduces late-1990s and early-2000s cyber-optimism as an independent 10th archetype:
- **Chrome (`variant: "chrome"`, default):** Polished metallic silver surfaces, high-contrast dark and light zones, chrome-beveled geometric framing, and bold futuristic typography.
- **Holographic (`variant: "holographic"`):** Iridescent accents, controlled spectral gradients, translucent colored layering, and soft chromatic reflections.
- **Retro Tech (`variant: "retro-tech"`):** Early internet cyber-optimism, futuristic industrial typography, modular console panels, and speculative hardware references.

### Brutalism Layout Taxonomy & Bento Consolidation

Bento Grid is consolidated into **Brutalism** as a native layout variant:
- **Raw Brutalism (`variant: "raw"`, default):** Pure structural honesty, visible scaffolding, deliberate visual tension, zero card-boundary mandates, and high-contrast typography.
- **Brutalist Bento (`variant: "bento"`):** Modular grid composition with diverse column/row spans and content prioritization, implemented strictly within brutalist physical laws (0px border-radius, 2px–3px solid borders, zero soft drop shadows, high-voltage signal accents `#ffde00` and `#ff3b30`).

**Backward Compatibility:** Requests specifying `style: "bento"` or prompts mentioning "bento grid" are automatically resolved by the style probe to `style: "brutalism"` with `variant: "bento"`. Existing project configurations specifying `"style": "bento"` are transparently normalized to Brutalist Bento. Neo-Brutalism remains 100% independent and unaffected.

A `custom` design direction is always allowed. Styles do not dictate page sections: the product's goals, content, and audience determine the page anatomy.

## Quality without a house style

Taste Engine separates user taste from non-negotiable engineering quality:

- **Anti-slop:** Reports defects, never authorship. Enforces 5 mechanical structural tests (Deletion, Inversion, Stranger, Attribution, Load-Bearing) across UI, copy, and code surfaces. Eliminates parataxis, triads, em-dash crutches, ghost code wrappers, assertion-free tests, and package hallucinations while preserving user-selected aesthetics.

- **Accessibility:** Semantic HTML, keyboard operation, focus feedback, responsive layout, and reduced-motion alternatives.

- **Public-site SEO:** Truthful metadata, heading structure, indexability checks, internal links, and performance guidance. Never invent a canonical URL or structured data.

- **Full-viewport hero:** New public portfolios and landing pages use a mobile-safe first-screen composition when a hero is appropriate, while respecting explicit instructions for shorter/no heroes.

- **Purposeful motion:** CSS and native APIs first; Anime.js v4 only when interaction complexity justifies it. No default animation dependency.

- **Conditional engineering:** React/Next.js, React Native/Expo, and view-transition guidance load only where applicable. Vue, Svelte, and Astro are not forced into React conventions.

Read the [core skill](skills/taste-engine/SKILL.md), [quality gates](skills/taste-engine/references/quality-tiers.md), [SEO guide](skills/taste-engine/references/seo.md), and [motion engine guide](skills/taste-engine/references/motion-engine.md).

## Repository structure

```text
.

├── skills/taste-engine/      # Canonical skill, references, styles, validation & npx skills discovery

│   ├── SKILL.md

│   ├── styles/               # 10 independent aesthetic packs (with native layout variants)

│   ├── examples/             # Production CSS recipes for all 10 styles

│   ├── references/           # SEO, anti-slop, motion, accessibility, engineering

│   ├── scripts/              # Validator, style probe, SEO auditor, updater

│   └── tests/                # Unit tests and agent evaluation scenarios

├── optional-standalone-skills/

├── bin/taste-engine.mjs      # Native multi-agent installation CLI

├── scripts/                 # Updater sync & release archive builder

└── .github/workflows/       # Validation and versioned releases
```

The canonical source is `skills/taste-engine/` (serving both the native `taste-engine` CLI and `npx skills add` discovery without duplication).

## Development and verification

```bash
python3 scripts/sync-agent-skills.py --check

python3 skills/taste-engine/scripts/validate-pack.py

python3 -m unittest discover -s skills/taste-engine/tests -p 'test_*.py'

node --test tests/cli.test.mjs

python3 scripts/build-release.py
```

The tests verify file structure, routing data, and helper scripts. They are **not a substitute for browser testing** or an empirical guarantee that a coding agent will obey every instruction.

## Updates and releases

For installs managed by the [`skills` CLI](https://github.com/vercel-labs/skills):

```bash
npx skills check

npx skills update -g
```

For the bundled Antigravity updater, once an official GitHub Release exists:

```bash
bash ~/.gemini/config/skills/taste-engine/scripts/update.sh --repo kennedys0/taste-engine
```

Releases are built from tags and include an updater-compatible ZIP. See [INSTALL.md](INSTALL.md) and [CHANGELOG.md](CHANGELOG.md).

## Contributing

Issues, new style proposals, accessibility improvements, translations of optional examples, and evaluation cases are welcome. Contributions must not impose a visual aesthetic on other users. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and follow the [Code of Conduct](CODE_OF_CONDUCT.md) when contributing.

## Sources and attribution

Original implementation, with documented research from [Anti-Slop Design](https://github.com/Ferousco-dev/anti-slop-design), [Hallmark](https://github.com/Nutlope/hallmark), [Anti-AI-Slop Writing](https://github.com/jalaalrd/anti-ai-slop-writing), [Anti-Slop](https://github.com/miqdadbadjuber/anti-slop), [Anti-Slop Structural Engine](https://github.com/AgriciDaniel/anti-slop), [Taste Skill](https://github.com/tasteskill/tasteskill), and [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills). This project is independent of those repositories and does not claim endorsement. See [research notes](skills/taste-engine/references/research-notes.md).

**License:** [MIT](LICENSE). © 2026 Taste Engine contributors.
