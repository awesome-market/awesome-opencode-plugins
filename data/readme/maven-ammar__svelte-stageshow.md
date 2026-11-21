# svelte-stageshow

Svelte 5 port of **Stageshow**, Benji Taylor's MIT kit for framed faux product
UI: a believable interface, cropped with intent, as one still or a short
scripted demo.

The whole upstream kit is ported: **13 motion primitives, 10 parts, 6 controls,
the Code/Chart/Keyboard/Messages/Prompt/Caret/LockScreen/Notification modules,
35 brand marks, all four looks, and all 69 example scenes.** No React,
react-dom or lucide runtime is shipped; `svelte` is the only peer.

Version **0.2.0** on npm, public repository at `maven-ammar/svelte-stageshow`.

## Install

```sh
pnpm add svelte-stageshow
```

## Use it as an agent skill

Stageshow is, upstream, a skill an agent reads. This port keeps that: `stageshow/` is the
skill, with the same rules and the same fifteen references, rewritten for Svelte. Install it
into an agent the same way you would his:

```sh
npx skills add maven-ammar/svelte-stageshow --skill stageshow
```

The agent then reads `stageshow/SKILL.md`, builds the scene from the kit, and films it to check
its own work.

```svelte
<script lang="ts">
  import { Avatar, Row, Stage, Window } from 'svelte-stageshow'
  import 'svelte-stageshow/style.css'
</script>

<Stage width={640} height={320} className="my-stage">
  {#snippet children(state, rect, layout)}
    <Window title="Customers" className="my-window">
      <div class="my-body">
        <Row selected title="Polaris Studio" subtitle="Scale - 24 seats">
          {#snippet lead()}<Avatar name="Polaris Studio" size={30} tone="accent" />{/snippet}
          {#snippet meta()}$12,400.00{/snippet}
        </Row>
      </div>
    </Window>
  {/snippet}
</Stage>
```

The Stage puts `className` on the outer `.ss-fit`; the scene's own CSS goes
under `.ss-stage`. The stage is the shot: give it a ground and let the window
bleed, rather than wrapping it in another card.

The kit assumes the standard host reset:

```css
*, *::before, *::after { box-sizing: border-box; }
```

Without it, padded max-width boxes (the bento copies) render 56px wide and
wrap differently from the reference; the gallery's `app.css` carries it, and a
consumer should too.

## API

```ts
import {
  // stage and runtime
  Stage, Cursor, Keycaps, useLook, getLook, capsOf, EASE, bezier, easeCss,
  MacPointer, MacIbeam, MacCrosshair, MacPointingHand, MacOpenHand, MacGrab,
  MacWait, MacResize, MacResizeNS, MacResizeEW, MacResizeNWSE, MacResizeNESW,
  // frames
  Window, Bar, Text, Row, Phone, Avatar, Chip,
  Prompt, Caret, LockScreen, Notification, WALLPAPER,
  // motion
  Connector, Count, Roll, Swap, Collapse, Fly, Follow, cellOf, States,
  Stream, Popover, Camera, Scroll, Expand,
  // parts
  BrandMark, brandMarks, Check, Facepile, Icon, Menu, Meter, Pin, Spinner,
  Toast, Tooltip,
  // controls
  Badge, Field, Segmented, Slot, Tabs, Toggle,
  // root modules
  Code, Chart, chartPoints, Keyboard, Thread, Bubble, Stamp, Receipt,
} from 'svelte-stageshow'
```

React prop names are kept verbatim. ReactNode props became `Snippet` (or
`Snippet | string` where a string is enough), and React callbacks became
callback props. `style` is a CSS string. `className` and Svelte's `class` are
merged on every component.

## The Act

`script` is a function given an `Act`:

```svelte
<Stage
  width={720}
  height={340}
  initial={{ open: false, typed: '' }}
  poster={{ open: true, typed: 'Which accounts churned in March?' }}
  script={async (a) => {
    a.mark('ask')
    await a.move('ask', { duration: 520 })
    await a.click('ask')
    await a.set({ open: true })
    await a.wait(180)
    await a.move({ at: 'field', x: 0.9, y: 0.55 })
    await a.type('typed', 'Which accounts churned in March?', { interval: 36 })
    await a.wait(700)
  }}
  cursor={{ at: { wide: { x: 410, y: 94 }, compact: { x: 210, y: 80 } }, idle: false }}
>
  {#snippet children(s, rect, layout)}...{/snippet}
</Stage>
```

The runtime supports `set`, `put`, `wait`, `rect`, `caret`, `center`, `move`,
`click`, `scroll`, `cursor`, `snap`, `key` (with keycaps), `stagger`, `mark`,
`type`, `drag`, `place` and `enter`.

`act.mark(name)` sets `data-mark="name"` on the stage. The upstream recorder's
`film.mjs --at name` waits on that attribute. The exact mark list for every
scene is in [`docs/marks.md`](docs/marks.md).

## Deterministic stepping

`runFrames(n)` runs the same script on a virtual 60fps clock, disables CSS
transitions with `data-still`, flushes Svelte, and returns one SHA-256 per
rendered frame. The gate runs the hero script twice on one page and twice after
a reload: **1,501 frames, identical within run and across loads**.

