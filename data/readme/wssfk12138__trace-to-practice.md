<p align="center"><strong>简体中文</strong> · <a href="README.en.md">English</a></p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-trace--to--practice-6F42C1?style=flat-square" alt="Agent Skill">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/License-MIT-2EA44F?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/tests-27%20passed-2EA44F?style=flat-square" alt="27 tests passed">
  <img src="https://img.shields.io/badge/Indexer-offline-0F766E?style=flat-square" alt="Indexer offline">
  <a href="https://linux.do/"><img src="https://img.shields.io/badge/LINUX-DO-FFB003.svg?logo=data:image/svg%2bxml;base64,DQo8c3ZnIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCIgaGVpZ2h0PSIxMDAiPjxwYXRoIGQ9Ik00Ni44Mi0uMDU1aDYuMjVxMjMuOTY5IDIuMDYyIDM4IDIxLjQyNmM1LjI1OCA3LjY3NiA4LjIxNSAxNi4xNTYgOC44NzUgMjUuNDV2Ni4yNXEtMi4wNjQgMjMuOTY4LTIxLjQzIDM4LTExLjUxMiA3Ljg4NS0yNS40NDUgOC44NzRoLTYuMjVxLTIzLjk3LTIuMDY0LTM4LjAwNC0yMS40M1EuOTcxIDY3LjA1Ni0uMDU0IDUzLjE4di02LjQ3M0MxLjM2MiAzMC43ODEgOC41MDMgMTguMTQ4IDIxLjM3IDguODE3IDI5LjA0NyAzLjU2MiAzNy41MjcuNjA0IDQ2LjgyMS0uMDU2IiBzdHlsZT0ic3Ryb2tlOm5vbmU7ZmlsbC1ydWxlOmV2ZW5vZGQ7ZmlsbDojZWNlY2VjO2ZpbGwtb3BhY2l0eToxIi8+PHBhdGggZD0iTTQ3LjI2NiAyLjk1N3EyMi41My0uNjUgMzcuNzc3IDE1LjczOGE0OS43IDQ5LjcgMCAwIDEgNi44NjcgMTAuMTU3cS00MS45NjQuMjIyLTgzLjkzIDAgOS43NS0xOC42MTYgMzAuMDI0LTI0LjM4N2E2MSA2MSAwIDAgMSA5LjI2Mi0xLjUwOCIgc3R5bGU9InN0cm9rZTpub25lO2ZpbGwtcnVsZTpldmVub2RkO2ZpbGw6IzE5MTkxOTtmaWxsLW9wYWNpdHk6MSIvPjxwYXRoIGQ9Ik03Ljk4IDcwLjkyNmMyNy45NzctLjAzNSA1NS45NTQgMCA4My45My4xMTNRODMuNDI2IDg3LjQ3MyA2Ni4xMyA5NC4wODZxLTE4LjgxIDYuNTQ0LTM2LjgzMi0xLjg5OC0xNC4yMDMtNy4wOS0yMS4zMTctMjEuMjYyIiBzdHlsZT0ic3Ryb2tlOm5vbmU7ZmlsbC1ydWxlOmV2ZW5vZGQ7ZmlsbDojZjlhZjAwO2ZpbGwtb3BhY2l0eToxIi8+PC9zdmc+" alt="LINUX DO 社区"></a>
</p>

<p align="center">
  <img src="assets/readme/cover.jpg" alt="Trace to Practice · 对话经验蒸馏项目封面" width="1280">
</p>

<h1 align="center">Trace to Practice</h1>

<p align="center"><strong>对话经验蒸馏：把任务历史变成可复核、可落地的工作流改进。</strong></p>

<p align="center">证据优先 · 本地索引 · 不把“没有反馈”当成满意</p>

<p align="center">
  <a href="#sponsor"><img src="assets/readme/fastai-sponsor-zh.png" alt="FastAI 模型赞助商" width="109" height="28" align="middle"></a>
  <a href="#support"><img src="https://img.shields.io/badge/%E5%BE%AE%E4%BF%A1-%E8%B5%9E%E5%8A%A9%E6%9C%AC%E9%A1%B9%E7%9B%AE-07C160?style=for-the-badge&logo=wechat&logoColor=white" alt="微信 · 赞助本项目" height="28" align="middle"></a>
</p>

Trace to Practice 是一个面向 AI 编程助手任务历史的蒸馏技能。它先建立可定位的任务索引，再按需做深度分析，最后把经验落实到规则、项目文档、技能、记忆或使用习惯。

