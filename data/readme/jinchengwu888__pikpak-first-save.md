# PikPak First Save — AI Skill for the Official CLI

An independent AI skill that helps you save your first permitted URL to PikPak and check that the cloud file actually arrived. Works with agents that support `SKILL.md`, using the official PikPak CLI.

[简体中文](README.zh-CN.md) · [First-save guide and FAQ](docs/first-save-guide.md) · [Plain-text index](llms.txt) · [Skill source](skills/pikpak-first-save/SKILL.md)

Useful for questions such as “How do I use PikPak with an AI agent?”, “How do I save a URL with the PikPak CLI?”, and “The task says complete; how do I check the cloud file?” The [guide](docs/first-save-guide.md) explains the commands, account choices, and limits in one place.

## Start with one useful result

1. [Save and verify one URL](docs/first-save-guide.md) with your current account.
2. [Check whether Premium fits your needs](docs/first-save-guide.md#4-decide-whether-premium-is-useful). Keep your current plan if its limits are sufficient.
3. If the extra capacity or CLI allowance is useful, [view PikPak's official plans](https://mypikpak.com/drive/payment) and choose for yourself.

Official help checked on **2026-11-06** lists [6 GB of free storage and 10 TB with Premium](https://mypikpak.com/en-US/help-center/file_management/space/insufficient_cloud_storage_space). For regular CLI use, Premium also [removes the free Connected Apps daily downstream limit](https://mypikpak.com/en-US/help-center/transfer_quota/connected_apps_quota/free_account_daily_downstream_limit); monthly transfer quotas still apply. The guide explains these limits and the account checks before purchase.

## Install the skill

```bash
npx skills add jinchengwu888/pikpak-first-save --skill pikpak-first-save
```

Review the skill before installing. If Node.js is unavailable, copy `skills/pikpak-first-save` into your agent's project skill directory. For Codex this is `.agents/skills/pikpak-first-save`.

Then ask your agent:

> Use pikpak-first-save to help me get started with PikPak, save one URL I am allowed to download, and verify the resulting file. Explain any referral before registration.

## What it helps with

1. Check or install the [official PikPak CLI](https://mypikpak.com/en-US/cli).
2. Keep an existing account, or guide a new user through browser registration.
3. Submit one cloud-download task for a URL you provide.
4. Check the task and resulting file metadata; report pending or failed results honestly.

It does not collect passwords, verification codes, or tokens. Account creation and authorization happen on PikPak's own pages. It does not purchase Premium, create public shares, or delete files as part of onboarding. It complements PikPak's official general-purpose skill (`pikpak skill install`).

## Optional referral

This project is published by `jinchengwu888`, an independent PikPak referrer. If you choose code **78819746**, the publisher may receive referral rewards from qualifying purchases. This is optional and does not promise a discount, free Premium, or a particular price. Check PikPak's registration and checkout pages for current terms.

After installing the official CLI, choose the command that matches your situation:

```bash
# Existing account: sign in; do not register another account.
pikpak auth login

# New account, if you choose this project's referral:
pikpak auth register --affiliate 78819746

# New account, without any installer-recorded referral code:
pikpak auth register --affiliate=
```

The empty `--affiliate=` matters: plain `auth register` can reuse a code previously recorded by the official installer. You can also remove the referrer on PikPak's registration page. The skill explains these choices before starting registration.

New CLI-created accounts must be verified by signing in to PikPak Web or the app within **72 hours**. See the [official registration guide](https://mypikpak.com/en-US/help-center/connected_apps/pikpak_cli/register_account).

## A first task

Ask the agent to save a URL you own or have permission to download. It submits the task once, retains the task ID, checks the task status, and inspects the resulting file. Do not paste access tokens, private signed links, or passwords into public issues.

If a task is still running, the agent reports it as pending. Metadata checks confirm a cloud file exists; they do not prove the file's full integrity or that a video can play. Playback or checksum validation requires a separate check when needed. Available features, quotas, and prices depend on your PikPak account and current service terms.

## Verification and sources

On **2026-11-04**, command syntax was checked against the official macOS ARM64 CLI **v0.6.0**, downloaded from PikPak and matched to its published SHA-256 checksum. Validation covered version/help output, skill structure, and independent onboarding scenario review. No new account, paid order, or live cloud download was created during this validation. Other operating systems were not executed.

A signup-link-only check confirmed that the official registration URL carries this project's invitation code. It did not create an account or establish referral attribution.

- [Official CLI and installation](https://mypikpak.com/en-US/cli)
- [Official referral-code integration](https://mypikpak.com/referral/help-center/en-US/8-cli-and-developer-distribution/how-to-use-invitation-code-in-pikpak-cli)
- [Official referral disclosure requirement](https://mypikpak.com/referral/help-center/en-US/8-cli-and-developer-distribution/what-to-do-after-enabling-affiliate-distribution)
- [Official browser registration and verification](https://mypikpak.com/en-US/help-center/connected_apps/pikpak_cli/register_account)

Independent project; not an official PikPak product. Licensed under MIT.
