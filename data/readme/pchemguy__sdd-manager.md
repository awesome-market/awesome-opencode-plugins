# SDD Manager

SDD Manager composes focused skills into specification-driven development workflows for Git projects, from project exploration and design through bounded implementation, verification and releases.

## Quick Start

Before project work, review the [execution prerequisites](.agents/plugins/sdd-manager/README.md#execution-prerequisites).

Choose the minimal Hello World app, the Tetris game, the calculator, or a template for your own project.

1. Create an initialized GitHub repository from [SDD Manager Template](https://github.com/pchemguy/SDD-Manager-Template).
2. [Create a fine-grained personal access token (PAT)](https://github.com/settings/personal-access-tokens/) restricted to the new repository. A suggested standard set grants **Read and write** permissions for:
    - Actions.
    - Commit statuses.
    - Contents.
    - Issues.
    - Pull requests.
    - Workflows.

    Individual workflows may require fewer permissions; this set is a convenience rather than a universal minimum.

3. Choose a prompt below. Replace `https://github.com/{OWNER}/{REPO}` and `{FINE_GRAINED_GH_TOKEN}` with your repository URL and token, then submit it in a new ChatGPT Work conversation or another agentic environment with SDD Manager available.

### Hello World demo prompts

Both Autodoc prompts display "Hello World" with red/blue/green radio controls. Deliver the browser app, Windows Electron app and Chromium/Firefox extensions in that order; the two extensions form one delivery phase.

| Prompt | Layout scope |
| --- | --- |
| [Autodoc 3in1](<docs/demo/hello_world/prompts/Autodoc 3in1.md>) | Browser/Electron panels; extension sidebar controls the message on the active webpage. |
| [Autodoc 3in1 Baseline](<docs/demo/hello_world/prompts/Autodoc 3in1 Baseline.md>) | Simpler shared UI, adapted to fit inside the extension sidebar. |

### Tetris demo prompts

Choose documentation preparation, how to submit the scope, and delivery forms separately. Featured prompts start with Greenfield; submit each later feature section when ready to develop it.

| Prompt | Preparation | Scope submission | Delivery |
| --- | --- | --- | --- |
| [Interactive](docs/demo/tetris/prompts/Interactive.md) | Interactive | One complete prompt | Browser, then Electron |
| [Autodoc](docs/demo/tetris/prompts/Autodoc.md) | Autodoc | One complete prompt | Browser, then Electron |
| [Single Page Autodoc](<docs/demo/tetris/prompts/Single Page Autodoc.md>) | Autodoc | One complete prompt | One HTML file |
| [Autodoc 3in1](<docs/demo/tetris/prompts/Autodoc 3in1.md>) | Autodoc | One complete prompt | Browser, Electron, extensions |
| [Multipass Autoloop](<docs/demo/tetris/prompts/Multipass Autoloop.md>) | Autodoc/autoloop | One prompt; ten cumulative scope passes | Browser, then Electron |
| [Featured Autodoc](<docs/demo/tetris/prompts/Featured Autodoc.md>) | Autodoc | Greenfield, then feature sections | Browser, then Electron |
| [Single Page Featured Autodoc](<docs/demo/tetris/prompts/Single Page Featured Autodoc.md>) | Autodoc | Greenfield, then feature sections | One HTML file |
| [Featured Autodoc 3in1](<docs/demo/tetris/prompts/Featured Autodoc 3in1.md>) | Autodoc | Greenfield, then feature sections | Browser, Electron, extensions |

Electron delivery targets Windows and follows browser UI layout. Extension delivery includes Chromium and Firefox together. Single-page variants embed application HTML/CSS/JavaScript and permit widely used CDN JavaScript libraries.

Browser-only staged exercises: [minimal starting description](docs/demo/tetris/README.md#minimal-starting-prompt), [baseline and enhancements as one project](docs/demo/tetris/README.md#variant-a-classical-baseline--modern-extensions), [baseline followed by features](docs/demo/tetris/README.md#variant-b-classical-baseline--feature-expansion), [further feature campaigns](docs/demo/tetris/README.md#further-feature-campaigns), [steering exercises](docs/demo/tetris/README.md#steering-exercises). [The Tetris guide](docs/demo/tetris/README.md) provides gameplay scope and verification context.

### Calculator demo prompts

Choose the complete target scope upfront or build the calculator through separately submitted project and feature requests.

| Prompt collection | How to use it |
| --- | --- |
| [All-inclusive project prompt](docs/demo/calculator/README.md#all-inclusive-project-prompt) | Submit the complete prompt for arithmetic, scientific/programmer operations, graphing and mode selection. |
| [Staged initial project](docs/demo/calculator/README.md#initial-project-calculator) | Combine its project description with the project template below; deliver basic arithmetic, powers/logarithms and trigonometry in three phases. |
| [Optional steering exercises](docs/demo/calculator/README.md#optional-steering-exercises) | Choose either unary-operation amendment at a paused implementation checkpoint. |
| [Feature campaign sequence](docs/demo/calculator/README.md#feature-campaign-sequence) | Submit basic/scientific mode, programmer operations, graphing and four-mode selection as separate feature requests. |

[The calculator guide](docs/demo/calculator/README.md) includes the prompt text, verification and release guidance.

### Your own project

Use the [Greenfield Project Prompt Template](<.agents/plugins/sdd-manager/assets/Greenfield Project Prompt Template.md>) with a short preliminary project description. Supply the target repository, required authorization and GitHub tracking preference. The agent should clarify material ambiguities before treating them as requirements.

### After document preparation

Interactive preparation keeps each necessary document checkpoint active unless preapproved. Autodoc proceeds after brief approval and stops after TASKS, before final documentation-package QC. Autoloop runs the predefined scope passes after the first brief approval, then reaches the same stop.

At that stop, request "Run final documentation-package QC and stop before implementation." To also select implementation, request a bounded range, for example: "Run final documentation-package QC, then implement phase 1 and stop." Document acceptance, verification and integration gates still apply; QC alone does not authorize implementation. See [modes and checkpoints](.agents/plugins/sdd-manager/README.md#doc-design-modes).

## Documentation and development

The plugin source package is in [`.agents/plugins/sdd-manager/`](.agents/plugins/sdd-manager/README.md). It is intended to be available for agents to load from this checkout when working on SDD Manager itself. A separate agent installation remains an option; this layout does not configure automatic loading. Instruction reload is controlled by the user.

See the **[full README](.agents/plugins/sdd-manager/README.md)** for capabilities, workflow diagrams, human checkpoints, reporting profiles, usage examples and packaging information.

Development uses [SDD Manager](SDD-MANAGER.md). See the [AI-assisted development disclosure](AI_DISCLOSURE.md) and [MIT license](LICENSE).
