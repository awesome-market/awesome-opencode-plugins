# ai-dev-setup

My working setup for coding and writing with AI agents in the terminal, built on [OpenCode](https://opencode.ai) (open source) and free models. It reflects how I like to work with an agent: evidence before conclusions, explicit approval before risky actions, minimal changes first, and a small fixed context.

> Documentation in English; the agent instructions are in Spanish because that is the language I work in.

## What's inside

| Path | What it does |
|---|---|
| `opencode/AGENTS.md` | Global rules for the agent (~500 tokens on purpose: it is sent with every message) |
| `opencode/opencode.json` | Default free model, permissions in "ask before" mode, MCP servers off by default, session sharing disabled, automatic pruning of old tool output |
| `opencode/agents/revisor.md` | Read-only reviewer subagent: it can analyze, it cannot edit |
| `opencode/agents/carrera.md` | Career agent for CVs, job postings and posts. It drafts and analyzes; it never applies, posts or sends anything |
| `opencode/commands/` | `/commit` (Conventional Commits, waits for OK), `/analisis` (review run as a subtask so the main session stays small), `/analizar-oferta`, `/adaptar-cv`, `/revisar-post` |
| `opencode/skills/` | Reusable skills: plain-language handoff messages, saving lessons as guides, module design, merge conflicts, writing for agents, stress-testing a plan |
| `opencode/rules/` | Code rules: write a failing test before fixing a bug; tidy in a separate commit before changing behavior |
| `opencode/bin/` | Launcher that runs the Chrome DevTools MCP with an explicit Node version |
| `opencode/tui.json` | Sound and notification when the agent finishes or needs permission |

## Design choices

- **Small fixed context.** Rules, MCP tool lists and memory indexes travel with every message. The global rules are kept short, MCP servers are off by default and switched on with `/mcps` when needed, and long reviews run as subtasks.
- **Ask before acting.** Shell commands are `ask` by default; only read-only git and file commands are allowed. Deleting uses `trash`, never `rm`.
- **Privacy-aware model choice.** The default free model is one whose provider states a zero-retention policy. Some free models may use prompts for training; check your provider's terms.
- **No cost by accident.** Paid usage is blocked at the account level (zero balance, no auto-recharge, zero monthly budget), not by hiding models, so new free models still show up.
- **Memory without lock-in.** OpenCode has no built-in long-term memory, so it is emulated: one fact per Markdown file, an index under 21 KB loaded through `instructions`, and a rule that nothing is saved without explicit approval. The memory files themselves are personal and not included here.

## Install

```bash
brew install anomalyco/tap/opencode
cp -R opencode/* ~/.config/opencode/
echo 'export OPENCODE_DISABLE_CLAUDE_CODE=1' >> ~/.zshrc   # use only ~/.config/opencode
npm i -g chrome-devtools-mcp                                # optional, for browser tasks
mkdir -p ~/.config/opencode/memoria && touch ~/.config/opencode/memoria/MEMORY.md
```

Then open `opencode`, run `/connect` to add a provider and `/models` to pick a model. For the Chrome MCP, set `NODE_DIR` in `opencode/bin/chrome-devtools-mcp.sh` to a Node ≥ 22.12 and enable `chrome://inspect/#remote-debugging`.

## License

MIT
