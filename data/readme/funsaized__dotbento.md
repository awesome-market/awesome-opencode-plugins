# Dotbento

An opinionated bootstrap for the development machines I support:

- macOS with Zsh, Ghostty, Starship, Zed, Neovim, OpenCode, and Pi
- Omarchy Linux with its shell and terminal defaults, plus Zed, Neovim,
  OpenCode, and Pi configuration

Dotbento intentionally does not replace Omarchy's Bash, Starship, or terminal
configuration.

## Documentation

The [design notes](docs/README.md) explain the decisions and tradeoffs behind
each supported tool:

- [bootstrap](docs/bootstrap.md) and [Git ownership](docs/git.md)
- [Ghostty](docs/ghostty.md), [Zsh](docs/zsh.md), and
  [Starship](docs/starship.md)
- [Neovim](docs/neovim.md), [Zed](docs/zed.md), and
  [OpenCode](docs/opencode.md) and [Pi](docs/pi.md)
- the shared [visual system](docs/visual-system.md)

## Install

```bash
git clone https://github.com/funsaized/dotbento.git ~/dotbento
cd ~/dotbento

./install.sh --dry-run             # inspect config changes
./install.sh                       # asks before changing files
./install.sh --packages            # also asks before installing dependencies
./install.sh --packages --yes      # approved, non-interactive bootstrap
```

Existing files are moved to `<name>.bak-<timestamp>` before replacement.
Python 3 is required to merge Pi settings. Package installation never happens
unless `--packages` is passed. Without
`--yes`, all changes require interactive approval.

Dotbento detects macOS and Omarchy Linux. Other platforms stop without making
changes.

## What gets configured

| Config | macOS | Omarchy Linux |
|---|---:|---:|
| Zed | symlink | symlink |
| Neovim | symlink | copy |
| OpenCode | symlink | symlink |
| Pi | instructions/prompts/skills symlink; settings merge | instructions/prompts/skills symlink; settings merge |
| Git | included from existing config | included from existing config |
| Zsh, Starship, Ghostty | symlink | keep Omarchy defaults |

Neovim is copied on Omarchy because `omarchy-nvim-refresh` owns and replaces
`~/.config/nvim`. Re-run Dotbento after an Omarchy Neovim refresh to restore
this opinionated setup. macOS uses a symlink so edits remain visible to Git.

`XDG_CONFIG_HOME` is respected, falling back to `~/.config`.

## Neovim

The LazyVim setup matches the plugins enabled on the reference Omarchy machine:

- Neo-tree, Snacks explorer, dial, and inc-rename
- JSON and SchemaStore support
- Markdown rendering and preview
- TypeScript with vtsls (types and navigation)
- Oxc extras: oxlint diagnostics and oxfmt via `<leader>cf`
- DAP core (generic debugger UI) and Neovim-Lua DAP
- the standard LazyVim editing, completion, Git, diagnostics, and UI plugins

On Omarchy, Neovim loads the current theme from
`~/.local/state/omarchy/current/theme/neovim.lua` at startup. On macOS it uses
the bundled Aether/Gruvy Glass fallback. Restart Neovim after changing an
Omarchy theme; Dotbento deliberately avoids a live-reload watcher and a cache of
every possible colorscheme.

Remote sessions retain OSC 52 clipboard support, with Wayland integration on
Omarchy and `pbcopy`/`pbpaste` integration on macOS.

## Zed

Zed uses oxfmt and oxlint for JavaScript, TypeScript, JSON, and JSONC. Other
languages use their language server formatter. Prettier is disabled, and Java
is discovered from the machine rather than a versioned Homebrew or SDKMAN path.

The tracked settings contain no API keys, so they can remain symlinked. Configure
MCP servers and credentials outside this repository.

## OpenCode

`opencode/opencode.jsonc`, `opencode/AGENTS.md`, and `opencode/plan-agent.md`
are linked into the detected XDG config directory. The adversarial review skill
definition is tracked in `opencode/skills/plan-review-adversarial/SKILL.md`.
Authentication remains in OpenCode's own credential store. Restart OpenCode
after changing OpenCode files; configuration is loaded at startup.

## Pi

