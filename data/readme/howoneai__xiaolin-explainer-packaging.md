# xiaolin-explainer-packaging

把出镜口播片段包装成小Lin说风格讲解视频的 agent skill，内含一套 Remotion 渲染引擎。

An agent skill with a Remotion engine. It turns talking-head clips into explainer videos in the visual style of the Chinese finance channel 小Lin说 (Xiao Lin Shuo). This is an unofficial project. It is not affiliated with or endorsed by the creator.

## 声明

- 这是非官方项目。它与小Lin说及其团队无关，没有得到授权或认可。"小Lin说"只用来描述视觉风格。
- 仓库不含她的视频、截图、肖像、声音或台标。演示画面里的出镜位置是占位色块。
- 成片默认带"AI生成 · 实验作品 · 非本人"标注。请保留这个标注。
- 不要用真实创作者的肖像或声音生成出镜画面后公开发布。不要把成片当成本人作品发布。
- 网页截图和 Logo 由使用者在自己的工程里抓取，仓库不含。Logo 是各公司的商标，只在讲到这个产品时用来指代它。截图里的新闻图片社照片要模糊掉。

## 效果

![9 种版式（默认的财经·剪纸印刷主题）](docs/layouts.jpg)

![卡片墙动效：镜头跟到当前项，当前项亮起，其余压暗并虚化](docs/demo_wall.gif)

上面的画面都来自 `--demo` 演示工程。数据是演示数据。

### 每期按选题定制画法（v1.4）

![同一组版式：上排只有骨架（v1.3），下排压在选题照片上、放了本期道具（v1.4）](docs/treat_before_after.jpg)

版式只是骨架，管坐标轴、箭头、扇区、航线和入场节奏。每期还要定画法：图形压在选题的真实照片上（Wikimedia Commons 自由许可，画面上带署名），再放为这一期生成的道具，让道具承担意思。讲咖啡豆涨价，就让咖啡豆小人骑在折线头上往上爬；讲一杯咖啡的成本，就把拿铁切成饼图；讲产地，就让货轮沿航线开。

![画法演示：咖啡选题 6 个场景和 OpenClaw 选题 3 个场景](docs/treat_grid.jpg)

![换一个选题，画法完全不同：龙虾管家把收件箱一封封扔进垃圾桶](docs/demo_inbox.gif)

换选题时骨架可以一样，画法要重做。OpenClaw 选题里，"36.8% 的 skill 有漏洞"画成 100 个 skill 包里有 37 个变成冒毒液的包；"接进 20 多个聊天软件"画成龙虾管家居中、信封从四周的平台流过来。做法、道具提示词和素材槽写在 `references/treatment.md`，示例在 `templates/scenes_treat.py`。

### 8 种扩展版式（v1.3）

![8 种扩展版式（财经·剪纸印刷主题）：折线图、时间轴、饼图和环形图、流程图、树状拆解、世界地图、左右对比、关系图](docs/layouts7.jpg)

![世界地图：国家上色，航线弧线画出后有圆点沿线流动，节点脉冲](docs/demo_map.gif)

每个版式都读主题，6 套主题下都能直接用。讲到哪一项，哪一项就亮起，其余压暗。折线图可以跟着台词分段画（`reveal`），讲到哪一年就画到哪一年。示例在 `templates/scenes_gallery.py`。这里只有骨架，做片时要按上一节加画法。

### 6 套主题（v1.2）

![同一份演示分镜在 6 套主题下的样子：片名、巨型数字、章节、卡片墙、文档页、公式条、计算器](docs/themes.jpg)

在 `project.json` 里写 `"theme": "press"` 这样一个词，整片的底图、纸张和屏幕材质、字体、卡片、片名卡和片尾卡一起换，分镜代码不用改。

