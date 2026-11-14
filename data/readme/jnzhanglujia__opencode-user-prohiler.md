# user-context-profile

> An OpenCode Skill for creating and managing detailed user profiles — so AI agents always know who you are and how you work.

[中文版本](#中文介绍)

---

## English

### What is this?
A plug-in Skill for [OpenCode](https://opencode.ai) (and compatible AI agents like OpenClaw, Hermes, Claude Code, Codex CLI). It builds a **rich personal profile** through a structured questionnaire, covering:

- **Personal Info**: name, age, gender, height, weight, education
- **Work & Dev Role**: occupation, dev role, work style, available hours, peak energy time
- **Tech Stack**: OS, IDE, frameworks, database, skill level, learning style
- **Personality & Preferences**: personality type, communication style, hobbies
- **Project Constraints**: project types, budget, performance targets, accessibility

Once the profile is saved, any AI agent using this Skill will automatically read `user-data.json` and tailor its responses — tech stack choices, code style, architecture decisions, communication tone — to match **your** preferences.

### Quick Start

#### 1. Installation
Copy the entire `user-context-profile` folder into your agent's skills directory:

| Agent | Path |
|-------|------|
| OpenCode | `~/.config/opencode/skills/user-context-profile/` |
| OpenClaw | `~/.openclaw/skills/user-context-profile/` |
| Hermes | `~/.hermes/skills/user-context-profile/` |
| Claude Code | `~/.claude/skills/user-context-profile/` |
| Codex CLI | `$CODEX_HOME/skills/user-context-profile/` |

#### 2. Configure Auto-Load
Add the following to your project's `AGENTS.md` file:

```markdown
At the start of every conversation, automatically:
1. Load the `user-context-profile` skill
2. Read `user-data.json` for user profile data
3. Tailor all responses based on the stored profile
```

#### 3. Run the Survey
Start a new conversation and say **"run user context survey"**. The agent will ask a series of ~25 questions covering all profile dimensions. At the end, review the summary and type **"submit"** to save.

#### 4. Done!
Now every time you ask the agent to plan or build something, it will automatically consult your profile and make personalized recommendations.

### File Structure

```
user-context-profile/
├── SKILL.md                 # Skill definition & questionnaire
├── user-data.json           # Your profile data (edit with care)
├── scripts/
│   └── update_helper.py     # CLI tool to update JSON fields
└── README.md
```

### Updating Your Profile
- **In conversation**: tell the agent "update my tech stack, add Rust" or "change communication style to concise" — it will update `user-data.json` automatically.
- **Manually**: edit `user-data.json` directly.
- **CLI**: `python scripts/update_helper.py --path personal_info.name --value 'Your Name'`

### Privacy
- All data is stored **locally only** — never sent to any external API.
- The template `user-data.json` ships with placeholder values. Fill in your own.
- Sensitive fields (API keys, passwords) should be stored in `.env`, not here.

### Requirements
- An AI agent that supports the [Agent Skills Open Standard](https://opencode.ai)
- Python 3.x (only needed for the CLI helper, the Skill itself is pure text)

---

## 中文介绍

### 这是什么？
这是一个专为 [OpenCode](https://opencode.ai)（及兼容的 AI 助手如 OpenClaw、Hermes、Claude Code、Codex CLI）设计的 **用户画像 Skill**。通过一份结构化问卷，构建你的详细个人画像，涵盖：

- **基本信息**: 称呼、性别、年龄、身高、体重、学历
- **职业与角色**: 职业、开发角色、工作方式、投入时长、精力时段
- **技术栈**: 操作系统、IDE、框架偏好、数据库、技术水平、学习方式
- **个性与偏好**: 性格、沟通风格、兴趣爱好
- **项目约束**: 项目类型、预算、性能要求、无障碍需求

画像保存后，AI 助手每次为你工作时都会自动读取，从技术选型、代码风格到沟通方式，都贴合你的个人习惯。

### 快速开始

#### 1. 安装
将 `user-context-profile` 整个文件夹复制到对应目录：

| 助手 | 路径 |
|------|------|
| OpenCode | `~/.config/opencode/skills/user-context-profile/` |
| OpenClaw | `~/.openclaw/skills/user-context-profile/` |
| Hermes | `~/.hermes/skills/user-context-profile/` |
| Claude Code | `~/.claude/skills/user-context-profile/` |
| Codex CLI | `$CODEX_HOME/skills/user-context-profile/` |

#### 2. 配置自动加载
在项目根目录的 `AGENTS.md` 中加入：

```markdown
每次对话开始时，自动执行以下步骤：
1. 加载 `user-context-profile` skill
2. 读取 `user-data.json` 中的用户画像数据
3. 根据画像为用户提供个性化服务
```

#### 3. 填写问卷
打开新对话，输入 **"填写画像"**。助手会依次问你约25道题（大部分是选择题），涵盖了你的基本信息、技术偏好、工作习惯等。全部答完后会展示摘要，确认无误后输入 **「提交」** 保存。

#### 4. 完成！
以后你再让助手做项目，它会自动读取你的画像，推荐最适合你的技术方案和代码风格。

### 文件结构

```
user-context-profile/
├── SKILL.md                 # Skill 定义 & 问卷内容
├── user-data.json           # 你的画像数据
├── scripts/
│   └── update_helper.py     # JSON 更新小工具
└── README.md
```

### 更新画像
- **对话中更新**: 直接说 "帮我更新技术栈，加个Rust" 或 "通信偏好改成简洁风格"，助手会自动修改 `user-data.json`
- **手动编辑**: 直接打开 `user-data.json` 修改
- **命令行**: `python scripts/update_helper.py --path personal_info.name --value '你的名字'`

### 隐私说明
- 所有数据**仅存储在本地**，不会发送到任何外部 API
- 仓库中的 `user-data.json` 是模板，请替换成自己的信息
- 敏感信息（API 密钥、密码等）请放在 `.env`，不要放这里

### 环境要求
- 支持 [Agent Skills Open Standard](https://opencode.ai) 的 AI 助手
- Python 3.x（仅 CLI 工具需要，Skill 本身是纯文本）
