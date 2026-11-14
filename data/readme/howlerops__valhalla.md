# HowlerOps Valhalla

HowlerOps Valhalla ships the same seven agent workflows for [OpenCode](https://opencode.ai) and the [Pi coding-agent harness](https://pi.dev), plus the Vegvisir planning skill in both runtimes. Bifrost and Heimdall are no longer included.

## Agents

| Command | Role |
| --- | --- |
| `/hugin <goal>` | Build a verified, dependency-aware plan without editing. |
| `/tyr <goal>` | Implement one goal with architecture, verification, and review. |
| `/munin <objective>` | Run a measured research and improvement loop. |
| `/eitri <request>` | Create narrow, harness-native agents, workflows, skills, or tools. |
| `/vidar <goal>` | Persist through implementation and review loops. |
| `/skuld <target>` | Review and repair a diff or pull request. |
| `/polaris <task>` | Orchestrate planning through final review. |

## Vegvisir

`/vegvisir <destination>` in OpenCode (or `/skill:vegvisir <destination>` in Pi) maps a genuinely multi-session, uncertain effort into decision tickets. It establishes a destination, fog of war, frontier, dependencies, and evidence-backed resolutions, then hands off to specification work. It never implements the destination.

Vegvisir is an original Pi adaptation of the operating model described at [AI Hero: Wayfinder](https://www.aihero.dev/skills-wayfinder). Use it only when the route cannot be settled in one session.

## Install Pi

```bash
pi install git:github.com/howlerops/valhalla
```

For a local checkout:

```bash
pi install /absolute/path/to/valhalla
```

Verify the package and run a small command:

```bash
pi list
pi -p "/hugin Plan a small refactor"
```

Pi loads the package's prompt templates and Vegvisir skill. Trust project-local packages only after reviewing their contents.

## Install Prime Agent

[Prime Agent](https://github.com/PrimeIntellect-ai/prime-agent) is a fork of pi-mono that reads the same `pi` package key, so the same package works there:

```bash
prime-agent package install git:github.com/howlerops/valhalla
prime-agent package list
prime-agent -p "/hugin Plan a small refactor"
```

All seven agents and `/skill:vegvisir` were verified against Prime Agent 0.9.4. Note the config directory is `PRIME_AGENT_CODING_AGENT_DIR` and there is no `--approve` flag.

Full installation and troubleshooting guide: [`docs/guide/installation.md`](docs/guide/installation.md).

## Install OpenCode

```bash
npm install --prefix "$HOME/.config/opencode" github:howlerops/valhalla
node "$HOME/.config/opencode/node_modules/@howlerops/valhalla/scripts/install-opencode.mjs"
```

The installer registers the plugin, writes `/hugin`, `/tyr`, `/munin`, `/eitri`, `/vidar`, `/skuld`, `/polaris`, and `/vegvisir` as native OpenCode commands, and installs the Vegvisir skill for OpenCode. Restart OpenCode after installation.

## Test

```bash
npm ci
npm test
npm pack --dry-run
```

The test suite verifies all eight OpenCode commands and runs every Pi agent plus Vegvisir through the real Pi CLI against a local fake OpenAI-compatible provider.
