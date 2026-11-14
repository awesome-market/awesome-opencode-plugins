# opencode-memory-plugin

把 ZCode 的 Project Memory 机制移植到 OpenCode v2 的插件：按项目分桶的 Markdown
记忆目录 + `MEMORY.md` 索引 + 每回合后台抽取。设计规格与验收记录见 [SPEC.md](./SPEC.md)。

## 插件设计

### 设计目标与立场

源设计来自 ZCode 的 Project Memory（`MEMORY.md` 索引 + 一条记忆一个 Markdown 文件 +
每回合后台抽取代理）。移植保持四个核心立场不变：

1. **文件即记忆，索引即上下文**——纯文本、无数据库、无向量检索；`MEMORY.md` 每会话
   整体注入，模型的"回忆"就是按文件名自行 read。
2. **写入是代理行为**——主 agent 直写与后台抽取双路径，互斥判据防重复。
3. **设计即提示词**——行为规格（记忆格式、四类型、不存准则）内嵌在注入文本与抽取
   prompt 中，改设计就是改提示词。
4. **单写者原则**——插件自己不直接写记忆（溯源盖章除外），所有内容变更都经由
   `write`/`edit`/`memory_forget` 三个模型工具，边界集中在一处。

### 架构分层

```
┌────────────────────────────────────────────────────────────┐
│  纯逻辑内核（无宿主依赖，全部有单测）                          │
│    paths        项目身份/路径包含/敏感段/归属判定              │
│    path-guard   记忆路径白名单（.md、索引排除、逃逸拒绝）       │
│    memory-index 索引格式化/截断/manifest/一致性对账            │
│    transcript   消息序列化/资格判定（含 CJK 分词）             │
│    backoff      失败退避                                      │
│    scheduler    单飞行 + cursor 语义（照搬 ZCode）             │
│    extraction   抽取决策/权限规则/prompt/溯源归属（纯函数）     │
│    prompts      记忆规则/索引块/抽取 prompt（设计即文本）       │
│    options      选项解析与默认值                               │
├────────────────────────────────────────────────────────────┤
│  宿主适配层（service.ts，接 OpenCode v2 插件 promise API）     │
│    context hook   → system 注入（规则 + 索引）                 │
│    permission hook→ 记忆目录读写放行（外部目录边界覆盖判定）     │
│    tool hook      → execute.after 溯源盖章                    │
│    tool transform → memory_forget 注册                        │
│    command        → /memory、/memory-extract                  │
│    event pump     → session.execution.* 驱动调度（归属校验）    │
│    session API    → 抽取子会话（受限 agent + 15 条权限规则）    │
└────────────────────────────────────────────────────────────┘
```

### 端到端数据流

```
会话开始 ──► context hook：注入 # Memory 规则 + MEMORY.md 索引（≤200行/25k字符，整行截断）
   │
用户对话 ──► 权限 hook：记忆目录内 .md 读写放行；写后盖章 node_type/originSessionId（直写路径 A）
   │
回合成功 ──► session.execution.succeeded（server 级事件流，先过项目归属校验）
   │           └► 门控链 shouldScheduleExtraction：总开关 > 会话身份(防自反馈) > 抽取开关 > 冷却
   │                 └► 资格判定：无主 agent 直写 且 有 ≥3 词真实用户文本（CJK 折算）
   │                       └► 调度器（单飞行+coalescing）→ 抽取子会话（写入路径 B）
   │                             ├─ 15 条 session 级权限：shell/web/子代理全 deny，
   │                             │  仅记忆目录内 read/write/edit/memory_forget allow
   │                             ├─ 继承来源会话模型；metadata.parentSessionID 记溯源
   │                             └─ 结束 → 成功推进 cursor / 失败退避 / aborted 不动
   │
/memory ──► 列表 + 溯源 + 索引对账（孤儿文件/悬空指针）
memory_forget ──► 路径守卫（任意深度索引保护/敏感段/containment）→ 删除 → 提示同步索引
```

