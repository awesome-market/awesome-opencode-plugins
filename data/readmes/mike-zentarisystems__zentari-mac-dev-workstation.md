# Zentari Mac Dev Workstation

A reproducible, local-first AI development and verification workstation for Apple Silicon Macs.

## M0 goals

- Zed as the primary editor and cockpit
- OpenCode as the primary local coding agent
- LM Studio as the local inference server
- OrbStack as the Docker/Linux runtime and disposable integration-test environment
- Playwright Test + Playwright MCP for browser verification
- Layered verification with linting, type checks, tests, security scans, container scans, and CI
- Portable agent skills under `.agents/skills`
- Idempotent, non-destructive bootstrap and health checks

## Architecture

```text
Zed
 └─ OpenCode (ACP)
     ├─ LM Studio :1234
     │   ├─ General/Vision model
     │   ├─ Coding model
     │   └─ Heavy reviewer model
     ├─ Skills
     ├─ Playwright MCP
     ├─ Git/GitHub
     └─ Shell

OrbStack
 ├─ Docker/Compose
 ├─ disposable Postgres/Redis/etc.
 └─ production-artifact verification
```

## Verification levels

### FAST
Format, lint, typecheck, and affected unit tests.

### FULL
FAST plus unit/integration tests, production build, Playwright, accessibility, secret scanning, security scanning, and diff review.

### RELEASE
FULL plus dependency scanning, container build/scan, clean-room testing, cross-browser E2E, failure-mode testing, and CI.

## Status

M0 bootstrap in progress. See `docs/ROADMAP.md` and `docs/MILESTONES.md`.
