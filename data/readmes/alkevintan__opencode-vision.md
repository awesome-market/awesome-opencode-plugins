# opencode-vision

Give a cheap, text-only model eyes.

An [opencode](https://opencode.ai) plugin that registers a `vision` tool. When your
coding model hits an image, screenshot, diagram, or PDF, it asks a vision model one
specific question and gets back only the answer — no analysis, no advice, no code.

Your main model stays cheap. Only the pixels go to a model that can see them.

## Why

Switching your whole session to a vision model to read one screenshot is expensive: every
subsequent turn re-sends the entire conversation to the pricier model. This keeps the
vision call to a single round trip in a throwaway session, then throws it away.

A typical call costs **well under a cent**.

## Install

Drop the plugin into your opencode config directory:

```sh
mkdir -p ~/.config/opencode/plugin
curl -fsSL https://raw.githubusercontent.com/alkevintan/opencode-vision/main/src/vision.ts \
  -o ~/.config/opencode/plugin/vision.ts
```

Restart opencode. The `vision` tool is now available to every model.

You need at least one authenticated provider serving a vision-capable model
(`opencode auth login`).

## Use

You normally don't call it — your model does, on its own:

```
> what does this error screenshot say?          # paste an image
> read the totals in reports/q3-invoice.pdf
```

It handles two sources:

- **Files on disk** — the model passes `paths`.
- **Pasted or attached images** — the model omits `paths` and the tool pulls the
  attachment straight out of the conversation. A clipboard paste never touches disk;
  opencode stores it as a `data:` URL on the message, and the tool reads it from there.

### Making a non-vision model actually use it

A model without vision doesn't know what it's missing — it sees an attachment it can't
decode and apologises. So the plugin also watches incoming messages: when a model that
lacks image input receives an attachment, it appends one line telling it to call the
`vision` tool.

This means **the plugin adds a synthetic text part to user messages** on non-vision
sessions. It's the piece that makes discovery work, but it is real behaviour beyond
registering a tool, so it's called out here rather than buried. Models that can already
see are never touched.

## Configuration

Default model: **`openai/gpt-5.6-luna`**.

The default is treated as a model *name*, not a fixed provider. The tool finds every
authenticated provider serving `gpt-5.6-luna`, tries the cheapest first, and moves on if
one has a dead credential — so a bad `OPENAI_API_KEY` doesn't break it. A failed auth
handshake costs no tokens.

Override per call:

```
> use openrouter/openai/gpt-5.6-luna to read this chart
```

An explicit override is used exactly as given — no silent substitution. To change the
standing default, edit `DEFAULT_MODEL` at the top of the file.

Only vision-capable models are accepted. A model without image input is rejected with a
list of ones that work, cheapest first. Image *generation* models are kept out of that
list — they accept images but don't describe them — though an explicit override can
still reach them.

## How it stays cheap

- A fresh child session per call, deleted afterwards, so no conversation history is
  ever re-sent — the dominant cost in a long session.
- Every tool disabled inside that session: one round trip, no agentic loop.
- A system prompt that forbids preamble, advice, speculation, and code. If the answer
  isn't visible it replies `NOT VISIBLE` rather than guessing.
- Only text parts reach the caller; reasoning and step parts are dropped.
- Files are validated before anything is read or encoded, so a bad model or a missing
  file never costs an encode.

## Limits

- Up to 4 files per call, 10MB each.
- `png`, `jpg`, `jpeg`, `webp`, `gif`, `bmp`, `heic`, `heif`, `pdf`.
- Attachments come from the most recent message that has any, so an older screenshot
  can't silently ride along.
- The PDF path is implemented and capability-gated but has not been exercised
  end-to-end.

## Licence

MIT
