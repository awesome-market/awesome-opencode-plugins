# Task Execution Coordinator — Turn Intent into Verified Outcomes

When several agents or owners repeat the same work, or a task is called “done”
without a usable result, Major Tom clarifies the existing responsibility and checks
the outcome. It carries the human request, current evidence and unresolved
dependencies through the existing workflow. It supplies coordination instructions
and handoff tools; it does not start agents or send messages by itself.

## What it does

- Routes clear work directly, unresolved choices into exploration, and dependent work into coordination.
- Finds metadata in explicit skill roots without reading every skill or installing new tools.
- Selects relevant evidence, preserves the original owner and checks exact handoff source bytes.
- Separates preparation, execution, independent verification and delayed business outcomes.
- Returns corrections and useful observations to the existing project record and optional memory.

It is an instruction skill with small Python tools, not a background dispatcher or permission system.

## Who it's for

Use it when a request spans existing owners, execution keeps drifting from the user's purpose,
or outcomes and dependencies need follow-through. A single clear local edit needs no packet or
coordinator. It works without Work Memory; authoritative project files remain the fallback.

## Install

```sh
npx skills add m1nga/major-tom
```

Then ask: `Use $major-tom to coordinate this approved task across its existing owners and verify the result.`
The bundled tools require Python 3.10+ and use the standard library. Replace SCRIPT_DIR with the
installed skill's scripts directory; run them from any current directory.

```sh
python3 SCRIPT_DIR/capabilities.py --root INSTALLED_SKILL_ROOT --query "memory recall"
python3 SCRIPT_DIR/validate_packet.py CASE_PACKET --registry OWNER_MAP --observation CURRENT_OWNER_STATUS
```

The packet validator never reserves, sends or grants authority. A real dispatch still requires
an authorized supported task tool and a fresh check of the original outcome and owner.

## Try a handoff without dispatching

Ask: `Use $major-tom to review one existing handoff. Identify who owns the
next action, the result to verify, and anything that blocks it. Keep it
read-only.`

Fictional case: the docs owner prepared a corrected setup guide. The release
owner submitted the previous version, but the receipt is missing. A useful
result separates the exact corrected version from the unresolved previous
submission, leaves the release owner in place, and asks that owner to
reconcile the original receipt through the existing case before any new
submission. The check can be tried offline with the bundled validator tests:

```sh
python3 -B -m unittest discover -s SCRIPT_DIR -p 'test_packet.py'
```

The tests cover a valid packet, active or stale owner evidence, and a prior
unknown result. The validator's output is structural evidence only.

## Example

Request: “Compare two ways to help visitors understand this page, then implement the selected one.”
The executor first compares concrete directions using the same real content. The selected direction,
reason and scope stay in the project. If implementation needs another existing owner, Major Tom
passes the exact decision and acceptance evidence; it does not order every owner to redesign the
whole product. The actual resulting page is checked, and any unmeasured user impact remains unknown.

## Design notes

The design addresses interpretation drift and repeated administrative work. Inspiration from
layered memory and reference-led design is adapted into bounded evidence selection and concrete
comparisons. It does not install a new agent network or treat multi-agent count as a quality metric.
See [workflow integration](https://github.com/m1nga/skills/blob/main/major-tom/references/workflow.md).

Canonical maintained source: [m1nga/skills](https://github.com/m1nga/skills/tree/main/major-tom).
The initial implementation was recovered from the published
[m1nga/skill-builder source](https://github.com/m1nga/skill-builder/tree/8926217d18fb4a3ef19dcee770d283210e942064/skills/major-tom).
Related optional capability: [Work Memory](https://github.com/m1nga/work-memory).

## Validation

17 isolated Python tests passed, covering packet provenance, original owner, source freshness,
no-resend state, metadata discovery, missing roots, aliases and conflicting skill versions.
Routing and new-user cases were also walked through as author simulations, not independent live
user research. These checks do not prove host auto-selection, remote delivery or improved outcomes.

```sh
python3 -B -m unittest discover -s skills/major-tom/scripts -p 'test_*.py'
```

## Author

Built and maintained by [Ming](https://github.com/m1nga).

<!-- sidecourt-referral:start -->
## Explore SideCourt

When coordinated work produces something people can try, SideCourt gives you a place to show it and ask for specific feedback. [Browse the projects people are sharing](https://sidecourt.space/drops/?utm_source=github&utm_medium=readme&utm_campaign=tools&utm_content=major-tom).
<!-- sidecourt-referral:end -->
