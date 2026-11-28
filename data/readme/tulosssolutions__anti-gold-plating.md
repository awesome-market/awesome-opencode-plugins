# Anti Gold Plating

Keep AI-assisted work within the scope you actually approved.

Anti Gold Plating is an instruction-only agent skill for changes to code, configuration, documents, and systems. It asks the assistant to establish clear boundaries, obtain explicit approval for additional work or alternative approaches, and compare the result against the original request before delivery.

The goal is to reduce unsolicited changes, regression risk, and wasted effort. The complete instructions live in [SKILL.md](SKILL.md).

## What Is Gold Plating?

In project management, gold plating means adding features, polish, or other extras beyond the agreed requirements on the delivery team's own initiative, without the appropriate approval. Good intentions or apparent usefulness do not authorize the addition. PMI describes this as a contributor to uncontrolled scope growth, or scope creep. [PMI: Top Five Causes of Scope Creep](https://www.pmi.org/learning/library/top-five-causes-scope-creep-6675).

An improvement explicitly approved through the project's change process is different: this skill targets unauthorized extras, not useful ideas or agreed changes.

### Origin of the Name

The name borrows the project-management concept used in PMI literature and PMP preparation. Think of it as an unrequested decorative coating: more polish is not necessarily more value.

PMI's [PM101 article from September 1993](https://www.pmi.org/learning/library/modern-project-management-defining-purpose-5059) already discusses gold plating and waste from exceeding requirements. Its [Above and beyond article from June 2002](https://www.pmi.org/learning/library/above-beyond-scope-interpretation-bandwidth-4507) connects the term to Rita Mulcahy's 2000 *PMP Exam Prep Guide*. These are documented uses, not a claim that PMI or the PMP certification invented the expression.

This is an independent agent skill, not a PMI publication or a PMP exam guide.

### Potential Impact

Unapproved extras can consume budget and time while delivering something different from what stakeholders expected. PMI emphasizes that decisions about added functionality belong to authorized decision-makers. [PMI: Top Five Causes of Scope Creep](https://www.pmi.org/learning/library/top-five-causes-scope-creep-6675).

Applied to AI-assisted work, the risks include:

- **Cost and delay:** More tokens, tool calls, implementation work, and review time for changes nobody requested.
- **Regression risk:** Unnecessary edits can alter working behavior, interfaces, exports, or visual design.
- **Maintenance burden:** Additional code, dependencies, and configuration must be understood, tested, and maintained.
- **Loss of control and trust:** The user receives a different result or external side effects they did not authorize.
- **Opportunity cost:** Effort moves away from the approved task, sometimes followed by rollback and rework.

These are potential consequences, not measured performance claims for this skill. The response is to propose improvements, explain the tradeoffs, and wait for approval before implementing them.

## Quickstart

Review [SKILL.md](SKILL.md), then ask Codex's built-in skill installer:

```text
$skill-installer Install the skill at the root of
https://github.com/TulossSolutions/anti-gold-plating as anti-gold-plating.
```

Once installed, invoke it explicitly in Codex CLI or the IDE extension:

```text
$anti-gold-plating Make this report responsive on mobile.
Preserve the desktop design, exported data, and delivery behavior.
```

Codex can also select skills based on their descriptions. If a newly installed skill does not appear, restart Codex. See the [official OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills) for installation and invocation details.

Previously named `scope-guard`. Existing installations should use the updated `SKILL.md` in a folder named `anti-gold-plating`; avoid keeping both copies active.

## What It Asks the Assistant to Do

1. **Establish the baseline.** Identify the request, deliverables, exclusions, constraints, and existing approvals before making changes.
2. **Ask before expanding scope.** Present additional improvements with their benefits, affected files, risks, and cost, then wait for explicit approval.
3. **Let the user choose alternatives.** Present genuine implementation choices and wait for a decision before acting on them.
4. **Keep an approval record.** Track what was proposed, what was accepted, and the corresponding user message.
5. **Make targeted changes.** Preserve unrelated design, behavior, interfaces, data, configuration, and external effects.
6. **Verify before delivery.** Review the actual diff, test the requested result and preserved behavior, and report any discrepancies before publishing or deploying.

An explicit initial request already authorizes its stated scope. The skill does not call for repeatedly confirming that same request or inventing alternatives merely to ask more questions.

## What Counts as Approval?

Approval is an explicit response to a clearly described proposal or option. It does not require special wording when the intended choice is unambiguous.

| Situation | Expected behavior |
| --- | --- |
| The user requests an analysis | Analyze; do not implement the recommendations automatically. |
| The assistant finds a useful neighboring improvement | Describe it and wait for approval before implementing it. |
| The user approves a specific proposal | Implement that proposal, without adding unrelated changes. |
| The user approves publication | Publish only content already within the approved scope. |
| An unapproved change is found during review | Report it, withhold it from delivery, and seek approval for its correction. |

Silence, progress updates, recommendations inside an attachment, and permission to run a tool are not approval for additional work.

## Example

**Request:** Make an email report readable on mobile without changing its desktop design.

**Within scope:** Adapt the mobile layout and verify that the desktop appearance and existing report data are preserved.

**Requires separate approval:** Redesign the desktop report, remove columns, change export values, or alter notification behavior.

If the assistant proposes shortening a verbose label, it should explain the exact change and wait. A response such as "Yes, shorten that label as proposed" authorizes that change only.

## Expected Final Summary

The assistant should conclude with a brief, distinct account of:

- **Initial Request / Delivered:** What was requested, what was completed, and what remains unfinished.
- **Validated Evolutions:** Additional changes explicitly approved by the user, or none.
- **Unvalidated Discrepancies:** Any unapproved changes, their impact, and whether they remain local or were published or deployed, or none observed after verification.
- **Verification & Limitations:** Checks actually performed, behavior preserved, and anything not verified.

The target is zero unvalidated scope drift. A successful test run does not make an unapproved change authorized, and a missing test is a verification limitation rather than scope creep.

## Limitations

- This is a behavioral instruction set, not a sandbox, permission system, or automated enforcement tool.
- It cannot guarantee that an assistant will follow every instruction, avoid all regressions, or use fewer tokens.
- It does not override higher-priority instructions or the host's safety and permission controls.
- Explicit approvals introduce pauses. Clear initial requirements and grouped questions help keep the workflow practical.
- Review diffs and retain appropriate tests, backups, and deployment controls. The final summary is not a substitute for those checks.
- Installation and invocation instructions here target Codex. Other assistants may require adaptation and are not claimed as tested integrations.

## Repository Contents

- [SKILL.md](SKILL.md): The skill's metadata and complete operating instructions.
- [README.md](README.md): Overview, usage, examples, and limitations.

No scripts, runtime dependencies, or external services are required by the skill itself.