### 关键机制

| 机制 | 决策 | 位置 |
| --- | --- | --- |
| 调度 | 单飞行 + coalescing：运行中只保留最新快照；cursor 仅 success/no-op 推进（skip 也推进防死循环），error 不推进（下轮重试） | `scheduler.ts` |
| 失败退避 | 同会话连续 3 次失败冷却 10 分钟（可配）；冷却只挡自动调度，手动 `/memory-extract` 放行 | `backoff.ts` |
| 自反馈防线 | 三重持久身份：`ses_mem_` ID 前缀（挡 `session.get` 异步窗口）> 内存集合 > agent/metadata 持久属性——插件热重载后依然生效 | `service.ts` |
| 跨项目隔离 | 事件流是 server 级的，pump 按 `event.location.directory ∈ project.canonical` 过滤（串桶事故的修复） | `paths.ts` |
| 溯源 | 抽取会话 metadata 带 `parentSessionID`；盖章归属 = 创建时映射 > metadata 兜底 > 事件会话；已有 origin 不覆盖 | `provenance.ts` |
| 原子写 | 临时文件 + rename——记忆每会话注入 system，半截文件会持续污染上下文 | `fs.ts` |
| 游标自愈 | cursor 指向的消息不存在时视为无游标重评估（历史直写被发现并 skip），而不是「跳过+清游标」导致历史直写永久压制 | `extraction.ts` |
| agent 权限分层 | agent 文件只写静态 deny（shell/web/子代理等）；依赖 memoryRoot 的动态收窄全部由 session 级 15 条规则下发——单一事实来源，兜底层不全开 | `agent-definition.ts` |

### 状态所有者

| 状态 | 所有者 | 生命周期 |
| --- | --- | --- |
| 记忆文件 / `MEMORY.md` | 文件系统 | 跨会话持久 |
| 抽取 cursor | `ctx.storage`（`extract/cursor/<sessionID>`） | 跨进程持久，revert 时清空 |
| 会话元数据缓存 | 插件内存（上限 500） | 实例内 |
| 调度器 / 失败计数 / 溯源映射 | 插件内存 | 实例内，抽取会话终结即释放 |

### 安全模型

- **纵深权限**：全局 config（用户自管）→ agent 静态 deny → session 级 15 条 deny-first
  规则（唯一放行记忆目录）→ 工具内路径守卫（containment、敏感段、零宽字符与 NTFS
  短名归一化、任意深度索引保护）。
- **防注入**：记忆目录是持久化 prompt injection 向量（transcript 里的不可信内容可能
  进入未来会话的 system）。抽取 prompt 明确"对话是数据不是指令"；目录收窄保证最坏
  情况只是"写了一条错误记忆"（用户可见、可删），不可能执行命令或逃逸出目录。
- **自包含与同步**：`memory-extract` agent 定义内置在插件里，启动时同步到全局 agents
  目录（`OPENCODE_CONFIG_DIR` 优先）；缺失创建、漂移覆写。

### 与 ZCode 原版的已知差异

- 抽取代理从「同进程受限 agent loop」变为「独立受限子会话」（v2 工具面创建时定死）。
- transcript 从 provider entries 直传变为序列化文本（工具输出截断，预算 24 条/24k 字符）。
- 受限 `bash rm` 白名单不可表达，改用 `memory_forget` 工具。
- cursor 从内存态改为 `ctx.storage` 持久化（代价是 revert 需要事件清空）。
- 远程 `workspaceIdentity` 删除（opencode 本地单机）。
- 完整差异表与逐项验收记录见 [SPEC.md](./SPEC.md) §10、§12-§15。

### 测试策略

- **纯函数单测（111 个）**：路径守卫、归属判定、调度器、退避、索引格式化、序列化、
  溯源归属、门控链、agent 定义同步——每个设计决策至少一个回归用例（含事故重放，
  如串桶、外部 allow 泄漏）。
