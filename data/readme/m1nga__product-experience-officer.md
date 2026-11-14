# First-Time User Tester — See Where Your Product Confuses New Users

Find where a first-time user gets stuck completing a task in your product. Give
the agent an entry point and an intended outcome, such as finishing onboarding or
creating the first project. It attempts the journey without owner explanations,
then produces an HTML usability report with evidence, prioritized fixes and retests.
An agent walkthrough does not measure customer conversion or replace user research.

## Run a first-use report

The [CLI recovery sample](https://github.com/m1nga/product-experience-officer/blob/main/skills/product-experience-officer/examples/cli-recovery.json)
shows one observed failure, one recovery, and a remaining documentation retest.
It is a maintainer-run exercise on disposable data. No customer app is involved.

```sh
printf '%s\n' '{"url":"https://example.org/one"}' '{"url":"https://example.org/two"}' |
  python3 -m json.tool
# Observed: exit 1, Extra data: line 2 column 1 (char 34)

printf '%s\n' '{"url":"https://example.org/one"}' '{"url":"https://example.org/two"}' |
  python3 -m json.tool --json-lines --compact
# Observed: exit 0, two records printed

python3 SKILL_DIR/scripts/report.py --input SKILL_DIR/examples/cli-recovery.json --out first-use-report.html
```

Open the generated HTML to see the verdict, the two attempts, and what remains
to verify. Replace `SKILL_DIR` with the installed skill directory and choose a
new output path. The renderer requires no account, server, or paid API.

For a real review, supply your public entry point, one task a newcomer should
complete, and a disposable profile if that task writes data. The separate
`examples/report.json` fixture shows how to label a simulation and missing
coverage. The renderer checks the evidence fields and preserves the review mode.

## What it does

Runs your product (or reads your screenshots) in two phases. Phase 1: follow the public entry path and record confusion before consulting internal specifications or code. A README or help screen that users naturally encounter is part of that experience. If the reviewer already knows the product, disclose that context; the run cannot honestly be called a fresh independent test. Phase 2: a product/UX expert who reads the code and docs to explain each confusion and prescribe a fix. The output is a single report: a one-paragraph verdict up top ("would a stranger come back tomorrow?"), a first-person experience log, severity-ranked findings with evidence, one recommended fix each, and effort estimates, plus an honest list of what this round couldn't verify.

## When it fires

- "Walk through my app as a first-time user."
- "Does this onboarding make sense?"
- "UX audit these screenshots."
- "Pretend you've never seen this and try it."
- "帮我从用户视角体验一下这个产品"
- "看看新用户会怎么想"

It does not fire for debugging a specific error from a screenshot, or for code review — it evaluates the experience, it doesn't repair the build.

## Install

```
npx skills add m1nga/product-experience-officer
```

## Try an evidence-bound review

After installation, ask your agent to use `product-experience-officer` on your
product's public entry point and one core task. Supply a disposable profile for
any action that writes data.

Illustrative recovery case: a text-only walkthrough shows the task completing
and invalid input returning a useful error. No major defect is observed. The
report should say **zero evidenced major findings in this tested path**, record
the actions and outputs, and leave visuals and untested paths under To verify.
It must not manufacture a blocker to sound rigorous or claim retention from one
session. If the reviewer read the spec earlier, the report must disclose that.

This example describes expected behavior; it is not a user study or a claim that
an application was tested here.

## Example

> **You:** I just finished the onboarding flow for my journaling app. Walk through it as a first-time user — here's the local dev command.
>
> **Claude:** launches the app cold, freezes on the first screen ("I see a text box and the word 'begin'. I don't know what this app is for yet"), wanders off the happy path, answers a prompt with "idk", pastes 2000 words, quits mid-flow and comes back. Then reads the code and reports: verdict first, then findings like — 🟠 Major: the first screen never says what the product does before asking for personal writing; evidence quoted verbatim; fix: one line of promise copy above the input; effort S.

## Works well with

- [`map-product-system`](https://github.com/m1nga/map-product-system/) — map what the product actually is before or after an experience run.
- [`diagnose-project-rebuild`](https://github.com/m1nga/diagnose-project-rebuild/) — when the report's Blockers point at structural rot rather than surface fixes.

## Design notes

The methodology is opinionated on purpose, and each rule comes from real reviews of solo-built products:

- **Two phases, never mixed.** A builder cannot un-know their product; neither can a reviewer who read the spec first. The stranger must run before the expert, because confusion is perishable evidence.
- **Verdict first.** A solo builder reading the report needs one decision ("is this ready, and what do I fix now?"), not a flat list of twenty items. Prioritization is the deliverable, not a garnish.
- **One recommended fix per finding.** Listing three options without a pick pushes the decision cost back onto the person who asked for help. The skill always recommends, with a reason, and labels taste as taste.
- **Treat the developer's data as production.** Live runs happen on the builder's own machine, next to their real files. The skill refuses writes that touch pre-existing user data and records the attempt as a finding — a rule written after runs where the product cheerfully offered to overwrite the builder's real archive.
- **Degrade honestly.** No browser? Copy and flow get reviewed; every visual claim moves to a to-verify checklist instead of being guessed from HTML. A smaller honest report beats a complete fabricated one.

## Field-tested

Probed 7 scenarios across 5 personas · 5 fired correctly · 2 correctly stayed quiet.

> **"Does this onboarding make sense? Here are three screenshots."** → Fired in Mode A — and an English-speaking user gets an English report. (An earlier probe caught this skill answering English builders in Chinese; that fix is now verified green.)

> **"Here's a screenshot of the error my app throws on login — what's wrong?"** → Correctly stayed quiet. A screenshot is not automatically a UX review: the description's NOT-clause sends debugging elsewhere, a boundary added after a real false-fire.

> **"Run my web app and review it as a first-time user"** — in an environment with no browser or screenshots → Fired, and degraded honestly: copy and flow reviewed from text, every visual dimension moved to an explicit To-verify checklist, and inferring "the spacing is probably fine" from CSS is banned as fabricated evidence.

Probe method: [scenario-probe](https://github.com/m1nga/scenario-probe/)

## Author

Built by [Ming](https://github.com/m1nga). The design notes above explain the real problem and tradeoffs that shaped this skill.

<!-- sidecourt-referral:start -->
## Explore SideCourt

A fresh perspective starts with someone trying the work. [Browse projects on SideCourt](https://sidecourt.space/drops/?utm_source=github&utm_medium=readme&utm_campaign=tools&utm_content=product-experience-officer) to find something to try, or share your own product and explain what you want feedback on.
<!-- sidecourt-referral:end -->
