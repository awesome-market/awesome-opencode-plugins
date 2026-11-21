# Obsidiar**IA**

> *Obsidian + diary + **AI***: a concrete, **operational** operating system for your knowledge work — **capture once, the agents file** — not a generic "chat with your notes" wiki.

<sub>Unofficial, community-built template — not affiliated with or endorsed by Obsidian (Dynalist Inc.).</sub>

This is a ready-to-clone **Obsidian vault template** wired to AI coding agents (OpenCode, Claude Code, Kilo). It turns a pile of notes into a system that tracks **project progress**, drafts **deliverables**, runs **critical brainstorming**, processes your **inbox**, and never lets a **deadline or follow-up** slip — because an agent keeps the structure clean for you.

The thesis: most "LLM + notes" setups stop at retrieval ("ask your notes a question"). This one is **operational**. It is built around how a busy knowledge worker actually works — many parallel threads of work, a heavy meeting load, outputs to produce, follow-ups that must not slip — and it gives the AI a precise contract for where every piece of information lives. It fits a wide range of roles — developers and tech leads, IT and delivery managers, consultants, back-office and HR, researchers — anyone juggling many parallel commitments. For you, day-to-day use is deliberately dull: **drop everything into a single inbox and let the agent do the filing.**

It ships pre-filled with one illustrative example profile — *Daniel Lacemore*, a consultant — so you see a working system from minute one; it's only an example, not the intended audience. A one-command wizard (`/setup`) rewrites that example into *your* profile, whatever your role.

> **Note:** *Daniel Lacemore* is a fictional name (an anagram-style placeholder), used only as the template's example profile — it is not a real person.

---

## How it works — capture once, the agent files

The system optimizes for the one habit you can actually sustain: **capture everything in the Inbox, and let the agent do the organizing.** No tags to pick, no folder to choose, no deciding upfront which project a stray thought belongs to — that filing work is the agent's job, not yours.

**1. Capture.** A meeting note, a forwarded email, a half-formed idea → a new note in `01_Inbox/`. That single folder is the only entry point, and capturing is the only discipline the system asks of you.

> **Tip — make capture one keystroke.** In Obsidian, open **Settings → Files and links → Default location for new notes**, choose *In the folder specified below*, and set the folder to `01_Inbox`. Now `Cmd/Ctrl + N` always creates the new note straight in the Inbox — capture without ever thinking about where it goes.

**2. Route.** When you run `/obs.inbox` (or `/obs.eod`), the agent reads each capture, finds or creates the right **Activity**, and sends every piece of it to its one correct home:

| A captured… | …lands in |
|---|---|
| open question / blocker | the Activity's **Open Points** table |
| to-do | the Activity's **Tasks** (as a `#task`) |
| decision | the Activity's **Log** + the impacted deliverable |
| technical detail | a support note, or a client-facing deliverable |
| meeting | a concise minute in `05_Meetings/`, with actions extracted |

All of it obeys one rule — the **anti-scatter principle: a piece of information lives in exactly one place.**

**3. Read.** To get back up to speed on anything, open its **Activity** (the *Master note*): current state and pointers at the top, the detail one link away. You never go hunting across folders.

> Want a scratchpad the agent won't touch? Tag a note `ongoing` in the Inbox and it stays put — persistent working notes are never auto-filed.

---

## Why it's different

- **Activity-centric, not note-centric.** Work is organized around *Activities* (multi-day units of work). Each Activity is a *Master note*: a hub of state + pointers. Detail lives in linked child notes. One rule governs everything: **a piece of information lives in exactly one place** (the anti-scatter routing matrix).
- **Tool-agnostic by design.** The AI reads and writes plain markdown files. No lock-in to one assistant. The same vault works with OpenCode, Claude Code and Kilo, and stays fully compatible with native Obsidian features (Bases, Dataview, Tasks).
- **A small team of specialized agents**, not one do-everything bot (see below).
- **Single source of truth for AI config.** You edit one place (`.opencode/`) and a sync script regenerates the per-tool configs.
- **Light on purpose.** No taxonomy sprawl. The agents are told to keep the system simple.

---

## The agents

One primary orchestrator delegates to four specialists, plus a directly selectable brainstorming partner. The codenames are deliberate and memorable; here's what each one does:

