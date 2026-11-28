# vision-bridge-mcp

Give your text-only [OpenCode](https://opencode.ai) agent eyes.

OpenCode's text-only models (e.g. DeepSeek V4) can't read images — so if you
attach a screenshot of an error, a whiteboard sketch, or a photo of a UI
mockup, the agent has no idea what's in it. `vision-bridge-mcp` is a small
[MCP](https://modelcontextprotocol.io) server that plugs straight into
OpenCode and gives it two new tools: **`analyze_image`** (general
description / visual Q&A) and **`ocr_image`** (exact text transcription),
both backed by the Gemini API (`gemini-3.6-flash` by default — override with `GEMINI_MODEL` if Google
retires it later; check https://ai.google.dev/gemini-api/docs/models for current model IDs).

Once it's configured, you just tell the agent to look at a file:

```
Look at ./screenshots/error.png and tell me what's failing.
```

and it will call `analyze_image` itself — no manual copy-pasting into a
chat window, no separate CLI step.

## Requirements

- Node.js 18 or later
- A free Gemini API key — get one at https://aistudio.google.com/apikey
  (free tier: 1,500 requests/day, no credit card required)

## Install

No cloning required. Add this to your OpenCode config
(`opencode.json` in your project root, or `~/.config/opencode/opencode.json`
for a global setup):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "vision-bridge": {
      "type": "local",
      "command": ["npx", "-y", "vision-bridge-mcp"],
      "environment": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Restart OpenCode (or run `opencode mcp` to reconnect) and the
`analyze_image` and `ocr_image` tools will show up automatically. `npx`
downloads and caches the package the first time it runs — nothing to build
or install by hand.

> Prefer an env var over hardcoding the key in the config file? Set
> `GEMINI_API_KEY` in your shell profile instead and drop the
> `"environment"` block — the server reads it from the process environment
> either way.

### Running it standalone (for development or testing)

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/vision-bridge-mcp.git
cd vision-bridge-mcp
npm install
cp .env.example .env   # then fill in GEMINI_API_KEY
npm start
```

The server speaks MCP over stdio, so on its own it just sits there waiting
for a client (like OpenCode) to connect — that's expected.

## Tools

### `analyze_image`

General-purpose image understanding. Give it a path and, optionally, a
custom prompt.

| Parameter    | Required | Description                                                        |
| ------------ | -------- | -------------------------------------------------------------------|
| `image_path` | yes      | Path to a local image (absolute, or relative to OpenCode's cwd)    |
| `prompt`     | no       | Custom instruction. Defaults to a developer-focused description.   |

### `ocr_image`

Transcribes visible text verbatim — useful for error dialogs, terminal
screenshots, or photographed notes.

| Parameter    | Required | Description                                                     |
| ------------ | -------- | ----------------------------------------------------------------|
| `image_path` | yes      | Path to a local image (absolute, or relative to OpenCode's cwd) |

Both tools support PNG, JPEG, WEBP, GIF, and HEIC/HEIF, up to 20MB by
default.

## Configuration

All configuration is via environment variables (set them directly, in a
`.env` file for standalone use, or in the `"environment"` block of your
`opencode.json` MCP entry):

| Variable                     | Required | Default            | Description                                  |
| ----------------------------- | -------- | ------------------- | --------------------------------------------- |
| `GEMINI_API_KEY`              | yes      | —                    | Your Gemini API key                           |
| `GEMINI_MODEL`                | no       | `gemini-3.6-flash`   | Any Gemini model with vision support          |
| `VISION_BRIDGE_MAX_IMAGE_MB`  | no       | `20`                 | Reject images larger than this                |

The server starts even without `GEMINI_API_KEY` set (so `opencode mcp` can
still list the tools) — it only errors, with a clear message, the moment a
tool is actually called without a key configured.

## Error handling

Every tool call either succeeds with a text result, or fails with
`isError: true` and a specific, actionable message — a missing file, an
unsupported format, a file over the size limit, a missing/invalid API key,
or an upstream Gemini error. The server itself never crashes on a bad call.

## Development

```bash
npm install
npm test    # unit tests (node's built-in test runner, no network needed)
npm run lint
```

The test suite covers path resolution, MIME-type detection, and file
validation (missing files, directories, empty files, oversized files) —
the input-handling logic most likely to break on real-world usage. The
Gemini API call itself isn't mocked/tested here since it requires a live
key; if you want to verify that path, set `GEMINI_API_KEY` and run
`npm start`, then connect with any MCP client (or the
[MCP Inspector](https://modelcontextprotocol.io/legacy/tools/inspector)).

## Publishing (maintainers)

```bash
npm login
npm publish --access public
```

Bump the `version` in `package.json` first — `npx -y vision-bridge-mcp`
always resolves to the latest published version.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT — see [LICENSE](./LICENSE).
