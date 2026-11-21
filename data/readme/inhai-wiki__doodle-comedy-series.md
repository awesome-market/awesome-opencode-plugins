<div align="center">
  <img src="assets/cover.jpg" alt="White-ground doodle comedy shorts" width="900" />
  <h1>Doodle Comedy Series</h1>
  <p><strong>One line of dialogue → a 68-second 3:4 vertical short, a matching cover, and a full set of WeChat Channels publish assets. Reproducible, auditable, zero style drift.</strong></p>
  <p>
    <code>Claude Code</code> · <code>OpenClaw</code> · <code>Codex</code> · <code>MiniMax Code</code> · <code>Agent Skill</code>
  </p>
  <p>
    <a href="#quick-start">Quick Start</a> ·
    <a href="#shot-to-frame">How a shot becomes a frame</a> ·
    <a href="#pipeline">Full pipeline</a> ·
    <a href="#scripts">Script reference</a> ·
    <a href="EVALUATION.md">Evaluation</a> ·
    <a href="README.zh-CN.md">中文文档</a>
  </p>
</div>

---

## What this is

A **short-video production line for AI agents**, built for one specific look:
a pure white ground, black line art, big-headed stick figures, 行楷 (running-script) captions
with red keywords — the kind of vertical, deadpan short where workplace absurdity gets drawn.

It is not about writing a joke. Models write jokes fine. What this skill covers is the
pile of details between *one line of dialogue* and *a finished video you can actually post*:

| Where things usually go wrong | How the skill catches it |
| --- | --- |
| Text on screen lands on top of a face | `check_overlap.py` audits the geometry — **non-zero exit means fix it** |
| Captions split a word in half, or emit an empty line | `build_segments.py` is quote-aware and enforces three hard invariants |
| 498 characters written — how long is that? | The script prints an estimated duration and warns past ±10% |
| The cover doesn't match the episode | Covers are **redrawn with the same primitives and fonts**, never AI-generated |
| The cover looks fine full-size but dies in the feed | A 300px thumbnail readability check before delivery |
| Titles and tags written by hand, off-spec | `make_metadata.py` enforces ≤22-char titles and tags that must appear in the description |
| Episode runs 71s and the series drifts longer | `deliver.py` solves for an atempo that lands the cut on target |

**Zero style drift** is the central promise. Re-running the pipeline on the three delivered
covers reproduces them **pixel for pixel** (pixel diff = 0) — because the cover and the film
are drawn by the same `Canvas` in the first place.

<p align="center">
  <img src="assets/style-board.jpg" alt="Visual spec" width="900" />
</p>

---

## Quick Start

Install the whole repository into your agent (`SKILL.md`, `scripts/`, `references/`, `examples/`),
then send it one line:

```text
Use doodle-comedy-series to make a 68-second 3:4 vertical short about "a worker's first
resignation", with a cover and WeChat Channels title, description and tags.
```

If you only want the script first:

```text
Use doodle-comedy-series to write a "first resignation" episode. Show me the voice-over
script, the storyboard and the cover copy first — I'll confirm before you render.
```

Install (works with Claude Code, Codex, MiniMax Code, and any framework that supports
GitHub skill installation):

```bash
git clone https://github.com/inhai-wiki/doodle-comedy-series.git
```

Four complete example episodes ship in `examples/` so you can see the output immediately.

---

## What one episode delivers

| Output | File | Spec |
| --- | --- | --- |
| Subtitled cut | `out/<title>_简笔吐槽_字幕版.mp4` | 1080×1440, 30fps, H.264+AAC, ≈68s |
| Clean cut | `out/<title>_简笔吐槽_无字幕版.mp4` | same, caption layer removed |
| Subtitles | `out/<title>.srt` | ≤16 chars per line, monotonic, non-overlapping |
| 3:4 cover | `out/<title>_封面.png` | 1080×1440, same line weight and fonts as the film |
| Publish assets | `publish.md` + `publish.json` | 3 title options, 1 description, 5–8 topics, 1 pinned comment |

Plus `out/<title>_预览.png`, a four-frame contact strip so you can review an episode at a glance.

---

## How a shot becomes a frame

This is the heart of the skill: **every line of dialogue maps to one scene function, and the
function returns one frame.**

The four GIFs below put the *input* (the `story.json` line plus the code that draws it) next to
the *output* (real frames pulled out of the delivered film). The frames are extracted from the
shipped cut, so what you see is exactly what ships.

### 1. 人情世故 · `prepay`

```json
{ "scene": "prepay",
  "text": "我算是看明白了，人情世故就是大型预付。",
  "red": ["大型预付"] }
```

