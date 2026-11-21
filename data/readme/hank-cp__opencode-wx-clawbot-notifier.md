# opencode-wx-clawbot-notifier

OpenCode V2 插件：当 AI 调用 `question` 等人工介入工具、等待用户回答**超时**时，通过**微信（ClawBot）**主动通知用户。

> 场景：你发起一个长任务后离开电脑，AI 中途用 `question` 工具问你问题，但你不在终端前。默认超过 5 分钟未响应，插件会用微信给你发一条消息，附上问题内容，催你回来回答。

## 工作原理

```
question 工具开始执行（等待用户回答）
        │  tool.execute.before → 启动超时计时器（默认 5 分钟）
        ▼
   用户及时回答？
   ├─ 是 → tool.execute.after → 取消计时器，一切正常
   └─ 否 → 计时器触发 → 通过微信 iLink Bot 网关发送通知
```

- 监听基于 OpenCode V2 插件 API：`ctx.tool.hook("execute.before")` / `execute.after`
- 通知通道复用 [opencode-wechat-plugin](https://github.com/Ikaros12643/opencode-wechat-plugin) 验证过的 **微信 ClawBot → iLink Bot 网关**协议（已按 2.4.10 报文修正，适配 Node 24）

## 安装

```sh
opencode plugin add @laxture/opencode-wx-clawbot-notifier --global
```

或在 `opencode.jsonc` 中配置：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["@laxture/opencode-wx-clawbot-notifier"]
}
```

## 首次登录（必须）

微信 bot 只能给**主动联系过它**的用户发消息，所以需要先扫码登录：

1. 在 OpenCode 里运行 `/wx-login`
2. 插件会在聊天流里直接渲染终端二维码（主方式），同时把二维码图片保存到 `~/.opencode/wx-clawbot/account.json.qrcode.png`（兜底，终端渲染不佳时可打开图片），并打印原始登录链接
3. 用手机微信扫描终端二维码（或打开 PNG 图片扫码）并确认
4. 扫码成功后，插件会提示你用微信**给 bot 发一条消息**（这一步让网关生成会话凭据，bot 才能反向联系你）
5. 收到你的消息后，插件会自动：
   - 在会话中显示连接状态（与 `/wx-status` 相同的内容）
   - 通过 ClawBot 给你发一条微信消息，告诉你已连接成功
   - 请 AI 用 `question` 工具问你一个问题来测试通知：这次等待超时临时缩短为 **10 秒**，你不回答就能马上在微信收到提醒（测试结束自动恢复默认 5 分钟；若 3 分钟内测试没有开始，也会自动恢复默认）
6. 如果 3 分钟内没有给 bot 发消息，插件会提示你稍后补发并运行 `/wx-status` 检查

之后插件会在后台长轮询，保持会话凭据新鲜。

## 配置

通过 `opencode.jsonc` 的插件 options 配置（均为可选）：

```jsonc
{
  "plugins": [
    {
      "package": "@laxture/opencode-wx-clawbot-notifier",
      "options": {
        "timeoutMs": 300000,                    // 超时毫秒数，默认 5 分钟
        "tools": ["question"],                  // 监听的工具名列表
        "accountFile": "~/.opencode/wx-clawbot/account.json",
        // "toUser": "o9cq800kvzLUYAs0ALz_IT0McuWc@im.wechat",  // 固定收件人（真实的 @im.wechat id）；不填则发给所有给 bot 发过消息的用户
        "enabled": true
      }
    }
  ]
}
```

| 选项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `timeoutMs` | number | `300000` | 超时阈值（毫秒） |
| `tools` | string[] | `["question"]` | 监听的工具名；V2 内置人工介入工具是 `question`（V2 已无独立 `confirm` 工具） |
| `accountFile` | string | `~/.opencode/wx-clawbot/account.json` | 微信凭据存储位置 |
| `toUser` | string | 无 | 固定收件人；不填则发给所有已知用户。**必须填真实的 `xxx@im.wechat` id**：占位 id（如 `someone@im.wechat`）会让网关返回 `ret=-3 invalid arguments`，通知静默发不出去 |
| `enabled` | boolean | `true` | 关闭插件 |

## 命令

| 命令 | 作用 |
| --- | --- |
| `/wx-login` | 扫码登录微信 ClawBot，并引导完成激活、连接通知与超时通知测试 |
| `/wx-status` | 查看登录状态、收件人、超时阈值、监听工具 |

## 限制与说明

- **V2 没有内置 `confirm` 工具**：OpenCode V2 的内置人工介入工具只有 `question`（`confirm` 是 V1 的产物）。如果你的 agent 自定义了 confirm 类工具，把名字加进 `tools` 配置即可。
- **登录二维码会以会话消息呈现**：`/wx-login` 生成的二维码以用户消息形式写入当前会话（完整显示），会话 agent 会看到该消息并可能回应；状态变化则以一行通知呈现。
- **必须先有会话**：微信策略要求用户先给 bot 发过消息，bot 才能反向发消息。
- **长时间静默后会话凭据会过期**：如果一段时间没有在微信上给 bot 发消息，网关的会话凭据（`context_token`）会过期，通知发送会失败并在会话中提示 `prepare failed`；此时在微信上给 bot 发一条消息即可恢复，无需重新登录。注意：已失败的通知不会自动补发，需要重新触发发送。
- **只支持私聊**：目前只向私聊用户发送，群聊消息仅用于更新凭据。
- **通知是单向的**：本插件只负责「催你回终端」，不支持在微信里回答问题（那需要完整的双向桥接，见参考项目）。

## 本地开发

```sh
bun install
bun run typecheck
bun test
bun run build     # 产出 dist/index.js + d.ts
```

本地加载（V2 支持直接挂目录）：

```jsonc
{
  "plugins": ["./path/to/opencode-wx-clawbot-notifier"]
}
```

## 参考

- [opencode-wechat-plugin](https://github.com/Ikaros12643/opencode-wechat-plugin)：微信 ClawBot 连通方案（仅适配 opencode 1.0，本项目取其协议层并重写为 V2）
- [OpenCode Plugins 文档](https://opencode.ai/docs/build/plugins)

## License

MIT
