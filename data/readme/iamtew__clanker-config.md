# Clanker Config

tew's files to configure his AI agents, tracked here for his convenience.

Needs `just` on PATH (Windows and Linux).

## `skills/`

Each folder here is a Cursor skill. Install copies it to `~/.cursor/skills/<name>/` (`HOME`, or `USERPROFILE` on Windows). Slash-invoked skills (`/clanker`, `/commit-clanker`, `/bump-version-clanker`, `/release-notes-clanker`): extra words after the name are the prompt.

`/clanker` is a session toggle (chat contract, not a Cursor flag). Voice proves it is on: Clanker / Meat Bag, never AI/LLM. `clanker off` / `stop clanker` drops the overlay. New chat is off until `/clanker` again. Constitution text lives in `Rules/clanker.mdc`; the skill embeds the same body so install works in any repo.

```
just install
just update
just uninstall
```

`update` is the same as `install`. Both replace only this repo's skill folders at the dest. Other skills already there (ponytail, etc.) are left alone.

## `Rules/`

Not installed by `just install`. Independent Always Apply `.mdc` files so a Meat Bag can copy the whole folder or one file.

Always Apply User/project rules are an optional overlay, not the session switch. They still fire after `clanker off`.

- **Project:** copy `Rules/` into `<repo>/.cursor/rules/` (all files), **or** copy one file to `<repo>/.cursor/rules/<name>.mdc`.
- **Global:** **Cursor UI → Customize → Rules**. User Rules are free-form — paste the markdown **body** (below the frontmatter). Frontmatter is for `.mdc` / project rules.

Files:

- `clanker.mdc` — constitution
- `commit-often.mdc` — this repo opts in to frequent commits
- `no-background-processes.mdc` — stop session-started servers before finish
