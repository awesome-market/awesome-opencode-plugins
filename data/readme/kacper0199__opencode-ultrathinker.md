# Opencode-Ultrathinker

> A high-context, multi-agent OpenCode harness for coding, research, planning, writing, web intelligence, and long-running autonomous workflows.

**Opencode-Ultrathinker** is my personal global OpenCode configuration. It combines provider routing, specialist agents, reusable skills, persistent memory, codebase graph intelligence, web research, scraping, documentation lookup, and other third-party tools into one practical AI operating system for coding, research, planning, writing, automation, and daily use.

The config can be wired to many providers. My current setup uses a **Codex Pro plan** together with a **GitHub Copilot Educational plan**. With the right credit limits and project-specific local configuration, this harness can work continuously on hard tasks for hours, or until the provider budget run out.

This repository is not just a model list. It is a complete workflow:

- planner agents that design the work before code is touched,
- builder agents that implement the plan,
- specialist subagents for frontend, backend, AI, infrastructure, QA, research, and orchestration,
- MCP tools for code intelligence, browsing, search, GitHub, documentation, transcripts, local data, and more,
- skills that force repeatable workflows for planning, TDD, verification, GitNexus, Macrodata memory, and project standards,
- global directives that teach agents how to behave across repositories.

## Why this exists

Most AI coding setups fail because the model is asked to do everything directly: read a repo, plan, write code, test, search docs, remember decisions, and refactor safely. This config turns OpenCode into a coordinated harness where the main agent delegates work to specialists and uses dedicated tools for context instead of guessing.

It can be used as:

- a coding agent,
- a software architect,
- a researcher,
- a planning assistant,
- a technical writer,
- a web scraping and information synthesis system,
- a shopping/trip/research assistant,
- a general-purpose daily automation cockpit.

The only real limit is creativity and how carefully you adapt the global config to each project.

## Important note

This is an example of the **global OpenCode config** I use. I change it often. Local OpenCode configs can have higher precedence over this global config, so every serious project should have its own local overrides.

Use this repository as a starting point, not as a drop-in universal truth. Review every permission, model, path, MCP server, and agent instruction before running it on your machine.

For reference, my setup is macOS-oriented. The same design can be ported to Linux or Windows, but paths and local server wiring will differ.

## Credits and ecosystem

This config is built around several excellent open-source projects and ideas. If this repository helps you, please also check out and star the tools that make it possible:

- **OpenCode** — the agent runtime/config system.
- **everything-claude-code** — used as inspiration and source material for skill files.
- **awesome-claude-code-toolkit** — used as inspiration and source material for agent files.
- **Macrodata** — persistent project memory, journal, onboarding, and dreamtime-style continuity.
- **GitNexus** — codebase graph intelligence, impact analysis, symbol context, and safer refactoring.
- **Crawl4AI** — browser-backed scraping through the `crwl` CLI.
- **Context7, Exa, Brave Search, Gitingest, GitHub MCP, MCP Compass**, and the other MCP tools listed below.

Please star their repositories too. This harness is only useful because the ecosystem around it is moving fast.

## Repository layout

```text
Opencode-Ultrathinker/
├── AGENTS.md                  # Global workspace constitution for all agents
├── opencode.json              # Main OpenCode config: providers, permissions, agents, MCPs
├── planner-directive.md       # Lead planner/orchestrator instructions
├── update_agents_model.py     # Utility for changing models across agent files
├── agents/                    # 66 specialist subagents grouped by domain
└── skills/                    # 28 reusable skill workflows
```

## Main config

The heart of the repo is `opencode.json`. It defines:

- plugins: `@opencode-ai/plugin` and `@macrodata/opencode`,
- global permission policy,
- primary agents such as cheap planners/builders and high-reasoning planners/builders,
- wildcard cluster routes such as `core-development/*` and `data-ai/*`,
- MCP servers for search, documentation, GitHub, code intelligence, scraping, data exploration, and more.

The permission model is intentionally capable but not fully reckless. Most normal coding commands are allowed, destructive or sensitive tools are gated, and some MCPs are disabled by default.

## Primary agent routes

