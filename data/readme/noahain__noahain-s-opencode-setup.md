# Noahain's OpenCode Setup

AI coding agent configuration for [OpenCode](https://opencode.ai). Contains subagent definitions, skill packages, behavioral guidelines, and MCP server setup.

## Features

- **8 specialized subagents** — explore, git-agent, docs-fetcher, test-engineer, spec-verifier, code-reviewer, fast-coder, vibe-tester
- **101 skills** — reusable packages for frontend, backend, design, debugging, DevOps, and more
- **7 plugins** — superpowers, agent-skills, dcp, snip, notification, handoff, see-image
- **3 MCP servers** — Context7 (docs), Chrome DevTools (browser automation), 21st.dev (UI components)
- **RPD optimization mode** — parallel tool calls, batched reads, no permission seeking

## Structure

```
├── opencode.json          # Main config — agents, plugins, MCP
├── dcp.jsonc              # Deep Context Preservation config
├── AGENTS.md              # Behavioral guidelines for LLM agents (177 lines, loaded as instruction)
├── .gitignore
├── prompts/               # System prompts for each subagent
│   ├── explore.md         # Read-only search agent
│   ├── fast.md            # Fast coder for simple/boilerplate tasks
│   ├── git.md             # Git operations agent
│   ├── docs.md            # Documentation fetcher (Context7/WebFetch)
│   ├── test.md            # Build/lint/test runner
│   ├── spec.md            # Spec-compliance reviewer
│   ├── review.md          # Senior code reviewer
│   └── vibe-tester.md     # Spec validation simulator
└── skills/                # 101 reusable skill packages
    ├── frontend-design/   # Production-grade UI components
    ├── backend-patterns/  # Express, Next.js, Node.js patterns
    ├── brainstorming/     # Creative planning workflow
    ├── database-migrations/ # Prisma, Drizzle, Django, TypeORM patterns
    ├── debugger/          # Systematic debugging workflow
    ├── security-review/   # Auth, input handling, secrets patterns
    ├── cs-senior-engineer/ # Senior engineering standards
    ├── fable-mode/        # Staged execution discipline
    ├── project-markdown/  # Repo documentation generator
    ├── readme-writing/    # README improvement workflows
    ├── vibe-app-audit/    # AI-built app security & hardening audit
    └── ... (90 more)
```

## Subagents

| Agent | Model | Access | Purpose |
|---|---|---|---|
| `@fast-coder` | deepseek/deepseek-v4-flash | bash | Simple/boilerplate coding |
| `@vibe-tester` | opencode-go/kimi-k2.7-code | bash (read-only) | Spec validation & gap analysis |
| `@explore` | deepseek/deepseek-v4-flash | bash (read-only) | Code/file search |
| `@git-agent` | deepseek/deepseek-v4-flash | bash (read-only) | Git operations |
| `@docs-fetcher` | deepseek/deepseek-v4-pro | none | Documentation lookup |
| `@test-engineer` | deepseek/deepseek-v4-pro | bash (read-only) | Build/test/lint |
| `@spec-verifier` | deepseek/deepseek-v4-pro | bash (read-only) | Spec compliance |
| `@code-reviewer` | opencode-go/kimi-k2.7-code | bash (read-only) | Code quality review |

## MCP Servers

| Server | Purpose | Auth Required |
|---|---|---|
| Context7 | Library documentation queries | API key |
| Chrome DevTools | Browser automation and testing | None |
| 21st.dev | UI component search and generation | API key |

## Plugins

- `superpowers` — skill-based development workflow
- `opencode-agent-skills` — expanded skill library
- `@tarquinen/opencode-dcp` — deep context preservation
- `opencode-snip` — snippet management
- `opencode-notification` — system notifications
- `opencode-handoff` — session handoff
- `opencode-see-image` — screenshot viewing via vision model

## Key Behavioral Guidelines (from AGENTS.md)

- **Delegation** — explore, docs-fetcher, git-agent, test-engineer, vibe-tester, spec-verifier, code-reviewer, fast-coder are the only things delegated. Main agent does reasoning/design/fixes.
- **Ask before committing** — git commits require explicit user approval.
- **Verify before claiming** — tests, lint, and typecheck must produce fresh evidence before marking anything done.
- **Simplicity first** — minimum code that solves the problem. No features, abstractions, or config that wasn't requested.
- **RPD mode** — collapse work into fewest turns, batch reads, skip optional verification.
- **Surgical changes** — touch only what's required, match existing style, clean up only your own mess.
- **Subagent-Driven Development** — vibe-tester → build → spec-verifier → code-reviewer pipeline.

## Configuration

Edit `opencode.json` to:

- Add or remove subagents under `agent`
- Add plugins under `plugin`
- Configure MCP servers under `mcp`

MCP API keys (`Context7` and `21st`) are configured in `opencode.json` and should be populated before first use.

## License

MIT
