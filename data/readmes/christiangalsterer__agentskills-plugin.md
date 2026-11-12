# agentskills-plugin

A Claude Code compatible plugin that provides commands and skills to create and manage Agent Skills following the [agentskills.io](https://agentskills.io) specification.

## Commands

## Skills

### `agentskills-creator`

Creates a new Agent Skill following the [agentskills.io](https://agentskills.io) specification and best practices. If you haven't provided a name or purpose for the new skill, it asks for them before proceeding.

**How it works:**

1. Gathers the skill name and purpose (asks if missing).
2. Validates the name against the spec (lowercase, hyphens, matches the directory name).
3. Drafts a trigger-optimized `description` and confirms it with you.
4. Scaffolds `SKILL.md` (plus `scripts/`/`references/`/`assets/` only when needed), proposing the author metadata from existing skills for your confirmation (you can provide your own name) and starting at version `1.0.0`.
5. Writes the body following progressive-disclosure and instruction-design best practices.
6. Verifies the result by linting with [skillscheck](https://github.com/swival/skillscheck) when available (via `uvx`), validating with `skills-ref` when available, plus a manual spec checklist.

The full field-by-field specification, script design rules, and eval workflows ship in `references/specification.md`, loaded on demand.

### `agentskills-doctor`

Validates an existing Agent Skill against the [agentskills.io](https://agentskills.io) specification and best practices, reports every finding with its check ID, and fixes findings on request. Read-only by default — it never modifies a skill unless you ask it to fix something.

**How it works:**

1. Takes the path to the skill to validate (asks if not provided).
2. Detects findings by running [skillscheck](https://github.com/swival/skillscheck) and `skills-ref` when available, plus a manual checklist.
3. Reports findings grouped by severity, each with check ID, file:line, the rule, and a suggested fix.
4. Fixes findings only when you ask — auto-applies safe mechanical fixes, confirms judgment calls (rewrites, removals) first.
5. Re-runs the linters to confirm the findings are gone.

Per-finding fix guidance ships in `references/fix-rules.md`; the full specification ships in `references/specification.md`. Both load on demand.

## Installation

This plugin is loaded automatically by Claude Code when placed in your project or global plugin directory. See the [Claude Code plugin documentation](https://docs.anthropic.com/en/docs/claude-code/plugins) for setup details.
