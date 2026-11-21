# opencode-goal-restart-resume

OpenCode plugin that resumes built-in `/goal` loops after the background service restarts.

OpenCode pauses an active goal when the server process changes, with the reason `The server restarted while the goal was active`. It does not continue that goal on its own. This plugin calls the official `/goal resume` command, which re-arms the goal on the current process and keeps working.

User pauses, round limits, blockers, and other stop reasons are left alone.

Requires OpenCode 2.2 or newer, with the built-in `/goal` command.

## Install

```sh
opencode plugin add github:officialPlocki/opencode-goal-restart-resume
```

Or add it to `opencode.json`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["github:officialPlocki/opencode-goal-restart-resume"]
}
```

OpenCode reloads plugins after the config change. Run `/reload` if a goal is already paused and has not resumed yet.

## What it does

- Watches goal changes and session execution, and sweeps recent sessions shortly after load.
- Resumes only goals paused because the service restarted.
- Skips a busy session during the automatic sweep and resumes it when that turn ends.
- Adds `/goal-restart-resume`, which scans the current location and resumes every matching goal, including busy sessions.

`/goal resume` resets the round budget and sends the normal continuation, so the agent starts working again.

To keep a restarted goal stopped, pause it again or run `/goal clear`. A later pause is recorded as a user pause and is not resumed.

## Disable

Remove the plugin, or add its id to `plugins`:

```jsonc
{
  "plugins": ["-goal-restart-resume"]
}
```

Set `OPENCODE_GOAL_RESTART_RESUME=0` on the OpenCode service process to turn it off without removing the package.

## License

MIT
