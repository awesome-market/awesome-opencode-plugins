<div align="center">

# 🎬 漫剧老李 · H3 短剧全流程导演

## **v2.1.1** · forest-laoli-h3

> 🎥 面向 **MiniMax H3（海螺 3.0）** 的短剧工业化导演中枢
> 剧本 → 资产参考图 → H3 分镜 → 三字段 / 六段式投喂稿 → 机检 → 交付包，一条链走完
> 🧩 **通用型**：不绑定渲染平台、生产机与队列接口，只交**平台无关的纯文本载荷 + 投喂包**
> 📐 画幅推荐 **9:16 竖屏**；**16:9 横屏实测同样可用**，全片一个画幅，禁 `auto`

![Version](https://img.shields.io/badge/版本-v2.1.1-6a5acd)
![Rulebooks](https://img.shields.io/badge/规则库-20%20份-00b4d8)
![QC](https://img.shields.io/badge/机检-H1~H36-ff6b6b)
![Tests](https://img.shields.io/badge/用例-29%2F29%20零放水-2ec4b6)
![Model](https://img.shields.io/badge/模型-MiniMax%20H3-9d4edd)
![Aspect](https://img.shields.io/badge/画幅-9%3A16%20推荐%20%7C%2016%3A9%20可用-ff9f43)
![Platform](https://img.shields.io/badge/平台-通用%20%7C%20不绑定渲染端-00b4d8)
![Stars](https://img.shields.io/github/stars/lixiaoxiao9888-create/forest-laoli-h3?style=social)

**简体中文** ｜ [English](README.en.md)

---

### 🎬 短剧生产管线

```
G0 锁 → ① 剧本 → ② 资产 → ③ 分镜 → ④ H3 编译 → ⑤ 清洗机检 → ⑥ 交付
        (G1)      (G2)      (G3)       (G4)          (G5)          (G6)
```

</div>

---

## 🧭 这是什么

一套 **给 AI 助手执行的 H3 短剧规则库**（OpenClaw Skill / Agent 技能包），不是提示词模板合集——把 `SKILL.md` 与 `references/` 放进 Agent 技能目录即可调用。

**只做一件事：把短剧从文字做到能投进 MiniMax H3 的成片级提示稿与投喂包。**

它不负责"写得好看"，负责**写得能跑**——H3 对词根极度敏感、每段独立生成零记忆、遇到某些动作组合会直接卡死。这套规则把这些坑全部前置成可检查的门。

> **人格**：漫剧老李（漫剧老李系）。包名 `forest-laoli-h3`：`forest` = 森林，`laoli` = 老李，`h3` = 这一包只做 H3。
>
> ⚠️ **非官方项目**：与 MiniMax 官方无隶属关系。字段规范参考官方开源仓库，规则与真机实证为本包原创；测试版，二次修改整合开源内容。
>
> 🔎 **关键词**：MiniMax H3 提示词 · 海螺 3.0 / Hailuo 3.0 短剧 · H3 分镜脚本 · Ref2VA 六段式 · T2VA 三字段 · 参考图图槽 · 越轴 · 站位 · 词根清洗 · 氛围层 · AI 短剧制作 · AI 漫剧 · 提示词工程 · 机检 · OpenClaw Skill

## 🚫 它治什么病

| 症状 | 病根 | 规矩 |
|---|---|---|
| **写"不要越轴"，它去画一条轴** | H3 按词找画面，否定词会被丢弃、词根会被渲染 | 五遍词根清洗 + H13/H14：分号后禁否定词、镜头术语、抽象评价、心理动词、比喻、声音词 |
| **写"压迫感"，出来只会皱眉眯眼** | 抽象词 = 通用滤镜，回落到训练集平均值 | 情绪必须落成**四区肌肉**（眉·眼·口·颌可见动作）+ 可见计数，30 种短剧情绪英文配方 |
| **画面有物件、有动作，就是没有空气** | 参考图只锁"长什么样"，锁不住"被什么光照着" | **三层分工**：外形锁图、空间锁位、氛围写到死；段首氛围六件套 + H35 |
| **段与段接不上、人物越跑越不像** | H3 每段零记忆 | 全片固定 **9 图槽**（每段全挂不省图）+ 段首空间锚点卡复述 + 镜末正向维持句 + 末镜 1 秒定格；省图会整体错位（H36） |
| **门自己提前开了 / 单扇门分裂成双扇门** | 跨镜结果词抢跑、段首把动态门死锁成 `fully_preserved` | 门窗状态锁：未开门段全程 `stays shut`；段末有门状态变化 → 场景标 `partially_preserved`（H31） |
| **一个人变成两个（左右两个林昭）** | 段内依托物跳变 + 同框第三人带旁观动词触发图层复制 | 同框人数硬锁（一镜最多两人）+ 段内依托物唯一锁（H30/H32） |
| **门内人背对镜头敲自己家的门** | 画外敲门动词被 H3 绑定给画面唯一人物 | 画外声源动作隔离：门外动作只进 `overall_soundscape`，正文只写门内可见受迫结果（H31） |
| **人物穿门时半透明融化蒸发** | 人穿过门洞/窗洞触发 alpha 消融 | 禁穿门动作，改"停在门内扶门"或只拍门自己关上（H29） |
| **卡在 76%、成片冻帧** | 全蹲低姿态 + 窄缝穿物动态过程触发物理推理死锁 | 高危物理死锁禁区：半蹲/弯腰 + 结果态静置（H33） |
| **横屏项目被判成违规 / 段间换画幅** | 画幅写进正文、写成 `auto`、或全角冒号漏检 | 画幅只进载荷 `aspect_ratio`；全片一个画幅；机检吃 `9:16` / `9：16` / `16x9` 并统一归一（H14） |

## ⚡ 核心机制速览

- **六阶段门控**：G0 锁 → 剧本 → 资产 → 分镜 → H3 编译 → 清洗机检 → 交付，每阶段有交付物与放行门；
- **双 checkpoint 路由**：`H3-Base-FL2VA`（零/一/两图 → 三字段）· `H3-Base-Ref2VA`（多模态参考 → 六段式），字段顺序固定；
- **五遍词根清洗**：否定根 / 元描述 / 镜头术语 / 情绪结论 / 声音硬根，逐层剥除后正文只剩可见事实；
- **H1–H36 机检**：`h3_lint.py` 支持单段、多段合稿自动切分、交付清单数组、BOM 容错、`9：16`/`16x9` 归一化，跨段图槽一致性（H34）与槽位越界（H36）；
- **交付即剥壳**：正文去 Markdown 外壳出 `.txt` + 图槽表 + 清单 JSON，平台无关，灌官方 API / 自建 H3-Base / ComfyUI / 任意客户端都行；
- **29 个零放水用例 + 文档自检**：`run_tests.py` 跑基线，`check_docs.py` 防版本串、条目数漂移与跨文件死链。

## 📂 文件架构

```
forest-laoli-h3/
├── SKILL.md                                     总控：定位边界 · 六阶段 · 六项锁 · 铁律 · 机检索引
├── CHANGELOG.md                                 版本变更记录（v2.0 → v2.1.0）
├── references/                                  20 份执行级规则库（全量自包含 · 零外部依赖）
│   ├── checklist.md                             62 项出稿前必查清单
│   ├── gates.md                                 P0 阻断 25 条 / P1 修复 16 条 / P2 优化 7 条
│   ├── diagnose.md                              50 条症状 D01–D50 + 卡死四维排查树
│   ├── delivery.md                              剥壳硬规矩 · 图槽铁律 · 清单 JSON · 出片三关复检
│   ├── spatial-anchor-and-hold.md               空间锚点卡 · 维持句 · 动作预算 · 站位/门窗/分身专治
│   ├── atmosphere-and-light.md                  氛围层三层分工 · 段首六件套 · 国漫 3D 正词表
│   ├── camera-four-axis-h3.md                   八档四轴 · 回合制切镜 · 神态动作双挂
│   ├── camera-movement.md                       22 种运镜物理刻度 · 运镜收敛铁律 · 竖/横画幅句式
│   ├── h3-shot-grammar.md                       景别机位运镜 · 越轴正向不变式 · 站位四要素
│   ├── dialogue-density.md                      台词铺轨 · 3.3 字/秒标定 · 一镜一句
│   ├── acting-facs.md / acting-recipes.md / acting-listen.md   四区肌肉 · 30 种情绪配方 · 听戏五步
│   ├── h3-lexicon-cleanup.md                    词根黑名单 · 九条改写公式 · 五遍清洗流程
│   ├── h3-format.md                             三字段 / 六段式官方规格
│   ├── h3-constraints-qc.md                     H1–H36 硬约束对照
│   ├── script-layer.md / asset-layer.md         带刺活人话四式 · 三视图与 9 图固定槽
│   ├── pipeline.md / examples.md                全流程拆段 · 完整正反例
├── scripts/
│   ├── h3_lint.py                               H1–H36 机检（单段 / 多段 / 清单 JSON）
│   └── tests/                                   29 个用例 + run_tests.py 基线 + check_docs.py 文档自检
├── README.md / README.en.md
└── LICENSE
```

## 🚀 快速开始

```bash
git clone https://github.com/lixiaoxiao9888-create/forest-laoli-h3.git
```

把 `forest-laoli-h3/` 整个目录放进你的 Agent 技能目录（如 `~/.openclaw/workspace/skills/`、Claude Code 的 `skills/`），或直接用 skills CLI 安装：

```bash
npx skills add https://github.com/lixiaoxiao9888-create/forest-laoli-h3 --skill forest-laoli-h3
```

**出稿后先机检（三条命令，复制即用）：**

```bash
# ① 单段 / 多段合稿（自动切段）
python scripts/h3_lint.py 稿子.md --duration 12

# ② 横屏项目显式声明画幅
python scripts/h3_lint.py 稿子.md --duration 12 --aspect 16:9

# ③ 交付清单数组（自动读同目录 .txt + 取 aspect + 逐段查 H36 图槽越界）
python scripts/h3_lint.py 清单.json --json
```

> **判读**：`FAIL` 必须清零；`WARN` 逐条修正或写明为什么留。
> **退出码**：`0` 无 FAIL / `1` 有 FAIL / `2` 输入问题（文件不存在、空稿、坏 JSON）——可直接接 CI。
> **清单与 txt 必须放同一目录**：条目里没写 `prompt` 时，机检会去读 `file` 指向的 `.txt`。

**改完规则先跑基线：**

```bash
python scripts/tests/run_tests.py     # 29 个用例，正例全绿、反例精准命中
python scripts/tests/check_docs.py    # 机检码缺号 / 条目数漂移 / 死链
```

## 🔒 G0 六项锁（缺一项就停下来问，不许默认）

| 锁 | 取值 | 默认 |
|---|---|---|
| **A 模式** | T2VA / I2VA / L2VA / FL2VA / Ref2VA | **Ref2VA** |
| **B 时长档** | 4 / 5 / 8 / 10 / 12 / 15 秒 | 按节拍定，一般 8–15s |
| **C 画风基底** | BASE_LIVE 真人 / BASE_ANIME 3D·半写实 / BASE_2D 手绘 / BASE_INK 水墨 | **未定不许动手** |
| **D 资产形态** | M1 文字档 / M2 已锁参考图 | M1 起步，有图升 M2 |
| **E 段缝** | 尾帧锚定 / 换机位硬切 / 空镜过渡 | 情绪顶点尾帧锚，文戏慢段空镜 |
| **F 空间锚点** | 全片一张锚点卡：家具清单 + 座位/站位表 + 三个方位词 + 门窗初始开闭态 | **未钉不许动手** |

**画幅不是死锁，是推荐档**：默认 `9:16` 竖屏；`16:9` 横屏实测同样可用（横屏项目、双人并置、空间全景更好使）。三条规矩——全片一个画幅、禁 `auto`/`adaptive`、画幅只进载荷不进正文。

## 🎛️ 模式路由（H3 只有两个 checkpoint）

| checkpoint | 输入 | 场景 | 输出 |
|---|---|---|---|
| `H3-Base-FL2VA` | 零图 | 纯文本段（T2VA） | 三字段 |
| `H3-Base-FL2VA` | 一图 | 首帧（I2VA）/ 尾帧（L2VA） | 指令行 + 三字段 |
| `H3-Base-FL2VA` | 两图 | 首尾帧（FL2VA） | 指令行 + 三字段 |
| `H3-Base-Ref2VA` | 多模态参考 | 角色三视图 + 场景主视角 + 道具（Ref2VA） | **六段式** |

- **三字段**：`integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music`
- **六段式**：`subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music`

## ✅ 机检 H1–H36

| 组 | 覆盖 | 级别 |
|---|---|---|
| H1–H3 | 字段完整与六段顺序、时间戳递增、绑定切镜词、时长 4–15s | FAIL |
| H4–H7 | 正文全英文 + `<d>` 语言标签、标签定义与引用、保留度合法 | FAIL/WARN |
| H8–H12 | 栏名/符号清洗、画外声固定短语 + 闭口证据、声音分层、首镜具名主体 | FAIL/WARN |
| H13–H14 | **词根清洗**、**画幅全片一致**（9:16 推荐 / 16:9 可用；`auto` 或混用 FAIL，未声明 WARN） | FAIL/WARN |
| H15–H19 | 运镜物理刻度量、禁用运镜、运镜×景别矛盾、连续同运镜 | FAIL/WARN |
| H20–H22 | 台词密度、回合制换嘴切镜、道具物理接地 | WARN |
| H23–H25 | 镜行词数上限（>100 词 FAIL）、维持句、单镜过薄 | FAIL/WARN |
| H26–H28 | 同性别多说话人声学反差、末镜定格、空间尺度膨胀 | WARN |
| H29–H33 | 穿门融化、同框分身、门窗状态锁与画外敲门污染、依托物跳变、高危物理死锁 | WARN |
| H34 | 跨段 `Picture N` 图槽一致性 | FAIL |
| H35 | **氛围层缺失**（光位 / 空气介质 / 前景景深缺两类以上） | WARN |
| H36 | **图槽越界**（正文最大 `Picture N` > `images` 张数，或槽位为空） | FAIL |

## 🩺 片子跑崩了、一直卡着怎么办

1. **卡住（0% / 76%）**：按四维排查树（`diagnose.md §十`）定位——① 图槽省图错位/素材贴反 ② 渲染端排队/限流/会话未建（**属渲染端，本包不管**）③ 真卡审核 ④ 物理推理死锁（H33）。本包只保证 ①③④ 这三类"稿子本身"的病查得出。
2. **画面崩坏**：取证（哪段哪镜）→ 查 D01–D50 症状码 → 只改病灶句 → 机检复验零新增。

## 📌 边界

- **只做短剧**：不接广告片、产品片、品牌宣传、MV、游戏片头；
- **通用型，不绑定渲染端**：产出是纯文本载荷 + 投喂包（剥壳 `.txt` + 图槽表 + 清单 JSON），跑片、排队、并发、账号容量是你所用渲染端的事，本包不带任何推送脚本；
- **平台规格不越界**：红果/抖音的"单集 60–90 秒、付费卡点"只指导剧本层，H3 生成层只认 4–15 秒的独立生成单元；
- **不假装有记忆**：跨段连续靠图槽、锚点卡、维持句与定格句硬接，不靠模型自洽；
- **本包不持有图**：参考图由你在外部平台生成，本包含生图词与 9 图槽表。

## 🙏 致谢

规则底座参考 MiniMax H3 官方提示指南（`base-en` / `ref-en`）与 MiniMax-H3 开源仓库的字段规范；打戏与分镜方法论吸收自「漫剧老李」Short-Drama Director Suite V7.4.26。真机实证部分（《门后》段 01–04、H29–H33）与 v2.0 通用化改造为本包原创。

## 📄 License

[MIT](LICENSE)
