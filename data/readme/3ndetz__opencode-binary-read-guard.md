# opencode-binary-read-guard

A tiny [opencode](https://github.com/sst/opencode) plugin that stops the model from
`read`-ing **raw binary files** — which wastes huge amounts of context tokens and is a
common cause of opencode **hangs and OOM crashes**.

## The problem

opencode's built-in `read` tool, pointed at a binary file (`.png`, `.jpg`, `.pdf`, `.zip`,
`.mp4`, a font, a `.so`, …), feeds the raw bytes into the model context:

- **On a text-only model it's pure waste** — the model can't see an image, yet the
  base64/blob is billed as input tokens. A single 1 MB screenshot ≈ hundreds of thousands
  of tokens **per read**.
- **On any model it can crash opencode.** A large binary blows past the context window and
  routinely **hangs or OOM-kills** the process — especially in headless / server runs where
  there's no human to abort. This bites agents that loop and re-read a screenshot every turn.

## What it does

It hooks `tool.execute.before` and transparently **redirects** the `read` so the raw binary
is never loaded:

| File type | Redirected to |
|-----------|---------------|
| Images (`png jpg jpeg gif webp bmp svg …`) | a short **text note**: "binary image — use a multimodal/vision tool, don't read raw" |
| `pdf` | timeout-bounded **`pdftotext`** extraction → returns the **text** |
| Other binaries (`mp4 zip jar so woff sqlite …`) | a short **text note**: "binary — extract with the right tool" |
| Plain text | passes through untouched |

The note/extract files are written inside your project (`.opencode/.binguard/`) so the
redirected read needs no extra approval. The hook never throws — if anything goes wrong it
simply leaves the read alone.

## Install

**Option A — drop-in file (simplest):**

```bash
mkdir -p .opencode/plugin
curl -L https://raw.githubusercontent.com/3ndetz/opencode-binary-read-guard/main/index.js \
  -o .opencode/plugin/binary-read-guard.js
```

opencode loads every `*.js` in `.opencode/plugin/` automatically.

**Option B — as a package** in your `opencode.json`:

```jsonc
{
  "plugin": ["opencode-binary-read-guard"]
}
```

(install it with your package manager from this repo / npm.)

## Notes

- PDF extraction needs `pdftotext` (from `poppler-utils`) on PATH; without it the PDF branch
  returns a short note instead of text.
- It only guards the `read` tool — your model can still operate on binaries through proper
  tools (vision models, `ffmpeg`, `python`, `unzip`, …).
- Want a different extension list or a custom image hint? It's ~80 lines of plain JS — fork
  `index.js` and tweak `IMG` / `BIN` / the note text.

## License

MIT © 3ndetz
