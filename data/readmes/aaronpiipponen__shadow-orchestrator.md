# shadow-orchestrator

An OpenCode v2 plugin that connects a working session to a shadow orchestrator session in the same workspace.

Plan-based workflows suit large mechanical changes. Interactive UI work is a stream of small decisions, and the plan drifts while the interface changes. A second session above the loop holds the plan, reviews each step, and records cleanup tasks. The working session makes the decisions, and code review belongs to the orchestrator.

## What it does

### Registration

Registration starts an orchestrator session in the current workspace and binds it to that workspace. Each workspace holds one binding, so a registration replaces it. The session receives the configured initial message as a user prompt, uses the selected model, and stays idle until a wake arrives.

The manual mode replaces the configured message with a typed message from a dialog. The terminal UI opens the started session when it shares the OpenCode service.

![Register dialog with the initial message field](assets/shadow-register-manual.png)

### Wake

A wake sends one message to the bound orchestrator session and does not run a turn in the working session. The manual mode replaces the configured wake message with a typed message from a dialog. The automatic mode reports through a synthetic notice, and the manual mode reports through a toast.

A missing binding returns an error that asks for a registration. A missing or archived target clears the binding and returns the same error. The wake runs a turn on the orchestrator's selected model, agent, and variant.

![Wake dialog with the wake message field](assets/shadow-wake-manual.png)

### Commands

| Command | Description |
|---|---|
| `/shadow-register` | Start a shadow orchestrator session for the current workspace |
| `/shadow-register-manual` | Register shadow orchestrator with a message |
| `/shadow-wake` | Wake the shadow orchestrator for the current workspace |
| `/shadow-wake-manual` | Wake the shadow orchestrator with a message |

An empty dialog cancels the command.

## Install and configure

### Requirements

- OpenCode v2.
- Node.js 18 or later for the test suite.

The plugin uses the v2 server plugin API and the v2 terminal UI API. A local plugin directory needs no build step.

### Install

1. Copy the example configuration and edit the messages and repository entries.

```bash
cp config.example.json config.json
```

2. Add the plugin directory to the `plugins` array in `opencode.json` or `opencode.jsonc`. The `config` option points at the configuration file.

```json
{
  "plugins": [
    {
      "package": "/path/to/shadow-orchestrator",
      "options": {
        "config": "/path/to/shadow-orchestrator/config.json"
      }
    }
  ]
}
```

3. Reload OpenCode to load the plugin.

The plugin provides four commands. The server part provides the two automatic commands, and the terminal UI part provides the two manual commands. No files are needed under `~/.config/opencode/commands/`.

### Configure

`config.json` holds the default messages and the repository overrides.

| Key | Type | Meaning |
|---|---|---|
| `logFile` | string | Log path relative to the configuration file. Optional. |
| `default.initial_message` | string | Initial message sent when a registration starts a session. Required. |
| `default.wake_message` | string | Wake message sent to the bound session. Required. |
| `repositories` | object | Directory keys mapped to message overrides. Optional. |
| `paths` | object | Alias of `repositories`. Optional. |

Each repository entry accepts `initial_message` and `wake_message`. Both fields are optional. A missing field uses the value from `default`. When `repositories` and `paths` name the same directory, `repositories` takes precedence.

```json
{
  "logFile": "shadow-orchestrator.log",
  "default": {
    "initial_message": "You are the Shadow Orchestrator for this workspace. Your assigned step is to inspect the workspace, verify that the work is complete, and record every remaining task. Stay silent until you receive a wake message. On each wake, execute the assigned step and report the verification result and the remaining tasks.",
    "wake_message": "Shadow orchestrator wake. Execute your assigned step."
  },
  "repositories": {
    "~/projects/ui-repo": {
      "initial_message": "You are the Shadow Orchestrator for an interactive UI iteration. The working session pairs the user with a fast implementer that executes one small visual decision at a time. Your assigned step is to keep the plan and the big picture stable above that work. On each wake, inspect the workspace, compare the completed step with the decision it implements, verify that the step stays inside the phase scope, run the repository's review checks for the step, and report the review result. Record every deviation, cleanup task, and plan change in the plan so the normal workflow can absorb it. Do not redesign the interface and do not make product decisions. The user does not review code. Stay silent until you receive a wake message.",
      "wake_message": "Shadow orchestrator wake. Another UI step is complete."
    }
  }
}
```

The configuration directory is watched. A saved edit applies without a restart. A save with invalid JSON or a failed validation keeps the configuration in effect and appends the failure to `logFile` when configured.

## How it works

`index.js` is the server part. It loads and watches the configuration, resolves workspace keys, holds the bindings, registers the two automatic commands, and injects prompts. `tui.js` is the terminal UI part. It provides the two manual dialogs and opens the session a registration starts. `rpc.js` connects the terminal UI to the server.

A workspace key is the git root inside a repository and the resolved session directory outside a repository. A configured key expands a leading `~` to the home directory, and a relative key resolves against the configuration directory. Keys match by path segments, and the longest matching prefix wins. An entry overrides only the message fields it sets. The plugin matches the directory of the invoking session, or the terminal UI location when no session is open.

`state.json` sits beside the configuration and holds one binding per workspace. The plugin reads it before each command and writes it after a change, so separate OpenCode processes see the same bindings. A process-wide `Symbol.for` map keeps the same data across a plugin reload. `logFile` holds timestamped error lines. The plugin appends to the file and does not rotate it.

`npm test` runs the offline suite against a mock plugin context.

## Caveats

- The manual commands come from the terminal UI part. A client without that part shows only the two automatic commands.
- A wake starts a model run on the orchestrator's selected model, agent, and variant.
- The plugin reads the configuration when it loads. An invalid configuration file at startup prevents the plugin from loading.

## License

MIT
