<div align="center">
  <p>
    <img src="https://www.topy.ai/long_logo.svg" alt="TOPY AI CEO" width="420" />
  </p>
  <h1>TOPY AI CEO Skills</h1>
  <p><strong>51 skills that make your coding agent a founder's AI CEO: business plans and revisions, strategy, fundraising, finance, operations and leadership, on top of the TOPY.AI MCP server.</strong></p>
  <p>
    <a href="https://www.npmjs.com/package/@topy-ai/ceo-skills"><img alt="npm" src="https://img.shields.io/npm/v/@topy-ai/ceo-skills?style=for-the-badge&color=ff1212" /></a>
    <a href="https://github.com/TOPY-AI-LTD/TOPY-AI-CEO-Skills/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-111827?style=for-the-badge" /></a>
    <a href="https://topy.ai/developers"><img alt="MCP" src="https://img.shields.io/badge/MCP-topy.ai%2Fmcp-0f172a?style=for-the-badge" /></a>
  </p>
  <p>
    <a href="#install">Install</a> ·
    <a href="#connect-topyai">Connect TOPY.AI</a> ·
    <a href="#how-the-skills-fit-together">How they fit</a> ·
    <a href="#packages">Packages</a> ·
    <a href="#repository-structure">Structure</a> ·
    <a href="#skills">Skills</a>
  </p>
</div>

---

