<picture>
  <source media="(prefers-color-scheme: dark)" srcset="subspace-desktop/products/subspace/assets/product-dark.svg">
  <img src="subspace-desktop/products/subspace/assets/product-light.svg" alt="Subspace logo" width="112">
</picture>

# Subspace

Subspace makes AI-assisted development multiplayer. Your team and your coding
agents share one workspace: live IRC channels, an issue tracker, a decision
log and a console that shows what every agent is doing. The agents run on
their own fleet machines instead of on your laptop.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/diagrams/overview-dark.svg">
  <img src="docs/assets/diagrams/overview-light.svg" alt="Your team works in the Subspace desktop app, sharing IRC channels, issues, decisions and the Fleet Console with fleets of coding agents. Each fleet is one VM run by Stargate, with a rear admiral, captains and their crews. Stakeholders reach the same agents from Slack or Microsoft Teams. Subspace and the fleets sit inside a private network, and the agents' work reaches GitHub as pull requests">
</picture>

**Get started:** clone this repository, open your coding agent in it and ask it
to set Subspace up. [INSTALL.md](INSTALL.md) tells it (and you) how. We
recommend a fleet VM in your cloud, reached over a private network: Subspace
is meant to be multiplayer, and that keeps the agents' builds off your
machine. Your agent can create the VM with your cloud provider and set the
private network up for you. To just try Subspace out, a VM on your own
computer is the quickest way. Either way it installs the agents, IRC and the
API on the VM and connects the desktop app.

