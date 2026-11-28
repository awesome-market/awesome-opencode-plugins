<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/spec-flow-lockup-dark.svg">
    <img alt="spec-flow" src="assets/logo/spec-flow-lockup.svg" width="480">
  </picture>
</p>

**Two phases for AI coding agents: strict gates, flexible work inside them.** Agree on goals, scope and acceptance, then implement and deliver under an explicit delegation. The user decides what review, revision, merging and production actions are authorized.

There is no runtime or service: these are Markdown instructions an agent reads. The spec path preserves an approved specification, an execution issue and traceable sources. Direct implementation creates no mandatory spec or execution issue, but still has delivery and merge gates. Code mapping remains off by default; source, the actual diff and relevant tests establish impact.

`SKILL.md` is **entry and navigation only**. Existing budgets remain **4,700 characters** for its body, **500** for frontmatter and **5,200** overall, including newlines. [`scripts/check-docs.sh`](scripts/check-docs.sh) also guards against hiding rules in metadata. Character budgets do not guarantee tokens or retention across clients; reread action-specific rules when unavailable or changed.

Every rule has a recorded origin: **37 entries** in [`references/rationale.md`](references/rationale.md) retain cases, decisions, costs and verification limits. History is not a second set of operating rules.

**English** · [中文](README.zh-CN.md)

<!-- s:shape -->
## What using it looks like

With a request like “add avatar uploads,” an agent without a shared understanding can deliver an unwanted database table and a size limit it invented.

With spec-flow, a new request starts with the user's choice of direct implementation or a spec. For a spec, grill-me helps clarify the goal and real alternatives; spec-flow collects one proposal. No permits rethinking, not just local patching. No spec is written before the first Yes.

**Yes creates the common outline and the same Draft PR before the page decision.** Pages wait for the user's design, then analyze behavior and APIs; no-page work analyzes rules and APIs against material that can be judged. Both paths converge on unresolved decisions, then one split-or-keep choice and a refined final spec. Sufficient prose, tables or diagrams are valid; four columns or three examples are not arbitrary admission requirements.

An implementable spec and consent to send it for review lead to that deliverable's review choice, chosen revisions and a separate merge confirmation. After the spec merges and execution issues are handed off, implementation waits for explicit delegation. Implementation delivery gets a fresh review choice. Exceptions and edits to merged specs are conditional, not questions on every run.

<!-- s:problem -->
## The problem

Failures happen at seams: unconfirmed understanding, missing upstream deliverables, duplicate claims, review mistaken for merge approval, or a merged implementation described as done while documentation or deployment is still missing.

The answer is not more ceremony inside every step. It is a clear home for **decisions, authority, deliverables and evidence**: investigate facts first and ask only what the user must decide.

<!-- s:scars -->
## Where the rules came from

The rationale keeps the original evidence and its limits; old cases do not expand a new task's scope:

- **R1**: an IDC criterion expanded to CIDR ∪ ASN, while implementation, acceptance and the parent stayed stale. A changed criterion needs its current landing points checked.
- **R7**: two agents treated an open issue as unclaimed. The actual claim is Git successfully creating the worktree.
- **R15**: file boundaries were mapped, but two owners defined the same “enabled” decision differently. Dependencies and shared decisions need ownership too.
- **R12**: one spec's body changed across 17 commits. Editing a merged specification needs the user's new-spec-or-edit decision.
- **R37**: responsibilities were reorganized, the common outline/Draft moved earlier, and format, example counts and reporting style stopped acting as approval gates.

<!-- s:what -->
## How it solves them

**Still two phases, not a third management workflow.**

- **Design**: clarification and proposal confirmation → common outline/Draft → page or rule analysis → common gap confirmation → one split decision → final spec → review/separate merge → execution handoff.
- **Implementation**: explicit delegation → isolated claim, implementation/tests/supporting docs → fresh review/separate merge → all actual sources and evidence → necessary acceptance and applicable release → close-out.

The sole operating owners are [one-path](references/one-path.md) for flow/state, [gate-details](references/gate-details.md) for choices/authority, [phase-handoff](references/phase-handoff.md) for delivery information and [done-criteria](references/done-criteria.md) for completion. The entrypoint and guides do not repeat those rules.

<!-- s:self-review -->
## The one rule worth stealing: a subagent is not a second opinion

A spawned agent is still the agent's execution delegate. A different model, name or prompt does not automatically make its opinion independent. Testing and drafting must not masquerade as review.

The user chooses whether and how to review each deliverable. Where a genuinely different party must decide, prepare the material and stop for that party; do not substitute another self-dispatched agent. Markdown is not platform access control.

<!-- s:smooth -->
## Why it doesn't feel heavy

Necessary decisions use a choice tool, with a recommendation, major costs and room to add information. Without a tool, present equivalent explicit options; missing tools and silence do not imply approval. Valid decisions survive method changes, and spontaneous explicit instructions are not erased by card formalities.

Review still offers none/light/heavy/heavy+mutation; revision still offers all/blockers+high/none; merging remains separate. Defaults, rounds, costs and stopping rules live only in the gate owner. Wording and synchronization mistakes can be corrected; authority violations, missing deliverables and real safety gaps do not disappear under “flexibility.”

<!-- s:longrun -->
## Why it survives long work

Git retains the claim lock; the original handoff retains the current phase; the spec retains approved scope; the original task retains all implementation sources and passing evidence. A new session need not guess who is working or assume the last PR represents the entire delivery.

Promotion reads expected deliverables before checking the design PR and all implementation/supplementary sources. Archived specs are checked at their actual contents, existing content is verified rather than duplicated, shared files are not overwritten from moving dev, and unready tasks do not ride along. Repair the original record or missing deliverable, not a second ledger.

