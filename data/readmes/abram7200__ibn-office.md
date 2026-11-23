<div align="center">

# IBN Office

**Your AI agents, working as one office.**
A Manager plans, a Deputy checks, a Secretary records, and every AI agent on your computer gets a desk —
with a live 3D office that shows who is doing what, how far along it is, and how long is left.

[![CI](https://github.com/abram7200/ibn-office/actions/workflows/ci.yml/badge.svg)](https://github.com/abram7200/ibn-office/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![Free-First](https://img.shields.io/badge/Free--First-no%20silent%20paid%20calls-success)
[![GitHub stars](https://img.shields.io/github/stars/abram7200/ibn-office?style=social)](https://github.com/abram7200/ibn-office/stargazers)
[![Discussions](https://img.shields.io/github/discussions/abram7200/ibn-office?label=discussions)](https://github.com/abram7200/ibn-office/discussions)
[![Built with Claude Code](https://img.shields.io/badge/built%20with-Claude%20Code-d97757?logo=anthropic&logoColor=white)](https://claude.com/claude-code)
[![Reviewed with Codex](https://img.shields.io/badge/reviewed%20with-Codex-412991?logo=openai&logoColor=white)](https://github.com/openai/codex)

![The IBN Office, live](docs/media/office-live.gif)

[![▶ Watch the tutorial on YouTube](docs/media/tutorial-thumbnail.jpg)](https://www.youtube.com/watch?v=BGL2drP4qLQ)

**▶ [Watch the 4½-minute tutorial on YouTube](https://www.youtube.com/watch?v=BGL2drP4qLQ)** (narrated, with chapters)

[**Explainer page**](https://abram7200.github.io/ibn-office/) · [Guide for daily use](docs/GUIDE.md) ·
[Every feature explained](docs/FEATURES.md) · [How it works inside](docs/ARCHITECTURE.md) · [Commands](docs/COMMANDS.md) · [Install (for your agent)](INSTALL_FOR_AGENTS.md)

**🚀 [Install with one paste](INSTALL_PROMPT.md)**: copy one prompt into Claude Code or Codex and walk away

*Created by **Ibram** · free and open source (MIT)*

**⭐ If IBN Office saves you time, star the repo — it helps other engineers find it.**

</div>

---

## In one minute

You probably already have one or more AI agents on your computer: Claude Code, Codex, OpenCode, Gemini, Qwen…
Each one is smart, but on its own it:

- works alone, with nobody checking its work;
- forgets what you corrected yesterday;
- uses the biggest, most expensive model even for a small task;
- stops when its quota runs out;
- gives you a "done" that is sometimes not done.

**IBN Office turns them into a team.** It does not replace your agents: it organises them. You keep typing to your
agent as usual. The Office works behind it, on every message, with no trigger word.

| Without IBN Office | With IBN Office |
|---|---|
| One agent answers alone | The **Manager** plans, workers do the parts, the **Deputy** checks with fresh eyes, the **Secretary** records |
| You repeat the same corrections | Your corrections become **owner notes**, applied to every later request, in every project |
| "Done" means the agent says so | "Done" means a **check passed**: tests, the expected result, coverage of every record |
| Every task gets the biggest model | Small tasks go to **small models / low effort**; hard tasks to strong ones. Fewer tokens, same quality |
| Quota runs out → work stops | The agent **switches to its next model**; a hard task only goes to a model strong enough for it |
| Similar work is solved from scratch | The **cabinet** remembers solved cases: a 70%-similar task reuses the plan and costs less |
| You can't see what is happening | A **live 3D office**: desks, step *x of y*, % done, time left, who hands work to whom |

## What you see

<table>
<tr>
<td width="50%"><img src="docs/media/office-overview.jpg" alt="Dashboard with the 3D office"></td>
<td width="50%"><img src="docs/media/office-wall.jpg" alt="Close-up: Manager, Deputy, Secretary and the workers"></td>
</tr>
<tr>
<td><b>The dashboard.</b> Every mission with its %, step x of y and time left; the 3D office below.</td>
<td><b>The team.</b> Name tags above each robot; the Manager, Deputy and Secretary in the middle; workers at their desks.</td>
</tr>
</table>

What moves in the office is **real state**, read from the Office's own records every second:

- **A task goes out:** a task card flies from the Manager to the agent's desk.
- **The agent works:** it sits at its desk facing its two screens; code scrolls on the screens while it types.
- **It finishes:** it swivels its chair, stands up, carries the result to the Deputy, and the Deputy takes it with a nod.
- **You leave a note:** a yellow sticky note flies into the cabinet; the *Owner notes* drawer slides open, takes it and closes.
- **A case is learned:** a blue folder goes from the Secretary into the *Cases* drawer.
- **Progress:** a ring above each working agent fills with its real %; it turns amber near its time budget and red over it.
- **The mission wall** shows every mission, its %, the time left, and **how much of the solution was reused, taken from
  GitHub, or invented**. The **task board** shows the steps; the **pin board** shows your latest notes; the **server rack**
  has one light per provider (green up, amber slow, red down). The **wall clock** is your PC's time; idle agents take a
  coffee break.
- **More agents, bigger office:** when a new agent is installed, a desk is added and the room grows. Empty desks wait,
  with no "not found" labels.

## The team

| Role | Who plays it | What it does for you |
|---|---|---|
| **Manager** | your strongest agent (Claude Code or Codex) | Reads your request and your notes, writes the plan: the expected result, how it will be checked, the steps, which agent does each step, and which steps can run in parallel. |
| **Deputy** | another agent, or the same one at another level | Checks the work with fresh eyes ("Goldfish" reviewers who see only the work, not the excuses), and receives every finished part. |
| **Secretary** | another agent | Keeps the records: what was asked, done, checked and fixed, what it cost, your notes, the six project files. |
| **Workers** | every other agent on your PC | Do the steps they are given, each with the model and effort that fits the step. |
| **The Office** | IBN Office itself | Runs the loop, measures time and tokens, keeps the chain of records that cannot be silently changed. |

## The methods inside (in plain words)

- **Elephant and Goldfish.** The *Elephant* (Manager) remembers everything about the task. The *Goldfish* reviewers
  start fresh every time and see only the result, so they catch what a tired author would miss.
- **Ponytail.** Every finding is sorted into **Must fix**, **Should fix** and **Nice to have** — and *all three are done*,
  in an order that avoids conflicts (one after another when they touch the same file, in parallel when they don't).
  Every finding is answered "fixed" or "not a real problem, because…" — never just accepted as a risk.
- **Solution order.** First use what already exists on your PC (tools, skills, libraries); then look on GitHub; only then
  invent — from first principles. Each mission reports this as numbers, for example
  *65% reused · 25% from GitHub · 10% invented*, with what each part was.
- **Control loop.** Measure → compare with the target → correct → measure again, instead of a single attempt.
- **Dish Pong.** When something misses, the cause is found and only that part is changed.
- **Cause and effect matrix.** Every miss is written as WHERE / WHAT / WHY / HOW, so it is not repeated.
- **Coherence.** When one file changes, the files that build on it are re-read and brought to the same level before
  delivery — no new engine in an old body.

## Everything inside — in one line each

Full explanations, with how each one works: **[docs/FEATURES.md](docs/FEATURES.md)**.

| Feature | What it does for you |
|---|---|
| **Sub-tasks** | A worker can split a big step into up to 6 linked sub-tasks on other agents/models (one more level at most). Sub-tasks only read; the parent writes — so they never clash. |
| **The router** | Every step gets the right agent and model level (light / standard / strong). A step that keeps failing is escalated by itself. With one agent, the split happens across its own models and effort levels. |
| **Owner notes** | Your corrections and rules are caught from any message, in English or Egyptian Arabic, and pinned for every later request, project and chat. The plan must answer each one by id. |
| **Elephant & Goldfish** | The Manager remembers everything; reviewers start fresh and see only the work. A planted "canary" proves they did not see the chat. |
| **Ponytail** | Must fix, Should fix, Nice to have — all done, each answered "fixed" or "not real, because…", scheduled without conflicts. |
| **No hallucination** | Fixed result format, a checker per job, and the Office's own truth check: claims vs what really changed on disk, independent re-run, tamper-evident record. |
| **No laziness** | The plan lists how a worker could cheat; reviewers are calibrated with a planted error first; done means *every* record is covered; direct agent calls behind the Office's back are blocked. |
| **Control loop · Dish Pong · matrix** | Measure, compare, correct; change only the part that missed; write every miss as WHERE / WHAT / WHY / HOW. |
| **Solution order in numbers** | Each mission shows how much was reused, taken from GitHub, or invented. |
| **Learning cabinet** | Verified cases are reused at 80%+ similarity and adapted at 50–80%; the token and time saving is measured. |
| **Coherence** | Files that build on a change are re-read and brought to the same level before delivery. |
| **Manager oversight** | Step x of y, % and time left from measured durations, budgets with a safety factor, a reason when a step is slow, steering mid-step. |
| **Provider health** | Down or rate-limited hosts are detected and paused; work goes elsewhere. |
| **Quota failover · Free-First** | Next model when one runs out; never a weak model for a hard step; never a silent paid call. |
| **Always on** | Starts with the PC, works on every message through hooks; every firing is logged. |
| **Goal loop + watcher** | One goal, a bounded loop and a watcher every 3 min: stopped hangs and orphan helpers, stalled goals and silent agents raised in every chat (the ibn-goal-loop-watcher kit, built in). |
| **IBN connected** | When IBN is on the PC, every plan asks IBN's brain first (`ibn-brain find`), then GitHub, then new code. |
| **Hook doctor** | Hook commands that run in every shell (Git Bash, cmd, PowerShell), proved in each one at setup, and every chat checked for its hook lines: a chat that skipped the Office raises an alarm with the fix. |
| **One shared toolbox** | One set of skills, tools, libraries, MCP servers and hooks for all agents — tools instead of tokens. |
| **Six project files** | GOAL, CORE_IDEA, TASK, TASKS, WORKING_PROGRESS, OWNER_NOTES — always current. |
| **Proof** | `office.py proof`, `SETUP_PROOF.md`, and an evaluator (90 probes, 540-run matrix, 44/44 mutants caught). |

## What it detects by itself

On a fresh computer, the installing agent runs one command and IBN Office finds:

- **Agents:** Claude Code, Codex, OpenCode, Gemini CLI, Qwen Code, Cursor agent, Copilot CLI, Aider, Goose, Crush,
  Hermes Agent, AlphaCode — and any agent installed **later** (it re-scans every 30 seconds and adds a desk).
- **Your machine:** hardware, programs, skills, libraries, MCP servers, hooks.
- **Older systems** (an earlier agent pool, office or task router): it adopts, bridges or leaves them alone — never
  overwrites them.
- **Each agent's models and their quotas**, so it can switch model when one runs out.

## Four free helpers (optional)

IBN Office can come with four free tools. The installing agent first checks which ones you already have —
*"I found 2 of 4 on your PC; 2 can be added"* — and asks you which to add (type `1 3`, `all`, or `none`). Nothing you
already have is reinstalled or overwritten; any config it touches gets a dated backup.

| # | Helper | What it gives you | Free use |
|---|---|---|---|
| 1 | [OpenCode](https://opencode.ai) | an open-source coding agent | its free Zen models, no key |
| 2 | [FreeLLMAPI](https://github.com/tashfeenahmed/freellmapi) | one local address for the free plans of many AI providers, with automatic fallback | works with **no key** (no-account providers are switched on for you); every free key you add gives more |
| 3 | [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Nous Research's agent with tools and skills | runs on FreeLLMAPI's free models |
| 4 | [AlphaCode](https://github.com/dragonked2/alphacode) | a fast terminal coding agent | its built-in free lane, no key |

After installing, each one gets a **real test** (a one-line prompt that must answer). You get `COMPANIONS_GUIDE.md`
in plain words: what each tool does, its state, the links where you create free keys, and where to paste them. A
FreeLLMAPI login is created for you in a private file — sign in and change the password.

## When a model's quota runs out

Many agents reach several models, each with its own quota (OpenCode, FreeLLMAPI, Antigravity, Claude Code…).
When one answers "quota reached":

1. that model is marked out until its reset — the time is read from the provider's own message
   ("refreshes in 4 hours, 59 min"); models that share one quota go out together;
2. the same agent continues with its **next model that is strong enough** for the job — and that retry is not held
   against the agent;
3. **a hard job never goes to a weak model.** If the agent has nothing strong enough left, it takes a lighter job it can
   do, and the hard job goes to another agent that fits — a worker, or the Deputy, Secretary or Manager;
4. if no agent fits right now, the job waits with the earliest reset time while the rest of the work goes on.
   The work never stops, and it never drops below the strength it needs.

A stronger model may take a lighter job, at lower effort, so tokens stay low. Paid models are never used silently
(Free-First).

## Daily use

You don't run anything special. Open your agent and work as usual:

1. You type a request. The Office adds your notes, its status, and any similar past case to your agent's context.
2. If you correct it ("no, always put the legend under the title block"), that becomes an owner note — kept for good.
3. Bigger work becomes a **mission**: plan → check the plan → do the parts → check the result → polish → deliver.
   Watch it on the dashboard (desktop shortcut **IBN Office**).
4. Every project gets six files, always current: `GOAL.md`, `CORE_IDEA.md`, `TASK.md`, `TASKS.md`,
   `WORKING_PROGRESS.md`, `OWNER_NOTES.md`.

More in the [daily guide](docs/GUIDE.md).

## Install

**Easiest: one paste.** Open Claude Code or Codex, paste the prompt from **[INSTALL_PROMPT.md](INSTALL_PROMPT.md)**,
change the first line to your name, and walk away. It creates an `IBN OFFICE` folder (on a drive other than C: when
there is one), clones this repo, installs everything including the four free helpers, fixes every Ponytail finding,
runs the full final test, makes the Office start with your computer, puts **IBN Office** on your desktop and opens
the live 3D office. It asks you nothing; it stops only for a click that has to come from you.

**Or** give this folder to your agent (Claude Code or Codex) and say:

> Read `INSTALL_FOR_AGENTS.md` and install IBN Office on this computer.

It checks Python, profiles the machine, finds your agents and older systems, installs the hooks for every project,
runs the tests, asks you about the four helpers, puts **IBN Office** on your desktop, and writes `SETUP_PROOF.md` with
the evidence of each step. Manual install, for the curious:

```bash
python ibn_setup.py --owner "YOUR NAME"      # everything above, with a proof file
python companions.py menu                     # the four optional helpers
python office.py proof                        # facts: hooks fired, missions run, notes applied, models used
python hooks_doctor.py check                  # hooks in place, working in the agents' shells, used by every chat
```

Requirements: Python 3.10+. For the helpers: Node.js 20+ and Git (the installer tells you if they are missing).

## What has been tested

- 128 automated tests (Pool, Office, evidence, quota failover, helpers, hook doctor, goal loop, IBN link) on Linux / Python 3.13; web tests on Node 22.
- The evaluator: 90 probes, a 540-run scenario matrix with crash-and-resume, and 44 of 44 code mutants caught.
- The four helpers were installed for real on a clean Linux home and each answered a prompt on free models.
- **Fresh-clone test:** `git clone` of this repo on a clean Linux home → `ibn_setup.py` 11 of 12 steps PASS (the live
  agent step is skipped by design: Free-First), dashboard up, a demo mission accepted, an Arabic correction captured as an
  owner note by the prompt hook, and OpenCode, FreeLLMAPI (no key), Hermes and AlphaCode all answering on free models.

**Not yet verified:** Windows and macOS end to end (the code supports them; CI runs Windows as experimental), and
every agent CLI with real accounts. See [SECURITY.md](SECURITY.md) for how to report a problem.

## FAQ

**Do I need to know programming?** No. Your agent installs it; you use your agent as before and watch the dashboard.

**Does it cost money?** IBN Office is free. It never starts paid API calls by itself. Your own agent subscriptions are
used as you already use them — just more carefully (small models for small steps).

**Does it change my existing setup?** No. Nothing is deleted or overwritten. Configs it merges get a dated backup.

**Can I remove it?** Yes: `python install_manager_contract.py --user --remove` (and `--project PATH --remove` for a project), then delete the folder.

**Is my data sent anywhere?** No. Everything stays on your PC; agents talk to the providers you already use.

## Team, credits and the projects it stands on

| | Who | Role |
|---|---|---|
| <img src="https://github.com/abram7200.png" width="48"> | **[Ibram](https://github.com/abram7200)** | creator · architecture · the engineering vision |
| 🤖 | **[Claude Code](https://claude.com/claude-code)** (Anthropic) | AI pair programmer: code, tests, docs, the 3D office (co-author on the commits) |
| 🤖 | **[Codex](https://github.com/openai/codex)** (OpenAI) | AI reviewer during development; one of the agents IBN Office runs |
| 🧭 | **ibn-goal-loop-watcher kit** (Ibram, part of IBN) | the goal + bounded loop + watcher rules, shipped in `goal_loop/` |

IBN Office would not exist without these open-source projects — please star them too:

| Project | What IBN Office uses it for |
|---|---|
| [**OpenCode**](https://github.com/anomalyco/opencode) | a free coding agent at its own desk; free Zen models |
| [**FreeLLMAPI**](https://github.com/tashfeenahmed/freellmapi) | one local endpoint over the free tiers of many providers |
| [**Hermes Agent**](https://github.com/NousResearch/hermes-agent) | Nous Research's agent, running on FreeLLMAPI's free models |
| [**AlphaCode**](https://github.com/dragonked2/alphacode) | a terminal coding agent with a built-in free lane |
| [**Ponytail**](https://github.com/DietrichGebert/ponytail) | the review discipline: Must / Should / Nice to have, all done |
| [**Elephant–Goldfish Model**](https://github.com/google/elephant-goldfish-model) | the fresh-eyes reviewer personas |
| [**agent-office**](https://github.com/ignitrondev/agent-office) · [**whatsmyagentdoing**](https://github.com/Charonyuu/whatsmyagentdoing) · [**Three.js**](https://github.com/mrdoob/three.js) | the live office view and agent activity |

## Join in

- 💬 **[Discussions](https://github.com/abram7200/ibn-office/discussions)** — show your setup, ask, propose ideas.
- 🟢 **[Good first issues](https://github.com/abram7200/ibn-office/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)** — small, well-described tasks to start with.
- 🧩 **Add an agent:** if your favourite agent CLI is missing, one entry in `agent_discovery.py` gives it a desk.

[![Star History](https://api.star-history.com/svg?repos=abram7200/ibn-office&type=Date)](https://star-history.com/#abram7200/ibn-office&Date)

## Contributing

Ideas and fixes are welcome — read [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md);
the PR form ([.github/pull_request_template.md](.github/pull_request_template.md)) asks for the solution order and the
checks. What changed in each release: [CHANGELOG.md](CHANGELOG.md).

## Credits

Created by **Ibram**. IBN Office builds on open-source work — Ponytail, Elephant–Goldfish, agent-office,
whatsmyagentdoing, Three.js, and the four helpers — see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Licensed under the [MIT License](LICENSE). Free for everyone.
