# AI Need Help — Reset, Access & Reliability Tools

Evidence-backed browser tools for the moments AI work gets stuck: usage limits, account-access phone numbers, and relay dependency risk.

**Live site:** https://aineedhelpfromotherai.com/

## Core product surfaces

- [Phone Number Survival Guide](https://aineedhelpfromotherai.com/tools/phone-number-survival-guide/) — plan how to buy, activate, verify, use abroad, keep alive, and recover a number that an important account may need again
- [Cursor Usage Reset Calculator](https://aineedhelpfromotherai.com/tools/cursor-usage-reset/) — understand Cursor reset timing and usage pacing
- [Claude Code Limit Reset Calculator](https://aineedhelpfromotherai.com/tools/claude-code-limit-reset/) — track session and weekly reset timing from the reset information shown by Claude
- [AI Relay Exit Risk Checker](https://aineedhelpfromotherai.com/tools/relay-exit-risk-checker/) — assess relay dependency with an evidence-backed 0–100 Exit Risk Index
- [All tools](https://aineedhelpfromotherai.com/tools/)

## What this project is now

The product is intentionally focused on three related jobs for AI power users:

1. **Access continuity** — keep control of phone numbers that AI accounts or services may depend on.
2. **Usage continuity** — understand when AI usage limits reset and when work can resume.
3. **Dependency continuity** — assess whether relying on a third-party AI relay creates avoidable exit risk.

Phone Number Lifecycle is the primary product surface. Reset tools and Relay Exit Risk are supporting surfaces. Older general calculators and image tools remain available but are maintenance-only rather than the product direction.

The site favors official/current sources, explicit unknowns, browser-side execution where practical, and stable canonical URLs. It does not require sign-up for the public tools.

## Development

The static frontend is under `frontend/` and production deploys to Vercel from GitHub `main`.

```bash
npm --prefix frontend ci
npm --prefix frontend run build
```

Current development rules and project state live in:

- `AGENTS.md`
- `PROJECT_CONTEXT.md`
- `docs/MASTER_PLAN.md`
- `docs/OPERATING_WORKFLOW.md`

## Historical components

This repository previously centered on an AI-agent debugging/MCP backend. Those components are retained for history and compatibility where needed, and the historical backend still supports Relay Exit Risk API functionality. They are not the current product direction.

Legacy scheduled workflows tied to the old Failure Memory/MCP product are kept manual-only unless a current product need explicitly reactivates them.

## License

MIT
