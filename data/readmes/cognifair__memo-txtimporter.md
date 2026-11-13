# 墨记文档导入 Memo-TXT

> 🌐 [墨卡大师 · 专业制卡工作流](https://moka-master.app.workbuddy.host/?sharecode=ZYHGDS4GEB)

专注墨墨记忆卡（Markji）TXT 导入文档的文件容器格式：把已有卡片正文按牌组和章节组织为可交付的 UTF-8 TXT，并检查章节、分卡符与答案线；也负责「TXT 先导入、图片后回填」这条混合路线。

调用名：`$memo-txt`。版本以 [SKILL.md](SKILL.md) 的 `metadata.version` 和 [version.json](version.json) 为准。

## 稳定 CLI

不再手写 TXT 容器或另写校验器：

```text
python -B scripts/cli.py lint <TXT> [--require-answer-line]
python -B scripts/cli.py finalize <TXT> [--member pro|free] [--require-answer-line]
python -B scripts/cli.py guide
```

完整退出码与边界见 [references/cli-contract.md](references/cli-contract.md)。

## 核心格式

| 标记 | 含义 |
|---|---|
| `牌组名称：`、`牌组简介：` | 文件开头的牌组信息，简介可为空 |
| `### 章节名` | 独占一行，指定后续卡片所属章节 |
| `===` | 独占一行，分隔不同卡片 |
| `---` | 独占一行，同一卡片的题面与答案分界 |

空行只用于排版，不负责分卡。默认沿用样本在最后一张卡片后保留 `===`；其后的空白不算新卡。

以下是说明结构的纯文本示例；生成的 TXT 文件本身不含 Markdown 代码围栏：

```text
牌组名称：格式演示
牌组简介：两张简单问答卡

### 基础知识
水的化学式是什么？
---
H2O
===
常压下水的凝固点是多少？
---
0 ℃
===
```

完整规范与边界见 [references/container-format.md](references/container-format.md)。

## TXT + 图片：先导入，后回填

卡片里有表格或题干配图、但用户选择 TXT 路线时，不必改走整批 API 制卡：

1. 表格图交给 Memo-Canvas 渲染成透明 PNG，文件名即打标（如 `T02-中国教育史-2012-15-唐代儒学学校一览.png`）。
2. TXT 的答案面写一行占位标记，独占一行、编号与资产号一致，例如 `[T#!90959b#表格图 T02]`；
   用的是现成的 `T#` 行内标签，不破坏卡片，结构校验照常通过。
3. 交付 TXT + PNG 目录 + 资产清单（资产号 ↔ 卡片键）。
4. 用户导入后：核对牌组卡片数 → 逐项上传文件 → 把标记整行替换成 `[Pic#ID/<file id>#]`，
   其余内容逐字符不动 → 更新后回读。
5. 验收：占位标记残留数为 0、全部文件 ID 可解析、抽样（含「一卡多图」那张）与本地交付逐字符一致。

细节、接口与已踩过的坑（尤其是「一卡多图必须每次重读最新正文，否则后写覆盖前写」）见
[references/image-backfill.md](references/image-backfill.md)。

## 能做什么

- 将现成的卡片正文、题面与答案列表、章节映射组织成导入文档。
- 保留原有正文标签、公式、选项与媒体引用，仅修改用户要求的文件结构。
- 统计牌组、章节、每章卡数、分卡符与答案线，报告问题及行号。
- 请求修复时默认另存新文件，避免覆盖原件。
- **混合路线**：卡片走 TXT，表格/配图由 Memo-Canvas 出透明 PNG；先在 TXT 里写占位标记，用户导入完成后，
  再用官方 OpenAPI 上传图片并把标记整行替换为 `[Pic#ID/…]`，最后回读验收。

## 使用示例

> 使用 $memo-txt，把这些已有卡片按指定章节整理成 TXT，并检查分卡和答案线，不改动正文语法。

仅整理已有正文时不询问会员状态、不索取凭证、不访问账户。如果还需要从原始学习材料设计新卡，交由 [墨卡大师 Memo-Cardest](https://github.com/Cognifair/memo-cardest) 处理内容层；表格渲染属于可选 Memo-Canvas 技能。

## 结构校验

Python 3 标准库即可运行，检查器只读，不修改输入文件：

```text
python -B scripts/lint_txt.py path/to/cards.txt
python -B scripts/lint_txt.py path/to/cards.txt --require-answer-line
python -B scripts/test_check_updates.py
```

常规问答每卡恰有一条答案线时可加 `--require-answer-line`；特殊题型应结合报告中的警告判断。检查器不验证卡片内部标签语法、知识正确性或客户端显示。

## 导入演示

不知道怎么把 TXT 导入墨墨记忆卡时，先看四步：

1. 打开电脑版 Markji，进入「制卡桌面」。
2. 点进要导入的牌组。
3. 点右上角「批量制卡」→「从文本导入」。
4. 粘贴或上传 TXT，按弹窗提示确认。

图文版见 [references/import-guide.md](references/import-guide.md)（含完整流程 GIF 与步骤图）；离线 HTML 版见 `references/import-guide.html`。截图只指示按钮位置，界面以当前客户端为准。交付 TXT 时，技能会运行 `scripts/finalize_txt.py`，自动附上四步教程、GIF 和 `交付自检` 标记。

## 使用边界与更新框架

文件格式来自经整理的用户样本，不代表所有客户端版本都已验证。交付后仍需使用者先少量试导入；不自动上传卡片、不操作客户端导入、不保证覆盖原卡或保留旧 ID、链接和学习进度。图片回填只在用户导入完成并明确要求后执行，且只替换 TXT 里已有的占位标记。

附带本地可选扩展识别与授权后启动同步。清单已配置 GitHub 仓库与 `version.json`，授权后可 fetch 并快进更新，不执行远端代码；自动检查默认关闭。详见 [references/satellite-framework.md](references/satellite-framework.md) 和 [references/satellites.md](references/satellites.md)。

**图片回填不是纯离线交付**：自动回填需要官方 API 凭证，并对上传/写入单独授权。选择 TXT 不等于已授权回填；没有 API 条件时，只交付 PNG 与“手工插入”说明。

## Memo 系列

<!-- memo-series:begin -->
| 技能 | 职责 |
|---|---|
| [墨卡大师 Memo-Cardest](https://github.com/Cognifair/memo-cardest) | 核心制卡：知识拆解、题型、正文语法与牌组操作 |
| [Memo-MinerUOCR](https://github.com/Cognifair/memo-mineruocr) | 扫描件与大 PDF 识别、拆分并合并 Markdown |
| [墨兰迪 Memo-Canvas](https://github.com/Cognifair/memo-canvas) | 表格图片与 LaTeX array 表格制作，扫描图像高清化与忠实重绘 |
| [迁墨 Memo-AnkiGo](https://github.com/Cognifair/memo-ankigo) | Anki 图片挖空转墨墨原生遮罩 |
| [Memo-QAhelper](https://github.com/Cognifair/memo-qahelper) | 墨墨记忆卡使用答疑（官方百科与论坛） |
| [卡跳跳 Memo-CardLink](https://github.com/Cognifair/memo-cardlink) | 卡片单向跳转、双向互链与 Card 引用审计（原 Memo-Link） |
<!-- memo-series:end -->

## License

[MIT](LICENSE)
