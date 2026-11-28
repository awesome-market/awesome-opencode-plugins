# Design Agent — Turn Visual References into Usable Interfaces

When an AI-generated page misses the reference, Design Agent connects the visual
choices you care about to a responsive interface and concrete checks. Give it a
reference, the existing page and the change you want. You get a design brief or a
scoped implementation, with accepted choices, working interactions and remaining
prototype behavior kept explicit. A brief alone is not a verified visual match.

## Try the brief renderer

Turn a research/reference pile into a page a builder can act on:

```sh
python3 SKILL_DIR/scripts/brief.py --input SKILL_DIR/examples/capture-brief.json --out design-brief.html
```

Copy the small example JSON into your project, replace its goal, content and tasks, then render a new output file. Each task connects a method to steps, reference decisions and observable checks, with a ready-to-use implementation prompt. An unseen reference stays labeled unseen. The renderer does not inspect references or build the interface. No accounts or paid API are needed.

## When it fires

Use it to analyze a reference, establish a brand direction, refine an AI-generated
interface, or build an already scoped design. It does not automatically redesign
a site when you only ask for an opinion. For unrelated coding or marketing copy,
use the relevant workflow instead.

## Install

```bash
npx skills add m1nga/design-agent
```

Ask: `Use $design-agent with this reference. Preserve its color transition, then
redesign this page for desktop and mobile.`

The package contains instructions, not a background service. Image generation,
Figma, browsing, code execution and hosting depend on the tools in your environment.
TaskDock is useful for continued work but is optional; the skill explains the fallback.
No paid account is required merely to use the instructions. A new session may be
needed for an installed skill to appear in automatic discovery.

## What it does

- Reference observations separated from accepted choices.
- A visual direction or the implementation authorized by your request.
- Asset prompts with composition, cropping and motion constraints when needed.
- Focused revisions tied to visible problems.
- A handoff distinguishing working operations, simulations and untested behavior.

## Example

Input: “I like this reference's color transition. The rest isn't decided.
Show me a mobile and desktop direction. Don't build the app yet.”

Expected result: inspect the reference, explain the specific transition to borrow,
make a bounded visual comparison using the same content, and preserve the remaining
brand choices as proposals. No production app edits follow from that request.

Input: “Build the approved submission flow and make it reopen locally.”

Expected result: implement the actual submission behavior, check failure and recovery,
and verify a maintained entry after restarting the required services. If the agreed
deliverable is only a prototype, submission is labeled simulated.

These examples describe intended behavior; they are not claims of a deployed app.

## Evidence from reference to result

For an authorized build, a handoff for the sample capture flow would include:

| Evidence | What a reviewer can verify |
|---|---|
| Reference crop or timestamp and the chosen relationship | Which part of the reference informed the capture flow |
| The same content on desktop and mobile, with viewport sizes | Whether the input and recovery message remain visible and readable |
| Valid paste, invalid paste and repeated-link checks | Whether save, recovery and deduplication actually occurred |
| Entry point, result location and status | How to reproduce the check and which behavior is simulated |

The downloadable brief above is a real renderer output you can create locally.
Its included sample marks the reference as unseen. The capture flow and
evidence list describe a proposed build. There are no screenshots or live
save results attached to that example.

## Design notes

A cinematic tutorial can teach composition and iteration without establishing
backend correctness or an approved brand direction. This skill preserves useful
methods—negative space, stable camera motion, media seams, specific revisions—and
avoids carrying a tutorial's palette, model version or promotional tactics into
every project. It also addresses a common delivery error: a success screen alone
does not show that a submission reached storage.

The review considered [Anthropic's frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)
for subject-grounded visual decisions and
[Vercel's web-design-guidelines](https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md)
for focused interface review. This package uses original wording and no copied code.

## Validation

Release checks validate package structure, reference links, metadata and installation.
Scenario walkthroughs cover intended requests, routing overlap, missing tools, stale
decisions and misleading success states. Walkthroughs are author simulations, not
independent user studies or proof of future model behavior. No visual taste, browser
compatibility or application backend is certified by installing this skill.

## Author

Built by [Ming](https://github.com/m1nga). MIT licensed.

<!-- sidecourt-referral:start -->
## Explore SideCourt

Once an interface is ready for someone else to try, you can share it on SideCourt and ask about the parts you are unsure of. [Browse what people are making](https://sidecourt.space/drops/?utm_source=github&utm_medium=readme&utm_campaign=tools&utm_content=design-agent) to get a feel for the place.
<!-- sidecourt-referral:end -->
