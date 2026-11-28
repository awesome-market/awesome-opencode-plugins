<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img alt="knowledge" src="assets/banner-light.svg" width="880">
  </picture>
</p>

<p align="center"><b>English</b> | <a href="i18n/README.tr.md">Türkçe</a> | <a href="i18n/README.es.md">Español</a> | <a href="i18n/README.pt.md">Português</a> | <a href="i18n/README.fr.md">Français</a> | <a href="i18n/README.de.md">Deutsch</a></p>

<!-- Pills and hero: one SVG per theme, holding every language; the reader's browser languages pick
     one (assets/i18n.mjs). i18n/README.<lang>.md uses the <name>-<lang>-<theme>.svg files instead. stars
     and latest are rewritten daily and on each release by .github/workflows/badges.yml onto the
     orphan `badges` branch; the rest are drawn by assets/build.ts. downloads joins row one once a
     release has assets. -->
<p align="center">
  <a href="https://github.com/atlasatakahraman/knowledge/stargazers"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/atlasatakahraman/knowledge/badges/stars-dark.svg"><img alt="stars" src="https://raw.githubusercontent.com/atlasatakahraman/knowledge/badges/stars-light.svg" height="28"></picture></a>
  <a href="https://github.com/atlasatakahraman/knowledge/tags"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/atlasatakahraman/knowledge/badges/latest-dark.svg"><img alt="latest version" src="https://raw.githubusercontent.com/atlasatakahraman/knowledge/badges/latest-light.svg" height="28"></picture></a>
</p>
<p align="center">
  <a href="#harnesses"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/badges/harnesses-dark.svg"><img alt="harnesses: Claude Code, Codex, opencode, Claude app" src="assets/badges/harnesses-light.svg" height="28"></picture></a>
  <a href="#requirements"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/badges/platforms-dark.svg"><img alt="platforms: Windows, Arch pending" src="assets/badges/platforms-light.svg" height="28"></picture></a>
</p>
<p align="center">
  <a href="docs/benchmark.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/badges/prompt-hook-dark.svg"><img alt="prompt hook: ~17.8 ms" src="assets/badges/prompt-hook-light.svg" height="28"></picture></a>
  <a href="docs/benchmark.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/badges/guard-dark.svg"><img alt="guard: ~24.9 ms" src="assets/badges/guard-light.svg" height="28"></picture></a>
  <a href="docs/benchmark.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/badges/tokens-dark.svg"><img alt="tokens: 82% lower than grep" src="assets/badges/tokens-light.svg" height="28"></picture></a>
  <a href="docs/benchmark.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/badges/find-dark.svg"><img alt="knowledge find: 33/33, ~33 ms" src="assets/badges/find-light.svg" height="28"></picture></a>
</p>

<p align="center"><b>Knowledge that grows with you and your agents.</b><br>
Memory and rules for coding agents. Who you are, what you ruled out and what you
decided, loaded into every session of every harness you use.</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img alt="Agents forget you. Who you are and how you work load first, whole, in every session. They ignore your rules. A guard on every tool call denies what you ruled out: git push waits for your yes. Nobody writes it down. Sessions, commits and decisions record themselves. Each tool keeps its own memory. Claude Code, Codex, opencode and the Claude app read one vault." src="assets/hero-light.svg" width="100%">
</picture>

## Quick start

### Let your agent do it

Paste this into Claude Code, Codex or opencode:

```text
Install knowledge for me from https://github.com/atlasatakahraman/knowledge.
Follow its AGENTS.md, show me each step's output, and ask before anything you write.
```

[AGENTS.md](AGENTS.md) walks it through the same steps as below, with the output each one should
print. It shows you the setup plan, applies it only on your yes, then asks which rule packs you want,
fills in who you are and your rules with you one question at a time, and offers a private GitHub
repo for the vault.

### Requirements

`git`, `gitleaks`, Claude Code (`claude`) and the GitHub CLI (`gh`, for the build provenance).
Each release has a signed archive per platform, checked before you extract it
([docs/verify.md](docs/verify.md)). Without one for your platform, the binary builds from source
with the Rust toolchain (`rustup`), in two to three minutes.

### By hand

```bash
git -c advice.detachedHead=false clone --branch v0.13.2 https://github.com/atlasatakahraman/knowledge ~/dev/knowledge
# the binary: your platform's release archive, verified, into ~/.local/bin (docs/install.md),
# or from source: cargo install --path ~/dev/knowledge --locked
knowledge setup --plan
knowledge setup --apply <id>      # the id is the plan's last line
```

