<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/qubrics-logo-horizontal-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/qubrics-logo-horizontal-light.svg">
  <img alt="Qubrics" src="assets/qubrics-logo-horizontal-light.svg" width="450">
</picture>

# Qubrics Agent Skills

Official Qubrics skills for AI coding agents. See the [Qubrics Agent Skills guide](https://qubrics.com/docs/guides/agent-skills) for setup and usage.

## Marketplace install

This repository contains Qubrics plugin bundles for Cursor, Claude, and Codex. Cursor installation through `/add-plugin` requires marketplace approval.

Cursor (after marketplace publication):

```text
/add-plugin qubrics
```

Claude app, Claude Desktop, and Cowork:

1. Open **Customize**.
2. Go to **Plugins**.
3. In **Personal plugins**, click **+** and choose **Add marketplace**.
4. Choose **Add from a repository**.
5. Enter `qubrics/skills`, then install the **Qubrics** plugin.

Claude Code:

```text
/plugin marketplace add qubrics/skills
/plugin install qubrics@qubrics
/reload-plugins
```

Codex app and Codex CLI:

```bash
codex plugin marketplace add qubrics/skills
```

Then open **Plugins** in the Codex app or `/plugins` in Codex CLI and install **Qubrics** from the Qubrics marketplace.

### Deprecated compatibility entry

The **Sendmux (deprecated)** plugin remains installable in the `qubrics` marketplace and includes the same Qubrics skills. Install **Qubrics** for new setups. If you added the repository before the rename, add `qubrics/skills` again to refresh the marketplace name.

For Claude Code, the compatibility entry is `/plugin install sendmux@qubrics`. In Codex, select **Sendmux (deprecated)** from the Qubrics marketplace.

## Direct Agent Skills install

Use `skills add` when your agent supports raw Agent Skills rather than plugin marketplaces.

```bash
npx skills add qubrics/skills
```

Install one skill from the pack:

```bash
npx skills add qubrics/skills --skill qubrics-send-email
```

Update an installed pack:

```bash
npx skills update
```

## What This Pack Teaches

- Choose the cheapest correct Qubrics surface for the task: MCP for connected agents, the `qubrics` CLI for terminal one-shots, and SDKs for application flows.
- Register an agent inbox without an existing account or key by using `qubrics agent:register`; the saved profile keeps durable read access while active, and sending remains owner-gated.
- Connect an existing account through scoped REST OAuth, validate access without sending email, and manage login, refresh and logout through the CLI.
- For API-key workflows, use `smx_root_*` for account-level work, send-capable `smx_mbx_*` keys for owner-created workflows, durable agent profiles for self-registered mailbox reads, and one-hour delegated tokens after owner-approved agent sends.
- Prefer efficient calls: batch operations, cursor pagination, conditional requests, idempotency keys, counts, snippets, and delta sync where the public surface supports them.
- Verify results before reporting success.

## Skills Catalogue

The catalogue is built item by item from the local API, SDK, CLI, and MCP source of truth.

| Skill                           | Use when                                                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `qubrics-agent-email-inbox`              | Reviewing an authorised inbox and preparing reply drafts without changing messages or sending.          |
| `qubrics-email-for-ai-agents`            | Sending one approved outbound email and reconciling retries with a stable idempotency key.               |
| `qubrics-getting-started`       | Choosing a Qubrics surface, setting up auth, or making a first verified call.                           |
| `qubrics-send-email`            | Sending single or batch transactional email.                                                            |
| `qubrics-attachments`           | Uploading, downloading, or sending attachments without wasting context on base64.                       |
| `qubrics-mailbox-agent`         | Reading, triaging, replying, or syncing one mailbox.                                                    |
| `qubrics-management`            | Managing domains, mailboxes, sending accounts, webhooks, billing, and logs.                             |
| `qubrics-cli`                   | Using the `qubrics` CLI from a terminal.                                                                |
| `qubrics-mcp-setup`             | Connecting Qubrics MCP servers to an agent client.                                                      |
| `qubrics-token-efficient-usage` | Choosing low-token Qubrics calls and avoiding wasteful reads.                                           |
| `qubrics-email-for-agents`      | Giving an AI agent an inbox, durable self-registration flow, or email workflow, even when Qubrics is not named. |

## Target matrix

| Target | Recommended install |
| --- | --- |
| Cursor | After official marketplace publication, run `/add-plugin qubrics`. |
| Claude app, Claude Desktop, Cowork | Add marketplace from repository `qubrics/skills`, then install **Qubrics**. |
| Claude Code | `/plugin marketplace add qubrics/skills`, then `/plugin install qubrics@qubrics`. |
| Codex app and Codex CLI | `codex plugin marketplace add qubrics/skills`, then install **Qubrics** from **Plugins** or `/plugins`. |
| Agent Skills clients | `npx skills add qubrics/skills`. |
| Single-skill installs | `npx skills add qubrics/skills --skill <skill-name>`. |

Marketplace plugins and raw Agent Skills only teach workflows. They do not grant Qubrics access. Authorise hosted MCP or scoped REST OAuth, create API keys, or use agent access before asking an agent to act on Qubrics data.

## Development

This repo uses the Agent Skills format:

```text
skills/
  <skill-name>/
    SKILL.md
    references/
    scripts/
    assets/
```

Each skill must be validated, benchmarked against a baseline, and packaged before it is marked complete.

Generate Cursor, Claude, and Codex marketplace bundles:

```bash
node scripts/build-plugin-bundles.mjs
node scripts/check-plugin-bundles.mjs
```

The canonical skill source stays in `skills/`. Cursor reads it directly; generated Cursor, Claude, and Codex manifests plus both MCP files are checked for drift in CI.

See `docs/eval-lint-package-playbook.md` for the local eval, lint, package, and install-smoke loop.
See `docs/regen-update-playbook.md` for the source drift check and regeneration procedure.