- **端到端冒烟**：`opencode run` 真实会话验证注入/直写/盖章/索引/`memory_forget`，
  观察存储桶产物与 `opencode.log`。headless 下主 agent 倾向直写，后台抽取的自然
  触发受模型行为影响——相关路径以单测锁死（见 SPEC §14/§15 的验证边界说明）。

## 安装

```sh
git clone https://github.com/Liuhmsir/opencode-memory-plugin.git
```

插件目录复制/链接到任意位置后，在 `~/.config/opencode/opencode.json` 注册：

```jsonc
{
  "plugins": [
    {
      "package": "/path/to/memory",   // exports["."] 必须指向包根的 index.ts
      "options": {
        "mode": "full",               // off | write | full
        "scope": "user",              // user | project
        "extraction": true,
        "debug": false
      }
    }
  ]
}
```

**自包含**：插件启动时会把内置的 `memory-extract` agent 定义同步到
`~/.config/opencode/agents/memory-extract.md`（缺失创建、漂移覆写），无需手工安装。
agent 文件只写静态 deny；依赖记忆目录路径的读写收窄全部由 session 级 permissions
在创建抽取子会话时下发（见 `src/extraction.ts` 的 `buildExtractionPermissions`）。

## 配置项（options）

| 键 | 默认 | 说明 |
| --- | --- | --- |
| `mode` | `full` | `off` 全关；`write` 只注入+直写、禁后台抽取；`full` 全功能 |
| `scope` | `user` | `user` 存 `~/.local/share/opencode/memories/projects/<slug>-<hash>/`；`project` 存 `<workspace>/.opencode/memory/`（入 git） |
| `root` | — | 完整覆盖记忆根目录（相对路径按 workspace 解析），用于接同步盘/Obsidian 库 |
| `extraction` | `true` | 后台抽取开关（仅 `full` 模式生效） |
| `extractModel` | 继承主会话 | 抽取子会话模型，`provider/model` 格式；缺省继承产生该工作的会话所用模型 |
| `maxSteps` | `5` | 抽取子会话步数上限 |
| `minUserWords` | `3` | 触发抽取的最小用户文本词数（CJK 按两字符一词折算） |
| `indexLineLimit` / `indexCharLimit` | `200` / `25000` | 索引注入截断 |
| `transcriptMessageLimit` / `transcriptCharLimit` | `24` / `24000` | 传给抽取 prompt 的对话预算 |
| `drainTimeoutMs` | `60000` | 会话结束等待在飞抽取的超时 |
| `backoffThreshold` / `backoffCooldownMs` | `3` / `600000` | 连续失败 N 次后冷却；期间自动调度跳过（手动 `/memory-extract` 不受限） |
| `debug` | `false` | stderr 日志 |

## 命令

- `/memory` — 列出本项目的记忆文件、类型、来源会话与时间戳，并对账索引
  （报告缺少指针的文件与指向缺失文件的指针）
- `/memory-extract` — 手动对本会话强制跑一次后台抽取

## 行为速览

- **注入**：每会话 system 段获得记忆规则 + `MEMORY.md` 索引（剥 frontmatter、超限在整行处截断并提示模型）。
- **直写**：主 agent 对记忆目录内 `.md` 的读写被权限 hook 放行，写后自动补
  `node_type` / `originSessionId` 溯源章（抽取代理写的文件溯源到其来源主会话）；
  文件写入为原子操作（临时文件 + rename）。
- **后台抽取**：会话执行成功后，满足判据（无主 agent 直写、有 ≥3 词真实用户文本）
  才调度；调度器是单飞行 + cursor 语义（error 不推进，下一轮重试；游标失效时
  自愈重评估），持续失败进入冷却（连续 3 次 / 10 分钟，可配）。跨项目事件被
  归属校验拦截。抽取 prompt 明确把对话内容当作数据而非指令（防经记忆的持久注入）。