| Agent route | Mode | Model | Purpose |
| --- | --- | --- | --- |
| plan-cheap | primary | github-copilot/gpt-5-mini | Cheap planner |
| build-cheap | primary | github-copilot/gpt-5-mini | Cheap builder |
| build-gpt | primary | openai/gpt-5.3-codex | Elite implementation agent |
| plan-gpt | primary | openai/gpt-5.4 | Deep thinking planner |
| plan-gemini | primary | github-copilot/gemini-3.1-pro | Deep thinking planner |
| build-gemini | primary | github-copilot/gemini-3-flash | Fast & Cheap builder |
| core-development/* | subagent |  | CORE IMPLEMENTATION CLUSTER. A group of specialized models for building high-quality software. Delegate here to generate production-ready Frontend, Backend, and API code. These agents are optimized for specific framework implementations and architectural patterns. |
| data-ai/* | subagent |  | AI & DATA SPECIALIST CLUSTER. Dedicated experts for advanced AI engineering and data science. Use this group for designing RAG systems, vector database indexing, feature engineering, and model training workflows. |
| infrastructure/* | subagent |  | INFRASTRUCTURE & OPERATIONS CLUSTER. A specialized team for cloud environments and deployment stability. Delegate all tasks involving AWS/GCP/Azure, Kubernetes, CI/CD pipelines, and systems security to this group. |
| quality-assurance/* | subagent |  | QA & AUDIT CLUSTER. Independent verification experts. Use this group for objective code reviews, vulnerability assessments, performance profiling, and automated testing to ensure the highest reliability standards. |
| developer-experience/* | subagent |  | WORKFLOW & TOOLING CLUSTER. Experts in development ergonomics and repository hygiene. Delegate Git operations, dependency management, and MCP tool development to this specialist group. |
| research-analysis/* | subagent |  | TECHNICAL KNOWLEDGE CLUSTER. Specialized agents for deep research and synthesis. Use them for academic literature reviews, competitive technical analysis, benchmarking, and tracking technology trends. |
| orchestration/* | subagent |  | META-PROCESS CLUSTER. Experts in managing long-running, multi-step workflows. Delegate to this group when the task requires complex context management, error recovery across agents, or multi-task coordination. |
| general | subagent |  | Can be used for executing subtasks, writing code, and modifying files. You can delegate implementation to this agent. |
| explore | subagent |  | CRITICAL: USE PROACTIVELY to search patterns, read files, and explore the codebase. DO NOT guess file contents or architecture. You MUST use this agent to read code. |

## Specialist agent clusters

| Cluster | Agents | Examples |
| --- | --- | --- |
| Core Development | 8 | api-designer, api-gateway-engineer, backend-developer, event-driven-architect, frontend-architect... |
| Data & AI | 13 | ai-engineer, computer-vision-engineer, data-engineer, data-scientist, data-visualization... |
| Infrastructure | 6 | cloud-architect, deployment-engineer, devops-engineer, kubernetes-specialist, security-engineer... |
| Quality Assurance | 7 | code-reviewer, error-detective, penetration-tester, performance-engineer, qa-automation... |
| Developer Experience | 14 | api-documentation, build-engineer, cli-developer, dependency-manager, developer-portal... |
| Research & Analysis | 10 | academic-researcher, benchmarking-specialist, competitive-analyst, data-researcher, market-researcher... |
| Orchestration | 8 | agent-installer, context-manager, error-coordinator, knowledge-synthesizer, multi-agent-coordinator... |

See [`AGENT_CATALOG.md`](AGENT_CATALOG.md) for the full list of all 66 agents.

## Tooling and MCP layer

| MCP | Type | Default | What it does |
| --- | --- | --- | --- |
| puppeteer | local | disabled | Browser automation through the Model Context Protocol. Useful when an agent needs rendered pages, browser flows, screenshots, or JS-heavy websites. Disabled by default in this template. |
| memory | local | disabled | Reference MCP memory server for local memory experiments. Disabled by default because Macrodata is the primary persistent memory layer. |
| gitnexus | local | enabled | Code intelligence MCP. Builds and queries a graph of the repository so agents can inspect symbols, dependencies, call chains, impact radius, and safe refactoring paths. |
| exa | remote | enabled | Remote research MCP for web search, advanced search, code-context lookup, crawling, company/person research, and long-running deep research workflows. |
| brave-search | local | enabled | Search MCP backed by Brave Search. Good for recent public web results and a second opinion next to Exa. |
| fetcher | local | enabled | Single-page fetcher for quickly pulling web pages, documentation, or raw markdown into context. |
| reddit | local | enabled | Reddit MCP for community research, product opinions, debugging anecdotes, and sentiment checks. |
| youtube-transcript | local | enabled | Transcript extraction for YouTube videos, useful for turning talks, demos, tutorials, and product announcements into agent-readable text. |
| youtube-data | local | enabled | YouTube Data API integration for metadata, channel/video lookup, and richer YouTube research workflows. |
| time | local | enabled | Time and timezone MCP used when tasks depend on local time, schedules, or date-sensitive planning. |
| context7 | local | enabled | Documentation MCP for fetching current library/framework docs directly into the agent context. |
| desktop-commander | local | enabled | Local desktop/file-system automation MCP. Powerful and intentionally gated behind ask permissions in this config. |
| github | local | enabled | GitHub MCP for repository exploration, issues, pull requests, files, and source context from GitHub. |
| gitingest | local | enabled | Repository ingestion MCP that converts repositories into LLM-friendly summaries/context for analysis. |
| data-explorer | local | enabled | Local data and file exploration MCP for inspecting workspace structure, datasets, and tabular assets. |
| kaggle | local | disabled | Kaggle MCP for dataset and notebook workflows. Disabled by default because it needs user-specific credentials. |
| google-maps | local | disabled | Google Maps MCP for geospatial and place research. Disabled by default because it needs an API key and is not needed for most coding tasks. |
| simple-arxiv | local | disabled | Lightweight arXiv research MCP for papers and academic discovery. Disabled by default in this template. |
| mcp-compass | local | enabled | MCP discovery and navigation helper. Useful for understanding what MCP tools are available and how to route tasks to them. |

The config also allows a small set of shell-level tools:

| Tool | Purpose |
| --- | --- |
| git | Version control and branch workflow. |
| npm | Node.js package scripts and package management. |
| bun | Fast JS runtime/package runner used by selected MCP tools and modern web projects. |
| python3 | Python execution for scripts, data utilities, automation, and Python projects. |
| ls / cat | Basic project inspection and temporary markdown/document reading. |
| crwl / Crawl4AI | Browser-backed scraping pipeline that renders JS, bypasses noisy UI, and produces clean Markdown or JSON for agents. |
| npx gitnexus | CLI fallback for GitNexus analysis, graph queries, impact analysis, and safe refactoring when MCP calls fail. |

See [`TOOLING.md`](TOOLING.md) for the full tool catalog.

## Macrodata memory model

Macrodata is the continuity layer. The idea is simple: the agent should not wake up with amnesia every time a new session starts.

In this workflow, Macrodata is used for:

- project onboarding,
- global memory across projects and conversations,
- session journals,
- workspace state,
- summaries of what was done,
- preparation for the next session.

The dreamtime-style workflow is especially important. Macrodata can summarize previous work, consolidate memory, and help the next session start with awareness of what the project is, what was already done, what is blocked, and what should happen next.

This is one of the biggest reasons the harness works well on multi-day and multi-repository tasks.

## GitNexus code intelligence

GitNexus is the codebase brain of the setup. Instead of asking an agent to blindly grep files and guess architecture, GitNexus builds a graph-oriented understanding of the repository.

It is used for:

- indexing the codebase,
- representing code as higher-level nodes and relationships,
- finding symbols, callers, dependencies, and execution flows,
- impact analysis before changing a function/class/module,
- safer refactoring,
- detecting changed symbols,
- keeping generated codebase context in sync.

The workflow strongly prefers GitNexus MCP tools first, then the GitNexus CLI as a fallback. GitNexus changes quickly, so I recommend keeping it up to date and checking its repository often.

## Crawl4AI / `crwl` scraping protocol

The global directives include a Crawl4AI protocol through the `crwl` CLI. The pattern is:

1. scrape or crawl a website into a temporary Markdown/JSON file,
2. read the raw extracted content into context,
3. use it for implementation or research,
4. remove the temporary file.

This keeps browsing grounded. The agent does not guess documentation syntax, library APIs, pricing pages, or website data. It fetches the page, distills the useful content, injects it into the workflow, and cleans up the temporary artifacts.

## Skills

The `skills/` directory contains reusable procedures. These are not random notes. They are workflow modules that push agents toward repeatable behavior: planning, code review, security review, test-driven development, GitNexus usage, Macrodata maintenance, frontend/backend standards, and verification loops.

See [`SKILLS_CATALOG.md`](SKILLS_CATALOG.md) for the full skill list.

## How I recommend customizing it

Do not copy this config blindly. Adapt it.

Start with:

- `opencode.json` — choose your models, providers, MCPs, and permissions,
- `planner-directive.md` — adapt the planning and delegation rules,
- `AGENTS.md` — adapt the global style, coding rules, memory rules, Git rules, and scraping/code-intelligence protocols,
- `agents/**` — tune the specialist prompts to your stack,
- `skills/**` — add your own repeatable workflows.

One practical tip: agent instructions sometimes work better when critical routing rules are written as **BOLD UPPERCASE DIRECTIVES**. Use this carefully for non-negotiable behaviors, such as **EXPLORE BEFORE CODING**, **USE GITNEXUS IMPACT BEFORE REFACTORING**, or **DO NOT GUESS DOCUMENTATION SYNTAX**.

## Security warning

This harness can read files, run shell commands, call MCPs, inspect repositories, and use external APIs. Treat it like a powerful development assistant, not a harmless chatbot.

Before publishing or using your own fork:

- replace all local paths with placeholders,
- never commit real API keys or tokens,
- review enabled MCPs,
- review shell permissions,
- keep destructive tools gated behind ask/approval,
- understand that local configs may override global behavior.

See [`SECURITY_AND_PRIVACY.md`](SECURITY_AND_PRIVACY.md).

## Installation

See [`INSTALLATION.md`](INSTALLATION.md). It intentionally describes what needs to be installed and configured without pretending there is one universal command sequence for every machine.

## Contact

If this config helped you, or if you have ideas for improving the harness, see [`CONTACT.md`](CONTACT.md).
