# opencode-video-gateway

An OpenCode plugin that turns a first-line video directive into real prompt attachments.

It supports two flows:

- `/video <local-path-or-url>`: attach the whole video as a `video/*` prompt part for models that accept direct video input.
- `/video-frames <local-path-or-url>`: use `ffmpeg` to sample frames and attach them as images for models that do not accept full video.

## Why this exists

OpenCode's provider layer already understands `video/*` input, but the built-in `read` tool only auto-attaches images and PDFs. This plugin fills that gap without forking OpenCode core.

## Install

Add it to your OpenCode config:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    [
      "opencode-video-gateway",
      {
        "direct_max_bytes": 41943040,
        "frames": 6
      }
    ]
  ]
}
```

## Usage

Whole video:

```text
/video ./demo.mp4
Describe what happens in this clip.
```

Frame fallback:

```text
/video-frames https://example.com/demo.mp4
Summarize the key scenes.
```

## Notes

- `ffmpeg` and `ffprobe` must be available in the environment for `/video-frames`.
- `/video` downloads remote URLs before attaching them.
- Large direct video attachments can exceed provider limits; use `/video-frames` when that happens.
