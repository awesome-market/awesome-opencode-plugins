# context-workflow

A context-management + compact-relay workflow for opencode, built for **read-heavy, non-pure-code tasks** — reports, multi-document analysis, architecture planning, skill refactors — where you read a lot of files, analyze and plan, then execute or produce a deliverable.

**The problem it solves.** These tasks are context-hungry: every turn pulls in new files, so the total context keeps growing — and you pay for the full window on every request. Once you pass ~100K tokens the cost climbs steeply and long jobs (5h+) become impractical. Interrupting is expensive too — resuming means re-reading big files back into context.

**The insight.** These tasks are step-plannable up front. Each step has a different focus and doesn't need the whole project in context. So instead of dragging everything along, you split the task into steps, keep only what each step needs, and relay state between steps via lightweight JSON files.

**How it works (v2).** Breaks a task into independent steps persisted to `workflow.json`, drops notes summaries the moment key files are read, writes a `handoff.json` relay at step completion, validates the handoff before compact, and restores in one shot after compact — all enforced by **script gates, not prompt soft-rules**. The v2 architecture binds the workflow to the **exact current opencode session** (full-session SHA-256 binding), so the agent calls `wf_*_current` native tools without passing paths every time; a shared library (`wf_common.ps1`) backs every script with schema-v2 identity, transaction journals, and generation-CAS safety. This keeps the window between 100K–150K tokens across multi-hour runs, cutting cost dramatically, while the JSON relay makes long tasks resumable and less error-prone.

Pairs with the `context-workflow-guard` plugin, which registers the native `wf_*` tools, auto-injects token water-level every turn, runs a compact relay pipeline, and gates built-in subagent delegations with a one-time token.

## Core Features

- **Full-session binding (v2)**: the workflow is bound to the exact current opencode session via SHA-256; `wf_current` resolves it, and `wf_*_current` tools derive the workdir automatically — no path passed every call
- **Schema-v2 identity & transactions**: marker/workflow/state/manifest/handoff all match `protocol_version/workflow_id/revision`; every mutation commits inside an exclusive-handle lock with a transaction journal, auto-rollback on interruption; step authority is `step_uid + exact step_dir` only
- **Step-based workflow**: tasks split into independent steps, relayed via JSON, no shared context between steps
- **Notes persistence**: summaries extracted the moment important files are read, surviving compact; quality warnings flag thin summaries on the spot
- **Handoff relay**: a handoff file written at step completion drives the next step's recovery
- **Compact gate & relay**: scripts validate the handoff is complete before compact; compact is forbidden mid-step; after compact, a bounded resume packet (`wf_resume_current`, ≤9000 chars) re-injects brief + plan + handoff + notes
- **Read tracking**: the plugin records successful `Read` / `ctx_execute_file` calls into `manifest.read_files`; "read but not summarized" files trip the done gate
- **Diagnostics & migration**: `wf_doctor` read-only health check (binding/compact/transaction/owner heartbeat); `wf_migrate` upgrades legacy v1 roots to v2 in place (Preview → Apply)
- **Automatic water-level injection**: the plugin injects token levels every turn — no manual probing needed
- **Subagent gate**: built-in `general`/`explore` delegations are paused with a one-time confirmation token, so the main session stays in control of context spend
- **Auto mode (opt-in)**: after `wf_mode_current(mode="auto")`, the plugin continues the next step on session idle, pausing on stall after 3 retries

## Installation

### 1. Install the skill

Copy the `skills/` directory into opencode's skill discovery location:

```powershell
# Windows
Copy-Item -Recurse skills "$env:USERPROFILE\.agents\skills\context-workflow"

# macOS / Linux
cp -R skills "$HOME/.agents/skills/context-workflow"
```

### 2. Install the guard plugin

The plugin registers the native `wf_*` tools and the water-level/compact/subagent hooks. Copy the `plugins/` directory into opencode's plugin directory:

