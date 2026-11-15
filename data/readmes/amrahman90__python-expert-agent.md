# Python Expert Agent for OpenCode

[![npm version](https://img.shields.io/npm/v/python-expert-agent.svg)](https://www.npmjs.com/package/python-expert-agent)
[![License: MIT](https://img.shields.io/npm/l/python-expert-agent.svg)](https://opensource.org/licenses/MIT)
[![npm downloads](https://img.shields.io/npm/dm/python-expert-agent.svg)](https://www.npmjs.com/package/python-expert-agent)
[![experimental](https://img.shields.io/badge/status-experimental-orange)](https://github.com/amrahman90/python-expert-agent)

**A comprehensive Python agentic tool for [OpenCode](https://opencode.ai) with 10 skills, 4 subagents, and production-ready FastAPI patterns.**

> **Note:** This package is experimental and works great for local project-based use.

---

## Why Use This?

**Stop repeating yourself.** This agent pack gives OpenCode deep Python expertise:

| What You Get | Benefit |
|--------------|---------|
| **10 specialized skills** | Load expertise on-demand (FastAPI, SQLAlchemy, pytest, etc.) |
| **4 subagents** | Delegate to specialists for coding, review, testing, exploration |
| **Production patterns** | Code that scales, not just code that works |
| **Zero-config** | Install and start coding |

**Before:** Explain FastAPI patterns, Pydantic schemas, JWT auth, async database every time.

**After:**
```
skill(name="python-fastapi")
Create a login endpoint
```

---

## Features

- **1 Primary Agent** - `python-expert` with intelligent skill loading
- **4 Specialized Subagents** - Code generation, review, testing, and exploration
- **10 On-Demand Skills** - FastAPI, SQLAlchemy, pytest, asyncio, and more
- **4 Context Files** - Standards, patterns, security, and navigation
- **Production Ready** - Targets Python 3.13+, FastAPI, Pydantic v2, SQLAlchemy 2.0

---

## Installation

### From npm (Recommended)

```bash
# Install globally
npm install -g python-expert-agent

# Install to current project
python-expert-agent init

# Install globally (for all projects, experimental)
python-expert-agent init --global
```

### Using npx (No install needed)

```bash
npx python-expert-agent init
```

### Manual Installation

Copy the `.opencode` directory and `AGENTS.md` to your project root.

---

## Quick Start

```bash
# 1. Install the agent pack
npm install -g python-expert-agent
python-expert-agent init

# 2. Start OpenCode in your Python project
cd /path/to/your/python/project
opencode

# 3. The python-expert agent is automatically detected

# 4. Use skills on-demand
skill(name="python-fastapi")
skill(name="python-backend")
```

---

## Common Use Cases

### Create a REST API Endpoint

```
skill(name="python-fastapi")

Create a POST /api/users endpoint with:
- Email validation
- Password hashing (bcrypt)
- JWT token generation
```

### Add Tests to Existing Code

```
skill(name="python-testing-general")

Write tests for src/services/user.py:
- Unit tests for create_user, get_user
- Mock the database
- Test edge cases (empty input, duplicates)
```

### Debug Async Issues

```
skill(name="python-asyncio")

Fix the memory leak in src/services/websocket.py.
Connections are not being cleaned up properly.
```

### Security Code Review

```
Review src/api/auth.py for:
- SQL injection vulnerabilities
- Hardcoded secrets
- Missing authentication checks
```

### Database Model with Migrations

```
skill(name="python-backend")

Create an async SQLAlchemy model for:
- User entity with relationships
- Alembic migration
- Repository pattern
```

---

## How It Works

### Activation Flow

```
Project Opens
     │
     ▼
┌─────────────────────────────────────────────┐
│  OpenCode reads .opencode/config.json       │
│           ↓                                 │
│  Loads python-expert agent                  │
│           ↓                                 │
│  Detects .py files in project               │
│           ↓                                 │
│  Invokes skill(name="python-fundamentals")  │
└─────────────────────────────────────────────┘
```

### Request Processing Flow

```
User: "Create a FastAPI endpoint with JWT auth"
     │
     ▼
┌─────────────────────────────────────────────┐
│         python-expert (Primary Agent)       │
│                                             │
│  1. Parse request for keywords:             │
│     "fastapi" → python-fastapi              │
│     "jwt" → python-backend                  │
│                                             │
│  2. Invoke skills:                          │
│     skill(name="python-fastapi")            │
│     skill(name="python-backend")            │
│                                             │
│  3. Determine complexity:                   │
│     "create" + multi-step = Complex         │
└────────────────────┬────────────────────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │   Complex Task?     │
          └──────────┬──────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│Simple Query  │          │Complex Task  │
│              │          │              │
│Answer        │          │Delegate to   │
│directly      │          │subagent      │
└──────────────┘          └──────────────┘
```

### Subagent Collaboration Flow

```
Complex Task: "Create user authentication system"
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│              python-expert (Primary Agent)              │
│                                                         │
│  Delegates context discovery:                           │
│  task(subagent_type="explore", description="Find auth   │
│      patterns, existing user models, similar endpoints")│
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│               python-scout (Explore Subagent)           │
│                                                         │
│  1. Search codebase for relevant files                  │
│  2. Read existing patterns and conventions              │
│  3. Check .opencode/context/ for standards              │
│  4. Return ranked recommendations:                      │
│     - Files to reference                                │
│     - Patterns to follow                                │
│     - Skills to load                                    │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│              python-expert (Primary Agent)              │
│                                                         │
│  Receives context from scout, delegates implementation: │
│  task(subagent_type="general", description="Create auth │
│       system", prompt="Context: [scout findings]...")   │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│               python-coder (General Subagent)           │
│                                                         │
│  1. Load skills: python-fastapi, python-backend         │
│  2. Read reference files found by scout                 │
│  3. Follow project patterns from context                │
│  4. Create endpoint, schema, service, tests             │
│  5. Run verification (mypy, ruff, pytest)               │
│  6. Return summary of changes                           │
└─────────────────────────────────────────────────────────┘
```

### Subagent Roles

| Subagent | When Used | What It Does |
|----------|-----------|--------------|
| `python-scout` | Before implementation | Discovers context, finds patterns, recommends files |
| `python-coder` | Implementation tasks | Creates/modifies code following skill patterns |
| `python-reviewer` | After implementation | Reviews code for quality, security, performance |
| `python-tester` | Testing tasks | Writes unit/integration tests with mocking |

### Typical Workflow

```
1. Scout     → Discover context and patterns
2. Coder     → Implement following patterns  
3. Tester    → Write tests for new code
4. Reviewer  → Review for quality/security (optional)
```

### Key Points

- **Skills are on-demand**: Load via `skill(name="...")` - no auto-loading
- **Context first**: Complex tasks start with scout for context discovery
- **Pattern-driven**: All code follows loaded skill patterns
- **Verification included**: Type checking, linting, tests run automatically

---

## Components

### Primary Agent

| Agent | Description |
|-------|-------------|
| `python-expert` | Main agent with skill loading protocol, keyword detection, and task delegation |

### Subagents

| Subagent | Type | Purpose |
|----------|------|---------|
| `python-coder` | general | Code generation and feature implementation |
| `python-reviewer` | general | Code quality and security review |
| `python-tester` | general | Test writing with pytest patterns |
| `python-scout` | explore | Context discovery and file finding |

### Skills

| Skill | Triggers | Best For |
|-------|----------|----------|
| `python-fundamentals` | `*.py`, `python`, `dataclass` | Core Python 3.11+ patterns |
| `python-fundamentals-313` | `3.13`, `jit`, `free-threading` | Python 3.13+ specific features |
| `python-fastapi` | `fastapi`, `pydantic`, `endpoint` | REST APIs, Pydantic schemas |
| `python-backend` | `sqlalchemy`, `database`, `orm` | Async database, migrations |
| `python-testing-general` | `pytest`, `test`, `mock` | Unit/integration testing |
| `python-testing-deep` | `hypothesis`, `property-based` | Advanced testing techniques |
| `python-asyncio` | `async`, `await`, `asyncio` | Async/await, concurrency |
| `python-type-hints` | `typing`, `mypy`, `pyright` | Type annotations, mypy config |
| `python-package-management` | `uv`, `pip`, `pyproject` | Dependencies, virtual envs |
| `python-tooling` | `docker`, `ci`, `cd` | Docker, GitHub Actions, profiling |

---

## Project Structure

```
.opencode/
├── config.json              # Agent selection
├── opencode.json            # Schema reference
├── agent/
│   └── python-expert.md     # Primary agent definition
├── subagents/
│   ├── python-coder.md      # Code generation
│   ├── python-reviewer.md   # Code review
│   ├── python-tester.md     # Test writing
│   └── python-scout.md      # Context discovery
├── skills/                  # 10 Python skills
│   ├── python-fundamentals/
│   ├── python-fastapi/
│   ├── python-backend/
│   └── ...
├── context/
│   ├── navigation.md        # Quick reference
│   └── python/
│       ├── standards.md     # Code quality standards
│       ├── patterns.md      # Common patterns
│       └── security.md      # Security patterns
├── config/
│   └── agent-metadata.json  # Agent registry
└── docs/                    # Documentation
```

---

## CLI Reference

```bash
python-expert-agent init [path]    # Install to project
python-expert-agent init --global  # Install globally (experimental)
python-expert-agent init --force   # Overwrite existing files
python-expert-agent --version      # Show version
python-expert-agent --help         # Show help
```

---

## Example Technology Stack standard choice for a Python backend focused developement project

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.13+ |
| Web Framework | FastAPI | 0.115+ |
| Data Validation | Pydantic | 2.7+ |
| ORM | SQLAlchemy | 2.0 (async) |
| Database | PostgreSQL | 16 |
| Testing | pytest | latest |
| Package Manager | UV | latest |
| Linting | ruff, mypy | latest |

---

## Documentation

Full documentation is available in `.opencode/docs/`:

| Document | Description |
|----------|-------------|
| [Overview](./.opencode/docs/overview.md) | System introduction |
| [Architecture](./.opencode/docs/architecture.md) | Component relationships |
| [Agents](./.opencode/docs/agents.md) | Agent configuration |
| [Skills](./.opencode/docs/skills.md) | Skill documentation |
| [Subagents](./.opencode/docs/subagents.md) | Subagent workflows |
| [Workflow](./.opencode/docs/workflow.md) | Development patterns |
| [Configuration](./.opencode/docs/configuration.md) | Customization guide |

---

## Requirements

| Requirement | Version |
|-------------|---------|
| [OpenCode](https://opencode.ai) CLI | latest (Currently tested on v1.2.15) |
| Node.js | 18+ (for CLI installer) |
| Python | 3.11+ (for projects using this agent) |

---

## FAQ

### How is this different from plain OpenCode?

OpenCode is general-purpose. This pack adds:
- Python-specific patterns and best practices
- Framework expertise (FastAPI, SQLAlchemy, pytest)
- Specialized subagents for different task types
- Context files with project standards

### Does it work with my existing project?

Yes. The agent reads your existing code patterns and follows them.

### Can I customize the skills?

Yes. Edit any `.opencode/skills/*/SKILL.md` file to add your own patterns.

### Which Python versions are supported?

Python 3.11+ is required. Patterns use 3.13+ features where applicable.

### Do skills auto-load?

No. Skills must be explicitly invoked with `skill(name="...")`. This gives you control over context usage.

### Can I use this globally for all projects?

Yes: `python-expert-agent init --global` (experimental feature).

---

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License - see [LICENSE](./LICENSE) file for details.

---

## Links

- [OpenCode](https://opencode.ai) - The open source AI coding agent
- [OpenCode Docs](https://opencode.ai/docs) - Official documentation
- [npm Package](https://www.npmjs.com/package/python-expert-agent) - npm registry

---

## Acknowledgments

- [OpenCode](https://github.com/anomalyco/opencode) - The amazing AI coding agent
- [Agentic](https://github.com/Cluster444/agentic) - Reference for CLI structure