<!-- s:limits -->
## What it doesn't do

- It does not schedule or resume agents, or provide platform authorization isolation. Git locks and this repository's static checks have limited, specific guarantees.
- It does not promise zero future bugs. Done means the agreed delivery exists, necessary tests/acceptance pass, no known blocker remains and evidence is available.
- It does not equate an implementation merge, label or tag with deployment success. A successful snapshot does not mean every service is currently on the same version.
- It does not silently install tools, upgrade adopting repositories, create long-lived branches, CI/hooks or a release platform. The issue/PR path assumes GitHub; unavailable platform capabilities must be reported.

<!-- s:install -->
## Install

```bash
git clone https://github.com/Strelizialeomon/spec-flow.git ~/.claude/skills/spec-flow
```

Alternatively, clone into a code directory and symlink it into the client's skill location. The example is Claude Code's personal skill path; other clients use their own discovery locations. Installing a skill is not project adoption, configuration readiness or verified client behavior.

Professional clarification in PLAN/ANALYZE needs loadable grill-me and its actual grilling dependency. If needed and missing, verify sources and exact installation locations before asking Yes/No. Refusal or failure pauses that clarification path, not direct implementation, an existing implementation or delivery. Do not silently substitute a template or claim a skill ran. Superpowers is not a dependency.

<!-- s:usage -->
## Using it

Describe a request or invoke spec-flow. For an existing task, say “do #12.” Continue the current valid phase instead of restarting an interview. The strict same-window bare-start rules are in gate-details; a globally unique task is not enough to infer delegation.

Choose useful working methods: examples, diagrams, prose and tables should clarify rules, APIs and verifiable acceptance. Honor explicitly agreed project formats, and do not use replaceable guides to omit necessary contracts. Within-scope implementation methods need no approval at every internal step; stop the affected portion at actual declared stopping points.

Say “apply spec-flow to this project” to adopt, or “update this project's spec-flow integration” for an explicit upgrade. Only authorized pointers and project locations are written. Repeat runs are idempotent; no copied workflow, surprise optional adoption or automatic migration of existing projects.

The options remain `adr`, `doc-lifecycle`, `issue-status`, `issue-type` and `release`, all off by default. `release` covers **Git branching and release** together: adoption chooses single-mainline or three-layer operation and real branch mappings, not a separate Git switch. In three layers, ordinary documentation also enters staging by task. With no deployment obligation and required branch delivery/acceptance complete, it can finish and wait for the next normal snapshot; no documentation hotfix/tag ceremony. Code still requiring deployment cannot finish early.

Code mapping remains disabled unless explicitly requested for a trial/restoration; see [code-map](references/code-map.md). Already adopted ADR and document-reading rules apply at their existing moments. Read the current approved construction spec; do not redesign these systems merely for structural symmetry.

<!-- s:evidence -->
## This repo is its own case study

Specifications, issues, PRs and the rationale preserve design and delivery evidence. Old specs and decisions are not rewritten into new operating rules. Each delivery's verification distinguishes input, expectation, actual behavior and limits: static green is not client compliance, and a fake repository or limited client run is not production or all-model certification.

This reorganization follows merged design PR #164 and execution issue #165. Implementation review and merging still need the current user's choices; specification review is not implementation acceptance.

<!-- s:docs -->
## Files

| File | Responsibility |
|---|---|
| `SKILL.md` | Entry/navigation, not complete workflows/cards/templates |
| `AGENTS.md`, `CLAUDE.md` | Repository maintenance rules; the latter imports the former |
| `references/one-path.md` | Sole flow/final diagram/state and transition owner |
| `references/gate-details.md` | Sole choices, approval scope, release/stop, review and merge owner |
| `references/phase-handoff.md` | Sole delivery information, all sources and update responsibilities |
| `references/done-criteria.md` | Sole finite completion, evidence and approved-exception criteria |
| `references/spec-maturity.md` | Replaceable outline/counterpart/final working guide |
| `references/split-large-spec.md` | Replaceable deliverable/dependency/splitting guide |
| `references/spec-revision-sync.md` | Replaceable method for synchronizing current landing points |
| `references/worktree-lock.md` | Git workspace, locks, takeovers and safety boundaries |
| `references/apply-to-project.md` | Adoption intent, pointers, locations and asset/install boundaries |
| `references/release-discipline.md` | Optional release: Git mappings, complete candidates and necessary release |
| `references/adr-decision-records.md` | Optional ADR, retaining its existing responsibilities |
| `references/documentation-lifecycle.md` | Optional document lifecycle and reading order |
| `references/issue-status-labels.md` | Optional phase/blocker labels and sorting |
| `references/issue-type-labels.md` | Optional type labels and authorized migrations |
| `references/code-map.md` | Boundaries for disabled-by-default map trials/restoration |
| `references/adoption-model.md` | Historical adoption explanation, not additional obligations |
| `references/rationale.md` | R1–R37: evidence, tradeoffs and verification limits |
| `docs/maintainer-notes.md` | Local wiring and history |
| `scripts/check-docs.sh` | Existing budgets/links/bilingual/adoption checks plus necessary owner/delivery presence; no literal guide-format enforcement |

The README introduces the system. Follow entry navigation to the corresponding sole operating owner; do not use the README as an alternative rulebook.

<!-- s:contributing -->
## Contributing

Open an issue or PR. Record real evidence for rule changes under a new rationale number; keep the entrypoint to navigation and short reason pointers. Update both READMEs in the same delivery and run the existing documentation check.

<!-- s:license -->
## License

MIT — see [LICENSE](LICENSE).