| 主题 | 适合 | 样子 |
|---|---|---|
| `finance`（默认）· 剪纸印刷 | 财经、民生、政策 | 暖灰底、剪纸色块、钞票边框、粉笔涂鸦，优设标题黑 |
| `press` · 报刊纸本 | 历史、人文、社会、国际 | 旧报纸拼贴、牛皮纸、撕边纸条和胶带，网点印刷的红色数字，宋体 |
| `blueprint` · 工程蓝图 | AI、软件、互联网、工程 | 蓝晒图纸、白色机械线稿、橙色尺寸线、图钉卡片 |
| `terminal` · 复古终端 | 网络安全、编程史、游戏 | CRT 显示器外框和扫描线、荧光字、Win95 窗口，像素字体 |
| `desk` · 桌面实物 | 生活、消费、个人理财、教程 | 胡桃木桌面、索引卡、便签，手写字体 |
| `editorial` · 现代杂志 | 品牌、商业、通用 | 米白纸面、超大粗黑体、单一品牌蓝 |

### 真实素材

![OpenClaw 测试片（蓝图主题）：片名、巨型数字、真实 Logo、图标砖墙、真实网页截图和片尾](docs/openclaw_blueprint.jpg)

![网页截图：荧光笔、下划线和聚光跟着台词出现，镜头推到当前这句](docs/demo_webshot.gif)

这两组画面来自一支测试片。测试片用 Wikimedia Commons 上林亦LYi 的《一个视频搞懂OpenClaw！》（CC BY 4.0）重新剪辑包装，本身不在仓库里。截图里是 PCMag、star-history 和 GitHub 的公开页面，PCMag 头图（Getty Images）已经模糊处理。

## 能做什么

输入是两样东西：每句台词一段 1920×1080 的出镜 mp4，以及每句的朗读文本和字幕文本。输出是讲解画面、字幕、转场、配乐和音效合成后的成片。

| 部分 | 内容 |
|---|---|
| 主版式 | 巨型数字 `bignum`、卡片墙 `wall`、白卡图表 `paper`、整页文档加荧光笔 `docpage`、真实网页截图 `webshot`（浏览器外框，荧光笔、下划线、红框、聚光，跟着台词滚动）、实体卡 `ent6`、大公式条 `formula6`、白底计算器 `ui` |
| 扩展版式 | 折线图 `line6`、时间轴 `timeline6`、饼图和环形图 `pie6`、流程图 `flow6`、树状拆解 `tree6`、世界地图 `map6`（国家上色、航线、脉冲点）、左右对比 `vs6`、关系图 `graph6`（持股、资金流） |
| 画法 | 版式当骨架，每期按选题定制：照片背景（压暗、虚化、慢推）、为本期生成的道具（`prop`：待机动作、沿路径移动、成串流动）、象形图 `stack6`（道具堆成柱，或网格里一部分换图），以及每个骨架上的素材槽（骑在线头的道具、切成扇区的实物、沿航线开的载具、角色节点、沿边流动的道具）。道具提示词按主题画风分 6 套 |
| 主题 | 6 套：`finance`（默认）、`press`、`blueprint`、`terminal`、`desk`、`editorial`。每套有自己的底图、纸张或屏幕纹理、字体、卡片材质、片名卡和片尾卡。在 `project.json` 里切换，单个场景可以换底图 |
| 其他元素 | 片名卡、章节卡、片尾卡、照片卡、真实 Logo 片 `logo`、图标砖墙 `tiles`、标签、小人、金币流、印章、弹幕、对话气泡、手绘圈等约 25 种；25 个 2.5D 图标和 12 个图标方块 |
| 计时 | 元素入场对齐台词关键词：`S.k('关键词', -0.15)` |
| 镜头和转场 | 镜头跟随当前项；场景间自动分配推拉、甩镜、推移、闪白、旋转推近 |
| 画中画 | 全屏、圆形、矩形三种 |
| 声音 | 人声、配乐、合成音效（嗖声、重击声等）混音，响度归一到 -16 LUFS |
| 资料检索 | 每种版式要查的资料、来源分级、事实文件模板；Wikimedia Commons 自由许可照片的搜索和下载脚本，自动生成署名 |
| 真实素材 | `web_shot.mjs`：用无头 Chrome 截网页，输出原文短语的像素坐标给荧光笔定位，能把指定段落滚进画面、模糊图片社照片；`commons_logo.py`：从 Wikimedia Commons 下载 Logo 并记录许可。拍历史版本的方法（GitHub 历史提交、Wayback 存档）写在 `research.md` |
| 质检 | 关键帧审片拼图；整片视频帧和静帧逐帧对比 |

