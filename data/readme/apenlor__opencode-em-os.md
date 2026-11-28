# OpenCode Engineer Manager OS
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9c806630f03343ffa763f91b7673157d)](https://app.codacy.com/gh/apenlor/opencode-em-os/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Latest Tag](https://img.shields.io/github/v/tag/apenlor/opencode-em-os)](https://github.com/apenlor/opencode-em-os/releases/latest)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

An Engineering Manager Operating System (EM-OS) built natively for [OpenCode](https://opencode.ai).

## What This Does

Transforms OpenCode into a context-aware Engineering Manager assistant. It encodes proven management frameworks into automated workflows for initiative planning, 1:1 lifecycle management, strategy development, and product delivery.

For deep dives into concepts like strategy kernels, vision frameworks, and the OS architecture, see the [Full Guide](./GUIDE.md).

## Quick Start

1.  **Create your workspace**: Use this repository as a template.
    ```bash
    gh repo create my-em-workspace --template apenlor/opencode-em-os --private --clone
    cd my-em-workspace
    ```

2.  **Environment**: Copy `.env.example` to `.env.local` and add your Jira credentials. Authenticate with `gh auth login`.

3.  **Jira CLI**: Install and initialize the Jira CLI (one-time step).
    ```bash
    brew install ankitpokhrel/jira-cli/jira-cli
    ```
    Then run `jira init` once inside the session after starting OpenCode (see step 5).

4.  **Team Data**: Create your team folder and roster.
    ```bash
    mkdir -p data/teams/my-team/one-on-ones
    cp data/teams/example/team.md data/teams/my-team/team.md
    ```

5.  **Start OpenCode**:
    ```bash
    ./opencode-em.sh
    ```
    The runner loads `.env.local` automatically. On first use, run `/connect` to set up your AI provider, then `jira init` once to initialize the Jira CLI in isolated mode.

    > **Without the wrapper**: If you run `opencode` directly, export credentials manually before any Jira operation:
    > ```bash
    > set -a; source .env.local; set +a
    > opencode
    > ```

## Workspace Structure

```text
opencode-em-os/
├── data/                           # Shared memory (Teams, Products, Strategies)
│   ├── teams/                      # Roster + 1:1 history
│   │   └── {team}/
│   │       ├── team.md
│   │       └── one-on-ones/
│   ├── products/                   # Tech context + Architecture
│   ├── strategies/                 # Strategy documents
│   └── visions/                    # Vision documents
├── initiatives/                    # Active efforts (one folder per project)
│   └── [slug]/
│       ├── data/                   # Input (PRDs, specs, notes)
│       ├── output/                 # Generated artifacts (plans, epics, stories)
│       ├── scripts/                # Ad-hoc scripts
│       └── tmp/                    # Scratchpad
├── .opencode/                      # Skills, commands, and EM persona
└── .env.local                      # Local secrets (git-ignored)
```

## Available Tools

### Strategy & Planning
| Skill | Trigger Examples |
|-------|-----------------|
| `plan-initiative` | "plan an initiative", "help me structure this" |
| `write-strategy` | "write a strategy" |
| `write-vision` | "write a vision" |
| `tidy-initiative` | "tidy initiative", "clean up output", "organize initiative" |

### Product & Delivery Authoring
| Skill | Trigger Examples |
|-------|-----------------|
| `us-mapping` | "user story map", "story mapping" |
| `write-epic-build` | "write an epic", "implementation plan" |
| `write-epic-technical-discovery` | "technical discovery", "discovery epic" |
| `decompose-epic` | "decompose this epic", "break down epic" |
| `write-us` | "write a user story", "write a US" |

### People & Leadership
| Skill / Command | Trigger Examples |
|-------|-----------------|
| `prepare-one-on-one` | "prepare my 1:1 with", "1:1 prep" |
| `log-one-on-one` | "log my 1:1 with", "record 1:1" |
| `mentor-me` | "mentor me with", "help me think" |
| `/ic-activity` | "/ic-activity John last month" |

### Integrations
| Skill | Trigger Examples |
|-------|-----------------|
| `jira` | "create in Jira", "show me bugs", "issues completed" |

## Isolation & Security

This workspace is designed to run in **Isolated Mode** via `./opencode-em.sh`. This prevents global OpenCode configurations from bleeding into your management workspace, ensuring your data and persona remain private and consistent.

See [GUIDE.md](./GUIDE.md) for detailed Data Access Rules and security considerations.

## License

See [LICENSE](./LICENSE).