<p align="center">
  <img src="assets/gifs/prepay.gif" alt="人情世故 · prepay" width="820" />
</p>

### 2. 养生朋克 · `split_life`

```json
{ "scene": "split_life",
  "text": "我今年三十，养生和放纵各占一半。",
  "red": ["养生", "放纵"] }
```

<p align="center">
  <img src="assets/gifs/split_life.gif" alt="养生朋克 · split_life" width="820" />
</p>

### 3. 相亲现场 · `requirement`

```json
{ "scene": "requirement",
  "text": "第一个要求：有房有车有稳定工作。",
  "red": ["有房有车"] }
```

<p align="center">
  <img src="assets/gifs/requirement.gif" alt="相亲现场 · requirement" width="820" />
</p>

### 4. 第一次离职 · `hand_in`

```json
{ "scene": "hand_in",
  "text": "我写了三版，交上去领导说：再想想？",
  "red": ["三版", "再想想"] }
```

<p align="center">
  <img src="assets/gifs/hand_in.gif" alt="第一次离职 · hand_in" width="820" />
</p>

### Writing a scene function

One scene, one function, fixed signature:

```python
def scene_prepay(c, t, d):
    """Opening: the hero holds a bill. Action: he turns around. Payoff: the screen lights up."""
    p = clamp(t / d)          # 0 → 1 progress
    person(c, 262, 612, 1.04, 'dead', False, 'point', t)
    c.rect((534, 404, 1014, 966), 6, r=16)
    c.text((774, 502), '预付', 40)
    if p > .5:
        c.text((700, 614), '订单确认中', 34)
```

- `c` is the canvas (`Canvas`), exposing `rect / ellipse / line / poly / curve / text`
- `t` is the time inside this shot (seconds), `d` its duration — **animation is driven by these two**
- Paint background elements first, then characters, then text
- Redefine `SCENES = {"prepay": scene_prepay, ...}` at the end of the file, this episode's ids only

All drawing primitives live in [`scripts/render/doodles.py`](scripts/render/doodles.py):
`person` `head` `woman` `speech` `paper` `phone` `laptop` `battery` `bubble`
`calendar` `popup` `desk` `hand` `rays` `coin` `cart` `plant` `stamp` …
They are plain functions and compose freely.

> ⚠️ Two traps: `c.curve` takes **exactly 4 control points**; `c.text` supports **no stroke and
> no wrapping**, and `(x, y)` is a **centre anchor**.

---

## Full pipeline

### 0. Environment

```bash
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
export PATH="/opt/homebrew/bin:$PATH"     # ffmpeg is often not on the default macOS PATH
```

> If `python3` fails with `You have not agreed to the Xcode license agreements` (exit 69),
> your system Python isn't set up. Build the venv with a working interpreter instead —
> `/opt/homebrew/bin/python3.13 -m venv .venv` — rather than touching Xcode's licence.

Voice synthesis goes through `mcode-tools` (MiniMax TTS/ASR); the `mcode-tools-master` skill
must be on PATH.

### 1. Topic and series positioning

One episode: just name a comedic register. A series: give each episode a **mutually exclusive
register** — never the same joke in a new costume.

- **Self-deprecating absurdity** (the narrator spirals)
- **Dialogue reversal** (two people talk; the last line flips it)
- **Cold observation** (dry, detached, quietly cutting)
- **Absurd premise taken seriously**

Adjacent episodes in a series should differ in register. See
[`references/series-plan.md`](references/series-plan.md).

### 2. Write the script

Read [`references/writing-style.md`](references/writing-style.md). Hard requirements:

- One line, one shot — roughly 40–45 lines, 480–520 characters, landing near 68s
  (**characters ÷ 7.4 ≈ seconds**)
- Every punchline needs a **visible** action or prop change; subtitles alone don't count
- The ending flips the power relationship and leaves one line worth screenshotting

Write it as JSON:

```json
{
  "title": "第一次离职",
  "target_seconds": 68,
  "segments": [
    {"scene": "decide", "text": "我决定离职了。", "red": []},
    {"scene": "return_form", "text": "第一行：物品返还单。", "red": ["物品返还单"]}
  ]
}
```

`scene` is the shot id; `red` lists the keywords to paint red (each must appear verbatim in `text`).

**The timing constant**: the finished cut runs at **7.17–7.69 characters/second**
(measured across three episodes, mean 7.47), hence ÷ 7.4. The raw TTS track is slower
(6.3–7.2) because every line carries a pause; `deliver.py` solves for an atempo afterwards.

### 3. Cut the shots

```bash
.venv/bin/python scripts/build_segments.py --story story.json --out project_ep4
```

