# composer-search-skill

> OpenCode / Claude / Codex 技能 —— 在 Packagist 上搜索 PHP 类库，并按下载量排序。

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Lang: Node](https://img.shields.io/badge/Language-Node.js-339933.svg)
![Skills: 1](https://img.shields.io/badge/Skills-1-orange.svg)
![Platform: Packagist API](https://img.shields.io/badge/API-Packagist-4A154B.svg)

## 📖 简介

`composer-search` 是一个 **Agent Skill**：当 AI 代理需要为 PHP 项目寻找第三方类库时，它会通过 [Packagist 公开搜索 API](https://packagist.org/apidoc) 检索，并优先返回下载量最高、最受社区欢迎的库。技能还内置了安装流程，可直接在指定项目目录执行 `composer require` 完成安装。

- **来源**：[Anthropic Skill 规范](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)（`SKILL.md`），兼容 OpenCode、Claude Code、Codex 等支持 Skills 的代理。
- **零依赖**：仅使用 Node.js 内置模块（`https`、`child_process`），无需安装任何 npm 包。
- **安全**：脚本只做只读搜索与显式确认后的安装，不采集任何数据。

## ✨ 功能特性

| 能力 | 说明 |
| :--- | :--- |
| 🔍 关键词搜索 | 按关键词在 Packagist 检索 PHP 类库，默认返回 10 条，按下载量从高到低 |
| ⚠️ 废弃检测 | 自动标记已被 `abandoned` 的包，提示用户避免使用 |
| 📦 一键安装 | 确认后在指定目录执行 `composer require vendor/package` |
| 💬 结构化输出 | 统一以 JSON 返回，Agent 解析后渲染为 Markdown 表格 |

## 🚀 快速开始

### 目录结构

```text
composer-search/
├── SKILL.md                      # 技能定义（Agent 读取的指令文件）
└── scripts/
    ├── search_packagist.js       # 搜索脚本
    └── install_packagist.js      # 安装脚本
```

### 安装

将本仓库克隆到你的 opencode 技能目录（例如 `~/.config/opencode/skills/`）即可：

```bash
git clone https://github.com/dongpengfei1994/composer-search-skill.git
# 或手动将 SKILL.md 与 scripts/ 复制到 opencode 技能目录
```

> 也可以直接放在任意 Agent 的 skill/plugins 目录中，只要支持读取 `SKILL.md` 即可。

## 🔧 使用方式（供 Agent 调用）

### 1. 搜索类库

```bash
node scripts/search_packagist.js "pdf" 10
```

示例输出：

```json
{
  "status": "success",
  "data": [
    {
      "name": "mpdf/mpdf",
      "downloads": 30000000,
      "description": "A PHP class generating PDF files from UTF-8 encoded HTML.",
      "abandoned": false
    }
  ]
}
```

### 2. 安装类库

```bash
node scripts/install_packagist.js "mpdf/mpdf" "/path/to/project"
```

示例输出：

```json
{
  "status": "success",
  "message": "已在 \"/path/to/project\" 成功安装 mpdf/mpdf。"
}
```

## 📦 输出格式约定

所有脚本统一输出单行 JSON，供 Agent 解析：

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `status` | `string` | `success` / `error` |
| `data` | `array` | 搜索结果（包含 `name`、`downloads`、`description`、`abandoned`） |
| `message` | `string` | 成功提示或错误信息 |

**约定**：脚本无论结果如何均退出码 `0`，Agent 依据 JSON 中的 `status` 判断，禁止在 `error` 时重试脚本。

## 🧩 Agent 行为规范（已写入 SKILL.md）

1. 从用户输入中提取核心关键词，调用搜索脚本。
2. 将结果整理为表格展示，包名 / 下载量 / 描述必含。
3. 对 `abandoned: true` 的包附加 ⚠️ 废弃警告。
4. 安装前必须获得用户明确同意。

## 📚 相关资源

- [Packagist API 文档](https://packagist.org/apidoc)
- [Composer 官方文档](https://getcomposer.org/doc/)
- [Anthropic Agent Skills 规范](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)

## ⚠️ 免责声明

本项目仅封装 Packagist 公开 API 与 Composer 命令行，与 Packagist / Composer / PHP 官方无任何关联。

## 📄 许可证

[MIT](LICENSE) © 2026 dongpengfei1994