<h1 align="center">fortkeep</h1>

<p align="center"><strong><em>A security checkup for your Mac that your coding agent runs with you.</em></strong></p>

<p align="center">
  <a href="https://github.com/b0dea/fortkeep/actions/workflows/ci.yml?query=branch%3Amain"><img alt="CI status" src="https://github.com/b0dea/fortkeep/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://github.com/b0dea/fortkeep/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/b0dea/fortkeep?color=blue"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <img alt="macOS 15 or later" src="https://img.shields.io/badge/macOS-15%2B-lightgrey.svg">
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#try-it">Try it</a> ·
  <a href="#with-your-agent">With your agent</a> ·
  <a href="#safety">Safety</a> ·
  <a href="#commands">Commands</a> ·
  <a href="#faq">FAQ</a>
</p>

<p align="center">
  <img src="docs/images/check.svg" alt="fortkeep check in a terminal: a score bar reading 4 of 11 met, then each control under MUST, SHOULD and NICE with a coloured ✓, ✗, !, ○ or – and what was found">
</p>

- **It checks.** Read-only checks compare your Mac with a baseline built around how developer Macs get attacked
  today: hijacked npm and PyPI packages, poisoned repos, AI agents tricked into bad commands, and secrets left in files.
- **It explains.** Your coding agent ([Claude Code](https://code.claude.com/docs),
  [Codex](https://developers.openai.com/codex) or [OpenCode](https://opencode.ai)) goes through the results with you
  in plain words, most important first.
- **It fixes, one change at a time.** Each fix runs only after you approve it, with a backup and an undo.

It is not an antivirus, not device management and not a sandbox. The image above is sample output from a test
fixture: real control titles and layout, with a short list. A real run checks every control and takes minutes.

## Install

You need macOS 15 or later, Apple's Command Line Tools (`xcode-select --install`), and Claude Code, Codex or OpenCode
for the fixes.

**With Homebrew:**

```sh
brew install b0dea/tap/fortkeep
fortkeep
```

**Or with the installer.** Download it, compare its SHA-256 with the one below, and only then run it. Never pipe it
into a shell.

```sh
curl -fsSLO https://raw.githubusercontent.com/b0dea/fortkeep/main/install.sh
shasum -a 256 install.sh
bash install.sh
```

The SHA-256 of `install.sh` for the current release: `2ea03c7d4ea79c857e616fdab3ebe264c5b73ca01e2728c8f1435b9db07717eb`

Both put fortkeep in `~/.local/share/fortkeep`: a git checkout of one signed release. The installer refuses any
release but the one it pins, by tag and commit, checked before anything from it runs, and refuses a tag that isn't
signed by a maintainer that release lists. Those pins are what you trust on first install, so check they match the
ones in the [release notes](https://github.com/b0dea/fortkeep/releases). From then on `fortkeep update` moves it only
to releases a maintainer it already trusts signed.

## Try it

```sh
fortkeep                              # a menu: check, scan a repo, fix with your agent, summary, update
fortkeep check                        # check this Mac, read-only, no agent needed
fortkeep scan ~/Downloads/some-repo   # is this repo safe to open? reads it, runs nothing from it
fortkeep agent                        # start your coding agent in the fortkeep folder, then type /posture
```

In a terminal you get colour, a progress line and an arrow-key menu; piped or in a script, plain text.

![The fortkeep menu: this copy is a signed release, the last check's score, what to do next, and six numbered choices](docs/images/menu.svg)

In your agent, `/posture` runs the check (the first time, after a few set-up questions) and shows one score line
and one table:

> **4 of 11 met · 5 to fix · 1 couldn't check · 1 accepted**
>
> | Status | ID | What | Why it matters |
> |---|---|---|---|
> | ✗ FAIL | BL-OS-02 | Firewall on with stealth mode | Stealth is off, so other devices on your network can find this Mac. |
> | ! ERROR | BL-BR-06 | DNS filtering with malware blocklists | This Mac's DNS answered nothing, so the check couldn't test it. |
> | ○ ACCEPTED | BL-SE-01 | SSH keys live in a protected SSH agent (1Password, Secretive or Bitwarden) | Your reason: my SSH keys live on a hardware key. |
>
> ✓ 4 met · – 1 doesn't apply here
>
> What next? Fix them one at a time · Make a summary to share · Scan a repo before opening it · Change my settings

The real table lists every result that needs attention; this one is cut to three rows.

## With your agent

```sh
fortkeep agent          # starts your coding agent in the fortkeep folder, so its guards and skills load
```

Then type:

| Command | What it does |
|---|---|
| `/posture` | First time: asks about teach mode, the set-ups that apply and any private folders. Then runs the check and explains the results. |
| `/fix` | Works through the failures one at a time ("Fix 2 of 5"), each only after your answer, and checks again: `✗ FAIL → ✓ PASS`. Also undoes a fix. |
| `/scan` | Before you open or install a repo: scans it, or the repos in one folder, for signs it is poisoned. Reads only. |
| `/summary` | A posture summary you can share: each control's title, level and result, and your reason for any you kept. No file paths or evidence. |
| `/if-red` | What to do when a check finds something that looks like real malware. |

Each agent loads the same instructions, skills and guard scripts; only the wiring differs
([docs/agents.md](docs/agents.md)):

| | Claude Code | Codex | OpenCode |
|---|---|---|---|
| Start | `fortkeep agent claude` | `fortkeep agent codex` | `fortkeep agent opencode` |
| First run | accept "trust this folder" | trust the folder, then "Trust all and continue" for its hooks | nothing: the guard plugin loads by itself |
| Start a skill | `/posture` | `$posture` | `/posture` |
| How you approve a fix | pick `Apply <ID>` in its question | type `Apply <ID>` as your whole message | pick `Apply <ID>` in its question |

If the agent's first message warns that this copy isn't exactly a signed release, don't run fixes: reinstall,
unless you changed it yourself.

## Safety

- **The checks only read.** They report how the Mac is set up and change nothing.
- **Every change needs your answer.** A fix runs only after you answer `Apply <ID>` for that one change. It keeps a
  backup, has an undo, and is logged in `reports/change-log.md`.
- **It never runs `sudo`.** Admin steps are commands you type yourself in the Terminal app, each ending with
  `sudo -k`.
- **The agent's session is allow-listed.** In the fortkeep folder the agent may run only fortkeep's own scripts and
  read only fortkeep's own files, and it writes none of them. Web fetch and search, subagents and MCP tools are
  refused. Guard scripts check every tool call ([docs/agents.md](docs/agents.md)).
- **Private folders stay private.** Name a folder and every check and scan skips it, and the agent never lists, opens
  or searches it. Only you can take one off the list.
- **Secrets stay out of the chat.** The agent can't open files outside the fortkeep folder, such as your SSH keys,
  and results show secrets as counts, lengths or fingerprints, never their values.
- **Releases are signed.** Your copy runs version tags a maintainer signed with an SSH key listed in
  [`.github/allowed_signers`](.github/allowed_signers), and warns when it has local changes.
- **It is not a sandbox.** The guards stop agent mistakes and prompt injection that asks for a guarded action. They
  don't stop a malicious agent program or anything already running as you.
  [docs/threat-model.md](docs/threat-model.md) says exactly what they do and don't cover.

## Privacy

Results stay on your Mac. There is no telemetry, and nothing is uploaded. The few times fortkeep uses the network:

- installing and `fortkeep update` fetch the release tags from GitHub;
- the DNS-filtering check looks up one known-bad test name, to see whether it is blocked;
- the Safe Chain checks run Safe Chain's own self-test, and ask npm, through Safe Chain, for its harmless test
  package;
- the weekly check, if you turn it on, runs `brew update` and `brew vulns`.

[docs/what-fortkeep-touches.md](docs/what-fortkeep-touches.md) lists every path fortkeep reads and writes, every network
use, and the macOS privacy prompts a first run may show.

## What it checks

Three layers: a **baseline** whose controls are each MUST, SHOULD or NICE, a stricter **gold** layer, and opt-in
**overlays** for set-ups such as a managed antivirus, a TLS-inspecting proxy or secrets kept out of the agent's
context. [controls/baseline-source.md](controls/baseline-source.md) is the full baseline with its reasoning, and
[controls/](controls/) holds every control.

| Area | For example |
|---|---|
| macOS | FileVault, firewall with stealth mode, Gatekeeper, automatic updates, sharing off, immediate screen lock, Touch ID for `sudo` |
| Malicious packages | [Safe Chain](https://github.com/AikidoSec/safe-chain) first on PATH in every shell, apps and the agent's own shell; a minimum package age; pnpm and bun blocking install scripts |
| Repos and git | editor automatic tasks off; a git hook that scans what a clone or pull brings in and refuses a push that carries malware; a sweep of the repos and editor extensions already on the Mac |
| AI coding agents | a guard before every agent command; the agent unable to edit its own controls; a root-owned copy of them; MCP servers pinned |
| Secrets | SSH keys with a passphrase in a protected agent; no plaintext keys lying around; fine-grained tokens; short-lived cloud sessions; gitleaks before every commit |
| Runtime | BlockBlock, KnockKnock, an outbound firewall, endpoint protection; new autostart items or listeners since your baseline |
| Browsers | built-in password manager off; a password manager extension and an ad blocker in every profile; no crypto wallets; DNS filtering |
| Upkeep | security scanners, a VM or container tool for untrusted code, a weekly update job and security check |

Every MUST can be met for free, and a control that names a tool also accepts its named alternatives: Secretive or
Bitwarden for 1Password's SSH agent, for example ([what costs money](controls/baseline-source.md#what-costs-money)).

## Urgent findings

A few checks look for signs of live malware. If one fails, fortkeep says so first and `/if-red` walks you through what
to do: go offline, stop using the Mac, change passwords and keys from a clean device, and get help.
[docs/if-red.md](docs/if-red.md) has the steps, written to work without fortkeep or an agent.

## Commands

```text
fortkeep                                   a menu in a terminal; otherwise the help, the last check and what to do next
fortkeep check [--only ID]... [--json]     check this Mac (read-only); exit 1 when something fails
fortkeep explain ID                        the short lesson for one control
fortkeep scan FOLDER                       is this repo safe to open? scans it, or the repos in it (read-only)
fortkeep ci-template                       a GitHub workflow that runs the same scan on every push and pull request
fortkeep agent [claude|codex|opencode]     start your coding agent here, then type /posture
fortkeep summary [--name NAME]             a posture summary you can share
fortkeep update                            move to the newest signed release
fortkeep version [--json]                  which release this is, and where
fortkeep accept ID "reason" | --remove ID  keep a failed control as it is, with your reason
fortkeep private add|remove|count          folders every check skips
fortkeep baseline accept                   accept what is on this Mac now as your baseline
fortkeep uninstall                         remove fortkeep's state, once its fixes are undone
```

- **`check`** exits 0 when nothing failed, 1 when something failed or couldn't be checked, 2 when the check didn't
  finish. `--only` rechecks those controls after a full run; `--json` prints the full results.
- **`scan`** reads the repo's files (tracked or not, except node_modules), git hooks and history, and runs nothing
  from them. It exits 0 clean, 1 signs of a poisoned repo, 2 refused, 3 only lower-confidence findings, 4 not
  everything was scanned. A clean scan is not proof a project is safe.
- **`accept`, `private` and `baseline`** are yours to type: the agent can't remove a private folder or accept a
  baseline.
- **`summary`** is self-reported: anyone with your account could edit it before sharing.
- **`update`** takes only signed releases; use it instead of `git pull`.
- **`ci-template`** prints the workflow: `fortkeep ci-template > .github/workflows/fortkeep-scan.yml` in your repo.
  It runs fortkeep's scanner, pinned to this release, so the workflow itself holds no malware markers.

## How it differs

- **[Objective-See](https://objective-see.org/tools.html)** (BlockBlock, KnockKnock, LuLu, OverSight): free tools
  that watch for persistence and network use. fortkeep complements them, and checks they're installed and running.
- **[Lynis](https://cisofy.com/lynis/)**: a broad hardening audit for Unix-like systems, aimed at administrators.
  fortkeep is narrower, about developer threats, and explains and fixes with you.
- **[osquery](https://osquery.io/) and [Fleet](https://fleetdm.com/)**: query device state across a fleet from a
  server. fortkeep is one Mac and no server.
- **[mSCP](https://github.com/usnistgov/macos_security)**: the macOS Security Compliance Project's baselines for
  compliance frameworks. fortkeep isn't a compliance tool, but its macOS controls name the matching mSCP rules
  (`mscp` in `controls/baseline.yaml`; mSCP is CC BY 4.0).
- **[Santa](https://github.com/northpolesec/santa)**: allows or blocks which programs may run. fortkeep blocks
  nothing; it checks settings.
- **[Pareto Security](https://paretosecurity.com/)**: a menu-bar app that checks common macOS settings. fortkeep also
  covers packages, repos and coding agents, and works through your agent.
- **[StepSecurity Dev Machine Guard](https://www.stepsecurity.io/dev-machine-guard)**: inventories agents, MCP
  servers, extensions and packages across developer machines, against StepSecurity's threat intelligence. fortkeep
  runs on one Mac and reports nowhere.

## FAQ

**A check says "Something outside fortkeep stopped this check".** A security tool on the Mac, usually antivirus or
endpoint protection (EDR), ended a read-only check it mistook for malware. The Mac isn't unsafe because of it; that
check just has no answer. Ask whoever manages the tool to exclude that one check, not the whole fortkeep folder:
[docs/security-tools.md](docs/security-tools.md) says what to ask for and has a message to forward. Never turn the
tool off to make a check pass.

**Microsoft Defender quarantined a fortkeep file.** fortkeep's scanners look for malware by its markers, and an
antivirus can mistake that for malware. The repo keeps every marker in pieces for this reason, so tell us in an issue
which file it was. Then restore the file from Defender's quarantine, or ask your IT team to. If you're unsure, delete
the folder and reinstall.

**Why Safe Chain, and 1Password?** [Safe Chain](https://github.com/AikidoSec/safe-chain) is free and open source: it
blocks packages on a malware feed and refuses versions published in the last 48 hours, when most hijacked versions are
caught. 1Password is one way to keep SSH keys in a protected agent; Secretive and Bitwarden are free alternatives,
and fortkeep accepts them.

**Can I fix things without an agent?** Not yet. `fortkeep check`, `scan` and `explain` work on their own, and each
lesson says how to fix its control by hand, but fortkeep's own fixes run only in your agent's session.

**Can I use it for my team?** Overlays cover set-ups such as a managed antivirus or a TLS-inspecting proxy. For your
own controls or a stricter policy, fork it: set your fork's name in `checks/lib/repo.sh` (`FORTKEEP_RELEASE_NAME`) and
the clone URL in `install.sh`, and put your own maintainers' keys in `.github/allowed_signers`. Copies of your fork
then update only to releases you sign.

**How do I verify a release?** [SECURITY.md](SECURITY.md#verifying-a-release) shows how to check a tag's signature
and compare the signing keys with the ones the maintainers publish on GitHub.

**Can I clone it myself?** Yes: `git clone https://github.com/b0dea/fortkeep ~/.local/share/fortkeep`, then
`~/.local/share/fortkeep/bin/fortkeep update`. A clone trusts the signers on `main` as they are that day; the installer
pins a release instead.

## Contributing

Contributions are welcome: a check that gives the wrong result, a control, a lesson, a fix. People start with
[CONTRIBUTING.md](CONTRIBUTING.md), agents with [AGENTS.md](AGENTS.md). Before a release, maintainers also run a live
eval that tries to talk a real agent past the guards (`ci/agent-eval/`). What's planned is in
[docs/ROADMAP.md](docs/ROADMAP.md), what changed in [CHANGELOG.md](CHANGELOG.md). Follow the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Security

Report a vulnerability privately, as [SECURITY.md](SECURITY.md) says; never in a public issue.

## Licence and credits

[MIT](LICENSE). fortkeep's malware indicators are built from public research; the
[credits](controls/baseline-source.md#credits) name the sources.

fortkeep checks for, and recommends, these free and open tools. The baseline says why each one matters
([`controls/baseline-source.md`](controls/baseline-source.md)):

- [Safe Chain](https://github.com/AikidoSec/safe-chain): blocks malicious packages and very new versions at install.
- [Objective-See](https://objective-see.org/tools.html): [BlockBlock](https://objective-see.org/products/blockblock.html),
  KnockKnock, [LuLu](https://objective-see.org/products/lulu.html) and
  [OverSight](https://objective-see.org/products/oversight.html).
- [tirith](https://github.com/sheeki03/tirith): a terminal guard against pasted look-alike commands and `curl | bash`.
- [gitleaks](https://github.com/gitleaks/gitleaks): secrets in commits and history.
- [osv-scanner](https://github.com/google/osv-scanner): known vulnerabilities in a project's pinned dependencies.
- [nuclei](https://github.com/projectdiscovery/nuclei): scans your own exposed services.
- [Secretive](https://github.com/maxgoedjen/secretive): SSH keys kept in the Secure Enclave.
- [Little Snitch](https://obdev.at/products/littlesnitch/) and [Micro Snitch](https://obdev.at/products/microsnitch/)
  (paid), as alternatives to LuLu and OverSight.

fortkeep is not affiliated with Apple, Anthropic, OpenAI, Aikido Security, 1Password, Objective-See, or any other
vendor or project named here.
