# opencode-teams

[![npm version](https://img.shields.io/npm/v/opencode-teams.svg)](https://www.npmjs.com/package/opencode-teams)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> The policy, config, and UX layer for OpenCode Agent Teams

A CLI tool and library that brings intelligent task routing to [OpenCode](https://github.com/opencode/opencode). Automatically route tasks to the right agent based on complexity, security sensitivity, and task type—saving costs while maintaining quality.

## Features

- **Smart Task Routing** - Automatically routes tasks to the most appropriate agent based on signals like complexity, security sensitivity, and task type
- **Multiple Agents** - 7 specialized agents: teams (orchestrator), explorer, reviewer, impl-cheap, impl-fast, impl-deep, and quick
- **Cost Optimization** - Use cheaper models for simple tasks, reserve expensive models for complex work
- **Presets** - Three built-in presets: balanced, cost-optimized, and quality-first
- **Flexible Configuration** - Global defaults + per-project overrides with JSONC support
- **Pattern Matching** - Custom routing rules using regex patterns

## Installation

```bash
npm install -g opencode-teams
# or
bun add -g opencode-teams
```

## Quick Start

### 1. Initialize Configuration

```bash
# Interactive setup
opencode-teams init

# Or use a preset directly
opencode-teams init --preset balanced --yes

# Force overwrite existing config
opencode-teams init --preset cost-optimized --force --yes
```

### 2. Install Agents

The init command automatically installs agent files to `~/.config/opencode/agents/`. These are markdown files that define each agent's behavior and capabilities.

### 3. Validate Setup

```bash
opencode-teams doctor
```

This checks that your configuration is valid and all required agents are installed.

### 4. Test Routing

```bash
# See which agent would handle a task
opencode-teams explain "Add authentication to the API"

# Show detailed signals
opencode-teams explain "Fix typo in README" --signals
```

## Agents

| Agent | Capability | Default Model | Use Case |
|-------|------------|---------------|----------|
| `@teams` | lead | claude-sonnet-4 | Orchestrator, delegates to other agents |
| `@explorer` | explore | claude-haiku-4 | Read-only codebase exploration |
| `@reviewer` | review | claude-sonnet-4 | Code review and analysis |
| `@impl-cheap` | cheap | claude-haiku-4 | Simple implementations, tests |
| `@impl-fast` | fast | claude-sonnet-4 | Standard implementations |
| `@impl-deep` | deep | claude-opus-4 | Complex/security-sensitive work |
| `@quick` | quick | claude-haiku-4 | Trivial changes (typos, renames) |

## Configuration

Configuration uses JSONC (JSON with comments) and is loaded from two locations:

1. **Global**: `~/.config/opencode/teams.jsonc` - User defaults
2. **Local**: `./opencode-teams.jsonc` - Project overrides

Local config is merged on top of global config.

### Example Configuration

```jsonc
{
  // Use auto-routing based on task analysis
  "routing": {
    "mode": "auto",
    "fallbackAgent": "impl-fast",
    "patterns": [
      // Custom patterns (evaluated first)
      { "match": "migration|database", "capability": "deep", "agent": "impl-deep", "reason": "DB work needs care" }
    ]
  },
  
  // Model assignments per capability
  "capabilities": {
    "fast": {
      "primary": "anthropic/claude-sonnet-4-20250514",
      "fallback": ["openai/gpt-4o"]
    },
    "cheap": {
      "primary": "anthropic/claude-haiku-4-20250514",
      "fallback": []
    },
    "deep": {
      "primary": "anthropic/claude-opus-4-20250514",
      "fallback": ["openai/o3"]
    }
  },
  
  // Execution settings
  "execution": {
    "backend": "compat",
    "parallelAgents": 1
  },
  
  // Failover behavior
  "failover": {
    "maxRetries": 2,
    "retryDelay": 1000
  },
  
  // Logging for cost analysis
  "logging": {
    "enabled": true,
    "logDir": ".opencode-teams/logs"
  }
}
```

### Presets

Use `--preset` with the init command:

| Preset | Description |
|--------|-------------|
| `balanced` | Default. Sonnet for most work, Haiku for cheap tasks, Opus for complex work |
| `cost-optimized` | Haiku everywhere possible, Sonnet only for deep work |
| `quality-first` | Opus for everything, o3 for deep thinking |

## Routing Logic

The router analyzes task descriptions to extract signals:

- **Task Type**: explore, implement, test, review, fix, refactor
- **Complexity**: Architecture, algorithms, concurrency, etc.
- **Security**: Auth, tokens, encryption, XSS/CSRF, etc.
- **Trivial**: Typos, formatting, renames, etc.
- **Test Related**: Test keywords or test file patterns

### Routing Priority

1. **Pattern Match** - Custom patterns in config (highest priority)
2. **Security** - Security-sensitive → impl-deep
3. **Complexity** - Complex/architectural → impl-deep
4. **Exploration** - Find/explore tasks → explorer
5. **Review** - Review/audit tasks → reviewer
6. **Tests** - Test tasks → impl-cheap
7. **Trivial** - Typos, renames → quick
8. **Default** - Standard work → impl-fast

## CLI Commands

```bash
# Initialize configuration
opencode-teams init [options]
  --preset <name>    Use a preset (balanced, cost-optimized, quality-first)
  --local            Create local config only (no global)
  --force            Overwrite existing files
  -y, --yes          Skip confirmation prompts

# Validate configuration
opencode-teams doctor

# Explain routing for a task
opencode-teams explain <task> [options]
  --signals          Show detailed signal analysis
  --json             Output as JSON

# Print agent content (for debugging)
opencode-teams print-agent <name>
```

## Programmatic Usage

```typescript
import { createPlan, loadConfig, extractSignals } from 'opencode-teams'

// Load merged config
const config = await loadConfig()

// Create execution plan
const plan = createPlan('Add authentication to the API', config)

console.log(plan.steps[0].agent)      // 'impl-deep'
console.log(plan.steps[0].capability) // 'deep'
console.log(plan.steps[0].rationale)  // 'Security-sensitive task'

// Just extract signals
const signals = extractSignals('Fix typo in README')
console.log(signals.isTrivial)        // true
```

## How It Works

1. **Signal Extraction** - Analyzes task description for keywords, patterns, and context
2. **Pattern Matching** - Checks custom routing patterns from config
3. **Heuristic Routing** - Falls back to built-in rules based on signals
4. **Model Resolution** - Maps agent capability to configured model
5. **Plan Generation** - Creates execution plan with rationale and risks

## Integration with OpenCode

This package is designed to work with OpenCode's emerging Agent Teams feature. It provides:

- **Policy Layer** - Define which models/agents handle which tasks
- **Config Layer** - Centralized configuration with presets
- **UX Layer** - CLI tools for setup and debugging

Once OpenCode's native Teams API is available, this package will integrate directly.

## Development

```bash
# Install dependencies
bun install

# Build
bun run build

# Run tests
bun run test

# Run tests once
bun run test:run

# Type check
bun run lint
```

## License

MIT
