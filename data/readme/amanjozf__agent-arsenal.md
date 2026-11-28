# ⚡ Agent Arsenal: Curated AI Coding Skills & Customizations

A curated, personal catalog of high-impact AI coding skills, agent prompt rules, multi-provider gateways, UI design engines, browser automation, and persistent memory workflows for Claude Code, Antigravity, Cursor, Codex, OpenCode, and any `AGENTS.md`-compatible assistant.

> **💡 Quick Tip:** Every skill folder contains a `WHAT_THIS_DOES.txt` file with a 1–3 sentence explanation and a real-world prompt example for instant reference!

---

## 📚 Categorized Skills Catalog

### 💻 1. Coding & Engineering Playbooks (`skills/coding/`)
| Skill | Description | Quick Install | Source | Details |
|---|---|---|---|---|
| [**Caveman**](./skills/coding/caveman/) | **Terse Mode & Token-Saving Suite**<br>Cuts 40-70% of output tokens by stripping conversational filler and pleasantries while keeping code exact. Includes `/caveman-commit` for minimal Conventional Commits and memory compression. | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/coding/caveman/AGENTS.md -o AGENTS.md` | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | [Setup Guide](./skills/coding/caveman/README.md) |
| [**Ponytail**](./skills/coding/ponytail/) | **Minimalist Senior Dev Mode**<br>Reduces code bloat (-53%), cuts tokens (-45%), ensures 98% risky logic is tested, and forbids premature abstraction. Includes 5 review/audit tools. | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/coding/ponytail/AGENTS.md -o AGENTS.md` | [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail) | [Setup Guide](./skills/coding/ponytail/README.md) |
| [**Vercel Suite**](./skills/coding/vercel-suite/) | **Vercel Labs Engineering Suite (33k+ stars)**<br>Official performance rules for React 19 / Next.js (Server Components, Suspense streaming), view transitions, composition patterns, and automated deployment. | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/coding/vercel-suite/AGENTS.md -o AGENTS.md` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | [Setup Guide](./skills/coding/vercel-suite/README.md) |
| [**Agent Skills (Addy Osmani)**](./skills/coding/agent-skills/) | **Production-Grade Engineering Skills**<br>25 battle-tested senior engineering skills by Addy Osmani (Google Chrome Lead): TDD, spec design, code review, simplification, debugging, and security. | `/plugin marketplace add addyosmani/agent-skills && /plugin install agent-skills@agent-skills` | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | [Setup Guide](./skills/coding/agent-skills/README.md) |

---

### 🌐 2. Gateways & Infrastructure (`skills/gateways/`)
| Skill | Description | Quick Install | Source | Details |
|---|---|---|---|---|
| [**OmniRoute**](./skills/gateways/omniroute/) | **Multi-Provider AI Gateway & Router**<br>One OpenAI-compatible endpoint for 375+ providers & 1,400+ models. Auto-fallback, RTK token compression (saves 15-95%), and 46 sub-skills. | `npm install -g omniroute && omniroute serve --daemon` | [cheaper-inference/OmniRoute](https://github.com/cheaper-inference/OmniRoute) | [Setup Guide](./skills/gateways/omniroute/README.md) |
| [**FreeLLMAPI**](./skills/gateways/freellmapi/) | **Free LLM Gateway & Pool Router**<br>Aggregates 7.4B tokens/mo across 34 free providers & 635 models behind one /v1 endpoint with auto-setup generators for Claude Code, Cursor, Codex, and Aider. | `curl -fsSL https://freellmapi.co/install.sh \| bash` | [tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi) | [Setup Guide](./skills/gateways/freellmapi/README.md) |

---