Captions are cut at punctuation to ≤16 chars per line — the renderer cannot lay out 17+.
The break is chosen near 10 characters so words aren't split in half ("大型预付" never
becomes "大型预" + "预付"); a quoted phrase stays intact, so no caption ever starts with a
dangling `」`. The script validates red words, checks that nothing was lost, rejects
punctuation-only captions, and prints an estimated duration with a warning past ±10%.

### 4. Draw the shots

Write `scene_<id>(c, t, d)` functions in `project_ep4/scenes.py` and redefine `SCENES` at the
bottom with this episode's ids only. Primitives: [`scripts/render/doodles.py`](scripts/render/doodles.py).

Then pass two gates:

```bash
.venv/bin/python scripts/check_overlap.py project_ep4/scenes.py   # static layout audit
.venv/bin/python scripts/check_project.py project_ep4             # caption check + contact sheet
```

`check_overlap.py` catches text over characters, text overlapping text, and elements outside
the safe area. It already recognises two cases that *look* like collisions but aren't
(mutually exclusive text in an if/else, and a white block painting over an old element), so
what it reports is usually a real bug — **fix it before rendering**.

When an overlap is intentional (a badge painted on a character's chest), register it explicitly:

```python
OVERLAP_ALLOW = {"three_years", "me_too"}
```

`check_project.py` checks captions before drawing the contact sheet: the captions must spell
the same sentence as the script (hand-polished punctuation is fine; extra, missing or swapped
words are not), and no caption may be empty. It exits immediately on failure instead of wasting
time on a contact sheet nobody can trust.

### 5. Voice

```bash
.venv/bin/python scripts/build_voice.py --project project_ep4 --speed 1.5 --gap 0.10
```

**Per-line synthesis** is the key: every line is TTS'd on its own, silence-trimmed, and
re-joined with a fixed gap. Because each line's start and end are *known*, `asr.json` is
constructed directly from them — subtitle alignment is exact, with no word-level ASR needed.

### 6. Timeline, render, verify

```bash
.venv/bin/python scripts/deliver.py project_ep4 第一次离职 --target 68
.venv/bin/python scripts/verify.py project_ep4
```

`deliver.py` solves for the atempo that lands the cut on target, so the series doesn't drift
longer every episode. `verify.py` runs the ASR round-trip, the subtitle timing check and a
decode check.

### 7. Cover

```bash
.venv/bin/python scripts/make_cover.py project_ep4
```

The cover is **not AI-generated**. You define the main visual in the project's `cover.py`
as `illustration(c)`, and the script renders it with **the same primitives and fonts as the
film**, at 1080×1440:

```python
# project_ep4/cover.py
def illustration(c):
    c.rect((556, 452, 1026, 916), 7, r=26)
    c.text((791, 546), '人情账户', 36)
    person(c, 250, 640, 1.32, 'dead', False, 'stand', 0, arms=False)
    speech(c, 112, 406, 212, 96, 'down', 46)
    c.text((218, 454), '夸', 46)
```

The copy lives in `project_ep4/cover.json`:

```json
{"title": "人情世故", "subtitle": "大型预付", "title_size": 146,
 "lines": [{"text": "请先开口", "size": 64}, {"text": "值就输了", "red": "输了", "size": 64}]}
```

Layout skeleton, margins and the "one visual centre is enough" rule are in
[`references/cover-design.md`](references/cover-design.md). Before shipping, shrink the cover to
300px wide and look — the headline still has to read in a feed.

### 8. WeChat Channels assets

```bash
.venv/bin/python scripts/make_metadata.py project_ep4 \
  --titles "title A" "title B" "title C" \
  --desc "description body, topics inline as #topic" \
  --tags "topic1" "topic2" "topic3" \
  --comment "pinned comment"
```

The script enforces: titles ≤22 chars with one emoji each, a 2–3 line description whose first
line is the hook, **5–8 topics that all appear inside the description**, and a pinned comment
that doesn't merely repeat the description. Details in
[`references/publish-channels.md`](references/publish-channels.md).

Run with no arguments to get **material mode**: the full script, the red-word table, frequent
words and the last three lines, ready for writing:

```text
=== project_ep4 素材包 ===
【标题候选要抓的点】[...]
【高频词】我说 她说 ...
【全稿】
  01 [decide] 我决定离职了。
  ...
```

---

## Script reference

| Script | What it does | Exit code |
| --- | --- | --- |
| `build_segments.py` | story.json → segments.json; cuts captions, validates red words, estimates duration | non-zero = the script is wrong |
| `check_overlap.py` | static layout audit: text over characters, text over text, out-of-bounds | non-zero = must fix |
| `check_project.py` | caption/script consistency check, then renders a contact sheet | non-zero = must fix |
| `build_voice.py` | per-line TTS, silence trimming, fixed-gap join into `voice.wav` | — |
| `tts.py` | TTS wrapper with rate-limit retry and local caching | — |
| `deliver.py` | solves atempo, builds the timeline, renders, archives into `out/` | non-zero = render failed |
| `verify.py` | ASR round-trip, subtitle timing check, decode check | non-zero = something's wrong |
| `make_cover.py` | redraws the 3:4 cover with the film's own primitives | — |
| `make_preview.py` | builds the four-frame preview strip | — |
| `make_metadata.py` | publish assets: material mode / publish mode | non-zero = off-spec |
| `render/render.py` | the renderer itself (ffmpeg encoding) | — |
| `render/prepare.py` | timeline alignment, caption timestamps, audio mix | — |
| `render/doodles.py` | every drawing primitive | — |
| `render/common.py` | shared helpers and `segments.json` structure validation | — |
| `render/fonts.py` | discovers a usable Chinese 行楷 / 黑体 without bundling fonts | — |

**Three hard gates**: `check_overlap` → `check_project` → `verify`.
A non-zero exit from any of them means go back and change something —
**don't render with a red light**.

---

## Examples

`examples/` holds four complete episodes:

| Episode | Register | Central analogy |
| --- | --- | --- |
| [人情世故](examples/人情世故/) | cold observation | 人情世故就是大型预付 |
| [养生朋克](examples/养生朋克/) | self-deprecating absurdity | 养生和放纵各占一半 |
| [相亲现场](examples/相亲现场/) | dialogue reversal | 我妈给我报了七个相亲角 |
| [第一次离职](examples/第一次离职/) | absurd premise | 离职要填物品返还单 |

Each contains `scenes.py`, `segments.json`, `cover.py` + `cover.json`, `publish.md`,
`cover.png`, `preview.png` and `subtitles.srt`.

---

## Does it actually help?

We ran a controlled comparison: the same task (a 68-second short + 3:4 cover + Channels
assets), one group with the skill and one without. The baseline could still use the older
Codex-side skill and the three delivered episodes.

The finding: **the skill does not make the writing better.** The baseline's central analogy
("resigning is uninstalling an app tied to your phone number") was sharper than ours
("a return slip"), and its red-word density was higher (1.11 vs 0.74 per line). But the
baseline delivered text specifications only — no cover image, no runnable `scenes.py`,
no validated publish assets.

**The skill's value is turning "script → film → cover" from an unrepeatable process into
one command you can re-run.**

The evaluation also exposed three genuine defects in the skill itself (a wrong timing
constant, a caption splitter that broke quoted dialogue, and captions that could drift from
the script). All three are fixed and covered by regression tests. Full report:
[`EVALUATION.md`](EVALUATION.md).

---

## Verify it yourself

The repository is self-contained — the examples in `examples/` are the real, delivered
projects, not re-drawn mock-ups. Clone it and check:

```bash
pip install -r scripts/requirements.txt

# 1. the layout audit passes on every shipped episode
for e in examples/*/; do python scripts/check_overlap.py "$e/scenes.py"; done

# 2. re-draw a cover from the example and compare with the shipped PNG
python scripts/make_cover.py examples/第一次离职 --out /tmp/cover.png
python - <<'EOF'
from PIL import Image, ImageChops
a = Image.open("/tmp/cover.png").convert("RGB")
b = Image.open("examples/第一次离职/cover.png").convert("RGB")
print("pixel diff:", ImageChops.difference(a, b).getbbox() or "IDENTICAL")
EOF
```

Step 2 prints `IDENTICAL` — the cover in this repository really is the cover that ships,
produced by the same primitives as the film.

---

## Troubleshooting

**`python3` fails with an Xcode licence error (exit 69)**
Your system Python isn't set up. Build the venv with a working interpreter:
`/opt/homebrew/bin/python3.13 -m venv .venv`.

**`ffmpeg: command not found`**
`export PATH="/opt/homebrew/bin:$PATH"`.

**Voice synthesis is slow**
The upstream TTS is rate-limited; `build_voice.py` retries and caches automatically. Lines
already synthesised are not redone — re-run the same command after an interruption and it
resumes where it stopped.

**The render fails with `Subtitle is too long`**
A caption exceeded 17 characters. Shorten the line, or let `build_segments.py` re-cut it.

**I want to keep an element that looks like an overlap**
Register it in `scenes.py` as `OVERLAP_ALLOW = {"scene_id"}` and note why.

---

## License

[MIT](LICENSE) © 2026 inhai-wiki
