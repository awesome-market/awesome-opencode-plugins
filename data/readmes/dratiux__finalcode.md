<p align="center">
  <img src="assets/finalcode-logo.svg" alt="FinalCode" width="468">
</p>

# FinalCode

<p align="center">
  <a href="https://www.skills.sh/b/dratiux/FinalCode"><img src="https://www.skills.sh/b/dratiux/FinalCode" alt="Skills"></a>
  <a href="https://github.com/dratiux/FinalCode/releases"><img src="https://img.shields.io/github/v/release/dratiux/FinalCode" alt="Release"></a>
  <a href="https://github.com/dratiux/FinalCode/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT"></a>
</p>

FinalCode is a context-aware production certification and organization intelligence platform. It runs a senior-engineering audit across 13 quality gates, automatically adapts certification requirements to project type, architecture, deployment target, and maturity, validates engineering decisions to distinguish defects from intentional trade-offs, and extends analysis from single repositories to entire engineering organizations — correlating, comparing, and improving multi-repository ecosystems with cross-repository findings, organizational dashboards, team insights, and executive reporting. Produces a standardized Certification Report with a clear verdict: READY TO SHIP, READY WITH WARNINGS, or NOT READY.

Engineering quality is universal. Certification requirements are contextual. Not every deviation from best practice is a defect — FinalCode's Engineering Decision Validation Framework ensures intentional decisions and accepted trade-offs are recognized, not penalized.

## Project Status

