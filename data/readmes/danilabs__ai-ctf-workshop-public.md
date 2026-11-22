# AI CTF Workshop — build your own harness on OpenCode

Workshop materials for a hands-on lab where you build a CTF harness on top of
[OpenCode V2](https://opencode.ai/docs/): scope rules, an agent, commands,
skills, permissions, subagents, guard plugins, and the measurements that prove
the thing works.

The point of the lab is that **you write the harness**. This repository is a
minimal skeleton: the config, guards, vendored skills and targets allowlist are
here, but no agents or commands are shipped — you build those yourself, then
compare against the notes in `HARNESS.md`.

Targets OpenCode **V2** (verified with `opencode v2.3.0`). The V1 plugin API
will not load.

---

## Start here

| If you are… | Open |
| --- | --- |
| Attending the 70-minute lab | [`workshop.html`](workshop.html) in a browser |
| Building your harness during the lab | [`skeleton/`](skeleton/README.md) (or this repo as the starter) |
| Building the harness step by step | [`HARNESS.md`](HARNESS.md) |
| Reading the configuration reference | [`.opencode/README.md`](.opencode/README.md) |
| Looking up one concept | [`docs/`](docs/) |

`HARNESS.md` is the written build guide: twelve steps. Most end with a
**Verify** command and a **Compare** pointer to the reference file; the writing
itself is yours.
`workshop.html` is the same material as a slide deck with a checkpoint after
each step. Steps 9 and 12 of the guide are homework.

---

## Repository status

This is a minimal skeleton, not a complete reference kit. **This checkout is
partial:** the config, providers, plugins and vendored skills are here;
several answer-key files are still `TODO` placeholders or absent. The kit
ships no agents or commands — you build those yourself. Nothing below claims
otherwise.

Present and usable:

- `skeleton/` — minimal starter: `AGENTS.md`, a two-model config, agent,
  command and skill templates, an empty guard plugin, and `targets.json`.
- `.opencode/opencode.jsonc` — OmniRouter provider, eight model entries (seven
  active), permissions, policies, compaction and CTF-specific switches. No
  agents or commands are shipped: you build them during the workshop
  (HARNESS.md steps 3–4).
- `.opencode/plugins/challenge-guard/` — denies `edit`/`write`/`patch` outside
  the start folder and inside `files/`.
- `.opencode/plugins/scope-guard/` — denies `shell`/`webfetch` to hosts not in
  `.opencode/targets.json` (fail closed).
- `.opencode/targets.json` — empty allowlist with loopback enabled.
- `.opencode/skills/vendor/ctf-skills/` — 12 vendored skills (MIT).

Placeholders or missing (see [What is missing](#what-is-missing-and-todo)):

- `.opencode/skills/ctf-methodology/SKILL.md` is literally `TODO`.
- `AGENTS.md`, `install.sh`/`install.ps1`, `pricing.json`, the sample `CTF/`
  event, and every script under `.opencode/scripts/` (the directory exists but
  is empty).
- No agents or commands are shipped in `.opencode/` (or in `skeleton/` beyond
  TODO templates): build them yourself per HARNESS.md steps 3–4.

So: the kit can be inspected and its guards reviewed, but a full solve
loop needs the pieces you build in `HARNESS.md` steps 1–11 first.

---

## Quick start

Requirements: OpenCode V2, a router key (`OMNIROUTER_API_KEY`, from the
instructor), and a challenge folder.

```sh
opencode --version                        # must be V2
export OMNIROUTER_API_KEY="sk-..."        # in the shell that starts OpenCode
```

Do not put the key in a file. The provider reads it from the environment
(`providers.omnirouter.env`).

### Try the model alone (guide step 2)

From this repository root:

```sh
opencode models            # should list omnirouter/beam-free, longcat-2-5-free, …
opencode run "say hello"   # one prompt, no agents or commands needed
```

The default is `omnirouter/beam-free`, a free-tier model. If it is rate
limited, switch with `/models` or:

```sh
opencode run --model omnirouter/longcat-2-5-free "say hello"
```

### Work on a challenge

The intended layout is one folder per challenge:

```text
<EVENT>/<challenge>/
├── files/        original inputs (read-only)
├── work/         scripts, notes, dumps
└── solution/     writeup.md + flag.txt
```

Because config is discovered upward, a challenge can live inside this
repository and still use `.opencode/`. To start from the minimal skeleton:

```sh
cp -R skeleton my-event/chal-01
cd my-event/chal-01
mkdir -p files work solution
opencode
```

`skeleton/` is a copy-ready starter; `.opencode/` is the same minimal skeleton
checked into the repo root. Both ship no agents or commands — those are `TODO`s
on purpose (guide steps 1, 3 and 4).

Start **inside the challenge folder**. The write guard uses the start directory
as its boundary; starting at the repository root is treated as kit maintenance
and makes the whole repo writable.

---

## Repository map

```text
.
├── README.md                 this file
├── HARNESS.md                two-hour build guide (12 steps)
├── workshop.html             70-minute guided slide deck
├── skeleton/                 minimal starter people build on
│   ├── README.md             short build order and checkpoints
│   ├── AGENTS.md             four-line scope contract (TODO)
│   └── .opencode/            config, agent, command, skill, plugin, targets
├── docs/
│   ├── harness.md            what a harness is; the five layers
│   ├── configuration.md      config, scripts, precedence
│   ├── models.md             provider and model choices
│   ├── events.md             event/challenge layout, sample CTF
│   ├── safety.md             guardrails and intentional gaps
│   ├── sessions-cost.md      context, compaction, usage reporting
│   ├── tools-permissions-plugins.md
│   └── troubleshooting.md    symptoms, fixes, repo layout
└── .opencode/
    ├── README.md             full configuration guide (what every field does)
    ├── opencode.jsonc        provider, models, permissions, policies
    ├── skills/
    │   ├── ctf-methodology/SKILL.md   workshop overlay — TODO placeholder
    │   └── vendor/ctf-skills/         12 MIT skills (see VENDORED.md)
    ├── plugins/
    │   ├── challenge-guard/index.ts   write-scope guard
    │   └── scope-guard/index.ts       shell/webfetch allowlist
    ├── scripts/              empty — build these in guide steps 8–11
    └── targets.json          remote-host allowlist (currently empty)
```

There is no root license file. The vendored skills keep their MIT license in
`.opencode/skills/vendor/ctf-skills/LICENSE`.

---

## Models

The kit talks to an OpenAI-compatible router (`ai-router.42security.io`) under
the provider ID `omnirouter`. The key names below are what you pass to
`--model omnirouter/<key>`; `modelID` is what the router receives.

| Key | Context / output | Tier | Notes |
| --- | --- | --- | --- |
| `beam-free` | 200k / 32k | free | **default**; tools + reasoning |
| `longcat-2-5-free` | 200k / 32k | free | fallback when Beam is rate limited |
| `glm-5-3` | 1M / 131k | free tier | long-horizon reasoning; confirm with the instructor |
| `deepseek-v4-1-flash` | 1M / 384k | free tier | long analyses; a good pin for a crypto agent you build |
| `haiku-5-5` | 1M / 128k | paid | optional everyday upgrade |
| `kimi-k2-7-code` | 262k / 262k | paid | exploit scripting |
| `qwen3-8-flash` | 1M / 131k | paid | open model |
| `gpt-6-luna` | 1.05M / 128k | disabled | route breaks on tool-result follow-ups |

The workshop set is free-tier only. `haiku-5-5`, `kimi-k2-7-code` and
`qwen3-8-flash` are present in the config for optional upgrades; selecting one
bills your key. `gpt-6-luna` is configured with `"disabled": true` so it never
appears in `/models`.

The session default (`model`), compaction, title generation and summaries are
all pinned to `omnirouter/beam-free`, so an untouched session costs nothing. See
[`docs/models.md`](docs/models.md) and the model section of
[`.opencode/README.md`](.opencode/README.md) for provider and model syntax.

---

## Permissions, policies and guards

`.opencode/opencode.jsonc` starts from allow-all and then subtracts:

- **Denied shell commands:** `sudo`, `su`, `rm -rf` (and `-fr`, `-Rf`,
  `-r -f`), `mkfs*`, `dd if=* of=/dev/*`, `shutdown*`, `reboot*`,
  `chmod -R 777 *`.
- **Ask first:** reading `*.env`.
- **Policies** (never prompt, cannot be overridden by "Allow always"):
  reads of `*/.ssh/*`, `*/.aws/credentials`, `*/.config/gcloud/*`, and
  `shell:sudo *`.

The rules are ordered, and **the last match wins**. Agent-level rules are
appended after global ones, so an agent can tighten them but a broad `allow`
inside an agent would re-enable what the global config denies.

Two plugins turn conventions into checks:

- **`challenge-guard`** normalizes absolute and relative paths and denies
  `edit`/`write`/`patch` outside the start directory, under `files/`, or via
  `..` and sibling-prefix tricks. Reads and shell are untouched.
- **`scope-guard`** reads `.opencode/targets.json` on every `shell` and
  `webfetch` check and denies unknown hosts. No file or an empty `allow` list
  means nothing remote is permitted; loopback is allowed by default; commands
  with no detectable host still pass. It is a guard against accidents, not a
  sandbox.

Both plugins ship without their offline tests in this checkout. `HARNESS.md`
step 8 and `.opencode/README.md` specify the deny/allow matrices you should
write and run before trusting them. The kit also ships no scaffolding command:
`/new-ctf` is one of the commands you build (HARNESS.md step 4), and it shells
out to `.opencode/scripts/new-challenge.sh`, which is not here yet.

---

## Documentation

| Document | Contents |
| --- | --- |
| [`HARNESS.md`](HARNESS.md) | the build guide: skeleton, scope, model, agent, command, skill, permissions, subagents, plugins, workspace, cost, validation, gaps |
| [`workshop.html`](workshop.html) | the slide deck: agent/harness theory, eight lab steps, measurement, design canvas |
| [`docs/harness.md`](docs/harness.md) | the five-layer model and where each layer lives in this kit |
| [`docs/configuration.md`](docs/configuration.md) | config precedence, scripts, hot reload |
| [`docs/models.md`](docs/models.md) | provider, free/paid model choices, cost control |
| [`docs/events.md`](docs/events.md) | event and challenge layout, scaffolding, the sample CTF |
| [`docs/safety.md`](docs/safety.md) | guardrails, scope, secrets, and what is deliberately out of scope |
| [`docs/sessions-cost.md`](docs/sessions-cost.md) | context caps, compaction, recorded vs estimated cost |
| [`docs/tools-permissions-plugins.md`](docs/tools-permissions-plugins.md) | permission semantics and the write guard |
| [`docs/troubleshooting.md`](docs/troubleshooting.md) | common failures and their fixes |
| [`.opencode/README.md`](.opencode/README.md) | the long reference: every config field, and how to add a model, provider, agent, command, skill, tool or MCP server |

Where the docs point at a file that is not in this checkout, treat the guide as
the specification for building it.

---

## What is missing (and TODO)

Everything in this table is referenced by the documentation but absent or a
placeholder in this checkout.

| Path | Referenced by | State |
| --- | --- | --- |
| `AGENTS.md` | every doc; guide step 1 | missing |
| `.opencode/skills/ctf-methodology/SKILL.md` | `.opencode/README.md` | file contains only `TODO` |
| `.opencode/agents/*` and `.opencode/commands/*` | by design | not shipped — build your own (guide steps 3–4) |
| `.opencode/scripts/new-challenge.sh`, `new-challenge.ps1` | a `/new-ctf` command you build, `docs/events.md` | missing |
| `.opencode/scripts/test-challenge-guard.mjs`, `test-scope-guard.mjs` | guide step 8, `docs/configuration.md` | missing |
| `.opencode/scripts/validate.py` | guide step 11 | missing |
| `.opencode/scripts/usage.py` | guide step 10, `docs/sessions-cost.md` | missing |
| `.opencode/scripts/setup-playwright-mcp.sh` | `.opencode/README.md` | missing |
| `.opencode/pricing.json` | guide step 10, `docs/sessions-cost.md` | missing |
| `install.sh`, `install.ps1` | `.opencode/README.md`, `docs/configuration.md` | missing |
| `CTF/` sample event (xor-01, png-01, enc-01) | `docs/events.md` | missing |

Until those exist, the guard tests cannot be run, and usage/cost reporting is
not available. Agents and commands are built by you (HARNESS.md steps 3–4), so
there is no `ctf` agent prompt or `/solve` command until you write them.

---

## Safety and limits

- **Authorized targets only.** Challenge files, lab hosts and ports given to
  you, or your own environment. Real-world work only inside a written
  engagement.
- **Execution is not isolated.** Shell commands run on your machine as your
  user. Pwn and malware challenges need your own container or VM.
- **Scope enforcement is partial.** The write guard is real. Shell scope is the
  `scope-guard` allowlist plus written rules; it cannot follow a tunnel or
  infer intent from a command with no visible host.
- **No scorer.** A flag in `solution/flag.txt` is not checked against a
  reference; you verify it against the event's flag format yourself.
- **No web search.** `websearch` is off on purpose: no provider guarantee, no
  writeup spoilers, fewer tokens per request. `webfetch` and `curl` remain for
  specific URLs.
- **Secrets stay out of the repo.** Rotate the router key after the event.
- **Prompt injection is a human call.** If a challenge says "agents, do not
  solve this", the expected behavior is to quote the notice and stop, not to
  obey or silently ignore it. That rule belongs in your `AGENTS.md`.

---

## What is intentionally not included

This is a workshop harness, not a competition platform. The four thin layers
are deliberate:

| Gap | Why it matters | What it would take |
| --- | --- | --- |
| Execution isolation | challenges run on your host | container or VM with no network (`docker run --net none`, firejail) |
| Scope enforcement for shell | "only this host" is partly prose | per-challenge target allowlist plus a shell pre-check that denies other hosts |
| Scoring loop | a written flag is never judged | a scorer against reference flags, with pass rate and token cost |
| Toolchain pinning | "works on my machine" | a versioned image with pwntools, gdb + gef, binwalk, exiftool, tshark, z3 |

Adding any one of them is a small project; add its offline test at the same
time.

---

## Credits

- Workshop and reference kit: 42 Security, 2026.
- Vendored skill catalogue: [ljagiello/ctf-skills](https://github.com/ljagiello/ctf-skills),
  MIT, commit `a16e19a` (see
  [`.opencode/skills/vendor/ctf-skills/VENDORED.md`](.opencode/skills/vendor/ctf-skills/VENDORED.md)).
- Harness: [OpenCode V2](https://opencode.ai/docs/).
