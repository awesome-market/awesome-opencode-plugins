<p align="center">
  <img src="src/packages/ui/src/assets/brand/neuratal-wordmark.png" alt="Neuratal" width="480" />
</p>

<p align="center">
  <img src="src/packages/ui/src/assets/brand/nura-avatar.png" alt="Nura — the Neuratal mascot" width="96" />
</p>

# Neuratal Code

> **The autonomous desktop AI software engineering agent.**
> OpenCode's engine, Neuratal's chrome, and a mascot named Nura — watching your build logs so you don't have to.

**Status:** public preview. It works, it has taste, and it will occasionally out-argue you — which is sort of the point.

Neuratal Code is a free, open-source, desktop-native AI coding agent: it plans, writes, reviews, debugs and ships — directly on your machine, with your tools, in your repo, with your blessing (and occasional permissions). Built on the excellent [opencode](https://github.com/anomalyco/opencode) core, then re-skinned, re-wired and re-imagined by Neuratal.

---

## About Neuratal

**Neuratal is an independent AI research organization founded by Rüzgar Erdem. Built from the ground up with limited resources and deep engineering discipline — focused on creating genuinely capable, reasoning-native AI models.**

Neuratal was built the slow, deliberate way: no launch-week war room, no hundred-person foundation on day one, no investor deck that promises artificial general insight by quarter four. Just one stubborn founder, a small pile of compute, a mountain of engineering discipline, and a conviction that "reasoning-native" should describe how a model actually thinks, not how the marketing page photographs.

**What we care about:**

- 🧠 **Reasoning over autocomplete.** Models that think before they type. Tokens are cheap; wrong diffs are not.
- 🛠️ **Tools that respect the workshop.** The agent edits your repo, runs your commands, and asks before doing anything you would regret at 3 AM.
- 🎨 **Craft, end to end.** Because if your coding tool looks like a tax form, you will feel like one too.

**The Neuratal model family:**

| Model | Tagline | Intended for |
| --- | --- | --- |
| 🍂 **Akisame** (`1x`) | Fast coding | Refactors, quick edits, everyday logic work |
| ❄️ **Kazahana** (`3x`) | Balanced pro | Complex architecture, large features, careful refactors |
| 🍃 **Hatsukaze** (`8x`) | Deep architecture | Massive context (1M tokens), heavyweight design & review |

The Neuratal family is served through a **Neuratal Host** — an OpenAI-compatible endpoint. You can bring your own (see [Running the models](#running-the-models)), or just use the provider you already love; Neuratal Code ships with first-class support for OpenAI, Anthropic, Google, DeepSeek, OpenRouter, Ollama, LM Studio and friends.

---

## What's inside

- **Neuratal Aurora** — a true-black OLED design system: violet (`#7C5CFF`), cyan (`#22D3EE`) and fuchsia (`#E879F9`) on layered deep-space surfaces, typeset in Inter and JetBrains Mono. Easy on the eyes at line 400 of a debugging session.
- **Nura** — the mascot. Floats, glows, blinks. Shows up in the new-session welcome, the command deck, empty states and your first assistant reply. `prefers-reduced-motion` is respected, because restraint is also a personality.
- **Five agent profiles, one roof:** 🛠️ **Build** (autonomous dev), 📐 **Plan** (read-only strategy), 🔍 **Code Review** (diffs & standards), 🐞 **Debug** (stack-trace archaeology), 🔬 **Research** (docs & web).
- **Multi-provider model access** with capability tags, live status and per-provider credential hygiene.
- **Audio feedback engine** — subtle Web Audio cues for done / error / send / first-token / warning. Off by default. It can stay off; it judges no one. (But it *is* satisfying.)
- **Safe-by-default** — destructive shell commands need explicit confirmation, sensitive files (`.env`, `*.key`, SSH keys) are protected, and the workspace boundary is enforced.
- **Neuratal Studio** — a command-deck home screen with quick-start modes (Build, Plan, Review, Extract, Research), a mission bar, and a composer that actually understands `/`, `@` and `$`.

---

## Quick start

### Desktop (Electron)

```bash
git clone https://github.com/Neuratal/neuratal-code.git
cd neuratal-code/src
bun install
bun run dev:desktop
```

### Web client

```bash
cd neuratal-code/src/packages/app
bun run dev
```

### CLI

```bash
cd neuratal-code/src
bun run dev            # opencode-compatible interactive TUI/CLI
```

> Requires [Bun](https://bun.sh) 1.4+ and a recent Node 22 runtime for packaging.

---

## Running the models

Out of the box, Neuratal Code works with any provider you configure. The bundled **Neuratal** provider speaks to a Neuratal Host (an OpenAI-compatible `/v1/chat/completions` endpoint). Point it at your own host:

```bash
export NEURATAL_HOST_URL="https://your-host.example.com/v1"
export NEURATAL_API_KEY="..."
```

Without a Host, the bundled Neuratal models simply don't answer — the rest of the app is fully usable. Bring your own keys for OpenAI, Anthropic, Google or anything else, and you'll never need a Host at all.

---

## Build & package (Linux)

```bash
cd src
bun run --cwd packages/app build        # web frontend
bunx electron-vite build                # desktop main+renderer  (from packages/desktop)
bunx electron-builder --linux --x64 --dir --config electron-builder.config.ts
```

Artifacts land in `src/packages/desktop/dist/`. Signing, notarization and auto-update feeds are deliberately **not** wired in this open-source tree — your build, your certificates, your call.

---

## Project layout

```
neuratal-code/
├── README.md
├── CHANGELOG.md           # public changelog (Turkish, because it was born that way)
├── UPSTREAM.md            # how Neuratal Code diverges from opencode
├── THIRD_PARTY_NOTICES.md # licenses of the things we build on
└── src/                   # the monorepo (Bun workspaces)
    ├── packages/
    │   ├── ai/            # provider drivers (Neuratal + everyone else)
    │   ├── core/          # agent orchestration, tools, sessions
    │   ├── app/           # SolidJS web/desktop UI
    │   ├── desktop/       # Electron shell, packaging
    │   └── ui/            # Neuratal Aurora design system
    └── ...
```

---

## Open source & credits

Neuratal Code stands on the shoulders of people who ship radically open software:

- **[opencode](https://github.com/anomalyco/opencode)** by Anomaly Innovations — the core engine, the CLI, the TUI, the plugin system, and a whole lot of excellent engineering you can read right here in `src/`. MIT licensed. Thank you.
- Every other library and tool listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

See [UPSTREAM.md](UPSTREAM.md) for how this fork diverges and how upstream changes flow back in.

---

## About the founder

**Rüzgar Erdem** — founder & sole full-time human at Neuratal. Independent AI research, desktop tooling, and reasoning-native model work, built the way small studios build big things: carefully, and with a grudge against mediocrity. Find more at [neuratal.com](https://neuratal.com).

---

## License

MIT — see [src/LICENSE](src/LICENSE).

Neuratal Code is a derivative work of opencode (MIT License, Copyright 2024-2026 Anomaly Innovations, Inc. and OpenCode Contributors). Neuratal-specific modifications are Copyright 2026 Rüzgar Erdem / Neuratal.
