# image-optimizer

An OpenCode V2 plugin that downscales and recompresses images right before they are sent to the model.

It covers prompt attachments and images returned by any tool (`read`, MCP screenshot tools, and so on), for agent
turns, compaction, and `generate` requests. Only the outgoing request changes; session history keeps the original.

## Why

OpenCode already caps images at 2000px and 5 MiB of Base64 (`media.image`). Anthropic downscales anything over a
1568px long edge on its side, so the extra pixels only add tokens and latency. This plugin applies a tighter,
provider-aware limit:

1. Within `maxEdge` and `maxBase64Bytes`: sent unchanged.
2. Longer edge over `maxEdge`: resized to fit, aspect ratio kept, never enlarged.
3. Still over the size budget: re-encoded as JPEG at quality 90, 80, 70, then 60, and shrunk further if needed.
4. Oversized animated GIFs are flattened to their first frame, the only frame providers read.

When `annotate` is on, a note follows each changed image with its old and new size and the factor that maps
coordinates back to the image OpenCode provided. That matters when the model clicks on screenshots.

Results are cached by content, so the same image is processed once and produces identical bytes every turn, which keeps
provider prompt caching working.

## Install

```sh
opencode plugin add github:hiddentn/opencode-image-optimizer
```

This adds the plugin to your global configuration. OpenCode installs it with its dependencies, including `sharp`,
and checks for updates when it starts. Pin a release by adding a tag or commit, for example
`github:hiddentn/opencode-image-optimizer#v0.1.0`.

If `sharp` cannot load, the plugin logs a warning and passes images through unchanged.

## Options

Use the object form in `opencode.jsonc` to change the defaults:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "github:hiddentn/opencode-image-optimizer",
      "options": {
        "maxEdge": 1568,
        "maxBase64Bytes": 5242880,
        "annotate": true,
        "providers": { "anthropic": true, "google": true, "openai": false },
        "default": true,
      },
    },
  ],
}
```

| Option           | Default   | Meaning                                                      |
| ---------------- | --------- | ------------------------------------------------------------ |
| `maxEdge`        | `1568`    | Longest edge allowed, in pixels                              |
| `maxBase64Bytes` | `5242880` | Budget for the Base64-encoded image                          |
| `annotate`       | `true`    | Add a text note next to each changed image                   |
| `providers`      | `{}`      | Per-provider on/off switches, keyed by provider ID           |
| `default`        | `true`    | Used when nothing else decides                               |

Whether a request is optimized is decided in this order:

1. An explicit `providers` entry for the request's provider ID.
2. The model ID: `claude` and `gemini` models are on, `gpt-*` and `o*` models are off. This catches models served
   through gateways such as `opencode/claude-haiku-4-5`.
3. Built-in provider defaults: `anthropic`, `google`, and `google-vertex` on; `openai` off.
4. `default`.

## Development

```sh
git clone https://github.com/hiddentn/opencode-image-optimizer
cd opencode-image-optimizer
npm install
npm run typecheck
npm test
```

To try local changes, point a project's `plugins` entry at the clone's absolute path. If the same copy is also
auto-discovered from a `plugins/` folder, the copy configured with options takes over.

## License

MIT
