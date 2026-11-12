# multitool

![multitool — fast workflows for Codex and OpenCode](docs/gallery/banner.svg)

Registers five OpenCode commands and distributes their matching Codex skills.
The source instructions remain in the Markdown files in this repository.

## Codex

### Install

Add the repository as a plugin marketplace, then install `multitool`:

```sh
codex plugin marketplace add alexeyco/multitool
codex plugin add multitool@multitool
```

Codex installs the packaged skills from the marketplace. Start a new Codex session to use them.

### Commands

- [`$multitool:branch`](codex/skills/branch/SKILL.md) — create an approved branch for the current task.
- [`$multitool:commit`](codex/skills/commit/SKILL.md) — review changes, run defined checks, and create confirmed commits.
- [`$multitool:pr`](codex/skills/pr/SKILL.md) — prepare and create a pull or merge request after confirmation.
- [`$multitool:tag`](codex/skills/tag/SKILL.md) — create and push a tag after approval.
- [`$multitool:bump`](codex/skills/bump/SKILL.md) — review a release baseline and prepare an approved version bump.

## OpenCode

### Install

Add the npm package to the `plugin` array in OpenCode's `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["@alexeyco/multitool"]
}
```

OpenCode installs the npm plugin and registers its commands and skills at startup.

### Commands

Commands use the `/multitool.<action>` format:

- [`/multitool.branch`](opencode/commands/multitool.branch.md)
- [`/multitool.commit`](opencode/commands/multitool.commit.md)
- [`/multitool.pr`](opencode/commands/multitool.pr.md)
- [`/multitool.tag`](opencode/commands/multitool.tag.md)
- [`/multitool.bump`](opencode/commands/multitool.bump.md)

See [AGENTS.md](AGENTS.md) for the repository map and guidance for contributors and agents.

## Automation

CI runs on pull requests and pushes to `master`. npm publishing runs on `v*`
version tags after checking that the tag matches `package.json` and its commit
is on `master`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for the full license text.
