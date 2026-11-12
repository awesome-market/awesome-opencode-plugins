# Memo-QAhelper v1.0.11

> 🌐 [墨卡大师 · 专业制卡工作流](https://moka-master.app.workbuddy.host/?sharecode=ZYHGDS4GEB)

墨墨记忆卡（Markji）的**使用答疑**技能。回答产品功能、入口、设置、同步、导入导出、会员、API 等使用问题；不负责制卡内容、卡片语法、OCR 或表格。

## 硬规则

- 只允许三类来源：**墨墨百科**（`memodocs.maimemo.com`，官方）、**墨记论坛**（`markji.discourse.group`，用户反馈）、**本机同级的 Memo 系列技能说明**（与论坛同级，非官方，只读）。
- 其它来源一律不引用；不凭模型记忆、不推测、不类比、不杜撰。
- 三类来源都查不到 → 引导发邮件 `support@markji.com`，流程结束。
- 不调用 Memo 技能，不触发它们的 S0/提问/写入/API。

## 四档流程

```text
① site:memodocs.maimemo.com <关键词>   命中 → 据墨墨百科（官方）
        │ 未查到
② site:markji.discourse.group <关键词>  命中 → 据论坛用户反馈（非官方）
        │ 未查到
②b 读同级 ../memo-*/SKILL.md           命中 → 据 Memo 系列技能说明（非官方）
        │ 未查到
③ 引导发邮件 support@markji.com，结束
```

账号、支付、数据丢失这类个人问题不检索公开文档，直接走 ③。

## TXT 导入固定答案

问「TXT 怎么导入」「从文本导入在哪」时，直接发内置教程，不检索：

1. 打开制卡桌面，进入目标牌组
2. 右上角「批量制卡」→「从文本导入」
3. 粘贴 TXT，保持 `###` / `===` / `---` 默认，先看预览，再点「导入」

教程全文与 GIF 见 `SKILL.md` 的「固定答案：TXT 导入」。只适用于 TXT；CSV/表格、API、Anki 仍走对应技能或白名单检索。

## 回答格式

```text
结论：<一句话>
依据：<来源> · <链接>
步骤：<页面里的实际步骤>
来源：据墨墨百科（官方） / 据论坛用户反馈（非官方）
```

产品使用与设置问题走本技能；制卡内容走 `memo-cardest`，OCR 走 `memo-mineruocr`，TXT 容器走 `memo-txt`，表格渲染走 `memo-canvas`。细节见 [references/sources.md](references/sources.md)。

## Memo 系列

<!-- memo-series:begin -->
| 技能 | 职责 |
|---|---|
| [墨卡大师 Memo-Cardest](https://github.com/Cognifair/memo-cardest) | 核心制卡：知识拆解、题型、正文语法与牌组操作 |
| [Memo-MinerUOCR](https://github.com/Cognifair/memo-mineruocr) | 扫描件与大 PDF 识别、拆分并合并 Markdown |
| [墨兰迪 Memo-Canvas](https://github.com/Cognifair/memo-canvas) | 表格图片与 LaTeX array 表格制作，扫描图像高清化与忠实重绘 |
| [墨记文档导入 Memo-TXT](https://github.com/Cognifair/memo-txt) | TXT 容器格式、分卡校验与图片回填 |
| [迁墨 Memo-AnkiGo](https://github.com/Cognifair/memo-ankigo) | Anki 图片挖空转墨墨原生遮罩 |
| [卡跳跳 Memo-CardLink](https://github.com/Cognifair/memo-cardlink) | 卡片单向跳转、双向互链与 Card 引用审计（原 Memo-Link） |
<!-- memo-series:end -->

## License

[MIT](LICENSE)
