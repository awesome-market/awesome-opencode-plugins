# Agent Approve - Support

This is the public issue tracker for [Agent Approve](https://www.agentapprove.com). Use it to report bugs, request features, or ask questions.

- [Open an issue](https://github.com/agentapprove/support/issues/new)
- [Browse existing issues](https://github.com/agentapprove/support/issues)
- [Join discussions](https://github.com/agentapprove/support/discussions)

## What is Agent Approve?

Agent Approve lets you monitor AI coding agents and approve commands from your iPhone or Apple Watch. Go out and enjoy life while your agents stay busy. We'll ping you.

AI coding agents like Claude Code, Cursor, and Gemini can write code, refactor files, run tests, and execute shell commands autonomously. But when they hit a permission boundary -- something sensitive that requires human approval -- they stop and wait. And so do you.

Agent Approve fixes this. When your agent needs approval, you get a push notification on your phone or watch. You see the command, tap to approve or deny, and your agent keeps working. When it finishes a task, you get notified and can issue a follow-up with voice input.

Set your policies, configure your privacy level, and let your agents run. We'll find you when they need you.

## Supported Agents

- **Claude Code** - Anthropic's CLI for Claude
- **Cursor** - AI code editor
- **Gemini CLI** - Google's CLI
- **VS Code Agent** - VS Code agent hooks
- **GitHub Copilot CLI** - GitHub's coding agent
- **OpenClaw** - Open-source AI agent platform
- **OpenAI Codex** - coming soon
- And more

## Features

- **Approve on the go** - Hooks send events through our cloud so you can monitor and approve while walking the dog or getting coffee
- **Push notifications** - Never miss an approval request. Avoid wasted idle time with your agents
- **Apple Watch** - One-tap approvals from your wrist. Review context and respond without reaching for your phone
- **Voice commands** - Send follow-up commands to your agents using the microphone when they finish a task
- **Agent observability** - Full visibility into what all your agents are doing, especially autonomous agents like OpenClaw or long-running loops
- **Centralized policies** - Set auto-approve and deny rules across all your agents from a single policy
- **End-to-end encryption** - You own the keys. Approval requests are encrypted on your machine and decrypted only on your device
- **Privacy tiers** - Choose minimal, summary, or full data logging. Control retention from 1 to 365 days

## Getting Started

1. Download Agent Approve from the App Store and start your 7-day free trial
2. Follow the in-app onboarding, which prompts you to run `npx agentapprove` on each machine
3. The installer pairs your device, sets up hooks, and configures your agents
4. Approve or deny actions from your phone or watch

## npm Packages

| Package | Description |
|---------|-------------|
| [`agentapprove`](https://www.npmjs.com/package/agentapprove) | CLI installer for all supported agents |
| [`@agentapprove/openclaw`](https://www.npmjs.com/package/@agentapprove/openclaw) | OpenClaw plugin |

## Links

- [Website](https://www.agentapprove.com)
- [iOS App](https://apps.apple.com/app/agentapprove)
- [Contact](mailto:hello@agentapprove.com)

## License

Proprietary. Copyright (c) 2026 Agent Approve LLC. All rights reserved.
