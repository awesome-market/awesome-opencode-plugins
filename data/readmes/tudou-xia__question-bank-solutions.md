# 题库逐章解答 · Question Bank Solutions

把一份题库文档，变成**逐章交付的带解析答案**。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/type-Agent%20Skill-blue.svg)](SKILL.md)

---

## TL;DR

- 丢一个题库文件进来（PDF / Word / PPT / 纯文本 / 拍照图片都行），说一句「帮我做一下这份题库」
- 它先认出章节，出一张**批次清单**给你确认；确认后**一次只答一章**
- 每题给：**答案 + 干练解析 + 考点 + 该复习什么**
- 说「继续」进下一章；说「只要第三章」就只答第三章；说「整卷速通」就一次给完
- 需要时随时说「导出」，它把已答内容攒成一份 Word 文档（详细版 / 速通版各一个文件）

> 输入：一份 312 题的 PDF 题库 → 输出：9 章答案，每章一次，带解析。
> 全程按原书顺序，绝不重排。

---

## 为什么不用「直接丢给模型」

批量做题有三个具体失败模式，这个技能就是为它们写的：

| 问题 | 表现 | 本技能的处理 |
|------|------|-------------|
| **上下文崩坏** | 一次答 300 题，答到后半程题号错位、选项张冠李戴 | 分章控制上下文，一批只装一章 |
| **错误无标记** | 瞎猜的题和确定的题长得一模一样，你不知道该复核哪几道 | 不确定就给倾向答案 + ⚠️ 标注 + 翻转条件 |
| **文档脏** | 水印被读成选项、选项粘连、跨页截断、表格排版 | 解析前先做清洗，剔除水印后重跑题号连续性校验 |

---

## 效果示意

输入（`examples/demo-chapter.md` 中的一段）：

```
7. 某信道带宽为 3 kHz，信噪比为 30 dB，根据香农定理，该信道的最大数据速率约为（  ）
A. 3 kbit/s   B. 6 kbit/s   C. 30 kbit/s   D. 29.9 kbit/s
```

输出：

```
**7. D**
解析：本题考查香农定理，两步走。
　① 30 dB 换算：10lg(S/N) = 30 → S/N = 1000（不是 30，这是最常见的错点）。
　② 代入 C = W·log₂(1+S/N) = 3000 × log₂(1001) ≈ 3000 × 9.97 ≈ 29.9 kbit/s。
　③ 干扰项来源：A 项把带宽直接当速率，B 项用奈氏准则且误取 1 位/码元，C 项未做对数换算。
考点：香农定理 + dB 与信噪比换算
复习：C = W·log₂(1+S/N) 与奈氏准则 C = 2W·log₂N 的区别；dB 定义；两定理的适用前提
```

---

## 三种用法

| 你怎么说 | 实际行为 |
|---------|---------|
| 「做一下这套题」 | 问是否速通 → 出批次清单 → **一章一答**，每章后停下 |
| 「整卷速通」 | 跳过清单与停顿，一次给完全书；选择/判断/填空只给答案 |
| 「只要第三章」 | 回一行范围确认 → **直接答该章**，不问清单 |
| 「只要第三、五章，速通」 | 回执 → 一次给两章，客观题只给答案 |

粒度说明：

- **逐章模式**：每题完整解析，解析长度按题目复杂度自适应（简单 40–80 字 / 中等 60–120 / 复杂 150–350，350 为上限）。
- **速通模式**：选择题、判断题、填空题**只给答案**且紧凑连排；简答、计算、编程、材料分析仍完整作答。存疑题单独展开。

---

## 安装

把整个目录放进技能目录即可。

**方式一：git clone**（便于以后 `git pull` 升级）

```bash
# 用户级（所有项目可用）
git clone https://github.com/tudou-xia/question-bank-solutions.git \
  ~/.workbuddy/skills/question-bank-solutions

# 或项目级
mkdir -p .workbuddy/skills && cp -r question-bank-solutions .workbuddy/skills/
```

**方式二：下 zip 解压**（不想装 git 就用这个）

到 [Releases](https://github.com/tudou-xia/question-bank-solutions/releases/latest) 下载 `question-bank-solutions.zip`，解压后把整个 `question-bank-solutions/` 文件夹放进 `~/.workbuddy/skills/` 即可。

不依赖任何脚本或第三方包，`SKILL.md` 本身就是全部逻辑，其它目录只是可选的细节展开。

---

## 配置

| 键 | 取值 | 默认 |
|----|------|------|
| `scope` | `all` / `chapters:[...]` / `pages:[...]` | `all` |
| `batch` | `chapter` / `page` / `fixed:N` | `chapter`（无章节则 `page`） |
| `gate` | `on` / `off` | `on` |
| `fast_mode` | `off` / `on` | `off` |
| `explain` | `auto` / `short` / `deep` | `auto` |
| `lang` | `follow` / `zh` / `en` | `follow` |
| `search` | `auto` / `always` / `never` | `auto` |
| `export` | `docx` / `md` / `pdf` | `docx` |

---

## 导出

只有在你明确要求时才生成文件；但每答完一批会主动问一次。

| 文件 | 内容 |
|------|------|
| `<原名>_答案.docx` | 详细版：答案 + 完整解析 + 考点 + 复习 |
| `<原名>_答案速通.docx` | 速通版：客观题只答案，主观题完整 |

两个粒度**永远分成两个文件**，不混装。导出内容始终是**累积的**（当前批 + 之前所有批）。

---

## 它不做的事

- 不改你的原始文件（只读）
- 不自动生成文件（除非你要）
- 不猜「重点章节」这种主观范围，一律回问
- 不把不确定的题写成确定
- 不引用不存在的文献、页码、来源
- 不用于考场作弊或替考

---

## 目录结构

```
question-bank-solutions/
├── SKILL.md                  # 主流程（模型读这个）
├── README.md                 # 本文件
├── references/
│   ├── templates.md          # 各题型输出模板、导出文档结构
│   └── splitting.md          # 章节/页码切分、水印剔除、OCR 坑
├── examples/
│   ├── demo-chapter.md       # 逐章模式对照
│   ├── demo-fast.md          # 速通模式对照
│   └── demo-subset.md        # 只答指定章节的对照
├── CHANGELOG.md
└── LICENSE
```

---

## English

**Question Bank Solutions** turns a question-bank document into a chapter-by-chapter answer key with explanations.

**TL;DR** — Drop in a question bank (PDF, DOCX, PPTX, TXT/MD, or photos). It detects the chapter structure, shows a batch list for your confirmation, then answers **one chapter per reply**: answer + terse explanation + tested concept + what to review. Say "continue" for the next chapter, "only chapter 3" to target a subset, or "full speed" to get everything at once. Ask to export and it assembles a Word answer document.

Three failure modes it fixes:

1. **Context collapse** — answering 300 questions in one pass loses numbering and option alignment. Fixed by one chapter per batch.
2. **Silent errors** — guessed and certain answers look identical. Fixed by a confidence marker with the exact reason and what would flip the answer.
3. **Dirty source** — watermarks read as options, glued options, page breaks, table layouts. Fixed by a cleanup pass plus a re-check of question-number continuity.

Modes: per-chapter (default) · fast mode (objective items get bare answers, subjective items stay complete) · named-chapter subset · any combination.

Config keys: `scope`, `batch`, `gate`, `fast_mode`, `explain`, `lang`, `search`, `export`.

Install: copy this directory into your agent's skills folder. No scripts, no dependencies — `SKILL.md` is the whole logic.

License: MIT.

---

## License

MIT © 2026 question-bank-solutions contributors
