# opencode-step-pause

> 每 N 步自动在对话里汇报一次进度，说完立刻继续。
> 不占额外回合、不等你回复、不生成进度文档。

这是 [`cxv117793-blip/dsh-step-pause`](https://github.com/cxv117793-blip/dsh-step-pause) v0.4.9（MIT）的 OpenCode V2 移植版。核心机制、提示词、完成判定和自动续跑刹车都来自原项目，按 OpenCode V2 的插件接口重写。

- 目标版本：OpenCode `2.2.x`（在 `2.2.1` 类型定义、`2.2.4` 真机上验证）
- 状态：`0.1.0`，MVP
- 不包含：GUI 设置页、统计面板、多语言、V1 兼容

---

## 它做什么

长任务跑到第 20、40 步时，模型会主动停下来写几行：

```text
1. 正在做什么：给设置页补上表格导出的失败重试
2. 已完成什么：定位到 retry 没有重置 backoff；改了 3 处；单测补了 2 组
3. 接下来做什么：跑全量测试，然后提交
4. 卡点：无
```

然后**在同一条回复里**继续调用工具。检查点不会变成新的用户回合，也不会写进会话历史。

如果模型在检查点后只写了文字就停下，插件可以在轮次关闭前塞一条续跑提示，把它拉回来继续；次数有硬上限。

---

## 安装

### 1. 放到本地目录

```bash
git clone https://github.com/tkhs101/opencode-step-pause.git ~/opencode-step-pause
cd ~/opencode-step-pause
npm install
```

### 2. 在 `opencode.json` 里注册

```json
{
  "plugins": [
    {
      "package": "/home/you/opencode-step-pause",
      "options": {
        "everyNSteps": 20
      }
    }
  ]
}
```

`package` 使用绝对路径。改完后重启 OpenCode（或重新加载插件）。

### 3. 验证

把 `debug` 打开，运行一个多步任务：

```json
{
  "plugins": [
    {
      "package": "/home/you/opencode-step-pause",
      "options": {
        "everyNSteps": 2,
        "debug": true
      }
    }
  ]
}
```

调试日志会写到系统临时目录下的 `opencode-step-pause.log`（通常是 `/tmp/opencode-step-pause.log`），可用环境变量 `OPENCODE_STEP_PAUSE_DEBUG_FILE` 指定其他路径。日志里能看到 `context` / `inject` / `resume` 等事件；对话里会在第 2、4、6… 步出现进度小结。

---

## 配置

所有字段都在 `plugins[].options` 里，保存后重启生效（当前 MVP 没有热更新）。

| 键 | 默认 | 说明 |
|---|---|---|
| `enabled` | `true` | 总开关 |
| `everyNSteps` | `20` | 每多少步汇报一次，实际生效范围 `2–500`；写 `1` 会被夹成 `2` |
| `maxReportsPerTurn` | `0` | 每轮最多汇报几次，`0` 表示不限制，上限 `1000` |
| `prompt` | 内置 | 注入的提示词，支持 `{{step}}` `{{every}}` `{{turn}}` |
| `mainAgentOnly` | `true` | 只在主智能体里汇报，子智能体不汇报 |
| `autoResume` | `true` | 检查点后纯文字停下时，自动续跑 |
| `maxAutoResumesPerTurn` | `2` | 每轮最多自动续跑几次；`0` 等于关闭 |
| `debug` | `false` | 输出插件调试日志 |

示例：

```json
{
  "plugins": [
    {
      "package": "/home/you/opencode-step-pause",
      "options": {
        "everyNSteps": 10,
        "maxReportsPerTurn": 6,
        "mainAgentOnly": true,
        "autoResume": true,
        "maxAutoResumesPerTurn": 1
      }
    }
  ]
}
```

---

## 工作原理

OpenCode V2 的 `context` hook 在每次模型请求前运行，拿到的是**本次请求的消息数组**。插件向这个数组插入一条 user 消息，模型在同一次请求里就能看到；这条消息不会被持久化，所以不会污染后续会话。

### 步数怎么算

一个“逻辑轮次”从最后一条真实用户消息开始。插件同时维护三个计数：

1. **L1（主计数）**：`turnKey` 之后、`event.messages` 里的 assistant 消息数。
   - `turnKey` 是真实用户消息的 ID，不是“最近一条 user-role 消息”。
   - 因此 compaction、shell、skill 等 user-role 消息不会把计数打断。
2. **L2（修正）**：`session.step.ended` 事件里唯一的 `assistantMessageID`。
   - 事件流可能比下一次 `context` hook 晚几毫秒，所以 L2 只做修正。
3. **L3（回合识别）**：对新出现的 user-role 消息调用 `session.context()` 查真实类型。
   - 只有 `type === "user"` 才重置轮次。
   - 查询失败时保守地按真实用户消息处理。

最终：

```text
completed = max(L1, L2)
currentStep = completed + 1
```

第一次看到某个 session（或插件重载）时，会从消息记录回填 L1/L2，并把历史 assistant ID 标记为已计数，避免延迟事件重复计数。

### 自动续跑

只在以下条件**全部**满足时续跑：

- 本轮刚在注入检查点的那一步（或上一次续跑后的那一步）结束；
- 每轮续跑次数未超过 `maxAutoResumesPerTurn`；
- 没有后台任务在跑；
- 主智能体；
- 最后一条 assistant 消息是**纯文本**，不含 tool call；
- 没有明确写“任务已完成”；
- assistant 消息不是错误、不是空文本。

任何一条不满足就放手，让轮次正常结束。续跑通过 `ctx.session.synthetic({ resume: true, delivery: "steer" })` 注入，不传 `description`，所以时间线里不会出现额外的续跑条目。

### 完成判定

完成判定沿用原项目的保守启发式：

- 认“任务已完成 / 全部完成 / all done”等明确标记；
- 排除“已完成 5/8”“还剩 3 个”“尚未完成”等进度或否定语义；
- 排除“任务已完成。接下来继续创建 t4.txt”这类仍在继续的表述；
- 开头宣告和结尾宣告分开判断，因为模型通常先给结论再列细节。

不确定时**不续跑**。

---

## 与 DSH 版的差异

| 能力 | DSH v0.4.9 | 本移植 |
|---|---|---|
| 注入位置 | `agent/pre-step` 决策 | `context` hook 的 `event.messages` |
| 注入持久化 | 可配置是否显示 | 永不持久化，只影响本次请求 |
| 步数 | 宿主提供的 `payload.step` | L1 + L2 + L3 组合计数 |
| 自动续跑 | `agent/turn-stopping` + `steer` | `experimental.idle` + `synthetic` |
| 子智能体判定 | agent registry | `session.parentID && !session.fork` |
| 设置页 / 统计 / 多语言 | 有 | 无（MVP 范围外） |
| V1 兼容 | 不适用 | 无 |

---

## 已知限制

- `experimental.idle` 是实验性 hook。注册失败时插件仍会注入检查点，只是不自动续跑。
- 主智能体判定依赖 `session.get`。读取失败时会保守地跳过当前步骤（宁可不汇报，也不污染子智能体），下一步会重试。
- 如果宿主在两次请求之间丢失了原始用户消息（例如极端 compaction），L1 会退回 L2；L2 可能少算一步，插件会选择保守分支，不强行续跑。
- 自动续跑是启发式，不是语义理解。它只在“检查点后纯文本停下”这一种形态下工作。
- 当前没有 GUI 设置页，改配置需要编辑 `opencode.json` 并重启。
- 只在 OpenCode `2.2.x` 上验证；V1 不兼容。

---

## 开发

```bash
npm install
npm run typecheck
npm test
```

测试覆盖：

- 配置默认值、类型解析与夹取；
- L1/L2/L3 计数、回合重置、compaction 保持、事件去重；
- 完成判定与六道续跑刹车；
- 注入不落库、同一步去重、每轮上限、子智能体跳过、fork 放行、会话类型读取失败时保守跳过；
- idle 异常不会破坏执行、后台任务期间保留检查点、idle 后清理状态但保留轮次号；
- debug 文件日志。

### 真机验证

真机结果（检查点、自动续跑、subagent、fork）见 `VALIDATION.md`。下面是最小复现步骤：

```bash
mkdir -p /tmp/step-pause-it
cd /tmp/step-pause-it
cat > opencode.json <<'JSON'
{
  "model": "opencode/deepseek-v4.1-flash-free",
  "plugins": [
    {
      "package": "/home/you/opencode-step-pause",
      "options": { "everyNSteps": 2, "debug": true }
    }
  ]
}
JSON
opencode run --auto "Read a.txt, b.txt, c.txt, d.txt, e.txt one at a time, one tool call per response, then write summary.txt."
```

预期：

- 第 2、4 步出现进度小结；
- 小结后模型继续调用工具；
- 若模型在检查点后纯文字停下，idle 日志出现 `resume`，随后继续执行；
- 会话历史里没有注入的提示词原文。

---

## 许可证与致谢

MIT。核心设计、提示词、完成判定与自动续跑规则来自：

- [`cxv117793-blip/dsh-step-pause`](https://github.com/cxv117793-blip/dsh-step-pause) v0.4.9，MIT，Copyright (c) 2026 dsh-step-pause contributors

OpenCode 插件接口参考了 OpenCode 内置 `goal` 插件的 `context` / `experimental.idle` / `synthetic` 用法。
