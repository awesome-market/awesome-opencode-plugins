# Session Navigator

一个面向 **OpenCode Desktop** 的会话导航插件。它在对话右侧中间放一条轻量的消息位置栏，鼠标悬浮或键盘聚焦时展开为消息预览卡片，点击任意一条即可跳到对应的消息。

默认只显示右侧中间的一列短横线，不遮挡正文；悬浮后才显示具体消息内容。

## 功能

- 右侧**垂直居中**的消息位置栏，不挤压聊天区域。
- 默认只显示紧凑的短横线，鼠标悬浮或键盘聚焦时展开消息预览卡片。
- 鼠标移开后自动收起，打字/阅读时不会一直占用视野。
- 会列出当前会话的所有用户消息（不只是屏幕上已经渲染出来的几条）。
- 点击任意消息，平滑或快速定位到对应位置；长会话中也能正确跨越大段内容。
- 滚动对话时，导航中的当前消息会自动跟随并高亮。
- 当前消息在导航列表里自动滚入视野；手动滚动导航时不会被打断。
- 跟随 OpenCode 的明暗主题，使用应用自身的颜色变量。
- 不使用任何外部网络请求；消息只从当前 OpenCode 服务器读取。

## 安装

需要 OpenCode Desktop **2.4.x**，并在全局配置中启用插件。

### 从 GitHub 安装（推荐）

```powershell
opencode plugin add github:1bigmouse/opencode-session-navigator
```

也可以手动在 `~/.config/opencode/opencode.jsonc`（Windows 下即
`C:\Users\<你>\.config\opencode\opencode.jsonc`）的 `plugins` 中加入：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "github:1bigmouse/opencode-session-navigator"
  ]
}
```

保存后 OpenCode 会自动重载插件。如果右侧没有出现位置栏，可以关闭当前窗口再重新打开；也可以在
**设置 → 扩展 → 插件** 中确认 `opencode-session-navigator` 已经列出。

### 本地开发安装

```powershell
cd C:\Projects\Opencode_plugin
npm install
npm run build:dist
```

然后把本地目录加入 `plugins`：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "C:/Projects/Opencode_plugin"
  ]
}
```

> GUI 插件 API 目前标记为 experimental，本插件按 OpenCode Desktop **2.4.x** 的接口开发。

## 使用

- 会话有至少一条用户消息后，右侧中间会出现短横线位置栏。
- 鼠标移到位置栏上，展开消息预览卡片；移开自动收起。
- 点击任意条目跳转；当前条目会以强调色显示。
- 悬停条目可查看完整提问。
- 键盘：`Tab` 聚焦位置栏后自动展开，`↑` / `↓` / `Home` / `End` 移动，`Enter` 跳转，`Esc` 收起。

## 实现说明

- 使用 `@opencode/plugin/gui` 的 `window.bottom` slot，并通过 `Portal` 挂到
  `document.body`，因此不会影响应用布局。
- 消息通过当前会话所属服务器的 `client.message.list({ type: "user" })` 读取，然后按时间排序；
  会过滤被 revert 隐藏的消息。
- 右侧位置栏和展开卡片都放在一个覆盖时间线的容器里，用 flex 垂直居中；卡片向右对齐，
  与滚动条之间留出空隙。
- 位置栏最多采样 32 个标记，并始终保证当前消息有一个标记；窄窗口会自动减少标记数量。
- 定位使用 OpenCode 渲染出的锚点 `#message-<messageID>` 和
  `[data-slot="session-timeline-scroll"] [data-scrollable]` 滚动容器。
- 时间线是虚拟列表，远处消息不在 DOM 中。插件会根据已挂载消息的位置做插值，逐帧滚动逼近目标；
  找到目标后用隐藏层暂时遮住内容，再等待虚拟列表测量稳定后对齐，避免长会话中“跳一半”的问题。
- 跳转前会向时间线发送一次向上的滚轮意图，让 OpenCode 退出自动跟随；否则流式输出会把视图拉回底部。
- 样式全部使用应用已有的 `--v2-*` 主题变量，并带有回退值。

## 开发

```powershell
npm run watch      # 修改后自动构建，GUI 会热重载
npm run typecheck  # TypeScript 检查
npm run build:dist # 生成 dist/gui-experimental.cjs
```

目录结构：

```text
src/
  gui.tsx          GUI 入口：Style、Slot
  definition.ts    i18n
  navigator.tsx    导航组件、消息读取、滚动定位、悬浮/聚焦状态
  navigator.css    主题化样式
dist/
  gui-experimental.cjs
```

## 已知限制

- 依赖 OpenCode 时间线的 DOM 结构（`data-message-id`、`data-timeline-row` 等）。OpenCode
  大版本更新后如果结构变化，可能需要同步调整。
- 消息列表最多读取最近 1000 条用户消息；更早的消息可以通过 OpenCode 自己的历史加载查看。
- 侧边栏较窄或窗口处于窄屏模式时，导航会自动隐藏，避免遮挡对话。

## License

MIT
