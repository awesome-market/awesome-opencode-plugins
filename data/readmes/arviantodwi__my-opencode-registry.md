# my-opencode-registry

Personal [OpenCode](https://opencode.ai) configuration, versioned and synced across machines. This repository *is* `~/.config/opencode` — OpenCode reads everything here directly, no import step needed.

## Contents

| Path | Purpose |
|---|---|
| `AGENTS.md` | Global agent instructions shared by every session. Portable by design: no usernames or machine-specific paths. |
| `cli.json` | TUI preferences: theme (Catppuccin, system mode), session behavior, tabs, diffs, prompt paste, terminal, notifications/attention, scroll speed. |
| `opencode.json` | Main configuration: default agent (`plan`), MCP servers, websearch provider. |
| `commands/vault-capture.md` | `/vault-capture` — manual review of the current session for knowledge worth capturing to the Obsidian vault. |
| `skills/obsidian-vault/` | Portable Obsidian knowledge-base skill: `SKILL.md`, `scripts/resolve_vault.py`, tests, and its own README. See that README for setup and usage. |

## Machine-local files (never committed)

Kept out of the repo via `.gitignore`:

- `service.json` — contains credentials; must never be committed.
- `*.bak`, `*.backup` — ephemeral backup files.

These stay on each machine and are recreated there as needed.

## Per-machine overrides

**Vault location.** The vault root lives in `~/.config/obsidian-vault/config.json`, outside this repository. It is set on first use through the `obsidian-vault` skill's resolver (`scripts/resolve_vault.py`), which asks for the path, validates it, and saves it. Device-specific paths stay out of the shared config.

**`opencode.json` MCP entries.** Some MCP servers are machine-specific — for example `pencil` points at a macOS binary. On machines where an entry doesn't apply, set `disabled: true` locally and hide the change from git:

```bash
# hide local edits to opencode.json (they won't show as dirty or get committed)
git update-index --skip-worktree opencode.json

# unhide when you intentionally want to change the shared version
git update-index --no-skip-worktree opencode.json
```

## Syncing

On a fresh machine, if `~/.config/opencode` doesn't exist yet:

```bash
git clone git@github.com:arviantodwi/my-opencode-registry.git ~/.config/opencode
```

If the directory already exists with machine-local files, use the init-and-fetch flow:

```bash
cd ~/.config/opencode
git init -b main
git remote add origin git@github.com:arviantodwi/my-opencode-registry.git
git fetch origin
git checkout main
```

Day-to-day:

```bash
git pull                                # bring in changes from other machines
git commit -am "…" && git push          # share changes with other machines
```

Note: OpenCode rewrites `cli.json` when you change TUI settings, so expect it to show as modified occasionally — commit it like any other change.
