# opencode-image-budget

An [OpenCode](https://opencode.ai) plugin that keeps a request under the provider's image cap by replacing older images with text placeholders.

```
[image omitted to stay under the provider image limit: screenshot.png]
```

## The problem

A model request carries the **whole transcript**, not just the newest message. Every image you paste, and every screenshot a tool returns, stays in that request until the session ends. Providers cap how many images one request may carry — some reject at 16:

```
A request may carry at most 16 images; this one has N
```

Once you cross the cap, the session cannot send **anything**, including a plain text follow-up, because the offending images are still in the history. The only ways out are compacting or starting over.

## What it does

On every outgoing request, `image-budget` counts image parts and image files inside tool results. If the count is over `keep` (default **16**), it replaces the oldest ones with a short text placeholder and sends the trimmed copy. The newest images survive, so the thing you just looked at is still visible to the model.

It works on `context`, `compaction` and `generate` requests, and it is **unscoped by default** — it applies to every provider. Scope it with `providerID` if you only want it on one.

## Install

Published as a Git plugin, so no npm release is needed.

```sh
opencode plugin add github:rishikoushikz/opencode-image-budget
```

Or add it to `~/.config/opencode/opencode.jsonc` yourself:

```jsonc
{
  "plugins": ["github:rishikoushikz/opencode-image-budget"]
}
```

Pin a revision if you want stability:

```sh
opencode plugin add github:rishikoushikz/opencode-image-budget#v0.1.0
```

### Without the CLI

Clone anywhere and point a config entry at the directory:

```jsonc
{
  "plugins": ["~/projects/opencode-image-budget"]
}
```

Or drop `index.ts` and `trim.ts` into `~/.config/opencode/plugins/image-budget/` — files there load automatically.

## Configure

Pass options as an object entry in `plugins`:

```jsonc
{
  "plugins": [
    {
      "package": "github:rishikoushikz/opencode-image-budget",
      "options": {
        "providerID": "deeprelay",
        "keep": 12,
        "debug": true
      }
    }
  ]
}
```

| Option | Default | Meaning |
| --- | --- | --- |
| `providerID` | *unset* | Limit the hook to one provider. Unset applies it to every provider. |
| `keep` | `16` | How many images to keep, newest last. Any integer ≥ 1. |
| `debug` | `false` | Log each trim to the server console. |

Set `keep` to the cap your provider actually enforces — a lower value leaves headroom for images that arrive mid-request.

## Caveat

This is a mitigation, not a fix. A dropped image is **gone from that request**: the model sees the placeholder text and cannot see the picture again unless something re-supplies it. Nothing is written back to your stored history, so the images remain in the session and in the transcript you can scroll — only the outgoing request is trimmed.

If you need the model to reason about an old image, ask it about the image while it is still recent, or re-attach it.

## Development

```sh
npm install
npm test        # bun test — 6 unit tests over the pure trimmer
npm run typecheck
```

The trimming logic lives in [`trim.ts`](./trim.ts) with no SDK imports, so the tests run without an OpenCode runtime. `index.ts` only wires it to the session hooks.

## License

MIT © rishikoushikz
