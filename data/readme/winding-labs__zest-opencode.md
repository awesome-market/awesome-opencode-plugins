# Zest for OpenCode

Track opencode sessions in Zest: standups, token analytics, and how the team
actually works across every AI tool.

This repository is the **git-install tree** opencode installs from. There is
no marketplace and no compiled runtime download.

## Install

Works with opencode 2.x (`@opencode/cli`) and 1.18 or newer (`opencode-ai`).

opencode 2.x:

```bash
opencode plugin add github:Winding-Labs/zest-opencode
opencode service restart
```

opencode checks plugins for updates daily; `opencode plugin update` applies them.

opencode 1.x:

```bash
opencode plugin zest-opencode@github:Winding-Labs/zest-opencode -g
```

To update on 1.x, run the same command with the release tag and `-f`
(`…zest-opencode#vX.Y.Z -g -f`) — 1.x never refetches an installed plugin.

Then start opencode and run `/zest-login` in the chat.

Full instructions: https://app.meetzest.com/docs/install/opencode

## What it captures

Sessions, messages, tool calls, models, per-step token usage. Everything is
redacted on your machine before it is sent. Capture runs inside opencode after
every finished turn.

## Commands

| Command | What it does |
|---|---|
| `/zest-login` | Connect this machine to your Zest workspace |
| `/zest-logout` | Sign out of Zest |
| `/zest-status` | Auth, workspace, and sync state |
| `/zest-sync` | Upload queued sessions now |
| `/zest-standup` | Generate today's standup |
| `/zest-enable` | Enable remote sync of sessions to Zest |
| `/zest-disable` | Disable remote sync (keep capturing locally only) |
| `/zest-workspace` | View or switch workspace |
| `/zest-privacy` | View or configure privacy redaction |
| `/zest-ignore` | Stop tracking the current folder |
| `/zest-unignore` | Resume tracking the current folder |

Command output is relayed by the model, so each command costs one short model
call.

## Notes

Source lives in the Zest monorepo; this repository is the distribution
mirror and is regenerated on every release.

## License

Proprietary — see LICENSE.md. Third-party components included in this
distribution are listed in THIRD-PARTY-NOTICES.md.

Questions: hi@winding.ai
