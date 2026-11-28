# @te-river/opencode-alibabatokenplan

**Token Plan 优惠雷达 · 仪表盘优先**（opencode server + TUI 双入口插件）：装上后打开
**http://127.0.0.1:7777** 即得一块可随时查看的本地仪表盘 —— 错峰窗口倒计时（HH:MM:SS 每秒跳动）、
Qoder Credits 在卖/生效倍率总表、百炼 ¥ 价目（峰/谷）、免费额度与政策、实时额度进度条。
数据 = 百炼目录三级回退（live→本机 bl CLI→内置快照）+ Qoder 静态快照（2026-08-31），
合并后原子持久化到 `status.json`；边界翻转与启动摘要走 toast，无需任何命令。

> 💠 **把仪表盘钉成无边框小窗**（推荐贴屏幕角落常驻）——「运行」或终端执行：
>
> ```
> start msedge --app=http://127.0.0.1:7777 --window-size=430,900
> ```
>
> （端口若漂移，面板页脚「钉为独立小窗」区显示的就是当前实际端口的完整命令，点一下即复制。
> 也可配 `"dashboard": { "autoOpen": true }` 让插件启动时自动探测本机 Edge 开此小窗。）

```
┌ Token Plan 优惠雷达（sidebar_content · order 160）────────┐
│ ● Token Plan 优惠雷达   [实时接口 + Qoder快照08-31] [刷新] │
│ ▸ 错峰 5 折（22:00–08:00）[Qoder Credits]  优惠进行中      │
│   距结束 03:47:12  ▓▓▓▓▓▓░░░░                              │
│   qwen3.8-max  0.5x → 0.25x  错峰 5 折 [双源印证] ↗        │
│ 在卖倍率总表   qwen3.8-flash 0.1x · kimi 0.3x(highspeed…) │
│ 限时           preview 0.1x · glm-5.3-flash 0.05x …        │
│ 百炼价目(¥)    deepseek-v4-pro-0813 峰/谷 2250/1125 …      │
└────────────────────────────────────────────────────────────┘
```

TUI 终端内仍保留 sidebar/home 常驻摘要（opencode 终端版）；两者同吃
`~/.cache/opencode/alibabatokenplan/status.json`。

## 安装（两行手工注册）

`~/.config/opencode/opencode.jsonc` → `"plugin"` 数组追加一条：

```jsonc
// ~/.config/opencode/opencode.jsonc  →  "plugin": [ …原有条目…, "@te-river/opencode-alibabatokenplan@latest" ]
```

`~/.config/opencode/tui.json` → `"plugin"` 数组追加**同一字符串**：

```json
// ~/.config/opencode/tui.json        →  { "$schema": "https://opencode.ai/tui.json",
//   "plugin": [ "@slkiser/opencode-quota@latest", "@te-river/opencode-alibabatokenplan@latest" ] }
```

无 postinstall 魔法；两个入口都吃同一份 `~/.cache/opencode/alibabatokenplan/status.json`。

仪表盘默认开启（`http://127.0.0.1:7777`）；想钉成无边框小窗：`start msedge --app=http://127.0.0.1:7777 --window-size=430,900`（或配 `"dashboard": { "autoOpen": true }` 自动探测本机 Edge）。

## 数据源与隐私声明

- **百炼目录三级回退（零登录）**：公开控制台匿名接口（live）→ 本机 `bl model list`（cli）→ 随包内置快照（snapshot）。
  实时额度可选走 `bl usage token-plan`（需 `bl auth login --console --console-site domestic`）。
- **Qoder 数据 = 2026-08-31 静态快照**：全部优惠规则/倍率以常量形式内嵌（`src/core/qoder-snapshot.ts`），
  **不调用任何 Qoder 私有端点**（包内 0 处相关 fetch 代码）；展示一律带「截至 2026-08-31」标注，
  过期公告位会显示「快照可能失效」。快照更新流程：修订该文件 → `npm run build && npm test` → 重发版。
- 两套单位（Qoder Credits 倍率 / 百炼 ¥ 价格倍率）**永不互算**，各居其 facet；仅 (模型,窗口,倍率,单位)
  全等才合并为「双源印证」行。1 元 = 250 Credits 仅为展示换算注记（据百炼计费示例验证，非官方汇率）。
- 与旧版 `bailian-discount-panel.ts` 兼容：`bailian_discounts` 工具保留（委托到新名
  `tokenplan_discounts`）；旧缓存 `~/.cache/opencode/bailian-discount-cache.json` 首启自动迁移。

## 配置（可选）

`~/.config/opencode/alibabatokenplan/config.jsonc`（server + TUI 同读；缺失/坏 = 全默认）：

```jsonc
{
  "webpanel": { "enabled": true, "port": 7777 },     // 仪表盘=主界面（0.1.3 起默认开；端口占用自动漂移并粘滞记忆；样式=随包 src/server/panel.html）
  "dashboard": { "autoOpen": false },                 // true=启动时探测本机 Edge（msedge/edge 常见安装路径），以 --app 无边框小窗打开仪表盘；探测/启动失败静默，绝不用默认浏览器裸开
  "sidebar": { "order": 160, "showNonTokenPlan": false }, // 非匹配会话默认整块隐藏；true=弱化一行
  "toast": true,                                      // 窗口边界翻转提醒（每窗口每日恰 2 次）
  "toastOnBoot": true,                                // server 启动 5s 后的一次性摘要 toast（受 toast 总开关叠加；整进程仅一次）
  "slash": false,                                     // /tokenplan 转录命令：桌面版任何新消息都会中断进行中的回合，故默认停用；true=恢复 0.1.1 命令行为
  "refresh": { "catalogMin": 10, "quotaMin": 5 },    // server 刷新周期（分钟）
  "providerMatch": "family"                          // TUI 门控：family=阿里系全家族（alibaba-cn 亦显示，默认）；strict=仅 token-plan 专属
                                                     // 主机判定为完整域名锚定：仅 *.maas.aliyuncs.com / dashscope[-x].aliyuncs.com 及其子域命中，coding.net 等前缀撞车域不误判
}
```