FinalCode is an independent open-source project created and maintained by Dratiux. It is distributed through the Skills ecosystem and compatible with Skills-compatible AI coding agents.

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Workflow](#workflow)
- [Quality Gates](#quality-gates)
- [Certification Verdict](#certification-verdict)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Requirements](#requirements)
- [Examples](#examples)
- [Engineering Documentation](#engineering-documentation)
- [Contributing](#contributing)
- [Security](#security)
- [Support](#support)
- [License](#license)

## Quick Start

```bash
npx skills add dratiux/FinalCode
```

Then restart your AI coding agent and run:

```
Run FinalCode
```

## Installation

Install FinalCode using the official skills.sh CLI:

```bash
npx skills add dratiux/FinalCode
```

skills.sh automatically detects your environment and installs FinalCode to the correct location. No manual configuration required.

**Options:**

| Flag | Description |
|------|-------------|
| `-g` | Install globally (available in all projects) |
| `-y` | Skip confirmation prompts |
| `--skill finalcode` | Install only the FinalCode skill |
| `--list` | List available skills before installing |

**Examples:**

```bash
# Global installation
npx skills add dratiux/FinalCode -g

# Non-interactive installation
npx skills add dratiux/FinalCode -y

# List available skills
npx skills add dratiux/FinalCode --list
```

### Updating

```bash
npx skills add dratiux/FinalCode --update
```

## Workflow

FinalCode operates in four modes:

| Mode | Modifies Files | Use Case |
|------|----------------|----------|
| **Inspect** | No | Audit the repository and produce a report |
| **Repair** | Yes | Apply verified fixes, then re-inspect |
| **Refactor** | Yes | Improve maintainability without behavior change |
| **Certify** | No | Final sign-off before release |

### Commands

```
Run FinalCode                          # Inspect mode
Run FinalCode in Repair Mode           # Repair mode
Run FinalCode in Refactor Mode         # Refactor mode
Run FinalCode in Certify Mode          # Certify mode
```

## Quality Gates

FinalCode evaluates repositories across 13 quality gates:

| Gate | Scope |
|------|-------|
| Architecture | Project structure, module organization, dependency management |
| Code Quality | Complexity, duplication, naming conventions |
| Dead Code | Unused files, exports, variables, functions |
| Dependencies | Outdated packages, security vulnerabilities, license compliance |
| Type Safety | TypeScript strictness, type annotations, type errors |
| Error Handling | Try-catch blocks, error propagation, error recovery |
| Testing | Unit tests, integration tests, E2E tests, coverage |
| Performance | Bundle size, load times, memory usage |
| Security | 14-category security analysis (Security Gate 2.0) |
| Accessibility | WCAG compliance, screen reader support, keyboard navigation |
| UI Consistency | Design system compliance, component consistency |
| Documentation | README, API docs, inline comments, changelog |
| GitHub Readiness | Issue templates, PR templates, CI/CD, badges |

Detailed checklists: [skills/finalcode/references/gates.md](skills/finalcode/references/gates.md) and [skills/finalcode/references/security-gate.md](skills/finalcode/references/security-gate.md).

## Certification Verdict

| Verdict | Exit Code | Meaning |
|---------|-----------|---------|
| READY TO SHIP | 0 | All mandatory gates PASS |
| READY WITH WARNINGS | 1 | Mandatory gates PASS but warnings exist |
| NOT READY | 2 | One or more mandatory gates FAIL |
| NO PROJECT FOUND | 3 | No valid project detected |

## Architecture

FinalCode uses a Single Source of Truth (SSOT) architecture. All editable files live in `skills/finalcode/`.

```
skills/finalcode/
├── SKILL.md                     # Skill specification (v5.2.0)
├── scripts/                     # Deterministic helpers: health_score, validate_findings, report_scaffold (v5.1.0)
├── evals/                       # Measurable evals + fixtures (v5.2.0, 4 evals)
├── core/                        # Core engine + organization intelligence layer
│   ├── organization-registry.md           # Repository inventory (v5.0.0)
│   ├── multi-repository-analysis.md       # Cross-repo analysis (v5.0.0)
│   ├── repository-relationship-engine.md  # Relationship graph (v5.0.0)
│   ├── shared-library-discovery.md        # Duplicate detection (v5.0.0)
│   ├── engineering-organization-dashboard.md # Org dashboard (v5.0.0)
│   ├── organization-roadmap.md            # Org-wide roadmap (v5.0.0)
│   ├── team-engineering-insights.md       # Team metrics (v5.0.0)
│   ├── api-ecosystem-analysis.md          # Cross-repo API analysis (v5.0.0)
│   ├── dependency-graph-v2.md             # Org dependency graph (v5.0.0)
│   ├── platform-standardization.md        # Standardization (v5.0.0)
│   ├── release-governance.md              # Multi-repo release tracking (v5.0.0)
│   ├── organization-memory.md             # Org knowledge (v5.0.0)
│   ├── organization-benchmark.md          # Internal repo ranking (v5.0.0)
│   ├── executive-reporting.md             # Executive summaries (v5.0.0)
│   ├── engineering-decision-engine.md     # Observation classification (v4.5.0)
│   ├── decision-validation.md             # Intent validation (v4.5.0)
│   ├── decision-confidence.md             # Decision confidence (v4.5.0)
│   ├── tradeoff-registry.md               # Trade-off standardization (v4.5.0)
│   ├── decision-explainability.md         # Recommendation explanation (v4.5.0)
│   ├── recommendation-roi.md              # Recommendation ROI (v4.5.0)
│   ├── engineering-recognition.md         # Engineering strengths (v4.5.0)
│   ├── benchmark-intelligence.md          # Benchmark comparison (v4.5.0)
│   ├── decision-timeline.md               # Decision history (v4.5.0)
│   ├── engineering-intent-memory.md       # Intent persistence (v4.5.0)
│   ├── decision-engine.md       # Decision pipeline and rule matching
│   ├── policy-engine.md         # Policy engine and built-in policies
│   ├── rule-registry.md         # Rule registry and lifecycle
│   ├── report-engine.md         # Report engine and section definitions
│   └── certification-engine.md  # Certification pipeline and validation
├── plugins/                     # Plugin layer
│   ├── sdk.md                   # Plugin SDK and registration
│   ├── profiles.md              # Framework profiles (14 frameworks)
│   └── marketplace.md           # Extension marketplace foundation
└── references/                  # Reference documentation
    ├── examples.md              # Worked example reports
    ├── gates.md                 # Quality gate checklists
    ├── security-gate.md         # Security gate checklist
    ├── configuration.md         # Configuration schema
    ├── plugins.md               # Plugin architecture
    ├── health-score.md          # Health score formula
    ├── confidence-model.md      # Confidence model 2.0
    ├── finding-classification.md # Finding classification
    ├── explainability.md        # Explainability engine
    ├── release-engine.md        # Release blocker engine
    └── architecture.md          # System architecture
```

## Configuration

FinalCode can be configured without editing the skill. Place a `finalcode.config.json` at the repository root or `.finalcode/config.json`. See [skills/finalcode/references/configuration.md](skills/finalcode/references/configuration.md) for the schema.

### Built-in Policies

| Policy | Use Case |
|--------|----------|
| POLICY-DEFAULT | Default behavior |
| POLICY-PRODUCTION | Production systems |
| POLICY-ENTERPRISE | Enterprise environments |
| POLICY-STARTUP | Rapid development |
| POLICY-OPENSOURCE | Open source projects |
| POLICY-EDUCATIONAL | Learning projects |
| POLICY-MINIMAL | Minimum checks |
| POLICY-STRICT | Maximum strictness |

### Policy Selection

1. Explicit configuration (`policy: "POLICY-PRODUCTION"`)
2. Project profile default
3. Command-line flag (`--policy POLICY-ENTERPRISE`)
4. Default (`POLICY-DEFAULT`)

## Requirements

| Requirement | Minimum |
|-------------|---------|
| Node.js | 18+ |
| npm | 9+ |

FinalCode works with any Skills-compatible AI coding agent. Refer to the [Skills documentation](https://skills.sh) for the latest supported environments.

## Examples

### Clean Repository

```
Certification: READY TO SHIP
Exit Code: 0
Health Score: 94 / 100
Grade: A+
```

### Repository with Issues

```
Certification: NOT READY
Exit Code: 2
Health Score: 67 / 100
Grade: C+
Blocking Issues: 3
```

Full examples: [skills/finalcode/references/examples.md](skills/finalcode/references/examples.md).

## Engineering Documentation

FinalCode generates persistent documentation inside `.finalcode/`:

| Document | Purpose |
|----------|---------|
| `reports/<timestamp>-<mode>.md` | Immutable execution reports |
| `CHANGE_REPORT.md` | Engineering change log |
| `REFACTOR_REPORT.md` | Refactoring history |
| `FINALCODE_SUMMARY.md` | Executive summary |
| `CERTIFICATION_HISTORY.md` | Certification log |
| `TREND.md` | Historical trend analysis |
| `BASELINE.md` | First-execution baseline |

Reports are immutable. New executions create new timestamped files.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md).

## Support

- [GitHub Issues](https://github.com/dratiux/FinalCode/issues)
- [GitHub Discussions](https://github.com/dratiux/FinalCode/discussions)
- dratiux@gmail.com

See [SUPPORT.md](SUPPORT.md) for troubleshooting.

## License

MIT License. See [LICENSE](LICENSE).

---

<p align="center">
  <br>
  <sub>CRAFTED WITH CARE BY DRATIUX</sub>
  <br><br>
  <a href="https://paypal.me/dratiux"><img src="https://img.shields.io/badge/PayPal-F2F2F2?logo=paypal&logoColor=003087&style=flat" alt="PayPal"></a>
  <a href="https://ko-fi.com/dratiux"><img src="https://img.shields.io/badge/Ko--fi-F2F2F2?logo=ko-fi&logoColor=FF5E5B&style=flat" alt="Ko-fi"></a>
</p>
