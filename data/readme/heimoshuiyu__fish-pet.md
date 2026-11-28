# fish-pet 🐟

**中文** | [English](#english)

## 中文

OpenCode V2 桌面宠物插件：一条跟随会话状态的大肥鱼（吃白饭、碎碎念、看你干活、庆祝/沮丧），窗口内渲染，移植自 DSH 的 dsh-pet（大肥鱼）。双半架构：server 是脑，窗口只做展示。

### 安装

```bash
opencode plugin add opencode-fish-pet
```

或 opencode.json：

```jsonc
"plugins": [
  "opencode-fish-pet",
  // 可选：余额六档（BYO key，每 30 分钟自查一次）
  { "package": "opencode-fish-pet", "options": { "balance": {
      "deepseek": { "apiKey": "sk-…", "total": 50 },
      "custom": [ { "name": "中转站", "url": "https://…/balance", "headers": { "Authorization": "Bearer …" }, "path": "data.remaining", "total": 100 } ]
  } } }
]
```

注意：
- 需要 OpenCode ≥ 2.0；GUI 插件通道为 experimental，宿主大版本升级后可能要求更新本插件
- 桌面/Web 窗口可见；TUI 端无鱼（GUI 插件不进终端，属预期）
- 鱼的碎碎念/对话会创建一个普通 OpenCode 会话（标题 🐟 fish-pet 对话），走你自己配置的模型计费
- 右键鱼有完整菜单：睡觉、多开、开聊、待办、余额、碎碎念、起名、重置鱼脑、通知开关、大小/归位等
- 桌面端 `Settings → Extensions → Plugins` 可关

### 行为速览

- **109 段动画**：五分类随机池（小动作 / 玩耍 / 吃什么 / 时节 / 文字），点击 5 种回应，拖拽/抛掷/双击弹弓，多开互撞
- **工作状态机**：聚合所有运行中会话（thinking/working/result/waiting），最近 90s 工具调用折叠成一句话随气泡显示（如「干活中 · 跑命令×3」）
- **完成庆祝**：前台会话收官全量庆祝，后台完成冒气泡不抢动画；子代理完成静默
- **碎碎念**：每 5 分钟随口一句（10 分钟无观众则沉默；右键可总开关），带时间背景——它知道今天星期几、快到什么节日、外面天气如何；睡觉时说梦话
- **待办**：`@2026-11-20 15:00` / `@18:30` / `@2h` 截尾定截止，越近提醒越密
- **多开**：鱼 0 演聚合状态，其余各绑一个运行中会话
- **面板聊天**：Fish 标签页直接对话，发送即有"正在琢磨"反馈、逐字流式回复；可给鱼起名字（面板标题随之变化）
- **语言**：右键菜单 → 语言 直选（English / 中文 / 日本語；默认 English），UI、鱼的台词与提示词全链路切换

### 包结构

| 文件 | 角色 |
|---|---|
| `index.ts` | server 脑（入口 `.`） |
| `rpc.ts` | server ↔ 窗口的 JSON-Schema 契约（入口 `./rpc`） |
| `gui-experimental.cjs` | 前端渲染器 bundle（入口 `./gui-experimental`，CJS，~28MB 含内嵌资产） |

源码、资产管线与开发循环见仓库：<https://github.com/heimoshuiyu/fish-pet>（`DEVELOPMENT.md`）。

### 致谢与素材条款

- 社区作品，与 OpenCode / DeepSeek Harness 无关联
- 动画链/物理等部分代码与全部动画、音效源自 dsh-pet（PC2005-cloud）：代码 MIT（LICENSE 内已保留其版权行）；**素材禁止商用**，公开渠道分发须署名 https://github.com/PC2005-cloud/dsh-pet —— 本包据此标注 `SEE LICENSE IN LICENSE`（代码 MIT + 素材条款，详见 LICENSE）

---

## English

An OpenCode V2 desktop pet plugin: a chubby freeloader fish that follows your coding sessions (munching, muttering, watching you work, celebrating/moping). Rendered in-window; ported from dsh-pet (DSH). Two halves: the server is the brain, windows only present.

### Install

```bash
opencode plugin add opencode-fish-pet
```

or in opencode.json:

```jsonc
"plugins": [
  "opencode-fish-pet",
  // optional: six-tier balance meter (BYO keys, self-checked every 30 min)
  { "package": "opencode-fish-pet", "options": { "balance": {
      "deepseek": { "apiKey": "sk-…", "total": 50 },
      "custom": [ { "name": "relay", "url": "https://…/balance", "headers": { "Authorization": "Bearer …" }, "path": "data.remaining", "total": 100 } ]
  } } }
]
```

Notes:
- Requires OpenCode ≥ 2.0; the GUI plugin channel is experimental — major host upgrades may require updating this plugin
- Visible in desktop/web windows; no fish in the TUI (GUI plugins don't run in the terminal, by design)
- The fish's muttering/chat creates a normal OpenCode session (titled 🐟 fish-pet chat) billed to your own model
- Right-click the fish for the full menu: sleep, more fish, chat, to-dos, balance, murmur, naming, brain reset, notification toggle, size/position, and more
- Toggle it off in `Settings → Extensions → Plugins` on desktop

### Behavior at a glance

- **109 animations**: five weighted random pools (small moves / play / eating / seasonal / text), 5 click reactions, drag/throw/slingshot, multi-fish collisions
- **Work state machine**: aggregates all running sessions (thinking/working/result/waiting); the last 90s of tool calls fold into one line on the bubble (e.g. "Working · commands ×3")
- **Completion**: full celebration when the foreground session finishes, unobtrusive bubbles for background completions; subagent completions stay silent
- **Muttering**: one line every 5 minutes (silent without an audience for 10 min; right-click to toggle), with time context — it knows the day, upcoming holidays and the weather outside; sleep-talks while asleep
- **To-dos**: due times via an `@2026-11-20 15:00` / `@18:30` / `@2h` suffix; reminders escalate as the deadline approaches
- **Multiple fish**: fish #0 plays the aggregate state, the rest each bind to a running session
- **Panel chat**: talk to the fish in the Fish tab with instant "thinking" feedback and word-by-word streaming; name it and the tab title follows
- **Language**: right-click → Language (English / 中文 / 日本語; default English) switches UI, the fish's speech and prompts end to end

### Package layout

| File | Role |
|---|---|
| `index.ts` | server brain (entry `.`) |
| `rpc.ts` | JSON-Schema contract between server and windows (entry `./rpc`) |
| `gui-experimental.cjs` | renderer bundle (entry `./gui-experimental`, CJS, ~28MB with embedded assets) |

Source, asset pipeline and dev loop live in the repo: <https://github.com/heimoshuiyu/fish-pet> (`DEVELOPMENT.md`).

### Credits & asset terms

- Community project; not affiliated with OpenCode or DeepSeek Harness
- The animation chain/physics code and all animations and sounds derive from dsh-pet (PC2005-cloud): code is MIT (its copyright line is preserved in LICENSE); **assets may not be used commercially**, and public redistribution requires attribution to https://github.com/PC2005-cloud/dsh-pet — hence the package is marked `SEE LICENSE IN LICENSE` (MIT code + asset terms, see LICENSE)
