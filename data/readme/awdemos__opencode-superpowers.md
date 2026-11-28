# OpenCode Superpowers

This repository installs and configures the [Superpowers](https://github.com/awdemos/opencode-superpowers) workflow for [OpenCode](https://opencode.ai).

Superpowers is a workflow system for AI coding assistants that enforces best practices like:

- Test-Driven Development (TDD)
- Systematic debugging
- Structured planning
- Subagent-driven development

## Quick Start (recommended)

Add this repository as a plugin in your `opencode.json`:

```json
{
  "plugin": ["superpowers@git+https://github.com/awdemos/opencode-superpowers.git"]
}
```

Restart OpenCode. The plugin registers the Superpowers skills and injects a lean per-session bootstrap.

Verify by asking: **"Tell me about your superpowers."**

See `SKILL.md` for project-level templates.

## What's in this repository

| Path | Purpose |
|------|---------|
| `SKILL.md` | **Start here.** Installation skill for OpenCode and project-level workflow templates. |
| `prompts/AGENTS.md.template` | Project-level `AGENTS.md` template. Copy to your project root and customize. |
| `prompts/superpowers-reminder.md` | Inline reminder variant for clients that support system reminders. |
| `templates/PROJECT_CONFIG.yaml` | **Copy this** to your project root as `PROJECT_CONFIG.yaml`. |
| `scripts/validate-links.sh` | Repository health check: internal markdown links. |
| `skills/` | Vendored Superpowers skills (used when this repository is cloned as the install source). |

## Compatibility

- **OpenCode**: Any modern version with the `skill` tool and plugin support.
- **Windows / macOS / Linux**: Works on all platforms OpenCode supports.

## License

MIT (same as Superpowers)