风格规则写在 `references/style-bible.md`。规则来自对她 5 期公开视频的逐帧拆解，例如"主体要被画面边缘裁切，或者占画面 60% 以上""每 2–3 个深色场景插 1 个白纸场景"。

## 不做什么

- 不生成出镜画面。出镜片段要用别的工具生成或自己拍摄。
- 不写口播稿。
- 骨架（图形语言）只有这一套。主题换的是材质、底图、字体和片名片尾；骨架本身要改组件代码。
- 道具不随选题自动生成。在 Manus 里用图像生成工具按 `treatment.md` 的提示词生成；没有图像生成工具时，要自己准备透明 PNG。
- 不录屏，也不下载平台上的视频。网页截图是静态长图，靠滚动和镜头运动做出动感。
- 只支持 1920×1080、24 帧。
- 国旗只有 6 个：智利、中国、德国、法国、日本、美国。
- 世界地图是 Natural Earth 1:1.1 亿的低精度示意图，不符合中国大陆公开出版地图的审核要求。涉及中国疆域时，请改用自然资源部标准地图服务系统的图片，并标注审图号。

## 安装

### Manus

1. 从 [Releases](../../releases) 下载 `xiaolin-explainer-packaging.skill`。
2. 在 Manus 里把这个文件添加为技能。
3. 对 Manus 说："用 xiaolin-explainer-packaging，给 `<目录>` 里的口播片段做讲解包装，台词在 `<文件>`。"开工前，Manus 会先问三件事：有没有固定在用的底图、台标怎么定、有没有指定要放的真实素材。

### 其他支持 SKILL.md 的 agent

把 `xiaolin-explainer-packaging/` 文件夹复制到该 agent 的 skills 目录，例如 Claude Code 的 `~/.claude/skills/`。这种用法未测试。

### 不用 agent，直接用引擎

先准备环境：

- Node 18 或更高版本、ffmpeg、python3（带 numpy 和 Pillow）。
- `npm install` 和第一次渲染要联网。第一次渲染时，Remotion 会下载 Chrome。
- 只在 macOS（Apple Silicon）上测试过。其他系统默认用软件渲染 `swangle`，可以用环境变量 `REMOTION_GL` 改。

然后跑演示工程：

```bash
git clone https://github.com/howoneai/xiaolin-explainer-packaging.git
S=$PWD/xiaolin-explainer-packaging/xiaolin-explainer-packaging
bash $S/scripts/new_project.sh demo --demo        # 复制引擎、生成 4 段假出镜、npm install
cd demo
python3 story_core.py timeline.json scenes.py     # 生成分镜数据，应输出 gaps/overlaps []
python3 -c "import json;print(' '.join(str(f) for _,f in json.load(open('keyframes.json'))))" | xargs node render.mjs stills stills/k1
python3 $S/scripts/sheet.py stills/k1 keyframes.json 6   # 关键帧审片拼图
bash $S/scripts/render_chunks.sh video.mp4        # 整片
python3 $S/scripts/mix_audio.py timeline.json mix_raw.wav
bash $S/scripts/finalize.sh video.mp4 mix_raw.wav final.mp4
python3 $S/scripts/audit.py video.mp4 72          # 逐帧质检，flagged 应为 0
python3 story_core.py timeline_gallery.json scenes_gallery.py   # 换成 8 种扩展版式的图鉴（只有骨架）
python3 story_core.py timeline_treat.json scenes_treat.py       # 换成画法演示（咖啡和 OpenClaw 两个选题）
```

做自己的视频时，按 `SKILL.md` 的步骤走：开工确认（底图、台标、真实素材）、准备输入、建工程、规划场景和画法、查资料并备齐照片和道具、写分镜、关键帧审片、整片质检。分镜写法从 `templates/scenes_treat.py` 复制。参数见 `references/layouts.md` 和 `references/storyboard-api.md`。

### 字体：优设标题黑

`finance` 主题的标题和所有主题的字幕都用优设标题黑。它的官网允许免费商用，但没有写允许再分发，所以仓库不带这个字体。

请从 https://www.uisdc.com/uisdc-first-free-font 下载，再存为工程里的 `public/fonts/YouShe.ttf`。另一种方法是设置环境变量 `YOUSHE_TTF` 指向字体文件，`new_project.sh` 会自动复制。缺这个字体时，标题和字幕回退到思源黑体 900 字重，没有斜切，风格会明显变弱。

