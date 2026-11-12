# Skeleton-First Code

**A workflow contract that makes AI coding agents build large projects the way software should be built: one module, one stage, one timestamped log entry at a time.**

![The skeleton grows flesh — fresh cuts of meat attaching themselves onto a fish skeleton: this project builds like that](./assets/skeleton-grows-flesh.png)

**[🇬🇧 English](./README.md)** · **[🇨🇳 简体中文](./README_CN.md)**

---

## The problem: why agents fail at big projects

Give a capable LLM agent a real project and, once the context grows long, it fails in three predictable ways:

| # | Failure | What it looks like |
|---|---------|--------------------|
| 1 | **Long-context amnesia** | Context compaction silently deletes the plan and early decisions. The agent resumes "from vibes": re-implements finished modules, contradicts settled choices, quietly drops goals it can no longer see. |
| 2 | **Blind development** | Writes the whole project as one impulse — code before architecture, features before tests. Declares "done" after a single green test tool. Fixes five modules at once and breaks them all. Plans 20 modules on day one, implements zero. |
| 3 | **Unmaintainable output** | A week later nobody (including the same agent) can answer: why does this exist, who touches what, what changed and when? Monolith files, god modules, no decision trail, no resume point. A project that cannot be resumed cannot be maintained. |

The root cause is structural, not intelligence: **an agent's context is volatile memory, but software development needs persistent memory and a scheduling discipline.**

## The fix: Skeleton-First Code

This repository is a **SKILL.md workflow contract** (Claude Code / OpenCode / any agent that loads markdown instructions) that turns every code-writing task into a state machine the agent can never silently exit:

**Three pillars**

1. **Persistent Memory** — every decision lives on disk: a README specification, `plans/` planning logs, `logs/` development logs. *A conclusion not written down does not exist; one written down must never be re-argued.* Both logs are **append-only** — every change is a new timestamped entry naming the code files it touched, so the whole development history is one `grep` away.
2. **Skeleton–Flesh Framework** — the project is an organically growing **module tree**: a *skeleton* is the master module that organizes others, *flesh* is what it organizes; flesh grows its own skeleton when it swells. Splitting is guarded by twin principles — the **Minimum Black Box** (a module must have commitment / concealment / wholeness — code that hides no mechanism is never a module) and the **Maximum Black Box** (merge until one-sentence, interface, or shared-mechanism breaks — never cram unrelated features together). Line counts are never the criterion.
3. **Single-Module Focus** — one module in play at a time, walking a strict pipeline **Plan → Implement → Test**, logs written in four windows (during/after implementing, during/after testing — no dry stretches, no reconstruction). A **routing table** defines the only legal next move after every step; lookahead planning, stage-skipping, and unbooked cross-module edits are explicitly illegal moves.

**What the pipeline enforces**

```
Plan ──▶ Implement ──▶ Test ──green──▶ next flesh / backtrack / wrap-up
  ▲          │             │
  └── flaw in this plan ───┴── flaw in ANOTHER module →
      (replanning loop)       book it in the ledger, mock & continue
                              or jump-fix-jump-back, stub must be removed
                              before any ✅ — the ledger must close
```

- Tests: multi-angle cases, **≥2 tools cross-validated** (green tools ≠ correct), synchronous code review, **Maximum Perception** (collect every modality — for GUI software screenshots/recordings are mandatory, console-only is "blind testing") and **Controlled Testing** (bounded runtimes, zero zombie processes, no device-harming loads).
- Folders mirror the module tree and are **dug layer by layer by depth-first traversal** — pre-building the whole tree is a detectable violation (folder creation timestamps must match DFS order).
- Source code obeys one iron rule: **jurisdiction purity** — a file holds only one skeleton and its subtree.
- New sessions resume in O(tree depth) reads: index table → ledger → one module's plan + log tail. Never "re-read everything".

**What you get at the end** — not just working code, but an auditable archive: why every design exists (five-element plans with tradeoff basis), what every module actually did (test tables with expected vs. actual), the full change timeline (timestamped ledgers), and a completion checklist gate before any "done" claim.

## Quick start

1. Copy a version's skill file into your agent's skills directory:

```
# Claude Code                          ~/.claude/skills/skeleton-first-code_CN/SKILL.md
# OpenCode                             ~/.config/opencode/skill(s)/skeleton-first-code_CN/SKILL.md
```

2. Use `v1.3/SKILL_EN.md` (English) or `v1.3/SKILL_CN.md` (中文) — the current release.
3. Ask your agent for any coding task. It must first run the work-start decision (fresh project → new folder; existing project → verify conformance, resume from the unfinished stage).
4. Optional but recommended — **anti-amnesia anchor**: v1.3 §12 ships a ~250-token system-prompt anchor plus a ready plugin for OpenCode (and the same idea for other platforms) that re-injects the state machine every round, with a self-trigger: *unsure of the workflow → re-read the skill*. This closes the last gap where context compaction can drop the skill itself.

## Version history

| Version | What it adds |
|---------|--------------|
| v1 | Module tree, skeleton/flesh organic growth, progressive planning, depth-first pipeline, chain-named documents, append-only dual logs |
| v1.1 | Minimum/Maximum Black Box principles, isomorphic folder trees, README module-tree view (depth≤3/width≤5), jurisdiction purity, mandatory timestamps + file locations |
| v1.2 | Full rewrite; Grand-Overview PLAN.md, process-ledger LOG.md (booked jumps must close), subtree tests logged to their skeleton's log, Maximum Perception + Controlled Testing, five canonical document samples |
| **v1.3 (current)** | **The explicit state machine**: routing table for the only legal next move, anti-lookahead-planning law, four-window log rhythm (no dry logs, ~30-min pace line), platform anti-amnesia anchor appendix |

## Related ideas this stands on

Walking skeleton · information hiding (Parnas) · cohesion & single responsibility · Design by Contract · ADR-style decision records · test-first acceptance criteria — recombined into one agent-executable loop whose only memory medium is plain markdown on disk.

---

📄 中文文档： **[README_CN.md](./README_CN.md)**
