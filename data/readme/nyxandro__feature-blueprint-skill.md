<div align="center">

# Feature Blueprint

**A Claude Code skill that writes the feature spec and the implementation plan before your AI agent writes any code.**

[![Release](https://img.shields.io/github/v/release/nyxandro/feature-blueprint-skill)](https://github.com/nyxandro/feature-blueprint-skill/releases)
[![License](https://img.shields.io/github/license/nyxandro/feature-blueprint-skill)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-SKILL.md-6f42c1)](https://agentskills.io/specification)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-d97757)](#install)

**English** · [Русский](README.ru.md)

</div>

Feature Blueprint brings spec-driven development to Claude Code, Codex, OpenCode, Cursor and any
other agent that reads Agent Skills. You give it a rough feature idea. It studies your project,
looks up how others solved the same problem, and writes a spec with a PRD-style product part, a
technical design and a step-by-step plan with tests. Then it asks you only about the decisions
that change the product.

## Who it's for

People who build a product with AI agents and do not write or read the code themselves:
founders, product owners, solo builders, agencies. You bring an idea or a PRD and make only the
decisions nobody else can make. The agents design, build, test and ship. This way of working is
often called a dark factory, and Feature Blueprint is its first station: it turns your idea into
a spec the agents can build from without coming back to you.

Developers can use it too, but it is written for the person who decides what the product does,
not for the one who reads the code. Every decision comes in plain words, with its consequences
and a recommendation. That is where it helps most in our [benchmarks](#benchmarks).

## Why

Hand an AI agent a feature idea and it builds the happy path. Everything else gets filled in
quietly, and usually badly.

- An empty screen says "No data" and offers no next step.
- A spinner never stops.
- A customer gets charged twice after a double click.
- Nobody has ever restored from the backups.
- A sync stopped working a month ago and nobody noticed.

Feature Blueprint makes the agent think these through before the first line of code. It settles
what it can on its own and brings you the rest in plain words, each with a recommendation.

## Install

| Agent | Command |
|---|---|
| Claude Code, as a plugin | `/plugin install feature-blueprint --marketplace nyxandro/skills` |
| Claude Code, Codex, OpenCode, Cursor and others | `npx skills add nyxandro/feature-blueprint-skill` |
| Any agent, by hand | Download the [latest `.skill` archive](https://github.com/nyxandro/feature-blueprint-skill/releases/latest/download/feature-blueprint.skill) and unpack it into the agent's skills folder |

Pick one. If you install it two ways, Claude Code loads the skill twice.

<details>
<summary>More install options</summary>

<br>

- The one-line plugin install needs Claude Code 2.1.275 or later. On an older version, add the
  catalog first with `/plugin marketplace add nyxandro/skills` and then run
  `/plugin install feature-blueprint@nyxandro`.
- The catalog pins no version, so every commit here reaches plugin users as an update. Run
  `claude plugin marketplace update nyxandro` and `claude plugin update feature-blueprint@nyxandro`,
  or turn on auto-update under `/plugin` → Marketplaces.
- With `npx skills`, add `-g` to install the skill for every project. To install a given version,
  add its tag, as in `nyxandro/feature-blueprint-skill@v1.2.0`.
- You can also clone this repository and link the `feature-blueprint/` folder into your agent's
  skills folder. There is no build step.
- The research step needs web search and page fetching. The fresh-agent review needs a tool that
  starts subagents. Without them the skill still works and tells you what it could not check.

</details>

## Usage

Ask for a feature the way you would ask a colleague. These requests all start the skill.

- *Design two-way sync between the agent's reminders and Google Calendar.*
- *Plan a CSV product import for the admin panel and write the spec.*
- *Work out nightly database backups. How much data can we lose, and how do we restore?*
- *Here's the client's chat and brief. Design appointment rescheduling for our Telegram bot.*
- *Check this feature plan for holes.*

The skill stays out of the way when you only want to talk an idea through. Small changes like a
new button or a clear fix skip the spec entirely. The agent says in a few lines what it will
change and does it.

## How it works

```mermaid
flowchart LR
    A[Idea and materials] --> B[Reads the project]
    B --> C[Research]
    C --> D[Draft spec and plan]
    D --> E[Fresh-agent review]
    E --> F[One message with your decisions]
    F --> G[Build]
```

1. The agent reads what you gave it and then your project. It looks at how similar things
   already work, how much data there is and who keeps it running. It doesn't ask what the code
   can answer, and it never touches production while designing.
2. It looks up how others solved the same task in official docs, engineering blogs, postmortems
   and popular repositories. For every practice it notes the scale at which it starts to pay off.
3. It writes the whole draft before asking anything, unless a single answer would flip most of
   the design.
4. It picks the simplest option that meets your goals at your project's size, and writes down
   when it would be worth moving up.
5. It checks the draft, then hands it to a fresh agent that has never seen the conversation and
   reads it as the person who has to build it.
6. It saves the spec in `docs/specs/` and sends you one message with the open decisions. If your
   answers don't change the plan, that counts as a go and the agent starts building.

There is also a review mode. Bring an existing plan or pull request and you get the gaps, worst
first. On request the agent also draws HTML mockups of every screen state and diagrams of the
flows.

## Example

Every decision that's yours comes with a real situation, the options and a recommendation. Here
is one from a booking bot for a barbershop.

> **F2. Can a client move an appointment shortly before it starts?**
>
> Oleg is booked for 18:00 with Anna. At 17:20 he moves the visit to tomorrow, and Anna is left
> with a 40-minute gap that nobody can book at such short notice. This affects the barbers' income
> and how strict the shop wants to be. The code works either way.
>
> **A. Free moves until 2 hours before, later only through the admin.** Barbers lose fewer slots.
> At 17:20 Oleg sees "Less than 2 hours left, so the bot can't move this visit. Message the admin
> at @barber_admin." It adds one check and one message, and some clients won't like it. The 2
> hours is a single setting.
>
> **B. Free moves at any time.** Easiest for clients. Barbers lose last-minute slots.
>
> **I recommend A.** The shop already asks for 2 hours' notice on phone bookings
> (`docs/rules.md`), so clients know the rule. If nobody decides, the agent goes with A.

## What's in the spec

| Part | Written for | What's inside |
|---|---|---|
| At a glance | You | What we build and why, how it will work, what to watch, decisions waiting for you, scope in hours |
| For the owner | You | Goals and non-goals, what the design rests on, options compared, scenarios, your decisions |
| Behaviour | The implementing agent | Screen and message states, errors with their full texts, edge cases, how background jobs fail and recover |
| How to build | The implementing agent | What to reuse, the design, steps with tests, acceptance criteria |

The skill itself is written in English. The spec, the questions and the summaries come in the
language you write in.

## What it covers

| Features people use | Internal mechanisms |
|---|---|
| Web apps and admin panels, sites and online shops, mobile and desktop apps, Telegram and other bots, Mini Apps, AI features and agent tools, voice interfaces, CLIs, APIs and webhooks | Backups, sync with external services, queues and background jobs, data migrations, monitoring, integrations |

## Works well with

[Owner Decisions](https://github.com/nyxandro/owner-decisions-skill) keeps your decisions from
all projects in a private base and answers a question the way you already answered a similar
one. Feature Blueprint asks you about every decision that changes the product. With both
installed, the forks you have already settled elsewhere are taken from the base and do not reach
you again, the agent's own decisions follow what you decided before, and your new answers go
back into the base. So each design asks you less than the one before.

Neither skill needs the other. Feature Blueprint only checks whether the environment keeps your
earlier decisions and works the same when it does not.

## Benchmarks

We measured the skill against Superpowers and against the same model with no skill: four
features, three runs of each, Opus 5.5 in Claude Code, a blind judge.

| Across 4 features | Feature Blueprint | No skill | Superpowers |
|---|---|---|---|
| The owner can understand it and decide, of 96 checks | **92–94** (96–98%) | 44–45 (46–47%) | 47–51 (49–53%) |
| Problems handled before code, of 144 | 131–135 (91–94%) | 130–131 (90–91%) | 118–122 (82–85%) |
| Serious technical errors in 12 runs | 3–6 | 5–6 | 11–12 |
| Cost of one design at API list price | $1.9–3.9 | $0.35–0.8 | $0.5–1.3 |
| Time of one design | 8–15 min | 2–5 min | 3–6 min |

Each range spans the judge's two passes.

- **The clearest gain is a spec you can decide on without reading code.** With the skill, every
  decision left to you came as a question with options, consequences and a recommendation in 23
  of 24 checks. Without it, that happened in 0 to 2. Costly or irreversible consequences were
  named in 24 of 24 checks, against 5 of 24.
- **Opus 5.5 alone already handles most problems.** On the two user-facing features the plain
  model handled 93–94% of them, so the skill adds little coverage there. It adds the most where
  documentation matters: Ozon's API limits were handled in 6 of 6 checks with the skill and in 2
  of 6 without it.
- **Fewer wrong technical decisions on user-facing features.** The skill made no serious error
  there in 6 runs. Without it, a double-booking guard that PostgreSQL rejects at migration showed
  up in 1 of 3 plain runs and all 3 Superpowers runs. On internal mechanisms this edge is gone:
  3–6 subtle errors in 6 runs with the skill against 3 without it. One example is a cron line
  for the first Sunday of the month that also fires on every other Sunday.
- **It costs 4–5 times more and takes about 3 times longer:** about $2–4 and 8–15 minutes per
  feature at list price.

These numbers are for versions 1.0.0 and 1.1.0. Version 1.2.0 adds three fixes aimed at the weak
spots above. The fresh-agent review now also questions claims about how platforms and settings
behave, the message to you carries the whole "At a glance", and an external service's raw error
never reaches people. These fixes have not been measured yet.

<details>
<summary>How we measured</summary>

<br>

- **Features.** Rescheduling in a Telegram booking bot, from a raw idea with no code. A weekly
  import of a 3,000-item price list into a small shop admin, with the project's code. Stock and
  price sync with the Ozon marketplace in the same shop. Backups of a shop that runs on one VPS.
- **Arms.** Feature Blueprint 1.0.0 on the first two features and 1.1.0 on the other two; the
  only difference is the removed length limit. Superpowers 7.0.2. Opus 5.5 with no skill. Each run
  is an isolated `claude plugin eval` session with no user settings, CLAUDE.md or other skills,
  and no shell.
- **The same ending in every request:** the owner is away, so decide on your own, collect the
  questions at the end and write no code. This keeps the arms comparable, but it is not how
  Superpowers is meant to be used. When the user opts out of questions, its own rules turn its
  design dialogue off. Superpowers in live dialogue was not measured.
- **Grading.** Before any run, an isolated agent that saw only the request and the project files
  wrote 12 problems per feature that a good design must handle. It also wrote 8 general criteria
  for an owner who does not write code. The judge, Opus 5.5 in an isolated session, saw the
  submissions with skill names removed, shuffled, three at a time with one from each arm. It
  graded every item pass or fail with a quote. Two passes in different orders agreed on 96% of
  verdicts (690 of 720).
- **Not measured:** the code built from the specs, weaker models, Compound Engineering,
  Superpowers in live dialogue, real owners reading the specs.
- Cases, criteria and the runner are in [`feature-blueprint/evals/`](feature-blueprint/evals/README.md).
  Measured on 2026-11-06 with Claude Code 2.1.318 and 2.1.319.

</details>

## Versions

The current version sits in `metadata.version` of `feature-blueprint/SKILL.md`, so any installed
copy tells you which one it is. Every version has a git tag and a
[release](https://github.com/nyxandro/feature-blueprint-skill/releases) with its own archive.
[CHANGELOG.md](CHANGELOG.md) lists what changed.

<details>
<summary>Repository layout</summary>

<br>

```text
feature-blueprint/                    the skill
  SKILL.md                            principles and the order of work
  references/document-template.md     the spec format, plan included
  references/checklists.md            what not to miss, and the self-check
  references/examples.md              good and bad decisions, summaries and plan steps
  references/review-mode.md           finding holes in a ready plan or PR
  references/builder-check.md         the prompt for the fresh-agent review
  references/mockups.md               HTML mockups and diagrams, on request
  evals/                              cases that compare the skill with others, not in the archive
dist/feature-blueprint.skill          the skill folder as a downloadable archive
CHANGELOG.md                          what changed in each version
README.md, README.ru.md               this page in English and in Russian
```

</details>

<details>
<summary>Credits</summary>

<br>

The skill is written from scratch, with ideas from these open projects.

- [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)
  (MIT). Build an unrequested mechanism only when its absence harms quietly or is costly to add
  later. Check what two decisions do together and check claims about the project against the
  code. Look at earlier attempts and unwritten rules of the code. Keep production safe after each
  step that ships on its own. Separate the goal from the means and ask how a feature could be
  built as written and still miss the goal.
- [obra/superpowers](https://github.com/obra/superpowers) (MIT). Study the project before asking,
  review the document with a fresh agent, the plan format, rules every step keeps.
- [garrytan/gstack](https://github.com/garrytan/gstack) (MIT). The states table, open decisions
  with what happens if nobody decides, failures on new paths.
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0). Propose the likely
  option and ask for corrections, the edge-case checklist, kinds of empty states.
- [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills) (MIT). The
  error-handling chain, comparing options by behaviour.
- [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD). Scenarios with real
  people, the section on what we deliberately leave out.
- [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
  (Apache-2.0). Goals and non-goals, priorities P0 to P2, acceptance criteria.

Research, scale and reliability rules draw on
[Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/),
[Choose Boring Technology](https://mcfunley.com/choose-boring-technology) and the
[AWS Well-Architected reliability pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-principles.html).
Rules for AI agent tools follow Anthropic's
[Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents),
OpenAI's [function calling guide](https://developers.openai.com/api/docs/guides/function-calling)
and the [MCP tools spec](https://modelcontextprotocol.io/specification/2025-11-25/server/tools).

The shape of the skill follows Anthropic's
[skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
the [Agent Skills specification](https://agentskills.io/specification), OpenAI's
[Build skills](https://learn.chatgpt.com/docs/build-skills) and the chapters on Agent Skills and
clarifying requirements in Bojie Li's book "AI Agents from the Inside".

</details>

## License

[MIT](LICENSE)
