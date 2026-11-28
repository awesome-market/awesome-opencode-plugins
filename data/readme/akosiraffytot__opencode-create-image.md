# opencode-create-image

Generate images from any OpenAI-compatible API directly inside opencode. The plugin registers a single `create_image` tool so the agent can generate and save images on its own — no manual commands, no copying URLs.

## What it does

The agent calls `create_image` whenever a page or piece of visual content needs imagery. The agent writes the prompt itself, the plugin generates the image through your configured API endpoint, saves it to disk, and returns the absolute file path (plus a file attachment). The agent can then drop that file into the page it is building.

### Example: fitness app landing page

You ask opencode to build a landing page for a fitness app. During the build the agent needs a hero image, so it calls `create_image` itself:

- The agent writes a detailed prompt ("runner crossing a finish line at sunrise, energetic motion, bold backlighting, saturated coral and indigo palette, magazine-style sports photography") and calls `create_image` with `size: "1792x1024"`.
- The plugin generates the image and returns an absolute path like `C:\path\to\project\images\2026-08-15T10-30-00-000Z-runner-crossing-a-finish-line-at-sunrise.jpg`.
- The agent reads that path, references `./images/...` in the page markup, and moves on to the next image.

This is autonomous plumbing: the plugin handles the API call, the file write, and the path hand-off so the agent can keep building.

## Install

```sh
# global (all projects)
opencode plugin opencode-create-image -g

# current project only
opencode plugin opencode-create-image
```

Or add it to your opencode config in tuple form with options:

```json
{
  "plugin": [["opencode-create-image", { "baseUrl": "...", "model": "..." }]]
}
```

## Configuration

The plugin is configured through plugin options (which win) or environment variables:

| Setting      | Plugin option | Env var              | Default                        |
| ------------ | ------------- | -------------------- | ------------------------------ |
| API key      | `apiKey`      | `OPENAI_API_KEY` or `OPENAI_KEY` | — (required)       |
| API base URL | `baseUrl`     | `OPENAI_BASE_URL`    | `https://api.openai.com/v1`    |
| Model        | `model`       | `OPENAI_IMAGE_MODEL` | `gpt-image-1`                  |
| Size         | `size`        | —                    | `1024x1024`                    |
| Quality      | `quality`     | —                    | `auto`                         |
| Output dir   | `outputDir`   | —                    | `images`                       |

Plugin options always take precedence over environment variables.

### Tool arguments

The `create_image` tool accepts:

- `prompt` (string, required) — detailed description of the image to create
- `size` (enum: `1024x1024`, `1024x1792`, `1792x1024`, `auto`) — optional
- `quality` (enum: `auto`, `standard`, `high`) — optional
- `outputDir` (string) — directory relative to the project dir; defaults to `images`

### Output

Images are saved under `<project>/images/` with timestamped filenames (e.g. `2026-08-15T10-30-00-000Z-hero-runner.jpg`). The tool result returns the absolute file path plus a file attachment so the agent can inspect and reference the image.

## Compatibility

- Works with any OpenAI-compatible API that implements the `/v1/images/generations` endpoint (any provider exposing the standard `/v1/images/generations` shape; Azure OpenAI needs a compatible gateway/proxy, and many local/self-hosted providers).
- Handles both `b64_json` and `url` response formats.

## Companion skill

The repo ships a companion skill in `skills/create-image` that keeps generated image sets cohesive (consistent art direction, prompt quality guidance). Install it by copying the folder into your skills directory:

```sh
cp -r skills/create-image ~/.config/opencode/skills/
```

or add it to your opencode config with a `skills.urls` entry pointing at this repository.

## Development

```sh
bun install
bun run typecheck
bun run test
bun run build
```

## License

MIT
