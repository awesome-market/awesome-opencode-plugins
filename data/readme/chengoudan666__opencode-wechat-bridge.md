# 微信 ⇄ opencode 桥接

把 [thawline/dsh-wechat-bridge](https://github.com/thawline/dsh-wechat-bridge)（MIT）完整移植到 **opencode** 上。

微信里来的消息丢给 opencode 会话，再把回复发回微信。已经跟 DeepSeek Harness 完全解耦，
**不再需要 DSH**。

- 宿主：opencode 2.1.4+（桌面版，插件跑在 `opencode serve` 里）
- 模型：默认 `opencode/deepseek-v4.1-flash-free`（0 成本，支持看图），可改
- 只支持 **Windows**，微信 **4.x** 需已登录

```
微信  ──(本地 SQLite 只读)──>  wechat_bridge.py  ──HTTP──>  插件  ──HTTP──>  opencode 会话
      <──(UI 自动化 + 剪贴板)──
```

---

## 它解决什么问题

微信没有开放接口。这个项目的办法是：

- **收**：只读打开微信本地的 `db_storage` SQLite（不写、不改），0.4 秒轮询新消息；
- **发**：Windows UI 自动化 —— 切会话、粘贴、回车；
- **中间**：一个开放 HTTP 接口，任何 agent 宿主都能接。这个仓库接的是 opencode。

---

## 安装

### 1. 放插件

```powershell
$插件目录 = "$env:USERPROFILE\.config\opencode\plugins"
New-Item -ItemType Directory -Path $插件目录 -Force
Copy-Item .\wechat-bridge.js $插件目录\
```

opencode 会自动扫描 `plugins/` 目录，所以 `opencode.json` 里的 `plugin` 数组**留空**即可
（把文件路径写进去反而会报 `configured plugin path must be a directory`）。

### 2. 重启 opencode

```powershell
$exe = "$env:LOCALAPPDATA\Programs\@opencode-aidesktop\resources\opencode-cli.exe"
& $exe service restart
```

重启后插件**不会立刻加载** —— 要等某个 workspace 初始化。在 opencode 里随便打开/新建一个会话
就会触发，之后：

```powershell
Get-Content "$env:USERPROFILE\.local\share\opencode\wechat-bridge\host.log" -Encoding UTF8 -Tail 5
```

看到这行就对了：

```
微信桥接已加载 v2.2.0｜宿主 opencode http://127.0.0.1:28894｜模型 opencode/deepseek-v4.1-flash-free｜设置页 http://127.0.0.1:39527/
```

### 3. 装 Python 依赖

打开设置页 <http://127.0.0.1:39527/>，点「装依赖」。它会自己找 Python ≥3.10、
在 `%USERPROFILE%\.local\share\opencode\wechat-bridge\wechat-bridge-venv` 建独立环境，
不动你别的环境。几分钟。

> 也可以手动装，但 **`winsdk` 必须装**（原仓库的依赖表跳过了它，因为只有源码包要 Rust 编译）。
> 不装的话发送这一步必挂 `No module named 'winsdk'`。完整依赖：
> `wechatauto-replica`（`--no-deps`）、`uiautomation pywin32 pyperclip Pillow psutil colorama cryptography zstandard imageio-ffmpeg winsdk opencv-python pyautogui`

### 4. 启动桥接 + 接会话

设置页里：**启动桥接** → 选 **默认会话**（或给某个聊天单独绑定）→ 填 **主人** →
打开 **总开关**、关掉 **试运行**。

改配置不用重启，存了就生效（Python 那边 30 秒内拉到新配置）。

### 5. 自检

```powershell
node selfcheck.mjs
```

```
【服务】     ✓ 插件 v2.2.0｜宿主 opencode｜模型 opencode/deepseek-v4.1-flash-free
【Python】   ✓ 虚拟环境 / ✓ 依赖就绪 / ✓ 桥接运行中
【配置】     ✓ 总开关：开 / ✓ 试运行：关 / ✓ 默认会话 / ✓ 主人
```

---

## 怎么用

在 opencode 里打 **`/wechat`** —— 这是面板的正门。它会调 `wechat_panel` 工具，
把当前设置和状态原样贴给你；直接说「把总开关打开」「每小时上限改成 9」「把三班那群绑到工作那间」，
它就会自己改。

| 入口 | 说明 |
| --- | --- |
| 斜杠命令 **`/wechat`** | 面板正门：看设置 / 改设置 / 启停桥接 |
| 工具 `wechat_panel` | `action` = `show` / `set` / `start` / `stop` / `install` / `sessions` / `usage`，`fields` 带要改的键 |
| 工具 `wechat_block` / `wechat_bind` | 「以后别理老李」「把三班绑到工作那间」这类口语指令 |
| 设置页 <http://127.0.0.1:39527/> | 想点按钮就用这个（四大块，和 DSH 原版面板对齐） |

插件本身也会出现在 **设置 → Extensions → Plugins** 列表里（状态 active），但桌面版的插件行是只读的，
点不开任何东西 —— 这就是为什么要做 `/wechat` 这条正门。

---

## 设置页有什么

| 区块 | 内容 |
| --- | --- |
| 一、装依赖 | 虚拟环境状态、安装日志、`解释器`（可选，指向已装好 wechatauto 的 python.exe） |
| 二、启动桥接 | 启动 / 停止、运行秒数、Python 进程实时日志 |
| 三、接到哪间会话 | 总开关、试运行、默认会话下拉、**单独绑定**（增删行 + 最近聊天一键勾选）、**思考强度**（低/高/最高）、**人设提示词**、接口令牌、群上下文条数、群回复间隔 / 每小时上限、**活跃群**（不点名也回的群）、外人只能聊天、群聊日记 + 目录、主人、**主人微信名**（主动搭话）、**不回谁（屏蔽）** |
| 四、试一试 | 发到微信 / 灌一条进会话 |
| 日志 | 宿主日志 tail |

### 特别说明几个开关

- **总开关**：关着 = 一句都不发（收消息照收，日志照记）。
- **试运行**：开着 = 只在日志里记「该发什么」，不真发。刚接上时先用这个跑两天。
- **主人**：填 wxid 或微信昵称。非主人发言会自动加「这条不是你主人」的提示前缀，
  并且（默认）**只能聊天、不能用工具** —— 靠插件的 `tool.execute.before` 钩子拦。
- **主人微信名**：填了之后，你在 opencode 里自己跟它说话，它的回答也会顺手发到这个微信私聊
  （「主动搭话」）—— 等于手机上也能收到。
- **活跃群**：这些群不点名也回。没列进去的群要 @ 别名（`大肥鱼`/`鲸鲸`/`鲸鱼娘`/`鲸鱼`/`肥鱼`，
  可用 `--aliases` 改）或者主人说话才会应。

---

## 装在哪

所有东西都在 opencode 自己的数据目录下面，不碰 `~/.dsh`。

| 东西 | 位置 |
| --- | --- |
| 插件（生效的那份） | `%USERPROFILE%\.config\opencode\plugins\wechat-bridge.js` |
| 桥接家目录（`家`） | `%USERPROFILE%\.local\share\opencode\wechat-bridge\` |
| 配置 | `家\config.json` |
| 宿主日志 | `家\host.log` |
| 用量账本 / 最近聊过谁 / 好感度 | `家\usage.json`、`chats.json`、`affinity.json` |
| 群聊日记 | `家\wechat-diary\<日期>\<群名>.md` |
| Python 桥接脚本 | `家\bridge\wechat_bridge.py` |
| Python 虚拟环境 | `家\wechat-bridge-venv` |
| 临时文件（微信附件落地） | `家\wx-tmp` |

`家` 可以用环境变量 `WECHAT_BRIDGE_HOME` 覆盖。

---

## 相对原 DSH 版的改动

### 1. 宿主从 DSH 换成 opencode

opencode 的插件 API 没法注册 HTTP 路由，所以插件自己起了一个 `node:http` 服务
（`127.0.0.1:39527`），对外路径和 DSH 版**一模一样**：

```
GET  /dsh-wechat-bridge/state
POST /dsh-wechat-bridge/receive
GET  /dsh-wechat-bridge/outbox
POST /dsh-wechat-bridge/outbox/ack
POST /dsh-wechat-bridge/save  /send  /test-send  /test-inbound
POST /dsh-wechat-bridge/bridge/{start,stop,status,install}
```

因此 `wechat_bridge.py` 只动了几处小地方，启动参数从 `--dsh <DSH地址>` 变成
`--dsh http://127.0.0.1:39527`。`版本` 报 `2.2.0`（≥1.2.0），桥接才会把图片**路径**转过来
而不是自己做识别。

插件加载格式必须是 `export default { id, setup }`（opencode 2.1.4 的 schema），
不是命名导出。`setup` 每个 workspace 都会调一次，靠 `globalThis` 去重。

opencode 自己的 API 走 `http://127.0.0.1:28894`（v2 的 `/api/*`，v1 路径全是 SPA 的 404），
端口是插件启动时用 `netstat` 按自己的 pid 找出来的，口令读 `~/.config/opencode/service.json`。
**所有 opencode 调用都走 HTTP** —— 直接 `await ctx.session.prompt(...)` 会把 setup 的 Effect fiber 卡死。

### 2. 修了「微信窗口找错」的致命 bug

`WeChatGUI()` 不加参数时按「标题含微信 / 类名前缀 / 进程名」打分挑窗口。如果机器上还有别的
窗口标题带「微信」两个字，评分能到 7 分，把真微信挤掉 —— 结果每条回复都**贴进了那个窗口的输入框**：

```
✗ 发送失败：文字没发出去（微信窗口没接住）
```

`wechat_bridge.py` 里加了 `_微信主窗口()`：用 `psutil` 找出 `Weixin.exe` 的 pid，
再用 `win32process.GetWindowThreadProcessId` 精确匹配，只认类名以 `Qt` 开头的可见窗口。
日志里能看到 `WeChatGUI 已就绪（按进程锁定 hwnd=…）`。

### 3. 图片直接喂给模型

免费档的 `capabilities.input` 里有 `image`，所以不再走「先用别的视觉模型描述成文字」那条路。
`/receive` 带 `图片` 路径时，插件把它们转成 `file://` 附加到 prompt 的 `files` 上。
反向也支持 —— 模型输出的 `content[].type === 'image'` 会被捞出来塞进发件队列。

### 4. 会话落在「看得见的目录」

opencode 桌面版的侧边栏只列 `location.directory === 当前项目目录` 的会话。
插件原来把微信会话建在 `家` 下面，等于建在另一个 project 里，**界面里根本看不到**。现在：

- `建会话()` 不传目录时落在 `/api/location` 报的当前目录；
- 插件启动时会把 `默认会话` + 所有 `绑定[].会话` 用 `POST /api/session/{id}/move` 挪到当前目录
  （move 保留全部历史，只改元数据）；
- `会话清单()` 会遍历 `/api/project` 里所有项目合并去重，设置页的会话下拉才看得全。

### 5. 工具返回格式

opencode 2.1.4 的插件工具只要声明了 `output` schema，就必须回 `{ output: '...' }`；
直接回字符串会抛 `a is not an Object. (evaluating '"output" in a')`。
现在三个工具统一包 `output: 输出结构` + `execute: async (...) => ({ output: String(await 原(...)) })`。

### 6. 假会话直接拦、发送超时不再谎报成功

两个都是原版就有的坑：

**假会话会「一直在搜」。** 以前 `send_one` 不管名字对不对都硬发，`open_chat` 找不到就原地
重试 3 轮 × 75 秒，每轮都点搜索框、粘贴名字、扫侧栏 —— 界面上就是「一直在搜这个字」。
现在发之前先查库（`_会话存在()`），查不到直接返回「微信里找不到这个会话」，一次界面都不用碰。
另外 `_开会话(chat, 超时=30)` 给 `open_chat` 套了超时，切不过去就认输，不会把字打进上一个会话。

**超时被当成成功。** 原来的 `带超时` 超时后 `return "发送超时"`，而调用方写的是
`if not isinstance(r, Exception) and (r is None or r)` —— 非空字符串是真值，于是卡死的发送
被记成「✅ 已发到微信」，消息其实一条没出去。现在返回 `(种类, 结果)` 三元组：

```python
if t.is_alive():
    return "timeout", None
if "e" in 盒:
    return "err", 盒["e"]
return "ok", 盒.get("r")
```

### 7. 主动搭话

原版靠 `turn/end` 里 `source.kind === 'speak-up'` 的标记，把**主人在宿主里自己说的话**
顺手转发到主人的微信私聊。opencode 端拿不到事件（`ctx.event.subscribe` 和 `ctx.session.hook`
在 `setup` 返回后一律零回调，全探针验证过），所以改成 **3 秒轮询**：每轮拉
`GET /api/session/{id}/context`，用「游标 + 有主人说过」两个 Map/Set 判断
「这一轮是不是主人自己在 opencode 里说的」。

判定顺序和原版一致：总开关关 → 不发；试运行 → 只记日志；桥没跑 → 不发；`[不回]` → 不发。
另外要求这一轮里**已经出现过 `type === 'idle'`**，否则流式输出的半截也会被发出去。

**防回环。** 发到「文件传输助手」的消息会被 listener 立刻读回来，不拦就自问自答。
`sent_by_chat` 按会话记我们发出去的每句话（10 分钟窗口），并在**点发送之前**就记账 ——
因为出站是串行的，每条要等 8 秒数据库确认，等真正发完，原来那个 12 秒静音窗口早过期了。

### 8. 思考强度 与 自定义人设

**思考强度**用 opencode 的 model variant：`low` / `high` / `max`，留空 = 不指定。
建会话时带进 `model.variant`，对已有会话由 `钉模型()` 用
`POST /api/session/{id}/model {model:{id,providerID,variant}}` 切过去（204）。

**自定义人设**绕了一个必要的弯。opencode 的 `POST /api/session/{id}/prompt` 虽然**收**
`system` 字段（不报错），但**不生效** —— 实测传了「只回复 BANANA」，模型照样正常回答。
真正能让模型听人设的只有 agent 的 `system`：

```js
await ctx.agent.transform((草稿) => {
  草稿.update('wechat-bridge', (a) => { a.system = 人设文本 })
})
```

为这个专门建了一个 `wechat-bridge` agent（`草稿.update` 对不存在的 id 会**新建**），
只给微信这几间会话用 —— 改 `build` 会影响你自己在 opencode 里聊天的每一轮，所以不能动它。

### 9. 群消息发不出去：侧栏宽度自己量 + 搜索框兜底

原版在 3072 宽的屏幕上标定过布局，写死 `sidebar_ratio = 0.22`；换到 694 宽的小窗口后比例还是
0.22，于是「会话名右边界」被算成 83 px，而侧栏里真名字都排在 x≈118 往右 ——
`find_session` 把所有行都当聊天区标题扔掉了，**任何会话都切不过去**。
私聊之所以看着正常，是因为那个窗口本来就开着，`_chat_is_open()` 直接命中。

另外有些机器上 **UIA 树是空的**：主窗口下只有一个 `PaneControl 'MMUIRenderSubWindowHW'` 子节点，
再往下 `GetChildren()` = 0，`EditControl(searchDepth=16)` 直接 `LookupError`。试过
`_set_screen_reader_flag`、`_hot_activate_accessibility`、`_wake_accessibility` 都返回 True
但树依旧空（微信 4.x Qt 自绘不暴露）。所以**不能指望 UIA**。

两条补丁：

**① `_侧栏真宽()` / `_校正侧栏()` —— 用像素量，不用 OCR。**
按列统计「偏离该列中位数 ≥45 的像素占比」当文字密度，找 `0.2W` 之后**第一段**
`密度 < 0.02`、宽度 ≥16 的低密度带，起点就是侧栏右边界。跟当前比例差 >0.03 就写回
`gui._sidebar_ratio` 并 `_update_layout()`。

> 必须是「第一段」而不是「最长的一段」。窗口最右边（聊天区后面的显示窗边缘）也是一条
> 低密度竖带，而且往往比侧栏那道缝更长（实测 694 宽窗：侧栏缝在 x=300 宽 20px，
> 右边缝在 x=670 宽 24px）。写成取最长会量出 ≈0.97W，被范围检查否掉，于是永远返回 0。

```
侧栏宽度按实测校正：0.220 → 0.432（300 / 694 px，会话名右边界 83 → 165）
```

**② `_输入框走键()` —— 搜索框粘名字，点下拉第一行，不认字。**
点搜索框 → `Ctrl+A`/`Delete` → 剪贴板粘名字 → 轮询搜索框角落底色（下拉浮层比侧栏背景深）
判断浮层出来没有 → 点第一行。微信的搜索结果把最像的那个人/群排在第一位，所以只要
「浮层出现了」就能点中，完全不需要 OCR 认中文名。

`_开会话()` 现在是三级：① 正常 `open_chat`（带超时）→ ② `_校正侧栏` 后重试 →
③ `_输入框走键` 兜底。三级全挂才报「切不到」。

### 10. 绑定只显示一个、会话被删了永久 404

**① 「单独绑定 + 群聊，只显示一个」是设置页自己的 bug。**
`load()` 每 5 秒拉一次 `/state`，然后无条件 `S = j` 把整个页面数据源换掉；可「加一条绑定」
是往 `S.配置.绑定` 上改的。轮询一过 `S.配置` 就变回服务器旧值，再点「＋ 加一条绑定」
是在旧值上 concat —— 刚填的那行当场消失。

```js
if (脏 && S && S.配置) j.配置 = S.配置;   // 有没保存的改动就别覆盖配置
S = j;                                    // 活着的会话 / 桥接状态 / 日志照旧用新的
```

**② 你在 opencode 里删掉会话之后，微信那边永久不回复。**
配置里存的是会话 id；那间会话被删掉后，每条微信消息走 `/prompt` 都是
`404 SessionNotFoundError`。现在 `转入消息()` **先探再钉**：`GET /api/session/{目标}`，
404 就 `重开会话()`（现开一间 + 把 `默认会话`/`绑定[].会话` 里指向旧 id 的引用一并改掉），
然后再 `钉模型` / `挂人设`。搭话轮询遇到 404 静默跳过，别的错去重后只记一次。

---

## 坑

**`winsdk` 必须装**（见上）。

**opencode 持着文件锁。** 插件文件被 watch 着的时候直接改会报
`ReplaceFileW EIO (Win32 1175)`。改源码 → `Copy-Item` 覆盖 → 重启。

**重启后插件不会立刻加载。** `setup` 要等某个 workspace/location 初始化才被调用。
重启完要在 opencode 里动一下（开个会话），或者自己扫一遍 API：

```powershell
$pw = (Get-Content "$env:USERPROFILE\.config\opencode\service.json" -Raw | ConvertFrom-Json).password
$b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("opencode:$pw"))
$h = @{ Authorization = "Basic $b64" }
foreach ($p in 'location','project','session/active','model','agent','skill') {
  Invoke-RestMethod -Uri "http://127.0.0.1:28894/api/$p" -Headers $h | Out-Null
}
```

**日志是 UTF-8。** PowerShell 里 `Get-Content` 要加 `-Encoding UTF8`，否则中文全是乱码。

**HTTP 里的中文。** PowerShell 直接 `Invoke-RestMethod -Body $json` 会乱码，必须
`[Text.Encoding]::UTF8.GetBytes($json)` + `-ContentType 'application/json; charset=utf-8'`，
读回来也要 `[Text.Encoding]::UTF8.GetString($r.RawContentStream.ToArray())`。

---

## 会话被删了怎么办

会自动重开一间顶上，并把配置里的引用改掉（见「改动 10」）。日志里能看到：

```
「某群」原来那间会话（ses_xxx）没了，重开了一间：ses_yyy
```

---

## 风险

微信个人号接自动化**有封号风险**，官方不允许。先用小号试，别拿主号长期跑。

---

## 许可

MIT。基于 [thawline/dsh-wechat-bridge](https://github.com/thawline/dsh-wechat-bridge)
（作者 [Yuuyuko-uu](https://github.com/Yuuyuko-uu) 及 contributors）移植。
