# 卡跳跳 Memo-CardLink v1.0.5

> 🌐 [墨卡大师 · 专业制卡工作流](https://moka-master.app.workbuddy.host/?sharecode=ZYHGDS4GEB)

**卡跳跳**：在已有墨墨记忆卡之间建立可核验的跳转与互链。

调用名：`$memo-cardlink`。原名 Memo-Link；旧 `$memo-link` 不再作为独立安装入口。

## 它解决什么

- 目录卡点进详情卡，读完再跳回来；
- 一组相关卡互链，而不是每张都手动找 ID；
- 已有 `[Card#...]` 引用错位、重复或缺失，需要修复；
- 不改卡片正文和排版，只加一条可跳转的 Card 引用。

“卡跳跳”只修改链接，不创建卡片、不移动卡片、不批量改写正文。

## 两种模式

| 模式 | 效果 | 修改范围 |
|---|---|---|
| 单向 | A → B | 只改 A；读取 B 核实目标 |
| 双向 | A ↔ B | A 引用 B，B 引用 A |
| 审计/修复 | 按指定方向检查或补缺 | 审计只读；修复只改授权方向 |

只说“加个链接”且给出来源和目标时，默认单向；不会因为旧名 Memo-Link 就自动做成双向。

## 三种“卡片链接”不要混

### 1. 正文跳转引用（卡跳跳写入）

```text
[Card#ID/<目标 root_id>#显示文字]
```

单向和双向**语法相同**，只差改哪张卡：

- 单向 A → B：只改 A；
- 双向 A ↔ B：A、B 各插一条；
- 正文里必须用目标 `root_id`，不能用 `card_id` 代替。

### 2. 网页定位链接（不是卡跳跳产出）

```text
https://www.markji.com/deck/editor/<牌组网页 ID>?cardId=<卡片网页 ID>
```

这是网页端编辑器深链，使用网页 24 位 ID，不是 `mkjd_` API 牌组 ID，也不是 `root_id`。它用于打开/定位卡片，不是可写入正文的 Card 语法。

### 3. 牌组入口

```text
https://www.markji.com/deck/<牌组网页 ID>
```

这是整个牌组的入口，不是单卡跳转，也不是分享授权。

详见 [references/card-link-formats.md](references/card-link-formats.md)。

## 稳定 CLI

不再手写 `[Card#...]` 或临时拼格式：

```text
python -B scripts/cli.py ref --root-id <root_id> --label <文字>
python -B scripts/cli.py check "<引用>"
```

只读查询用 `scripts/cl_probe.py`。完整命令与退出码见 [references/cli-contract.md](references/cli-contract.md)。

## 安装

```powershell
git clone https://github.com/Cognifair/memo-cardlink.git "$env:USERPROFILE\.codex\skills\memo-cardlink"
```

安装后重启客户端或新开会话，让它重新扫描技能目录。调用：

```text
$memo-cardlink 把「总纲」这张目录卡指向「第一章」和「第二章」，单向。
```

## 一次典型操作

```text
用户：把总纲卡里的“第一章”链到第一章详情卡，单向。

卡跳跳：
1. 找到总纲卡和第一章详情卡，核对 card_id / root_id；
2. 预览要插入的 [Card#ID/...] 片段和位置；
3. 只改总纲卡，保留其余正文、图片和 grammar_version；
4. API 回读，确认引用只出现一次、目标可解析；
5. 说明哪些验证做了、哪些客户端渲染/点击未验证。
```

双向则分别检查两端，只补缺失的一端；已经正确的一侧不重复插入。

## 验证分三层

1. **API 回读**：正文、引用数量、`card_rids`、`grammar_version`；
2. **客户端渲染**：标签和周围文字正常显示，不露出原始语法；
3. **实际点击**：真的能跳到目标卡。

渲染正常不等于能点击；只验证了前两层时，会明确说“点击未验证”。

## 边界

- 只使用官方 MaiMemo OpenAPI；不切换私有 Web API；
- 不保存 token、Cookie 或真实卡片/牌组 ID 到技能与示例；
- 不创建卡片、不移动卡片、不批量重写正文；
- 双向改单向涉及删除反向引用，必须由用户明确要求；
- 锚点不唯一、目标歧义、并发冲突时停止受影响写入；
- 执行规则与授权边界以 [SKILL.md](SKILL.md) 和 [references/workflow.md](references/workflow.md) 为准。

## 仓库结构

```text
memo-cardlink/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── version.json
├── LICENSE
├── agents/openai.yaml
└── references/
    ├── workflow.md
    └── satellites.md
```

## Memo 系列

<!-- memo-series:begin -->
| 技能 | 职责 |
|---|---|
| [墨卡大师 Memo-Cardest](https://github.com/Cognifair/memo-cardest) | 核心制卡：知识拆解、题型、正文语法与牌组操作 |
| [Memo-MinerUOCR](https://github.com/Cognifair/memo-mineruocr) | 扫描件与大 PDF 识别、拆分并合并 Markdown |
| [墨兰迪 Memo-Canvas](https://github.com/Cognifair/memo-canvas) | 表格图片与 LaTeX array 表格制作，扫描图像高清化与忠实重绘 |
| [墨记文档导入 Memo-TXT](https://github.com/Cognifair/memo-txt) | TXT 容器格式、分卡校验与图片回填 |
| [迁墨 Memo-AnkiGo](https://github.com/Cognifair/memo-ankigo) | Anki 图片挖空转墨墨原生遮罩 |
| [Memo-QAhelper](https://github.com/Cognifair/memo-qahelper) | 墨墨记忆卡使用答疑（官方百科与论坛） |
<!-- memo-series:end -->

## License

[MIT](LICENSE)
