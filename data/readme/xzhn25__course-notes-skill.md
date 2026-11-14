# course-notes-skill · 课件精读

> Turn an English lecture slide deck into a Chinese self-study document, delivered as PDF.
> A Claude Code / Codex / Agent Skill distilled from real-world lecture-note production.

---

## 这是什么

把**英文课件**（PPT / 讲义 PDF）变成一份**中文可自学**的精读文档，交付 PDF。

它不是为了「把 PPT 翻译一遍」，而是解决一个具体问题：

> **PPT 是讲课的提词卡，不是教材。**
> 老师站在讲台上会口头补三样：① 这个术语什么意思 ② 这一步怎么推过来的 ③ 这个工具是干嘛用的。
> PPT 上只留结论和页码。

所以精读 = **把「老师口头会补的那部分」还原成文字**。

## 为什么要配模板和脚本

只写方法论不够。实测发现：AI 做一份讲义，时间几乎全花在**从零写 CSS、造渲染/裁剪/打印流程**上，而不是在内容上。
所以这个仓库除了方法论，还直接给了三样能省掉这些时间的成品：

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 给 AI 的执行清单（约 2KB，不解释为什么，只说要做什么） |
| `assets/template.html` | 排版样式（已按 A4 打印验证）：封面 / 目录 / 公式块 / 色块 / 习题 / 插图 / 分页。**只改 body，CSS 不动** |
| `assets/print-pdf.ps1` | Windows 一键出 PDF：自动内联相对路径图片 + 绕开中文路径坑 + 校验产物 |
| `prompt/lecture-notes-prompt.zh-CN.md` | 独立提示词版，不需要 skill 机制，粘给任何 AI 就能用 |

## 安装

### 作为 Agent Skill

```bash
# Claude Code / Codex / 兼容 skills 目录的工具
git clone https://github.com/XZhn25/course-notes-skill.git ~/.codex/skills/course-notes
```

之后说「精读这份课件」「总结第 3 讲」「把 PPT 做成讲义」就会触发。

### 不用 skill 机制

把 `prompt/lecture-notes-prompt.zh-CN.md` 整段粘给 AI，附上课件即可。

## 核心方法论

**八查**（每节过一遍）：术语 · 符号 · 常数/系数来历 · 跳步 · 用途 · 约定 · 图说 · 配图

**分寸**（和八查同等重要）：判断标准只有一条——**读者会不会因为这一处卡住就读不下去？**
会 → 必补；只是「更完整 / 更漂亮」→ 不补。机械地补会把 1 页撑成 5 页。

**最终的验收标准：读者不看 PPT，只看这份文档也能懂。**

## 适用 / 不适用

**适用**：大学理工科课件（公式与图表多的）、英文授课 / 中外合办、期末复习与考前补课。

**不适用**：纯文字型商业 PPT（用不上八查）、需要 OCR 的手写扫描件、想要「逐字翻译」的场景。

## 用法示例

```powershell
# Windows
.\assets\print-pdf.ps1 -In .\第7讲_全内容中文精读.html
# → 同目录生成 .pdf，并打印 "OK ... (217 KB, 内联图 3 张)"
```

## License

Apache-2.0，见 [LICENSE](LICENSE)。
