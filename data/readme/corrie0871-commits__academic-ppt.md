<p align="center"><img src="docs/assets/banner.svg" alt="Academic PPT — Evidence-led, editable presentations" width="100%"></p>

# Academic PPT · 学术汇报 Skill

**让论文变成有证据、讲得清楚、可以继续编辑的学术汇报。**

[使用方法](#快速开始) · [工作流程](#从材料到汇报) · [贡献指南](CONTRIBUTING.md) · [MIT License](LICENSE)

面向论文汇报、课程展示、会议报告与答辩的中文优先 Agent Skill。它定义证据核对、叙事规划和交付检查流程；PPTX 的生成需要运行环境提供可编辑演示文稿制作工具。

## 为什么使用它

| 能力 | 带来的改变 |
| --- | --- |
| 证据可追溯 | 主张对应论文页码、图表与原始数值，不编造研究发现 |
| Rubric 对齐 | 把评分项映射到证据和页面，识别缺口 |
| 一页一个目的 | 按口头论证组织内容，兼顾时长与讲述节奏 |
| 可编辑优先 | 原生文字、表格与可重建图表保持可编辑 |
| 双语讲解与答辩 | 按需提供中文理解、英文页面、讲稿与问答 |
| 仅排版模式 | 保留原文、数据与语义，专注视觉层级 |

## 快速开始

1. 下载本仓库，将文件夹命名为 `academic-ppt`。
2. 放入支持该 Skill 格式的 Agent 的技能目录，确保 `academic-ppt/SKILL.md` 可被发现。
3. 提供论文、汇报要求和评分标准；使用下面的请求：

```text
使用 $academic-ppt，根据附件论文制作 10 分钟学术汇报。
英文页面、中文讲解，16:9，输出可编辑 PPTX。
请对齐附件 rubric，核对每个结论的来源，并加入逐页讲稿。
```

只优化已有材料：

```text
使用 $academic-ppt，仅优化附件 PPT 的排版。
保留全部文字、数字、引用和语义，不增加页数。
```

## 从材料到汇报

```mermaid
flowchart LR
  A[论文与要求] --> B[证据表与评分映射]
  B --> C[核心回答与逐页叙事]
  C --> D[可编辑页面与讲稿]
  D --> E[证据核对与渲染检查]
```

## 文件导航

- [SKILL.md](SKILL.md)：主要流程与模式选择。
- [证据与图表](references/evidence.md)：数值、来源和研究图规则。
- [场景与叙事](references/storytelling.md)：不同汇报场景的结构。
- [视觉系统](references/design.md)：层级与页面设计。
- [质量检查](references/quality.md)：交付检查。
- [偏好与边界](references/personalization.md)：通用偏好处理，不含作者私人聊天。
- [调研与取舍](references/research.md)：设计来源及局限。

## 能力边界

本仓库是工作流 Skill，不包含独立 PPT 生成引擎、付费工具授权或论文数据集。科研图可保留原图，其内部数据不会因此变为可编辑。实际导出、字体及渲染能力取决于使用环境；未经渲染的输出不能视为完成视觉检查。

## 开源

原创内容使用 [MIT](LICENSE) 许可。引用项目和用户输入材料的权利属于各自权利人。本仓库不分发个人作业、论文附件或聊天记录。
