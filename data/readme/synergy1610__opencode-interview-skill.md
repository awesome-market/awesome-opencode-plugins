# opencode-interview-skill

An [OpenCode](https://opencode.ai) skill that interviews you about the project
you want to build. It keeps asking questions until it has the full picture,
saves the answers to a spec file, and then builds the project from that file.

## Why?

Most back and forth between you and the agent happens because the first prompt
was vague. This skill makes the agent ask first, so it understands what you
want from the start.

## Installation

Copy the `interview` folder (the one containing `SKILL.md`) into your global
OpenCode skills directory:

- **Linux / macOS:** `~/.config/opencode/skills/`
- **Windows:** `%USERPROFILE%\.config\opencode\skills\`

To install it for a single project instead, copy it to
`.opencode/skills/` inside that project.

Restart OpenCode afterwards.

## Usage

- Type `/skills` and pick **interview** from the list, or
- Type '@interview' followed by your prompt.

The agent will ask you questions one at a time. When it has enough detail, it
saves everything to `docs/PROJECT_SPEC.md` and uses it to build the project.


## License

MIT
