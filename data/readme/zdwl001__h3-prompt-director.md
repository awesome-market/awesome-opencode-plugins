# H3 Prompt Director

[简体中文](README.md) | [English](README.en.md)

把一篇故事、小说、剧本或人物设定，变成**一份可直接投喂 MiniMax H3 Ref2VA（R2V）的分镜与提示词交付文件**。

它不只是一段提示词，而是从故事到成片的完整工作流：拆镜头、算时长、装箱分段、出资产表、写六段提示词、过质检。默认面向 ComfyUI 本地 Ref2VA 工作流 + `MiniMaxH3AddGuide` 跨段接续。

> 这是围绕 MiniMax H3 的独立工作流层，不是官方项目，也不隶属于 MiniMax。

## 它解决什么

官方 `h3-prompt-writing` 解决“怎么写一条 H3 提示词”：字段、标签、语法、参考关系。

本 skill 解决官方不管的那一层：

- 一篇几千字的故事，怎么拆成可拍的镜头；
- 每个镜头多长，怎么装进 3.75–14.38 秒的生成段；
- 跨段的 22 帧怎么接，尾音频怎么锚定；
- 角色、场景、道具、音色怎么变成可复用的资产；
- 每段的六段提示词怎么和连接清单一一对应；
- 写完之后，按哪张清单质检、出问题怎么排障。

## 核心能力

| 能力 | 说明 |
|---|---|
| 六阶段流程 | 故事解析 → 分镜与时长预算 → 分段装箱 → 一致性资产 → 提示词成文 → 质检与交付 |
| 双通道 | R2V 参考输入（`<Subject N>` / `<Picture N>` / `<Video N>` / `<Audio N>`）与 AddGuide 引导通道分离，引导片段不占标签 |
| 接段模式 B | 上一段末 22 帧 → 本段 AddGuide image（`frame_idx=0`）+ 同源尾音频；成片拼接裁前 22 帧 |
| 时长网格 | 24 FPS 下 17k+5 帧，3.75–14.38 秒；时间戳与总览表严格一致 |
| 装箱三原子性 | 镜头不跨段、连续对白不跨段、每段参考 ≤9 图 / 3 视频 / 3 音频 |
| 资产规范 | 角色多视图、12 格场景图、道具多形态图、音色参考音频 |
| 质检与排障 | 完整检查清单 + 故障速查表 + 级联重生成规则 |

## 快速开始

### 1. 安装 skill

**Cherry Studio**

把整个目录复制到：

```
<CherryStudio Data>/Skills/h3-prompt-director/
```

Cherry 会自动同步技能目录。

**Claude Code / 其他 agent**

放到用户级或项目级 skills 目录：

```bash
# 用户级
cp -r h3-prompt-director ~/.claude/skills/

# 或项目级
cp -r h3-prompt-director .claude/skills/
```

任何能读取 `SKILL.md` 与本地文件的 agent 都可以使用。

### 2. 拉取官方语法文档

官方三文档不随本仓库分发（原因见 [references/official/README.md](references/official/README.md)）。在仓库根目录运行：

```bash
bash scripts/fetch-official.sh
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/fetch-official.ps1
```

脚本会要求确认接受 MiniMax H3 Community License，然后把 `official-skill.md`、`base-en.txt`、`ref-en.txt` 下载到 `references/official/`。这些文件已被 `.gitignore` 忽略。

### 3. 给故事

```
把下面这个故事做成 H3 视频提示词，按 h3-prompt-director 的流程走：

清晨的湖边，老渔夫阿禾收起最后一张渔网。网里只有一片枯叶。
他怔了一下，把枯叶放回水里，低声说：“又是空网。”然后摇橹离开。
```

skill 会产出**一个 Markdown 文件**，包含：

1. 改编说明、全局参数、决策记录
2. 解析与分镜计划表（人物 / 场景 / 镜头 / 形态变化 / 台词核算）
3. 总览表（段号、镜头构成、网格时长、参考槽位、引导来源）
4. 资产表（含每张图的生图提示词或用户提供标记）
5. 逐段区块（参数、连接清单、说话人映射、六段提示词、拼接说明）
6. 跨段终检结论

完整示例见 [`examples/`](examples/)。

## 输出示例

每段提示词固定六节：

```text
subject_definitions:
...

summary:
[reference generation] ...

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2]): fully_preserved - ...

detailed_description:
[Shot 1] ...
[Shot 2] At 00:03.500, ...

overall_soundscape:
...

non_diegetic_music:
...
```

## 目录结构

```
h3-prompt-director/
├── SKILL.md                     # 触发描述 + 六阶段 + 不变量 + 文件路由
├── references/
│   ├── 00-workflow.md           # 流程、装箱、交付结构、完整质检清单
│   ├── 01-grammar.md            # Ref2VA 语法底线、时长网格、节点参数
│   ├── 02-assets.md … 09-transition.md
│   ├── 10-troubleshooting.md
│   └── official/                # 官方三文档（安装时拉取，不随仓库分发）
├── assets/delivery-template.md  # 交付文件骨架
├── scripts/                     # 官方文档拉取脚本（bash / PowerShell）
└── examples/                    # 完整交付示例
```

## 兼容性

- 不依赖 MiniMax Hub、外部 API 或在线知识库；
- 只需本地文件读写工具；
- 可在 Cherry Studio、Claude Code、Claude Agent SDK、Cursor、Windsurf 或任何读取 `SKILL.md` 的 harness 中运行；
- 生成执行端为 ComfyUI 本地 Ref2VA + `MiniMaxH3AddGuide`；skill 只负责产出提示词文本。

## 官方文档与许可

- 官方仓库：https://github.com/MiniMax-AI/MiniMax-H3
- 官方文档适用 **MiniMax H3 Community License Agreement**：https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE
- 该协议授权范围限于 Applicable Territory（全球排除欧盟、英国、韩国、美国），并对再分发设有条件。本仓库因此不直接收录官方三文档，改为安装时从官方仓库拉取。
- 本仓库的 MIT 许可**不覆盖**官方文档；官方文档的使用与再分发以该协议为准。

## License

本仓库中的原创内容（`SKILL.md`、`references/00`–`10`、`assets/`、`scripts/`、`examples/`、文档）采用 [MIT License](LICENSE)。

第三方材料与商标归其各自权利人所有。详见 [NOTICE](NOTICE)。

## 贡献

欢迎 issue 与 PR。修改规范时请保持 `references/` 的逐字稳定；需要澄清规则时，优先写进 `SKILL.md` 的“最容易踩”或 `references/README.md` 的说明，而不是改动原文。新增示例请确认不含个人路径、项目名或密钥。

## 免责声明

- 本项目与 MiniMax 无隶属、 endorsement 或赞助关系。
- ComfyUI 节点接线、模型选择、生成参数与最终成片质量由使用者自行负责。
- 生成内容的使用需遵守当地法律、平台规则与 MiniMax H3 Community License Agreement。