| Codename | Role | When it runs |
|---|---|---|
| **Jarvis** | Primary orchestrator — runs the vault, the daily routines, and delegates | Always on; your main interlocutor |
| **Socrates** | Dialogic brainstorming partner (read-only, can't edit the vault) — directly selectable | To think an idea through: progressive questions, plain language, converges only when you ask |
| **Archie** | Solution architect / technical writer | Produce client-facing deliverables: proposals, solution designs, estimates |
| **Friday** | Presentation builder (HTML/CSS decks) | Turn a deliverable into a slide deck |
| **Melio** | Vault gardener | Improve structure, naming, templates, views — keep the system tidy |

The full prompts live in `.opencode/.prompts/`. Edit there, then re-sync (below).

---

## Folder structure

```
00_System/      Operating model, dashboard, templates, bases, views, AI config
01_Inbox/       Single raw-capture folder — everything enters here first
02_Daily/       One daily note per day (YYYY-MM-DD)
03_Projects/    One note per project (WBS-coded)
04_Activities/  Activities (Master notes); tasks live as #task checkboxes inside
05_Meetings/    Concise, extraction-friendly meeting notes
06_Notes/       Support notes (type: note) and deliverables (type: deliverable)
07_Accounts/    Client details
08_Attachments/ Files (incl. non-markdown deliverables)
09_People/      People profiles
90_Archive/     Inactive material
```

The complete property schema and conventions are in **`00_System/System Guide.md`** — the contract both you and the agents follow. The high-level rules the agents load on every session are in **`AGENTS.md`**.

---

## Daily workflow

In practice the loop is small and repeatable:

- **Morning — `/obs.morning`.** The agent reads yesterday's note, scans your ongoing Activities, surfaces open tasks and blockers, and proposes a Top-3 + focus for the day (it asks you to confirm).
- **Through the day — just capture.** Meeting notes, ideas, follow-ups → `Cmd/Ctrl + N` → Inbox, and keep moving. Don't stop to file. Need a structured minute on the spot? `/obs.meeting`. Want to think a decision through first? Talk to **Socrates** directly (read-only, dialogic brainstorming).
- **End of day — `/obs.eod`.** The agent empties the Inbox into the right Activities, checks off finished tasks, closes resolved open points, updates deliverables and projects, and writes the day's summary. The vault is clean again — and you filed nothing.
- **Weekly — `/obs.weekly`.** A retrospective over the week: stagnant open points, overdue tasks, project health, and the priorities for the week ahead.

When a real client output is due, **Archie** drafts the deliverable and **Friday** turns it into a slide deck; **Melio** keeps the vault's structure tidy over time.

The full command set:

| Command | What it does |
|---|---|
| `/obs.morning` | Build today's plan from your ongoing Activities, open tasks and blockers |
| `/obs.inbox` | Process and route raw captures into the right Activities (Activity-centric) |
| `/obs.eod` | End of day: update Activities/tasks, close open points, write the summary |
| `/obs.weekly` | Weekly review: stagnant open points, project health, next-week priorities |
| `/obs.meeting` | Create a structured meeting note and extract actions/decisions |
| `/obs.status` | Quick status overview centered on Activities |
| `/obs.new-project` | Scaffold a new project |
| `/playground` | Generate a self-contained interactive HTML tool |
| `/setup` | The customization wizard (run this first) |

---

## Quick start

1. **Clone** this repo and open the folder as a vault in **Obsidian**.
2. **Install the community plugins** it relies on: **Dataview**, **Tasks**, **Templater**, and enable core **Bases**. (Excalidraw optional, for diagrams.) Point Templater's template folder at `00_System/Templates`.
   - **Make capture one keystroke:** in **Settings → Files and links**, set **Default location for new notes** to *In the folder specified below* → `01_Inbox`. Now `Cmd/Ctrl + N` drops every new note straight into the Inbox.
3. **Open the folder with your AI agent** (OpenCode recommended; Claude Code or Kilo also work).
4. **Run the wizard:**
   ```
   /setup
   ```
   It asks for your name, role, language, domain and a few labels, then rewrites the vault to be yours. (Prefer the terminal? See `setup/README.md`.)
5. **Restart your AI tool** so the updated agents and commands load.
6. Start your day with `/obs.morning` or `/obs.inbox` if you just want to process the inbox notes.

> Node.js is required only for the two maintenance scripts (`setup/apply-profile.mjs` and `00_System/AI/sync-agents.mjs`). The vault itself is plain markdown.

---

## Customization

Everything user-specific is captured in **`setup/profile.yml`** (name, role, organization type, working language, domain one-liner, project-code label, vault path). The `/setup` wizard — or `node setup/apply-profile.mjs` — propagates those values across `AGENTS.md`, the System Guide, the agent prompts, the commands and the templates. Reset to the shipped example any time with `--defaults`. Details in **`setup/README.md`**.

To change agent behavior, edit the source under `.opencode/` and regenerate the per-tool configs:

```bash
node 00_System/AI/sync-agents.mjs   # rebuilds .kilo/, .claude/ and CLAUDE.md
```

The generated files (`.kilo/`, `.claude/`, `CLAUDE.md`) carry an `AUTO-GENERATED` header — don't edit them by hand.

---

## Plugins & integrations

- **Required Obsidian plugins:** Dataview, Tasks, Templater, Bases (core). Optional: Excalidraw.
- **MCP servers** (search, vendor docs, diagrams) are **not** versioned here: configure them at your tool's user scope. They often hold API keys and machine-specific paths. The agents degrade gracefully when an MCP is missing. See `00_System/System Guide.md §7` for the matrix and the secret-hygiene rule (use env-var interpolation, never cleartext keys).
- **Skills:** see **`SKILLS.md`** for the bundled and the optional external skills (with attribution).

---

## License & credits

- Code and configuration: **MIT** — see `LICENSE`.
- The optional external skills referenced by the agents belong to their respective authors — see `SKILLS.md`.
- Agent codenames are a playful nod to fictional assistants; the system itself is your own.