`--plan` writes nothing. It lists every file it would create or change, for Claude Code and then
every other harness it finds, and ends with the plan's id. `--apply <id>` refuses if anything moved
since, then writes exactly that plan. A new vault lands at `~/knowledge`; an existing folder can be
adopted instead. Flags, Windows, and every step by hand: [docs/install.md](docs/install.md).

### After a new vault

Make it yours. Fill `00-Meta/Identity.md` and `00-Meta/Hard-Rules.md`
(`grep -rn "^<!-- FILL:" ~/knowledge/00-Meta` lists what is left), and replace the questions in
`00-Meta/retrieval-cases.json` with ones the vault must always answer. `knowledge doctor --repair
--pretty` builds the first index, and `knowledge rules list` with `rules enable <pack>` turns on
the rule packs you want.

## A session, in practice

Real output from the public fixture [docs/benchmark.md](docs/benchmark.md) uses: this repository's
docs as the vault. Paths are shortened and long snippets cut.

**You type a prompt.** The prompt hook adds the notes that answer it before the agent reads a word:

```text
> update knowledge to the newest release

Relevant notes from the knowledge vault (~/knowledge):
- **update** — $ knowledge update --plan  knowledge 0.13.2, x86_64-pc-windows-msvc …
- **verify** — …from `knowledge setup --plan`, or update.md over an older version. How a release …
- **release** — …A release is eight archives (build.yml's targets), one SHA256SUMS over them, …
```

**The agent looks something up** in one call, from any folder, instead of grep and a pile of reads:

```text
$ knowledge find "check the signature on a downloaded release"
release — ~/knowledge/20-Knowledge/knowledge/release.md
  …download v0.13.2 -R atlasatakahraman/knowledge -p SHA256SUMS … 5. Check the signature…
verify — ~/knowledge/20-Knowledge/knowledge/verify.md
  …Three checks, each answering a different question: | The signature over SHA256SUMS | …
```

**The agent tries something you ruled out.** The guard answers before the tool runs:

```text
$ git reset --hard HEAD~3
ask: push-destructive-git (nothing-is-committed-until-i-give-an-explicit-go): each push needs
its own yes, and destructive git is the owner's call (Hard-Rules § Git)
```

**The session ends.** Its daily note, its commits and the decisions it made are written into the
vault, and pushed to your own remote for your other machines.

## Harnesses

"Verified" means a live session on a real install (Windows, 2026-11-23); the same checks on Arch
wait for its pass. Every adapter's code path also runs in CI on fixture installs.

| Harness | What it gets | Enforcement | Status |
|---|---|---|---|
| Claude Code | Identity and Hard-Rules imported whole into `~/.claude/CLAUDE.md`; the plugin's hooks on nine events; `/knowledge`; the code map (`knowledge find --code`, `graph --code`) | The guard on `PreToolUse` (shell, edit and MCP calls) with deny and ask; the session-start restore; the pre-commit backstop | Verified |
| Codex CLI | The block written whole into `~/.codex/AGENTS.md`; the plugin's hooks on eight events, pinned to the binary's version; `/knowledge` through `~/.agents/skills`; `knowledge` over MCP, the code map included | The guard on `PreToolUse` (`Bash`, `apply_patch`, MCP calls), deny only: an ask rule is a deny, since Codex cannot ask; hooks run only once you review them; restore and backstop | Verified |
| opencode | The block in `~/.config/opencode/AGENTS.md`; the shim plugin on eight events, seven of which run the binary; `/knowledge` | The guard in `execute.before` (`shell`, `edit`, `write`, `patch`), deny only; restore and backstop | Verified; its compaction and session-delete events only run in the interactive app and were not reached |
| Claude desktop app, Chat | `knowledge mcp`: `find`, `graph`, `read`, and `note`, which asks before it writes | None: no shell and no hooks, so no tool call of ours to guard | Verified |
| ChatGPT app's Codex | The Codex plugin's hooks, once trusted in the CLI | As Codex; hooks not yet trusted are skipped silently | Built, not verified |
| Any other (`generic`) | The block in a file you name, `knowledge find` and `graph`, and `knowledge note` to write back | None at run time: the rules are text only. The pre-commit backstop still runs in every clone `setup` set | Built, not verified |

