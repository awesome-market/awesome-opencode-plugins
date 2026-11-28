# img-read

Read an image with a vision model (LM Studio / OpenAI-compatible, local or remote). Use it as a **CLI** (streams the description to stdout) or as a **library** (returns the result object).

[![npm Package Version](https://img.shields.io/npm/v/img-read)](https://www.npmjs.com/package/img-read)

## Features

- **CLI**: read an image from a file path, positional arg, or stdin; stream reasoning + content + refusal to stdout
- **Library**: `read_img()` returns `{ reasoning_content, content, refusal }`
- Auto-detect image vs prompt by file extension (`--file`)
- Console output with ANSI colors, or `--json`
- Works with any OpenAI-compatible vision model (LM Studio, Ollama, remote APIs)
- Built-in TypeScript support

## Installation

```bash
npm install img-read
```

You can also install `img-read` with [pnpm](https://pnpm.io/), [yarn](https://yarnpkg.com/), or [slnpm](https://github.com/beenotung/slnpm)

## CLI Usage

The CLI is designed to be called by an **AI agent** (or a human) to read an image and get a text description. It reads from stdin or a file path, so an agent can pipe an image in and capture the output.

```bash
# read an image file
img-read image.png

# read an image from a URL (pipe curl output)
curl -s https://example.com/image.png | img-read

# auto-detect image vs prompt by extension
img-read --file image.png --file prompt.txt

# custom prompt
img-read image.png --prompt "Extract the table and output as markdown"

# custom model (base url auto-detected)
img-read image.png --model glm-5.3-flash

# JSON output (machine-parseable)
img-read image.png --json

# remote server with API key
img-read image.png --base-url https://api.example.com/v1 --api-key YOUR_KEY
```

Run `img-read --help` for all options.

## Library Usage

All fields are required (no defaults in the library). The values below match the CLI defaults for a local LM Studio setup.

**Example 1 — extract a table as CSV:**

```typescript
import { read_img } from 'img-read'

let result = await read_img({
  input: 'ollama-cloud-usage.png',
  prompt:
    'Extract the table from this image and output it as CSV without any other text',
  base_url: 'http://localhost:1234/v1',
  model: 'google/gemma-4-e2b',
  api_key: 'no-api-key',
  // max_completion_tokens is optional; leave unset so reasoning models
  // have room to finish thinking and still produce content
  on_content: content => process.stdout.write(content),
})

// result.content holds the CSV table in string
```

**Example 2 — extract two fields as JSON (no streaming, use the result):**

```typescript
import { read_img } from 'img-read'

let result = await read_img({
  input: 'receipt.png',
  prompt:
    'Extract the total amount and the date from this receipt. ' +
    'Output as JSON: {"total": "...", "date": "..."} without any other text',
  base_url: 'http://localhost:1234/v1',
  model: 'google/gemma-4-e2b',
  api_key: 'no-api-key',
})

// result.content holds the JSON, e.g. {"total": "HK$120", "date": "2026-08-30"}
```

## Typescript Signature

```typescript
export async function read_img(args: {
  input: string
  prompt: string
  base_url: string
  model: string
  api_key: string
  max_completion_tokens: number
  reasoning_effort?: ReasoningEffort
  on_reasoning_content?: (content: string) => void | Promise<void>
  on_content?: (content: string) => void | Promise<void>
  on_refusal?: (refusal: string) => void | Promise<void>
}): Promise<{
  reasoning_content: string
  content: string
  refusal: string
}>
```

## License

This project is licensed with [BSD-2-Clause](./LICENSE)

This is free, libre, and open-source software. It comes down to four essential freedoms [[ref]](https://seirdy.one/2021/01/27/whatsapp-and-the-domestication-of-users.html#fnref:2):

- The freedom to run the program as you wish, for any purpose
- The freedom to study how the program works, and change it so it does your computing as you wish
- The freedom to redistribute copies so you can help others
- The freedom to distribute copies of your modified versions to others