`pi/AGENTS.md`, the review/planning/handoff templates in `pi/prompts`, the
`plan-review-adversarial` skill, and `pi/pinata.json` (per-role models for
[pinata](https://github.com/funsaized/pinata) subagents) are linked into
`~/.pi/agent` (or `PI_CODING_AGENT_DIR`). `pi/settings.json` is merged into the machine's settings
with a backup when changes are needed; it enables codemode by default while
preserving the machine's theme, packages, device identity, and unrelated
preferences. Authentication and sessions are never copied into this repository.

The model cycle contains OpenAI GPT-6 Luna at xhigh (default), GPT-6 Astra at
medium, GPT-6.1 Sol at low, and DeepSeek V4.1 Flash at max. DeepSeek's API
identifier is `deepseek-flash`.
Per-model compaction budgets target 200k context tokens for the OpenAI models
and 400k for DeepSeek with the current Pi catalog limits. Cache-miss notices are
enabled. See [context management](docs/pi.md#context-management) for the retained
history budgets and catalog assumptions.
Run `/reload` after resource changes; start a new session to apply startup model
defaults. Existing sessions can restore their previous model.

Use `/review [focus]` in a fresh session for independent adversarial review. It
is a prompt, not an enforced read-only agent or an automatic model switch.

Use `/plan <task>` to investigate and maintain root `PLAN.md`, optionally run
`/plan-review-adversarial [plan-path] [feedback-output-path]` (defaults: `PLAN.md`
and `PLAN-REVIEW.md`), then reconcile feedback in the planning session. Start a
fresh Pi session in the repo and run `/implement-plan [plan-path]` to implement
from that durable handoff. These prompts do not switch models or enforce edit
permissions. See [the planning workflow](docs/pi.md#planning-and-fresh-session-handoff).

Install Pi separately using its [installation instructions](https://pi.dev),
then authenticate with `/login`. `--packages` installs Ponytail and
pi-web-access from reviewed commits, plus Pi Atelier 0.13.0, when `pi` is on
PATH. Ponytail is version 4.10.0. For a Pi-only package install:

```bash
pi install git:github.com/DietrichGebert/ponytail@e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156
pi install git:github.com/nicobailon/pi-web-access@ba36f6a3fad8abad3836e3c005ef7aecf2b886d2
pi install npm:pi-atelier@0.13.0
```

Ponytail starts in its own default mode (`full` unless configured otherwise).
Use `/ponytail status` to inspect it or `/ponytail off` to disable it for a
session. Pi Atelier adds a status rail and live sidebar (`/atelier` or F6); its
preferences remain in the local `pi-atelier.json`. Herdr's Pi integration
remains managed by Herdr, not Dotbento.

### Web access and Tavily credentials

`pi/web-search.json` contains **no key**. The installer merges it into a private
machine-local file, not a symlink. Search is restricted to Tavily; page fetching
uses direct HTTP, with browser cookies and hosted extraction fallbacks disabled.
Curator UI, summary generation by default, source-check tooling, and video
features are disabled to keep the initial setup small.

pi-web-access chooses its config path differently from Pi itself:

1. `$PI_CODING_AGENT_DIR/web-search.json` when that variable is set.
2. With `XDG_CONFIG_HOME`, `$XDG_CONFIG_HOME/pi/web-search.json`, unless only the
   legacy `~/.pi/web-search.json` already exists.
3. Otherwise `~/.pi/agent/web-search.json`, with the same legacy-file fallback.

Supply `TAVILY_API_KEY` through a private shell/secret-manager setup, or set
`tavilyApiKey` **only in the machine-local config**. That field also supports an
environment reference such as `${TAVILY_API_KEY}` or a trusted `!command` secret
resolver. Never put the actual key in `pi/web-search.json`, shell commands saved
in history, or repository files. Installation preserves local credentials;
config and backup files are restricted to mode `0600`.

Run `/reload` after installation or config changes. A Tavily search will fail
until a key is available; it will not silently switch to another search provider.

## macOS shell

The Zsh setup initializes Starship, direnv, zoxide, fzf, and optional language
toolchains when they are installed. Homebrew's actual prefix is detected rather
than assuming `/opt/homebrew`.

`--packages` installs the command-line tools, Zsh plugins, Ghostty, Zed,
OpenCode, and the required Nerd Font through Homebrew. Operator Mono remains an
optional commercial font.

## Omarchy

Omarchy's Bash aliases, prompt, terminal, and package conventions remain in
charge. `--packages` uses `omarchy pkg add` only for the editor/tooling packages
Dotbento needs; it does not install a second shell stack.

## Git identity

Dotbento adds its shared Git settings as an include in the global config Git
already uses: `~/.gitconfig` when present, otherwise
`$XDG_CONFIG_HOME/git/config`. Existing identity and credential helpers remain
untouched, and the repository does not track a name or email:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Verification

```bash
./scripts/scan-secrets.sh
bash -n install.sh scripts/scan-secrets.sh zsh/.zshrc
python3 -m unittest discover -s scripts -p 'test_*.py'
XDG_CONFIG_HOME="$PWD" nvim --headless +qa
```
