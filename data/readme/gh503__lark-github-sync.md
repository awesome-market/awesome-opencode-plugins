# lark-github-sync (AI Agent Orchestrator)

[![GitHub Issues](https://img.shields.io/badge/Sync-GitHub_Issues-181717?logo=github&logoColor=white)](https://github.com)
[![Feishu](https://img.shields.io/badge/Sync-Feishu_Docs-00D3A6?logo=lark&logoColor=white)](https://feishu.cn)
[![AI Agent](https://img.shields.io/badge/Powered_by-AI_Agent-8A2BE2)](https://github.com/gh503/lark-github-sync)

> A lightweight alternative to OpenAI's Symphony, designed for daily workflows.

An AI agent orchestrator skill that actively monitors, syncs, and executes tasks from both **GitHub Issues** and **Feishu (Lark) Docs**.

Instead of waiting passively, this skill turns your AI coding agent into a proactive project manager that drives work from requirement to Pull Request.

## 🚀 Features

- **Dual-Source Sync**: Pulls `todo` and `doing` tasks from GitHub Issues and unchecked Todo blocks from Feishu Docs.
- **Smart Context Recovery**: Automatically detects if a task is already in progress and checks out the corresponding local/remote branch to continue work.
- **End-to-End Execution**: Understands the requirement -> Plans the work -> Writes code -> Commits & Pushes -> Creates PR -> Updates original task status (checks Feishu block, closes GH Issue).
- **Interactive Triage**: Presents a unified task list and asks what you want to focus on today.

## 📦 Installation

Install this skill globally in your environment:

```bash
npx skills add gh503/lark-github-sync
```

## 🛠️ Usage

In your AI agent terminal or chat (e.g., Opencode), simply trigger:

```text
/lark-github-sync
```

Or just say:
> "帮我同步一下今天的任务" (Sync my tasks for today)

## 💡 How it works

1. Runs `gh issue list` to find GitHub tasks.
2. Uses the `lark-doc` skill (requires local Lark CLI setup) to read Feishu docs.
3. Consolidates everything into a clean Todo list.
4. Auto-creates branches (`feature/issue-<id>`).
5. Implements the feature and uses `gh pr create` to submit work.
