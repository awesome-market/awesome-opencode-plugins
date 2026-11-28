# Alonzo v0.1

Alonzo is a visual workflow editor for OpenCode. Design, run, and inspect YAML
workflow diagrams in the browser, with node-by-node messages, logs, routing,
human input, handoffs, and judge checks.

![Alonzo editor demo](docs/assets/alonzo-demo.gif)

**Workflows are executable agent instructions.** They can inspect or change the
selected project. Read node prompts, confirm the target project, and use a
disposable branch or test project for unfamiliar workflows.

## Start Here

1. [Getting Started](docs/GETTING-STARTED.md): install Alonzo and run your first workflow in the editor.
2. [Examples](docs/EXAMPLES.md): choose a safe first workflow.
3. [Troubleshooting](docs/TROUBLESHOOTING.md): resolve plugin, editor, model, and gate issues.

## What You Get

- YAML workflows in `*.alonzo.yaml` files
- Agent, router, and human-gate nodes
- Per-node OpenCode child sessions with `reuse` and `fresh` policies
- Optional user input delivered to the start node as workflow input
- Text handoffs between workflow nodes
- Optional judge retry checks for agent nodes
- JSONL traces and human-gate fallback files
- A browser editor for diagram authoring, execution, logs, and messages

## Repository Layout

- `core/`: workflow format, validator, runner, trace, and bridge protocol
- `adapter/`: OpenCode plugin, session orchestration, and editor bridge
- `controller/`: local controller for editor server discovery
- `editor/`: React workflow editor
- `workflows/`: ready-to-open workflows and editor-created project workflows
- `schema/`: JSON schema for `alonzo: 1` workflow files
- `skills/`: workflow authoring and operations instructions

## Requirements

- Bun
- OpenCode 1.17.19
- A target project where workflows may inspect or change files

Install repository dependencies from the root:

```sh
bun install
```

## Use The Editor

From the Alonzo checkout, start the local stack for an installed project:

```sh
bun run ui -- --project /path/to/project
```

The launcher starts OpenCode, the controller, and the editor, then waits for the Alonzo bridge. Open the printed editor URL, normally `http://127.0.0.1:5173`.

The editor is automatically scoped to the launcher target project. Its project
picker lists editable workflows directly under that project's `workflows/`
directory. The editor creates new workflows in the same directory.

The installer adds `workflows/ping.alonzo.yaml`, a minimal one-node connectivity
check. The source checkout also includes `workflows/hey.alonzo.yaml` as an
optional interactive demo; copy it into a target project's `workflows/` directory
when wanted.

To open a different project, install Alonzo there and start another launcher with
that project's path. A browser cannot register an arbitrary local directory with
the running OpenCode server, so the editor does not provide a directory picker.

Default ports are OpenCode `4096`, controller `4097`, and editor `5173`. Override them when needed:

```sh
bun run ui -- --project /path/to/project \
  --opencode-port 4098 \
  --controller-port 4099 \
  --editor-port 5174
```

One launcher manages one project. Multiple stacks can run only when every configured port is distinct. The launcher fails before startup when a requested port is occupied. Press `Ctrl+C` in the launcher terminal to stop the local stack.

## Use The TUI

For a terminal-only run, open the OpenCode TUI from the installed target project:

```sh
cd /path/to/project
opencode
```

Then run a workflow with `/alonzo`:

```text
/alonzo workflows/ping.alonzo.yaml
```

An optional prompt after the workflow path becomes the start node's workflow input:

```text
/alonzo workflows/ping.alonzo.yaml Hello from the TUI.
```

Stop the current run with:

```text
/alonzo stop
```

## Local Runtime Data

Alonzo keeps project-local runtime data in `.opencode/alonzo/.alonzo/`:

- `.opencode/alonzo/.alonzo/trace/run-*.jsonl`: execution traces
- `.opencode/alonzo/.alonzo/human/`: human-gate fallback requests and responses

Bridge discovery is local controller state under `~/.config/opencode/alonzo/bridges/`. Both locations can contain project-sensitive data and are ignored by Git.

## Documentation

- [Getting Started](docs/GETTING-STARTED.md)
- [Editor Guide](docs/EDITOR.md)
- [Examples](docs/EXAMPLES.md)
- [Running Alonzo](docs/RUN.md)
- [Workflow Format](docs/FORMAT.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Changelog](CHANGELOG.md)
- [Workflow Authoring Skill](skills/alonzo-workflow-authoring/SKILL.md)
- [Workflow Operations Skill](skills/alonzo-workflow-ops/SKILL.md)

## Install Into Another Project

Use the cross-platform Bun installer to add Alonzo's project-local OpenCode files
to a target project:

```sh
bun scripts/install-opencode-template.ts /path/to/target-project
```

The installer does not modify an existing target `opencode.json`. OpenCode
automatically discovers Alonzo from `.opencode/`. The generated plugin wrapper
imports this checkout's `adapter/src/plugin.ts`, so keep this checkout available
while the target project uses Alonzo.

If the launcher cannot start, a port is occupied, or the editor cannot connect,
see [Troubleshooting](docs/TROUBLESHOOTING.md) before retrying.

## Verify

Run these commands from the repository root:

```sh
bun run typecheck
bun run test
bun run test:controller
bun run test:editor
bun run test:e2e
bun run test:repo
```
