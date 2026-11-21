<div align="center">

<img src="docs/logo-128.png" width="96" alt="Better Web Controls">

# Better Web Controls

Vibe Coding 网页控件翻译词典

把做个下拉、加个按钮、做个好看的导航这类模糊需求，翻译成 AI 一次就能做对的准确描述：控件名称、形式与操作规则。

[中文](README.md) | [English](README.en.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-22.20%2B-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org)
[![Install](https://img.shields.io/badge/Install-npx%20skills%20add-2563eb)](#安装)
[![Agents](https://img.shields.io/badge/Agents-75%2B-8b5cf6)](https://github.com/vercel-labs/skills)
[![Benchmark](https://img.shields.io/badge/Eval-100%25%20vs%2086.1%25-f59e0b)](#评测结果)

</div>

---

## 效果预览

下列页面均由 AI 按本技能的工作流生成，单文件 HTML，出自评测场景，可在 `web-controls-workspace/` 中直接打开。

| 登录页（Split Screen） | 月度经营报告（上总下分） |
|:---:|:---:|
| ![登录页](https://files.seeusercontent.com/2026/10/28/0Dvo/login.png) | ![经营报告](https://files.seeusercontent.com/2026/10/28/6fyN/chart.png) |
| 下拉选人 + 表格筛选 | 导航栏（悬浮吸顶） |
| ![下拉选人](https://files.seeusercontent.com/2026/10/28/lgS8/dropdown.png) | ![导航栏](https://files.seeusercontent.com/2026/10/28/iG0h/navbar.png) |
| 轮播 | 删除确认（输入文字确认） |
| ![轮播](https://files.seeusercontent.com/2026/10/28/gYk2/carousel.png) | ![删除确认](https://files.seeusercontent.com/2026/10/28/bDi4/confirm.png) |
| 空状态（首次使用） | |
| ![空状态](https://files.seeusercontent.com/2026/10/28/0Ybh/empty.png) | |

## 为什么需要它

让 AI 生成页面时，一句做个下拉往往只能靠运气：形式靠猜，操作规则也靠猜，猜错了就返工。

同一个需求，两种说法，结果不同：

| | 用户对 AI 说 | AI 的产出 |
|---|---|---|
| 翻译前 | 帮我做个下拉，能选负责人 | 产出不定：可能是原生 `<select>`，也可能缺清空、缺键盘操作，且没有选型依据 |
| 翻译后 | 负责人用 Select 单选下拉：选项为团队成员、单选、选中打勾、可清空重选、点外部或 Esc 关闭 | 按规格一次成型，形式与操作规则全部到位 |

本技能把这段翻译过程做成 AI 的工作流：识别需求类型、查参考文件、列出候选并写明选型理由，最后输出可执行的规格。

## 安装

```bash
# 交互式：自动检测已安装的 agent（OpenCode / Claude Code / Cursor 等），选择后安装
npx skills add shanchuann/better-web-controls

# 指定只装这一个技能、只装到 OpenCode
npx skills add shanchuann/better-web-controls --skill better-web-controls -a opencode

# 全局安装（跨项目可用）
npx skills add shanchuann/better-web-controls -g
```

需要 Node.js 22.20 以上版本。skills CLI 支持 75 个以上的 agent，安装时会写入对应 agent 的技能目录（OpenCode 为 `.opencode/skills/`，全局安装为 `~/.config/opencode/skills/`），不需要手动放置。

## 工作流

安装后，agent 收到网页、页面或控件类需求时会自动执行以下流程。

1. 识别需求类型，路由到对应的参考文件（控件、布局、交互规则、修复、图表）。
2. 列出候选并说明选型理由。同一类控件往往有多种形式（下拉 7 种、进度 8 种动画、导航 9 种），输出 2 至 3 个候选及适用场景；信息不足时先向用户确认判断依据。
3. 写选型笔记。候选对比、判断依据与升级条件写入 `notes.md`，交付物可复核、可验收。
4. 输出规格。给出可直接使用的 Prompt（名称、形式、操作规则按固定顺序），或按规格直接生成页面。

## 评测结果

评测覆盖 9 个真实场景（导航栏、页面修复、轮播、下拉选人、删除确认、保存提示、经营报告图表、空状态、登录页），每个场景 4 条断言，对比带技能与不带技能的两组产出；不带技能的一组在评测中禁止读取技能目录。评分按断言逐条核对产物，每条判定附产物证据。

- 基线（iteration-2）：同一 GLM flash 模型，每场景 1 次运行。
- 多次运行（iteration-3）：同一模型每场景 3 次运行，全部 headless CLI 执行；53/54 由自动评分给出（1 项评分遇免费额度耗尽改人工，判据与自动评分一致），并抽样人工复核。

| 轮次 | 带技能 | 不带技能 | 差值 |
|:---:|:---:|:---:|:---:|
| 单次运行（iteration-2） | 36 / 36（100%） | 31 / 36（86.1%） | +13.9pp |
| 多次运行均值（iteration-3） | 106 / 108（98.1%） | 90 / 108（83.3%） | **+14.8pp** |

iteration-3 各场景的运行均值 ± 标准差（每格 3 次运行）：

| # | 场景 | 带技能 | 不带技能 |
|:---:|---|:---:|:---:|
| 0 | 导航栏 | 100% ± 0% | 75% ± 0% |
| 1 | 页面修复 | 100% ± 0% | 100% ± 0% |
| 2 | 轮播 | 100% ± 0% | 83% ± 12% |
| 3 | 下拉选人 | 100% ± 0% | 75% ± 20% |
| 4 | 删除确认 | 100% ± 0% | 92% ± 12% |
| 5 | 保存提示 | 100% ± 0% | 100% ± 0% |
| 6 | 经营报告图表 | 83% ± 12% | 67% ± 24% |
| 7 | 空状态双场景 | 100% ± 0% | 92% ± 12% |
| 8 | 登录页 | 100% ± 0% | 67% ± 12% |

三点发现。

- 带技能组高度稳定。27 次运行中 25 次满分，仅图表场景出现 2 次 3/4（KPI 卡未全部标注环比），从未低于 3/4；两轮测得的差值也稳定在 14–15pp。
- 不带技能组波动明显。同一场景多次运行可相差两档：下拉选人与图表两组里都出现过最低 2/4 与最高 4/4 共存；删除确认、轮播、空状态在 3/4 与 4/4 之间摇摆。单次运行的成绩可能是运气，方差数据才能说明行为差异是否真实。
- 失败模式可复现。18 个失败断言里 12 个是“无候选对比与选型理由”（导航栏不带技能 3 次全部丢同一分）；其余集中在 KPI 卡缺环比标注（4 处，带技能与不带技能各占半）以及个别运行的操作规则、布局要素、防误触细节缺失。这些是稳定的内容差距，不是评分噪声。

完整报告（含每条断言的判定证据）：基线 [web-controls-workspace/iteration-2/benchmark.md](web-controls-workspace/iteration-2/benchmark.md) · 多次运行 [web-controls-workspace/iteration-3/benchmark.md](web-controls-workspace/iteration-3/benchmark.md)

## 内容覆盖

| 参考文件 | 内容 |
|---|---|
| `references/controls.md` | 按钮 6 形态、下拉 7 种、轮播 7 种、Tab 6 种、侧边栏 5 种、弹窗、进度 8 种、上传 5 种、表格 5 种、长列表加载 3 种、步骤条、Tooltip、命令面板、特殊控件 10 种、表单输入控件 |
| `references/layouts.md` | 网站布局 7 种、AI 产品布局 6 种、登录页 5 种、导航 9 种、首页 10 模块、首屏设计、大屏 5 种布局、工作台实战、风格参考图 |
| `references/rules.md` | 提示 7 级、二次确认 7 种、等待体验 6 种、校验时机、表单 7 检查点、空状态 5 种、对齐 5 种、长页面定位 7 种、分组方式、设计术语 7 词、暗色模式、移动端降级 7 项 |
| `references/fixes.md` | 细节修复 7 句（症状、病因、指令）、常见问题 6 句 Prompt |
| `references/charts.md` | 10 种图表与场景选型、决策问句 |

## 仓库结构

```
skills/better-web-controls/   技能本体（npx skills add 的安装源）
├── SKILL.md                  触发条件、工作流、核心公式、完整示例
├── CHANGELOG.md              版本记录
└── references/               5 个参考文件（按需加载）
docs/logo.svg                 标识（IP 角色，含 32/128/512 PNG）
web-controls-workspace/       评测（9 个场景，对比带与不带技能的结果）
```

各 agent 的技能目录（如 `.opencode/skills/`、`.agents/skills/`）是安装时自动生成的本机副本，不入版本控制。

## 更新

技能更新后，在本地执行：

```bash
npx skills update
```

## License

[MIT](LICENSE)