status.json schema、陈旧降级（`staleAfterSec`/坏 JSON/缺席 → TUI 内嵌快照+灰徽标）见包内架构契约。

## 开发

```bash
npm install        # devDeps: esbuild/typescript/@types/node/@opencode-ai/plugin
npm run typecheck  # tsc --noEmit
npm run build      # esbuild → dist/server.js dist/tui.js dist/core.mjs（packages:external）
npm test           # 零宿主单测（回退链/合并/跨午夜/JSONC/陈旧判定）
npm run smoke      # 零宿主冒烟：窗口断言(23:30/15:00 注入 now)+status.json 落盘
npm run publish:check
```

## Changelog

### 0.1.3

- **仪表盘升格：默认开启+Qoder 倍率版式重做+slash 默认关+boot toast**：
  - web 仪表盘（默认 `http://127.0.0.1:7777`，端口漂移粘滞保留）升格为主信息面**默认开启**；页面按新 status.json 契约重做为七区块布局——错峰窗主卡（credits-factor 窗优先、HH:MM:SS 每秒本地 tick、划线价/双源印证/外链）、Qoder 在卖倍率总表（E 行+错峰外直降合并带「限时」标签，脚注「截至 2026-08-31，以官方活动页为准」）、百炼 ¥ 价目分面（峰/谷双列+Batch 叠加，与倍率区不混排）、活动与政策（免费额度/降级/预警，过期置灰+截止日）、额度进度条、页脚钉窗命令一键复制。零 CDN/零框架，动态值全部 HTML 转义、外链仅放行 http(s)。30s 轮询 + 回前台即刷。
  - 新增 `dashboard.autoOpen`（默认 false）：true 时探测本机 msedge/edge 常见路径，以 `--app` 无边框小窗自动打开；失败静默、绝不重开、绝不用默认浏览器裸开。
  - `/tokenplan` slash 命令**默认停用**（`slash: false`）：桌面版发出任何新消息都会中断进行中的回合，转录注入命令属误设计；命令与拦截代码全保留，配置 `slash: true` 即恢复。
  - toast 增强：启动 5s 后一次性摘要 toast（`toastOnBoot`，默认 true，含窗口状态/代表倍率/带实际端口号的仪表盘地址）；窗口边界翻转 toast 保留并附端口。
  - slash=true 时注入的 synthetic 指令缩为一句「仅回复一词：✅」，机制说明挪进用户可见的摘要尾部（桌面不再把长指令渲染给用户看）。

### 0.1.2

- **修复：多实例宿主（桌面版）下插件命令/工具丢失（守卫只挡副作用，hooks 每实例返回）**——桌面版同一 server 进程会按 workspace/实例多次调用 `plugin()`，0.1.1 的双实例守卫让第二次之后的调用拿到无 hooks 存根，`/tokenplan` 命令与查询工具在后启实例里静默消失。现在守卫只保护进程级副作用（状态落盘/后台刷新/定时器/面板，仅首启执行、dispose 也仅首启实例真清理），配置解析与完整 hooks（config / command.execute.before / tool / dispose）每次实例化都返回。

### 0.1.1

- **桌面端确定性命令**：`/tokenplan` 经 server 侧 `command.execute.before` 拦截，优惠摘要（窗口状态+倒计时、在卖倍率、限时优惠、来源与截至声明、时区）由插件直接写入当前会话转录（`ignored` 部分对用户可见、不进模型上下文），模型仅回一句确认——Opencode 桌面版（Electron，不渲染 TUI 插件层）从此可见；支持可选模型名过滤（`/tokenplan qwen3.8-max`）。hook 失败时回退旧「经 LLM 调工具」模板，不炸命令。
- **门控放宽**：新增 `providerMatch` 配置（默认 `family`）——TUI sidebar/home_bottom 门控从「仅 token-plan 专属 provider/主机」放宽为「阿里系全家族」，provider=`alibaba-cn` 会话也显示；`strict` 保持 0.1.0 语义。桌面命令不受门控限制（显式调用总是可用，非阿里系供应商时输出行首注明）。

### 0.1.0（初版要点）

- server + TUI 双入口：百炼目录三级回退（live→cli→snapshot）+ Qoder 静态快照并入，原子持久化 `status.json`（`staleAfterSec` 陈旧降级 + 灰徽标）。
- TUI：sidebar 优惠面板 / 折叠、home_bottom 一行摘要、`/tokenplan` 分类明细对话框，秒级本地倒计时。
- 边界 toast（双源同窗只弹一次）、`tokenplan_discounts` 查询工具（旧名 `bailian_discounts` 委托）、可选本地 web 面板（默认关）。
- Qoder 数据为纯静态快照（来源：Qoder 客户端公开界面快照转录 2026-08-31），不调用任何 Qoder 私有端点。

## License

MIT © te-river