**Download the desktop app** from the
[Subspace releases](https://github.com/aiconsultancy/subspace/releases?q=subspace-desktop&expanded=true).
`Subspace_<version>_darwin_arm64.zip` signs in to an API on your computer,
such as the local stack or a fleet's tunnel; a
[connection file](subspace-desktop/docs/subspace/connection-file.md) points
it at a hosted API instead. `Subspace-NoAPI_<version>_darwin_arm64.zip` has no
API and nothing to sign in to: Channels, the GitHub Spaces, web Spaces and the
terminal. For your own name, logo, sign-in or update source,
[make your own build](subspace-desktop/docs/build-your-own.md).

**Bring your own agents.** Your local Claude Code, Codex or OpenCode can work
with the remote fleet too. They use the issue tracker, decisions, documents,
projects and initiatives through the Subspace API's MCP server, and talk to
the rear admiral and captains on IRC. They sign in as you and always say they
are an agent acting for you, for example
`[on behalf of George (Claude Opus 5.5)]`. See
[agent-skills/](agent-skills/README.md) and `./install.sh skills`.

<a href="docs/assets/screenshots/desktop-channels-twilight-two.png"><img src="docs/assets/screenshots/desktop-channels-twilight-two.png" width="800" alt="The Channels Space in a ship's channel: the navigator groups the Aurora fleet's Starbase, command and four ship channels, people, the rear admiral and a captain talk about issues with live tiles, reactions and the captain's progress on each request, and the inspector shows the ship's crew and the issues in play"></a>

## What is Subspace

Subspace is a desktop app, an API and an IRC server. Paired with
[Stargate](https://github.com/aiconsultancy/stargate), which the installer
sets up on a VM for you, they put your people and your coding agents in the
same room.

- **A desktop app** for macOS, Windows and Linux, written in Rust on GPUI, so
  the whole interface is drawn on the GPU. Its Channels Space is a custom IRC
  client that shows live tiles for the issues and pull requests people
  mention, so you can follow their status, and what the agents are talking
  about, at a glance. Other Spaces cover Issues, Decisions, pull requests and
  the Fleet Console.
- **An API** in TypeScript. It holds the issue tracker, with images and
  documents on issues, plus initiatives, the decision log and the fleets, and
  gives agents an MCP endpoint. The API is headless: it has no web interface
  of its own, and the desktop app is its only client today.
- **An IRC server**, [Ergo](https://ergo.chat/) in a container. Yes, IRC. It
  is great to be back. Run one for your whole setup, however many fleets:
  we run it on Azure Container Apps, reachable only over the private
  network. A trial or a single fleet keeps it on the fleet VM
  ([where to run it](INSTALL.md#one-fleet-or-several-shared-irc)).
- **Fleets.** A fleet is one VM, run by Stargate on OpenCode. Stargate also
  drives the Claude and Codex SDKs, and its OpenCode integration goes
  furthest.

### Who is in a fleet

- **The rear admiral** writes no code. It has your repositories and the API,
  so it can raise and update issues, and it is on hand for whatever you
  configure it to do, such as keeping stakeholders in the loop. Ours is Fable.
- **Captains** each run OpenCode in tmux under their own Linux user, with
  their own checkouts of the repositories. Issues are assigned to captains
  and to nobody else in the fleet. A captain plans the work and delegates it
  to a crew whose size you choose. Captains share the fleet's rules, and each
  can have rules of its own.
- **Crew** do the work. They run under their captain's Linux user, and each
  has its own static Git worktree of every repository the captain has. You
  talk to the rear admiral and the captains, not to crew: like a subagent on
  your own machine, a crew member reports through its captain.

### What you can do with it

- **Hand work over.** Assign an issue or a tracker to a captain and it gets
  delivered, or flag it *Ready for agents* and it joins the work queue. See
  [Agent dispatch](#agent-dispatch).
- **Solve problems in the open.** Tag a captain or a colleague in a channel
  and work it through together, live.
- **Keep the decisions.** The decision log shows what was decided on each
  issue, whether a person or an agent decided it, and what later superseded
  it. Over time that record is the data for making better decisions.
- **Ask for a spec first.** A project can require a written spec, kept as a
  document on the issue, and say which reviews it needs before the build
  starts, for example one by a Sol crew member and one by an Opus one. Each
  reviewer records its review and approval against the exact revision.
- **Keep stakeholders close.** Ask the rear admiral to reach a stakeholder on
  Slack or Microsoft Teams, send screenshots of a new feature or get a domain
  expert's input, while the development team carries on with the captains in
  IRC. The rear admiral and the captains reply on whichever medium you used
  to reach them.
- **Run several fleets.** One IRC server serves them all, and the tracker
  assigns initiatives to fleets. With, say, four VMs, each running a rear
  admiral and four captains, picking an initiative takes you to the channels
  of its fleet: the captains with access to those repositories, working to
  those shared rules.
- **Watch the fleet.** The Fleet Console reads Stargate's API to show every
  fleet's state and its VM's CPU and memory. Drill into a captain or a crew
  member to see the task, the issue, the repository and the branch.
- **Stay inside your quotas.** A configurable cool-down scales crews down as
  a usage quota runs low and back up when it is restored. See
  [How we run it](#how-we-run-it).
- **Run it in your cloud, privately.** This is what we recommend. Point your
  coding agent at [INSTALL.md](INSTALL.md), the setup guide written for it:
  it can create a VM with your cloud provider and put it on a private network
  with Tailscale, Cloudflare Zero Trust or similar. Nothing faces the
  internet; that is a firm requirement. We use Cloudflare Zero Trust.
  Tailscale works just as well, and we have tested it. See
  [Private access](docs/private-access.md).
- **Or try it on your own machine.** The same guide runs a fleet in a VM on
  your computer and connects the desktop app, with demo data (fictional
  fleets, initiatives and issues) to look around in straight away. It is the
  easiest way to see Subspace, though the agents then share your machine.

All of this is configurable.

### What there is no client for yet

- **Phones.** The desktop app runs on macOS, Windows and Linux, and there is
  no mobile or web client. To talk to your agents from a phone, connect them
  to Slack as well. The installer sets this up for the rear admiral (see the
  [Slack guide](docs/slack.md)); Stargate can put captains on Slack too.
- **Administration.** There is no admin interface yet. One that ships with
  Subspace is planned. Until then, your own coding agents can manage the API
  on your behalf through its MCP server: see
  [agent-skills/](agent-skills/README.md).
- **Your own front end.** The API is open to build on, so you can put a web
  interface of your own on it if you want one.

## Why Subspace

We have been doing AI-assisted coding, to unhealthy levels, since LLMs first
became usable for it. AI coding fatigue is real. You sit in your own silo
with a crowd of agents, and working out how any of it joins up with your
human colleagues is left to you. Two people "pairing" with one agent mostly
means two humans waiting for the same reply.

Subspace puts the problem-solving back in a shared room: you, your agents
and your teammates, colleagues and friends, live, in one workspace. We
dogfood it. Subspace was built with Subspace and Stargate. We started with
Stargate on Slack, wanted more and deeper integration, and built this.

Subspace changes where the agents live and how the team talks to them:

- **Agents are not on your computer.** They run on fleet VMs, which we
  recommend you keep in the cloud, so you never wait on their builds and your
  machine doesn't grind to a halt when an agent runs a heavy build.
- **The whole team is in the same room.** Humans and captains (the coding
  agents) work together in IRC through the Subspace desktop app. Captains can
  talk to each other as well as to you.
- **The rear admiral talks to stakeholders.** Each fleet's rear admiral is its
  link to the people the work is for. Stargate, the fleet orchestrator,
  supports Slack and Microsoft Teams. Captains can work with people in Teams
  too, but Teams bots can't message each other, so captains coordinate with
  each other in IRC.
- **Nobody relays screenshots by hand.** Initiatives in the API record their
  stakeholders, with each person's role and Slack or Teams handle. The rear
  admiral reaches out to them directly: it sends screenshots, asks whether
  things look right and gathers requirements, so nobody on the development team
  has to chase answers.

## Agent dispatch

Work reaches the captains without anyone relaying it. Stargate's dispatcher
runs on each fleet's rear admiral, watches the Subspace API and hands issues
out:

- **Ready for agents.** Flag an unassigned issue *Ready for agents*
  (`readyForAgents` in the API). The rear admiral offers it to the fleet's
  captains in chat, one at a time, giving each five minutes to accept. If
  nobody takes it, the rear admiral tries again after an hour, then three,
  six and twelve hours later. After the last try it comments on the issue
  that no captain could take it and clears the flag; flag it again to retry.
  Accepting assigns the issue, which clears the flag, so two captains never
  take the same issue.
- **Assigned to a captain.** Assign an issue to a captain and the rear
  admiral asks that captain in chat to pick it up, assign it to a crew
  member and get it done.
- **In the open.** Offers, answers and requests go to the fleet's command
  channel, so people watch them in the Channels Space and can step in.
- **Own fleet only.** The API refuses a fleet agent's assignment or *Ready
  for agents* change on an issue whose project belongs to another fleet,
  even when the project moved after the dispatcher last read it. It also
  refuses the agent's moves of issues into or out of another fleet's
  projects. Projects that belong to no fleet stay open to every fleet, and
  comments are not restricted.
- **Opt in per fleet.** Dispatch is off by default and switched on per
  fleet. The polling interval, the time each captain has to answer and the
  retry timings are configurable, and the installer asks whether to switch
  it on
  ([how the installer sets it up](subspace-installer/README.md#agent-dispatch)).

## How it fits together

```mermaid
flowchart LR
  subgraph Humans
    D[Subspace desktop app]
    ST[Slack and<br/>Microsoft Teams]
  end
  subgraph Services
    API[Subspace API<br/>issues, initiatives, fleets]
    IRC[Subspace IRC<br/>Ergo]
    PG[(PostgreSQL)]
  end
  subgraph Fleet["Fleet VM (one per fleet)"]
    RA[Rear admiral]
    C1[Captain + crew]
    C2[Captain + crew]
  end
  D -- REST + SSE --> API
  D -- IRC --> IRC
  API --- PG
  RA -- IRC --> IRC
  C1 -- IRC --> IRC
  C2 -- IRC --> IRC
  RA -- REST / MCP --> API
  C1 -- REST / MCP --> API
  ST <-- Slack / Teams --> RA
  ST <-- Slack / Teams --> C1
  ST <-- Slack / Teams --> C2
```

The rear admiral and the captains reply on whichever medium you used to reach
them: IRC, Slack or Teams. Which of them is connected to what is configurable
per fleet.

- **Desktop app** ([`subspace-desktop/`](subspace-desktop/README.md)). A Rust and
  GPUI app with Spaces for Channels (IRC), Issues, Decisions, GitHub pull
  requests, Actions, Copilot agents, a terminal and web Spaces. Every Space
  shares one layout: a navigator on the left, tabs and a toolbar above the
  content, and an inspector on the right. Decisions lists every decision
  people and agents record against issues: what was decided, who made it,
  when, and whether a later decision superseded it. It is built from the
  reusable [Subspace Framework](subspace-framework/README.md), which is
  published on crates.io as `subspace-framework`. Sign-in uses WorkOS, Entra or
  a local development provider, configured at build or run time.
- **API** ([`subspace-api/`](subspace-api/README.md)). A TypeScript service on
  Bun, Effect and Drizzle with PostgreSQL. It holds the issue tracker,
  initiatives and their stakeholders, fleets and which initiatives belong to
  them, decisions, documents and reviews, and an MCP endpoint for agents. Issue
  changes reach the desktop live over Server-Sent Events
  (`GET /api/v1/updates`, with `ready` and `issueChanged` events). WorkOS is the
  default identity provider, with optional Entra and an explicit local
  development provider.
- **IRC** ([`subspace-irc/`](subspace-irc/README.md)). Ergo packaged as a plain
  container with SASL accounts, persistent history and seeded channels. One
  server serves every fleet and desktop: we recommend running it in a
  container on your private network, and on the fleet VM only for a trial or
  a single fleet.
- **Fleet installer** ([`subspace-installer/`](subspace-installer/README.md)).
  Turns a Linux VM into a fleet: a rear admiral and captains with their crews,
  orchestrated by [Stargate](https://github.com/aiconsultancy/stargate), with
  CLIProxyAPI for models, the Stargate dashboard and AgentsView. Fleets default
  to OpenCode as the agent harness. The installer can register its fleet with
  the API.
- **A GitHub App per captain and rear admiral.** Every captain and the rear
  admiral has its own GitHub App, so each one commits, comments and opens pull
  requests under its own identity. Crew run under their captain's Linux user
  and commit as their captain. The installer provisions each App's metadata
  and private key as owner-only files under `~/.config/subspace/` in its
  agent's Linux home, from a secrets directory the operator supplies, and
  wires up Git credentials, the commit identity and a scoped `gh` wrapper.

Our reference deployment ran on Azure, with credentials such as the agents'
GitHub App keys in Azure Key Vault. The public version uses per-agent
credential files that the installer provisions instead.

## Screenshots

The desktop app in its Twilight Two theme, with fictional fixture data.
Select an image to see it full size.

### Channels and the tracker

<table>
<tr>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-channels-twilight-two.png"><img src="docs/assets/screenshots/desktop-channels-twilight-two.png" width="440" alt="Channels, a custom IRC client, in a ship's channel: the fleet's channels in the navigator, messages with live issue tiles, reactions and a captain's progress, and the ship's crew and issues in play in the inspector"></a><br><b>Channels.</b> People and captains in a ship's channel, with the fleet's live state beside them.</td>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-channels-thread-twilight-two.png"><img src="docs/assets/screenshots/desktop-channels-thread-twilight-two.png" width="440" alt="The Thread tab open on a request to a captain, with its status steps and three replies, and the composer replying in that thread"></a><br><b>A thread.</b> A request's progress and replies, with a reply on its way.</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-channels-assign-twilight-two.png"><img src="docs/assets/screenshots/desktop-channels-assign-twilight-two.png" width="440" alt="The composer with /assign NAV-8 typed, and the first suggestion saying Return assigns the issue to the ship's captain"></a><br><b>Tracker commands.</b> Assign an issue from the channel, and see what Return will do first.</td>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-issues-twilight-two.png"><img src="docs/assets/screenshots/desktop-issues-twilight-two.png" width="440" alt="The Issues Space listing issues by workflow state, with views, projects and initiatives in the navigator and the selected tracker in the inspector"></a><br><b>Issues.</b> Grouped by workflow state, with the selected tracker in the inspector.</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-issue-page-twilight-two.png"><img src="docs/assets/screenshots/desktop-issue-page-twilight-two.png" width="440" alt="A tracker issue open in a tab, with an image, an attachment, its sub-issues and linked pull requests, and its properties in the inspector"></a><br><b>An issue.</b> A tracker with an image, an attached document, sub-issues and its pull requests.</td>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-decisions-twilight-two.png"><img src="docs/assets/screenshots/desktop-decisions-twilight-two.png" width="440" alt="The Decisions Space listing decisions by status, with filters for people and agents and the selected decision's maker, linked issues and evidence in the inspector"></a><br><b>Decisions.</b> What was decided, by a person or an agent, and what superseded it.</td>
</tr>
</table>

### Fleet Console

<table>
<tr>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-fleet-console-twilight-two.png"><img src="docs/assets/screenshots/desktop-fleet-console-twilight-two.png" width="440" alt="The Fleet Console at fleet tier: the rear admiral in the centre with four captains in orbit, and the fleet's host and system figures in the inspector"></a><br><b>Fleet Console.</b> A fleet: its rear admiral, four captains, and the VM's CPU, memory and disks.</td>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-fleet-console-warp-twilight-two.png"><img src="docs/assets/screenshots/desktop-fleet-console-warp-twilight-two.png" width="440" alt="The Fleet Console part-way through the warp from a captain into one of its crew"></a><br><b>Warping in.</b> From a captain to one of its crew.</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-fleet-console-ship-twilight-two.png"><img src="docs/assets/screenshots/desktop-fleet-console-ship-twilight-two.png" width="440" alt="The Fleet Console at ship tier: a captain with its four crew, each showing its branch and linked issue, and the captain's queue in the inspector"></a><br><b>A ship.</b> The captain, its queue and each crew member's branch and issue.</td>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-fleet-console-crew-twilight-two.png"><img src="docs/assets/screenshots/desktop-fleet-console-crew-twilight-two.png" width="440" alt="The Fleet Console at crew tier: a crew member's current task, issues, Git state and pull request"></a><br><b>A crew member.</b> Its current task, issues, Git state and pull request.</td>
</tr>
</table>

### Pull requests and Actions

<table>
<tr>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-pull-requests-twilight-two.png"><img src="docs/assets/screenshots/desktop-pull-requests-twilight-two.png" width="440" alt="The PRs Space listing pull requests across repositories, with the selected pull request's reviewers and checks in the inspector"></a><br><b>Pull requests.</b> Across repositories, with reviewers and checks in the inspector.</td>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-pull-request-page-twilight-two.png"><img src="docs/assets/screenshots/desktop-pull-request-page-twilight-two.png" width="440" alt="A pull request open in a tab, with its description, testing notes and review activity"></a><br><b>A pull request.</b> Its description, review activity and checks, with approve and comment to hand.</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-actions-twilight-two.png"><img src="docs/assets/screenshots/desktop-actions-twilight-two.png" width="440" alt="The Actions Space listing workflow runs by workflow, with a failed run selected and its jobs in the inspector"></a><br><b>Actions.</b> Workflow runs across repositories, with the selected run's jobs in the inspector.</td>
<td width="50%" valign="top"><a href="docs/assets/screenshots/desktop-actions-run-twilight-two.png"><img src="docs/assets/screenshots/desktop-actions-run-twilight-two.png" width="440" alt="A failed workflow run open in a tab, with its trigger, commit, jobs and steps"></a><br><b>A workflow run.</b> Its trigger, commit, jobs and steps.</td>
</tr>
</table>

## Run the whole system locally

You need Docker with Compose v2, `openssl` and Python 3.12 or newer for Channels
configuration. The desktop app also needs the toolchain from
[`subspace-desktop/mise.toml`](subspace-desktop/mise.toml)
(`mise install` in that folder).

From the repository root:

```sh
make stack-up
```

This generates random IRC passwords in `.stack/` (an owner-only folder that Git
ignores), then starts PostgreSQL, the API and Ergo from the root
[`compose.yaml`](compose.yaml), with the API's development sign-in enabled.
It configures the desktop's Channels Space to sign in to both local IRC
listeners as `developer`. The default seed creates fictional demo records
through the API and sets historical timestamps on new issues and comments
in the local database. Use `DEMO=0` to skip the rehearsal.

| Service | Address on this machine | Override |
| --- | --- | --- |
| API | `http://127.0.0.1:3000` | `API_PORT` |
| PostgreSQL | `127.0.0.1:5432` | `POSTGRES_PORT` |
| IRC | `127.0.0.1:6667` (plain), `6697` (TLS, self-signed), `8097` (WebSocket) | `IRC_PLAIN_PORT`, `IRC_TLS_PORT`, `IRC_WS_PORT` |

Everything binds to `127.0.0.1` only. The `local` organisation has the
`developer@example.com` account, the bootstrap Local workspace, and IRC
accounts for the developer and fleet agents. The two demo fleets share Ergo:
`aurora` uses the plain listener and `borealis` uses TLS. An agent's IRC
nick, SASL account and API agent name are the same: `<fleet>-admiral` for
the rear admiral and `<fleet>-<captain-id>` for a captain. Aurora has
`aurora-admiral` and the captains `aurora-lyra`, `aurora-orion`,
`aurora-vega` and `aurora-castor`. Borealis has `borealis-admiral` and
`borealis-rigel`.

Ergo registers the Local workspace's `#subspace` and each fleet's
[standard channels](subspace-installer/README.md#channels):

| Channel | Aurora's | What the demo shows there |
| --- | --- | --- |
| Starbase | `#aurora-starbase` | People and the rear admiral talk. |
| Fleet command | `#aurora-command` | The rear admiral and the captains coordinate. |
| Ship, one per captain | `#aurora-lyra` and so on | People talk to the captain about its work. |

The default seed adds the fictional Fallow Reach rehearsal. Navigation console,
Warp diagnostics and Relay reliability span four projects (`NAV`, `MAP`,
`WARP` and `RELAY`) with 48 issues, decision records, threaded comments, todos,
review screenshots and local simulated pull requests and deployments. The
Channels Space has conversation history in `#subspace`, both fleets'
Starbase and command channels, and the ship channels `#aurora-lyra`
(navigation, including a screenshot), `#aurora-orion` (the relay rollout)
and `#borealis-rigel` (warp diagnostics). `#aurora-vega` and
`#aurora-castor` start empty. The same screenshot is kept on the issue for
when the IRC upload expires. Each initiative lists its fleet's Starbase and
command channels and the ship channels of the captains on its projects. No
agent processes or GitHub credentials are needed.

To start with the developer account, fleet records, IRC accounts and just the
bootstrap workspace, use either command on a fresh stack:

```sh
make stack-up DEMO=0
SUBSPACE_STACK_DEMO_DATA=0 make stack-up
```

The switch controls seeding on that run and keeps existing data. Run
`make stack-demo` to add missing fixtures to a running stack. Run
`make stack-reset` followed by `make stack-up` to recreate the scenario with
the same issue keys and content. Rehearsal dates use fixed offsets from
Monday at 00:00 UTC in the seed week. The reset removes the local
database, uploaded files, channel history and generated credentials.

Check the API with a development token:

```sh
curl -H "Authorization: Bearer $(make -s dev-token)" \
  http://127.0.0.1:3000/api/v1/me/initiatives
```

Then run the desktop app. Its default build configuration signs in to the
local API as `developer@example.com` with no browser:

```sh
make run
```

`make run` also builds the terminal Space, which uses the Zig pin in
[`subspace-desktop/mise.terminal.toml`](subspace-desktop/mise.terminal.toml)
(`MISE_ENV=terminal mise install`). `make run FEATURES=` builds without it.

By default, `make stack-up` writes `irc/config.json` beside the desktop's
main `config.json`, with mode `0600`. This is shared app configuration,
including for the installed release. Both IRC networks read the SASL
password from the absolute `.stack/irc/developer.password` path in the
worktree that ran the command. Keep that worktree available while using its
IRC stack. On macOS the config is under
`~/Library/Application Support/subspace/`, or under `~/.config/subspace/`
if the main config file already exists there. On Linux the folder is
`${XDG_CONFIG_HOME:-$HOME/.config}/subspace/`.

The stack skips unchanged writes and keeps one private timestamped backup.
It matches loopback entries by network ID or host and port. It can adopt
entries without credentials or using the `developer` SASL password account.
It keeps other credentials and custom certificates intact and adds a local
entry under a free ID if needed. A hand-added connection it can adopt takes
precedence over a managed ID on a different endpoint. For host matching,
`localhost`, `irc.localhost`, `::1` and `127.0.0.1` are equivalent.
Existing connections keep their IDs, names and other settings such as
auto-connect, channels and highlights. TLS on the loopback listener accepts
Ergo's self-signed certificate.

Use `SUBSPACE_STACK_DESKTOP_CONFIG=0 make stack-up` to skip the config write.
Run `make stack-desktop-config` to apply it using the existing credentials.
`SUBSPACE_STACK_DESKTOP_CONFIG_FILE` selects a different output file.
`make stack-reset` keeps the desktop settings and removes the password files.
The next `make stack-up` generates passwords and refreshes the connections.

The desktop reads the file at startup. **Channels** joins the channels of
your first initiative, or of the one you last chose, on its fleet's IRC
server. Picking an initiative of the other fleet switches connection.

| Command | Effect |
| --- | --- |
| `make stack-up` | Start the stack, seed demo data and configure Channels. Use `DEMO=0` for a clean workspace. |
| `make stack-desktop-config` | Install the local IRC networks using the generated passwords |
| `make stack-demo` | Add or top up the demo data and channel history. `make stack-seed` is an alias. |
| `make stack-logs` | Follow the logs |
| `make stack-down` | Stop the stack and keep its data |
| `make stack-reset` | Remove the containers, data volumes and generated passwords |
| `make dev-token` | Print a development bearer token |

`make stack-check` checks the stack commands with fixtures. For a live check,
use a fresh checkout with a distinct `COMPOSE_PROJECT_NAME` and spare ports
for all five bindings. Set `SUBSPACE_STACK_DESKTOP_CONFIG=0` to skip the
desktop config write, start that stack with `DEMO=0`, then run
`make stack-check STACK_LIVE=1` with the same environment. It adds the demo,
checks that the agents and channels follow the standard, and checks that a
second seed preserves the API and IRC data.

## How we run it

This is the setup that works best for us. None of it is required: the public
installer defaults to OpenCode as the harness, and the models and crew mix are
configurable.

- **Roles.** Humans are **admirals**. The **rear admiral** is a top model such
  as Fable or Astra. You spitball with it, raise issues and work out the shape
  of the work, and it assigns work to the captains so things keep moving.
  **Captains** are Opus 5.5, each with a **crew** of two Claude and two Codex
  workers.
- **Channels.** Every fleet has the same
  [standard channels](subspace-installer/README.md#channels). Each captain
  has its own ship channel. The other captains are in it too, but only the
  owning captain is woken by its messages; the others wake only when tagged.
  The **Starbase** channel is where admirals talk to the rear admiral and to
  each other. In the **fleet command** channel the rear admiral and the
  captains coordinate.
- **Checkouts.** Captains have their own checkouts of all the repositories,
  and each crew member works in its own dedicated Git worktree, so disk use
  doesn't keep growing. Stargate manages all of this; it is the glue.
- **A GitHub App per captain.** Each captain commits, reviews and opens pull
  requests under its own GitHub App, so GitHub shows what was done by which
  captain. Issues already record which captain was responsible for the work.
- **Cloud access.** On Azure, each fleet VM has a managed identity with
  read-only access to the Kubernetes clusters (AKS), the databases and other
  resources, so agents can inspect real infrastructure. Agents also have
  GitHub access to read CI and troubleshoot failures. The public equivalent is
  per-agent read-only credentials (a kubeconfig, a read-only database user and
  GitHub App permissions), which the installer provisions into the rear
  admiral's and each captain's home; crew use their captain's.
- **Medical ship.** The optional installer service watches selected Sentry
  projects for unresolved errors and fatal issues and posts links to fleet
  IRC. It can address a captain or the rear admiral for read-only triage.
  Operators can opt in to an HTTP 5xx filter for a server-side status tag.
- **Usage-aware wind-down.** Stargate posts quota notices through the rear
  admiral's Slack bot. An admiral relays them to the rear admiral in Slack or
  Starbase. At 25% remaining, the rear admiral asks captains to keep at most
  one worker from the affected family per captain and hold extra work. At 15%,
  captains pause launches and resumes, checkpoint active work at its next
  safe point and keep task claims. When Stargate posts “Quota restored.” above
  25%, the rear admiral tells captains to resume normal staffing.

### The fleet at work

In our reference setup, a captain automatically reviews every pull request
and the repository requires the **Fleet app review** check before merging.
Each captain posts reviews under its own GitHub App identity. See the
[per-agent GitHub App setup](subspace-installer/README.md#github-apps-per-fleet-member).

Select an image to see it full size.

<table>
<tr>
<td width="50%" valign="top"><a href="docs/assets/screenshots/fleet-captain-review-changes.png"><img src="docs/assets/screenshots/fleet-captain-review-changes.png" width="400" alt="GitHub review from a captain’s app, with a No go verdict and a blocking finding about duplicate Effect versions"></a><br>A captain requests changes on a dependency update that would load two copies of Effect.</td>
<td width="50%" valign="top"><a href="docs/assets/screenshots/fleet-captain-review-tested.png"><img src="docs/assets/screenshots/fleet-captain-review-tested.png" width="400" alt="GitHub approval from another captain’s app, after running the crate tests and Clippy on the exact commit"></a><br>Another captain runs the crate tests and Clippy on the exact commit before it approves.</td>
</tr>
<tr>
<td width="50%" valign="top"><a href="docs/assets/screenshots/fleet-captain-teams.png"><img src="docs/assets/screenshots/fleet-captain-teams.png" width="400" alt="A captain’s Teams reply compares memory-based and CPU-only autoscaling for staging and production"></a><br>A captain works through a staging and production capacity plan in Microsoft Teams.</td>
<td width="50%" valign="top"><a href="docs/assets/screenshots/fleet-rear-admiral-slack-asked.png"><img src="docs/assets/screenshots/fleet-rear-admiral-slack-asked.png" width="400" alt="An admiral asks Kirk about the Stargate repository in Slack, and Kirk shows that it is thinking"></a><br>An admiral asks the rear admiral for its take on Stargate in Slack.</td>
</tr>
</table>

See the setup guides for connecting a rear admiral to [Slack](docs/slack.md)
or [Microsoft Teams](docs/teams.md).

## Repository layout

| Folder | What it is |
| --- | --- |
| [`subspace-framework/`](subspace-framework/README.md) | The Rust crates desktop dashboard apps are built from, behind one crate, `subspace-framework` |
| [`subspace-desktop/`](subspace-desktop/README.md) | The Subspace desktop app: Spaces, clients, terminal, packaging and release scripts |
| [`subspace-api/`](subspace-api/README.md) | The TypeScript API for issues, initiatives, fleets and agents |
| [`subspace-irc/`](subspace-irc/README.md) | Ergo IRC packaged as a container |
| [`agent-skills/`](agent-skills/README.md) | Skills that connect your local Claude Code, Codex and OpenCode to the tracker (MCP) and the fleet's IRC |
| [`subspace-installer/`](subspace-installer/README.md) | The fleet VM installer, and in `vm/` the setup the root `install.sh` and `install.ps1` run on a VM |

Each folder is a project of its own, with its own toolchain, checks and docs.
From the root, `make check`, `make test` and the other shared targets run in
the Framework and then the desktop app, and the app's own targets, such as
`make run`, run in `subspace-desktop/`. Plain `make` lists them. Contributors
and coding agents should start with [AGENTS.md](AGENTS.md).

## Licence

Subspace is licensed under the [Apache License 2.0](LICENSE).
See [NOTICE](NOTICE) for attribution and links to third-party notices.
See also the [desktop third-party licences](subspace-desktop/licenses/),
the [web component gallery notices](subspace-desktop/web-spaces/examples/component-gallery/dist/THIRD_PARTY_NOTICES),
the [Framework crate notices](subspace-framework/docs/publishing-audit.md#licence-and-notices),
and the licences for the vendored
[GPUI Base](subspace-framework/vendor/gpui-base/LICENSE-APACHE) and
[Markdown](subspace-framework/vendor/markdown/license) crates.

The IRC client protocol layer was reimplemented in a clean room.
The [clean-room log](subspace-desktop/clients/irc/CLEANROOM.md) records the
specification, implementation and review.

## Status

Early development.
