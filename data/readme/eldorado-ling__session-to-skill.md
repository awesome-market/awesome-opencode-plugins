# session-to-skill

从 OpenCode 会话分享链接中提取可复用模式，自动生成符合 SkillHub TRACE 评测体系和安全三线审核标准的可发布 Skill，并打包为 ZIP。

## 安装

将 `session-to-skill/` 目录放置到以下任一位置：

- 项目级：`.opencode/skills/session-to-skill/`
- 全局级：`~/.config/opencode/skills/session-to-skill/`

在 `opencode.json` 中添加权限：

```json
{
  "permission": {
    "skill": {
      "session-to-skill": "allow"
    }
  }
}
```

## 使用

1. 在任何 OpenCode 会话中执行 `/share` 复制分享链接
2. 新开一个会话，粘贴 share URL
3. 该 skill 自动触发，分析会话内容
4. 自动生成可发布的 Skill 并打包为 ZIP

触发短语：
- 「把会话做成 skill」
- 「从 share 链接提取 skill」
- 「生成 skill」「打包 session」「导出 skill」
- 直接在会话中粘贴 `opencode.ai/s/*` 或 `opncd.ai/share/*` 链接

## 工作流程

```
URL 校验 → 抓取会话 → 模式分析 → 生成 SKILL.md → TRACE 自检 → 安全三线审核 → ZIP 打包
```

## 输出

```
<skill-name>.zip
  ├── SKILL.md
  └── README.md
```

## 常见问题 & 避坑提示

### Q: 最多能处理多长的会话？
单次分享内容上限 **1MB**，超过会直接拒绝。生成内容上限 **500KB**，超过会自动截断。建议分享前在源会话中删掉无关的调试日志、长文件内容等。

### Q: macOS / Linux 能用吗？
可以。打包命令会自动适配系统：Windows 用 `Compress-Archive`，macOS/Linux 用 `zip -j`。

### Q: ZIP 上传 SkillHub 被拒怎么办？
常见原因：
- **ZIP 内有 LICENSE 等多余文件** → 只保留 SKILL.md + README.md
- **ZIP 多了父目录** → 确保 `zip -j` 或逐个文件压缩
- **SKILL.md 包含敏感关键词** → 避免在安全描述中使用 `eval`、`ignore previous instructions` 等字面值

### Q: WebFetch 抓取失败怎么办？
- 检查分享链接是否已过期（`/unshare` 后链接立即失效）
- 检查网络连接
- 在会话中说「重试」即可重新抓取

### Q: 生成的 skill 名称可以自己改吗？
可以。生成时会先告诉你建议的名称，你可以说「改成 xxx」。

### Q: TRACE 或安全检查不通过怎么办？
skill 会展示具体不通过的原因和修改建议。按建议修改源会话中的内容，重新 `/share` 后再运行。

## 从何而来

此 skill 由 session-to-skill 自身设计，专为 SkillHub（https://www.skillhub.cn）平台创建。