它适合定期复盘，也适合排查反复出现的协作问题。默认由本地脚本做机械索引、性价比模型做整理与初评、旗舰模型做深度蒸馏。批量整理前确认成本选择，深度蒸馏前确认能力选择；已有明确选择不重复询问。小规模任务可在用户接受后由同一模型完成，不强制换窗。

> **赞助商**：[FastAI](https://www.fastaitoken.com/register?aff=BF9KNKFHX725&promo=WSSFK&utm=trace-to-practice) 是本项目的模型赞助商。如果你需要接入 DeepSeek、GLM、Kimi、GPT、Claude 等模型，可以了解其模型中转服务；注册即送 3 美元体验金，套餐、模型可用性与质量以服务商页面为准。通过此链接注册或充值，作者会获得返利，用于继续维护本项目。赞助不影响技能功能、分析结论和推荐。[查看赞助说明 ↓](#sponsor)

## 为什么需要它

很多“复盘”最终变成一份读起来不错、却无法验证的总结：成功归功于方法，失败归咎于模型，缺少反馈被写成满意，新增需求被算成返工。

Trace to Practice 把顺序倒过来：

1. **先保存证据。** 每条判断都能回到源文件、线程、回合、消息和原文摘要。
2. **先整理，再分析。** 用任务卡和任务链降低重复阅读，深度分析只回看争议与高风险证据。
3. **先归因，再评分。** 区分模型遗漏、用户改需求、环境故障和证据不足。
4. **先确认授权，再落地。** 只读建议、项目修改、发布和跨供应商操作分别遵守各自授权。

## 快速开始

### 作为技能安装

把整个仓库安装到客户端的技能目录，而不是只复制 `SKILL.md`。引用、脚本、案例和模板都是技能的一部分；模板仅在需要时使用。

按 [Codex 当前官方文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)，个人技能放在 `~/.agents/skills/`。将完整仓库目录复制或链接为 `~/.agents/skills/trace-to-practice/`，确保其中直接包含 `SKILL.md`；Windows 对应用户目录下的 `.agents/skills/trace-to-practice/`。

其他客户端或已有安装可能采用不同位置，请沿用其支持的技能目录。Codex 支持符号链接，能够检测技能变化；若新技能未出现，按客户端说明刷新或重启。

### 安装 Release

从 [v1.2.0 Release](https://github.com/wssfk12138/trace-to-practice/releases/tag/v1.2.0) 下载 `trace-to-practice-v1.2.0.zip`，解压后把其中的 `trace-to-practice` 文件夹放入 `~/.agents/skills/`。最终路径应为 `~/.agents/skills/trace-to-practice/SKILL.md`，不要多套一层版本目录。Windows 对应 `%USERPROFILE%/.agents/skills/trace-to-practice/`。更新前保留已有本地定制，避免安装两个同名副本。

ZIP 是可直接使用的独立 Skill，包含完整引用和脚本；不需要 OpenAI 官方插件目录审核。安装后在 Codex 输入 `$trace-to-practice`，若客户端未检测到则按客户端说明刷新或重启。

### 生成第一份索引

```bash
git clone https://github.com/wssfk12138/trace-to-practice.git
cd trace-to-practice
python scripts/build_index.py --input examples/snapshots --out ./run/example
```

示例只使用虚构数据。成功后会得到 `task-candidates.jsonl`、`quality.json`、`index.md` 和 `manifest.json`。

### 调用技能

```text
使用 $trace-to-practice 蒸馏过去两周指定项目的任务。
先整理任务索引和用户反馈，区分原要求漏做与新增需求。
复用上轮未变化的材料。先只读输出建议，列出证据和未知项；
已授权的改动按授权范围落实，最后集中给出使用习惯建议。
```

## 模型分工与成本控制

1. **脚本**完成机械提取、来源哈希与候选索引，不调用模型。
2. **性价比模型**合并任务链、分类、归因和初评；先检查少量代表案例，系统性误判应纠正后再批量处理。
3. **高推理能力模型**先核对交接包与关键判断、独立抽查原始来源，再提炼规则和工作流；不默认重读全部历史。
4. **按授权落实**到已有权威文件，验证成果并集中给出用户习惯建议。

模型未选定时，在相应阶段开始前向用户确认；用户可提前指定两阶段模型，或明确接受单模型完成。不要求证明模型排名，不绑定品牌、不自动调用其他供应商或创建新会话。此技能提供流程约束和交接方式，不自带模型调度器，也不保证节省比例。详见 [模型分工与阶段确认](references/model-stages.md)。

阶段选择必须能回到用户的实际答复。提问已发出、选项预选、等待超时或助手自己说“已接受”，都不构成授权；缺少答复时停在已获准范围并结束本轮回复。整理阶段的归因与初评可以单独交付，跨任务规律、规则取舍和修改方案属于深度分析。

## 输入是什么

索引器读取一个目录下的 `*.json` 快照，不递归扫描，也不直接读取 ChatGPT、Claude、Codex 或其他平台的私有数据库。每份快照使用明确的 `thread / turns / items` 结构：

```json
{
  "thread": { "id": "example-thread", "title": "Example" },
  "captured_at": "2026-01-03T12:00:00+00:00",
  "page": { "hasMore": false },
  "turns": [{
    "id": "example-turn",
    "startedAt": "2026-01-02T10:00:00+00:00",
    "completedAt": "2026-01-02T11:00:00+00:00",
    "items": [
      { "id": "u1", "type": "userMessage", "content": [{ "type": "text", "text": "Build an index" }] },
      { "id": "a1", "type": "agentMessage", "phase": "final_answer", "text": "Index created" }
    ]
  }]
}
```

完整契约见 [评分与证据规范](references/scoring-and-evidence.md)，可直接运行的样例见 [examples/snapshots/example-thread.json](examples/snapshots/example-thread.json)。

时间窗使用半开区间 `[start, end)`：回合结束时间等于窗口起点时不计入。`--start` 和 `--end` 都省略时处理全部快照；提供时必须带时区。

```bash
python scripts/build_index.py \
  --input ./snapshots \
  --out ./run/index-2026-01 \
  --start 2026-01-01T00:00:00+08:00 \
  --end 2026-02-01T00:00:00+08:00
```

## 工作流

![工作原理：确定边界、本地机械索引、整理与证据绑定、审查与蒸馏、按授权落实、验证与复用](assets/readme/workflow-zh.png)

[查看流程图原图](assets/readme/workflow-zh.png) · 按 01–06 阅读：上排从左到右，下排从右到左。

| 阶段 | 主要动作 | 产出 |
|---|---|---|
| 1. 划定边界 | 确认时间、项目、来源、时区和授权范围 | 本轮 manifest 与来源说明 |
| 2. 低成本整理 | 读取元数据、用户要求、最终回复和下一条反馈 | 候选卡、任务链、证据索引 |
| 3. 深度分析 | 先审查交接与关键证据、独立抽查来源，再对照正反例并回看争议 | 审查记录、归因、置信度、改进建议 |
| 4. 落实与验证 | 按授权修改最小适用位置，运行相关测试 | 变更记录、验证结果、回退点 |

技能把建议落在五个位置：全局 `AGENTS.md`、项目约定、可复用 skill、持久记忆和用户使用习惯。优先修改已有的权威位置，避免同一事实在多处重复维护。

### 蒸馏之后如何使用

先检查原始需求、有效变更和交付是否对应，必要时核对相关产物；再区分确定缺陷、明确偏好、环境限制与待验证经验。报告优先列出最值得落实的变化，说明下次何时使用、从哪里读取和如何验证，不凑固定数量。

需要落地时，技能会检查已有规则与记忆入口，给出具体修改预览；已授权部分直接落实，缺少授权时集中询问。已有体系优先合并；没有体系时可从一个私有记忆页或项目规则补丁开始。也可以只保留报告。普通 Markdown 即可，不要求 Obsidian、数据库或后台服务。

- [经验落地指南](references/practice-integration.md)：选择落点、接通读取入口、维护与撤回。
- [三个虚构案例](examples/practice-cases.md)：从零建立、合并已有体系、修正失效经验。
- 可选模板：[记忆条目](assets/templates/memory-entry.md)、[私有索引](assets/templates/memory-index.md)、[项目入口](assets/templates/project-index.md)。只选需要的内容，不批量创建文件。

```text
使用 $trace-to-practice 落实上一轮已核验的建议。
先检查现有规则与记忆入口，给我具体修改预览和下次使用方式。
目前只读，不修改文件；已有报告不需要重新蒸馏。
```

文件写入、宿主能找到文件、后续任务正确使用，是不同验证层级。自定义文件名不会自动获得读取能力。技能会明确哪些已验证；没有后续观察时不宣称提效。案例中的结果均为演示，不是产品效果数据。

本节与上方安装说明对应当前 v1.2.0 源码与已准备的 Release 包；新增内容包含落地指南、模板、虚构案例，以及分析前审查和阶段授权等待规则。上方 Release 链接在正式发布后可用。

## 索引输出

| 文件 | 内容 | 可以拿来做什么 |
|---|---|---|
| `task-candidates.jsonl` | 每个最终回复一张候选卡，含要求、交付、下一条反馈、证据定位 | 人工或模型复核 |
| `index.md` | 候选卡的简短目录 | 快速浏览和挑选回源对象 |
| `quality.json` | 去重、缺失 ID、开放回合、截断和问题式回复的计数 | 了解材料完整度，不是质量分 |
| `manifest.json` | 来源 SHA-256、时间窗、配置和产物哈希 | 复核本轮输入与输出 |

缺失或重复的回合开始时间会使跨回合反馈关联保持未知，依据记录在 `feedback_order_basis`；同回合反馈仍可按消息顺序定位。开放回合的重复快照若采集时间不同，会明确报冲突，要求选择一份明确截止的输入。

候选卡的 `score` 始终是 `null`，状态是 `unreviewed`。脚本只做机械整理，不做语义评分，也不计算满意率或节省比例。

## 评分不是“满意度打分”

评分是用于复核的序数量表，不是精密测量：

| 分值 | 何时使用 |
|---|---|
| `+2` | 明确验收，且真实使用路径有证据 |
| `+1` | 明确接受或批准阶段，但验证有限 |
| `0` | 用户指出结果有好有坏，尚不能整体接受 |
| `-1` | 有证据表明遗漏或违背此前已知要求 |
| `-2` | 同一已知要求在修正后仍反复未满足 |
| `null` | 没有反馈、反馈模糊、新任务或证据不足 |

“按方案开始”只肯定方案阶段，不等于验收实现。需求变化可以产生流程建议，不自动成为负分。

完整规则、反馈归类和归因方式见 [评分与证据规范](references/scoring-and-evidence.md)。

## 隐私与边界

> [!IMPORTANT]
> 索引输出会保留对话摘要和来源定位，属于个人数据。不要把 `run/`、真实快照或包含私人信息的报告提交到公开仓库。
>
> “离线”只描述 Python 索引器。使用 skill 让模型阅读和分析材料时，相关内容会进入当前客户端和所选模型的处理流程；是否传到云端及如何保留数据，取决于该客户端和服务商。请先限定材料范围并按需脱敏。

- **只读本地文件。** 脚本不抓取平台历史、不访问网络、不调用模型，也不读取账号配置。
- **默认不写绝对路径。** `manifest.json` 只记录快照文件名；确实需要本机绝对定位时，才显式使用 `--path-mode absolute`。
- **不把注入内容当成用户要求。** `AGENTS.md` 指令、环境上下文等会进入 `context_messages`，不会混入 `requests`。
- **不把提问当成交付。** 助手消息即使被标为最终回复，也可能只是澄清问题；卡片的 `delivery_looks_like_question` 只提示复核。
- **不把抽取当结论。** 来源工具可能截断消息或遗漏工具轨迹。`quality.json` 会列出这些限制，关键判断应回源核对。
- **不自动写规则。** 技能只提出带证据的建议，实际修改仍取决于授权和验证。

完整的公开数据处理说明见 [隐私政策](PRIVACY.md)。

## 兼容性

| 项目 | 要求或说明 |
|---|---|
| Python | 3.10 或更高版本，仅使用标准库 |
| 客户端 | 支持 Agent Skills 目录结构的客户端均可使用；安装位置按客户端调整 |
| 输入 | 显式 `thread / turns / items` JSON 快照 |
| 验证 | 27 个合成测试通过 Python 3.10.20、3.11.4、3.12.13、3.13.14 |
| 网络 | 索引器不联网 |
| 模型 | 索引器不调用模型 |

其他平台的原始日志需要先转换成公开契约中的结构，并核对消息类型、最终回复标记和时间语义；本项目不宣称可以自动识别所有日志格式。

## 项目结构

```text
trace-to-practice/
├── SKILL.md                         # 触发边界与四阶段工作流
├── references/
│   ├── scoring-and-evidence.md      # 评分、归因、证据与输入契约
│   ├── model-stages.md              # 模型分工与阶段确认
│   ├── analysis-and-actions.md      # 需求覆盖、归因与修改落点
│   └── practice-integration.md      # 按需落地、接入和维护
├── scripts/
│   └── build_index.py               # 本地索引器
├── tests/
│   └── test_build_index.py          # 合成数据测试
├── examples/snapshots/              # 匿名示例
├── examples/practice-cases.md       # 三个虚构落地案例
├── agents/openai.yaml               # 客户端展示元数据
├── .github/workflows/test.yml       # Python 3.10–3.13 CI
├── assets/readme/                   # 品牌图标、赞赏码与素材说明
├── assets/templates/                # 按需使用的记忆与项目入口模板
├── LICENSE
├── README.en.md                    # 英文说明
└── README.md
```

## 开发与测试

```bash
python -B -m unittest discover -s tests -v
```

修改索引器或输入契约时，至少检查以下场景：

- 半开时间窗的两个边界；
- 相同 ID 内容冲突时停止写入；
- 缺失消息 ID、缺失时间和开放回合被保留并披露；
- 注入上下文与真实用户要求分开；
- 摘要截断后仍保留来源哈希与消息定位；
- 非法标题、文本块和字段返回简短错误，在创建输出目录前停止；
- 开放回合的采集时间冲突不随文件名排序而改变结果；
- 时间缺失时不虚构跨回合反馈，正常顺序和同回合反馈仍保留；
- 合法非文本块有明确忽略计数。

磁盘写入故障仍可能留下未完成目录；只有 `manifest.json` 的 `status=complete` 才表示全部产物已写入。

GitHub Actions 会运行同一套测试和匿名示例索引。CI 配置只有在首次推送后才会在 GitHub 上实际执行。

## 贡献

欢迎提交问题、文档修正、输入适配器和测试用例。提交前请：

1. 使用虚构或已获授权的材料；
2. 不提交真实对话、账号、密钥或个人机器路径；
3. 为新行为补充有针对性的测试；
4. 在 PR 中说明输入、预期结果和实际验证范围。

如果你在某种平台上导出了新格式，请先描述字段含义，并在适配器中标明截断、分页和时间精度。

## 参考与致谢

本项目参考了 [Claudeception](https://github.com/blader/Claudeception) 对可复用经验和触发条件的要求，以及 [conversation-distiller](https://github.com/CS-Faith/conversation-distiller) 的结构化知识与索引思路。代码和文档为独立实现，没有复制这些项目的源码；上游效果和节省声明未在此复现。

## 许可证

原创代码和文档使用 [MIT](LICENSE)。第三方名称、商标、图标和徽章的权利归各自权利人，项目 MIT 许可不授予这些品牌的权利；素材来源和使用范围见 [素材说明](assets/readme/ATTRIBUTION.md)。

<a id="sponsor"></a>
## 赞助商

<h3><img src="assets/readme/fastai-icon.png" alt="FastAI 图标" height="34" align="middle"> FastAI · 模型赞助商</h3>

如果你正在寻找稳定、实惠的 AI 模型中转服务，可以看看 [FastAI](https://www.fastaitoken.com/register?aff=BF9KNKFHX725&promo=WSSFK&utm=trace-to-practice)。它支持 DeepSeek、GLM、Kimi、GPT、Claude 等模型，也提供图片与视频生成能力；国模分组采用大厂自部署模型，注册即送 3 美元体验金。具体套餐、可用模型和服务质量以 FastAI 页面为准。

通过上方链接注册或充值，作者会获得返利，用于继续维护本项目。赞助不影响技能功能、分析结论和推荐，也不代表对服务质量的背书。

<p align="center">
  <a href="https://www.fastaitoken.com/register?aff=BF9KNKFHX725&amp;promo=WSSFK&amp;utm=trace-to-practice">
    <img src="https://img.shields.io/badge/FastAI-%E6%B3%A8%E5%86%8C%E4%B8%8E%E4%BD%93%E9%AA%8C-4F7CFF?style=for-the-badge" alt="FastAI 注册与体验">
  </a>
</p>

<a id="support"></a>
## 赞助本项目

如果这个技能帮你节省了整理历史的时间，可以请作者喝杯咖啡。赞助是自愿支持，不代表购买服务、功能优先权或定制承诺。

<p align="center">
  <img src="assets/readme/wechat-sponsor-qr.png" alt="微信赞赏码" width="320">
</p>

感谢每一位提交问题、补充测试、分享使用经验和支持开发的人。
