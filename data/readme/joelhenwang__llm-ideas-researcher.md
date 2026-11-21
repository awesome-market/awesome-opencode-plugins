# Auto LLM Researcher

`auto-llm-researcher` is a Python-first framework for continuously discovering, ranking, synthesizing, reviewing, and handing off LLM research ideas that can be adapted into experiments for a PyTorch + RoCM model capped at 2.1B parameters.

The project uses OpenCode as the primary agent runtime while keeping ingestion, scoring, persistence, lifecycle management, and Markdown publishing in Python. The tokenizer policy is fixed to GPT-2, so the system filters out ideas that depend on tokenizer replacement or vocabulary redesign.

## What It Does

- Ingests research from arXiv and manual URLs
- Enriches source records with provenance and source-quality metadata
- Scores and shortlists studies with staged, auditable ranking signals
- Synthesizes evidence-aware single-study and mixed-study experiment briefs
- Persists candidates in SQLite and tracks review lifecycle state
- Exports approved candidates as raw handoff payloads for downstream tools such as `auto-llm-innovator`
- Supports unattended daemon runs with run summaries, health inspection, and daemon heartbeat state

## Features

- One-shot CLI research runs
- Long-running daemon mode
- Manual source submission from URLs
- arXiv + general web enrichment pipeline
- SQLite-backed run ledger, source persistence, and candidate lifecycle registry
- Per-topic Markdown and JSON research briefs
- Mixed-study synthesis from previously generated candidates
- Candidate lifecycle commands for review and handoff
- `doctor`, `status`, and `health` commands for setup and runtime inspection
- OpenCode-based synthesis with deterministic fallback output
- Sequential OpenCode execution with a cross-process lock

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
auto-llm-researcher doctor
pytest
auto-llm-researcher run
```

The supported local bootstrap flow is the editable install shown above. Use `python3`, not `python`, when creating the virtual environment. After `pip install -e .`, both `auto-llm-researcher ...` and `python3 -m auto_llm_researcher ...` work, but the CLI entrypoint is the primary interface.

## Core Workflow

1. Add manual URLs if you want to seed the queue with specific papers or blog posts.
2. Run `auto-llm-researcher run` for a one-shot pass or `auto-llm-researcher daemon` for unattended discovery.
3. Inspect recent runs with `status` and runtime state with `health`.
4. Review synthesized candidates with the `candidates` command group.
5. Export approved candidates to `outputs/handoffs/` for downstream use.

## Common Commands

Check local readiness:

```bash
auto-llm-researcher doctor
```

Run one research pass:

```bash
auto-llm-researcher run
```

Add a manual source:

```bash
auto-llm-researcher add-source https://example.com/post-about-efficient-llms
```

Inspect recent runs:

```bash
auto-llm-researcher status --limit 5
```

Inspect runtime health, daemon heartbeat, and lock state:

```bash
auto-llm-researcher health --limit 10
```

Run the daemon:

```bash
auto-llm-researcher daemon --interval-minutes 120
```

Create mixed-study briefs from recent candidates:

```bash
auto-llm-researcher mix-studies --recent-runs 5 --limit 3
```

Review candidate lifecycle state:

```bash
auto-llm-researcher candidates list
auto-llm-researcher candidates show <artifact-id>
auto-llm-researcher candidates review <artifact-id> --decision approve --note "Promising and grounded"
auto-llm-researcher candidates handoff <artifact-id>
```

Rebuild a brief from a stored candidate payload:

```bash
auto-llm-researcher rebuild-brief <candidate-id>
```

## Outputs And State

By default the repo writes under `outputs/`:

- `outputs/briefs/`: single-study Markdown and JSON briefs
- `outputs/mixes/`: mixed-study Markdown and JSON briefs
- `outputs/handoffs/`: approved candidate payloads exported for downstream consumers
- `outputs/state/run-<id>.json`: persisted run snapshots
- `outputs/state/daemon-status.json`: daemon heartbeat and last-run state
- `outputs/researcher.db`: SQLite store for runs, sources, candidates, lifecycle data, and events

## Candidate Lifecycle

Generated single-study and mix artifacts are automatically registered in a shared lifecycle ledger. The current workflow supports:

- listing candidates and mixes
- inspecting lifecycle state together with the persisted synthesis payload
- approving, rejecting, deferring, and reopening review state
- exporting approved artifacts as raw persisted JSON for downstream handoff

Human review notes are tracked as lifecycle events, separate from model-produced synthesis fields such as `review_notes`, `uncertainties`, and `evidence_map`.

## Observability And Health

Recent runs now persist structured summaries in `RunRecord.stats`, including:

- timings
- source activity counts
- ranking and shortlist counts
- brief-output counts
- failure counters

The daemon also writes a heartbeat file to `outputs/state/daemon-status.json`, and `auto-llm-researcher health` reports:

- database readiness
- daemon state
- OpenCode lock-file status
- recent runs
- last success and failure times
- consecutive failure count

## Configuration

Project configuration lives in `researcher.toml`. The file is optional because the app has built-in defaults, and `auto-llm-researcher doctor` reports whether you are running with an explicit config file or implicit defaults.

OpenCode project configuration lives in `opencode.json` and `agents/researcher.md`.

## OpenCode Concurrency

OpenCode synthesis is intentionally serialized through a filesystem lock at `outputs/state/opencode.lock` by default. This prevents concurrent OpenCode runs across CLI commands, daemon cycles, and local regeneration scripts, which is important for providers such as Z.Ai GLM-5-Turbo that do not allow concurrent runs.
