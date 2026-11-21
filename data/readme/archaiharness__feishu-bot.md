# ArchAIHarness Feishu Bot

[![OpenCode](https://img.shields.io/badge/OpenCode-Feishu%20Bot-111827?style=for-the-badge)](https://opencode.ai)
[![Node.js](https://img.shields.io/badge/Node.js-22-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org)
[![Feishu](https://img.shields.io/badge/Feishu-Bot-2563EB?style=for-the-badge)](https://open.feishu.cn)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Feishu-native OpenCode assistant runtime.**

`feishu-bot` connects Feishu messages to OpenCode sessions through an OpenCode plugin and a project skill. It lets a Feishu bot receive private or group messages, inject them into OpenCode, and send replies back through Feishu tools.

## What It Provides

- Feishu WebSocket event bridge
- OpenCode plugin tools for sending messages, searching users, and listing chats
- Project skill `feishu-bot` with strict usage rules
- Group reply support with automatic `@` resolution and quote reply
- Docker runtime for OpenCode Web mode
- Secret-safe example configuration

## Repository Layout

```text
.
├── AGENTS.md
├── Dockerfile
├── README.md
└── .opencode
    ├── feishu.yaml.example
    ├── opencode.json
    ├── package.json
    ├── package-lock.json
    ├── plugins/feishu-bot.js
    ├── reminders/
    └── skills/feishu-bot/SKILL.md
```

## Quick Start

```bash
cd .opencode
npm install
cp feishu.yaml.example feishu.yaml
```

Edit `.opencode/feishu.yaml` with your Feishu app credentials:

```yaml
app:
  app_id: cli_xxxxxxxxxxxxxxxx
  app_secret: your-feishu-app-secret
```

Then start OpenCode from the repository root:

```bash
opencode web --port 4096 --hostname 0.0.0.0
```

Restart OpenCode after changing `.opencode/opencode.json`, plugin files, skills, or Feishu config.

## Docker

The Dockerfile copies `feishu.yaml.example` as a placeholder. For real deployments, mount the actual config at runtime:

```bash
docker run --rm -p 4096:4096 \
  -v "$PWD/.opencode/feishu.yaml:/app/.opencode/feishu.yaml:ro" \
  archaiharness/feishu-bot
```

## Tools

| Tool | Purpose |
| --- | --- |
| `feishu_send_message` | Send private or group messages |
| `feishu_search_user` | Search users and return `open_id` |
| `feishu_list_chats` | List bot-visible group chats |
| `feishu_list_chat_members` | List members of a chat |

## Security

- `.opencode/feishu.yaml` is ignored by git.
- Do not commit Feishu `app_secret`, tokens, or private chat/user data.
- Use `.opencode/feishu.yaml.example` as the only committed config template.

## License

MIT

---

Engineered by Architects · Empowered by AI