### 🎬 3. Video & Media Generation (`skills/video-media/`)
| Skill | Description | Quick Install | Source | Details |
|---|---|---|---|---|
| [**Watch**](./skills/video-media/watch/) | **Video Understanding for Coding Agents**<br>Extracts timestamped frames and transcripts from YouTube, Loom, or local MP4s with `/watch`. Allows agents to recreate UI and isolate bugs directly from video. | `/plugin marketplace add bradautomates/claude-video && /plugin install watch@claude-video` | [bradautomates/claude-video](https://github.com/bradautomates/claude-video) | [Setup Guide](./skills/video-media/watch/README.md) |
| [**HyperFrames**](./skills/video-media/hyperframes/) | **HTML-to-Video Engine for Agents**<br>Enables agents to write standard HTML/CSS/GSAP and deterministically render frame-by-frame MP4/WebM videos, launch films, animations, and social clips. Includes 9 sub-skills. | `npx skills add heygen-com/hyperframes` | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | [Setup Guide](./skills/video-media/hyperframes/README.md) |
| [**Brag**](./skills/video-media/brag/) | **Automated Launch Video Generator**<br>Inspects your codebase and UI to automatically compose, storyboard, and render an animated product demo video with music and narration. | `/plugin marketplace add latent-spaces/brag && /plugin install brag@brag` | [latent-spaces/brag](https://github.com/latent-spaces/brag) | [Setup Guide](./skills/video-media/brag/README.md) |

---

### 🎨 4. Design & UI Systems (`skills/design/`)
| Skill | Description | Quick Install | Source | Details |
|---|---|---|---|---|
| [**UI/UX Pro Max**](./skills/design/ui-ux-pro-max/) | **#1 Design Intelligence & Search Engine (147k+ stars)**<br>Searchable database of color palettes by industry, Google Fonts pairings, UI styles (glassmorphism, brutalism), and UX anti-pattern checklists across 7 sub-skills. | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/design/ui-ux-pro-max/AGENTS.md -o AGENTS.md` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | [Setup Guide](./skills/design/ui-ux-pro-max/README.md) |
| [**Framer Motion**](./skills/design/framer-motion/) | **Production React Animation Engine & Physics**<br>Pre-calibrated spring physics presets, shared layout morphing (`layoutId`), scroll-linked triggers (`useScroll`), and exit animations (`AnimatePresence`). | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/design/framer-motion/AGENTS.md -o AGENTS.md` | [Motion.dev](https://motion.dev/) | [Setup Guide](./skills/design/framer-motion/README.md) |
| [**Taste Skill**](./skills/design/taste-skill/) | **Anti-Slop Art Direction & Design Engine (112k+ stars)**<br>Eliminates generic AI slop, purple blobs, and repetitive cards. Enforces real editorial typography, spacing, authentic photography, and quiet micro-interactions matching Figma and x.ai. | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/design/taste-skill/AGENTS.md -o AGENTS.md` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | [Setup Guide](./skills/design/taste-skill/README.md) |
| [**Image-to-Code Skill**](./skills/design/image-to-code-skill/) | **Image-First Art Direction & Implementation**<br>Directs agents to design spacious heroes, avoid "cards-inside-cards" UI, and implement pixel-perfect visual mockups optimized for real laptop viewports. | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/design/image-to-code-skill/AGENTS.md -o AGENTS.md` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | [Setup Guide](./skills/design/image-to-code-skill/README.md) |
| [**Web Design Guidelines**](./skills/design/web-design-guidelines/) | **Vercel Labs Web Interface Guidelines (33k+ stars)**<br>Audits and guides UI code against Vercel's production standards: accessibility (WCAG AA), semantic tags, touch targets, keyboard navigation, and zero layout shift. | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/design/web-design-guidelines/AGENTS.md -o AGENTS.md` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | [Setup Guide](./skills/design/web-design-guidelines/README.md) |
| [**Awesome Design MD**](./skills/design/awesome-design/) | **84+ Iconic Tech Brand Design Systems (126k+ stars)**<br>Complete token contracts (`DESIGN.md`) for Stripe, Linear, Apple, Vercel, Supabase, Tesla, Notion, Raycast, and Figma so agents build authentic brand UIs. | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/design/awesome-design/AGENTS.md -o AGENTS.md` | [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | [Setup Guide](./skills/design/awesome-design/README.md) |
| [**img2threejs**](./skills/design/img2threejs/) | **Image-to-Procedural 3D Three.js (21k+ stars)**<br>Reconstructs any 2D object image into an interactive, code-only Three.js 3D model with PBR materials, orbit controls, and studio lighting—no external 3D files needed. | `npx --yes img2threejs@latest install` | [img2threejs/img2threejs](https://github.com/img2threejs/img2threejs) | [Setup Guide](./skills/design/img2threejs/README.md) |
| [**21st.dev**](./skills/design/21st-dev/) | **Design Engineer & UI Component Generator**<br>Marketplace of 10,000+ production React/Tailwind (shadcn-compatible) components, AI UI generation like v0, and official SVG brand logo search via MCP. | `npx @21st-dev/cli@latest init --client cursor` | [21st-dev/magic-mcp](https://github.com/21st-dev/magic-mcp) | [Setup Guide](./skills/design/21st-dev/README.md) |
| [**Screenshot to Code**](./skills/design/screenshot-to-code/) | **Visual Frontend & Mockup Replicator (65k+ stars)**<br>Converts any UI screenshot, Figma design, or wireframe into clean, responsive HTML, React, or Vue code with Tailwind CSS matching typography, colors, and layout. | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/design/screenshot-to-code/AGENTS.md -o AGENTS.md` | [abi/screenshot-to-code](https://github.com/abi/screenshot-to-code) | [Setup Guide](./skills/design/screenshot-to-code/README.md) |
| [**Uiverse Galaxy**](./skills/design/uiverse/) | **Open-Source CSS & Tailwind Micro-Components (14k+ stars)**<br>Catalog of 3,000+ community UI micro-components: neon buttons, glassmorphic cards, animated loaders, and toggle switches with zero npm dependencies. | `curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/design/uiverse/AGENTS.md -o AGENTS.md` | [uiverse-io/galaxy](https://github.com/uiverse-io/galaxy) | [Setup Guide](./skills/design/uiverse/README.md) |

---

### 🌐 5. Browser Automation & Scraping (`skills/browser-automation/`)
| Skill | Description | Quick Install | Source | Details |
|---|---|---|---|---|
| [**Playwright CLI**](./skills/browser-automation/playwright-cli/) | **Token-Efficient Playwright CLI & Skills (15k+ stars)**<br>Microsoft's CLI-based browser automation for coding agents: tests flows and takes screenshots without bloating context windows with heavy accessibility trees. | `npm install -g @playwright/cli@latest && playwright-cli install --skills` | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) | [Setup Guide](./skills/browser-automation/playwright-cli/README.md) |
| [**Playwright MCP**](./skills/browser-automation/playwright-mcp/) | **Microsoft Playwright Browser Automation**<br>Control real Chromium/Firefox browsers directly from your agent: click elements, fill forms, navigate pages, and capture screenshots via MCP protocol. | `npx -y @playwright/mcp@latest` | [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | [Setup Guide](./skills/browser-automation/playwright-mcp/README.md) |
| [**Apify MCP**](./skills/browser-automation/apify/) | **Web Scraping & Cloud Actors**<br>Extract clean data from any website without getting blocked, search Google in real-time, and run 1,500+ pre-built cloud scrapers (YouTube, Twitter, LinkedIn). | `npx -y @apify/actors-mcp-server` | [apify/apify-mcp-server](https://github.com/apify/apify-mcp-server) | [Setup Guide](./skills/browser-automation/apify/README.md) |

---

### 🧠 6. Persistent Memory (`skills/memory/`)
| Skill | Description | Quick Install | Source | Details |
|---|---|---|---|---|
| [**Mem0**](./skills/memory/mem0/) | **Persistent Memory Layer for Agents**<br>Solves context drift and prompt fading by continuously remembering your personal coding preferences, habits, and rules across conversations and sessions. | `npx -y @mem0/mcp` | [mem0ai/mem0](https://github.com/mem0ai/mem0) | [Setup Guide](./skills/memory/mem0/README.md) |

---

### ⚙️ 7. Device Automation & Debloat (`skills/automation/`)
| Skill | Description | Quick Install | Source | Details |
|---|---|---|---|---|
| [**CleanYourTV**](./skills/automation/cleanyourtv/) | **Smart TV Debloater & Ad-Removal**<br>Connects your AI agent to any Android TV / Google TV over Wi-Fi via ADB to safely disable ads, telemetry, and sponsored rows with zero root required. | `python tools/check.py <TV_IP_ADDRESS>` | [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) | [Setup Guide](./skills/automation/cleanyourtv/README.md) |

---

## 🌐 Curated Resources & Inspiration Hubs (`resources/`)

Dedicated inspiration platforms, web galleries, and design hubs to browse for high-end UI concepts, prompts, and hosted media:

| Resource | Platform URL | Focus | Vault Path |
|---|---|---|---|
| [**MotionSites**](./resources/design-inspiration/motion-sites/) | [motionsites.ai](https://motionsites.ai/) | **Cinematic Animated Web Showcase**<br>Curated gallery of award-winning, motion-driven websites with 40+ prompt blueprints and 50+ hosted cinematic video backgrounds. | [Explore Vault](./resources/design-inspiration/motion-sites/README.md) |

---

## 📂 Repository Structure

```text
agent-arsenal/
├── README.md                           # Catalog index of all curated skills
├── .gitignore                          # Clean ignore rules
└── skills/
    ├── coding/                         # Senior engineering, clean code & workflow rules
    │   ├── caveman/                    # Terse mode, short commits & token savings (WHAT_THIS_DOES.txt)
    │   ├── ponytail/                   # Minimalist senior dev mode (WHAT_THIS_DOES.txt)
    │   ├── agent-skills/               # Addy Osmani's 25 production skills (WHAT_THIS_DOES.txt)
    │   └── vercel-suite/               # Vercel Labs React/Next.js engineering suite (WHAT_THIS_DOES.txt)
    │
    ├── gateways/                       # Multi-provider routing, proxy servers & token pools
    │   ├── omniroute/                  # 375+ providers & RTK compression (WHAT_THIS_DOES.txt)
    │   └── freellmapi/                 # 7.4B tokens/mo free gateway (WHAT_THIS_DOES.txt)
    │
    ├── video-media/                    # Video understanding & code-to-video rendering
    │   ├── watch/                      # Claude Video /watch (WHAT_THIS_DOES.txt)
    │   ├── hyperframes/                # HeyGen's HTML/CSS-to-video engine (WHAT_THIS_DOES.txt)
    │   └── brag/                       # Automated codebase launch video generator (WHAT_THIS_DOES.txt)
    │
    ├── design/                         # UI components, animations & design systems
    │   ├── img2threejs/                # Procedural image-to-3D Three.js generator (WHAT_THIS_DOES.txt)
    │   ├── ui-ux-pro-max/              # #1 Design intelligence & 7 sub-skills (WHAT_THIS_DOES.txt)
    │   ├── framer-motion/              # Spring physics & layoutId animation engine (WHAT_THIS_DOES.txt)
    │   ├── taste-skill/                # Anti-slop frontend art direction (WHAT_THIS_DOES.txt)
    │   ├── image-to-code-skill/        # Image-first visual implementation (WHAT_THIS_DOES.txt)
    │   ├── web-design-guidelines/      # Vercel Labs design audit & standards (WHAT_THIS_DOES.txt)
    │   ├── awesome-design/             # 84+ brand token systems (Stripe, Apple, Linear) (WHAT_THIS_DOES.txt)
    │   ├── 21st-dev/                   # 21st.dev Magic MCP (WHAT_THIS_DOES.txt)
    │   ├── screenshot-to-code/         # Visual screenshot-to-code replicator (WHAT_THIS_DOES.txt)
    │   └── uiverse/                    # 3,000+ pure CSS/Tailwind micro-components (WHAT_THIS_DOES.txt)
    │
    ├── browser-automation/             # Web automation, headless browsing & scraping
    │   ├── playwright-cli/             # Microsoft Playwright CLI & Skills (WHAT_THIS_DOES.txt)
    │   ├── playwright-mcp/             # Microsoft Playwright MCP (WHAT_THIS_DOES.txt)
    │   └── apify/                      # Apify MCP (WHAT_THIS_DOES.txt)
    │
    ├── memory/                         # Continuous cross-chat personal memory
    │   └── mem0/                       # Persistent agent memory layer (WHAT_THIS_DOES.txt)
    │
    └── automation/                     # IoT, hardware & device automation runbooks
        └── cleanyourtv/                # Android/Google TV Wi-Fi ADB debloater (WHAT_THIS_DOES.txt)
│
└── resources/                          # 🌐 Inspiration Hubs, Media Shelves & Web Galleries
    └── design-inspiration/
        └── motion-sites/               # motionsites.ai gallery, 40 prompts & video shelf (WHAT_THIS_DOES.txt)
```

---

## 🚀 How to Use Any Skill in a Project

Most skills provide either a universal rules file (`AGENTS.md`) or a specific agent configuration (`SKILL.md`):

1. **For Any Agent (Cursor, Antigravity, Windsurf, OpenCode):**
   Copy the `AGENTS.md` file directly into your target project's root folder:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/AmanJozf/agent-arsenal/main/skills/<category>/<skill-name>/AGENTS.md -o AGENTS.md
   ```

2. **For Claude Code / Copilot / Codex CLI:**
   Check each skill's dedicated `README.md` for native `/plugin` or marketplace installation commands.

---

## 📥 Adding New Skills to this Repo

Whenever a new skill or rule is discovered:
1. Place it into its logical category: `skills/<category>/<skill-name>/`
2. Extract the core instructions (`SKILL.md`, `AGENTS.md`, or prompt files).
3. Add a `WHAT_THIS_DOES.txt` quick-reference summary card.
4. Add a dedicated `README.md` with a 2-line "How to Install on Any Machine" guide.
5. Add the skill to the **Skills Catalog** table above.
6. Commit and push changes with a clean commit message.
