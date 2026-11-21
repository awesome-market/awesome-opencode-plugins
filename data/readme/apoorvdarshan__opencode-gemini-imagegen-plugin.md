# opencode-gemini-imagegen-plugin

An [OpenCode](https://opencode.ai) V2 plugin that gives your coding agent **AI image
generation** through Google's Gemini image models ("Nano Banana").

Ask the agent for an image and it gets generated, saved to disk, and shown in the
session.

## Features

- **`generate_image` tool** — the agent calls it with a prompt.
- **`/imagine <prompt>` command** — generate from the prompt box.
- **Per-call model override** — pick Nano Banana 2 / Lite / Pro per request.
- **Aspect ratios & resolutions** — 1:1 … 21:9, 1K / 2K / 4K.
- **Safe by default** — never overwrites an existing file (adds `-v2`, `-v3`, …).
- **No secrets in code** — the API key is read from env or a local config file.

## Requirements

- OpenCode V2
- A Gemini API key — get one free (for testing) at
  <https://aistudio.google.com/apikey>

## Install

Clone straight into your OpenCode plugins directory:

```sh
git clone https://github.com/apoorvdarshan/opencode-gemini-imagegen-plugin \
  ~/.config/opencode/plugins/gemini-imagegen
```

OpenCode auto-discovers plugins under `~/.config/opencode/plugins/` (one
directory per plugin). Restart OpenCode, or let it hot-reload.

Prefer to keep it elsewhere? Add the path to `plugins` in
`~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "plugins": ["/absolute/path/to/opencode-gemini-imagegen"]
}
```

## Configure

Provide the API key **one** of two ways.

**1. Environment variable** (in your shell profile):

```sh
export GEMINI_API_KEY="your-key"
# or: export GOOGLE_API_KEY="your-key"
```

**2. Config file** — `~/.config/opencode/plugin-data/gemini-imagegen/config.json`:

```json
{
  "apiKey": "your-key",
  "model": "gemini-3.1-flash-image",
  "aspectRatio": "1:1",
  "imageSize": "1K"
}
```

All fields are optional except the key. `config.example.json` is included for
reference. Keep this file out of version control (`chmod 600` is a good idea).

## Usage

Just ask:

> Generate an image of a corgi puppy in a sunny meadow, 16:9

Or use the command:

```
/imagine a corgi puppy in a sunny meadow
```

Or, explicitly:

> Use `generate_image` with `model: gemini-3-pro-image`, `image_size: 4K` to
> make a poster of a corgi.

### Tool arguments

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `prompt` | string | — | Image description (required) |
| `model` | string | config default | Per-call model override |
| `aspect_ratio` | string | `1:1` | `1:1 2:3 3:2 3:4 4:3 4:5 5:4 9:16 16:9 21:9` |
| `image_size` | string | `1K` | `1K` / `2K` / `4K` (2K/4K on Gemini 3 models) |
| `output_path` | string | plugin images dir | Directory to save into |
| `file_name` | string | timestamp+slug | Filename without extension |

## Models

| Value | Model | ~\$ per 1K image | Notes |
| --- | --- | --- | --- |
| `gemini-3.1-flash-image` | Nano Banana 2 | \$0.067 | **default**, balanced |
| `gemini-3.1-flash-lite-image` | Nano Banana 2 Lite | \$0.0336 | cheapest, fastest |
| `gemini-3-pro-image` | Nano Banana Pro | \$0.134 | best quality, 4K |
| `gemini-2.5-flash-image` | Nano Banana | ~\$0.0336 | legacy |

Set the default in `config.json`, or override per call with the `model`
argument. An explicit per-call model is used **exactly** as given — if it isn't
available you get an error rather than a silent downgrade. The configured
default, in contrast, falls back through
`gemini-3.1-flash-image → gemini-2.5-flash-image → gemini-3-pro-image` on a 404.

## Output

Default directory: `~/.config/opencode/plugin-data/gemini-imagegen/images/`.
Override per call with `output_path` / `file_name`.

## Logs

`~/.local/state/opencode/gemini-imagegen.log`

## Notes

- Image generation is billed by Google per image; see
  [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing).
- This plugin calls the public Gemini `generativelanguage` API with your key. It
  is not affiliated with Google.

## License

MIT — see [LICENSE](LICENSE).
