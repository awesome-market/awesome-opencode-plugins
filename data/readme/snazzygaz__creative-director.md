<p><img alt="creative director: design judgement for AI agents. A white great egret in profile with lace plumes, its level gaze drawn as a 20-degree viewing cone that runs through the red square mark." src="docs/assets/banner-dark.png" width="100%"></p>

Design judgement for any AI agent making or reviewing visual work and copy: drawings, illustrations, 3D, screens, flows, infographics, film and writing. **v0.11.4 starts from the idea, feeling and tone**, makes 4–8 roughs, compares them head-to-head in a fresh context of the same model, and shows the top 2–3 to the owner of the work. Only the winner enters the fix loop. Critiques label rule-backed, intent-backed and exploratory findings, with provenance and confidence. Choose the fix level before changing work; “the original is better” is a valid stop. [Energy](core/energy-pass.md) follows the named tone and genre, not a default ritual. Research and craft keep their evidence grades; taste stays with the owner of the work.

**Start here**
1. What it is: a rule set and critique loop an agent reads to judge and improve its own visual work.
2. Always load [`AGENTS.md`](AGENTS.md), [`core/principles.md`](core/principles.md) and [`core/critique-loop.md`](core/critique-loop.md).
3. Then add only the modules the task needs, from [`core/which-modules.md`](core/which-modules.md).

