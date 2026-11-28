# Anvil for OpenCode

Evidence-first coding agent with adversarial multi-model review, SQL-tracked verification, and automatic rollback.

## Features

- **Adversarial Review** - 3 DeepSeek reviewers (strict/balanced/creative) attack your code
- **SQL Verification Ledger** - Every check INSERTed to SQLite, evidence is a SELECT not prose
- **Baseline Snapshots** - Capture state before changes, detect regressions automatically
- **Pushback** - Senior engineer evaluation, not an order taker
- **Session Memory** - Persists build commands, patterns, and past failures across sessions
- **Git Autopilot** - Checks dirty state, creates branches, auto-commits with rollback

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/opencode-anvil.git
cd opencode-anvil

# Run the install script
./install.sh
```

### Manual Install

1. Copy tools to OpenCode config:
```bash
cp tools/*.ts ~/.config/opencode/tools/
```

2. Copy plugin:
```bash
cp plugins/*.ts ~/.config/opencode/plugins/
```

3. Copy agents:
```bash
cp agents/*.md ~/.config/opencode/agents/
```

4. Copy skill:
```bash
mkdir -p ~/.agents/skills/anvil
cp skills/anvil/SKILL.md ~/.agents/skills/anvil/
```

5. Update your `~/.config/opencode/opencode.jsonc` with the agent configuration (see `opencode.jsonc` in this repo)

6. Restart OpenCode

## Usage

### 1. Switch to Anvil Agent

Press **Tab** to cycle through primary agents until you see "Anvil".

### 2. Make a Request

```
Fix the login crash when users enter special characters in the email field
```

### 3. Watch the Anvil Loop

Anvil will:
1. Evaluate if it's a good idea (pushback if not)
2. Size the task (Small/Medium/Large)
3. Check git state (dirty working tree? wrong branch?)
4. Recall past memories about these files
5. Survey codebase for existing solutions
6. Capture baseline (build/test/lint state)
7. Implement changes
8. Run verification cascade (IDE diagnostics, build, lint, tests)
9. Launch 1-3 DeepSeek adversarial reviewers
10. Present Evidence Bundle with confidence level
11. Auto-commit with rollback command

### 4. Review the Evidence Bundle

```
## 🔨 Anvil Evidence Bundle

**Task**: fix-login-crash | **Size**: M | **Risk**: 🟡

### Baseline (before changes)
| Check | Result | Command | Detail |
|-------|--------|---------|--------|
| build | ✓ | npm run build | exit 0 |
| test | ✓ | npm test | 47 passed |

### Verification (after changes)
| Check | Result | Command | Detail |
|-------|--------|---------|--------|
| build | ✓ | npm run build | exit 0 |
| test | ✓ | npm test | 48 passed |
| lint | ✓ | npm run lint | no errors |

### Adversarial Review
| Reviewer | Verdict | Findings |
|----------|---------|----------|
| strict | ✓ | No issues found |
| balanced | ✓ | No issues found |
| creative | ⚠ | Found edge case with empty string |

**Issues fixed before presenting**: Empty string validation added
**Confidence**: High
**Rollback**: `git checkout HEAD -- src/auth/login.ts`
```

## Tools

### anvil_ledger_insert
INSERT a verification check result into the SQL ledger.

### anvil_ledger_query
SELECT evidence bundle for a task.

### anvil_ledger_count
COUNT checks by phase (for gate enforcement).

### anvil_baseline_capture
Run build/test/lint commands and store baseline state.

### anvil_baseline_compare
Compare current state vs baseline, detect regressions.

### anvil_memory_store
Persist facts across sessions (build commands, patterns, failures).

### anvil_memory_recall
Query past memories by file/topic.

## Task Sizing

- **Small**: Typo, rename, config → Quick verify only (no ledger, no reviewers)
- **Medium**: Bug fix, feature, refactor → Full loop with 1 reviewer
- **Large**: New feature, multi-file, 🔴 files → Full loop with 3 reviewers

## Risk Classification

- 🟢 **Green**: Additive changes, tests, docs, config
- 🟡 **Yellow**: Modifying business logic, function signatures, DB queries
- 🔴 **Red**: Auth/crypto/payments, data deletion, schema migrations, concurrency, public API

## Confidence Levels

- **High**: All tiers passed, no regressions, reviewers found zero issues
- **Medium**: Most checks passed but some uncertainty
- **Low**: A check failed you couldn't fix, or reviewer raised an issue you can't disprove

## Requirements

- OpenCode (latest version)
- DeepSeek API key (run `/connect` in OpenCode and select DeepSeek)
- Bun runtime (for SQLite support)

## Database Location

All verification data is stored in:
```
~/.local/share/opencode/anvil.db
```

Tables:
- `anvil_checks` - Verification ledger
- `anvil_memory` - Session memory

## Uninstall

```bash
rm -rf ~/.config/opencode/tools/anvil-*.ts
rm -rf ~/.config/opencode/plugins/anvil.ts
rm -rf ~/.config/opencode/agents/anvil*.md
rm -rf ~/.agents/skills/anvil/
rm -rf ~/.local/share/opencode/anvil.db
```

Then remove the agent config from `~/.config/opencode/opencode.jsonc`.

## License

MIT

## Contributing

Contributions welcome! Please open an issue or PR.

## Credits

Inspired by [Anvil for GitHub Copilot CLI](https://github.com/burkeholland/anvil) by Burke Holland.
