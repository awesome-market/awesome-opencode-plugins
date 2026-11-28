# git gen

[![npm](https://img.shields.io/npm/v/@gitgen/gitgen)](https://www.npmjs.com/package/@gitgen/gitgen)
[![docker](https://img.shields.io/docker/v/gilikv/gitgen?label=docker)](https://hub.docker.com/r/gilikv/gitgen)

**Generate code with git.**

```
$ git gen dev "add dark mode toggle" -b feat/dark

  plan     Analyzing codebase...
           Found: useLocalStorage hook, ThemeContext pattern
           Creating: src/components/ThemeToggle.tsx
           Modifying: src/App.tsx, src/styles/globals.css

  code     + src/components/ThemeToggle.tsx (42 lines)
           + src/hooks/useDarkMode.ts (28 lines)
           ~ src/App.tsx (+3 lines)
           ~ src/styles/globals.css (+24 lines)

  test     + src/components/ThemeToggle.test.tsx
           PASS  4 tests

  commit   feat(ui): add dark mode toggle with system preference detection

  push     → origin/feat/dark
           → PR #47: feat(ui): add dark mode toggle

  Done in 34s
```

---

## Quick Start

```bash
npm i -g @gitgen/gitgen
git gen setup                   # configure provider + platform
git gen init                    # analyze codebase
git gen dev "your feature"      # plan → code → test → push
```

## Commands

| Command | What it does | Creates |
|---------|-------------|---------|
| [`init`](.agent/commands/gitgen/init.md) | Setup gitgen in a project | `.gitgen.md` `SPEC.md` `PLAN.md` |
| [`dev`](.agent/commands/gitgen/dev.md) | Full workflow: plan → code → test → push | source files + PR |
| [`ask`](.agent/commands/gitgen/ask.md) | Answer questions about your code | — |
| [`learn`](.agent/commands/gitgen/learn.md) | Analyze codebase, capture patterns | `.gitgen.md` `.agent/context/*.md` |
| [`spec`](.agent/commands/gitgen/spec.md) | Generate architecture docs | `SPEC.md` |
| [`plan`](.agent/commands/gitgen/plan.md) | Design implementation plan | `PLAN.md` |
| [`code`](.agent/commands/gitgen/code.md) | Generate source files | source files |
| [`test`](.agent/commands/gitgen/test.md) | Generate and run tests | `TEST.md` + test files |
| [`fix`](.agent/commands/gitgen/fix.md) | Fix failing tests | source files |
| [`push`](.agent/commands/gitgen/push.md) | Commit and push | commit + PR |

**Options:** `--branch <name>` · `--issue <number>` · `--skip-tests` · `--skip-push` · `--max-fix <n>`

---

## Real Output Examples

### `git gen init`

```
$ git gen init

  setup    Provider: anthropic (claude-sonnet-4-20250514)
           Remote: origin → github.com:you/my-app.git

  learn    Analyzing repository...
           Stack: typescript, react, tailwind
           Patterns: hooks in src/hooks/, components in src/components/
           Test framework: vitest
           Style: single quotes, 2-space indent

  create   .gitgen.md (2.1 KB)
           SPEC.md (8.4 KB)
           PLAN.md (empty)

  Ready
```

### `git gen dev "add search functionality" -b feat/search`

```
$ git gen dev "add search functionality" -b feat/search

  branch   → feat/search

  plan     Reading codebase patterns...
           Similar: src/hooks/useDebounce.ts
           Creating:
             src/hooks/useSearch.ts
             src/components/SearchBar.tsx
             src/components/SearchResults.tsx
           Modifying:
             src/App.tsx
             src/types/index.ts

  code     + src/hooks/useSearch.ts
           │  export function useSearch<T>(
           │    items: T[],
           │    searchFn: (item: T, query: string) => boolean
           │  ) {
           │    const [query, setQuery] = useState('')
           │    const debouncedQuery = useDebounce(query, 300)
           │    ...
           │  }

           + src/components/SearchBar.tsx (34 lines)
           + src/components/SearchResults.tsx (52 lines)
           ~ src/App.tsx (+12 lines)
           ~ src/types/index.ts (+8 lines)

  test     Running vitest...
           ✓ useSearch returns filtered results
           ✓ useSearch debounces input
           ✓ SearchBar renders input field
           ✓ SearchBar calls onSearch on input
           ✓ SearchResults displays items
           ✓ SearchResults shows empty state

           6 passed (0.8s)

  commit   feat(search): add search functionality with debounced input

           + 3 files, ~ 2 files
           106 insertions, 0 deletions

  push     → origin/feat/search
           → PR #23: feat(search): add search functionality
             https://github.com/you/my-app/pull/23

  Done (4 files changed, 1 PR created)
```

### `git gen dev --issue 42`

```
$ git gen dev --issue 42 -b fix/42-null-error

  issue    #42: TypeError: Cannot read property 'name' of null
           Labels: bug, priority:high

           > When clicking on a deleted user's profile, the app crashes.
           > Steps: 1. Delete user  2. Click cached profile link

  plan     Root cause: UserProfile.tsx doesn't handle null user
           Fix: Add null check before accessing user.name
           Files: src/components/UserProfile.tsx (1 change)

  code     ~ src/components/UserProfile.tsx
           │  - return <h1>{user.name}</h1>
           │  + if (!user) return <NotFound message="User not found" />
           │  + return <h1>{user.name}</h1>

  test     ✓ existing tests pass
           + UserProfile shows NotFound for null user

  commit   fix(profile): handle deleted user in UserProfile (#42)

  push     → origin/fix/42-null-error
           → PR #48 (closes #42)

  Done
```

### `git gen ask`

```
$ git gen ask "who contributed most to the auth module?"

  Analyzing question...
  Source: git-history (blame analysis)

  auth/ contributions (last 6 months):

    alice@company.com    847 lines (52%)
    ├─ auth/login.ts        312 lines
    ├─ auth/oauth.ts        289 lines
    └─ auth/session.ts      246 lines

    bob@company.com      438 lines (27%)
    └─ auth/middleware.ts   438 lines

    carol@company.com    341 lines (21%)
    └─ auth/utils.ts        341 lines

  Alice is the primary author, focusing on login and OAuth flows.
  Bob owns the middleware layer. Carol maintains utilities.
```

```
$ git gen ask "what are the open performance issues?"

  Fetching GitHub issues...
  Found 3 open issues labeled 'performance':

  #42  Bundle size too large                    opened 3 days ago
       > Main bundle is 2.4MB, should be under 500KB
       Labels: performance, priority:high

  #38  Slow initial render on mobile            opened 1 week ago
       > First contentful paint > 4s on 3G
       Labels: performance, bug

  #31  API calls not cached                     opened 2 weeks ago
       > Same data fetched multiple times per session
       Labels: performance, enhancement
```

### `git gen learn`

```
$ git gen learn

  analyze  Scanning repository...
           Files: 127 (42 TypeScript, 38 React, 12 tests)
           Commits: 342 (last 6 months)

  detect   Stack: typescript, react, tailwind, vitest
           Patterns:
             hooks     → src/hooks/use*.ts
             components → src/components/**/*.tsx
             utils     → src/lib/*.ts
           Style: single quotes, no semicolons, 2-space indent

  create   .gitgen.md (2.4 KB)

  Done
```

### `git gen spec`

```
$ git gen spec

  analyze  Architecture analysis...
           Entry: src/index.ts → App.tsx
           Modules: auth, api, components, hooks, utils
           Patterns: Context providers, custom hooks, barrel exports

  create   SPEC.md (12.3 KB)
           │  # my-app Specification
           │  ## Architecture
           │  ## Directory Structure
           │  ## Commands
           │  ## Extension Points
           │  ...

  Done
```

### `git gen plan "add user preferences"`

```
$ git gen plan "add user preferences"

  analyze  Reading codebase...
           Found: useLocalStorage hook, UserContext
           Similar: src/hooks/useSettings.ts

  create   PLAN.md
           │  # User Preferences Implementation Plan
           │
           │  ## Overview
           │  Add persistent user preferences with sync support.
           │
           │  ## Files to Create/Modify
           │  | File | Action | Purpose |
           │  |------|--------|---------|
           │  | src/hooks/usePreferences.ts | create | Preferences hook |
           │  | src/context/PreferencesContext.tsx | create | Context provider |
           │  | src/components/PreferencesModal.tsx | create | Settings UI |
           │  | src/App.tsx | modify | Add provider |
           │
           │  ## Implementation Phases
           │  1. Core hook + context
           │  2. UI components
           │  3. Sync integration

  Done
```

---

## Workflow

```
git gen dev "feature description"
        │
        ▼
┌─────────────────────────────────────────────────┐
│                                                 │
│   plan ──────▶ Analyze codebase, design files   │
│     │                                           │
│   code ──────▶ Generate implementation          │
│     │                                           │
│   test ──────▶ Run tests                        │
│     │                                           │
│   fix ◀─────▶ Fix failures (loop until pass)   │
│     │                                           │
│   commit ────▶ Stage and commit                 │
│     │                                           │
│   push ──────▶ Push branch, create PR           │
│                                                 │
└─────────────────────────────────────────────────┘
        │
        ▼
    PR ready for review
```

---

## Setup

```bash
npm i -g @gitgen/gitgen
export ANTHROPIC_API_KEY=sk-ant-...  # or OPENAI_API_KEY, etc.
git gen setup                        # configure for your IDE
```

### Platforms

| Platform | Setup command |
|----------|---------------|
| Terminal | `npm i -g @gitgen/gitgen` |
| Docker | `docker pull gilikv/gitgen` |
| Claude Code | `git gen setup claude-code` |
| OpenCode | `git gen setup opencode` |
| Cursor | `git gen setup cursor` |
| Windsurf | `git gen setup windsurf` |
| Cline | `git gen setup cline` |
| Aider | `git gen setup aider` |
| Zed | `git gen setup zed` |
| GitHub Actions | `git gen setup github-actions` |

### Providers

| Provider | Environment Variable |
|----------|---------------------|
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Google | `GOOGLE_GENERATIVE_AI_API_KEY` |
| AWS Bedrock | `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| GitHub Models | `GITHUB_TOKEN` |

Auto-detects from environment. Override with `--model <name>`.

---

## Customization

Commands live in `.agent/commands/gitgen/`. Edit to customize prompts:

```
.agent/
├── commands/gitgen/       # Command prompts
│   ├── dev.md             # Full workflow
│   ├── ask.md             # Q&A with RAG
│   ├── code.md            # Code generation
│   └── ...
├── templates/gitgen/      # Shared fragments
│   ├── context.md         # Project context injection
│   └── code-style.md      # Style matching rules
└── context/               # Session state
```

Add new command: create `.agent/commands/gitgen/mycommand.md` → `git gen mycommand`

---

[Docs](https://gitgen.dev/docs) · [SPEC](SPEC.md) · [Samples](samples/) · MIT
