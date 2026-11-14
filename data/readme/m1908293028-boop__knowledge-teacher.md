# Knowledge Teacher

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](CHANGELOG.md)
[![OpenCode Compatible](https://img.shields.io/badge/OpenCode-compatible-brightgreen.svg)](https://opencode.ai)

> 一个智能的 Agent Skill，能够根据你的知识水平自适应调整讲解深度，生成系统、完整的教学文档。

## 什么是 Knowledge Teacher？

Knowledge Teacher 是一个专为 Agent 设计的智能教学助手Skill。它能够：

- **理解你的问题**：当你询问任何概念、原理或技术时，自动识别你的学习意图
- **评估你的水平**：通过智能问答了解你的知识背景（零基础/有自学基础/科班出身）
- **生成个性化教学**：根据你的水平生成适合的教学内容，从通俗解释到严格推导
- **提供完整输出**：支持对话、Markdown 文档、HTML 页面三种输出格式

## 核心优势

### 1. 自适应背景检测
**问题**：传统教学文档要么太浅（对专业人士无用），要么太深（让初学者困惑）。

**解决方案**：Knowledge Teacher 会智能询问你的背景，根据回答调整讲解深度：
- **零基础**：从最基础的概念开始，每个术语都解释
- **有自学基础**：识别并确认你已知的概念，跳过重复解释
- **科班出身**：直接进入高级内容，提供严谨的数学推导

### 2. 系统性讲解框架
**问题**：零散的知识点难以形成完整的理解。

**解决方案**：遵循"课本式"教学框架：
1. **认知起点**：从你已知的概念出发
2. **定义与直觉**：先建立直觉理解，再给出严格定义
3. **原理推导**：一步步展示知识是如何得出的
4. **示例验证**：通过具体例子加深理解
5. **总结与拓展**：强化记忆，指明学习方向

### 3. 多格式输出支持
**问题**：不同场景需要不同的文档格式。

**解决方案**：支持三种输出格式：
- **对话输出**：快速阅读，适合即时学习
- **Markdown 文档**：便于保存、分享和二次编辑
- **HTML 页面**：精美排版，支持数学公式，适合正式文档

### 4. 智能内容拆分
**问题**：复杂主题（如"Transformer"）涉及多个子概念，单文档难以承载。

**解决方案**：自动分析主题复杂度，智能拆分：
- 简单主题 → 单文档输出
- 复杂主题 → 生成目录页 + 多个子文档

### 5. 前置研究与参考文献
**问题**：教学内容的可信度和权威性不足。

**解决方案**：撰写前自动搜索权威来源：
- 从维基百科、学术论文、官方文档获取准确信息
- 整理为标准学术格式的参考文献列表
- 在正文中交叉引用，增强可信度

### 6. 质量自检机制
**问题**：生成的文档可能存在逻辑跳跃或错误。

**解决方案**：自动审查文档质量：
- 逻辑连贯性检查
- 推导完整性验证
- 术语一致性审查
- 公式正确性校验

## 具体作用

### 学习场景
- **概念理解**：快速理解复杂概念（如"反向传播算法"、"注意力机制"）
- **技术对比**：对比相似技术（如"PPO vs DPO"、"CNN vs Transformer"）
- **知识体系**：构建完整的知识框架（如"机器学习基础"、"深度学习原理"）

### 工作场景
- **技术文档**：生成专业的技术文档，供团队参考
- **培训材料**：创建个性化的培训内容，适应不同水平的员工
- **知识沉淀**：将个人理解系统化，形成可复用的知识资产

### 研究场景
- **文献调研**：快速了解新领域的核心概念和最新进展
- **论文写作**：获取准确的定义、公式和参考文献
- **学术交流**：生成清晰的概念解释，便于与他人讨论

## 工作流程

### 完整流程图

```
用户提问 → 意图识别 → 背景评估 → 前置研究 → 内容生成 → 质量自检 → 输出文档
    ↓           ↓           ↓           ↓           ↓           ↓           ↓
"讲解反向传播"  识别为学习请求  询问用户水平  搜索权威来源  生成教学内容  检查逻辑性  输出HTML/MD
```

### 详细步骤

#### 第一步：意图识别
**触发条件**：当用户询问以下类型的问题时自动触发：
- 概念定义："什么是注意力机制？"
- 原理解释："Transformer 的原理是什么？"
- 技术对比："DPO 和 PPO 的区别是什么？"
- 学习请求："给我讲一下反向传播算法"

**识别逻辑**：即使用户没有明确说"讲解"，只要意图是理解某个概念的本质和运作原理，也会触发。

#### 第二步：背景评估
**首次对话**：
1. 检查记忆存储中是否包含用户背景信息
2. 若不存在，使用 `question` 工具询问用户基础：
   ```
   在开始讲解之前，我想先了解一下你的基础，以便调整讲解的起点和深度。
   选项：
   - 零基础：完全零基础，只需要通俗易懂的入门讲解
   - 有自学基础：有一定了解但不系统（如自学过一些片段）
   - 科班出身：相关专业科班出身，可以接受严谨的数学推导与术语
   ```
3. 询问输出形式偏好（对话/Markdown/HTML/自定义）
4. 将所有信息写入记忆存储

**后续对话**：
1. 从记忆存储中读取用户背景信息
2. 询问是否保持当前存储结构（默认保持不变）
3. 直接使用已保存的背景信息，跳过询问步骤

#### 第三步：前置研究
**搜索内容**：
- 知识点的核心定义：从权威来源获取准确的定义
- 历史背景：搜索该知识点的提出者、提出时间、关键论文
- 最新进展：搜索该领域的最新研究或应用
- 常见误解：搜索人们对该知识点的常见疑问和误解

**搜索示例**：
```
websearch({ query: "反向传播算法 历史 1986 Rumelhart" })
websearch({ query: "backpropagation algorithm original paper" })
```

**参考文献整理**：
将搜索到的可靠来源整理为标准学术格式：
```
## 参考文献

1. Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*, 323(6088), 533-536.
```

#### 第四步：内容生成
**讲解框架**：
1. **认知起点**：从最相关的前置概念切入
2. **定义与直觉**：给出精确定义，立即用通俗语言构建直觉画面
3. **推导或原理展开**：一步不跳地展示该知识是如何得出的
4. **示意性示例**：通过极简案例将原理具象化
5. **重要性质或适用条件**：总结该知识在什么前提下成立
6. **与已知知识的联结**：若用户背景中有可连接的点，简短提及
7. **总结**：用一两句话回归本质

**教学方法**：
- **直觉引入**：从可感知的问题出发，不使用任何学科专有名词
- **历史脉络**：用故事化但严谨的方式叙述知识的发展历程
- **核心思想**：在给出任何公式之前，先用纯文字概括核心思想
- **从特例到一般**：先选取极简特例手工演算，再给出一般化形式

#### 第五步：质量自检
**检查项目**：
1. **逻辑连贯性**：每一节是否自然引出下一节？是否存在逻辑跳跃？
2. **推导完整性**：从前提到结论是否每一步都有交代？
3. **术语一致性**：同一概念是否使用了统一的术语和符号？
4. **口吻适当性**：语气是否正式但不生硬？
5. **例子充分性**：每个抽象概念是否有具体例子支撑？
6. **公式正确性**：数学公式是否语法正确、可渲染？
7. **前置依赖**：是否所有前置概念都已解释？

#### 第六步：输出文档
**输出格式**：
- **对话输出**：直接在对话中展示讲解内容
- **Markdown 文档**：生成 `.md` 文件，包含完整的数学公式、推导、示例和参考文献
- **HTML 页面**：生成自包含的 HTML5 页面，具有精美的课本风格排版

## 示例展示

### 输入示例
```
给我讲一下反向传播算法
```

### 处理过程
1. **意图识别**：识别为学习请求
2. **背景评估**：询问用户水平（假设选择"有自学基础"）
3. **前置概念确认**：确认是否了解"链式法则"、"梯度下降"等概念
4. **前置研究**：搜索反向传播算法的原始论文和最新应用
5. **内容生成**：按照讲解框架生成完整教学内容
6. **质量自检**：检查逻辑性、完整性和一致性
7. **输出文档**：生成 HTML 页面，包含数学公式和示例

### 输出示例（片段）

#### HTML 输出预览
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>反向传播算法</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <h1>反向传播算法</h1>
    
    <h2>1. 我们究竟想解决什么问题？</h2>
    <p>当我们训练一个神经网络时，我们需要调整网络中的权重参数，使得网络的输出尽可能接近我们期望的结果。这个过程称为"训练"。</p>
    
    <h2>2. 核心思想：链式法则</h2>
    <p>反向传播算法的核心思想是微积分中的<strong>链式法则</strong>。如果我们有一个复合函数 \( f(g(x)) \)，那么它的导数可以通过以下公式计算：</p>
    <p>\[ \frac{df}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx} \]</p>
    
    <h2>3. 具体步骤</h2>
    <p>假设我们有一个简单的神经网络，包含输入层、隐藏层和输出层...</p>
</body>
</html>
```

#### Markdown 输出预览
```markdown
# 反向传播算法

## 1. 我们究竟想解决什么问题？

当我们训练一个神经网络时，我们需要调整网络中的权重参数，使得网络的输出尽可能接近我们期望的结果。这个过程称为"训练"。

## 2. 核心思想：链式法则

反向传播算法的核心思想是微积分中的**链式法则**。如果我们有一个复合函数 \( f(g(x)) \)，那么它的导数可以通过以下公式计算：

\[
\frac{df}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx}
\]

