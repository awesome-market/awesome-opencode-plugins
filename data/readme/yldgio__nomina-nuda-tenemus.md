# Social Games - Vibe Coding Lab

A hands-on workshop for learning **agentic coding** with AI assistants. Build and customize multiplayer party games while mastering context engineering, background agents, and design-first development.

## What is Vibe Coding?

Vibe coding is AI-assisted development where you guide intelligent agents through natural language, iterate on plans before implementation, and leverage parallel exploration to scale your creativity. This repo provides a real codebase to practice these techniques.

## Workshop Guide

**Start here:** Open [.lab/GUIDE.md](.lab/GUIDE.md) for the full workshop walkthrough.

### Learning Objectives

1. **Context Engineering** - Onboard AI to your codebase with instructions and prompts
2. **Agentic Primitives** - Use plan mode, background agents, and cloud agents effectively
3. **Scaled Exploration** - Run parallel agents to explore design variations
4. **Design-First Vibing** - Build beautiful, distinctive frontends with AI collaboration

## Quick Start

### Prerequisites

- [VS Code](https://code.visualstudio.com/) v1.107+
- [Node.js](https://nodejs.org/) v18+
- GitHub account with Copilot access

### Setup

1. **Use this template** → Create your own repository (make it Public)

2. **Enable GitHub Pages**: Settings → Pages → Deploy from GitHub Actions

3. **Clone and open in VS Code**:
   ```bash
   git clone https://github.com/<your-username>/<your-repo>
   code <your-repo>
   ```

4. **Run the setup prompt**: Open Chat and run `/setup`

5. **Start developing**: `npm run dev` → Open `http://localhost:5173`

## Games Included

| Game | Description |
|------|-------------|
| **Word Chain** | Chain words by their last letter. 3 lives, 15 seconds per turn. |
| **Quick Draw** | Draw prompts on canvas while others guess. 60 seconds per round. |
| **Emoji Charades** | Describe movies/songs/phrases using only emojis. 45 seconds per round. |

## Workshop Tasks

### 1. Context Engineering
- Run `/setup` prompt for AI-guided installation
- Generate workspace instructions with `Chat: Generate Workspace Instructions File`
- Explore background agents for parallel tasks

### 2. Design-First Vibing
- Use **Plan mode** for redesigns: *"Let's do a full redesign. Make it Cyberpunk Neon..."*
- Run `/cloud-explore` for parallel design explorations
- Keep instructions updated with design changes

### Design Ideas to Try
Minimalist Mono • Retro Terminal Green • Vaporwave Sunset • Cyberpunk Neon • Brutalist Blocks • Soft Pastel Clouds • Dark Mode Noir • Pixel Arcade Style • Gradient Glass UI • Space Galaxy Glow

## Tech Stack

- **React 19** + **TypeScript** + **Vite 6**
- **Tailwind CSS v4** - CSS-first configuration
- **Zustand** - State management
- **Framer Motion** - Animations
- **React Router v7** - Navigation

## Project Structure

```
├── .github/
│   ├── instructions/    # AI agent instructions (Tailwind v4, design)
│   ├── prompts/         # Reusable prompts (/setup, /cloud-explore)
│   └── workflows/       # GitHub Actions (auto-deploy to Pages)
├── .lab/
│   └── GUIDE.md         # Workshop guide (start here!)
├── src/
│   ├── components/      # UI and game components
│   ├── games/           # Game implementations
│   ├── stores/          # Zustand state
│   └── index.css        # Tailwind theme
├── AGENTS.md            # Coding agent guidelines
└── README.md            # You are here
```

## Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server with hot reload |
| `npm run build` | Type-check and build for production |
| `npm run lint` | Run ESLint |
| `npm run preview` | Preview production build |

## Resources

- [Awesome Copilot](https://github.com/github/awesome-copilot) - More customizations
- [Tailwind CSS v4 Docs](https://tailwindcss.com/docs) - Styling reference
- [Framer Motion](https://www.framer.com/motion/) - Animation library

## License

MIT
