# opencode-vision

Video tools for [OpenCode](https://opencode.ai) v2. OpenCode does not pass video attachments to models, so this plugin adds three tools: record the screen, turn a video into labelled contact sheets any image-capable model can read, or send a short clip to a native video model.

Tested with OpenCode 2.0.30 (`@opencode/plugin` 2.0.30). Requires `ffmpeg` and `ffprobe` on `PATH`.

## Features

- `video_frames`: extract evenly spaced frames, or frames at exact timestamps, into contact-sheet PNGs. Every frame is stamped with its timestamp (`mm:ss.s`). Up to 48 frames, 16 per sheet, sheets kept within 2000 px and the image size limits. Works with any model that can read images, no subscription needed.
- `watch_video`: trim and downscale a clip (H.264, no audio, at most 300 s per call, under 20 MiB) and ask a native video model a question; returns the answer plus duration and token usage.
- `record_screen`: record a monitor or a single window to MP4 using Windows Desktop Duplication (`ddagrab`), which also captures fullscreen and GPU-rendered content such as emulators. Hardware encoders (NVENC, QSV, AMF) are tried first with a fallback to `libx264`, and `gdigrab` is used if `ddagrab` fails.
- A bundled skill (`video-analysis`) that teaches the model which tool to use when.

## Install

```sh
opencode plugin add github:KelpHect/opencode-vision
```

Pin a release with `github:KelpHect/opencode-vision#v0.2.1`. Manual configuration:

```jsonc
{
  "plugins": [
    { "package": "github:KelpHect/opencode-vision#v0.2.1", "options": { "captureDir": "/path/to/captures" } }
  ]
}
```

Restart the service afterwards (`opencode service restart`).

## Configuration

| Option | Default | Description |
| --- | --- | --- |
| `captureDir` | `~/.opencode-vision/captures` | Where recordings and frame sheets are written. |
| `model` | `step-5-preview` | Model used by `watch_video`. |
| `endpoint` | OpenCode Go OpenAI-compatible chat completions endpoint | Chat completions URL used by `watch_video`. |

Subagents need permission to call the tools. If an agent denies unknown actions by default, allow them explicitly:

```jsonc
{ "action": "video_frames", "resource": "*", "effect": "allow" }
```

The permission action names are `video_frames`, `watch_video` and `record_screen`.

## Tools

### `video_frames`

| Argument | Description |
| --- | --- |
| `path` | Video file. |
| `start`, `end` | Optional range in seconds. |
| `count` | Evenly spaced frames, default 12, max 48. |
| `at` | Exact timestamps in seconds; overrides `count`. |
| `columns` | Frames per row, default 4. |
| `frame_width` | Frame width in pixels, default 480 (reduced automatically to keep sheets within 2000 px). |

Returns the sheet paths and a table of sheet, frame, position and timestamp. Open each sheet with the `read` tool.

### `watch_video`

`{ path, question, start?, end? }`. Spans longer than 300 s are rejected with a hint to pass `start`/`end`. `watch_video` calls the OpenCode Go endpoint with the credential of the signed-in `opencode` integration, so it needs an OpenCode Go subscription. The model and endpoint are configurable (see above); the endpoint must accept `video_url` content parts in OpenAI chat completions format.

### `record_screen` (Windows only)

`{ seconds (1-300, default 10), window?, monitor?, fps? }`. With `window`, the first visible top-level window whose title contains the text (case-insensitive) is brought to the foreground and recorded, cropped to its bounds. If nothing matches, the error lists the visible window titles. On other platforms the tool returns a "not supported yet" error.

## The bundled skill

Plugins provide tools; they cannot tell the model when to use them. The `video-analysis` skill (`skills/video-analysis/SKILL.md`) is registered automatically. It tells the model to default to `video_frames` plus `read`, to use `watch_video` only when motion between frames matters, and how to ask good questions.

## Limitations and known issues

- `record_screen` is Windows-only for now (macOS and Linux capture are not implemented).
- Window lookup uses window titles as displayed, so titles are localized.
- Monitor selection assumes the DXGI output order matches the Windows device-name order; verified on a single-monitor setup only.
- The video model samples frames sparsely (roughly one frame every 0.75 s in testing) and may say it cannot see the end of a clip. For precise frame-level questions use `video_frames`.
- `watch_video` depends on an endpoint that accepts video input; it is tied to the OpenCode Go service by default.

## Development

```sh
bun install
bun test
bunx tsc --noEmit
```

## License

MIT, see `LICENSE`. Copyright (c) 2026 KelpHect.
