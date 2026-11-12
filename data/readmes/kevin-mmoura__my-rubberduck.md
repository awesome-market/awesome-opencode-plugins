# my-rubberduck

<p align="center">
  <img
    src="./assets/duck.png"
    alt="my-rubberduck — Think before you code"
    width="90%"
  />
</p>

<p align="center">
  <strong>English</strong> · <a href="README.pt-BR.md">Português (Brasil)</a>
</p>

<p align="center">
  <strong>Think before you code.</strong>
  <br>
  A programming rubber-duck skill for AI coding agents.
  <br><br>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License">
  </a>
  <a href="https://skills.sh/">
    <img src="https://img.shields.io/badge/skills.sh-published-38BDF8.svg" alt="Published on skills.sh">
  </a>
  <img src="https://img.shields.io/badge/Status-Active-10B981.svg" alt="Active">
</p>

---

## Overview

my-rubberduck is a duck, not an oracle. It does not write code for you, and it solves nothing on its own — which is exactly the point. Explain the problem out loud to a rubber duck and the duck stays silent; that silence forces you to think until you do.

This skill plays that same role for AI coding agents. It guides your reasoning through questions, hypotheses, and progressive hints. It reviews code by splitting actual defects from stylistic nitpicks. It explains concepts with trade-offs instead of verdicts. And it adapts to what you already know, so a beginner gets more hand-holding than someone who's shipped production systems.

AI guides, humans build, nobody outsources their thinking. A ready-made answer is never the default — hints come first, the full solution only when you ask for it or the moment calls for it.

## What it actually does

- Walks you through a programming problem with scope-defining questions before any implementation shows up.
- Debugs by investigating root causes through observation and hypotheses — no bug revealed, no fix handed over upfront.
- Explains concepts with examples and trade-off discussions, tuned to your demonstrated knowledge.
- Reviews code and separates real defects from stylistic preferences.
- Practices refactoring that preserves behavior while improving clarity, through incremental, test-verified changes.
- Generates exercises and challenges matched to what you already know.

## Interaction modes

Ask your AI coding agent for a specific mode:

| Mode | What it does |
|------|--------------|
| Default (mentoring) | Guides reasoning with questions, hypotheses, explanations, progressive hints. No complete solution unless you ask. |
| `--practice` | Coding exercises for a topic and language, with incomplete code and progressive hints. |
| `--challenge` | A problem statement and expected behavior, no starter code or implementation steps; your solution gets evaluated. |
| `--debug` | Buggy code to investigate or fix. Guides the hunt through observations and hints; explains root causes without coughing up the answer. |
| `--review` | Checks correctness, readability, maintainability, design. Defects and style preferences stay in separate buckets. |
| `--refactor` | Improves existing code without changing behavior, through small steps you verify yourself. |

The modes live in `skills/my-rubberduck/references/interaction-modes.md` alongside the skill's `SKILL.md`.

## Installation

my-rubberduck ships through the [skills.sh](https://skills.sh/) ecosystem and installs with the [skills CLI](https://www.skills.sh/docs/cli):

```bash
npx skills add kevin-mmoura/my-rubberduck --skill my-rubberduck
```

Project-level install keeps it to the current repo. Global install makes it available everywhere you work. Check the [CLI reference](https://www.skills.sh/docs/cli) for the flags.

## Quick Start

There's no CLI of your own to run. The skill is instructions consumed by a compatible AI coding agent after installation. Talk to your agent:

```text
"I want to build an authentication system in Python, but I don't know where to start."
→ default mentoring mode: questions that define scope before any code appears.

"My function returns None instead of a sum. Help me debug it."
→ --debug mode: you observe, you hypothesize, you find the bug yourself.

"Review this pull request and tell me what's wrong."
→ --review mode: real defects separated from style preferences.

"Give me a React exercise appropriate for a beginner."
→ --practice mode: incomplete code, TODOs, progressive hints.

"Improve this function without changing its behavior."
→ --refactor mode: improvement goals, incremental changes you verify.
```

Try something real. Pick a function you actually wrote and ask the agent to debug it in `--debug` mode. See if you can find the root cause before the hint shows up.

## Project Structure

```text
my-rubberduck/
├── LICENSE                    # MIT license text
├── README.md                  # This file (English)
├── README.pt-BR.md            # Brazilian Portuguese translation
├── CONTRIBUTING.md            # Contribution guidelines and PR process
└── skills/                    # Skill package
    └── my-rubberduck/         # Skill directory
        ├── SKILL.md           # Entry point: name, goal, instructions, workflow, examples
        └── references/        # Mandatory knowledge, loaded before any task
            ├── clean-code-guidelines.md
            ├── interaction-modes.md
            └── mentoring-methodology.md
```

`SKILL.md` carries the skill's name, description, goal, instructions, workflow, examples, and the rule that all three reference files must be read before any task. The `references/` folder holds the backing documentation.

## Contributing

This is a philosophy-driven mentoring skill. Touching `SKILL.md` or the references means keeping the rubber-duck spirit: guide reasoning, ask questions, explain trade-offs, never dish out complete solutions by default.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for local setup, commit conventions, and the pull-request process.

## License

MIT License. Full text in [`LICENSE`](./LICENSE).