[TOPY.AI](https://topy.ai) writes and maintains founders' business plans and keeps their CEO records:
decisions, risks, growth experiments, investors, GTM plans, research and the founder journal. These
skills teach Claude Code, Codex, Cursor, Gemini CLI, Pi and other agents to run that work the way a
good CEO would.

- **Core** (23, `topy-ai` plugin): connect, the goal tree and operating board, the daily brief and weekly review, milestones, KPIs and alerts, business plans,
  revisions and templates, investor-ready checks, SEIS Advance Assurance, and every CEO record. They
  use the TOPY.AI MCP server.
- **Strategy, fundraising, finance, operations, leadership** (28): decision memos, OKRs, user journeys, monthly close, plan vs actual, business
  models, pitch decks, term sheets, cap tables, financial models, unit economics, runway, hiring,
  board meetings, crisis response, debiasing and more. Most work without a TOPY account and offer to
  save the outcome to TOPY when it is connected.

Every change in TOPY takes two calls: a preview the agent shows you, then a confirmed call after you
say yes. Skills never confirm for you.

## Install

```sh
npx @topy-ai/ceo-skills install                  # this project, for the agents set up here
npx @topy-ai/ceo-skills install -g               # your user: every project
npx @topy-ai/ceo-skills install -g -a codex,pi   # pick the agents
npx @topy-ai/ceo-skills install --category fundraising,finance
npx @topy-ai/ceo-skills list                     # the catalogue
```

The core skills always come along. Supported agents: Claude Code, Codex, Pi, Cursor, Gemini CLI,
OpenCode, GitHub Copilot, Windsurf, Amp, Cline, Goose, Kiro, Qwen Code, Trae, Roo Code, Kilo Code,
Augment, Factory Droid, OpenHands and Antigravity. See the
[installer README](packages/skills/README.md) for folders, updates and removal.

Other ways:

- **Claude Code plugins**: `/plugin marketplace add TOPY-AI-LTD/TOPY-AI-CEO-Skills`, then
  `/plugin install topy-ai-all@topy-ai` (or one plugin, such as `topy-ai@topy-ai` with the MCP server).
- **Codex plugins**: `codex plugin marketplace add TOPY-AI-LTD/TOPY-AI-CEO-Skills`, then
  `codex plugin add topy-ai@topy-ai`.
- **Pi**: `pi install npm:@topy-ai/ceo-skills`.
- **By hand**: each skill is a self-contained folder with a `SKILL.md`; copy
  `plugins/<plugin>/skills/<id>/` into the folder your agent reads, or zip one and upload it in
  Claude.ai → Settings → Capabilities → Skills.

## Connect TOPY.AI

The core skills run on `https://topy.ai/mcp` (OAuth 2.1: sign in to TOPY.AI, no keys to paste).

| Client | How |
|---|---|
| Claude, ChatGPT (web, desktop) | add a custom connector with the URL `https://topy.ai/mcp` |
| Claude Code | `claude mcp add --transport http topy https://topy.ai/mcp`, or `npx @topy-ai/ceo-skills install --mcp` |
| Codex | `codex mcp add topy --url https://topy.ai/mcp` |
| Gemini CLI, Cursor, others with remote MCP | server URL `https://topy.ai/mcp` |
| Clients that only start a command | `npx -y @topy-ai/ceo-mcp` after `npx @topy-ai/ceo-mcp login`, or with `TOPY_API_KEY` |
| Terminal and scripts | `npm i -g @topy-ai/ceo-cli && ceo-cli login` |

Scheduled agents use the same one key (`TOPY_API_KEY`), mark their runs with the `X-Topy-Agent` header, and work
within a **standing permission** the founder grants in the chat: see the `topy-scheduled-agent` skill.

## How the skills fit together

```
topy-connect ─▶ topy-projects ─▶ topy-business-plan ─▶ topy-investor-ready ─▶ topy-plan-revision
                                        │                        │
                                        ▼                        ▼
                     strategy / finance skills        fundraising skills ─▶ topy-seis
                                        │
                                        ▼
       topy-decision-log · topy-risk-register · topy-growth-experiments · topy-founder-journal
                                        │
                                        ▼
                     topy-daily  ·  topy-weekly-review  ·  topy-scheduled-agent
```

A typical week: `topy-daily` each morning for the three things that matter; strategy and finance
skills when a decision comes up, with the outcome saved by `topy-decision-log`; `topy-weekly-review`
on Friday; `topy-plan-revision` when a figure, milestone or hire changes, so the whole plan stays
consistent; `topy-investor-ready` and the fundraising skills before a raise.

Try: *"Connect to TOPY.AI"*, *"What needs my attention as CEO today?"*, *"Is my plan investor-ready?"*,
*"Raise £250k instead of £200k across the whole plan"*, *"How much runway do we have?"*

## Packages

| Package | What it is |
|---|---|
| [`@topy-ai/ceo-skills`](https://www.npmjs.com/package/@topy-ai/ceo-skills) | these skills, installed into ~20 agents (`ceo-skills`) |
| [`@topy-ai/ceo-mcp`](https://www.npmjs.com/package/@topy-ai/ceo-mcp) | a local stdio MCP server for clients that only run local servers (`ceo-mcp`) |
| [`@topy-ai/ceo-cli`](https://www.npmjs.com/package/@topy-ai/ceo-cli) | TOPY.AI's AI CEO in the terminal (`ceo-cli`) |

All three use the same tools as `https://topy.ai/mcp`. API reference: [topy.ai/developers](https://topy.ai/developers).

## Repository structure

```
plugins/
  topy-ai/                 core skills + .mcp.json (Claude Code) and mcp.json (Codex)
  topy-ai-strategy/        topy-ai-fundraising/  topy-ai-finance/
  topy-ai-operations/      topy-ai-leadership/
  topy-ai-all/             bundle that depends on all six
.claude-plugin/marketplace.json     Claude Code marketplace
.agents/plugins/marketplace.json    Codex marketplace
skills.json                         machine-readable catalogue
packages/skills/                    the @topy-ai/ceo-skills installer
evals/                              prompts for checking the advisor skills
```

The skills are generated from a source catalogue kept next to TOPY.AI's MCP server; the build checks
every tool a skill names against the server's tool list. Please open an issue rather than editing a
`SKILL.md`.

## Releases

See [CHANGELOG.md](CHANGELOG.md). `v0.7.0` reorganised the catalogue into 42 skills in six plugins; `v0.8.0` added the operating records (51 skills);
`v0.7.1` named the packages `@topy-ai/ceo-cli`, `@topy-ai/ceo-mcp` and `@topy-ai/ceo-skills`.

## License

MIT © TOPY AI LTD. Privacy: [topy.ai/privacy](https://topy.ai/privacy).

## Skills

<!-- skills:start -->

**51 skills in 6 plugins**, plus the `topy-ai-all` bundle. Generated from the source catalogue: please open an issue rather than editing a `SKILL.md`.

### TOPY core (MCP) · `topy-ai`

| Skill | Tier | What it does |
|---|---|---|
| [`topy-alerts`](plugins/topy-ai/skills/topy-alerts/SKILL.md) | core | Set early-warning rules on KPIs in TOPY, work through the alerts they raise, and turn the serious ones into a corrective action, a risk or an incident. |
| [`topy-business-plan`](plugins/topy-ai/skills/topy-business-plan/SKILL.md) | core | Write a new TOPY.AI business plan (after a credit check), follow it to the end, then read, edit, fix and export it. |
| [`topy-connect`](plugins/topy-ai/skills/topy-connect/SKILL.md) | core | Connect an AI agent to TOPY.AI's AI CEO through the MCP server (OAuth, or the CLI / an API key without a browser) and pick the project to work on. |
| [`topy-customer-personas`](plugins/topy-ai/skills/topy-customer-personas/SKILL.md) | core | Keep the company's customer personas in TOPY — extracted from the business plan, corrected with evidence from research and customers, and compared to decide who to serve first. |
| [`topy-daily`](plugins/topy-ai/skills/topy-daily/SKILL.md) | core | The founder's daily brief on TOPY.AI, built from the operating board (goal health, stale KPIs, milestones due, overdue tasks) plus running plans and agent changes, in five lines or fewer and saved as a daily brief. |
| [`topy-decision-log`](plugins/topy-ai/skills/topy-decision-log/SKILL.md) | core | Record a founder's decisions in TOPY with context, options, rationale, confidence and a review date, and later review them against what actually happened. |
| [`topy-founder-journal`](plugins/topy-ai/skills/topy-founder-journal/SKILL.md) | core | Keep the founder's dated journal and the AI CEO's durable project memory in TOPY, and put each note in the right place so the CEO remembers facts without cluttering them with feelings. |
| [`topy-goal-tree`](plugins/topy-ai/skills/topy-goal-tree/SKILL.md) | core | Turn a founder's ambition into a North Star, up to three Company Goals and this quarter's Objectives with Key Results in TOPY, each with a KPI, an owner and a cadence. |
| [`topy-growth-experiments`](plugins/topy-ai/skills/topy-growth-experiments/SKILL.md) | core | Run growth experiments end to end in TOPY: a falsifiable hypothesis tied to a KPI and a journey stage, target fixed before launch, one owner, an honest read-out recorded as a KPI value, and a ship, kill or iterate call. |
| [`topy-gtm-plan`](plugins/topy-ai/skills/topy-gtm-plan/SKILL.md) | core | Build and keep the project's go-to-market plan in TOPY (positioning, channels, activation, retention, pricing, sales motion, funnel targets, launch), mapped to the stages of the customer journey, and hand plan-wide changes to topy-plan-revision. |
| [`topy-integrations`](plugins/topy-ai/skills/topy-integrations/SKILL.md) | core | Connect data sources (Stripe, QuickBooks, QuickFile, the cmo.so admin MCP) to TOPY in the chat, bind KPIs to them, and sync so actuals arrive on their own with their source. |
| [`topy-investor-ready`](plugins/topy-ai/skills/topy-investor-ready/SKILL.md) | core | Review a TOPY.AI business plan the way a seed investor would and list the five fixes that matter most, each with its section — then fix the ones the founder picks. |
| [`topy-investor-relations`](plugins/topy-ai/skills/topy-investor-relations/SKILL.md) | core | Keep a founder's investor pipeline and follow-ups in TOPY, draft the monthly investor update from the company's sourced numbers, and send it only with the founder's approval of text and recipients. |
| [`topy-milestones`](plugins/topy-ai/skills/topy-milestones/SKILL.md) | core | Create, track, complete and miss milestones in TOPY — product, revenue, funding, hire, launch and compliance deadlines — each tied to an objective with an owner, a due date and evidence. |
| [`topy-operating-board`](plugins/topy-ai/skills/topy-operating-board/SKILL.md) | core | Read the TOPY operating board and answer "how are we doing?" — objective health and why, stale KPIs, due and overdue milestones and tasks — with the next step for each red item. |
| [`topy-plan-revision`](plugins/topy-ai/skills/topy-plan-revision/SKILL.md) | core | Carry a change — a funding amount, price, milestone, KPI, hire or team change — through every affected section of a TOPY.AI business plan, consistently, as a new version. |
| [`topy-plan-templates`](plugins/topy-ai/skills/topy-plan-templates/SKILL.md) | core | Choose, copy, build and refine TOPY.AI business plan templates — official ones, the founder's own, AI-built from a requirement or a document — and set a project's defaults. |
| [`topy-projects`](plugins/topy-ai/skills/topy-projects/SKILL.md) | core | Create a TOPY.AI project from an idea or an existing website, keep its details right, explore and brainstorm ideas, and manage the media library. |
| [`topy-research-library`](plugins/topy-ai/skills/topy-research-library/SKILL.md) | core | Keep the research sources behind a project's business plan in TOPY, matched to the claims they support, with clean citations and no invented sources. |
| [`topy-risk-register`](plugins/topy-ai/skills/topy-risk-register/SKILL.md) | core | Keep the project's risk register in TOPY: score likelihood and impact, name an owner and a mitigation, review on a cadence, and close risks by status, never by deleting them. |
| [`topy-scheduled-agent`](plugins/topy-ai/skills/topy-scheduled-agent/SKILL.md) | core | Set up an agent that runs on a schedule (a daily brief, a weekly journal) on the founder's one TOPY.AI key and a standing permission, and keep it inside what the founder allowed. |
| [`topy-seis`](plugins/topy-ai/skills/topy-seis/SKILL.md) | core | Draft the answers for a UK SEIS Advance Assurance application from a TOPY.AI business plan, choose the right qualifying route, and list the documents HMRC expects. |
| [`topy-weekly-review`](plugins/topy-ai/skills/topy-weekly-review/SKILL.md) | core | The weekly operating review on TOPY.AI: record the week's KPI actuals with sources, read goal health from the board, settle the decisions that are due, and save a one-page weekly memo with next week's three priorities as tasks. |

### Strategy & direction · `topy-ai-strategy`

| Skill | Tier | What it does |
|---|---|---|
| [`topy-business-model`](plugins/topy-ai-strategy/skills/topy-business-model/SKILL.md) | connected | Maps how a startup creates, delivers and captures value on a business model canvas, checks that the pieces add up, and turns the riskiest assumptions into cheap, pre-registered tests. |
| [`topy-competitive-strategy`](plugins/topy-ai-strategy/skills/topy-competitive-strategy/SKILL.md) | connected | Reads competitor moves calmly, war-games the likely responses to a startup's own move, and identifies which defensible advantage the company can realistically build. |
| [`topy-decision-memo`](plugins/topy-ai-strategy/skills/topy-decision-memo/SKILL.md) | connected | Turns a hard founder call into a one-page decision memo with real options (including doing nothing), weighed trade-offs, a recommendation and the signals that would reverse it. |
| [`topy-market-entry`](plugins/topy-ai-strategy/skills/topy-market-entry/SKILL.md) | connected | Decides whether, where and how a startup should enter a new geography or customer segment: readiness, bottom-up sizing, entry mode, a beachhead, gated phases and kill criteria set in advance. |
| [`topy-okrs`](plugins/topy-ai-strategy/skills/topy-okrs/SKILL.md) | connected | Turns a startup's strategy into a few quarterly objectives with measurable key results, saved in TOPY as objectives linked to KR KPIs, then scores them at quarter end from recorded actuals and carries the lessons forward. |
| [`topy-prioritization`](plugins/topy-ai-strategy/skills/topy-prioritization/SKILL.md) | connected | Ranks a startup's competing initiatives against one goal and the team's real capacity using RICE, ICE or cost of delay, draws the cut line and writes down what the company will not do. |
| [`topy-scenario-planning`](plugins/topy-ai-strategy/skills/topy-scenario-planning/SKILL.md) | connected | Builds a small set of plausible futures around the uncertainties that matter most, tests the company's plans against each, and sets early-warning signals with responses agreed in advance; with TOPY, each scenario is saved as a financial scenario. |
| [`topy-user-journey`](plugins/topy-ai-strategy/skills/topy-user-journey/SKILL.md) | core | Map the customer journey for each persona in TOPY, tie every stage to a KPI and the experiments working on it, and find the stage where most customers drop out. |

### Fundraising · `topy-ai-fundraising`

| Skill | Tier | What it does |
|---|---|---|
| [`topy-cap-table`](plugins/topy-ai-fundraising/skills/topy-cap-table/SKILL.md) | connected | Keep the fully diluted cap table in TOPY and model dilution across rounds: SAFE/ASA and convertible conversion, option pool top-ups and the founders' ownership after each step, simulated without writing. Not legal or tax advice. |
| [`topy-data-room`](plugins/topy-ai-fundraising/skills/topy-data-room/SKILL.md) | connected | Build the due-diligence data room for a raise in TOPY: created from the plan in one step, completeness and red flags checked, shared per investor only with approval, and views tracked. |
| [`topy-fundraising-strategy`](plugins/topy-ai-fundraising/skills/topy-fundraising-strategy/SKILL.md) | connected | Decide whether to raise, how much, on what instrument, from which kinds of investor and when, tied to the milestones the money must buy and to TOPY's runway and cap table, saved as a planned round, with a fallback if the round is late. |
| [`topy-pitch-deck`](plugins/topy-ai-fundraising/skills/topy-pitch-deck/SKILL.md) | connected | Generate the 10-12 slide investor deck from the business plan in TOPY, review it slide by slide (one claim per slide, numbers that match the plan exactly) and export it as PPTX or PDF. |
| [`topy-term-sheet`](plugins/topy-ai-fundraising/skills/topy-term-sheet/SKILL.md) | connected | Read a startup term sheet in plain language: the economic and control terms, what they cost at real exit values and on the cap table (simulated in TOPY, never written), and the few points worth pushing on. Not legal advice. |

### Finance · `topy-ai-finance`

| Skill | Tier | What it does |
|---|---|---|
| [`topy-financial-model`](plugins/topy-ai-finance/skills/topy-financial-model/SKILL.md) | connected | Build a driver-based, three-statement-lite startup model (revenue build, headcount, costs, P&L, cash flow, simple balance sheet) with an assumptions sheet, scenarios and checks, saved in TOPY as financial scenarios with monthly projections. |
| [`topy-monthly-close`](plugins/topy-ai-finance/skills/topy-monthly-close/SKILL.md) | core | The founder's monthly close on TOPY.AI — last month's actuals recorded with their source, plan vs actual, runway at current pace and on plan, and a clear call on whether to reforecast or raise. |
| [`topy-plan-vs-actual`](plugins/topy-ai-finance/skills/topy-plan-vs-actual/SKILL.md) | core | Explain how far the company is from its business plan, which plan assumptions reality has broken, and turn that into a reforecast and a plan revision the founder approves. |
| [`topy-pricing-decisions`](plugins/topy-ai-finance/skills/topy-pricing-decisions/SKILL.md) | connected | Make the CEO-level pricing call: what to charge for, how to package it, whether to raise or cut prices, the break-even maths for each option, and a test plan saved as a decision and an experiment. |
| [`topy-runway`](plugins/topy-ai-finance/skills/topy-runway/SKILL.md) | connected | Measure burn and runway properly, check whether the company is default alive, and build a tiered cut plan with triggers so the founder decides early instead of in a panic. |
| [`topy-unit-economics`](plugins/topy-ai-finance/skills/topy-unit-economics/SKILL.md) | standalone | Work out what one customer is worth and costs to win: CAC, contribution margin, LTV, payback, net revenue retention and cohorts, then name the one thing to fix first. |

### Operations & people · `topy-ai-operations`

| Skill | Tier | What it does |
|---|---|---|
| [`topy-board-meetings`](plugins/topy-ai-operations/skills/topy-board-meetings/SKILL.md) | connected | Prepare and run a startup board meeting kept as a TOPY meeting record: the board pack generated from sourced numbers, a timed agenda, the asks, minutes, resolutions saved as decisions and actions saved as tasks. |
| [`topy-hiring-plan`](plugins/topy-ai-operations/skills/topy-hiring-plan/SKILL.md) | connected | Decide which roles to hire, in what order and when, what they cost against runway, and what each hire must achieve, with a scorecard per role; with TOPY each hire is saved as a hire milestone. |
| [`topy-kpi-dashboard`](plugins/topy-ai-operations/skills/topy-kpi-dashboard/SKILL.md) | connected | Choose the north-star metric, the input metrics that drive it and the guardrails, turn them into a weekly scorecard with owners, targets and red/amber/green rules, and with TOPY create them as KPIs and record their values. |
| [`topy-operating-cadence`](plugins/topy-ai-operations/skills/topy-operating-cadence/SKILL.md) | connected | Set the company's rhythm of weekly, monthly, quarterly and annual meetings, each with an owner, inputs, a timed agenda and the decisions it exists to make. |
| [`topy-org-design`](plugins/topy-ai-operations/skills/topy-org-design/SKILL.md) | standalone | Design a startup's structure as it grows: who owns which outcomes (DRI and RACI), reporting lines, spans of control and decision rights, plus how to roll the change out. |

### Leadership & decisions · `topy-ai-leadership`

| Skill | Tier | What it does |
|---|---|---|
| [`topy-ceo-advisor`](plugins/topy-ai-leadership/skills/topy-ceo-advisor/SKILL.md) | standalone | A general CEO decision advisor for cross-functional, ambiguous or board-level calls: frames the real question, compares options, checks bias, runs the numbers and ends in a recommendation, routing to narrower TOPY skills when one fits. |
| [`topy-crisis-response`](plugins/topy-ai-leadership/skills/topy-crisis-response/SKILL.md) | connected | Lead a company through a live crisis: classify severity, contain in the first hours, sequence who hears what and when, recover, and run a blameless review, kept as an incident record in TOPY with its alert, risk and decisions. |
| [`topy-debiasing`](plugins/topy-ai-leadership/skills/topy-debiasing/SKILL.md) | standalone | Stress-test a big call before committing: independent estimates, base rates, a pre-mortem, a red team, a bias scan and pre-set kill criteria, ending in an adjusted confidence. |
| [`topy-stakeholder-alignment`](plugins/topy-ai-leadership/skills/topy-stakeholder-alignment/SKILL.md) | standalone | Bring the people who matter along on a decision or change: map their power, interests and likely objections, choose the order to talk to them, and prepare each conversation. |

<!-- skills:end -->
