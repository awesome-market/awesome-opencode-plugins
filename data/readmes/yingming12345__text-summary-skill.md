# text-summary-skill

一个最小可用的 Agent Skill：把长文本压成结构化文字摘要。

> 输出固定四段：**一句话结论 → 关键要点 → 待办 / 待确认 → 摘要元信息**。长度可控，且不引入原文没有的信息。

这个仓库同时是一份可直接套用的 **Skill 模板**：`SKILL.md` 里只写触发条件、输入、步骤、输出，没有多余内容，照着改用途就能变成你自己的技能。

## 为什么是「最小可用」

- **单一职责**：只做摘要，不做翻译、改写、扩写、审核。边界清楚，才不会误触发。
- **纯提示词实现**：没有脚本依赖，复制目录即可用，改一行就能调行为。
- **可验收**：输出格式固定，四条硬性要求（不造事实 / 保原始数字 / 保留歧义 / 冲突并列）让结果能被检查，而不是"感觉还行"。
- **带调用示例**：`examples/basic-call.md` 有完整的输入输出对照，可以照着回归。

## 目录结构

```
text-summary-skill/
├── SKILL.md                 # 技能定义（唯一必需文件）
├── examples/
│   └── basic-call.md        # 调用示例：输入 → 输出 → 验证点
├── README.md
└── LICENSE
```

`SKILL.md` 的 YAML frontmatter 只有两个字段：

```yaml
---
name: text-summary
description: 把长文本压缩成结构化文字摘要……  （触发条件写在这里，模型据此判断是否加载）
---
```

## 安装

把整个目录放进 Agent 读取 skills 的位置即可：

```bash
# 全局可用
mkdir -p ~/.codebuddy/skills
git clone <this-repo> ~/.codebuddy/skills/text-summary

# 或只在本项目内可用
mkdir -p .claude/skills
cp -r text-summary ~/你的项目/.claude/skills/
```

无需安装依赖，无需配置环境变量。

## 使用

直接用自然语言触发，或显式调用：

```
把下面这段会议记录总结一下，只要结论和风险点：
<粘贴文本>
```

```
/summarize
text: <原文 / 文件路径 / URL>
length: medium
focus: 上线风险
```

参数（均可省略，省略时用默认值，不追问）：

| 参数 | 默认 | 取值 |
| --- | --- | --- |
| `text` | 必填 | 文本、文件路径或 URL |
| `length` | `short` | `short` / `medium` / `long` |
| `focus` | 全文均衡 | 任意关注点，如「只看风险」 |
| `audience` | 通用读者 | 影响术语深浅 |
| `lang` | 跟随原文 | 输出语言 |

## 完整示例

见 [`examples/basic-call.md`](examples/basic-call.md)：一段 766 字的产品周会记录，输出 `short` + `focus=灰度决策与上线风险` 的摘要（457 字，压缩比 1.68），并逐项列出这次调用验证了哪一步。

## 改成你自己的技能

1. 复制目录，重命名。
2. 改 frontmatter 的 `name` 和 `description`——`description` 里的触发词决定了它会不会被调用，务必写清「什么时候用、什么时候不用」。
3. 替换「输入」「步骤」「输出」三节，保持同样的骨架即可。

四条写作约束建议保留，它们是让技能稳定产出、而非随机发挥的关键：单一职责、默认值代替追问、固定输出模板、硬性不造事实。

## License

MIT，见 [LICENSE](LICENSE)。
