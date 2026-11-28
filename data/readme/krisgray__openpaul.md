<div align="center">

# OpenPAUL

**Plan-Apply-Unify Loop** — Structured AI-assisted development for OpenCode.

[![Coverage](https://codecov.io/gh/KrisGray/openpaul/branch/main/graph/badge.svg)](https://codecov.io/gh/KrisGray/openpaul)

[![npm version](https://img.shields.io/npm/v/openpaul?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/openpaul)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/KrisGray/openpaul?style=for-the-badge&logo=github&color=181717)](https://github.com/KrisGray/openpaul)
[![Docs](https://img.shields.io/badge/docs-live-brightgreen?style=for-the-badge)](https://krisgray.github.io/openpaul/)

<br>

```bash
npx openpaul
```

**Works on Mac, Windows, and Linux.**

<br>

_"Quality over speed-for-speed's-sake. In-session context over subagent sprawl."_

<br>

[📖 Documentation](https://krisgray.github.io/openpaul/) · [Why OpenPAUL](#why-openpaul) · [Getting Started](#getting-started) · [The Loop](#the-loop) · [Commands](#commands)

</div>

---

## Why OpenPAUL

OpenPAUL is an OpenCode adaptation of the Plan-Apply-Unify Loop project, originally created by Chris Kahler for Claude Code.

I build with Claude Code every day. It's incredibly powerful — when you give it the right context.

The problem? **Context rot.** As your session fills up, quality degrades. Subagents spawn with fresh context but return ~70% quality work that needs cleanup. Plans get created but never closed. State drifts. You end up debugging AI output instead of shipping features.

OpenPAUL fixes this with three principles:

1. **Loop integrity** — Every plan closes with UNIFY. No orphan plans. UNIFY reconciles what was planned vs what happened, updates state, logs decisions. This is the heartbeat.

2. **In-session context** — Subagents are expensive and produce lower quality for implementation work. OpenPAUL keeps development in-session with properly managed context. Subagents are reserved for discovery and research — their job IS to gather context.

3. **Acceptance-driven development** — Acceptance criteria are first-class citizens, not afterthoughts. Define done before starting. Every task references its AC. BDD format: `Given [precondition] / When [action] / Then [outcome]`.

The complexity is in the system, not your workflow. Behind the scenes: structured state management, XML task formatting, loop enforcement. What you see: a few commands that keep you on track.

---

## Who This Is For

**AI-assisted developers** who want structure without bureaucracy.

You describe what you want, OpenCode builds it, and OpenPAUL ensures:

- Plans have clear acceptance criteria
- Execution stays bounded
- Every unit of work gets closed properly
- State persists across sessions
- Decisions are logged for future reference

No sprint ceremonies. No story points. No enterprise theater. Just a system that keeps AI-assisted development reliable.

---

## Getting Started

### Initialize OpenPAUL in your project

```bash
npx openpaul
```

This creates two things:
- `.openpaul/state.json` — project registry (name, version, timestamps)
- `.opencode/` — OpenCode configuration and preset files

Then run `/openpaul:init` inside OpenCode to initialize loop state and create `.openpaul/model-config.json` and `.openpaul/state-phase-1.json`.

#### CLI Options

| Option | Description |
|--------|-------------|
| `-n, --name <name>` | Project name (defaults to directory name) |
| `-p, --path <path>` | Target directory (default: ".") |
| `--preset <preset>` | Template preset: `minimal` or `full` |
| `-f, --force` | Skip prompts and overwrite existing files |
| `-i, --interactive` | Force interactive mode |
| `-v, --verbose` | Enable verbose output |

#### Examples

```bash
npx openpaul                           # Interactive mode
npx openpaul --name my-project         # Skip name prompt
npx openpaul --path ./app              # Target directory
npx openpaul -n my-project -p ./app    # Combined options
npx openpaul --preset minimal          # Minimal template
npx openpaul --preset full             # Full template with examples
```

### Install as OpenCode Plugin

`npx openpaul` automatically adds `"plugin": ["openpaul"]` to `opencode.json`. Just restart OpenCode after scaffolding to load the plugin. `/openpaul:*` commands will appear in the TUI command list.

If you need to add it manually, edit `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "openpaul"
  ]
}
```

### Verify

- **CLI**: Run `npx openpaul --version`
- **Plugin**: Run `/openpaul:help` inside OpenCode (it should autocomplete in the command list)

### Local development (from source)

If you are iterating on OpenPAUL locally, load it as a local plugin file (OpenCode only auto-loads local plugins from the plugins directory):

```
.opencode/plugins/openpaul.ts
```

```ts
import plugin from "/absolute/path/to/openpaul/dist/index.js"
export default plugin
```

---

## Quick Start with OpenCARL (Recommended)

For the best experience, use OpenPAUL with **OpenCARL** ([github.com/KrisGray/opencarl](https://github.com/KrisGray/opencarl)) — a dynamic rule injection system that enforces OpenPAUL workflow discipline automatically.

### Install Both

```bash
# 1. Initialize OpenPAUL
npx openpaul

# 2. Initialize OpenCARL
npx opencarl --local
```

OpenCARL auto-loads OpenPAUL rules when it detects `.openpaul/` directory.

### Your First Loop (5 minutes)

```bash
# Initialize OpenPAUL in your project
npx openpaul
```

```
YOU: I want to add a dark mode toggle to my React app

# OpenCARL auto-loads OpenPAUL rules when it detects .openpaul/

YOU: /openpaul:plan
OpenPAUL: Describe what you're building...

YOU: Dark mode toggle that:
  - Remembers preference in localStorage
  - Defaults to system preference
  - Toggles without page reload

OpenPAUL: Created PLAN.json with:
  ✓ Objective: Add persistent dark mode toggle
  ✓ AC-1: Given user visits, When no preference, Then use system
  ✓ AC-2: Given user clicks toggle, When in light, Then switch to dark
  ✓ Task 1: Create ThemeContext
  ✓ Task 2: Add CSS variables
  ✓ Task 3: Create ThemeToggle component
  ✓ Boundary: DO NOT change auth components

YOU: Looks good. /openpaul:apply

OpenPAUL: 
  ✓ Task 1: Created ThemeContext (verified: imports work)
  ✓ Task 2: Added CSS variables (verified: themes render)
  ✓ Task 3: Created ThemeToggle (verified: toggle works)

YOU: /openpaul:unify

OpenPAUL: 
  ✓ Created SUMMARY.json
  ✓ Updated loop state
  ✓ Recorded 3 decisions

Done! Loop complete. State preserved for next session.
```

### Why OpenCARL + OpenPAUL?

| Without OpenCARL | With OpenCARL |
|------------------|---------------|
| Manual workflow discipline | Auto-enforced loop rules |
| Easy to skip UNIFY | Blocked from skipping |
| Context bloat | Rules load on-demand |
| Inconsistent quality | Consistent enforcement |

---

## Quick Start

### The Core Loop in Action

Here's a complete workflow example showing OpenPAUL in action:

```
┌─────────────────────────────────────────────────────────────────┐
│  YOU: I need to add user authentication to my app              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Initialize OpenPAUL                                   │
│                                                                 │
│  npx openpaul                                                   │
│                                                                 │
│  Creates: .openpaul/state.json (project registry) and          │
│  opencode.json (OpenCode config). Then run /openpaul:init in     │
│  OpenCode to create model-config.json and state-phase-1.json   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Plan Your Work                                        │
│                                                                 │
│  /openpaul:plan                                                 │
│                                                                 │
│  OpenPAUL prompts you to describe what you want to build,      │
│  then generates a structured PLAN.json with:                    │
│  - Objective (what & why)                                       │
│  - Acceptance Criteria (Given/When/Then)                        │
│  - Tasks with files, actions, verification steps                │
│  - Boundaries (what NOT to change)                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Review & Approve                                       │
│                                                                 │
│  YOU: The plan looks good, let's do it                         │
│                                                                 │
│  (Or: "Actually, I also need password reset" → plan updated)   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Execute the Plan                                       │
│                                                                 │
│  /openpaul:apply                                                │
│                                                                 │
│  Tasks execute sequentially:                                    │
│  ✓ Task 1: Create User model (verified: tests pass)            │
│  ✓ Task 2: Add login endpoint (verified: curl returns 200)     │
│  ✓ Task 3: Create login UI (verified: renders correctly)       │
│  ⏸ Task 4: Checkpoint — Verify login flow manually?            │
│                                                                 │
│  YOU: approved                                                   │
│                                                                 │
│  ✓ Task 5: Add session management                               │
│  ✓ All tasks complete                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Close the Loop (REQUIRED!)                            │
│                                                                 │
│  /openpaul:unify                                                │
│                                                                 │
│  Writes .openpaul/phases/{N}-{plan}-SUMMARY.json with:         │
│  - Task completion status (completed/skipped/failed)            │
│  - Plan vs actual comparison                                    │
│  - Criteria results                                             │
│                                                                 │
│  Advances state-phase-N.json to UNIFY, then creates            │
│  next phase state as UNIFY. Updates loop state (STATE.md if   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: Continue Development                                   │
│                                                                 │
│  /openpaul:progress                                             │
│                                                                 │
│  Shows: "Phase 1 complete. Next: Phase 2 - User Profile"       │
│  Suggests: ONE next action                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Real-World Example: Adding a Feature

```
YOU: /openpaul:plan

OpenPAUL: What would you like to build?

YOU: I need to add a dark mode toggle to my React app. It should:
- Remember the user's preference in localStorage
- Default to system preference on first visit
- Toggle without page reload

OpenPAUL: [Creates PLAN.json]

## Plan: Dark Mode Toggle

### Objective
Add a persistent dark mode toggle with system preference detection

### Acceptance Criteria
- **AC-1**: Given user visits app, When no preference stored, Then use system preference
- **AC-2**: Given user clicks toggle, When in light mode, Then switch to dark and save
- **AC-3**: Given user returns, When preference stored, Then apply saved preference

### Tasks
1. Create ThemeContext with useLocalStorage hook
2. Add CSS variables for dark/light themes
3. Create ThemeToggle component
4. Integrate into App.tsx

### Boundaries
- DO NOT change: auth-related components, API routes

YOU: Looks good. /openpaul:apply

OpenPAUL: [Executes tasks one by one with verification...]

YOU: /openpaul:unify

OpenPAUL: [Creates SUMMARY.json, updates loop state]

Done. Loop complete.
```

### Session Continuity

Resume work after a break:

```
[New session]

YOU: /openpaul:resume

OpenPAUL:
## Session Restored

**Last Session:** 2024-01-15
**Stopped at:** Phase 2, Plan 3 - User Profile
**Status:** 2/4 tasks complete

**What was built:**
- Profile display component
- Edit profile form

**What's next:**
Task 3: Add avatar upload
  File: src/components/AvatarUpload.tsx
  Action: Create component with drag-drop and crop preview

**Suggested command:** /openpaul:apply --phase 2 --plan 03
```

---

## Using OpenPAUL with OpenCARL

**OpenCARL** ([github.com/KrisGray/opencarl](https://github.com/KrisGray/opencarl)) is a dynamic rule injection system that loads rules based on context. Together, they create a powerful AI-assisted development experience.

### Why Use Both?

| OpenPAUL                                   | OpenCARL                     |
| ------------------------------------------ | ---------------------------- |
| Structured workflow (PLAN → APPLY → UNIFY) | Dynamic rule injection       |
| Guides planning & execution                | Loads rules based on context |
| Ensures loop closure                       | Keeps context lean           |
| State persistence                          | Preferences persistence      |

**The synergy:** OpenCARL loads OpenPAUL-specific rules when you're working in an OpenPAUL project, enforcing workflow discipline without bloating every session.

### Installation

```bash
# Initialize OpenPAUL
npx openpaul

# Initialize OpenCARL (local or global)
npx opencarl --local   # Current project only
npx opencarl --global  # All projects
```

### Combined Workflow Example

```
# 1. Initialize OpenPAUL
npx openpaul

# 2. OpenCARL detects .openpaul/ directory
#    → Automatically loads OpenPAUL-specific rules:
#    - "Loop enforcement (PLAN → APPLY → UNIFY)"
#    - "Boundary protection for DO NOT CHANGE sections"
#    - "Verification required for every task"

# 3. Plan your work
/openpaul:plan

# OpenCARL injects planning rules:
# - "Define acceptance criteria before tasks"
# - "Every task needs files, action, verify, done"
# - "Set boundaries — what NOT to change"

# 4. Execute the plan
/openpaul:apply

# OpenCARL injects execution rules:
# - "Run tests after implementation changes"
# - "Verify each task before moving on"
# - "Log deviations from plan"

# 5. Close the loop (required!)
/openpaul:unify

# OpenCARL injects closure rules:
# - "Create SUMMARY.json documenting what was built"
# - "Compare plan vs actual"
# - "Record decisions for future sessions"
```

### Real-World Scenario: Feature Development with Both

```
YOU: /openpaul:plan

OpenPAUL: Creates plan structure...
OpenCARL: [Injects OpenPAUL + Development rules]
  ✓ DEVELOPMENT_RULE_0: Code over explanation - show, don't tell
  ✓ DEVELOPMENT_RULE_1: Prefer editing existing files over creating new
  ✓ OPENPAUL_RULE_0: Loop enforcement - no skipping UNIFY
  ✓ OPENPAUL_RULE_1: Every task needs verification

YOU: [Describe the feature you want]

OpenPAUL: Generates PLAN.json with:
  - Objective
  - Acceptance Criteria (Given/When/Then)
  - Tasks with verification steps
  - Boundaries

YOU: /openpaul:apply

OpenPAUL: Executes tasks sequentially...
OpenCARL: [Injects execution rules + context tracking]
  ✓ Running tests after changes
  ✓ Verifying each task
  ✓ Logging deviations

[... work happens ...]

OpenPAUL: Task complete. Checkpoint: Run tests?
YOU: yes

OpenPAUL: Tests pass. Next task...
OpenCARL: [Context depleting → Injects fresh session rules]

[... more work ...]

YOU: /openpaul:unify

OpenPAUL: Creates SUMMARY.json, updates loop state
OpenCARL: [Injects closure rules]
  ✓ Document what was built
  ✓ Compare plan vs actual
  ✓ Record decisions

Done. Loop complete. State preserved for next session.
```

### OpenPAUL-Specific Rules That OpenCARL Enforces

When OpenCARL detects you're working in an OpenPAUL project:

1. **Loop Enforcement** — No skipping UNIFY. Every plan needs closure.
2. **Boundary Protection** — `DO NOT CHANGE` sections in plans are sacred.
3. **AC-First Development** — Acceptance criteria defined before tasks.
4. **Verification Requirements** — Every task needs a verify step.
5. **State Consistency** — Loop state JSON reflects reality after each phase (STATE.md if present).

These rules load automatically when you're in `.openpaul/` context and disappear when you're not.

---

## Migration from PAUL

If you have an existing project using `.paul/` directory:

1. Rename `.paul/` to `.openpaul/`
2. Update any hardcoded paths in your workflow

OpenPAUL will automatically detect and use `.openpaul/` for new files while still reading from `.paul/` for backward compatibility.

---

## The Loop

Every unit of work follows this cycle:

```
┌─────────────────────────────────────┐
│  PLAN ──▶ APPLY ──▶ UNIFY          │
│                                     │
│  Define    Execute    Reconcile     │
│  work      tasks      & close       │
└─────────────────────────────────────┘
```

### PLAN

Create an executable plan with:

- **Objective** — What you're building and why
- **Acceptance Criteria** — Given/When/Then definitions of done
- **Tasks** — Specific actions with files, verification, done criteria
- **Boundaries** — What NOT to change

### APPLY

Execute the approved plan:

- Tasks run sequentially
- Each task has verification
- Checkpoints pause for human input when needed
- Deviations are logged

### UNIFY

Close the loop (required!):

- Write `{N}-{plan}-SUMMARY.json` with task results and criteria
- Compare plan vs actual
- Advance loop state to ready for next PLAN
- Update loop state (STATE.md if present)

**Never skip UNIFY.** Every plan needs closure. This is what separates structured development from chaos.

---

## Commands

OpenPAUL provides 16 commands organized by purpose. The plugin registers them as OpenCode slash commands, so `/openpaul:*` appears in the TUI command list. Run `/openpaul:help` for the complete reference.

### Core Loop

| Command                  | What it does                                     |
| ------------------------ | ------------------------------------------------ |
| `npx openpaul`           | Initialize OpenPAUL in a project (CLI)           |
| `/openpaul:plan`        | Create an executable plan (TDD wizard)            |
| `/openpaul:apply --phase N --plan NN` | Execute an approved plan                         |
| `/openpaul:unify --phase N --plan NN` | Reconcile and close the loop                     |
| `/openpaul:help`         | Show command reference                           |

### Session

| Command                        | What it does                     |
| ------------------------------ | -------------------------------- |
| `/openpaul:pause`              | Create handoff for session break |
| `/openpaul:resume`             | Restore context and continue     |
| `/openpaul:progress`           | Smart status + ONE next action   |
| `/openpaul:handoff`            | Generate comprehensive handoff   |

### Milestone

| Command                        | What it does                      |
| ------------------------------ | --------------------------------- |
| `/openpaul:milestone <name>`   | Create new milestone              |
| `/openpaul:complete-milestone` | Archive and tag milestone         |

### Specialized

| Command                  | What it does                  |
| ------------------------ | ----------------------------- |
| `/openpaul:flows`        | Configure skill requirements  |
| `/openpaul:config`       | View/modify OpenPAUL settings |
| `/openpaul:map-codebase` | Generate codebase overview    |

### Quality

| Command              | What it does                    |
| -------------------- | ------------------------------- |
| `/openpaul:verify`   | Guide manual acceptance testing |
| `/openpaul:plan-fix` | Plan fixes for UAT issues       |

---

## How It Works

### Project Structure

After `npx openpaul` + `/openpaul:init`:

```
.openpaul/
├── state.json             # Project registry (npx openpaul)
├── model-config.json      # Model configuration (/openpaul:init)
├── state-phase-N.json     # Loop state per phase (/openpaul:init)
├── config.md              # Optional integrations
├── SPECIAL-FLOWS.md       # Optional skill requirements
├── HANDOFF.md             # Session handoff (/openpaul:pause)
└── phases/
    ├── 1-01-PLAN.json     # Plan (/openpaul:plan)
    ├── 1-01-PLAN.md       # Plan summary (/openpaul:plan)
    └── 1-01-SUMMARY.json  # Summary (/openpaul:unify)
opencode.json              # OpenCode config (npx openpaul)
.opencode/
└── (preset files)         # Commands, rules, agents
```

### State Management

Machine-readable loop state lives in **`state-phase-N.json`** (one per phase), tracking the current loop position (PLAN/APPLY/UNIFY), active plan ID, and timestamps.

If you maintain a human-readable **`STATE.md`**, OpenPAUL will update it when present:

- Current phase and plan
- Loop position (PLAN/APPLY/UNIFY markers)
- Session continuity (where you stopped, what's next)
- Accumulated decisions
- Blockers and deferred issues

When you resume work, `/openpaul:resume` loads your saved session from `.openpaul/SESSIONS/` and `HANDOFF.md`, then suggests exactly ONE next action. No decision fatigue.

### Plan Structure

Plans are created via `/openpaul:plan` and stored as JSON in `.openpaul/phases/`.

In the OpenCode TUI, use `/openpaul:plan` with no flags to run the TDD wizard. It prompts step-by-step for phase, plan ID, criteria, boundaries, and tasks.

Stored at `.openpaul/phases/1-01-PLAN.json` and `.openpaul/phases/1-01-PLAN.md`. Every task has: `files`, `action`, `verify`, `done`. If you can't specify all four, the task is too vague.

### OpenCARL Integration

OpenPAUL has a companion: **[OpenCARL](https://github.com/KrisGray/opencarl)** (Context Augmentation & Reinforcement Layer).

OpenCARL is a dynamic rule injection system. Instead of bloating your context with static prompts, OpenCARL loads rules just-in-time based on what you're doing:

| Trigger                           | Rules Loaded              |
| --------------------------------- | ------------------------- |
| Working in `.openpaul/` directory | OpenPAUL domain activates |
| Writing code                      | DEVELOPMENT rules load    |
| Managing projects                 | PROJECTS rules load       |

**OpenPAUL-specific rules OpenCARL enforces:**

- Loop enforcement (PLAN → APPLY → UNIFY — no shortcuts)
- Boundary protection (DO NOT CHANGE sections are real)
- State consistency checks at phase transitions
- Verification requirements for every task
- Skill blocking (required skills must load before APPLY)

The OpenPAUL domain contains 14 rules that govern structured AI development. They load when you're in an OpenPAUL project, disappear when you're not. Your context stays lean.

**Without OpenCARL:** You'd need massive static prompts in every session.
**With OpenCARL:** Rules activate when relevant, disappear when not.

---

## Philosophy

### Acceptance-Driven Development (A.D.D.)

Acceptance criteria aren't afterthoughts — they're the foundation:

1. **AC defined before tasks** — Know what "done" means
2. **Tasks reference AC** — Every task links to AC-1, AC-2, etc.
3. **Verification required** — Every task needs a verify step
4. **BDD format** — Given/When/Then for testability

### In-Session Context

Why OpenPAUL minimizes subagents for development work:

| Issue             | Impact                                |
| ----------------- | ------------------------------------- |
| Launch cost       | 2,000-3,000 tokens to spawn           |
| Context gathering | Starts fresh, researches from scratch |
| Resynthesis       | Results must be integrated back       |
| Quality gap       | ~70% compared to in-session work      |
| Rework            | Subagent output often needs cleanup   |

**When OpenPAUL does use subagents:**

- **Discovery/exploration** — Codebase mapping, parallel exploration
- **Research** — Web searches, documentation gathering

For implementation, OpenPAUL keeps everything in-session with proper context management.

### Loop Integrity

The loop isn't optional:

```
PLAN ──▶ APPLY ──▶ UNIFY
  ✓        ✓        ✓     [Loop complete]
```

- **No orphan plans** — Every PLAN gets a SUMMARY
- **State reconciliation** — UNIFY catches drift
- **Decision logging** — Choices are recorded for future sessions

---

## Configuration

### Optional Integrations

OpenPAUL supports modular integrations configured in `.openpaul/config.md`:

| Integration | Purpose                         |
| ----------- | ------------------------------- |
| SonarQube   | Code quality metrics and issues |
| _Future_    | Linting, CI/CD, test runners    |

### SPECIAL-FLOWS

For projects with specialized requirements, `.openpaul/SPECIAL-FLOWS.md` defines skills that must be loaded before execution:

```markdown
## Required Skills

| Skill            | Work Type     | Priority |
| ---------------- | ------------- | -------- |
| /frontend-design | UI components | required |
| /revops-expert   | Landing pages | required |
```

APPLY blocks until required skills are confirmed loaded.

---

## Troubleshooting

**Commands not found after install?**

- Restart OpenCode to reload plugins
- Verify `openpaul` is listed in the `plugin` array in `opencode.json` (npm package)
- If you are using a local build, verify `.opencode/plugins/openpaul.ts` exists
- Run `opencode debug config` and confirm `openpaul` is in the resolved plugin list

**Commands not working as expected?**

- Run `/openpaul:help` to verify installation (it should autocomplete in the TUI)
- Check the plugin is installed in `~/.cache/opencode/node_modules/openpaul/`

**Loop position seems wrong?**

- Check `.openpaul/state-phase-N.json` for machine-readable loop state (PLAN/APPLY/UNIFY)
- Check `.openpaul/STATE.md` if you maintain a human-readable companion
- Run `/openpaul:progress` for guided next action

**Resuming after a break?**

- Run `/openpaul:resume` — it reads state and handoffs automatically

---

## Comparison

### vs. Ad-hoc AI Coding

| Ad-hoc         | OpenPAUL                   |
| -------------- | -------------------------- |
| No structure   | Explicit planning gates    |
| State drifts   | Loop state JSON tracks everything |
| No closure     | Mandatory UNIFY            |
| Decisions lost | Decisions logged           |

### vs. GSD

OpenPAUL takes a different approach from GSD:

| Aspect    | GSD                | OpenPAUL               |
| --------- | ------------------ | ---------------------- |
| Execution | Parallel subagents | In-session context     |
| Loop      | Optional closure   | Mandatory UNIFY        |
| Criteria  | Embedded in tasks  | First-class AC section |
| Rules     | Static prompts     | CARL dynamic loading   |

Same comprehensive coverage, different philosophy. OpenPAUL prioritizes quality over speed-for-speed's-sake. See [OPENPAUL-VS-GSD.md](OPENPAUL-VS-GSD.md) for full comparison.

### vs. Traditional Planning

| Traditional          | OpenPAUL                |
| -------------------- | ----------------------- |
| Documentation-first  | Execution-first         |
| Human-readable specs | AI-executable prompts   |
| Separate from code   | Colocated in .openpaul/ |

---

## Attribution & License

Plan-Apply-Unify Loop was originally created by [Chris Kahler](https://github.com/ChristopherKahler) for Claude Code.

**OpenPAUL** is an OpenCode adaptation, maintained by [Kristian Gray](https://github.com/KrisGray).

The original project can be found on Chris Kahler's GitHub profile.

MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Kristian Gray** — OpenPAUL Maintainer

**Original Author** — Chris Kahler (Plan-Apply-Unify Loop creator)

---

<div align="center">

**OpenCode is powerful. OpenPAUL makes it reliable.**

</div>
