# dotfiles

Portable, [GNU Stow](https://www.gnu.org/software/stow/)-managed dotfiles for
**macOS** and **CachyOS/Arch Linux**. Each top-level directory is a Stow package
mirroring the paths it owns under `$HOME`.

## Layout

| Package | Symlinks to |
|---|---|
| `fish` | `~/.config/fish` (config, aliases, functions, plugins) |
| `nvim` | `~/.config/nvim` |
| `wezterm` | `~/.config/wezterm` |
| `starship` | `~/.config/starship` |
| `btop` | `~/.config/btop` |
| `zed` | `~/.config/zed` |
| `git` | `~/.gitconfig`, `~/.config/git/ignore` |
| `claude` | `~/.claude` (CLAUDE.md, settings, agents, commands, rules, skills, MCP server source) |
| `opencode` | `~/.config/opencode` (config, agents, commands, skills) |
| `packages/` | `Brewfile` (macOS) + `pacman.txt` / `aur.txt` (Linux) — not a Stow package |

## Setup on a fresh machine

```sh
git clone https://github.com/jchantrell/dotfiles.git ~/dotfiles
cd ~/dotfiles
./bootstrap.sh
```

`bootstrap.sh` detects the OS, installs packages (Homebrew bundle on macOS,
pacman/AUR on Linux), symlinks every package with Stow, installs fish plugins +
LTS node, syncs neovim plugins from the lockfile, and sets fish as the default
shell.

### Manual follow-ups
- Install the **Codelia** terminal font (paid; wezterm falls back to a Nerd Font).
- `gh auth login` for the GitHub credential helper.
- Restore `~/.ssh` keys if you sign commits.

## Managing packages by hand

```sh
stow --no-folding <package>      # link one package
stow -D <package>                # unlink
stow --no-folding --restow <package>   # re-link after changes
```

`--no-folding` is used everywhere so apps (fish/fisher, claude, opencode) can
write their own runtime state into the real directory alongside the symlinks.

> On an **already-configured** machine, existing real config files will conflict
> with Stow. Back them up (or remove them) first — the happy path assumes a
> fresh box.

## MCP servers

Claude reads MCP definitions from `~/.claude.json` (user scope) — **not** from
anything under `~/.claude/`. That file holds session state/secrets and isn't
tracked, so `bootstrap.sh` registers the servers with `claude mcp add`:
`repo-tools` (source vendored under `claude/`), `chrome-devtools`, and
`context7`. Re-run those commands by hand if the `claude` CLI wasn't installed
at bootstrap time.

## Notes
- **Not tracked:** gaming/GUI apps (manually maintained), plugin/marketplace
  content Claude reinstalls from `settings.json`, and all runtime state
  (sessions, caches, credentials).
- **git** intentionally mirrors the minimal live config. The retired Nix setup
  also configured `delta` + `difftastic`; re-add them if wanted.
- Migrated off the old NixOS/home-manager flake (see git history) to plain Stow.
