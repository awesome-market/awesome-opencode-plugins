# opencode-notification-skill

An [OpenCode](https://opencode.ai) agent skill that plays sounds and shows macOS desktop notifications when the agent needs your attention.

- **Ping** + alert when user input or permission is required
- **Tink** + alert when work is complete
- Fully configurable — sounds, alerts, and message text

## Requirements

- macOS (uses `afplay` and `osascript`)
- OpenCode

## Install

Clone the repo and run the install script:

```bash
git clone https://github.com/alesdrobysh/opencode-notification-skill.git
cd opencode-notification-skill
bash install.sh
```

The installer copies the skill files into `~/.config/opencode/skills/notification/` and appends the notification instructions to `~/.config/opencode/AGENTS.md` (creating it if it doesn't exist).

OpenCode loads the global `AGENTS.md` automatically in every session — no manual skill invocation required.

## How it works

`~/.config/opencode/AGENTS.md` instructs the agent to run `notify.sh input` before asking questions or requesting permissions, and `notify.sh done` when it finishes all work. The script fires a macOS notification banner and plays a system sound simultaneously via `osascript` and `afplay`.

## Configure

Edit `~/.config/opencode/skills/notification/config.json`:

```json
{
  "sound_enabled": true,
  "alert_enabled": true,
  "input_sound": "/System/Library/Sounds/Ping.aiff",
  "done_sound": "/System/Library/Sounds/Tink.aiff",
  "input_alert_title": "OpenCode",
  "input_alert_message": "User input required",
  "done_alert_title": "OpenCode",
  "done_alert_message": "Work complete"
}
```

Set `input_sound` / `done_sound` to `null` to fall back to system defaults (Sosumi / Glass).

**Available built-in macOS sounds** (all in `/System/Library/Sounds/`):
`Basso`, `Blow`, `Bottle`, `Frog`, `Funk`, `Glass`, `Hero`, `Morse`, `Ping`, `Pop`, `Purr`, `Sosumi`, `Submarine`, `Tink`
