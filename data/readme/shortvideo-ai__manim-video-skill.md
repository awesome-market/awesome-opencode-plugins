# Manim Video Skill

[中文](README.zh-CN.md)

Skill for generating and rendering Manim math, educational, and explainer videos.

## Features

- Guides agents to write Manim Community Edition scene code.
- Bundles local Manim reference docs for offline API lookup.
- Renders through `scripts/run_manim_script.py` so temporary Manim output stays isolated in a caller-provided job directory.
- Returns structured JSON with render status, log paths, and the final video path.

## Install

Clone or copy this repository into a compatible skills directory, then invoke it as `$manim-video`.

For Codex, that usually means:

```powershell
git clone https://github.com/ShortVideo-AI/manim-video-skill.git ~/.codex/skills/manim-video-skill
```

For opencode, OpenClaw, or another compatible agent runtime, place the folder in that runtime's skills directory.

## Requirements

- Python
- Manim Community Edition

By default, the render helper invokes:

```powershell
python -m manim
```

If your default `python` environment does not have Manim installed, pass a specific Manim executable with `--manim-command`.

## Example

See `examples/smoke-test/` for a minimal scene, a sample rendered video, and the command used to verify the helper.

![Smoke test preview](examples/smoke-test/GeneratedScene.gif)

[Open the MP4 sample](examples/smoke-test/GeneratedScene.mp4)

## Third-Party Content

This repository bundles a generated markdown copy of the Manim Community reference manual under `docs/` for local API lookup. See `NOTICE` for source and license attribution.