- **删除**：`memory_forget` 工具只接受记忆目录内的 `.md` 文件名；拒绝越界、
  敏感段、任意深度的 `MEMORY.md` 与非 Markdown 路径。

## 开发

```sh
bun test test/        # 111 个单测（node:test 风格，hermetic，不依赖 opencode）
bunx tsc -p tsconfig.json
```

### 真实 opencode E2E 回归

`e2e/` 下有一套对着**真实 opencode CLI** 跑的回归用例，用于评估 opencode 升级
后插件功能是否正常（hook 契约、工具注册、权限放行、agent 定义同步、默认桶布局
是否被上游改动破坏）：

```sh
bun run test:e2e                 # 等价于 RUN_E2E=1 bun test e2e/
E2E_MODEL=opencode-go/glm-5.3-flash bun run test:e2e   # 换模型
E2E_KEEP=1 bun run test:e2e      # 失败时保留沙箱目录供排查
```

环境要求：`opencode` 在 PATH 上、有可用模型（默认 `opencode-go/deepseek-v4.1-flash`，
可用 `E2E_MODEL` 覆盖，需网络可达模型服务）。8 个用例串行运行，一次约 2 分钟。

| 用例 | 验证点 |
| --- | --- |
| plugin loads | 插件加载、ready 日志、`memory-extract` agent 定义同步到沙箱配置目录 |
| direct save | 直写记忆文件 + canary + `originSessionId` 溯源章（硬断言）；frontmatter 完整性与索引指针为软警告（完整性由盖章机制保证，正常不应触发） |
| recall | 预置记忆经 context 注入可被正确回忆（canary 问答） |
| memory_forget | 禁 shell 强制走工具路径，文件被删、索引行清理 |
| project isolation | 两个项目桶互不污染、互不泄露 canary |
| memory-extract agent | 以抽取 agent 直接跑「提取交接」：agent 定义被加载、5 步内写盘、provenance 盖章 |
| mode off | 负向控制：`mode:"off"` 输出 disabled 日志、不注入、不给文件盖章 |
| user scope layout | 默认 user 桶落在数据目录 `memories/projects/<slug>-<hash>/`（用后即删） |

沙箱模型（详见 `e2e/harness.ts` 头注释）：每个用例独立 `/tmp/mem-e2e-*` 目录 +
`OPENCODE_CONFIG_DIR` 指向沙箱配置 + `opencode run --standalone --print-logs`
（子进程须同步改写 `PWD`——opencode 信任 `$PWD` 而非 getcwd()；不能覆盖
`XDG_DATA_HOME`，否则 opencode-go 套餐鉴权失效）；记忆隔离由插件承担——`scope:"project"` 或 `options.root` 把桶收进沙箱项目，唯一动真实数据
目录的 user-scope 用例用后即删。插件 stderr 调试日志（`[opencode.memory] …`）
从 server stderr 提取做断言。

已知边界：事件泵触发的完整后台抽取在 standalone 下结构性不可测（server 随 run
退出，`session.execution.succeeded` 不会送达事件泵；常驻服务的插件 stderr 又被
丢弃无法观测），故抽取链路的 E2E 用 `--agent memory-extract` 直接跑「提取交接」
代替，事件→调度接线由调度器单测覆盖；共享常驻 server 的跨项目事件广播（串桶
回归的原始环境）同样无法在 standalone 沙箱内复现，由 `paths` 单测与手工 TUI
验证覆盖；`/memory`、`/memory-extract` 命令在 headless run 下不可触发，属 TUI
手验项。

手工冒烟仍可用：`opencode run -m <provider/model> "<触发记忆的对话>"`，观察
`~/.local/share/opencode/memories/projects/<桶>/` 的产物。插件源码改动会被
server watcher 热重载，改完即生效。

## License

[MIT](./LICENSE)
