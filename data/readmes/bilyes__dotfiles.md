# dotfiles

Configs for macOS (AeroSpace) and Arch Linux (Hyprland + Noctalia).

| Config | Platform |
| --- | --- |
| `git`, `nvim`, `tmux`, `kitty`, `opencode`, `zsh` | macOS and Linux |
| `aerospace` | macOS |
| `hypr`, `noctalia`, `uwsm` | Linux |

## Requirements

- git, zsh and [Oh My Zsh](https://ohmyz.sh/)
- tmux 3.8+
- Neovim 0.12+, plus:
  - make and a C compiler (telescope-fzf-native)
  - the `tree-sitter` CLI (nvim-treesitter)
  - Node.js (copilot.vim)
  - fd and ripgrep (Telescope)
  - yazi 26.8.15+ (file manager)
- fzf 0.60+ and fd (shell functions in `zsh/conf.d/fzf-functions.zsh`; tmux's `prefix ?` uses fzf
  too)
- kitty and these Nerd Fonts: FiraCode, Roboto Mono, JetBrains Mono
- macOS: AeroSpace, plus optionally macmon (CPU temperature in tmux's status bar)
- Linux: Hyprland started through uwsm, and Noctalia, plus:
  - grim, slurp, tesseract and tesseract-data-eng (Noctalia's OCR plugin)
  - wl-clipboard (Ctrl-V paste in zsh)
  - libnotify (notifications from tmux's scratch popup)

## Installation

```sh
git clone https://github.com/bilyes/dotfiles.git ~/.config/dotfiles
~/.config/dotfiles/install.sh
```

The clone can live anywhere: only the links `install.sh` creates point to it, so re-run it after
moving the clone.

`install.sh` can be re-run safely. It:

- links each config, `zsh` included, into `$XDG_CONFIG_HOME` (`~/.config` if unset), moving
  anything already there to `<name>.bak.<timestamp>`
- links each script in `scripts/` into `~/.local/bin`, skipping names something else already uses
  there
- replaces `~/.zshrc`, unless it already loads `zsh/zshrc`, with one that does. The old
  file goes to `~/.zshrc.bak.<timestamp>`; move its machine-specific lines into the new one.
- creates an empty `~/.gitconfig` if there isn't one, so `git config --global` writes there
  instead of into this repo's `git/config`
- installs zsh-autosuggestions, powerlevel10k and TPM
- installs the tmux and Neovim plugins

Afterwards:

- On Linux, log out and back in so uwsm loads `uwsm/env`. Noctalia then writes the kitty and tmux
  colors to `kitty/themes/noctalia.conf` and `tmux/themes/noctalia.conf` (git-ignored). Without
  the tmux one, as on macOS, tmux uses Catppuccin.

## Updating

`install.sh` doesn't update the shell plugins it has already cloned. In zsh:

```sh
git -C "$ZSH_CUSTOM/themes/powerlevel10k" pull
git -C "$ZSH_CUSTOM/plugins/zsh-autosuggestions" pull
exec zsh  # powerlevel10k doesn't support `source ~/.zshrc` after an update
```

## Notes

- `~/.zshrc` is machine-specific: it loads `zsh/zshrc`, and the lines below that are for this
  machine only (work settings, setup that installers append). Lines above it run before
  powerlevel10k's instant prompt, which is where anything that reads input must go. It's a file
  rather than a link so that tools appending to it don't write into this repo.
- `zsh/zshrc` sets up Oh My Zsh, then loads every `*.zsh` file in `zsh/conf.d/` alphabetically,
  and `zsh/p10k.zsh` (the powerlevel10k config) last. A new file in `conf.d` needs no other change.
- `p10k configure` rewrites `zsh/p10k.zsh` from powerlevel10k's template, so edits such as the
  trimmed `POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS` are lost; check `git diff` afterwards. Decline when
  it offers to change `~/.zshrc` (`zsh/zshrc` has its lines), and restart zsh before running it
  again: after it runs, a second run in the same shell writes to `~/.p10k.zsh` instead.
- Machine-specific Neovim plugin settings go in `nvim/lua/plugins/local.lua` (git-ignored).
  lazy.nvim merges it with the plugin specs in this repo.
- `nvim/scripts/test-config.sh` checks that the Neovim config in its checkout loads without errors.
- The scripts in `scripts/` are on `PATH` through their links in `~/.local/bin`; re-run
  `install.sh` after adding one. `tmain` opens a tmux session running btop and fastfetch, which
  need to be installed. Scripts for a single config live in its own `scripts/` folder instead,
  e.g. `noctalia/scripts/export.sh`, which copies Noctalia's current settings into
  `noctalia/config.toml` without the machine-specific ones or the lock screen layout, which
  `noctalia/lockscreen.toml` declares.

#### Terminal tips

In zsh's vi normal mode, `v` opens the current command in `$EDITOR`.

`t` attaches to the last tmux session or starts one; inside tmux, it opens the session picker.
`prefix ?` opens a popup that fuzzy-finds the tmux bindings, copy mode's included; Enter runs the
one picked.

`prefix S` toggles a scratch popup for one-off commands, which keep running once it's hidden. It
opens on a new window while the last command is still running, and a failed command sends a
desktop notification. On macOS, that notification comes from Script Editor, so allow its
notifications in System Settings.

`prefix t`, or `<leader>nt` in Neovim, opens a box to type todos in. `:wq` adds each line to the top
of the todo file (`todo_file` in `nvim/plugin/todo-capture.lua`) as a checkbox, below its heading;
`:q!` cancels.

On macOS, tmux's status bar shows CPU, RAM and GPU usage, plus the CPU temperature once macmon is
installed. A reading turns red from 80%, or 90°C for the temperature.

On Linux, Super + / opens the Noctalia Keymap plugin, which lists the Hyprland bindings with their
descriptions.
