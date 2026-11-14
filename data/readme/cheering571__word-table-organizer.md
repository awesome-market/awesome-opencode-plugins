# Word Table Organizer（单词清单 → 三列表格 Skill）

一个 [WorkBuddy](https://www.workbuddy.cn) / Claude 风格的 Agent Skill：把**文本粘贴的英文单词/短语清单**整理成排版规范的三列表格 **Excel（.xlsx）文件**，并支持往同一张表里反复增量追加。

> 姊妹项目：[english-word-extractor](https://github.com/Cheering571/english-word-extractor) —— 负责**图片**里的单词提取。本 Skill 负责**文本**清单。两者共用同一份表格构建脚本，产出的表可以混用、交替追加。

## 为什么需要它

把单词抄进 Excel 是个纯粹的体力活：补音标、查词性、拆多义项、合并单元格、每次都要保证和上一批格式一致。而且下一批新词来了，还得手工往后接，一不小心就重复、串行、样式漂移。

这个 Skill 把整套约定固化成流程 + 脚本：

- 你只要说「整理单词」，粘贴清单；
- 它负责解析、补音标、查释义、去重、合并单元格；
- 默认**追加到已有的单词表**，格式与上一批完全一致；
- 数据源单独存一份 JSON，随时可重算、可回滚。

## 功能特性

- **解析脏清单**：自动剥掉序号/项目符号（`1.` `①` `-`），拆分「单词 + 词性 + 释义」，修掉 `liberalismn.` 这类词性与单词粘连的笔误
- **单词 / 短语分流**：单词补 IPA 音标，短语（含 `...`、`sb`、`sth` 的搭配）音标列留空，不硬塞
- **多词性纵向合并**：单词列与音标列跨该词所有词性行合并，释义列每词性一行（`n. …` / `v. …`）
- **增量追加 + 去重**：按 `word.lower()` 去重，同词不同词性自动并进同一条，已存在的词条不会重复出现
- **一词多音标注**：`separate` 这类形容词/动词读音不同的词，音标列分开标注
- **屈折形式溯源**：`blazes` `dubbed` `campuses` 保留原拼写，释义后括注原形与形式（`campus 的复数`）
- **格式统一**：所有表格由同一个 `build_word_table.py` 生成，不会因为分批而版式漂移
- **占用自愈**：表格正在编辑器里打开时不会崩，返回明确的处置提示（退出码 2），数据仍安全落盘

## 输出示例

| 单词 | 音标 | 词性与释义 |
|------|------|-----------|
| cruise | 美 /kruːz/ | n. 乘船游览；巡游 |
|        |           | v. 乘船游览；巡游；慢速行驶 |
| quick fix |  | 应急措施；权宜之计 |
| fuse | 美 /fjuːz/ | v. 熔化 |
|      |            | n. 保险丝 |

`cruise`、`fuse` 的单词与音标单元格各跨两行纵向合并；短语 `quick fix` 音标列为空。

## 版式规格

| 元素 | 规格 |
|---|---|
| 表头 | `单词` `音标` `词性与释义`，等线 12pt 加粗，底色 `D9E2F3`，细边框，居中 |
| 单词列 A | Calibri 12pt 加粗，居中，自动换行，列宽 16 |
| 音标列 B | Calibri 11pt 斜体，字色 `404040`，居中，列宽 24 |
| 释义列 C | 等线 12pt，左对齐，自动换行，列宽 48 |
| 边框 | 全表 `B0B0B0` 细线 |

## 目录结构

```
word-table-organizer/
├── SKILL.md                       # Skill 定义（触发边界 + 完整执行流程）
└── scripts/
    ├── build_word_table.py        # JSON → xlsx（版式真值来源）
    └── merge_and_build.py         # 增量合并 + 去重 + 重建 + 占用检测
```

## 安装

### 方式一：让 Agent 直接安装（推荐）

把仓库链接发给你的 AI 助手（如 WorkBuddy）：

```
帮我安装这个 Skill：https://github.com/Cheering571/word-table-organizer
```

### 方式二：手动安装

```bash
git clone https://github.com/Cheering571/word-table-organizer.git
```

把整个 `word-table-organizer` 文件夹复制到用户级 Skill 目录：

```
Windows: C:\Users\<用户名>\.workbuddy\skills\word-table-organizer
Linux/macOS: ~/.workbuddy/skills/word-table-organizer
```

重启会话（或新开会话）后生效。

## 使用方法

装好后直接说「整理单词」或「把这些单词加上去」，然后粘贴清单：

```
blazes
quarterly
compensate v. 补偿，赔偿
quick fix 应急措施，权宜之计
```

带不带释义都能处理：没给释义时由 Skill 查证补全，已给释义时优先采用并在必要时补上词性。

### 仅使用脚本（不装 Skill）

```bash
pip install openpyxl

# 增量追加并重建表格
python scripts/merge_and_build.py \
  --add   _add.json \
  --store _words.json \
  --xlsx  单词表_11.3.xlsx

# 只重建（改了 store 之后，或上次因文件占用失败时重试）
python scripts/merge_and_build.py \
  --store _words.json --xlsx 单词表_11.3.xlsx --rebuild-only
```

`_add.json` 与 `_words.json` 结构一致：

```json
[
  {
    "word": "fuse",
    "phonetic": "美 /fjuːz/",
    "entries": [
      {"pos": "v.", "meaning": "熔化"},
      {"pos": "n.", "meaning": "保险丝"}
    ]
  }
]
```

`phonetic` 可留空（短语就该留空）；`entries` 每个元素对应一个词性行。

脚本输出 JSON 摘要：

```json
{
  "status": "ok",
  "added": 44,
  "store_before": 8,
  "new_entries": 44,
  "total_words": 52,
  "total_rows": 59
}
```

目标文件被 Excel / 编辑器占用时返回 `"status": "locked"` 且退出码为 2，关闭占用后用 `--rebuild-only` 重跑即可。

## 与 english-word-extractor 的分工

| 输入 | 该用哪个 Skill |
|---|---|
| 图片 / 截图 | [english-word-extractor](https://github.com/Cheering571/english-word-extractor) |
| 文本粘贴的单词清单 | **word-table-organizer**（本仓库） |
| 图片 + 文本清单 | 图片走 english-word-extractor，文本部分走本 Skill，合并进同一张表 |

判定只看**输入媒介**，不看措辞：说「整理单词」但同时贴了图 → 走图片提取。

## 依赖

- Python 3.8+
- [openpyxl](https://pypi.org/project/openpyxl/) >= 3.0

## License

[MIT](./LICENSE)