`scripts/record.mjs` uses the same clock one frame at a time, screenshots each
frame, and hands the PNG sequence to ffmpeg. A 30-frame test produced
`shots/video-port-hero.mp4`; the React reference is
`shots/video-react-hero.mp4`. A recording is deterministic frame-by-frame; live
CSS transitions and text rasterisation are outside the DOM-hash contract.

## What is ported

| Area | Status | Notes |
| --- | --- | --- |
| `Stage`, `Window`, `Bar`, `Text`, `Row`, `Phone`, `Avatar`, `Chip`, `Cursor` | ported | Stage adds `deterministic`; keycaps wired into `act.key`; open/grab cursor share the hand glyph |
| Motion: Camera, Collapse, Connector, Count, Expand, Fly, Follow, Popover, Roll, Scroll, States, Stream, Swap | 13/13 | Roll/Swap/Popover freeze outgoing text/HTML for the fade; layout measurement uses `$effect` + RAF, one frame later than React's layout effect |
| Parts: BrandMark, Check, Facepile, Icon, Menu, Meter, Pin, Spinner, Toast, Tooltip | 10/10 | Icon uses an inline Lucide map; raw stroke width means sub-24px icons are slightly thinner than React's `absoluteStrokeWidth` |
| Controls: Badge, Field, Segmented, Slot, Tabs, Toggle | 6/6 | callback props, same classes and states |
| Code, Chart, Keyboard, Thread, Bubble, Stamp, Receipt, Prompt, Caret, LockScreen, Notification | ported | Thread assigns tails through a registry instead of `cloneElement`; `Bubble` string children have the React minimal-fidelity caveat; FLIP is MutationObserver-driven |
| Brands | 35 marks / 44 SVGs | local artwork, licence files kept under `src/lib/brands/` |
| Looks | light, dark, blueprint, glass | CSS in `style/stage.css`; the `looks` example carries upstream's three identity looks and six studies, not a four-theme sheet |
| Examples | 69/69 registered | all upstream example folders plus `static-card` and `hero-demo`; every scene has copied CSS |
| Cross-browser | Chromium only | Firefox/Safari deferred by owner |

Full per-component status and deviations: [`docs/port-status.md`](docs/port-status.md).

### Known deviations

- `Icon` stroke scaling differs from lucide-react's `absoluteStrokeWidth` below
  24px.
- `Roll`, `Swap` and `Popover` snapshot outgoing plain text/HTML; element
  children in `Swap` can reflect a parent update during the fade.
- `Thread`/`Bubble` use a Svelte registry and MutationObserver instead of
  React.Children/cloneElement and `useLayoutEffect`.
- `annotations` folds upstream's `composed.tsx` studies into the same scene, so
  it exposes 12 marks beyond `index.tsx`; see `docs/marks.md`.
- The `looks` example is the upstream identity/studies page, not a four-theme
  gallery.
- Reduced motion holds the poster (or initial) and stops the script. The
  upstream `--still` flag does not freeze a scripted scene; matched `--at`
  marks are the reliable motion comparison. Reduced-motion spot checks:
  ai-chat **49.7 dB**, hero-demo **36.7 dB**.

## Capture protocol and parity

`/?capture=<slug>` renders one scene under `<main id="example">`; the Stage
keeps its `.ss-fit` class and authored design size. This is the same protocol
as the upstream preview, so the skill's `film.mjs --select '#example'` works
unchanged. `?capture` with no slug shows the 69-scene gallery.

Final acceptance: **71/71 pass, 0 short, 0 missing** at settled marks —
full table in [`shots/acceptance.md`](shots/acceptance.md).

Earlier spot-check stills at 900 CSS px:

| Scene | PSNR | Result |
| --- | --- | --- |
| static-card | **48.3 dB** | pass; 0.00% changed, 0.00% aspect drift |
| hero-demo | **38.1 dB** | pass; 0.31% changed |

After the single bundle was completed (41 sheets), the three black-blob scenes
re-filmed as: messages **39.7 dB** (0.32%), imessage **33.1 dB** (0.49%),
opposite-corners **49.5 dB** (0.00%). The earlier sweep was 21 pass / 15 close
/ 33 fail before that bundle fix; the final per-scene table is
[`shots/acceptance.md`](shots/acceptance.md). Stills are in `shots/ref/` and
`shots/port/`.

## Verify

```sh
pnpm install
pnpm --filter svelte-stageshow build      # 138,656-byte dist/stageshow.css, 41 sheets
pnpm --filter svelte-stageshow check      # 0 errors, 0 warnings
pnpm --filter web build                   # gallery build
pnpm --filter web exec svelte-check --tsconfig ./tsconfig.json --fail-on-warnings
node scripts/sync-css.mjs                 # source CSS entry for the gallery
node scripts/smoke-scenes.mjs             # 69/69 capture routes have a stage
node scripts/determinism.mjs "http://127.0.0.1:4173/?test=determinism"
node scripts/record.mjs "http://127.0.0.1:4173/?capture=hero-demo" --frames 30
node scripts/list-marks.mjs               # mark audit
```

Consumer gate: packed **0.2.0** tarball **189,191 bytes**, installed into a
throwaway SvelteKit app, production build wrote **19 files** and completed.
The throwaway consumer preview was closed after the build.

## Licence and source

Ported from the public **`benjitaylor/skills`** Stageshow source, MIT,
© 2026 Benji Taylor. The original `LICENSE` and `NOTICE.md` are kept, with
port attribution. Brand artwork retains its upstream licence files.
`reference/` is ignored and not shipped.
