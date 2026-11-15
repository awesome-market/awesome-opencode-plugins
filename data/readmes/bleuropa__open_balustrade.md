# Balustrade (OpenCode Fork)

> **Opinionated rails for OpenCode development**

### Forked From

**[bcooke/balustrade](https://github.com/bcooke/balustrade)** - The original Balustrade meta-framework for Claude Code. This OpenCode version is a direct adaptation of that excellent work. All credit for the core concepts, architecture, and patterns goes to [@bcooke](https://github.com/bcooke).

---

Balustrade is a **meta-framework** providing structured guardrails for working with OpenCode.

**Meta-framework**: Manages the "meta" of OpenCode and agentic development - how you organize work, maintain context, and enforce standards.

**Primary job**: Give people and agents "rails" for OpenCode through an opinionated template.

**Language-agnostic. Minimal dependencies. Framework-focused.**

---

## What Is This?

A **reference implementation** showing how to use OpenCode's features together:
- **Git hooks** enforce conventions automatically (determinism)
- **Slash commands** guide consistent workflows (repeatability)
- **PROJECT_STATUS.md** provides token-efficient context (~500 vs 5000+ tokens)
- **Vault structure** organizes docs for both humans and agents (Obsidian patterns)

**This is both**:
1. **A template** - Fork it, customize it, make it yours
2. **An example** - Learn the patterns, adapt for your needs

**Not prescriptive**. Shows you HOW to build rails for YOUR conventions.

---

## What's Included

```
balustrade/
├── .opencode/                  # THE FRAMEWORK (keep this)
│   ├── hooks/                  # Git hooks for enforcement
│   ├── command/                # Slash commands for workflows
│   ├── agent/                  # Agent templates
│   ├── skill/                  # Reusable skills
│   └── opencode.json           # Configuration (in root)
├── vault/                      # DOCUMENTATION PATTERNS (keep this)
│   ├── product/                # Product vision, user journeys
│   ├── architecture/           # System design, decisions
│   ├── features/               # Feature specifications
│   ├── _meta/                  # Writing guidelines
│   ├── how-to/                 # Process docs
│   └── pm/                     # Project management (tasks, context)
├── _reference/                 # REFERENCE MATERIALS (gitignored)
│   ├── repos/                  # Cloned repos for inspiration
│   ├── screenshots/            # UI mockups, design references
│   └── docs/                   # PDFs, PRDs, external specs
├── example-app/                # EXAMPLE APP (delete this)
│   ├── server.js               # Minimal Node HTTP server
│   ├── index.html              # Vanilla JS + Tailwind CDN
│   └── README.md               # "This is just an example"
├── .devcontainer/              # Dev container config
├── opencode.json               # OpenCode configuration
├── AGENTS.md                   # Project instructions for OpenCode
├── PROJECT_STATUS.md           # Status tracking template
└── README.md                   # This file
```

---

## Quick Start

### 1. Fork This Repository

```bash
# Or use as template on GitHub
```

### 2. Delete Example App

```bash
rm -rf example-app/
```

The example todo app is just for demonstration. Delete it.

### 3. Add Your App

**Node.js?**
```bash
npm init
# Add your Node code
```

**Python?**
```bash
python -m venv venv
# Add your Python code
```

**Mobile? Rust? Elixir? Anything?**

Balustrade is language-agnostic. The `.opencode/` and `vault/` patterns work with any stack.

See `vault/how-to/Multi-Language Support.md` for examples.

### 4. Install Hooks

```bash
bash .opencode/hooks/install-hooks.sh
```

This creates symlinks in `.git/hooks/`:
- `pre-commit` - Validates code quality, docs, PM discipline
- `commit-msg` - Validates conventional commit format
- `post-commit` - Auto-updates PROJECT_STATUS.md

### 5. Customize

- Update `PROJECT_STATUS.md` with your project name and priorities
- Edit `vault/product/` docs for your product vision
- Modify `.opencode/hooks/pre-commit.sh` for your conventions
- Add your agents in `.opencode/agent/`
- Customize `AGENTS.md` with your project-specific rules

### 6. Use Agents and Skills (Examples Included)

Balustrade includes example agents and skills to help you understand these OpenCode features:

**Example Agents** (`.opencode/agent/`):
- `coordinator` - Multi-domain task coordination
- `full-stack-dev` - Feature implementation
- `code-reviewer` - Code quality review
- `bug-hunter` - Debugging specialist

**Example Skills** (`.opencode/skill/`):
- `refactor` - Code refactoring patterns
- `test-setup` - Testing guidance
- `api-design` - REST API best practices
- `docs` - Documentation writing

**Use them**:
```
@full-stack-dev Implement user profile editing
@bug-hunter Debug login failure
@code-reviewer Review auth module
```

**Customize them**: Replace with YOUR project's specialists and expertise!

### 7. Start Using Slash Commands

In OpenCode:

```
/status              # Quick status (reads PROJECT_STATUS.md only, ~500 tokens)
/p Add user auth     # Plan task (creates T-YYYY-NNN, updates status)
/s T-2025-001        # Start task (creates branch, updates status)
/ctx Key decision    # Update context doc
/call agent task     # Invoke specialized agent
/review              # Address PR feedback
/c                   # Close task (reviews, updates status, creates PR)
/wrap                # End-of-session summary
```

---

## The Real Value

### Not The Todo App

The example app (~100 lines) is just demonstration. Delete it.

### The Meta-Framework

**`.opencode/` directory** shows how to:
- Enforce conventions with hooks
- Guide workflows with commands
- Coordinate with agents
- Integrate with OpenCode

**`vault/` structure** shows how to:
- Organize product documentation
- Track architecture decisions
- Manage PM workflows
- Write evergreen docs

**`PROJECT_STATUS.md`** shows:
- Token-efficient status tracking (~500 tokens vs 5000+)
- Single source of truth
- Auto-updated by hooks

---

## Core Concepts

### 1. Hooks Enforce Conventions

**Pre-commit** validates before commits:
- Temporal language in evergreen docs (example - customize for your rules)
- Task structure and status
- Task size warnings
- Your conventions here

**Commit-msg** enforces:
- Conventional commit format

**Post-commit** auto-updates:
- PROJECT_STATUS.md timestamp and recent files

### 2. Commands Guide Workflows

Slash commands maintain consistency:
- `/p` - Plan tasks with standard structure
- `/s` - Start tasks with branch creation
- `/c` - Close tasks with review checklist
- `/ctx` - Update context docs
- `/status` - Token-efficient status checks
- `/wrap` - Session summaries

### 3. Vault Organizes Knowledge

**Evergreen docs** (product/, architecture/, features/):
- Timeless, no temporal language
- Describe current state
- Heavily linked with `[[wiki links]]`

**PM docs** (pm/):
- Tasks with standard structure
- Context docs for working notes
- Temporal language OK here

### 4. Status Tracking Optimizes Tokens

`PROJECT_STATUS.md`:
- Single file with complete project state
- ~500 tokens vs 5000+ for scanning vault
- Auto-updated by hooks and commands
- Read this first, not the entire codebase

---

## Customization

### What To Keep

- `.opencode/hooks/` structure (add your checks)
- `.opencode/command/` patterns (modify for your workflow)
- `vault/` organization (adapt for your domain)
- `PROJECT_STATUS.md` concept (your project state)

### What To Change

- Specific hook validations (temporal language is just an example)
- Agent definitions (add your specialists)
- Vault sections (add your domains)
- Dev container config (your stack)

### What To Delete

- `example-app/` (replace with your code)
- Todo app docs in `vault/` (replace with your product)
- Conventions that don't fit your project

See `CUSTOMIZATION.md` for step-by-step guide.

---

## Example Conventions

Balustrade includes these as **demonstrations**:

| Convention | What | Why | Customize |
|---|---|---|---|
| Temporal language | Block "will", "soon" in evergreen docs | Keeps docs current | Edit word list or remove |
| Task structure | Validate frontmatter fields | Consistent tracking | Add your fields |
| Task size | Warn if >7 checklist items | Right-sized work | Change threshold |
| Conventional commits | Enforce type(scope): format | Searchable history | Add your types |

**These are examples.** Add **your** conventions.

See `vault/how-to/Adding Your Conventions.md` for how to add:
- API naming standards
- Error handling patterns
- Test coverage requirements
- Database migration safety
- Documentation requirements
- Your team's rules

---

## Language Support

Works with **any** language or framework:

- **Node/Python/Ruby/Go** - Backend APIs
- **React/Vue/Angular** - Frontend apps
- **iOS/Android/Flutter** - Mobile apps
- **Rust/Elixir/C++** - Systems programming
- **Anything else** - It's just markdown + git hooks

The meta-framework is language-agnostic.

See `vault/how-to/Multi-Language Support.md`.

---

## Obsidian Integration (Optional)

Balustrade works great with Obsidian for:
- Graph view of linked docs
- Backlinks and connections
- Fast full-text search
- Wiki-style navigation

**Why it works so well**: Obsidian community best practices (atomic notes, rich linking) are optimal for OpenCode's context management.

**But it's optional.** Use VS Code, terminal, or any editor.

See `vault/how-to/Obsidian Integration.md` for deep dive on why Obsidian + OpenCode work well together.

---

## What Makes This Different

### It's a Meta-Framework

**Not a code framework** - It's a framework for working with OpenCode:
- Manages the "meta" of development (how you work, not what you build)
- Provides rails for agents and humans
- Enforces YOUR conventions (not prescriptive ones)
- Optimizes for OpenCode's specific needs (context management, determinism)

**No npm install. No CLI. Just patterns.**

Fork the repo, customize it, make it yours.

### Opinionated About Process, Not Code

**Strong opinions about**:
- How to provide context to OpenCode efficiently
- How to enforce standards deterministically
- How to organize knowledge for humans and agents
- How to track work that OpenCode manages

**Zero opinions about**:
- What programming language you use
- What frameworks you choose
- What your product does
- How you architect your code

**Your code, your stack, your product.**

### Language-Agnostic

Works with **any** tech stack:
- Node, Python, Rust, Go, Ruby, Elixir
- React, Vue, Angular, Svelte
- iOS, Android, Flutter
- Any combination of the above

The `.opencode/` directory and `vault/` structure sit alongside your code, regardless of language.

### Teaching By Example

**Includes minimal todo app** (~100 lines, zero dependencies):
- Shows patterns in action
- Not production code
- Delete it and replace with YOUR app

**The framework is the valuable part**, not the example.

---

## Documentation

**In this repo**:
- `HOW-IT-WORKS.md` - Visual walkthrough of the system
- `CUSTOMIZATION.md` - Make Balustrade yours
- `SUMMARY.md` - Complete file manifest and overview
- `vault/how-to/Meta-Framework.md` - Framework overview
- `vault/how-to/Hooks and Automation.md` - Hook details
- `vault/how-to/Git Workflow.md` - Commit conventions
- `vault/how-to/PM-Hierarchy.md` - Epics, Stories, Tasks, Bugs
- `vault/how-to/Adding Your Conventions.md` - Add your rules
- `vault/how-to/Using Reference Materials.md` - The `_reference/` pattern
- `vault/how-to/Multi-Language Support.md` - Any language
- `vault/how-to/Dev Container Setup.md` - Multi-agent setup
- `vault/how-to/Obsidian Integration.md` - Optional enhancement

**PM Templates** (in `vault/_templates/`):
- `Epic.md`, `Story.md`, `Task.md`, `Bug.md`, `Context.md` - Copy these to create new PM artifacts

**Example PM files** (in `vault/pm/`):
- `epics/E-2025-001-todo-app-mvp.md` - Example epic
- `stories/US-2025-001-setup-api.md` - Example user story
- `tasks/T-2025-001-setup-todo-api.md` - Example task
- `bugs/B-2025-001-fix-cors-error.md` - Example bug
- `_context/E-2025-001-context.md` - Example context doc

---

## Philosophy

### Convention Over Configuration

Like Ruby on Rails, Balustrade favors:
- Standard directory structure
- Predictable file naming
- Consistent workflows
- Automated maintenance

But for **project management**, not web apps.

### Determinism Over Flexibility

Hooks enforce standards automatically:
- No relying on memory
- No manual checklist
- Same validation every time
- Whether human or AI writes code

### Token Efficiency First

Every design decision optimizes for:
- Minimal context window usage (~10x reduction)
- Fast status checks (PROJECT_STATUS.md)
- Structured state tracking
- Preserved context across sessions

### Framework As Example

Don't copy prescriptively. Learn the patterns:
- See how hooks enforce conventions
- Understand command-guided workflows
- Study documentation organization
- Then adapt for your project

---

## Contributing

Found a bug or want to improve the template?

1. File an issue describing the problem/enhancement
2. Submit PR with changes
3. Include example demonstrating value

---

## License

MIT - Use freely, modify as needed, no attribution required.

---

## Credits

Inspired by Ruby on Rails, Git hooks, Obsidian, and [OpenCode](https://opencode.ai).

The `AGENTS.md` pattern follows [OpenCode's rules system](https://opencode.ai/docs/rules/).

Built to solve real problems in deterministic PM with AI.

---

## Get Started

1. **Fork** this repo
2. **Delete** example-app/
3. **Add** your code
4. **Customize** .opencode/ and vault/
5. **Build** with deterministic guardrails

The balustrade guides your path. Now build something great.
