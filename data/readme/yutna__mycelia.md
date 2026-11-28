# Mycelia

<!-- markdownlint-disable MD013 -->
[![ci](https://github.com/yutna/mycelia/actions/workflows/ci.yml/badge.svg)](https://github.com/yutna/mycelia/actions/workflows/ci.yml)
[![release](https://img.shields.io/github/v/release/yutna/mycelia?sort=semver)](https://github.com/yutna/mycelia/releases/latest)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
<!-- markdownlint-enable MD013 -->

Mycelia is a specification for an evidence-governed AI software factory on
OpenCode. It defines the roles, permissions, policies, execution loop,
assurance, observability, and readiness assessment that let autonomous agents
do real work in a repository without silent failure.

## Why Mycelia

Most agent setups optimize the prompt. A factory needs more:

- a work item that says what done means
- a role and permission contract that limits the blast radius
- a policy that a prompt cannot override
- evidence that a machine can check
- a trace that a human can audit
- a readiness assessment that says what the repository is missing

The name comes from the mycelium: the underground network that connects a
forest into one organism. In Mycelia, the agents are the fruiting bodies; the
network of contracts, evidence, and traces is the intelligence.

## What this repository is

- A normative specification for an OpenCode-based software factory.
- An OpenCode profile with least-privilege agents, policies, commands, and
  skills.
- A readiness model that reports the gap between a repository and the next
  safe autonomy level.
- A public audit trail of the specification itself.

It is not:

- product code, a runtime, or a hosted service
- a certification, an audit attestation, or legal advice
- a claim that every change can be fully autonomous

## The model in one page

| Layer | Question | Specification area |
| --- | --- | --- |
| Context | Does the agent see the right thing? | Context engineering |
| Control | What is it allowed to do? | Roles, policy, evidence |
| Execution | How does work move? | Loop, failure, concurrency |
| Assurance | How do we know it is right? | Verification, test integrity, review |
| Observability | What happened? | Trace, provenance, metrics |
| Evolution | How does it improve? | Evaluations, rules, adoption |

## Status

`v1.0.0` is the first stable specification release. It includes the normative
model, 24 readiness controls, three conformance profiles, 17 schemas, the
OpenCode profile, the readiness assessment, and the audit record.

The specification is not a certification, a complete autonomy guarantee, or
fitness for a particular regulatory regime. See [SCOPE.md](SCOPE.md) and
[CONFORMANCE.md](CONFORMANCE.md).

## Repository map

- [SCOPE.md](SCOPE.md) — boundaries, claims, and limitations
- [GLOSSARY.md](GLOSSARY.md) — shared terminology
- [AUDIT.md](AUDIT.md) — audit method, findings, and limitations
- [TRACEABILITY.md](TRACEABILITY.md) — requirements, controls, schemas
- [CONFORMANCE.md](CONFORMANCE.md) — v1.0.0 scope, claims, limitations
- [AGENTS.md](AGENTS.md) — the operating contract for agents
- [CONTRIBUTING.md](CONTRIBUTING.md) — the human version of the same process
- [docs/README.md](docs/README.md) — reading paths and the section map
- [opencode.json](opencode.json) — the OpenCode runtime profile
- `schemas/` and `examples/` — data contracts and worked examples (planned)

## Development

Requires [mise](https://mise.jdx.dev/). Then:

```sh
mise install
npm ci
mise run lint
```

`mise run lint` runs markdownlint and lychee. Link checking is offline, so a
third-party outage cannot block a pull request.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) and
[AGENTS.md](AGENTS.md) first. Every change follows the issue, draft pull
request, green CI, squash merge flow.

## License

[MIT](LICENSE)