**[Gallery](https://snazzygaz.github.io/creative-director/gallery/)** · **[Install as Grok Bot](https://x.ai/bot/XWBKgRnDOw7uR5SpKx3Af)** · **[Claude Skill zip](https://github.com/SnazzyGaz/creative-director/releases/latest/download/creative-director-skill.zip)** · **[Lite version](lite/CREATIVE-DIRECTOR-LITE.md)**

<p><picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/baseline-dark.jpg">
  <img alt="Same prompts without the skill, with the skill, and with the skill plus the aesthetic layer. Book cover: without, a busy rainbow cover with an invented subtitle, signs and slogans; with, a calm painted fox reading under a tree, lit by the low sun, with the title set in type; plus aesthetic layer, the same cover in warm golden-hour light, lit from the low sun on the left. Event poster: without, a rich street scene with an invented address and slogans; with, a plain cream poster with a navy double bass and only the given facts; plus aesthetic layer, a navy night street with lit windows and a lamp, same facts in cream type, the double bass standing in the lamp's light." src="docs/assets/baseline-light.jpg" width="100%">
</picture></p>

Same prompt and image model, one sample each: an illustration, not a benchmark. *Without:* the prompt as is. *With:* the skill's loop, with every word set in code from the brief's facts only. *+ aesthetic layer:* one more round with the [aesthetic module](modules/aesthetic-critique/). [Full write-up](examples/baseline-comparison/) · [aesthetic notes](examples/aesthetic-benchmark/).

## Before and after

| | |
|---|---|
| [<img alt="Book cover, baseline and with the skill: invented words and busy backgrounds behind the title, against a lone apple tree in a flood with only the title and author." src="examples/showcase/01-book-cover.jpg" width="100%">](examples/showcase/01-book-cover.jpg)<br>**Book cover:** no invented copy, and the type sits on calm ground. | [<img alt="Honey label, baseline and with the skill: a busy wreath and mixed scripts, against a pine whose hollow is a dripping honeycomb cell." src="examples/showcase/02-packaging-label.jpg" width="100%">](examples/showcase/02-packaging-label.jpg)<br>**Packaging:** the name becomes the mark, and the label reads in a clear order. |
| [<img alt="Character design, baseline and with the skill: an invented club logo and text, against a striding girl inventor with only the briefed props." src="examples/showcase/04-character-design.jpg" width="100%">](examples/showcase/04-character-design.jpg)<br>**Character:** the invented logo is gone, and her traits show in the pose. | [<img alt="Café logo, baseline and with the skill: three separate icons and an invented tagline, against one kettle that is also a kiln." src="examples/showcase/06-logo.jpg" width="100%">](examples/showcase/06-logo.jpg)<br>**Logo:** one mark a step past the literal, with no tagline. |
| [<img alt="Jazz poster, baseline and with the skill: a saxophone, against a trumpet whose sound becomes the northern lights." src="examples/showcase/08-event-poster.jpg" width="100%">](examples/showcase/08-event-poster.jpg)<br>**Poster:** the name's idea is used; the baseline was already strong. | [<img alt="Exploded lamp view, baseline and with the skill: invented descriptions and parts off-axis, against five labelled parts on one axis." src="examples/showcase/09-product-illustration.jpg" width="100%">](examples/showcase/09-product-illustration.jpg)<br>**Exploded view:** only the five labels, with the parts on one axis. |

Illustrative, not test evidence: one sample each, with six of ten pairs picked by the owner of the work. Notes and the rules that fired: [examples/showcase/](examples/showcase/). The evidence is the [blind test](examples/blind-test/RESULTS.md).

## Style bleed

Each sheet starts with a small thumbnail of the [lookbook](modules/lookbook/) look doing the influencing, then that look applied to one brief at rising strength. The first four are textless previews: a control render (no look), then 20 and 50%. The last three are finished designs with copy: a base render (full rules, no look), then 20, 50 and 80%. LOOK-1 keeps looks at 20-50% by default; LOOK-2 allows 80% only when the look's structure carries the brief's idea, after a check that its subject hasn't crept in.

[<img alt="Heron Jar jam jar label, control and one White-line block print look at 20 and 50%: 20% breaks the sky into white-ringed cells, 50% breaks the whole scene into flat colour cells divided by even white channels." src="examples/lookbook-strength/sheets/b02-02-heron-jar.jpg" width="100%">](examples/lookbook-strength/sheets/b02-02-heron-jar.jpg)<br>**Heron Jar: 50% won.** 20% only showed the white lines once the prompt dropped the control as a reference, so the oval is a little different from the control. *(LB-122 White-line block print; a heron standing in reeds, theme curiosity.)*

[<img alt="Beetle Lens album cover, control and one Circle-framed crest look at 20 and 50%: 20% sets the scene on indigo inside a white laurel ring, 50% flattens it into a centred white-on-indigo crest." src="examples/lookbook-strength/sheets/b02-03-beetle-lens.jpg" width="100%">](examples/lookbook-strength/sheets/b02-03-beetle-lens.jpg)<br>**Beetle Lens: 50% won,** and her skin holds at every level. All three versions have one flaw in common: the beetle in the lens is a second beetle, not the one on the leaf. *(LB-082 Circle-framed crest; a child with a magnifying glass looking at a beetle, theme play.)*

[<img alt="Baker magazine spread opener, control and one WPA Federal Art Project silkscreen poster look at 20 and 50%: 20% flattens the colour into silkscreen inks, 50% is a five-ink WPA-style screenprint with a bold empty slate band." src="examples/lookbook-strength/sheets/b02-07-baker.jpg" width="100%">](examples/lookbook-strength/sheets/b02-07-baker.jpg)<br>**Baker: 50% won,** and his skin holds. The first 50% barely moved from the control and needed a reroll. *(LB-007 WPA Federal Art Project silkscreen poster; a baker pulling bread from an oven, theme abundance.)*

[<img alt="Balloon Season podcast cover, control and one Contour Lozenge Drift look at 20 and 50%: 20% lays thin contour rings over the fields under a flat sage sky, 50% frames the farmland in a tilted lozenge with contour rings and a pale ring behind the balloon." src="examples/lookbook-strength/sheets/b02-09-balloon-season.jpg" width="100%">](examples/lookbook-strength/sheets/b02-09-balloon-season.jpg)<br>**Balloon Season: 50% won.** No head crept in. *(LB-R05R17 Contour Lozenge Drift; a hot-air balloon over farmland, theme change of season.)*

[<img alt="LOW END club poster, base and one collage look at 20, 50 and 80%, with the look's lookbook image as a reference thumbnail: a hooded figure under sound rings, then torn newsprint strips, then CMY circles behind the head." src="examples/lookbook-strength/sheets/17-low-end.jpg" width="100%">](examples/lookbook-strength/sheets/17-low-end.jpg)<br>**LOW END: 80% won.** The look's CMY circles read as speaker cones and its type strips stay illegible; at 50% the scraps carried near-words. *(LB-SD11 CMYK Newsprint Collage.)*

[<img alt="Cold Open podcast cover, base and one three-ink poster look at 20, 50 and 80%, with the look's lookbook image as a reference thumbnail: a figure under a street lamp, then a coat figure in red and navy blocks, then a woman with a red bar across her eyes." src="examples/lookbook-strength/sheets/16-cold-open.jpg" width="100%">](examples/lookbook-strength/sheets/16-cold-open.jpg)<br>**Cold Open: 80% won, with creep.** The red block became a redaction bar across the eyes, right for true crime, but the brief's anonymous coat figure turned into the look's own glamorous woman. *(LB-SD10 Three-Ink Block Poster.)*

[<img alt="Torsion Dance Company brochure, base and one serpentine-figure look at 20, 50 and 80%, with the look's lookbook image as a reference thumbnail: one curled dancer, then ribbon-painted pairs, then figures wrung into one knot." src="examples/lookbook-strength/sheets/06-torsion-dance.jpg" width="100%">](examples/lookbook-strength/sheets/06-torsion-dance.jpg)<br>**Torsion Dance: 80% won.** The look's structure is the brief's idea: figures wrung into one ribbon knot are the strongest read of "torsion". *(LB-155 Serpentine elongated figure painting.)*

Seven sheets, picked by the owner of the work, one kept render per level, not blind. The four textless rows come from a set of ten random bleeds (looks, subjects, themes and domains drawn at random); the three 20/50/80 rows are from the 21-sheet test. Tally and notes: [examples/lookbook-strength/](examples/lookbook-strength/README.md).

## Install

Works with any agent or LLM. [`docs/install.md`](docs/install.md) has the steps, with sources, for each one.

| Agent | Install |
|---|---|
| Grok Bot | One click: [Creative Director bot](https://x.ai/bot/XWBKgRnDOw7uR5SpKx3Af) |
| Hermes Agent | `hermes skills install SnazzyGaz/creative-director/skills/creative-director` |
| Claude Code, Codex, Cursor, Copilot, Devin, Cline | `gh skill install SnazzyGaz/creative-director creative-director --agent <agent>` (or `npx skills add SnazzyGaz/creative-director`) |
| Gemini CLI | `gemini skills install https://github.com/SnazzyGaz/creative-director.git --path skills/creative-director` |
| claude.ai, Claude desktop | Upload [`creative-director-skill.zip`](https://github.com/SnazzyGaz/creative-director/releases/latest/download/creative-director-skill.zip) in Customize > Skills ([steps](docs/install.md#claude)) |
| ChatGPT, Gemini Gems, Claude Projects, any chat LLM | Paste or upload [`creative-director-prompt.md`](https://github.com/SnazzyGaz/creative-director/releases/latest/download/creative-director-prompt.md) (about 11.4k tokens) or the [full bundle](https://github.com/SnazzyGaz/creative-director/releases/latest/download/creative-director-prompt-full.md) (about 97.5k) |
| Aider | `aider --read AGENTS.md` |

The skill is the [`skills/creative-director/`](skills/creative-director/) folder, in the open [Agent Skills](https://agentskills.io/specification) format. Inside a clone of this repo, agents read [`AGENTS.md`](AGENTS.md) directly or through a pointer file ([`CLAUDE.md`](CLAUDE.md), [`GEMINI.md`](GEMINI.md), [`.github/copilot-instructions.md`](.github/copilot-instructions.md), [`.cursor/rules/`](.cursor/rules/creative-director.mdc)). Every route leads back to `AGENTS.md`, and [`llms.txt`](llms.txt) is there for tools that read it.

## Usage

| Mode | What happens |
|---|---|
| **Self-check**<br>`+ creative director` | The agent runs the loop on its own output. Cheapest. |
| **Consult**<br>`consult creative director` | Send the brief and the real output; get back a neutral critique with ranked fixes ([template](core/critique-template.md)). |
| **Direct**<br>`creative director: direct this` | Joins at the start: writes the brief, sets direction, picks from rough options, reviews at checkpoints ([CD-1..7](core/creative-direction.md)). |
| **Remake from scratch**<br>"redo", "rejig", "start over", "reimagine" | Steps back first: what the piece is, who it is for, its one job, the feeling, the given facts (checked against each other) and what must survive. Sends a 5-8 line brief for sign-off, then 4–8 structurally different roughs, a fresh-context same-model head-to-head, the top 2–3 shown for a pick, and only the winner built and runs the full checks ([FP-1..9](core/first-principles.md), [example](examples/first-principles-remake/)). Without these words the light touch stays the default. |
| **Nudge**<br>"bolder", "quieter", "distill" | Bolder adds contrast, scale difference and commitment; quieter lowers whatever competes with the main thing; with a lookbook look applied, each moves its strength one step. Distill removes until the one job still works, and no further ([commands](core/commands.md)). The *Sitting right* guard still applies, so none of them centres things by default. |
| **Variations**<br>"variations", "more directions", "another look", or a generic set | Search the [lookbook](modules/lookbook/): keep an unbeled control, bleed one cluster of two or three related looks (splitting 20-50%), and add one wildcard at hint. Cite LB IDs. If a winner is already picked, bleed the picture only. Never on a fix. |

Always send the actual output (image, screenshot at real size, URL or renders), never a description. Interactive and 3D work is reviewed hands-on: clicked, panned, zoomed and recorded, then judged on how it feels to use, not from stills alone. Video is watched in motion at its delivered size with sound, then scrubbed and sampled frame by frame ([film module](modules/film/review.md)).

## In-repo tools (v0.11.4)

```sh
python3 tools/cd.py brief init 'A short description' --out brief.json
# Fill idea, feeling, fixed copy/counts, size and must-be-right first.
python3 tools/cd.py load --brief brief.json
python3 tools/cd.py check final.png --brief brief.json
python3 tools/cd.py rule CD-7
python3 tools/cd.py select r1.png r2.png r3.png r4.png --brief brief.json
```

[`tools/brief.md`](tools/brief.md) defines the JSON brief and comparison packet. `check` reuses the existing measurement tools; page copy comes from the rendered DOM, image copy from optional system Tesseract or a labelled transcript. Physical counts need crop/count evidence. Missing evidence is SKIP, not PASS; pixel-only type size still needs visual review. No script calls a second model or certifies taste. This is an in-repo helper, not a distributed CLI product.

## Modules

Only `AGENTS.md`, principles and the loop are always loaded: [40 existing rule IDs and compact reminders](core/principles.md#the-40-always-on-rules-v0100), with other rules looked up by `cd.py rule <ID>` or by module for the job ([`core/which-modules.md`](core/which-modules.md)).

| Module | Covers |
|---|---|
| [technical-drawing](modules/technical-drawing/) · [illustration](modules/illustration/) · [character](modules/character/) | perspective, light, anatomy (every hand, limb and face checked; a fail blocks delivery) |
| [web-ui](modules/web-ui/) · [ux](modules/ux/) · [3d](modules/3d/) | screens, flows and accessibility (states, dark mode, reflow, reduced motion, focus order, alt text), clicked and recorded; 3D build defects |
| [typography](modules/typography/) · [layout](modules/layout/) · [brand](modules/brand/) | type, social cards, posters, slides, print, infographics with charts drawn from the data in code; official logos placed unaltered, never redrawn; new logos made idea first and edited by LOGO-1 to 16, with notes on mark making and double readings |
| [composition](modules/composition/) · [colour-value](modules/colour-value/) · [aesthetic-critique](modules/aesthetic-critique/) | balance, focus, beauty and palette, graded from *well supported* to *myth*; intent model and side-by-side verdicts |
| [photo](modules/photo/) | photographs and photoreal images, shot or generated: distance and lens, camera height, named light, casting, styling, retouch limits, generated-photo tells |
| [writing](modules/writing/) (on demand) | website copy, emails and replies, blurbs, about text, UI microcopy and supporting copy: purpose, facts, flow, voice and style |
| [film](modules/film/) (optional) | story first: shots, continuity, light, grading, editing, sound, generated-video QC |
| [lookbook](modules/lookbook/) (optional) | 368 visual looks to offer as directions, named by technique or era, never by living artists; used at 20-50% by default, stronger only on purpose |

Also: a [font library](fonts/) of 107 free families in 29 themes, tagged by mood and searchable with `tools/font_find.py`, and [`tools/`](tools/) for every measurable check (one-command auto check, contrast, vanishing points, ellipses, layout grid, chart and route drawing).

## How it works

```text
idea + brief -> 4–8 roughs -> fresh-context comparison (same model)
 -> show top 2–3 -> owner picks -> render/check/look -> labelled critique
 -> choose fix level -> fix winner -> compare -> keep, revert or stop
```

Edits and consults preserve existing intent; they do not force a new concept round. Intervention levels: **edit, recompose, art-direct, reconceive, rebuild, explore**. Reconception needs authority to revisit the idea.

Each rule has an ID (`CORE-2`, `TD-PER-1`, `UI-6`) and the same parts: what, why, a check you can run, the usual fix, an honest evidence grade, and a source. Only explicit must-be-right brief conditions and **MUST-BE-RIGHT** errors (perspective, anatomy, light, contrast and accessibility, broken flows, 3D build defects) block; everything else is a default. Any picture with a person, hand or animal also gets an anatomy pass: every hand, limb and face is cropped and checked one by one (count, trace to the shoulder, grip, joints), and a fail blocks delivery ([CHAR-9](modules/character/README.md#char-9-anatomy-pass-crop-trace-count-must-be-right-delivery-gate)). Full loop: [`core/critique-loop.md`](core/critique-loop.md).

Passing the rules makes work correct, not necessarily good, so the [composition](modules/composition/), [colour-value](modules/colour-value/) and [aesthetic](modules/aesthetic-critique/) modules handle the rest; the [energy pass](core/energy-pass.md) joins only for stated energetic intent, and a *Sitting right* pass flags placement that looks accidental without pushing work toward centring. **Handing over work with no specific ask** gets a short, ranked list of changes, and nothing changes until you sign off ([`core/interaction-flow.md`](core/interaction-flow.md)).

## Examples

<details><summary>Three more before/after pairs</summary>

<p><picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/before-after-dark.jpg">
  <img alt="Three before/after pairs: a box and can drawing with its perspective rebuilt, a knight illustration with a quieter sky, and a landing page with readable contrast." src="docs/assets/before-after-light.jpg" width="100%">
</picture></p>

Generated, one or two rounds each.
</details>

Take-overs of bad work, nudges, one small case per common agent failure and the baseline above, all with critiques, logs and honest misses: [examples/](examples/), or the [gallery](https://snazzygaz.github.io/creative-director/gallery/). The [cross-model kit](examples/cross-model/) tests it on other models.

## Blind test

The owner of the work judged with-skill and plain-prompt images side by side without knowing which was which: over 100 briefs the skill won 59 to 40 with one tie (one-sided sign test p = 0.035), meeting the 59-of-100 bar set in advance, so a clear result. It leads on pictures, logos and packaging and is behind on screens and infographics. One judge, and later batches were not independent of the rule-writing, so read it as one person's taste, not research. Batches, keys and caveats: [`examples/blind-test/RESULTS.md`](examples/blind-test/RESULTS.md).

## Requirements

- **Vision.** The agent has to *see* its output: a model that accepts images.
- **A way to render or screenshot** the work at real size: a browser for UI, a renderer for 3D, the image file for pictures.
- **Recommended setup:** Playwright or headless Chrome for UI (`tools/shot.sh` uses Chrome; `tools/autocheck.py` uses Playwright for pages), Blender for 3D (plus [model-qa](https://github.com/SnazzyGaz/model-qa) for build checks), and Python 3 with Pillow and NumPy for the `tools/` scripts (the auto check, look tests, contrast, vanishing points, ellipses, layout grid, 3D intersections; `pip install -r tools/requirements.txt`).
- **Without vision** you only get a rules-only review of code or a description. It can still catch contrast, spacing and flow problems in code, but it can't judge how the work looks, and it is much weaker.

Context cost: about 5,900 tokens always loaded (`AGENTS.md`, principles and the loop; about 7,100 with the critique template), plus 1,200-5,800 per module README, with bigger modules split into on-demand files (film: about 10,300 for its three core files) ([table](core/which-modules.md#token-cost-per-module)). Budgets are enforced in CI (`tools/check_budgets.py`). For small context windows, [`lite/CREATIVE-DIRECTOR-LITE.md`](lite/CREATIVE-DIRECTOR-LITE.md) has the loop, core rules and blockers in about 2,500 tokens.

## What's inside

```
core/       always: principles, the loop (with sign-off and delivery). On demand: critique template,
            creative direction, first-principles remake, brand intake, evidence, module picker
modules/    technical-drawing · illustration · character · web-ui · ux · 3d
            typography · layout (social, posters, slides, print) · brand · aesthetic-critique
            composition (balance, focus, unity, space, beauty) · colour-value
            film (cinematography and video, story first: shots, continuity, light, grading, editing, sound, generated-video QC)
            lookbook (optional: 368 established looks and wildcards, tag file and image sheets)
tools/      cd.py: brief init, load, check (JSON), rule <ID>, select; auto check, look tests, WCAG contrast, screenshots, vanishing points, ellipses, layout grid, whitespace, balance, 3D intersections, before/after
examples/   stress tests, round by round, including this README's own critique
fonts/      107 free font families in 29 themes, catalogue and specimen sheets
lite/       the loop, core rules and blockers in one short file
skills/     the installable skill folder, generated from the files above
docs/       gallery, README images, reference library, design notes (DECISIONS.md, RETIRED-IDS.md; PROPOSED-REPO.md is historical)
```

## Principles of the critique

- **Neutral.** Factual, like a thesis supervisor. No praise padding, no harshness.
- **Evidence-labelled.** Rule-backed findings cite IDs; intent-backed findings cite the brief; exploratory findings are options. All carry provenance and confidence, not invented authority.
- **Light touch.** Keep the intent and what already works. At most three fixes a round, then stop when clearly better.
- **Take over when broken.** If the construction is fundamentally wrong, rework it, then re-check it still answers the brief.

This README went through the loop too: [examples/readme-self-critique](examples/readme-self-critique/).

## Sources and evidence

Every rule cites its sources in [SOURCES.md](SOURCES.md); what the research supports, and the myths to stop repeating, are in [core/evidence.md](core/evidence.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md): rule format, honest grades, example images as JPG or WebP at 1280 px or less.

## Licence

MIT, see [LICENSE](LICENSE). Cited works stay with their authors; this repo paraphrases and links to them. The lookbook's `getty_aat` era terms come from the Getty Art & Architecture Thesaurus (AAT), J. Paul Getty Trust, under ODC-By 1.0 ([SRC-266](SOURCES.md)).
