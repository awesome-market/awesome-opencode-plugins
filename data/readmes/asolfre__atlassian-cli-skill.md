# Atlassian CLI Skill for Agents

Teach your AI coding agent to use the official Atlassian Cloud CLI (`acli`) correctly, so it runs real commands instead of guessing wrong ones.

## The Problem

Ask a coding agent to "create a Jira bug in the TEAM project" without this skill and you'll get one of these:

- A Python script using the Jira REST API that you have to install dependencies for, configure, and run yourself
- Commands for [Bob Swift's ACLI](https://bobswift.atlassian.net/wiki/spaces/ACLI): a different, paid, third-party tool with completely different syntax
- Hallucinated flags like `--issue-type` (doesn't exist) or `--priority Critical` (wrong format)
- No safety check: it might run `delete` commands without asking you first

## The Fix

Install this skill and the same question produces:

```bash
acli auth status                    # checks you're logged in first
acli jira workitem create \
  --summary "Fix login bug" \
  --project "TEAM" \
  --type "Bug" \
  --assignee "@me"                  # correct flags, correct syntax
```

The agent confirms the command with you before running it (create = moderate safety tier), then executes it live and shows you the result.

## With Skill vs Without: Hard Numbers

We ran 13 eval scenarios covering Jira, Confluence, Admin, and cross-product workflows, totaling 93 individual assertions (correct command, correct flags, auth check, safety tier, no hallucinated flags, etc.).

|  | Assertions Passed | Score |
|---|---|---|
| **Without skill** | 18 / 93 | 19% |
| **With skill** | 93 / 93 | 100% |

**+81 percentage points.** The gap comes from three failure modes that disappear with the skill:

1. **Wrong tool.** Without the skill, agents default to REST API scripts or confuse the official `acli` with Bob Swift's ACLI. The skill teaches the correct `acli <product> <entity> <action> [flags]` pattern.
2. **Wrong flags.** Without the skill, agents guess flag names and get them wrong. The skill includes 1,250+ lines of command reference with every flag, short form, and default value.
3. **No safety guardrails.** Without the skill, agents run destructive commands without confirmation. The skill enforces three safety tiers (safe / moderate / dangerous) with escalating confirmation requirements.

## What It Covers

| Product | Operations |
|---|---|
| **Jira** | Work items (create, search, edit, transition, delete, clone, bulk ops), projects, boards, sprints, filters, dashboards, fields, CSV/JSON export |
| **Confluence** | Spaces (list, view, create, archive), pages (view), blog posts (create, list) |
| **Admin** | User management (activate, deactivate, delete, cancel-delete) |
| **Rovo Dev** | Session management (run, auth) |
| **Auth** | OAuth browser flow, API tokens, admin API keys, Rovo Dev scoped tokens, CI/CD pipeline setup |

## Safety Tiers

The skill classifies every command into a safety tier before execution:

| Tier | Actions | Agent behavior |
|---|---|---|
| **Safe** | `search`, `list`, `view`, `get`, `auth status` | Executes immediately -- read-only, no risk |
| **Moderate** | `create`, `edit`, `transition`, `assign`, `comment` | Shows command, asks for confirmation, then runs |
| **Dangerous** | `delete`, `archive`, bulk ops via `--jql` | Previews impact first (runs a count/search), shows what will be affected, requires explicit confirmation. Never auto-passes `--yes` |

## Install

```bash
npx skills add asolfre/atlassian-cli-skill
```

The skill auto-triggers when you ask the agent to do something with Jira, Confluence, or Atlassian from the terminal. No configuration needed.

<details>
<summary>Other install methods</summary>

```bash
# Per-project
git clone https://github.com/asolfre/atlassian-cli-skill.git .opencode/skills/atlassian-cli

# Globally for all projects
git clone https://github.com/asolfre/atlassian-cli-skill.git ~/.config/opencode/skills/atlassian-cli
```

</details>

### Prerequisites

1. **Install `acli`** (the official Atlassian Cloud CLI):
   ```bash
   brew tap atlassian/homebrew-acli && brew install acli
   ```
2. **Authenticate** with your Atlassian instance:
   ```bash
   acli auth login
   ```

## How It Works

The skill uses **progressive disclosure** to stay efficient:

1. **SKILL.md** (400 lines) loads on trigger -- contains the command pattern, safety tiers, execution workflow, and the most common commands for each product.
2. **Reference files** (1,250 lines across 4 files) load on demand -- the agent reads `references/jira.md` only when it needs exact flags for a Jira command. Same for `confluence.md`, `admin.md`, and `auth.md`.

This means the agent doesn't burn context on Confluence reference docs when you're doing Jira work.

## Trigger Accuracy

The skill triggers when it should and stays silent when it shouldn't. We tested 20 queries (10 that should trigger, 10 near-miss negatives that shouldn't) across 60 individual runs:

| Metric | Score |
|---|---|
| Precision | 100% |
| Recall | 100% |
| Accuracy | 100% |

Examples of queries that correctly **do not** trigger the skill:
- "How do I configure the columns on my Jira board?" (conceptual, not CLI)
- "Write a Python script using the Jira REST API" (REST API, not `acli`)
- "Help me design a Jira workflow with custom statuses" (workflow design, not execution)
- "Can you read the Confluence page at https://..." (web URL, not CLI)

## File Structure

```
SKILL.md                    # Main skill (400 lines)
references/
  jira.md                   # Jira command reference (660 lines)
  confluence.md             # Confluence command reference (240 lines)
  admin.md                  # Admin command reference (110 lines)
  auth.md                   # Auth methods reference (245 lines)
evals/
  evals.json                # 13 eval scenarios, 93 assertions
  trigger-eval.json         # 20 trigger accuracy queries
```

## License

MIT
