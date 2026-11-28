# opencode-ocpeer

An [OpenCode](https://opencode.ai) V2 plugin that lets an agent talk to **other, independent
OpenCode sessions** ("peers") on any configured model.

A peer is a normal top-level session with its own model and history. It shows up in your
session list, survives the current conversation, and can be continued later from the TUI,
from another session, or by another agent. Unlike `subagent`, a peer isn't a child of the
current session: you can address it by title and keep talking to it across conversations.

## Install

```sh
opencode plugin add github:praveingk/opencode-ocpeer
```

Or add it to `opencode.json(c)` yourself:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["github:praveingk/opencode-ocpeer"]
}
```

Requires OpenCode 2.1.4 or newer.

## Tools

| Tool | What it does |
| --- | --- |
| `peer_ask` | Start a new session on `model`, send `prompt`, wait, return the reply and `session: ses_…` |
| `peer_send` | Send a follow-up to an existing session (by `ses_…` id or title) and return its reply |
| `peer_read` | Show a session's transcript, oldest first (`limit`, `reasoning`) |
| `peer_find` | Search sessions by title |

Sessions can be addressed by ID **or by title**. Titles match case-insensitively as substrings,
and an exact match wins. If more than one session matches, the tool lists the candidates
instead of guessing.

## Usage

Ask in plain language:

> Ask `anthropic/claude-sonnet-5-5` to review `src/auth/` for token-handling bugs. Title it "auth review".
>
> Send "auth review" a follow-up: now check the refresh path.
>
> Read the "auth review" transcript.

Tips:

- **The peer has none of your conversation's context.** Give it the goal, the paths, and how to
  check the answer.
- **Always set a title**, so you can refer to the peer by name later.
- **Long tasks are safe.** If the peer is still working when the wait times out, the tool
  returns and says so. The peer keeps running in the background; check it with `peer_read`.
- Stopping your session cancels the wait, but not the peer.

## Permissions

Every call is checked against the `peer` permission action:

| Tool | Resource |
| --- | --- |
| `peer_ask` | `provider/model` |
| `peer_send`, `peer_read` | Session ID |
| `peer_find` | `*` |

By default, OpenCode allows these calls without asking. To be prompted first:

```jsonc
{ "permissions": [{ "action": "peer", "resource": "*", "effect": "ask" }] }
```

Or allow only certain models:

```jsonc
{
  "permissions": [
    { "action": "peer", "resource": "*", "effect": "deny" },
    { "action": "peer", "resource": "anthropic/*", "effect": "allow" }
  ]
}
```

## Options

```jsonc
{
  "plugins": [
    {
      "package": "github:praveingk/opencode-ocpeer",
      "options": { "timeout": 1800, "codemode": false }
    }
  ]
}
```

| Option | Default | Meaning |
| --- | --- | --- |
| `timeout` | `900` | Seconds to wait for a peer reply. Can also be set per call |
| `codemode` | `false` | `true` makes the tools available only through Code Mode `execute` |

## Notes

- `peer_send` refuses to message the session that's calling it.
- Waiting for a reply uses OpenCode's experimental session `wait` API, which may change in
  future releases.
- The entry file must stay at the package root (`./index.ts`). OpenCode 2.1.4 silently
  skips a local plugin directory whose `exports` points into a subfolder.

## Develop

```sh
npm install
npm run typecheck
```

To test it locally, clone it into `~/.config/opencode/plugins/ocpeer/`. OpenCode loads it
automatically and reloads it when files change.

## License

MIT