## 参考文献

1. Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*, 323(6088), 533-536.
```

## 输出格式示例

### Markdown 示例
查看 `references/examples/markdown/` 目录下的示例：
- **ppo-dpo-evolution.md**：强化学习对齐算法演进，包含完整的数学推导和理论分析
- **RAG召回与重排.md**：RAG 检索增强生成技术，涵盖召回和重排的核心原理
- **哈密顿力学体系.md**：经典力学中的哈密顿形式体系
- **诺特定理.md**：对称性与守恒定律的深刻联系

### HTML 示例
查看 `references/examples/html/` 目录下的示例：
- **index.html**：教材目录页面，展示完整的章节结构
- **docker.html**：Docker 容器化技术讲解
- **linux.html**：Linux 操作系统原理讲解
- **multi-token-prediction.html**：大模型推理加速技术
- **rag-retrieval-rerank.html**：RAG 召回与重排技术详解

## 前置要求

- **OpenCode**: 版本 1.0.0 或更高
- **Node.js**: 版本 18.0.0 或更高（用于 OpenCode 运行）
- **网络连接**：用于搜索参考资料（可选）

## 安装

### 方式一：直接复制（推荐）

```bash
# 将 knowledge-teacher 文件夹复制到你的项目目录下
cp -r knowledge-teacher your-project/.opencode/skills/
```

### 方式二：Git 克隆

```bash
cd your-project
git clone https://github.com/m1908293028-boop/Knowledge-Teacher.git .opencode/skills/knowledge-teacher
```

## 快速开始

1. **安装完成后**，在 OpenCode 中直接询问任何概念：
   ```
   给我讲一下反向传播算法
   ```

2. **Skill 会自动触发**，询问你的知识背景：
   ```
   在开始讲解之前，我想先了解一下你的基础，以便调整讲解的起点和深度。
   选项：
   - 零基础
   - 有自学基础
   - 科班出身
   - 其他
   ```

3. **选择输出格式**：
   ```
   你希望讲解内容以什么形式呈现？
   选项：
   - 对话输出
   - Markdown文档
   - HTML页面
   - 自定义组合
   ```

4. **生成教学文档**：Skill 会自动生成完整的教学文档，包含：
   - 概念定义和直觉理解
   - 数学公式和推导过程
   - 多维度示例（生活类比、学术例子、应用场景）
   - 参考文献和进一步学习路径

**预期输出**：一个完整的教学文档，包含从基础概念到高级应用的系统性讲解。

## 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| 输出格式 | string | `dialog` | 默认输出格式：`dialog`、`markdown`、`html`、`custom` |
| 讲解深度 | string | `adaptive` | 讲解深度：`basic`、`intermediate`、`advanced`、`adaptive` |
| 数学公式格式 | string | `latex` | 数学公式格式：`latex`、`mathml` |
| 自动搜索 | boolean | `true` | 是否自动搜索参考资料 |
| 质量自检 | boolean | `true` | 是否进行文档质量自检 |
| 参考文献数量 | number | `5` | 每个知识点包含的参考文献数量 |

## 常见问题 (FAQ)

### Q1: Skill 没有自动触发怎么办？
**A**: 确保你的问题包含明确的学习意图，如"讲解"、"解释"、"什么是"等关键词。如果仍然没有触发，可以手动调用：`@knowledge-teacher 讲解一下XXX`。

### Q2: 如何重置我的学习背景？
**A**: 删除记忆文件即可重置。记忆文件通常位于：
- `.opencode/memory/user-background.json`
- `.claude/memory/user-background.json`
- `.cursor/memory/user-background.json`

### Q3: 生成的文档质量不满意怎么办？
**A**: 可以通过以下方式改进：
1. 在提问时提供更具体的要求，如"请用更通俗的语言讲解"
2. 修改 `SKILL.md` 中的教学方法配置
3. 调整配置项中的讲解深度参数

### Q4: 支持哪些学科的知识点？
**A**: 目前主要支持计算机科学、数学、物理等理工科领域，但框架是通用的，可以扩展到其他学科。

### Q5: 生成的文档可以编辑吗？
**A**: 可以。生成的 Markdown 和 HTML 文档都是标准格式，可以使用任何文本编辑器或 HTML 编辑器进行修改。

### Q6: 如何提高生成文档的质量？
**A**: 建议：
1. 在提问时提供更具体的上下文，如"我是一名计算机专业学生，请讲解..."
2. 在背景评估时如实选择你的知识水平
3. 在前置概念确认时，对不了解的概念选择"请先解释"

## 项目结构

```
knowledge-teacher/
├── SKILL.md                              # Skill 主文件，包含完整的教学框架
├── README.md                             # 本文件
├── LICENSE                               # MIT 许可证
├── .gitignore                            # Git 忽略配置
├── CHANGELOG.md                          # 版本更新记录
└── references/
    ├── math-syntax.md                    # Markdown 数学公式语法指南
    ├── html-math-syntax.md               # HTML 数学公式语法指南
    ├── output-format-html.md             # HTML 输出规范
    ├── output-format-markdown.md         # Markdown 输出规范
    ├── network-error-handling.md         # 网络异常处理流程
    ├── image-download-process.md         # 图片下载处理流程
    └── examples/
        ├── html/                         # HTML 格式示例
        │   ├── index.html                # 教材目录页面
        │   ├── docker.html               # Docker 容器化技术
        │   ├── linux.html                # Linux 操作系统
        │   ├── multi-token-prediction.html # 大模型推理加速
        │   └── rag-retrieval-rerank.html  # RAG 召回与重排
        └── markdown/                     # Markdown 格式示例
            ├── ppo-dpo-evolution.md      # PPO/DPO 演进算法
            ├── RAG召回与重排.md           # RAG 检索技术
            ├── 哈密顿力学体系.md          # 哈密顿力学
            └── 诺特定理.md               # 诺特定理
```

## 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

### 贡献方式
1. **报告问题**：在 GitHub 上提交 Issue
2. **提交代码**：Fork 项目，创建功能分支，提交 Pull Request
3. **改进文档**：直接编辑 README.md 或其他文档文件

### 开发规范
- 遵循现有的代码风格和文档格式
- 添加新功能时请更新相关文档
- 确保所有示例都能正常运行

### 联系方式
- GitHub: [m1908293028-boop/Knowledge-Teacher](https://github.com/m1908293028-boop/Knowledge-Teacher)
- 问题反馈: [GitHub Issues](https://github.com/m1908293028-boop/Knowledge-Teacher/issues)

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```