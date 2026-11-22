<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/hero-dark.2efc5ab3.svg">
  <img src="docs/assets/hero-light.1db648a3.svg" alt="aval. Nothing without proof." width="100%">
</picture>

<br/>
<br/>

![macOS](https://img.shields.io/badge/-macOS-000000?style=flat-square&logo=apple&logoColor=white)
![Linux](https://img.shields.io/badge/-Linux-000000?style=flat-square&logo=linux&logoColor=white)
![Windows](https://img.shields.io/badge/-Windows-000000?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0yIDJoOS41djkuNUgyek0xMi41IDJIMjJ2OS41aC05LjV6TTIgMTIuNWg5LjVWMjJIMnpNMTIuNSAxMi41SDIyVjIyaC05LjV6Ii8+PC9zdmc+&logoColor=white)

<br/>

[**What it is**](#what-aval-is) &nbsp;·&nbsp;
[**Guarantees**](#guarantees) &nbsp;·&nbsp;
[**Stack and roadmap**](#stack-and-roadmap) &nbsp;·&nbsp;
[**Install**](#install) &nbsp;·&nbsp;
[**Commands**](#commands) &nbsp;·&nbsp;
[**Inside**](#inside) &nbsp;·&nbsp;
[**Principles**](#principles) &nbsp;·&nbsp;
[**Full guide →**](docs/guide.md)

</div>

<br/>

## What aval is

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/mark-dark.1e2f0412.svg">
  <img src="docs/assets/mark-light.ab7493b7.svg" alt="The aval mark: the a and the check in a single stroke" width="96" align="right">
</picture>

aval is an **engineering harness for AI coding agents**: the rules, memory,
skills, hooks and quality gates that Claude Code and OpenCode work with, plus
the terminal environment they run in. It ships as a single Go binary that is
versioned, covered by tests and installs on macOS, Linux and Windows.

The name is the principle. In Spanish, an *aval* is a **guarantee**, a
co-signature that vouches for something. No rule in aval depends on the agent's
good will: each one is backed by a mechanism that checks it, whether a test, a
hook or a gate with measured results. That is why the **v** in the logo is a
check mark.

<br/>

## Guarantees

| The promise | How it is checked |
| :--- | :--- |
| No secret reaches git | `gitleaks` scans the tree **and the full history** on every test run |
| Nothing ships without a test | Strict TDD: the agent writes a `[tdd-gate]` naming the failing test before any code |
| Nothing visual is approved by eye | A hook blocks UI edits until the design pipeline runs; the gates **measure** contrast |
| One source of truth | The TUI, `--yes`, `update`, `doctor` and `uninstall` all read `install.manifest`; nothing keeps its own list |
| Installing deletes nothing | Anything in the way moves to `~/.aval-backup/<date>/` before linking |
| The agent does not forget | Persistent memory with Engram across sessions and compactions |

<br/>

## Stack and roadmap

aval runs today on a set of proven tools. The roadmap moves every piece of the
**workspace** into aval itself, so that the only external dependency left is the
AI provider you choose. What stays is what the product is built with, ships
through or drives: Go, npm and Homebrew; Git, gitleaks and a headless browser.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/stack-dark.d49559e6.svg">
  <img src="docs/assets/stack-light.0ef176bf.svg" alt="Today: Ghostty is replaced by aval desktop (v0.9.0); tmux, Herdr and yazi by aval core and the aval TUI (v0.7.0); Engram and RTK move behind aval memory and context ports (v0.3.0); Claude Code and OpenCode are driven through aval agent adapters (v0.4.0). Kept: Go, npm, Homebrew, Git, gitleaks, Lightpanda, macOS, Linux and Windows" width="100%">
</picture>

<sub>Official logos of each project (<a href="docs/logos/SOURCES.md">sources</a>).</sub>

### What is configured today and what replaces it

| Job | Today | Replaced by | Ships in |
| :--- | :--- | :--- | :--- |
| Terminal window | Ghostty | **aval desktop**: a native window over `aval core` with an embedded terminal | [v0.9.0](https://github.com/alvaroofernaandez/aval/milestone/5) |
| Sessions, panes and agents | tmux, Herdr | **aval core**: persistent PTYs, spaces, tabs and panes, a socket API, worktree per task | [v0.6.0](https://github.com/alvaroofernaandez/aval/milestone/3) |
| Multiplexer UI, file panel, status bar | tmux, yazi | **aval TUI**: panes, agent list with status, diff review with line comments, file panel | [v0.7.0](https://github.com/alvaroofernaandez/aval/milestone/4) |
| Memory and context | Engram, RTK, code-review-graph | **aval memory** and **aval context**: native ports; today's tools become adapters | [v0.3.0](https://github.com/alvaroofernaandez/aval/milestone/1) |
| Harness glue | gentle-ai, agnix, Node screenshot script | **native aval commands**: `aval lint`, `aval shot` (CDP from Go), hook guard and done gate | [v0.3.0](https://github.com/alvaroofernaandez/aval/milestone/1) |
| Agent configuration | One config file per agent | **aval agents**: one config model with an adapter each for Claude Code, OpenCode, Codex and Gemini | [v0.4.0](https://github.com/alvaroofernaandez/aval/milestone/2) |
| Agent runtime | Claude Code, OpenCode | Stays. An own runtime on the provider's SDK is only **evaluated** for v1.0 | [v1.0.0](https://github.com/alvaroofernaandez/aval/milestone/6) |

### The desktop app

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/desktop-dark.872815f5.svg">
  <img src="docs/assets/desktop-light.7d1e149d.svg" alt="The aval desktop mark: the aval mark inside an app frame, followed by a terminal cursor" width="96" align="right">
</picture>

**aval desktop** is where the roadmap ends up: one lightweight app that is
shell, multiplexer and agent workspace at once, built on `aval core` and sharing
the TUI's features. Its mark is the aval mark inside an app frame, followed by a
terminal cursor.

### Milestones

| Version | Goal |
| :--- | :--- |
| [v0.1.0](https://github.com/alvaroofernaandez/aval/milestone/12) | First release: signed binaries, npm packages, Windows support |
| [v0.2.0](https://github.com/alvaroofernaandez/aval/milestone/13) | Maintainability: one local check equal to CI, generated CLI reference, architecture map, dependency and size budgets |
| [v0.3.0](https://github.com/alvaroofernaandez/aval/milestone/1) | Native harness core: guard, secrets, formatter, done gate, lint, shot, memory and context ports |
| [v0.4.0](https://github.com/alvaroofernaandez/aval/milestone/2) | Agent runtime adapters |
| [v0.5.0](https://github.com/alvaroofernaandez/aval/milestone/7) | Local observability and distribution: insights, usage, history, bench, update channels, Homebrew tap |
| [v0.6.0](https://github.com/alvaroofernaandez/aval/milestone/3) | aval core |
| [v0.7.0](https://github.com/alvaroofernaandez/aval/milestone/4) | aval TUI, and the retirement of tmux, Herdr and yazi |
| [v0.8.0](https://github.com/alvaroofernaandez/aval/milestone/9) | Development workflow: `aval init`, commands, rule-compliance evals |
| [v0.9.0](https://github.com/alvaroofernaandez/aval/milestone/5) | Desktop app, remote machines and personalization |
| [v1.0.0](https://github.com/alvaroofernaandez/aval/milestone/6) | Stable contract, and an evaluation of an own agent runtime |

Each issue is written as a spec an AI agent can implement directly. The full
plan lives in the [pinned roadmap issue](https://github.com/alvaroofernaandez/aval/issues/23).

<br/>

## Install

```sh
npx @alvaroofernaandez/aval@next   # prerelease from npm, or a binary from Releases
go install github.com/alvaroofernaandez/aval/cmd/aval@latest
git clone https://github.com/alvaroofernaandez/aval.git ~/aval && cd ~/aval

aval                  # TUI: choose what to install
aval --yes --dry-run  # no TUI: shows what it would do, touches nothing
aval --yes            # no TUI: installs everything that applies (--copy copies instead of linking)
```

`aval` looks for `install.manifest` in the repo: run it inside the clone or pass `--repo <path>`.
Subcommands that do not depend on the repo (`hook`, `design`, `tmux`, `pdf`…) work with the binary alone.
Everything installed on purpose with Homebrew is in the `Brewfile` (`brew bundle --file=Brewfile`).

Private material (company names, client skills) lives outside the repo, in `~/.config/aval/private`
(or `$AVAL_PRIVATE_DIR`): a `settings.json` that `aval sync` merges on top and a `links.manifest` that it links.

> [!NOTE]
> Until v0.1.0 is final, npm packages and binaries are prereleases: npm serves them under the `next` tag.

<br/>

## Commands

| Command | What it does |
| :--- | :--- |
| `aval doctor` | Checks links, hooks, agents and settings (`--fix`, `--json`, `--security`) |
| `aval sync` | Writes what the repo manages into `~/.claude/settings.json` and Codex/Gemini; transactional (`--dry-run`, `--check`) |
| `aval update` | `git pull` and links what is new (`--dry-run`) |
| `aval restore` · `aval uninstall` | Undo an install or sync from `~/.aval-backup` (`--list`, `latest`, `<id>`, `--pin`) · remove only this repo's links |
| `aval budget` | Always-on context per agent and the latency of each hook; exits 1 when over budget |
| `aval review assess` | Risk level of the diff, from git alone, and which reviewers to run |
| `aval rules sync` | Mirrors the shared rules of `CLAUDE.md` and the lessons into OpenCode's `AGENTS.md` (`--check`) |
| `aval hook <name>` | `lessons` · `design-gate` · `design-shot-stop` · `rtk-rewrite` · `repo-profile` · `pre-push` |
| `aval statusline` | Claude Code status line |
| `aval design ack <surface>` · `aval design gate <…>` | Design pipeline ack · measured gates: `contrast`, `tokens`, `pairs`, `hardcodes`, `theme-refs`, `component`, `emoji`, `native` |
| `aval tmux <…>` | `sidebar-toggle`, `sidebar-follow`, `sidebar-watch`, `open-file`, `close-file`, `paste-router`, `statusbar`, `launch` |
| `aval macos <…>` | `defaults`, `screenshot-clipboard install` / `copy` |
| `aval kiri up` · `aval docker cleanup` | Gets Docker ready on Kiri · safe prunes (`--dry-run`) |
| `aval pdf init` · `aval pdf assets` | PDF report project · `assets/brand.css` |
| `aval reap-orphan-tests` | Ends orphaned test processes (`--min-age`, `--dry-run`) |
| `aval release <…>` | Cuts versions, release candidates and promotions: [releasing](docs/releasing.md) |
| `aval dev` | Try aval in a sandbox that never touches your machine: [dev mode](docs/devmode.md) |

Details for each one are in the [guide](docs/guide.md#️-commands).

<br/>

## Inside

| | What | Details |
| :--- | :--- | :--- |
| `config/claude` · `config/opencode` | Instructions, agents, hooks, commands | [Agents](docs/guide.md#-agents) |
| `skills/` | Skills shared by every agent | [Skills](docs/guide.md#-shared-skills) |
| `config/ghostty` · `config/yazi*` · `config/herdr-*` · `home/tmux.conf` | Terminal, status bar, yazi sidebar, Herdr | [Status bar](docs/guide.md#-status-bar) · [Sidebar](docs/guide.md#-file-sidebar) |
| `home/` | zsh, p10k, git | [Shell](docs/guide.md#-shell-and-tools) |
| `cmd/aval` · `internal/` · `npm/` | The binary, by domain, and its packaging | [Map](docs/guide.md#️-repository-map) |
| `install.manifest` | What is installed and where: the single source | [Installation](docs/guide.md#-installation) |
| `.goreleaser.yaml` · `.github/workflows/release.yml` | SemVer versions, binaries with verifiable provenance and npm packages | [Releasing](docs/releasing.md) · [Changelog](CHANGELOG.md) |
| `tests/` | Go integration tests | [Tests](docs/guide.md#-tests) |

<br/>

## Principles

- **One Go binary.** All of aval's own logic is Go; no shell or Python of its own, except the zsh dotfiles (`home/`) and the 3-line `.githooks/pre-push` shim (git needs an executable).
- **Declarative manifest.** `install.manifest` says what is installed and where; the code reads data, not paths.
- **No vendored upstream.** Dependencies are modules, not copied trees.
- **Nothing is deleted.** Everything moved aside is kept in `~/.aval-backup` and `aval restore` brings it back.
- **Maintainability first.** A feature that makes aval harder to maintain waits until it does not.

[Contributing](CONTRIBUTING.md) · [MIT License](LICENSE) · [Security](SECURITY.md) · [Code of conduct](CODE_OF_CONDUCT.md)

<br/>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/wordmark-dark.3ba4fd49.svg">
  <img src="docs/assets/wordmark-light.8ec8a19c.svg" alt="aval" width="88">
</picture>

<sub>Images generated with <code>go run ./tools/brand</code> · every stack logo is a trademark of its project</sub>

</div>