```powershell
# Windows
Copy-Item -Recurse plugins "$env:USERPROFILE\.config\opencode\plugins\context-workflow-guard"

# macOS / Linux
cp -R plugins "$HOME/.config/opencode/plugins/context-workflow-guard"
```

> The plugin resolves the skill scripts at module load via `CONTEXT_WORKFLOW_SKILL_DIR` env → the installed copy (`~/.agents/skills/context-workflow/scripts`). To point at a custom location, set `CONTEXT_WORKFLOW_SKILL_DIR` and restart opencode. Do not hardcode absolute paths in `index.js`.

### 3. (Optional) run-long-script tool

If your long tasks run heavy scripts (tqdm/akshare/PDF parsing, typically >30s), the standalone [`run-long-script`](https://github.com/Thexinyi/run-long-script) tool redirects stdout/stderr to disk so progress bars never pollute the agent context, and a PowerShell watchdog auto-kills stuck processes. Install it separately if needed — context-workflow works without it.

### 4. Verify

Restart opencode, load the `context-workflow` skill, and run the `wf_current` tool. If it returns `WF_SESSION_NOT_BOUND` (no active binding yet), installation is done — call `wf_new` to create your first workflow.

## Default Working Directory

`wf_new` takes a `-ParentDir` parameter (the workflow's parent directory); the workflow root is created as a sibling under it. Without `-ParentDir`, the fallback is the user home directory (`$env:USERPROFILE` / `~`), so the workflow root lands at `~/<task-name>`.

Resolution order: `-ParentDir` explicit parameter → `$env:USERPROFILE` (user home) fallback.

Legacy v1 roots (created with `-WorkDir`) keep working via `-WorkDir/-StepId`; run `wf_migrate` to upgrade them to v2 in place.

## Quick Start (v2 native tools)

```text
# 1. Create the workflow (first action after loading the skill). Binds to the current session.
wf_new(task_name="my-task", plan_json='[{"id":"S01","name":"Step 1","goal":"Goal","actions":["Action 1"],"depends_on":[],"est_budget_tokens":60000}]')

# 2. Start the next runnable step (derives workdir from the session binding)
wf_start_next(key_files="C:/path/file.pdf")

# 3. After reading an important file, drop a summary
wf_note_current(source_file="C:/path/file.pdf", content="key info extracted")

# 4. Complete the step (validates handoff + that every key_file/read_files has notes)
wf_finish_current()

# 5. Compact sequence: guard check -> wf_compact -> resume after compact
wf_guard_current()
wf_compact()          # the plugin auto-executes compact at turn end; end your reply after it returns
wf_resume_current()   # after compact, re-injects brief + plan + handoff + notes

# 6. Archive when everything is done
wf_archive_current()
```

Legacy `*.ps1` scripts remain available for environments without the plugin tools; see `skills/SKILL.md` for the full tool manual, and `skills/references/details.md` for schemas and detail-level requirements.

## Water-Level Thresholds

| Total tokens | Level | Action |
|---|---|---|
| < 100K | normal | proceed normally |
| 100K ~ 120K | watch | monitoring starts |
| 120K ~ 140K | compact_recommended | prepare to compact |
| 140K ~ 150K | compact_now | compact immediately after completing handoff |
| >= 150K | compact_now | red line, compact now |

## Prerequisites

- **opencode's built-in compact must not be disabled**: the `wf_compact` tool calls opencode's native `client.session.summarize()` to compress context and depends on that feature working. If auto-compaction is disabled in the opencode config, this framework cannot auto-compact — you'll need to run `/compact` manually.
- **opencode auto-approve permission required**: for stable unattended long runs (5h+), enable opencode's auto-approve permission so the agent can proceed through steps and trigger `wf_compact` without per-action confirmation. With manual approval on, every tool call and compact waits for user input, which breaks the relay timing and defeats the point of an automated workflow.

## License

[MIT](LICENSE)

Copyright (c) 2026 Thexinyi
