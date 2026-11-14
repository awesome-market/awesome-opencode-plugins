# First Principles — A Codex Skill for Simpler, Complete Workflows

When a coding agent overengineers a small task, First Principles brings the work
back to the requested outcome: reuse the existing implementation, remove needless
steps and check the result where the user will use it. It is an optional workflow
instruction, not a new tool or a guarantee of faster work. The published comparison
below did not establish an advantage over the baseline.

Built for personal workflows. Install the instructions into your agent; no website,
account or separate service is required. This repository is the source and install entry.

## What it does

Turns a request into the simplest sufficient path through completion. It challenges
assumed dependencies, avoids repeated approvals and duplicate ownership, and checks
the outcome at the point of use. Necessary permissions, recovery and verification
remain part of the work.

## Who it's for

Use it when asking for first-principles execution, a simpler workflow, or fewer
unnecessary steps. It works for product changes, research, publishing and operational
work within the authority the user has actually given.

It does not force a thinking template onto every question, restart a working project,
resume paused tasks, or promise a globally optimal plan. An analysis-only request
remains analysis-only. It requires no account, API key or new service of its own.

## Install

```sh
npx skills add m1nga/first-principles
```

Then ask:

> Use $first-principles to finish this task with the fewest necessary steps. Reuse
> what we already have, preserve the full result and verify that I can actually use it.

## Example

**Request:** “The report is approved. Fix the broken download on the existing page
and give me the working link.”

**Expected behavior:** inspect the existing link and artifact, repair the relevant
path, verify an actual download, and return the link. If deployment is already
authorized, finish it. If a real permission is missing, prepare the fix and identify
that specific remaining action. No new portal, approval round or broad redesign.

**Boundary:** “Make the migration simpler, but keep the release paused.” Reuse the
existing state and prepare or test only permitted steps. Simplicity never lifts the
pause. A handoff must retain enough state for the recipient to execute correctly.

These examples are authored scenarios, not customer testimonials.

## Try it on a recurring false completion

> Use $first-principles. The second report still cannot be opened by a reader,
> even though generation says it succeeded. Reuse the current report pipeline
> and verify the link through the reader's entry point.

A useful comparison holds the report and acceptance check fixed. Record
whether the intended reader can open the correct file, how many follow-up
corrections it takes, and any manual steps still needed. This is a candidate
test for the repeated “generated but unusable” failure. The documented paired
trial below establishes its own results.

## Design notes

Ming repeatedly asked for complete outcomes with fewer detours. Historical reviews
showed an important distinction: shortening the visible instructions can still leave
more manual work, repeated decisions and incomplete execution underneath.

The skill therefore optimizes the whole route to a usable outcome. It is a compact
execution aid, not a new coordination system. It reads the user's current agreements
instead of embedding one person's model settings, task IDs or private history.

[Source comparisons](skills/first-principles/references/comparisons.md) explain what
was adapted and rejected. When authoring another skill, it searches relevant author
sources and records a concrete integration decision through the existing release
process rather than adding a second process.

## Validation

On 2026-11-03, six actual Codex executions compared three identical local tasks
with and without this skill. Both configurations passed all 15 acceptance criteria
across the three tasks on the first delivery, with zero correction rounds.
**This small test did not demonstrate an incremental reduction in rework.**

The tasks covered a broken download, a budget correction and a paused migration
handoff. They were reconstructed fixtures, not live business work or an independent
user study. See [measurement details](skills/first-principles/references/evaluation.md).
Use the skill as an optional execution aid; measured efficiency is not promised.

The release also includes 11 maintainer walkthroughs labeled as simulations, plus
actual package, metadata and publication checks. See the content-bound
[release evidence](https://github.com/m1nga/skills/blob/main/ops/skill-quality/reviews/first-principles.json).

## Common questions

**Does this create a new task or run in the background?** No. It guides the agent
working on the task you requested. It does not install a scheduler, service or a
separate coordination system.

**Should I use it for every question?** No. Invoke it for first-principles execution
or workflow simplification. Ordinary questions and small edits can stay direct.

**Does it replace permissions or project instructions?** No. Current scope, original
owners, publication holds and real verification requirements remain in force.

## Author

Built by [Ming](https://github.com/m1nga). Source, documentation and installation are
maintained in this GitHub repository.

<!-- sidecourt-referral:start -->
## Explore SideCourt

A simpler workflow leaves more room to finish the thing you started. [Browse projects on SideCourt](https://sidecourt.space/drops/?utm_source=github&utm_medium=readme&utm_campaign=tools&utm_content=first-principles), or share a tool or experiment you made and the feedback that would help.
<!-- sidecourt-referral:end -->