How a harness is added: [docs/architecture.md](docs/architecture.md#harnesses).

## How it works

One native binary, `knowledge`, answers every hook. No hook starts a JavaScript runtime, and the
vault's index is one SQLite file per machine.

- **Session start** imports who you are and your rules whole, pulls the vault, and puts back any
  rule changed without a relock.
- **Each prompt** gets the names of the notes that answer it, with their best passage
  (~17.8 ms).
- **Each tool call** passes the guard first (~24.9 ms): `deny` or `ask` with the rule's id.
- **Session end** writes the daily note, the commit notes and the decisions, then pushes only those
  records.
- **On demand:** `knowledge find` (notes, repo docs, captured output), `knowledge graph` (how notes
  connect), `find --code` and `graph --code` (where a symbol lives and what uses it), and
  `keep` and `fetch` (long output and web pages, stored and searchable).
- **`knowledge doctor`** checks it all in one run: the index, the questions the vault must always
  answer, links, the records, the rules. Silence at session start means healthy.

What each hook writes and when: `template/00-Meta/Hook-Lifecycle.md`. Every verb, with real output:
[docs/verbs.md](docs/verbs.md).

### Rules and the guard

`00-Meta/Hard-Rules.md` stays one note, loaded whole. Each `##` section is a pack. Each rule is a
bullet that opens with a bold line, and that line's slug is the rule's id. `00-Meta/rules.lock`
(JSON, tracked) holds what the text cannot: each rule's pack, kind, enforcement points and the hash
of its whole text, and the guards. Nothing is added to the primed text. You edit the note, then run
`knowledge rules lock`, or let the agent run it: the guard asks you first.

- **The guard** (`hook pre-tool`, on each harness's pre-tool event for shell, edit and MCP calls)
  splits a shell line into segments and words, and answers `deny` or `ask` with the rule's id. It
  reads only `rules.lock`. It prints nothing when it allows, and on a missing or broken lock it
  allows with one stderr line.
- **The backstop** is `githooks/pre-commit`. It runs the repo's own hook, gitleaks, then
  `rules check --staged`, which fails a commit holding a guard's staged names (`package-lock.json`)
  or a Hard-Rules that disagrees with the lock. `setup` sets it in the vault, the skeleton and
  each checkout a `10-Repos` page names.
- **The restore.** Each session start runs `rules check --restore`. A rule that differs from the
  lock comes back from `HEAD` when `HEAD` matches the lock, and one line says so. Otherwise the
  doctor FAILs until you relock or revert.

**What it cannot stop.** An agent that runs code as you can change any file you can. The guard puts
the plain forms to you: an Edit, `sed -i`, a redirect, `Set-Content`. It cannot judge a wrapper (an
interpreter's `-e`, a substitution, an escape). That case is caught afterwards, by the next
session start's restore and the doctor.

## Why not a memory file

A memory file works until the agent forgets to read it, or reads the copy that belongs to another
folder: Claude Code's own memory is sharded by working directory. Each harness keeps its own, so
what Codex learned never reaches Claude Code. And a rule written in a file is advice; nothing stops
the tool call that breaks it.

Here a hook runs whether or not the agent remembers to. Your rules load whole in every session of
every harness, a guard enforces the ones a command can break, and the records are written by the
hooks, not by the agent's goodwill. Every part has a watcher, because a pipeline like this fails by
going quiet: `template/00-Meta/Why-This-Exists.md`.

## Your data and network

- **The vault is plain Markdown in your own git repository.** Nothing is stored anywhere else but
  the per-machine indexes beside your config, which rebuild from the notes in about a second.
- **No telemetry.** No hook phones a server of ours, and nothing checks for updates on its own.
- **What touches the network:** `git pull` and the records push, to your vault's own remote;
  `fetch`, when you or the agent run it; `update --plan`, when you run it; the headless flush and
  compile, through your harness's own CLI and account.
- **Never read:** harness credentials. The engine runs the harness's CLI and lets it sign in itself.

The full list, and what `fetch` refuses: [docs/security.md](docs/security.md).

## Obsidian is optional

The vault is a folder of Markdown files with `[[wikilinks]]`, and every verb works on it without
Obsidian. Open it in Obsidian if you want the graph view: `setup` colours its groups by note type.

## Commands

Every command is a verb of one binary, `knowledge`. `knowledge <verb> --help` prints the verb's
usage, when to use it and why, and runs nothing. Every flag, with real output:
[docs/verbs.md](docs/verbs.md).

| Command | Use it when | Why |
|---|---|---|
| `find <query>` | you want what the vault says about X and the MOCs did not answer; `--captures`, `--repo` and `--code` search kept output, repo docs and symbols | one call returns the note and the passage that matched, instead of files read into context |
| `graph <note> [<note>]` | you want how two notes connect, or what uses a symbol (`--code`) | ~25 ms from the index, and no file is read |
| `keep <label> --q <query>` | a command's output is over ~2,000 chars and you need part of it | only the matching sections reach the context; the rest stays searchable |
| `fetch <url> --q <query>` | you are reading a page whose address you have | Markdown cut to your query; private addresses are refused |
| `code index` · `code duplicate` | you level every code map at once, or check a monorepo commit for copies | symbol answers at zero tokens; a copy is caught before it is two things to maintain |
| `index` | notes changed outside a session, or `find` misses a note you know is there | every reader uses this index; a stale row answers with an old passage |
| `inject <text>` | a prompt brought the wrong notes | it is the prompt hook's own path, run by hand |
| `events <transcript>` | you review what a past session decided | only the turns that matter, not a transcript of megabytes |
| `note log` · `note decision` | your harness runs no hooks, or the capture missed a decision | the same write-back the hooks do |
| `ledger list` · `ledger promote` | the session start says decisions are waiting | a raw capture becomes a decision record, or is ruled out |
| `doctor` | first, whenever something seems off; after setup or an update | the one place that says which part went quiet |
| `rules lock` · `check` · `guard add` | you edited Hard-Rules, the rules check failed, or a rule needs enforcing | a rule in a file is advice; a guard on every tool call is enforcement |
| `setup --plan` · `--apply <id>` | a new machine or harness, an update, a rules change | nothing is written before you have read the plan |
| `update --plan` | you choose to check for a new version | no telemetry and no auto-update |
| `config [<key>]` | a script needs the vault path, or a hook uses the wrong folder | one source per machine, no hard-coded paths |
| `records` | the doctor's `auth` check names a failed run; the hooks run it otherwise | records reach your other machine; your own commits wait for your yes |
| `flush` · `compile` | the flush canary fires, or a day was missed; the hooks run both | a session never flushed is never remembered |
| `post-bash --backfill <since>` | you committed in a terminal with no agent | every commit's why-body lands in the vault |
| `hubs` | a new note is not yet reachable from `00-MOC-Root` | the hubs are written from the folders, never by hand |
| `usage` | you want what a month cost, by project or by 5-hour window | read from local transcripts, sent nowhere |
| `mcp` | an app speaks MCP but runs no hooks; `setup` registers it | the same index and code map for apps without a shell |
| `hook <event>` | not by hand: `setup` wires each harness to it | one binary runs every harness on the same vault |
| `--version` | after an install or update, and in a bug report | says whether search (SQLite FTS5) works |

## Docs

[Install](docs/install.md) · [verify a release](docs/verify.md) · [update](docs/update.md) ·
[remove](docs/remove.md) · [every verb](docs/verbs.md) · [security](docs/security.md) ·
[troubleshooting](docs/troubleshooting.md) · [benchmark](docs/benchmark.md) ·
[architecture](docs/architecture.md) · [release](docs/release.md), for the maintainer.

## Contributing

How the engine is laid out, its crates, the per-machine config, sync and CI:
[docs/architecture.md](docs/architecture.md). How to work on this repository:
[AGENTS.md](AGENTS.md), second part.

## Third-party tools

Installed from their own upstreams, never vendored here:

- [gitleaks](https://github.com/gitleaks/gitleaks) - MIT. Scans every commit (`githooks/pre-commit`)
  and the records before they are pushed. Without it, nothing is committed.

The fonts drawn into the images (Newsreader, Hanken Grotesk, JetBrains Mono) are SIL OFL 1.1, and
the icons are [Lucide](https://lucide.dev) (ISC).

## License

MIT. See `LICENSE`. The third-party tools above keep their own licences.

Versions up to 0.4.0 were released under GPL-3.0-only and stay available under it; from 0.5.0 on
the skeleton takes no GPL dependency, so the MIT grant stays whole.