## 目录

```
xiaolin-explainer-packaging/
├── SKILL.md                    工作流、审片清单、已知陷阱
├── references/
│   ├── style-bible.md          图形语言、硬规则、色板、字体、转场、声音电平
│   ├── treatment.md            每期按选题定制画法：设计表、照片背景、道具提示词、素材槽
│   ├── layouts.md              每个版式的参数和示例
│   ├── storyboard-api.md       timeline.json 格式、分镜 API、渲染命令
│   └── research.md             资料检索规范、网页截图和 Logo、图片和商标权利
├── scripts/                    new_project、render_chunks、mix_audio、finalize、sheet、audit、commons_photo、commons_logo、web_shot、build_world
└── templates/
    ├── engine/                 Remotion 工程（src/、src/geo 地图数据、public/fonts、public/icons、public/plates 底图、public/tex 纹理）
    ├── scenes_example.py       覆盖 7 种主版式的示例分镜
    ├── scenes_gallery.py       8 种扩展版式的示例分镜，只有骨架（配 timeline_gallery.json）
    ├── scenes_treat.py         画法示例：骨架加照片和道具（配 timeline_treat.json）
    ├── demo_assets/            画法示例用的道具和照片（--demo 时拷进工程，来源见 CREDITS.md）
    ├── facts_template.md       事实文件模板
    └── *.example.json          时间线和工程配置示例
```

## 许可

| 内容 | 许可 |
|---|---|
| 代码、文档、图标、底图、纹理 | MIT，见 [LICENSE](LICENSE)。图标、`public/plates/` 的底图和 `public/tex/` 的纹理由 AI 图像工具生成 |
| 字体（D-DIN Condensed、Bebas Neue、Oswald、Quicksand、Noto Sans SC、Noto Serif SC、Ma Shan Zheng、Fusion Pixel） | SIL Open Font License 1.1，见 `templates/engine/public/fonts/LICENSES.txt` |
| 演示道具 `templates/demo_assets/props/` | MIT，由 AI 图像工具生成 |
| 演示照片 `templates/demo_assets/photos/` | 来自 Wikimedia Commons，各自为公有领域、CC BY 2.0、CC BY-SA 2.0 或 CC BY-SA 4.0，作者和原始页面见 `templates/demo_assets/CREDITS.md` |
| 地图数据 `src/geo/world110.json` | 由 Natural Earth 1:1.1 亿国界数据（公有领域）投影生成 |
| Remotion | 不在本仓库内，`npm install` 时下载。个人、3 人以内的公司和非营利组织可以免费使用。4 人以上的公司要购买公司授权：https://www.remotion.pro/license |
| 优设标题黑 | 不在本仓库内，见上文 |
| Logo、网页截图 | 不在本仓库内，由使用者抓取。Logo 是各公司的商标，Wikimedia Commons 上标为公有领域的文件也一样 |

## 来历

这个 skill 由 [Manus](https://manus.im) 在一次风格复刻实验中制作。制作过程是：先逐帧拆解她的公开视频，再用 Remotion 重建版式，最后用一期约 12 分钟的养老金选题，把讲解包装迭代了 4 版（v3–v6）。实验中的出镜画面用了真人形象的 AI 生成，所以那期成片没有放进本仓库。

v1.1 用一支 CC BY 4.0 的 OpenClaw 讲解视频做了第二次测试，从剪辑到成片走完全程。根据那次的反馈，加入了 tech 主题、3D 渲染底图、真实网页截图和 Logo，并把"开工前先问底图和素材"写进了工作流。

v1.2 根据测试片的反馈重做了全部背景：底图换成有实物质感的纸张、木头、屏幕和图纸，主题从 3 套扩到 6 套，每套有自己的字体、卡片材质、片名卡和片尾卡。OpenClaw 测试片用 `blueprint` 主题重新渲染了一遍。

v1.3 新增 8 种扩展版式（折线图、时间轴、饼图、流程图、树状拆解、世界地图、左右对比、关系图）。演示分镜默认不放画中画，公式条和计算器居中。
