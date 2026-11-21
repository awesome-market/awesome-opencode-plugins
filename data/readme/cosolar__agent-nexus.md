# Agent Nexus — AI Agent 开源生态图谱

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-贡献指南)

> 🤖 数据来源：GitHub API / GitHub Trending / 技术媒体交叉验证 | 数据真实可查
>
> 📊 收录 **23 大类 / 449 个开源项目**，统一 5 列表格；星数经 GitHub API 实测，精确采集时间见 `data/projects.json` 的 `stars_as_of` 字段。
>
> 📅 最新分析：[2026-11-03 · Agent 生态周报](analysis/2026-11-03.md) — 覆盖 10.20—11.02 的重大变化、十大趋势与选型建议。

![AI 开发者必备 Agent 开源生态图谱](assets/intro.png)

## 📑 目录

| 分类     | 章节              | 一句话定位                           |   条目数   | 头部项目                |
| :----- | :-------------- | :------------------------------ | :-----: | :------------------ |
| 一 | 🤖 Agent 框架 | 从「能跑」到「带缰绳」，百亿俱乐部扩容 | 110 | REA |
| 二 | 🧩 Agent Skills | GitHub 涨星最快品类，已卷到专业工具链 | 24 | Superpowers |
| 三 | 🦞 个人 AI 助手 | 全平台常驻，本地优先成主流 | 12 | OpenClaw |
| 四 | 🚀 AI 编程 / 开发工具 | 编码 Agent 三强 + 评审 / 并行 / 逆向三新层 | 37 | Codex CLI |
| 五 | 📚 RAG & 知识库 | 企业知识平台 / 上下文数据库 / 会话记忆三层分化 | 30 | claude-mem |
| 六 | ⚡ 推理 & 部署 | 本地推理 + 网关 + 国产算力解绑 | 20 | Ollama |
| 七 | 🏋️ 训练 / 微调 | LoRA 生态稳定盘 | 10 | Unsloth |
| 八 | 🎨 图像 / 视频生成 | 开源剪辑与 Agent 视频流水线 | 26 | SD WebUI |
| 九 | 🎤 语音 / 音频 | 本地语音工作室双雄 | 13 | Whisper |
| 十 | 👁️ 计算机视觉 | OCR 与分割 | 7 | OpenCV |
| 十一 | 🗄️ 向量数据库 | 六强格局 | 6 | Milvus |
| 十二 | 🔢 嵌入 / 检索 | 多模态嵌入补位 | 3 | Jina |
| 十三 | 🔌 协议 / 标准化 | MCP 事实标准 + Agent-Native 工具层 | 15 | awesome-mcp-servers |
| 十四 | 🖥️ UI 平台 | 开源 Chat 界面 | 5 | Open WebUI |
| 十五 | 🔄 工作流自动化 | 低代码 + Agent 节点 | 8 | n8n |
| 十六 | 📈 监控 / 评估 | 可观测性与评测 | 5 | LangFuse |
| 十七 | 🛡️ AI 安全与防护 | 事前扫描 + 事中拦截 + 事后审计 | 14 | strix |
| 十八 | 💰 AI 金融 / 量化 | 多 Agent 投研 | 5 | TradingAgents |
| 十九 | 🏢 Agent 办公自动化 | 并行 Agent 调度与 Office 套件 | 5 | orca |
| 二十 | 🧠 大模型（开源权重） | 开源 vs 开权重之争 | 28 | DeepSeek-V3/V4 |
| 二十一 | 🏗️ 基础框架 | 底座稳定盘 | 9 | TensorFlow |
| 二十二 | 🤖 具身智能 / 机器人 | 世界模型 + VLA | 8 | UnifoLM-WLA-1.0 |
| 二十三 | 📚 AI 学习教程 / 路线图 | 开源书 / 体系课 / 从零实现 / Cookbook / 中文社区 | 49 | awesome-llm-apps |
| **合计** | **23 大类** | **框架 → 技能 → 记忆 → 推理 → 安全 → 具身 → 教程** | **449** | — |

## 📅 分析存档

按分析日期归档，最新在上。项目清单常驻本页，事件与趋势详见各期周报。

| 日期 | 覆盖区间 | 内容 |
| :---: | :--- | :--- |
| [2026-11-03](analysis/2026-11-03.md) | 10-20 — 11-02 | 重大变化速览 · 十大趋势 · 选型四问 · 三个警惕信号 |

## 开源项目

### 一、🤖 Agent 框架（110+ 项目，最热赛道）

#### 👑 超级巨星（⭐ 100k+）

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**REA**](https://github.com/morluto/rea)                                     | ⭐ **456k** | TypeScript | morluto（独立开发者）       | **「🆕 万物皆可逆向的 Agent 工具编排层」** 🆕 **本轮最大现象级项目：10 月上旬不足 2 万星 → 10 月 15 日 26.09 万⭐**，连续约 8 天霸榜 GitHub 日榜第一（单日峰值 +2.5 万）。"Reverse Engineer Anything"——不是又一个提示词包，而是把 **Ghidra headless、Hopper（Unix socket）、IDA（上游 MCP）、pinned JADX、Binwalk/Unblob、CDP/Playwright** 整条逆向工具链桥接给编码 Agent，覆盖 20+ 目标类型（原生、.NET、WASM、EVM 字节码、Electron、APK、固件、HAR）。`npx rea-agents setup` 一行注册进 Claude Code / Codex / Cursor / Gemini CLI / Grok Build 等 13+ 客户端，MIT 许可，仓库创建于 4 月 14 日。强制"证据契约"输出（产物身份 / 源码位置 / 观测 / 推断 / 未决结论），并附 DX-Ball、Notion、TH04、Aegis 四个完整案例。 |
| [**Hermes Agent**](https://github.com/NousResearch/hermes-agent)              | ⭐ **263k** |   Python   | Nous Research        | **「自进化 AI Agent」** 2026年增长最猛的Agent项目，采用三层记忆架构（短期/长期/元记忆），能与用户共同进化。支持自我反思、自主学习和个性化适配，**10 月 15 日实测 25.4 万星**（Repo Tagline："The agent that grows with you"），代表了Agent从"工具"到"伙伴"的范式跃迁。核心亮点：skill失败时自动修复，让下一次运行更稳。                                                                                                                                                                                                                                                                                                                           |
| [**DeepSeek Harness (DSH)**](https://github.com/deepseek-ai/deepseek-harness) | ⭐ **280k** | TypeScript | DeepSeek             | **「万物皆插件 Agent 平台」** 🆕 **2026年8月13日开源，10 月 14—15 日突破 25 万⭐**。核心理念"Everything is a Plugin"——将 Agent 能力（对话、工具、MCP、技能、子Agent、UI）全部封装为可插拔插件。MIT许可，TypeScript编写。**10月里程碑：官方插件直接把 Claude Code / Codex 变成可插拔组件**，harness 之间从竞争走向互操作。**10 月 3 日的 v0.2.1-alpha.1 还塞进了实验性的 Claude Code Mods 兼容层**；npm 包 `@deepseek-ai/dsh` 截至 10 月 4 日单周下载 45.2 万次。插件生态（桌面端3个实现、插件市场、皮肤系统、awesome 列表）合计超30万⭐，是继 AutoGPT 之后增速最快的新开源项目。                                                                                                                            |
| [**AutoGPT**](https://github.com/Significant-Gravitas/AutoGPT)                | ⭐ **188k** |   Python   | Significant Gravitas | **「自主 AI Agent 始祖」** 全球首个自主AI Agent项目，支持自动任务分解、多步推理和工具调用，开创了Agent赛道。内置插件生态和可视化工作流编辑器，是理解Agent范式的入门必读。                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| [**LangChain**](https://github.com/langchain-ai/langchain)                    | ⭐ **149k** |   Python   | LangChain Inc        | **「Agent 工程平台」** LLM应用开发的事实标准框架，提供链式调用、工具绑定、记忆管理、Agent编排等核心能力。生态最完整，社区最活跃，几乎所有Agent项目都直接或间接基于LangChain构建。                                                                                                                                                                                                                                                                                                                                                                                                                               |
| [**pi**](https://github.com/earendil-works/pi) | ⭐ **122k** | TypeScript | earendil-works | 🆕 **本轮补漏的最大发现**：一个「AI Agent 工具包」——统一 LLM API + Agent 循环 + TUI + 编码 Agent CLI。12 万星却几乎没进中文圈视野，是 harness 层的隐形巨头。 |
| [**Paperclip**](https://github.com/paperclipai/paperclip)                     | ⭐ **113k** | TypeScript | Paperclip AI         | **「🆕 "跑一家公司"的 Agent 编排平台」** 🆕 **2026年9月底爆红，10 月中旬正式跨过 10 万星**。MIT许可，口号"Run a Company of AI Agents"——为Agent团队提供**组织架构图、角色分工与预算管理**的编排层，不替代现有工具而是统一调度。仓库创建于 3 月 2 日，是"Agent公司化"理念最完整的开源落地。                                                                                                                                                                                                                                                                                                                                              |

#### 🌟 准巨星（⭐ 50k - 100k）

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**DeerFlow**](https://github.com/bytedance/deer-flow)         | ⭐ **85.3k** | Python | 字节跳动                                 | **「长周期 SuperAgent」** 字节跳动开源的深度研究Agent框架，支持长周期任务的规划、执行与反思闭环。通过沙箱、记忆、工具、技能、子Agent和消息网关处理从几分钟到几小时的多层级任务，**9月初持续增长至81k+**；10 月 15 日实测 **8.39 万⭐**。社区热议 **DeerFlow 2.0**（10 月 10 日的 harness 横评多次点名），但截至本版未见正式 2.0 仓库，留待下一版核实。           |
| [**MiroFish**](https://github.com/666ghj/MiroFish)             | ⭐ **85.4k** | Python | MiroMind 系（仓库实际路径 `666ghj/MiroFish`） | **「🆕 通用群体智能引擎」** 🆕 多智能体社会仿真引擎，用大规模Agent群体模拟社会传播、舆论演化与决策推演，10月初入选GitHub Python热点Top榜。⚠️ 上一版链接写作 `MiroMind/MiroFish` 已 404，正确路径为 `666ghj/MiroFish`（另有社区离线镜像 `nikmcfly/MiroFish-Offline` 2,616⭐）。与"950个Claude Agent协作发现新酶"同属群体智能方向。 |
| [**MetaGPT**](https://github.com/geekan/MetaGPT)               | ⭐ **71.3k** | Python | DeepWisdom                           | **「多 Agent 模拟软件公司」** 用多个AI Agent模拟完整软件开发团队（产品经理、架构师、工程师、QA），自动生成需求文档、系统设计、代码和测试，是Multi-Agent协作范式的开创者。                                                                                                                              |
| [**AutoGen**](https://github.com/microsoft/autogen) | ⭐ **61.8k** | Python | Microsoft | 🆕 多 Agent 对话协作框架的**元老**。2026 年 4 月起与 Semantic Kernel 合并进 Microsoft Agent Framework，本体转入维护轨道——**读它是理解「多 Agent 对话范式」的起点**。 |
| [**OpenManus**](https://github.com/FoundationAgents/OpenManus) | ⭐ **59k** | Python | FoundationAgents                     | **「通用 Agent 平台」** Manus AI的开源复刻版，2026年增长最快的Agent项目之一。支持多步任务规划、工具调用和环境交互，提供完整的Agent运行时和可视化界面，降低了构建通用Agent的门槛。                                                                                                                       |
| [**CrewAI**](https://github.com/crewAIInc/crewAI)              | ⭐ **60.8k** | Python | CrewAI Inc                           | **「角色扮演式编排」** 以"船员"比喻Agent协作的编排框架。**1.14.6稳定版（5月28日）+ 6月11日更新**：可插拔默认后端（memory/knowledge/RAG/flow）、对话流Chat API、范围化运行时状态。API设计优雅简洁，上手极快。                                                                                            |
| [**DeepTutor**](https://github.com/HKUDS/DeepTutor)            | ⭐ **58.7k** | Python | HKUDS                                | 🆕 终身个性化 AI 辅导 Agent：多 LLM + RAG 检索 + 智能教学代理，11-01 日榜单日 +1,170。**教育场景里第一个冲进 5 万星梯队的 Agent**，也是「Agent 做长期陪伴型任务」的样本。                                                                                                                 |
| [**Goose**](https://github.com/aaif-goose/goose)               | ⭐ **56.5k** |  Rust  | Agentic AI Foundation                | **「MCP优先 Agent」** 🆕 Block（原Square）出品的开源AI Agent，Rust编写。**2025年12月捐赠给Linux基金会旗下Agentic AI Foundation**，与MCP、AGENTS.md同列，厂商中立治理。70+ MCP扩展，支持代码编辑、命令执行和测试运行，Apache 2.0许可。                                                            |

#### ⭐ 快速增长（⭐ 10k - 50k）

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**nanobot**](https://github.com/HKUDS/nanobot)                         | ⭐ **50k** |   Python   | HKUDS         | **「轻量 AI Agent」** 港大数据科学实验室出品，仅4000行代码实现完整Agent能力。极简设计哲学，零依赖、高性能，适合嵌入到现有系统中。                                                                                                                           |
| [**CowAgent**](https://github.com/zhayujie/CowAgent)                    | ⭐ **47.9k** |   Python   | zhayujie      | **「超级 AI 助手」** 国产超级AI助手，集成多模型对话、知识库、插件系统和多模态能力。支持微信/企微/飞书等多平台接入，是国内最活跃的AI助手开源项目。                                                                                                                       |
| [**Agno**](https://github.com/agno-agi/agno)                            | ⭐ **43.2k** |   Python   | Agno AGI      | **「极速轻量 Agent 框架」** 前身为Phidata，主打极速和轻量。Type-safe的API设计，内置RAG、记忆和工具调用。**🆕 v3.1.0（2026年10月2日）**：新增RBAC权限体系、AgentOS数据库文件系统（DbFileSystem）、MCP工具行为显式化，V3→V3.1有破坏性变更需按升级指南迁移。                               |
| [**OpenMAIC**](https://blog.csdn.net/u130130/article/details/166899588) | ⭐ **39.6k** | TypeScript | 未确认           | **「多智能体互动课堂」** 🆕 **2026年9月热榜项目**（9月月榜收录）。开放的多智能体AI互动课堂平台——多个Agent分别扮演教师、助教、同学，在虚拟教室里以对话和协作方式教学。是"Agent进入教育场景"的代表项目。                                                                                   |
| [**LangGraph**](https://github.com/langchain-ai/langgraph)              | ⭐ **44.9k** |   Python   | LangChain Inc | **「有向图 Agent 工作流」** 🆕 **v1.0 GA（2025年10月）→ v1.2.0（2026年5月12日）**：新增节点级超时、错误恢复（Saga/补偿路由）、DeltaChannel降低长线程checkpoint开销、v2类型化流式API。深度集成LangSmith可观测性，是构建复杂Agent工作流的首选工具。                                |
| [**DSPy**](https://github.com/stanfordnlp/dspy)                         | ⭐ **39k** |   Python   | Stanford NLP  | **「LLM 编程框架」** 斯坦福NLP出品，将LLM提示工程从"手工调参"提升为"自动编译"。通过声明式编程自动优化Prompt和Few-shot示例，是Prompt Engineering科学化的里程碑。                                                                                              |
| [**AgentGPT**](https://github.com/reworkd/AgentGPT)                     | ⭐ **36.3k** | TypeScript | reworkd       | **「浏览器端 Agent」** 将AutoGPT的能力搬到浏览器中，提供直观的Web界面来配置和运行自主Agent。无需本地环境搭建，降低了Agent使用门槛。                                                                                                                      |
| [**ChatDev**](https://github.com/OpenBMB/ChatDev)                       | ⭐ **34.7k** |   Python   | OpenBMB       | **「多 Agent 模拟软件公司」** 清华团队出品，用多Agent模拟虚拟软件公司。Agent之间通过自然语言对话协作完成软件开发全流程。                                                                                                                                |
| [**SmolAgents**](https://github.com/huggingface/smolagents)             | ⭐ **30.3k** |   Python   | HuggingFace   | **「极简 Agent」** HuggingFace出品的极简Agent框架，核心代码不到1000行。支持Code Agent范式（Agent直接写代码执行任务），与HuggingFace生态深度集成。                                                                                                  |
| [**AgentScope**](https://github.com/modelscope/agentscope)              | ⭐ **35.9k** |   Python   | 阿里达摩院         | **「可观测 Agent」** 阿里达摩院出品的多Agent平台，强调可观测性和可控性。提供丰富的Agent模板、分布式运行时和可视化调试工具。                                                                                                                               |
| [**OpenAI Agents SDK**](https://github.com/openai/openai-agents-python) | ⭐ **30.6k** |   Python   | OpenAI        | **「轻量多 Agent」** OpenAI官方Agent开发SDK，提供Agent定义、工具绑定、交接（handoff）和防护栏等核心能力。**2026年6月更新**：分层子Agent生成（最多3层）、fallback模型链、按Agent成本归因。                                                                          |
| [**Crush**](https://github.com/charmbracelet/crush)                     | ⭐ **29.1k** |     Go     | Charm         | **「终端 AI Agent」** 🆕 Charm出品的终端AI编码Agent，Go语言编写。优雅的TUI界面，支持多模型、MCP集成和会话管理，是终端重度用户的新选择。                                                                                                                 |
| [**Mastra**](https://github.com/mastra-ai/mastra)                       | ⭐ **29.5k** | TypeScript | Mastra AI     | **「TypeScript Agent 框架」** TypeScript生态最热门的Agent框架，提供类型安全的Agent构建API。内置工作流引擎、RAG和评估工具，与Vercel AI SDK深度集成。                                                                                               |
| [**Haystack**](https://github.com/deepset-ai/haystack)                  | ⭐ **27k** |   Python   | deepset       | **「NLP/RAG 编排」** deepset出品的NLP和RAG编排框架，提供模块化的Pipeline架构。擅长文档搜索、问答和RAG场景。                                                                                                                               |
| [**Vercel AI SDK**](https://github.com/vercel/ai)                       | ⭐ **27.9k** | TypeScript | Vercel        | **「前端 AI 开发 SDK」** Vercel出品的AI开发SDK，让前端开发者轻松集成LLM能力。支持流式输出、工具调用和多模型切换。                                                                                                                                 |
| [**Grok Build**](https://github.com/xai-org/grok-build)                 | ⭐ **27.8k** |    Rust    | SpaceXAI      | **「终端编码 Agent」** 🆕 **2026年7月14日开源**，Apache 2.0。SpaceXAI（前xAI）出品的终端AI编码Agent，Rust全量源码。包含Agent循环、工具层（读/改代码、搜索、命令执行）、终端UI和扩展系统（skills、plugins、hooks、MCP servers、subagents）。原生X/Twitter实时数据接入，支持完全本地优先运行。 |
| [**Letta**](https://github.com/letta-ai/letta)                          | ⭐ **25.4k** |   Python   | Letta AI      | **「有状态 Agent」** 前身为MemGPT，专注解决LLM的上下文窗口限制。通过虚拟上下文管理和长期记忆机制，让Agent拥有"无限记忆"能力。                                                                                                                           |
| [**BabyAGI**](https://github.com/yoheinakajima/babyagi)                 | ⭐ **22.4k** |   Python   | yoheinakajima | **「自主任务 Agent 先驱」** 最早的自主Agent项目之一，用极简代码实现了任务创建、优先级排序和自主执行的完整循环。                                                                                                                                       |
| [**OpenAI Swarm**](https://github.com/openai/swarm)                     | ⭐ **22.1k** |   Python   | OpenAI        | **「轻量多 Agent 协作」** OpenAI出品的实验性多Agent框架，主打轻量级Agent协作和交接。设计极简，强调教学价值。                                                                                                                                   |
| [**coze-studio**](https://github.com/coze-dev/coze-studio) | ⭐ **21.8k** | TypeScript | 字节跳动 | 🆕 扣子（Coze）的**开源自托管版**：一体化可视化 Agent 开发平台，创建 / 调试 / 发布全流程。字节把商业产品的骨架直接开源，是「平台型 Agent」里最完整的一份。 |
| [**Guidance**](https://github.com/guidance-ai/guidance)                 | ⭐ **21.8k** |   Python   | Microsoft     | **「LLM 结构化控制」** 微软出品，通过约束LLM输出来实现结构化和可控的文本生成。将传统编程的控制流引入LLM调用。                                                                                                                                         |
| [**Google ADK**](https://github.com/google/adk-python)                  | ⭐ **22.2k** |  Python/Go | Google        | **「企业级 Agent 开发套件」** Google推出的Agent Development Kit，提供Agent构建、工具集成、多Agent编排和企业级安全等全套能力。                                                                                                                |
| [**Suna**](https://github.com/kortix-ai/suna)                           | ⭐ **20.7k** | TypeScript | Kortix AI     | **「自主通用 Agent」** 🆕 通用自主AI Agent平台，支持浏览器自动化、数据采集、文档处理和深度研究。提供完整的Agent运行时和可视化界面，增长迅速。                                                                                                                   |
| [**OWL**](https://github.com/camel-ai/owl)                              | ⭐ **20.2k** |   Python   | CAMEL-AI      | **「多 Agent 协作」** CAMEL-AI团队出品的多Agent协作框架，在GAIA等Agent基准测试中表现优异。                                                                                                                                         |
| [**DB-GPT**](https://github.com/eosphoros-ai/DB-GPT)                    | ⭐ **20.3k** |   Python   | eosphoros     | **「数据驱动 Agent」** 专注数据库场景的Agent框架，支持自然语言查数据、智能数据分析和可视化。                                                                                                                                                 |
| [**agent-zero**](https://github.com/agent0ai/agent-zero) | ⭐ **19.8k** | Python | agent0ai | 🆕 非预定义型 Agent 框架：不写死流程，Agent 在使用中动态生长、持续学习。**与「工作流编排」是两条相反的路线。** |
| [**Pydantic AI**](https://github.com/pydantic/pydantic-ai) | ⭐ **21.2k** | Python | Pydantic | **「类型安全 Agent」** 🆕 **V2于2026年6月23日稳定发布**：harness-first重设计，引入"capability"核心原语（打包tools+hooks+instructions+model settings）。FastAPI风格工程体验，V1到V2为破坏性变更。 |
| [**rowboat**](https://github.com/rowboatlabs/rowboat) | ⭐ **18.2k** | TypeScript | rowboatlabs | 🆕 「AI 同事」：带记忆与协作能力，几分钟内把多 Agent 工作流搭起来。 |
| [**SuperAGI**](https://github.com/TransformerOptimus/SuperAGI) | ⭐ **17.7k** | Python | TransformerOptimus | **「模块化自主 Agent 平台」** 模块化的自主Agent平台，提供Agent创建、工具市场、资源管理和并发控制等企业级功能。 |
| [**Camel**](https://github.com/camel-ai/camel) | ⭐ **18k** | Python | CAMEL-AI | **「多 Agent 通信先驱」** 学术界最早的多Agent框架之一，首创了Agent间的角色扮演对话模式。 |
| [**Qwen-Agent**](https://github.com/QwenLM/Qwen-Agent) | ⭐ **17.3k** | Python | 阿里通义 | 🆕 阿里官方 Agent 框架：Function Calling、代码解释器、RAG、Chrome 扩展一应俱全，与 Qwen 系列深度配套。**国产模型方的「第一方框架」**，和模型一起迭代。 |
| [**Outlines**](https://github.com/dottxt-ai/outlines) | ⭐ **16k** | Python | dottxt-ai | **「LLM 结构化输出」** 通过有限状态机和正则约束实现LLM输出的100%结构化。 |
| [**Instructor**](https://github.com/instructor-ai/instructor) | ⭐ **14.1k** | Python | jxnl | **「LLM 结构化输出」** 基于Pydantic的LLM结构化输出库，通过类型注解让LLM直接返回Python对象。 |
| [**Agent-S**](https://github.com/simular-ai/Agent-S) | ⭐ **13k** | Python | Simular | 🆕 开源 computer-use Agent 的 SOTA 系列：像人一样看屏幕、点鼠标，是 CUA 赛道最常被引用的基线。 |
| [**Microsoft Agent Framework**](https://github.com/microsoft/agent-framework) | ⭐ **14.7k** | C#/Python | Microsoft | **「企业级统一 Agent 框架」** 🆕 **2026年4月3日发布1.0**，将 Semantic Kernel + AutoGen 合并为单一生产级SDK（.NET + Python特性对齐），命名空间 `Microsoft.Agents.AI`。原生支持MCP与A2A协议，紧密集成Azure AI Foundry。原SK与AutoGen v0.4转入维护轨道。 |
| [**JoyAgent-JDGenie**](https://github.com/jd-opensource/joyagent-jdgenie) | ⭐ **11.9k** | Java | 京东 | 🆕 京东开源的**端到端产品级通用智能体**，Java 技术栈——国内少见的「开箱即用整机方案」，而不是又一个 SDK。 |
| [**cloudflare-os**](https://blog.csdn.net/u130130/article/details/167174473) | ⭐ **11.0k** | TypeScript | 未确认（Cloudflare 系） | **「🆕 Agent 企业工作区」** 🆕 **2026年10月初热榜**。基于 Cloudflare Workers 的"公司级Agent工作空间"——内置安全框架与沙箱机制，把Agent接入企业账号、边界与合规体系。云厂商亲自下场定义"Agent运行时该长在哪"。 |
| [**VoltAgent**](https://github.com/VoltAgent/voltagent) | ⭐ **11k** | TypeScript | VoltAgent | **「Agent 工程平台」** 🆕 TypeScript生态Agent工程平台，内置可观测性、评估工具和工作流引擎。 |

#### 🔧 潜力新星（⭐ 10k 以下，含 8—10 月新开源的小体量项目）

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**MobileAgent**](https://github.com/X-PLUG/MobileAgent) | ⭐ **9.4k** | Python | 阿里 X-PLUG | 🆕 移动设备 GUI Agent 家族：让 Agent 直接操作手机 App，不依赖无障碍接口。 |
| [**PraisonAI**](https://github.com/MervinPraison/PraisonAI) | ⭐ **9.3k** | Python | MervinPraison | 🆕 低代码多 Agent 系统：融合 AutoGen / CrewAI 的思路，强调「少写胶水代码」，一句 `pip install` 就能起一套 Agent 团队。 |
| [**Astron Agent**](https://github.com/iflytek/astron-agent) | ⭐ **8.9k** | Java | 科大讯飞 | 🆕 企业级、商业友好的 Agentic 工作流平台，面向 SuperAgent 构建，主打私有化与合规。 |
| [**XAgent**](https://github.com/OpenBMB/XAgent) | ⭐ **8.6k** | Python | OpenBMB | **「自主复杂任务求解」** 清华团队出品的自主Agent，专注于复杂任务的自动分解和执行。 |
| [**MiroThinker**](https://github.com/MiroMindAI/MiroThinker) | ⭐ **8.5k** | Python | MiroMind | 🆕 开源**搜索 Agent 模型**，对标 OpenAI / Gemini Deep Research，专攻工具增强推理与真实信息检索。**「Agent 专用模型」这一支的代表。** |
| [**Voyager**](https://github.com/MineDojo/Voyager) | ⭐ **7.3k** | Python | NVIDIA | **「具身终身学习 Agent」** NVIDIA出品，在Minecraft中实现具身Agent的终身学习。 |
| [**OpenSquilla**](https://github.com/TokenRhythm/opensquilla) | ⭐ **7.1k** | Python | TokenRhythm | 🆕 令牌高效的**微内核** Agent——把「省 token」做进架构而不是提示词，内核极小、能力靠插件。 |
| [**PRAXIST**](https://github.com/sapientinc/PRAXIST) | ⭐ **5.5k** | Python | Sapient Inc | **「自主研究 Agent」** 🆕 **2026年8月27日开源**。自主研究系统，核心创新是"可测量、可计算机执行"的研究范式——不满足于写论文，而是产出可被计算机自动验证的研究成果。一周内冲上6k+⭐，代表Agent从"写代码"扩展到"做科研"的新方向。 |
| [**SandBox**](https://github.com/agent-infra/sandbox) | ⭐ **6.3k** | Python | agent-infra | 🆕 一体化 Agent 沙箱：**单个 Docker 容器**内集成浏览器、Shell、文件、MCP 与 VSCode Server。Agent 执行环境的「标准集装箱」。 |
| [**TaskWeaver**](https://github.com/microsoft/TaskWeaver) | ⭐ **6.2k** | Python | Microsoft | **「代码优先数据分析 Agent」** 微软出品的代码优先Agent，擅长数据分析和可视化。 |
| [**Nexent**](https://github.com/ModelEngine-Group/nexent) | ⭐ **6.2k** | Python | ModelEngine | 🆕 零代码生成 Agent 平台：不用拖拽编排，用自然语言直接生成 Agent——「编排」本身也被 Agent 化了。 |
| [**Agents**](https://github.com/aiwaves-cn/agents) | ⭐ **6k** | Python | AIWaves | 🆕 面向数据的**自演进** Agent 框架，主打「Agent 随数据一起进化」，与 EvoAgentX 同属「会改自己的 Agent」方向。 |
| [**AG2**](https://github.com/ag2ai/ag2) | ⭐ **5.1k** | Python | AG2 AI | **「AutoGen 社区版」** AutoGen项目的社区活跃分支，**正迈向v1.0**，对ConversableAgent、GroupChat等进行整理与弃用清理。 |
| [**DeepAnalyze**](https://github.com/ruc-datalab/DeepAnalyze) | ⭐ **4.8k** | Python | 人大 DataLab | 🆕 首个**自主数据科学** Agentic LLM：从取数、清洗、分析到产出分析师级报告，把「数据科学」整条链路交给 Agent。 |
| [**Youtu-Agent**](https://github.com/TencentCloudADP/youtu-agent) | ⭐ **4.6k** | Python | 腾讯云 ADP | 🆕 「仅用开源模型就能交付」的 Agent 框架，强调可落地而非刷榜。 |
| [**Vercel Eve**](https://github.com/vercel/eve) | ⭐ **5.9k** | TypeScript | Vercel | **「文件系统优先 Agent 框架」** 🆕 Vercel出品的开源Agent框架，核心理念"**文件系统即创作界面**"。Agent能力以约定文件结构存在（instructions.md、agent.ts等），项目更易检查、扩展和运维。`vercel deploy`一键部署，Apache 2.0许可。 |
| [**OpenBot**](https://github.com/CopilotKit/OpenBot) | ⭐ **11.7k** | TypeScript | CopilotKit | **「开源 AI 同事」** 🆕 **2026年8月17日开源**，MIT许可。每个AI Agent拥有自己的电脑——独立浏览器、文件和工具。核心理念：**每个动作执行前先决定、执行后留痕**（decide→act→record）。支持AG-UI协议接入任意Agent，是Agent治理（governance）理念的代表项目。 |
| [**OpenAgents**](https://github.com/openagents-org/openagents) | ⭐ **4.4k** | TypeScript | openagents-org | 🆕 面向开放协作的 **Agent 网络**——Agent 之间互相发现、互相调用，是「Agent 互联网」理念的落地尝试。 |
| [**agent-desktop**](https://github.com/vercel-labs/agent-desktop) | ⭐ **22.8k** | Rust | Vercel Labs | 🆕 跨平台 CLI + C 库，用**操作系统无障碍树**让 Agent 读取与操作桌面应用，绕开像素匹配。**桌面自动化从「截图点按」转向「语义操作」。** |
| [**LazyLLM**](https://github.com/LazyAGI/LazyLLM) | ⭐ **3.9k** | Python | LazyAGI | 🆕 低代码多 Agent 应用开发工具，配套 LazyCraft 平台，主打「从原型到上线」的最小阻力路径。 |
| [**treg**](https://blog.csdn.net/u130130/article/details/166899588) | ⭐ **3.8k** | Python | 未确认 | **「Agent 工具注册系统」** 🆕 **2026年9月热榜**（9月月榜收录）。面向AI Agent的工具注册与代理系统（Tool Registry）——把分散的MCP/函数/技能统一注册、发现和路由，是Agent工具层的"服务注册中心"。 |
| [**sprix-sage-router**](https://github.com/wang2122/sprix-sage-router) | ⭐ **3.6k** | Python | 屿智同行 | **「A2A Agent 路由器」** 🆕 **2026年8月18日开源**，MIT许可。为A2A Agent网络提供状态感知的SELF/COLLABORATE/HANDOFF三态路由，解决多Agent网络中"谁该处理这个任务"的动态路由问题。 |
| [**cumora**](https://github.com/yetone/cumora) | ⭐ **4.2k** | TypeScript | yetone | **「Agent 团队聊天」** 🆕 **2026年8月17日开源**，MIT许可。跨平台团队聊天，AI Agent作为一等公民参与——支持Cloud或自带模型（Claude Code/Codex作为"大脑"）。解决了多Agent协作中"Agent之间怎么沟通"的痛点，将团队聊天从"人与人"扩展到"人与Agent"。 |
| [**BeeAI**](https://github.com/i-am-bee/beeai-framework) | ⭐ **3.5k** | TypeScript | IBM Research | **「IBM 多 Agent 框架」** IBM研究院出品的多Agent框架，基于开放协议设计，支持跨框架的Agent互操作。 |
| [**EvoAgentX**](https://github.com/ANative-Lab/EvoAgentX) | ⭐ **3.4k** | Python | ANative Lab | 🆕 构建可自我演进的 Agent 生态：自动生成、评测、迭代 Agent 工作流。 |
| [**ii-agent**](https://github.com/Intelligent-Internet/ii-agent) | ⭐ **3.4k** | Python | Intelligent Internet | 🆕 新一代 Agent 框架，主打「构建 + 部署」一条龙，面向研究型长任务。 |
| [**PenguinHarness**](https://github.com/Prism-Shadow/penguin-harness) | ⭐ **3.2k** | TypeScript | Prism-Shadow | 🆕 统一的 **RSI（递归自我改进）平台**，桌面 / 服务器直接跑的自动化 Agent 构建器。 |
| [**TokenEconomizer**](https://github.com/microsoft/TokenEconomizer) | ⭐ **5.9k** | Python | Microsoft | 🆕 黑盒成本控制框架：微技能记忆 + 工具裁剪 + 失败循环干预，专治编码 Agent「越跑越贵」。**成本优化开始从「换模型」下沉到「改运行时」。** |
| [**MoA**](https://github.com/togethercomputer/MoA) | ⭐ **3k** | Python | Together AI | 🆕 Mixture-of-Agents：用多个 LLM 的集体输出提升单次回答质量（AlpacaEval 65.1%）。**「多模型投票」的经典实现。** |
| [**Atlas**](https://we0.ai/articles/github-trending-september-3-2026-ai-agent-e03e7f0d) | ⭐ **2.9k** | Rust | Atlas | **「多 Agent 会话版本控制」** 🆕 **2026年9月热榜**。Rust编写，为多Agent编码会话提供"源码管理"——并行Agent的产出可diff、可回溯、可合并。与orca、walgit共同构成并行编码Agent的Git层基建。 |
| [**fx**](https://github.com/vercel-labs/fx) | ⭐ **3.8k** | Zig | Vercel Labs | **「Unix 风格编码 Agent」** 🆕 **2026年8月11日开源**，Apache 2.0。Vercel Labs出品，用 **Zig** 编写的终端编码Agent，核心理念"Unix like coding agent"——极简、组合式、一切皆管道。代表了编码Agent从TypeScript/Rust向系统级语言扩展的新趋势。 |
| [**OmAgent**](https://github.com/om-ai-lab/OmAgent) | ⭐ **2.7k** | Python | OM AI Lab | 🆕 多模态 Agent 框架（EMNLP 2024），支持视频 / 图像 / 音频的复杂任务编排。 |
| [**AgentField**](https://github.com/Agent-Field/agentfield) | ⭐ **2.7k** | Go | Agent Field | 🆕 把 Agent 当 API / 微服务**运营**的控制平面：路由、记忆、可观测性、身份、鉴权、策略一体。**「Agent 的 Kubernetes 化」。** |
| [**agentUniverse**](https://github.com/agentuniverse-ai/agentUniverse) | ⭐ **2.4k** | Python | 蚂蚁集团 | 🆕 蚂蚁的多智能体框架，沉淀金融级领域模式（PEER / DOE），强调「可复用的协作范式」而不是又一套 SDK。 |
| [**Lagent**](https://github.com/InternLM/lagent) | ⭐ **2.3k** | Python | 上海 AI Lab | 🆕 轻量 Agent 框架，书生系配套，二次开发成本低。 |
| [**dsh-superagent-prototype**](https://github.com/deepseek-ai/dsh-superagent-prototype) | ⭐ **22.8k** | TypeScript | DeepSeek | 🆕 **11-01 开源的研究原型**：面向单个 GitHub 仓库的**主动编码代理**，Router / Ticket / Worker 三件套把「持续接活」与「执行」拆开，自动建工作项并提 PR，模拟调度 P95 15.7 分钟（对比 29.5 分钟）。首日即进日榜前五。 |
| [**OxyGent**](https://github.com/jd-opensource/OxyGent) | ⭐ **2.1k** | Python | 京东 | 🆕 ACL 2026 论文配套：让多 Agent 系统更「模块化、可替换」，京东在 Agent 框架层的第二枚棋子。 |
| [**rakazo**](https://github.com/elie222/rakazo) | ⭐ **8.1k** | TypeScript | elie222 | **「开源 Grok Bot 替代」** 🆕 **2026年8月13日开源**，Apache 2.0。开源Grok Bot替代方案，可选任意模型+沙箱执行。让用户不依赖xAI官方即可运行类Grok的自主Agent。 |
| [**FrontierAgent**](https://github.com/ApodexAI/FrontierAgent) | ⭐ **5.4k** | Python | Apodex AI | **「轻量 Agent 框架」** 🆕 **2026年8月22日开源**，Apache 2.0。原生命令行TUI，ReAct和Agent Team双模式，macOS/Linux一行命令启动，无需预装、无硬Docker依赖。定位为"零摩擦启动"的Agent框架。 |
| [**Agently**](https://github.com/AgentEra/Agently) | ⭐ **1.7k** | Python | AgentEra | 🆕 表达力优先的 Agent 开发框架，用接近自然语言的 DSL 描述 Agent 行为。 |
| [**Cooragent**](https://github.com/LeapLabTHU/cooragent) | ⭐ **1.7k** | Python | 清华 LeapLab | 🆕 Agent 协作社区：一句话生成协作团队，社区共享 Agent 组合。 |
| [**cindy**](https://github.com/makecindy/cindy) | ⭐ **10k** | TypeScript | makecindy | 🆕 开箱即用的开源 AI Agent，10-27 日榜单日 +1,446。 |
| [**oh-my-agent**](https://github.com/first-fluke/oh-my-agent) | ⭐ **1.4k** | TypeScript | first-fluke | 🆕 **厂商无关的 harness**：给已有编码 Agent（Claude Code / Codex CLI / Cursor）加规划、工程、评审、调试角色，只需一个可移植的 `.agents/` 目录。11-01 刚进 awesome 列表。 |
| [**OpenMausBot**](https://github.com/milind-soni/OpenMausBot) | ⭐ **21.8k** | TypeScript | milind-soni | 🆕 开源 Grok Bot 替代方案，自带虚拟机运行环境；11-01 日榜单日 +1,303。 |
| [**Tribe**](https://github.com/StreetLamb/tribe) | ⭐ **1.1k** | TypeScript | StreetLamb | 🆕 无代码多 Agent 团队编排工具。 |
| [**Orkas**](https://github.com/Orkas-AI/Orkas) | ⭐ **9.3k** | JavaScript | Orkas AI | 🆕 本地优先的桌面 AI 团队：Commander 协调 **16 个专家 Agent**，数据不出本机。 |
| [**Agentarium**](https://github.com/Thytu/Agentarium) | ⭐ **934** | Python | Thytu | 🆕 Agent 群体仿真框架，用于观察多 Agent 交互的涌现行为。 |
| [**IoA**](https://github.com/OpenBMB/IoA) | ⭐ **838** | Python | OpenBMB | 🆕 Internet of Agents：分布式异构 Agent 像互联网一样组队，解决跨组织协作。 |
| [**macos-harness**](https://github.com/browser-use/macos-harness) | ⭐ **1k** | Python | browser-use | **「LLM 操控 Mac」** 🆕 **2026年8月17日开源**，MIT许可。browser-use团队出品，"最简单、最薄的harness"让LLM完全自由操控Mac。与browser-use的浏览器自动化互补，覆盖了Agent操控桌面操作系统的最后一环。 |
| [**LazyCraft**](https://github.com/LazyAGI/LazyCraft) | ⭐ **677** | TypeScript | LazyAGI | 🆕 基于 LazyLLM 的 Agent 应用开发与管理平台，低门槛发布大模型应用。 |
| [**FastAgency**](https://github.com/ag2ai/fastagency) | ⭐ **548** | Python | AG2 | 🆕 把多 Agent 工作流最快送上生产（AutoGen 生态），专注「最后一公里」。 |
| [**Yunjue-Agent**](https://github.com/YunjueTech/Yunjue-Agent) | ⭐ **547** | Python | Yunjue Tech | 🆕 完全可复现、零起点、原位自演进的开放任务 Agent 系统。 |
| [**agent-safe-pipeline**](https://github.com/decionis/agent-safe-pipeline) | ⭐ **671** | TypeScript | Decionis | **「Agent 安全管线」** 🆕 **2026年8月13日开源**，Apache 2.0。**参考架构级**Agent安全方案：Agent提议动作但不可授权——不可变意图捕获、独立策略裁决（ALLOW/ESCALATE/BLOCK）、人工审批、单次意图绑定令牌的SafeExecutor。从架构层面保证Agent永远不可越权。（详见安全赛道） |
| [**rome**](https://github.com/rome-os/rome) | ⭐ **898** | TypeScript | rome-os | **「Agent 操作系统」** 🆕 **2026年8月23日开源**，MIT许可。"Rome is the agentic OS"——将Agent作为一等公民的操作系统概念验证。代表了Agent从"应用"走向"操作系统级抽象"的前沿探索。 |
| [**oc**](https://github.com/only-cli/oc) | ⭐ **690** | JavaScript | only-cli | **「网站转 CLI」** 🆕 **2026年8月18日开源**，MIT许可。将任意网站转化为AI Agent友好的精简CLI——用几百token浏览网页而非几万token。大幅降低Agent访问Web的Token成本，是headroom（上下文压缩）理念在Web领域的落地。 |
| [**whip**](https://github.com/context-labs/whip) | ⭐ **958** | Go | context-labs | **「Go 编码 Agent Harness」** 🆕 **2026年8月20日开源**，Apache 2.0。Go语言编写的快速编码Agent harness，工具循环+bubbletea TUI+模型路由+MCP支持+后台子Agent。单二进制、无运行时依赖，专为开源模型优化。 |
| [**teamai-cli**](https://www.toutiao.com/article/7683470774958555658/) | ⭐ **新项目** | Go | 腾讯 | **「企业级 Agent Harness CLI」** 🆕 **2026年9月9日开源**。腾讯把内部Agent工程能力以CLI形态开源，标志**Agent Harness 战火烧到大厂**——继DeepSeek DSH之后，国内大厂在harness层集体入场。 |

### 二、🧩 Agent Skills（🔥 2026 年 7 月爆发，10—11 月进入「记忆 + 审计」阶段）

> 2026 年 7 月，Agent Skills 生态爆发——三个 Skills 仓库单日合计涨星近 50 万。Skills 本质是**结构化的 Prompt 模板 + 工具调用配置 + 输出格式约束**的组合体，之于 Agent 就像 Dockerfile 之于容器。
>
> **10 月下旬的形态已经变了**：榜首从「提示词包」换成「专业工具链编排」（REA 26 万⭐），头部则被「方法论 + 多角色」占据（superpowers / mattpocock / ECC 三家都逼近 30 万）。同时出现了两条明确的分化：**一条往深走**——把某个专业领域（逆向、科研、安全审计、图表）的完整工具链封装成技能；**一条往分发走**——谁的注册中心被默认信任，谁就掌握入口（详见下方「分发之争」）。

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**Superpowers**](https://github.com/obra/superpowers) | ⭐ **317k** | Shell | Jesse Vincent (obra) | **Skills 赛道的总榜第一**。一套 Agent 驱动的软件开发方法论框架，遵循 Spec→Plan→Implement→Review→Ship 严格流程。23000+ Fork 说明大量团队基于它做二次定制，正在成为「企业内部 AI 开发流程标准」。10-02 日榜上「给编码智能体配技能和流程」的项目数量首次成为单期最多。 |
| [**Matt Pocock Skills**](https://github.com/mattpocock/skills) | ⭐ **323k** | TypeScript | Matt Pocock | 前 Vercel TypeScript 布道者开源的 21 个 Claude Code 技能。核心设计理念「小而可组合」——不走全流程接管，给你能自由搭配的积木块。明星技能：grill-me（Agent 反拷问需求）、tdd（红绿重构）、code-review（双轴并行评审）。 |
| [**ECC**](https://www.juejin.cn/post/7692703782765887488) | ⭐ **280k** | JavaScript | ECC 团队 | 面向多种编码 Agent 的**协调工程系统**——内置规划、审查、安全等 **68 个专用 Agent 角色**，把「一个 Agent 干活」升级为「一支训练有素的部队协作」。非模型类仓库星标最高者之一。 |
| [**Andrej Karpathy Skills**](https://github.com/multica-ai/andrej-karpathy-skills) | ⭐ **233k** | Shell | multica-ai | 基于 Karpathy 工程理念构建的 Agent 技能包，覆盖代码审查、架构设计、调试方法论等。星标增速惊人。 |
| [**Ponytail**](https://www.juejin.cn/post/7692703782765887488) | ⭐ **164k** | JavaScript | 社区 | **「让 AI 像懒开发者一样思考」**。核心机制是「最省力阶梯」——先读代码再决策、能不写就不写、能少写就少写，实测**减少 54% 代码产出**。直击 AI 编码「过度构建」痛点。 |
| [**G Stack**](https://github.com/garrytan/gstack) | ⭐ **141k** | Shell | Garry Tan | **Y Combinator 总裁 Garry Tan 的 Claude Code 配置包**。把创业公司角色拆成工具：CEO、设计师、工程经理、发布经理、文档工程师、QA。工作流：think→plan→build→review→test→ship→reflect。亮点 skill `/office-hours` 模拟 YC 合伙人拷问过程。 |
| [**caveman**](https://github.com/JuliusBrussee/caveman) | ⭐ **119k** | Go | JuliusBrussee | 「穴居人说话，省 Token」。让 Agent 用极度简练的「穴居人」式英语输出，**Token 消耗最高削减 65%**。核心实现已用 Go 重写；README 定位已从「提示词技能」改为「技能 + 代理层」。 |
| [**Agent Skills**](https://github.com/addyosmani/agent-skills) | ⭐ **117k** | JavaScript | Addy Osmani | Google Chrome 工程经理出品的生产级技能包，24 个技能 + 8 条 Slash 命令，覆盖 DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP 六阶段。三支柱：安全（OWASP Top 10）、性能（Lighthouse/Core Web Vitals）、无障碍（WCAG 2.2 AA）。 |
| [**impeccable**](https://www.juejin.cn/post/7692703782765887488) | ⭐ **98.2k** | JavaScript | 社区 | 「AI 设计语言」Skill——专治前端模板化问题，约束 AI 生成原创性更强的界面（配色、排版、动效去套路化）。与 hallmark 同属「反 AI 味设计」方向，但体量大了两个数量级。 |
| [**archify**](https://blog.csdn.net/u130130/article/details/166899588) | ⭐ **74.3k** | JavaScript | 未确认 | AI Agent 图表技能——让 Agent 生成可交互的 HTML 架构图/流程图/系统图，把「画架构图」这一高频需求封装成即插即用 Skill。10 月遭遇 diagram-design 正面竞争。 |
| [**diagram-design**](https://github.com/cathrynlavery/diagram-design) | ⭐ **66.8k** | Shell | cathrynlavery | 🆕 **10 月上旬新晋细分冠军**：44 种图表类型，输出自包含 HTML + SVG，设计原则写得很硬——「不要阴影、不要 Mermaid 味」。直接对标 archify，主打「能直接放进文档和 PPT 的图」。 |
| [**cloudflare/security-audit-skill**](https://github.com/cloudflare/security-audit-skill) | ⭐ **71.3k** | Shell | Cloudflare | 🆕 recon→hunt→verify→report 多阶段审计技能，设计规则很关键：**「发现的 Agent 不能是验证的 Agent」**——用角色隔离对抗自评偏差。云厂商第一次亲自下场写安全 Skill。 |
| [**i-have-adhd**](https://blog.csdn.net/u130130/article/details/166899588) | ⭐ **52.2k** | Python | 未确认 | ADHD 友好输出风格 Skill——强制编码助手以「要点先行、可执行步骤、无冗长铺垫」的方式输出。垂直人群 Skills 的典型代表，5 周冲上 5 万星。 |
| [**scientific-agent-skills**](https://github.com/K-Dense-AI/scientific-agent-skills) | ⭐ **57k** | Python | K-Dense AI | 🆕 **177 个科研技能 + 100+ 科学数据库连接**，每个 skill 自带 SKILL.md 与「验证范围」声明。把「科研工作流」整体技能化：检索、复现、统计、绘图、审稿。 |
| [**hallmark**](https://github.com/Nutlope/hallmark) | ⭐ **54.1k** | Shell | Nutlope | 「终结 AI 生成代码的 AI 味」。提供反 AI 味设计规范的 Skill，定义严谨的设计 Token（颜色、间距、排版、圆角、阴影），让 AI 生成的前端代码看起来像专业设计师出手。 |
| [**anatomy**](https://github.com/wheresryan22/anatomy) | ⭐ **27k** | JavaScript | wheresryan22 | 🆕 **10-15 日榜第一**。基于 Claude 代理的技能，用 JavaScript 生成**交互式等距 SVG / WebGL / 3D 插图**，把技术概念画成可旋转的「实体模型」。适用于技术文档、教学与演示——是「图表类 Skills」里最偏 3D 的一支。 |
| [**ip-as-logo-skill**](https://github.com/s1dashu/ip-as-logo-skill) | ⭐ **6.5k** | Shell | s1dashu | 生成高度简化、圆润、微妙新拟物风格的 IP 形象 Logo。Skills 赛道中「垂直设计」方向的标杆——将设计师审美固化为 Agent 可执行的配置。 |
| [**unslop**](https://github.com/heydamir/unslop) | ⭐ **15.2k** | JavaScript | heydamir | 🆕 专治「AI 味 UI」：识别并修复紫渐变、光晕、表情标签等 slop 特征，支持主流前端框架。与 impeccable / hallmark 组成「反 AI 味三件套」。 |
| [**mono-color-skill**](https://github.com/yanliudesign/mono-color-skill) | ⭐ **3.6k** | Python | yanliudesign | 单色编辑级印刷图像 Skill——暖纸感、半调摄影、负空间、克制排版。将专业平面设计经验封装为 Agent 可执行的 Skill。 |
| [**sepia**](https://github.com/Nanako0129/sepia) | ⭐ **3.8k** | Python | Nanako0129 | **去 AI 味写作 Skill**——适配 77+ Agent Skills 兼容客户端（Claude Code / Codex / Grok Build 原生插件）。基于 StoryScope 学术研究，对叙事结构做架构级修复，让 AI 生成的文字读起来像人写的。 |
| [**scroll-craft**](https://github.com/nateherkai/scroll-craft) | ⭐ **5k** | JavaScript | nateherkai | 构建高端沉浸式滚动驱动网站的 Agent Skill，适配 Codex / Claude Code 等编码 Agent。把「动效设计」经验固化为可复用 Skill。 |
| [**Claude-Code-Game-Studios**](https://github.com/Donchitos/Claude-Code-Game-Studios) | ⭐ **38.8k** | Shell | Donchitos | 🆕 把 Claude Code 变成游戏工作室：**49 个 Agent + 72 个工作流技能**。「技能包组织化」的极端样本。 |
| [**anthropics/skills**](https://github.com/anthropics/skills) | ⭐ **194k** | Python | Anthropic | 🆕 **Anthropic 官方 Agent Skills 仓库**——厂商亲自定义「技能该长什么样」，与社区注册中心（skills.sh / dshub）形成标准之争。 |
| [**expo/skills**](https://github.com/expo/skills) | ⭐ **4.1k** | Shell | Expo | 🆕 面向 Expo 项目的官方 Agent 技能集。**框架方开始自己发技能**，技能从社区自发转向生态标配。 |

> 📦 **分发之争（10 月新增观察）**：同一周冒出三个「官方插件仓库」——[**cursor/plugins**](https://github.com/cursor/plugins) 1.15 万⭐（Cursor 把插件规范与官方插件公开，周增 +1,140）、[**anthropics/knowledge-work-plugins**](https://github.com/anthropics/knowledge-work-plugins) 2.97 万⭐（面向销售/支持/产品/法务/金融/生物研究等角色的插件，10 月 9—11 日连续三天日榜）、**claude-plugins-official 3.84 万 / claude-plugins-community 4,652**。
>
> DSH 侧第三方索引 **dshub.cc** 已收录 **368** 个生态条目（其中 **76 个是独立 Skill 包**），官方市场仍在「施工中」，社区用 **dsh-market（6,417⭐）** 补位。**skills.sh** 仍是事实注册中心（vercel-labs/skills 3.45 万⭐，10 月 13 日榜首 find-skills 装机 **380 万**）。
>
> **结论：技能写得好不好，已经不如「装得上、验得了」重要。签名验证与来源信任，是 Skills 下半场的主战场。**

### 三、🦞 个人 AI 助手（新兴超级赛道）

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**OpenClaw**](https://github.com/openclaw/openclaw) | ⭐ **394k** | TypeScript | OpenClaw | 全平台个人AI助手，GitHub有史以来Star数最高的AI项目之一。支持桌面、移动和Web端，内置插件生态、多模型切换和本地知识库。🆕 **2026年9月30日发布 OpenClaw 2.0——号称"龙虾史上最大更新"**，重构底层调度系统；实测内存峰值4GB、冷启动8.2秒，社区围绕其与Hermes的"1.5GB/1.1秒"轻量表现展开激烈路线之争（"爱过，我选Hermes"梗刷屏）。 |
| [**Hermes Agent**](https://github.com/NousResearch/hermes-agent) | ⭐ **263k** | Python | Nous Research | 与你共同成长的AI伙伴，三层记忆架构实现个性化进化。不仅能完成任务，还能学习和适应用户习惯。 |
| [**OpenCode**](https://github.com/anomalyco/opencode) | ⭐ **226k** | TypeScript | anomalyco | 开源终端编程Agent，**9月初已突破20.4万星**。支持多模型、代码理解和自动修复，是终端重度用户的高效编程伙伴，7.5M月活开发者。 |
| [**Open Interpreter**](https://github.com/OpenInterpreter/open-interpreter) | ⭐ **68.9k** | Python | 社区 | 让LLM直接操控你的电脑——用自然语言执行代码、管理文件、控制系统设置。AGPL-3.0许可，2026年仍为唯一将本地执行做得既轻量又扎实的开源实现。 |
| [**Cherry Studio**](https://github.com/CherryHQ/cherry-studio) | ⭐ **53.5k** | TypeScript | CherryHQ | 🆕 全能AI桌面客户端，支持多LLM提供商（OpenAI/Gemini/Anthropic/Ollama等）。**300+预配置AI助手**、MCP Server支持、多模型同时对话、跨平台（Win/Mac/Linux）。AGPL-3.0许可，**v2.0.0-beta.1（7月24日）**，7700+次提交，社区极活跃。企业版支持私有化部署与统一知识库管理。 |
| [**CowAgent**](https://github.com/zhayujie/CowAgent) | ⭐ **47.9k** | Python | zhayujie | 国产超级AI助手，深度集成微信/企微/飞书等国内主流平台。 |
| [**AstrBot**](https://github.com/AstrBotDevs/AstrBot) | ⭐ **46.8k** | Python | AstrBotDevs | 🆕 松耦合、异步的多平台LLM聊天机器人及开发框架。支持QQ/微信/企微/飞书/钉钉/Telegram/Discord/Slack等平台接入。MCP服务器支持，多模型（OpenAI/DeepSeek/Gemini/Ollama等），**近800个插件**，WebUI管理。定位为OpenClaw替代方案，8月初已增长至3.8万星。 |
| [**OpenHuman**](https://github.com/tinyhumans-ai/openhuman) | ⭐ **36k** | TypeScript | TinyHumans AI | 🆕 **8月初已增长至36k**（6月仅21k）。主打"本地优先"的桌面AI助手。所有数据在本地处理，Rust实现，强调隐私和个性化，核心理念是"你的AI应该住在你家里"。 |
| [**DSH Desktop**](https://github.com/anywhere-labs/dsh-desktop) | ⭐ **35.9k** | TypeScript | anywhere-labs | 🆕 **2026年8月13日开源**。为DeepSeek Harness（DSH）插件生态打造的现代化桌面端解决方案，"万物皆插件，桌面本身也是插件"。是DSH生态中Star数最高的周边项目，与DSH本体合计超23万⭐。 |
| [**OpenWorker**](https://github.com/andrewyng/openworker) | ⭐ **19k** | TypeScript | Andrew Ng | 🆕 **吴恩达2026年7月24日开源**的桌面AI智能体。MIT许可，本地优先，不绑定模型（支持GPT-5.6/Claude Fable/Gemini 3.6及Kimi/GLM/DeepSeek等开源模型+Ollama本地）。在文件和日常工具中运行，执行任何重要操作前进行检查，从"聊天"转向"交付成果"。 |
| [**Octop**](https://github.com/TencentCloud/Octop) | ⭐ **12k** | Python | 腾讯云 | 🆕 **腾讯云2026年7月正式开源**的自托管AI助手。多用户、多Agent架构，单进程启动集成Web控制台+CLI+IM（飞书/钉钉/QQ/Discord/企微）。内置专家团库+16种MBTI人格模板，JWT安全隔离，ACP双向集成（OpenCode/Claude Code/Codex）。SQLite存储，所有数据在 `~/.octop/`，MIT许可。 |
| [**codex-with-chatgpt**](https://github.com/XiaoDuoYa/codex-with-chatgpt) | ⭐ **7.7k** | TypeScript | XiaoDuoYa | 🆕 **2026年8月28日开源**，MIT许可。"ChatGPT thinks. Codex works."——用ChatGPT作为规划大脑，同时保留Codex harness执行层。巧妙拆分"思考"与"执行"，让强推理模型负责规划、强编码模型负责落地。 |

### 四、🚀 AI 编程 / 开发工具

| 工具 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**Codex CLI**](https://github.com/openai/codex) | ⭐ **135k** | Rust | OpenAI | OpenAI官方终端编程Agent，Rust编写。**9月初已突破12.1万星**，rust-v0.145.0，4周内697次提交。支持沙盒和自主双模式，原生GitHub集成，npm月下载约1400万。 |
| [**browser-use**](https://github.com/browser-use/browser-use) | ⭐ **121k** | Python | 社区 | 让AI Agent像人一样操控浏览器。**9月初已突破11.2万星**，v0.13.6（7月17日发布），持续活跃迭代，解决了Agent与Web交互的核心痛点。 |
| [**Gemini CLI**](https://github.com/google-gemini/gemini-cli) | ⭐ **109k** | TypeScript | Google | Google出品的终端AI编程Agent，拥有100万token超大上下文窗口且免费使用（1000次/天）。**9月初增长至107k**，v0.52.0，688贡献者。 |
| [**OpenHands**](https://github.com/All-Hands-AI/OpenHands) | ⭐ **93.4k** | Python | All-Hands-AI | 原名OpenDevin，AI软件开发Agent。**8月初已增长至85k+**，cloud-1.47.1版本，能自主编写代码、运行测试、修复Bug，是Devin类产品的最佳开源替代。 |
| [**gpt\_academic**](https://github.com/binary-husky/gpt_academic) | ⭐ **71.7k** | Python | Binary-Husky | 面向学术的AI工具，支持论文阅读、翻译、润色、LaTeX排版和代码分析。 |
| [**Cline**](https://github.com/cline/cline) | ⭐ **71.6k** | TypeScript | cline | VS Code中最受欢迎的自主编程Agent插件。**9月初增长至67.5k**，v4.0.11，800万+活跃开发者。现以SDK、IDE扩展、CLI三种形态提供，核心是Plan/Act双阶段工作流+Kanban任务看板。 |
| [**GPT-Engineer**](https://github.com/AntonOsika/gpt-engineer) | ⭐ **55k** | Python | AntonOsika | 用自然语言描述需求，自动生成完整应用程序。 |
| [**Aider**](https://github.com/Aider-AI/aider) | ⭐ **50.1k** | Python | Aider-AI | 终端AI结对编程工具，与Git深度集成。**9月初增长至49k**，410万+安装，每次改动自动提交。 |
| [**open-code-review**](https://blog.csdn.net/u130130/article/details/166899588) | ⭐ **47.3k** | Go | 阿里 | 🆕 AI 代码评审 CLI |
| [**CLI-Anything**](https://github.com/HKUDS/CLI-Anything) | ⭐ **58.7k** | Python | HKUDS | 🆕 把任意 GUI 软件（GIMP / Blender / LibreOffice）用**一条命令 + 一套 7 阶段流水线**转成 Agent-Native 命令行——无需 API、无需截图点击，Claude Code / Cursor / Codex 可直接操控。10-19 仍在日榜（607⭐/日 +）。**它代表的方向很关键：与其让 Agent 学会看屏幕，不如让软件学会被调用。** |
| [**CopilotKit**](https://github.com/CopilotKit/CopilotKit) | ⭐ **38.7k** | TypeScript | CopilotKit | 为React/Next.js应用添加AI Copilot能力的前端框架。发起AG-UI协议标准。 |
| [**Continue**](https://github.com/continuedev/continue) | ⭐ **36.5k** | TypeScript | continuedev | 开源AI编程IDE插件。**8月初增长至36k**，v2.0.0-vscode。2026 Agent Mode支持多步自主任务，PR审查自动化规则以Markdown存于版本库，CI可强制执行。 |
| [**t3code**](https://github.com/pingdotgg/t3code) | ⭐ **58.5k** | TypeScript | pingdotgg | 🆕 AI 编程智能体**控制面板**：统一管理本机 Claude Code / Codex / Cursor 等多种 Agent，支持移动 / Web / 桌面远程操控。**并行 Agent 的「驾驶舱」**——当一个人同时开 6 个 Agent 时，谁来调度、谁来收结果。 |
| [**Tabby**](https://github.com/TabbyML/tabby) | ⭐ **33.9k** | Rust | TabbyML | Rust编写的自托管AI编码助手，数据完全私有化部署。 |
| [**GPT-Pilot**](https://github.com/Pythagora-io/gpt-pilot) | ⭐ **33.6k** | Python | Pythagora | AI开发搭档，模拟完整的软件开发流程。 |
| [**Kilo Code**](https://github.com/Kilo-Org/kilocode) | ⭐ **28k** | TypeScript | Kilo-Org | 🆕 Cline社区分支中增长最快的项目。4周内1355次提交、1166贡献者，是编码Agent生态中社区最活跃的项目之一。热度评分66.0，仅次于Codex CLI和Gemini CLI。 |
| [**Roo Code**](https://github.com/RooVetGit/Roo-Code) | ⭐ **24.2k** | TypeScript | RooCode Inc. | Cline的最活跃社区分支，在原版基础上增加了自定义模式、MCP增强和UI优化。 |
| [**SWE-agent**](https://github.com/SWE-agent/SWE-agent) | ⭐ **20.8k** | Python | Princeton NLP | 普林斯顿出品，自动定位和修复代码Bug并提交PR。**8月初增长至20.5k**，在SWE-bench评测中表现优异。 |
| [**Bolt.diy**](https://github.com/stackblitz-labs/bolt.diy) | ⭐ **20.1k** | TypeScript | StackBlitz Labs | Bolt.new的开源版本，AI全栈Web开发平台。 |
| [**Devika**](https://github.com/stitionai/devika) | ⭐ **19.5k** | Python | stitionai | Cognition AI旗下Devin的开源替代品，自主AI软件工程师。 |
| [**avante.nvim**](https://github.com/yetone/avante.nvim) | ⭐ **18.2k** | Lua | yetone | 🆕 Neovim用户的AI编码Agent插件，将Claude Code式体验带入Neovim生态，支持多模型和工具调用。 |
| [**text-to-cad**](https://segmentfault.com/a/1190000048333142) | ⭐ **17.4k** | Python | 社区 | 🆕 自然语言生成 CAD |
| [**Plandex**](https://github.com/plandex-ai/plandex) | ⭐ **15.9k** | Go | Plandex AI | 🆕 终端AI编码Agent，Go语言编写。支持复杂项目的增量规划和执行，适合大型代码库的渐进式开发。 |
| [**e2e**](https://github.com/tester-army/e2e) | ⭐ **13.8k** | TypeScript | tester-army | 🆕 Agent 驱动端到端测试 |
| [**walgit**](https://github.com/tobi/walgit) | ⭐ **2.7k** | Rust | tobi | 🆕 **2026年8月23日开源**，MIT许可。Rust编写的Git仓库管理工具，为AI编码Agent的并行工作流设计——支持Worktree隔离、多Agent并行提交管理和跨分支结果合并。 |
| [**git-ai / open_scion**](https://github.com/feder-cr/git-ai) | ⭐ **1k** | Go | feder-cr | 🆕 **10-19 日榜第一，断层领先**。用 Go 实现的开源 Scion 版本控制系统，**专为大量短生命周期编码代理设计**：服务端 API、即时落地（instant landing）、冲突自动解决。当 10 个 Agent 并行改同一仓库时，「谁先落地、怎么合」成了新问题——这是它给出的答案。 |
| [**esp32-iphone-agent**](https://github.com/onehumanbeing/esp32-iphone-agent) | ⭐ **4.9k** | Python | onehumanbeing | 🆕 用约 **7 美元**的 ESP32-S3 板卡，通过 AirPlay 镜像取屏 + USB HID 模拟鼠标键盘，让 AI 直接操作真实 iPhone。**无需 Mac、开发者账号或越狱**，可跑任何 iOS 应用（绘图、设闹钟等）。Agent 硬件化最便宜的一次尝试。 |
| [**goldie**](https://github.com/kacperkapusciak/goldie) | ⭐ **2.6k** | TypeScript | kacperkapusciak | 🆕 **2026年8月24日开源**。Agent化App Store预览和截图工具，自动生成应用商店质量的产品截图。让AI编码Agent的交付物从"代码"延伸到"上架素材"。 |
| [**open-claude-ui**](https://github.com/Caho1/open-claude-ui) | ⭐ **1.8k** | TypeScript | Caho1 | 🆕 用 **REA 逆向分析**完整还原 Claude 官方桌面端 UI：30 个高保真 React 组件 + 8 个交互物理算法 + 3000 行逆向手册。**「逆向」从二进制安全圈外溢到产品设计圈的标志性项目。** |
| [**lightpanda browser**](https://github.com/lightpanda-io/browser) | ⭐ **42k** | Zig | lightpanda | 🆕 为 AI 与自动化设计的**无头浏览器**，Zig 编写，主打低内存与快启动，替代 Puppeteer / Playwright 的重型方案。 |
| [**earshot**](https://github.com/Leonxlnx/earshot) | ⭐ **4.7k** | Python | Leonxlnx | 🆕 让编码 Agent 获得「听觉」：音频描述、匹配、查找、对比、鉴真、音画同步分析，以及用代码合成声音。补齐 Agent 在音频维度上的感知缺口。 |
| [**blender-ai-mcp-addon**](https://github.com/LiCinCan/blender-ai-mcp-addon) | ⭐ **785** | Python | LiCinCan | 🆕 把 MCP 服务器直接塞进 Blender：视觉聊天工作区 + 场景工具，多模型、多 Agent 自动化 3D 场景操作。**MCP 从「开发工具」渗透进「创意软件」。** |
| [**eleven**](https://github.com/Zfinix/eleven) | ⭐ **991** | TypeScript | Zfinix | 🆕 跨平台（macOS / Windows / Linux）逆向工程应用，**围绕「可插拔 Agent 客户端协议」构建**，支持二进制、APK、GPU 内核等文件类型的交互式分析。逆向工具开始按「Agent 优先」重新设计，而不是给 Agent 套壳。 |
| [**thinkrail**](https://github.com/JetBrains/thinkrail) | ⭐ **8.2k** | TypeScript | JetBrains | 🆕 JetBrains 出品的轻量 IDE 式 vibe coding 工具，在真实 IDE 里以对话方式改代码。**IDE 厂商开始自己做 Agent 客户端。** |
| [**agenttrail**](https://github.com/sodiumsun/agenttrail) | ⭐ **1k** | HTML | sodiumsun | 🆕 **2026年8月21日开源**，MIT许可。AI编码Agent的无限画布——每个仓库是可缩放实时地图上的一个区域，可视化Claude Code/Codex/Cursor的会话、计划、工具调用和文件变更。本地运行、零依赖。 |
| [**indra**](https://github.com/datalab-to/indra) | ⭐ **1.8k** | Python | datalab-to | 🆕 约 **1M 参数**的轻量 OCR 模型，专为 CPU 高速运行设计：**49 页/秒**把 PDF/图片转成 markdown、纯文本或带坐标 JSON。在「大模型做 OCR」的潮流里反向做小。 |
| [**ruflo**](https://github.com/ruvnet/ruflo) | ⭐ **81.6k** | TypeScript | ruvnet | 🆕 「原始 Agent Harness」——多智能体集群、自适应记忆与联邦协作。在 harness 层继续往「分布式」方向推。 |

### 五、📚 RAG & 知识库（含 Agent 记忆层，2026 年 10 月最拥挤赛道）

> **10 月 16 日是一个分界点**：在腾讯混元把「记忆专用模型 + 框架 + 桌面应用」三层一起开源之前，记忆项目的主流形态还是「插件」；之后，它变成了**有模型、有论文、有 benchmark 的独立基础设施层**。
>
> 现在这条赛道清晰地分成四层，选型时先分清自己在哪一层：
>
> | 层 | 解决什么 | 代表项目 | 选型建议 | 典型场景 |
> | :--- | :--- | :--- | :--- | :--- |
> | **企业知识平台** | 公司文档怎么变成可问答、可维护的知识 | WeKnora / RAGFlow / Danswer / FastGPT / MaxKB | 先看文档解析质量，再看知识治理能力 | 内部 Wiki、客服知识库 |
> | **Agent 上下文数据库** | 记忆 + RAG + 技能的统一抽象 | OpenViking / Mem0 / cognee / Hy-Memory 2.0 | 要长期跑多项目就选这层 | 长周期 Agent、多项目隔离 |
> | **会话记忆工具** | 编码助手跨会话「记得住」 | claude-mem / ai-memory / codebase-memory-mcp / OptMem | 按客户端生态选，注意记忆可携带性 | Claude Code / Codex 日常开发 |
> | **上下文压缩层** | Token 太贵，进来之前先压 | headroom / context-mode | 先量 token 账单，再决定「压」还是「隔离」 | 大日志、长工具输出 |

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**claude-mem**](https://github.com/thedotmack/claude-mem) | ⭐ **117k** | TypeScript | thedotmack | 专注 Claude Code 等编码助手的**跨会话持久记忆**与上下文压缩管理，用 AI 压缩技术处理长对话并在下次会话自动注入相关上下文。**10 月 9 日破 10 万**（10-07 为 9.72 万，10-12—13 连发 v13.36.1→v13.39.0），是 Claude Code 生态中增长最快的记忆方案，已迁移至 TypeScript 实现。 |
| [**RAGFlow**](https://github.com/infiniflow/ragflow) | ⭐ **94.1k** | Python | InfiniFlow | 深度文档解析 RAG 引擎，支持 PDF/Word/PPT 等复杂格式的精准解析。内置 OCR、版面分析和表格识别，文档理解能力最强的开源 RAG 方案，企业级知识库首选。 |
| [**headroom**](https://github.com/headroomlabs-ai/headroom) | ⭐ **79.5k** | Python | headroomlabs-ai | **AI Agent 上下文压缩层**，Token 消耗降低 60—95% 且答案不变。压缩工具输出、日志、文件和 RAG 分块后再送入 LLM；提供库、代理和 MCP 服务器三种形态，CCR（内容压缩检索）机制实现无损还原，对 Agent 完全透明。实测 SRE 调试场景从 65,694 token 压到 5,118（省 92%）。Apache 2.0，7 月 GitHub Trending #1。10-19 仍在日榜（317⭐/日 +）。 |
| [**Mem0**](https://github.com/mem0ai/mem0) | ⭐ **68.9k** | Python | Mem0 | AI Agent 通用记忆层，为 Agent 提供持久化的长期记忆能力，自动提取、存储和检索用户偏好与对话历史。⚠️ **1.0.0 服务器存在 CVE-2026-31241**（10 月 8 日披露，任意 `user_id/agent_id` 可未鉴权删除记忆记录），生产环境需先升级。 |
| [**AnythingLLM**](https://github.com/Mintplex-Labs/anything-llm) | ⭐ **68.2k** | JavaScript | Mintplex Labs | 最易用的本地 RAG 桌面应用，一键部署无需技术背景。 |
| [**PrivateGPT**](https://github.com/zylon-ai/private-gpt) | ⭐ **57.6k** | Python | zylon-ai | 100% 离线运行的 RAG 方案，所有数据和推理完全在本地处理。 |
| [**LlamaIndex**](https://github.com/run-llama/llama_index) | ⭐ **52.9k** | Python | LlamaIndex | 文档 Agent + 数据框架。**Workflows 1.0（6 月 22 日）**：轻量、事件驱动、async-first、step-based。LlamaCloud 更名为 LlamaParse，转向 agentic 文档处理。Salesforce、KPMG、Deutsche Telekom 等企业采用。 |
| [**hindsight**](https://github.com/vectorize-io/hindsight) | ⭐ **60.7k** | Python | vectorize-io | 🆕 **10 月 13 日发布 v1.0.0**，「会学习的 Agent 记忆」——记忆不只是存取，还带反馈与衰减。是 10 月第一批「有版本线」的记忆项目。 |
| [**codebase-memory-mcp**](https://github.com/DeusData/codebase-memory-mcp) | ⭐ **48.6k** | C | DeusData | 把代码库索引为持久化知识图谱，纯 C 编写，158 种语言 AST 解析，子毫秒级查询。完整 Linux 内核（2800 万行）3 分钟索引，官方宣称 Token 消耗减少 99%，并带 3D 可视化。 |
| [**OpenViking**](https://github.com/volcengine/OpenViking) | ⭐ **42.1k** | Python/Rust | 火山引擎 | **火山引擎开源的「AI Agent 上下文数据库」**（2026 年 1 月发布）。用虚拟文件系统统一管理**记忆、资源（RAG）与技能**，支持 **L0/L1/L2 分层检索**——Agent 上下文从「散件拼装」走向「数据库级抽象」，可自进化。 |
| [**Quivr**](https://github.com/Quivr-App/quivr) | ⭐ **39.4k** | Python | Quivr | 「开源第二大脑」，个人知识管理利器。 |
| [**LightRAG**](https://github.com/HKUDS/LightRAG) | ⭐ **40.7k** | Python | HKUDS | 港大出品，轻量高速的 RAG 框架。 |
| [**GraphRAG**](https://github.com/microsoft/graphrag) | ⭐ **36.6k** | Python | Microsoft | 微软出品，知识图谱增强 RAG。 |
| [**PageIndex**](https://github.com/VectifyAI/PageIndex) | ⭐ **40.4k** | Python | VectifyAI | 无向量推理 RAG，摒弃传统向量检索范式。 |
| [**WeKnora**](https://github.com/Tencent/WeKnora) | ⭐ **37.3k** | Go | Tencent | **腾讯开源的企业级 LLM 知识框架**，9 月中旬开源后不到一个月冲上 3 万星。定位「**RAG + Agent + Wiki 三合一**」：支持 GraphRAG，能自动把零散文档整理成**可自我进化的「活知识库 / Wiki」**，MIT 许可。 |
| [**Danswer**](https://github.com/danswer-ai/danswer) | ⭐ **33.4k** | Python | danswer-ai | 企业级 AI 搜索平台，连接 Slack / Google Drive / Confluence 等企业数据源。 |
| [**cognee**](https://github.com/topoteretes/cognee) | ⭐ **33.3k** | Python | topoteretes | 基于知识图谱的 Agent 持久化记忆引擎，替代传统 RAG 方案。通过图结构存储和检索知识，支持复杂的关联推理。 |
| [**context-mode**](https://github.com/mksglu/context-mode) | ⭐ **34k** | TypeScript | mksglu | 🆕 **10 月新晋**：把工具输出「沙箱化」后再交给模型，宣称上下文体积 **−98%**。与 headroom 的区别是它更偏「隔离与重放」，而非纯压缩。 |
| [**FastGPT**](https://github.com/labring/FastGPT) | ⭐ **30k** | TypeScript | Sealos | 知识库 + Agent 工作流平台，提供可视化工作流编辑器。 |
| [**TencentDB-Agent-Memory**](https://github.com/TencentCloud/TencentDB-Agent-Memory) | ⭐ **30.8k** | Python | TencentCloud | 🆕 **10 月 9 日 v2.0.2**。把 **Chat 记忆 / Skill / LLM-Wiki / Code-Graph** 当作四类「受治理资产」统一管理——记忆第一次被当成需要权限、版本与生命周期的东西。与混元 Hy-Memory 2.0 形成腾讯内部「双记忆」路线（一个偏基础设施、一个偏模型）。 |
| [**kotaemon**](https://github.com/Cinnamon/kotaemon) | ⭐ **25.9k** | Python | Cinnamon | RAG 文档 QA 工具，专注技术文档问答场景。 |
| [**MaxKB**](https://github.com/1Panel-dev/MaxKB) | ⭐ **23.2k** | Python | 1Panel-dev | 1Panel 团队出品的企业知识库问答系统。⚠️ **沙箱绕过 CVE-2026-77521**（10 月 4 日披露，攻击链经由被爬取网页的间接 Prompt Injection）。 |
| [**DocsGPT**](https://github.com/arc53/DocsGPT) | ⭐ **18.4k** | Python | arc53 | 技术文档问答专精工具。 |
| [**QAnything**](https://github.com/netease-youdao/QAnything) | ⭐ **14.2k** | Python | netease-youdao | 网易有道出品的本地知识库系统。 |
| [**production-agentic-rag-course**](https://segmentfault.com/a/1190000048333142) | ⭐ **9.6k** | Python | — | 生产级 Agentic RAG 开源课程——从检索管线、评估到 Agent 化的 RAG 编排全流程实战，一个月内近万星，反映市场对「RAG 生产落地」技能的饥渴。 |
| [**KAG**](https://github.com/OpenSPG/KAG) | ⭐ **9.2k** | Python | OpenSPG | 阿里 OpenSPG 出品的知识图谱增强 RAG 框架。 |
| [**OptMem**](https://segmentfault.com/a/1190000048333142) | ⭐ **1.9k** | Python | — | 轻量 AI Agent 永久记忆工具——本地存储、跨会话注入，主打「小而正确」，是个人开发者给 Agent 补记忆的最小可行方案。 |
| [**Hy-Memory 2.0**](https://github.com/Tencent-Hunyuan/Hy-Memory) | ⭐ **2k** | Python | Tencent-Hunyuan | 🆕 **本轮最重要新项目，10 月 16 日发布**。腾讯混元把记忆拆成三层同时开源：**模型层 Hy-Memory-30B-A3B**（30B 总参 / 3B 激活的记忆写入模型，4 个 benchmark 上开源框架第一，平均分超过 Opus 5）、**框架层 `hy-memory` SDK**（PyPI，快慢双系统 + 分层记忆 + 向量检索 + 知识图谱）、**应用层 MemHub**（桌面端，让 10 种 AI 工具共享一份个人记忆）。覆盖**聊天 / 工作 / 代码**三类记忆，是业界首个把「工作记忆」单独建模的方案；论文被 EMNLP 2026 接收。 |
| [**ai-memory**](https://github.com/akitaonrails/ai-memory) | ⭐ **15.8k** | Rust | akitaonrails | 🆕 **10-19 日榜第 5**。为编码 Agent CLI 提供长期记忆与**跨厂商交接**能力——换一个 Agent 客户端，记忆还能带走。Rust 实现，主打「记忆不该被厂商锁定」。 |
| [**PilotDeck 2.0**](https://github.com/OpenBMB/PilotDeck) | ⭐ **5k** | Python | OpenBMB | 🆕 **10 月 17 日开源**（清华 THUNLP × 面壁智能 × OpenBMB，AGPL-3.0）。以 **WorkSpace 工作舱**为单位隔离文件/记忆/任务；**白盒记忆**可查可改可回滚，空闲时 **Dream 模式**自动归纳去重，**Always-on** 支持关窗后继续跑；内置 **Smart Routing** 让强模型规划、小模型执行。Workbuddy Bench 上 Qwen3.6-35B-A3B 得 79.1（高于 Claude Code 77.3），7 个高难任务横评成本仅顶配单体的 **1/6**。 |

> 🎯 **选型口诀（10 月版）**
>
> - 管**公司文档** → WeKnora / RAGFlow（要「知识自己长成体系」选 WeKnora，要「复杂 PDF 解析准」选 RAGFlow）
> - 给 Agent 装**大脑外存** → OpenViking（要数据库级抽象）/ Mem0（要通用轻量）/ cognee（要图推理）/ **Hy-Memory 2.0**（要专用模型 + 可治理 + 桌面共享）
> - 给**编码助手**补记忆 → claude-mem（Claude Code 生态最顺）/ **ai-memory**（要跨厂商可携带）/ codebase-memory-mcp（要代码图谱）
> - **Token 太贵** → headroom（无损压缩）/ context-mode（沙箱隔离 + 重放）
> - **成本敏感的长任务** → PilotDeck 2.0（主强子弱路由，省 70—83%）

### 六、⚡ 推理 & 部署（本地推理 + 网关 + 国产算力）

> 10 月下旬这条赛道的主线不是「更快」，而是**「更便宜地跑 Agent」**。三组数字值得记住：Gartner 预测到 2028 年 **Agent 成本将涨 5 倍**（即便 token 在降价）；GPU 推理有高达 **60% 算力用于重算已处理过的上下文**；Arcade.dev 的工具推荐把企业输入 token 成本降了 **37%**。所以今年的关键词是：**前缀缓存、上下文压缩、分层路由、KV 下沉**。

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**Ollama**](https://github.com/ollama/ollama) | ⭐ **187k** | Go | Ollama | 「AI 界的 Docker」。v0.19+ 在 Apple Silicon 上原生使用 MLX 后端；10 月 8—14 日连发 v0.40.2→v0.40.5-rc0。新增云端 Pro（$20/月）/ Max（$100/月）层级，100+ 模型库。 |
| [**llama.cpp**](https://github.com/ggerganov/llama.cpp) | ⭐ **135k** | C++ | ggml | 让 CPU 也能高效推理 LLM 的传奇项目。2026 年 3 月破 10 万星，GGUF 格式成为事实标准。 |
| [**vLLM**](https://github.com/vllm-project/vllm) | ⭐ **96.8k** | Python | vLLM | 高吞吐 LLM 推理引擎。PagedAttention + 连续批处理，约每 6.8 天发一个版本，生产环境部署的事实标准。 |
| [**GPT4All**](https://github.com/nomic-ai/gpt4all) | ⭐ **77.4k** | Python | nomic-ai | CPU 优先的桌面 LLM 应用，无需 GPU 即可在普通笔记本上运行大模型。 |
| [**OmniRoute**](https://github.com/diegosouzapw/OmniRoute) | ⭐ **86.9k** | Python | diegosouzapw | 免费 MIT 协议 AI Gateway：一个端点接入 290+ 提供商、500+ 模型。统一的 OpenAI 兼容 API，内置负载均衡和 Fallback 机制。 |
| [**LiteLLM**](https://github.com/BerriAI/litellm) | ⭐ **63.2k** | Python | BerriAI | 统一 100+ LLM 的 API 网关。**10 月拆出 Rust core 发行版**，并新增 `litellm.agent(Harness.CLAUDE_CODE / CODEX / OPENCODE)`——网关开始直接「起 Agent」，从代理层上移到编排层。 |
| [**LocalAI**](https://github.com/mudler/LocalAI) | ⭐ **50.3k** | Go | mudler | 本地 OpenAI 兼容服务器。 |
| [**Jan**](https://github.com/janhq/jan) | ⭐ **45.7k** | TypeScript | janhq | 本地离线 AI 助手桌面应用。支持 MCP，零遥测。 |
| [**FastChat**](https://github.com/lm-sys/FastChat) | ⭐ **39.6k** | Python | lm-sys | LMSYS 出品的模型训练/推理/评估一体化平台。 |
| [**freellmapi**](https://segmentfault.com/a/1190000048222748) | ⭐ **35.6k** | TypeScript | — | 免费模型聚合网关——把多家厂商的免费额度/开放接口聚合成统一 API，配合 LiteLLM / OmniRoute 构成「零成本 LLM 接入」工具箱。 |
| [**heretic**](https://segmentfault.com/a/1190000048333142) | ⭐ **33.4k** | Python | — | 自动化 LLM「瘦身」工具——自动审查并剪除模型中冗余的结构与参数，在不显著损失能力的前提下缩小体积。自托管性价比战线的「模型侧」新武器。 |
| [**SGLang**](https://github.com/sgl-project/sglang) | ⭐ **38.8k** | Python | sgl-project | 2026 年增长最快的服务框架，RadixAttention 前缀缓存，RAG 场景比 vLLM 快最高 6 倍，全球 40 万+ GPU 运行。**在「60% 算力用于重算上下文」的现实里，前缀缓存直接决定毛利。** |
| [**MLX**](https://github.com/ml-explore/mlx) | ⭐ **29.2k** | Python | ml-explore | Apple 出品的机器学习框架，专为 Apple Silicon 优化。 |
| [**Strata**](https://github.com/Niko1221/Strata) | ⭐ **43.6k** | C++ | Niko1221 | 一个月涨 3 倍的黑马（10 月 3 日 7,285⭐ → 10 月 15 日 2.51 万）。MIT、单人项目，用 **VRAM/RAM/SSD 三级分层 + 投机解码**把 125B 级 Qwen3.8-Flash-Next 塞进 12—24GB 消费级显卡；10 月 10—14 日连发 v0.1.42→v0.1.44.1（v0.1.42 宣称解码提速 13—16%）。 |
| [**MLC-LLM**](https://github.com/mlc-ai/mlc-llm) | ⭐ **23.4k** | Python | mlc-ai | 让 LLM 在手机/浏览器/IoT 设备上运行的跨平台推理引擎。 |
| [**TensorRT-LLM**](https://github.com/NVIDIA/TensorRT-LLM) | ⭐ **15.1k** | Python | NVIDIA | NVIDIA 官方 GPU 推理优化库。 |
| [**LMDeploy**](https://github.com/InternLM/lmdeploy) | ⭐ **8.1k** | Python | InternLM | 上海 AI Lab 出品的高效推理引擎。 |
| [**DeepGEMM-Ascend / DeepEP-Ascend**](https://blog.csdn.net/debug_fan/article/details/167175851) | ⭐ **515**（对比 NVIDIA 侧 8,522） | C++ | — | 🆕 DeepSeek × 华为昇腾侧镜像库（9 月 30 日宣布，10 月持续发酵）。DeepGEMM-Ascend 需要 **Ascend 950 + CANN 9.20**，DeepEP-Ascend 需要 UBMEM 互联，DeepSelect 昇腾构建只有 BF16。**「一套代码跑遍所有芯片」方向确定，但可用性仍局限在少数新硬件上——别把叙事当现状。** |
| [**openJiuwen X-Router**](https://blog.csdn.net/debug_fan/article/details/167175851) | ⭐ 新项目 | Python | — | 自演进模型路由（openJiuwen 生态组件）——昇腾亲和设计，按任务动态选择模型，宣称可降低 **50% Token 消耗**。国产算力上的「路由层」卡位之作。 |
| [**DeepInfer**](https://www.leiphone.com/category/ai/HecXToP0EHbPjPd0.html) | ⭐ 新项目 | C++/Python | DeepSeek | 🆕 **10-31 开源**。单集群日处理约 **155 万亿 Token**，主打毫秒级推理优化。对照 79%—81% 的企业 GPU 长期半闲置，它把「利用率」本身做成了卖点。 |

> ⚠️ **重要变更**：HuggingFace TGI（text-generation-inference）已于 2026 年 3 月 21 日进入维护模式，官方引导用户迁移至 vLLM / SGLang / llama.cpp / MLX。
>
> 💡 **成本侧三条硬事实（10 月）**：① KV cache 下沉到 SSD 成为主流手段，叠加 Flash 价格同比 **+472%**，被广泛用来解释 token 成本；② 推理侧 60% 算力浪费在重算历史上下文，前缀缓存（SGLang RadixAttention / vLLM APC）是当前 ROI 最高的优化；③ 国内推理产能已成竞争维度——商汤大装置**日均服务 6 万亿 Token**。

### 七、🏋️ 训练 / 微调

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**Unsloth**](https://github.com/unslothai/unsloth) | ⭐ **79.4k** | Python | Unsloth | LLM微调加速引擎，2x加速训练且减少70%显存占用。支持LoRA/QLoRA等主流微调方法。**9月初增长至75.7k**。 |
| [**LLaMA Factory**](https://github.com/hiyouga/LLaMA-Factory) | ⭐ **76k** | Python | LLaMA Factory | 一站式LLM微调平台，支持100+模型的预训练/微调/评估。 |
| [**DeepSpeed**](https://github.com/microsoft/DeepSpeed) | ⭐ **43.3k** | Python | Microsoft | 微软出品的大规模深度学习优化库。ZeRO技术突破显存限制。 |
| [**Stanford Alpaca**](https://github.com/tatsu-lab/stanford_alpaca) | ⭐ **30.2k** | Python | tatsu-lab | 斯坦福出品的指令微调先驱。 |
| [**PEFT**](https://github.com/huggingface/peft) | ⭐ **21.9k** | Python | HuggingFace | HuggingFace出品的参数高效微调库。 |
| [**TRL**](https://github.com/huggingface/trl) | ⭐ **19.7k** | Python | HuggingFace | HuggingFace出品的Transformer强化学习库。支持RLHF/DPO/GRPO等对齐方法。 |
| [**Megatron-LM**](https://github.com/NVIDIA/Megatron-LM) | ⭐ **18.4k** | Python | NVIDIA | NVIDIA出品的大规模语言模型训练框架。 |
| [**ms-swift**](https://github.com/modelscope/ms-swift) | ⭐ **16.1k** | Python | modelscope | 阿里魔搭ModelScope官方微调框架。 |
| [**Axolotl**](https://github.com/OpenAccess-AI-Collective/axolotl) | ⭐ **12.7k** | Python | OpenAccess-AI-Collective | 易用的LLM微调框架，YAML配置文件驱动。 |
| [**OpenRLHF**](https://github.com/OpenRLHF/OpenRLHF) | ⭐ **10.2k** | Python | OpenRLHF | DeepSeek-R1时代最重要的开源GRPO/PPO框架。 |

### 八、🎨 图像 / 视频生成

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**SD WebUI**](https://github.com/AUTOMATIC1111/stable-diffusion-webui) | ⭐ **165k** | Python | AUTOMATIC1111 | Stable Diffusion的图形界面，AI图像生成的标准工具。 |
| [**ComfyUI**](https://github.com/comfyanonymous/ComfyUI) | ⭐ **147k** | Python | comfyanonymous | 节点式AI图像工作流引擎，可视化的方式构建复杂的图像生成Pipeline。 |
| [**MoneyPrinterTurbo**](https://github.com/harry0703/MoneyPrinterTurbo) | ⭐ **143k** | Python | harry0703 | 🆕 AI 短视频全自动生成利器（10月初达11.7万星，周榜飙星前列）。输入主题自动生成文案、素材、配音、字幕、BGM并合成成片，是"AI内容农场"争议与自动化创作需求交织下的现象级项目。 |
| [**OpenCut**](https://github.com/OpenCut-app/OpenCut) | ⭐ **98.2k** | TypeScript | OpenCut-app | 🆕 **开源版CapCut（剪映），10月初突破9.2万星**（9月初81.9k，月增1万+）。Rust渲染内核+TypeScript/Next.js前端，桌面/移动/浏览器三端支持。内置MCP server供AI Agent集成，headless模式支持批量渲染，插件优先架构。MIT许可，隐私保护。 |
| [**OpenMontage**](https://github.com/calesthio/OpenMontage) | ⭐ **80k** | Python | calesthio | 🆕 **全球首个开源Agent视频制作系统**，**10月初达6.4万星**（9月初46.3k）。12条生产流水线、100+专业工具、700+ Agent技能。从调研→脚本→素材→剪辑→合成→配音全流程自动化，技能模块化设计可自由组合。 |
| [**deepfakes/faceswap**](https://github.com/deepfakes/faceswap) | ⭐ **57.6k** | Python | deepfakes | Deepfake换脸开源项目。 |
| [**Fooocus**](https://github.com/lllyasviel/Fooocus) | ⭐ **53.9k** | Python | lllyasviel | 专注"输入Prompt即出图"的极简体验。 |
| [**Hyperframes**](https://github.com/heygen-com/hyperframes) | ⭐ **83.5k** | TypeScript | heygen-com | 🆕 HeyGen出品。"写HTML，渲染视频"——用HTML和CSS写动画，可包含Three.js 3D场景，渲染成确定性MP4。面向Agent构建，适合产品Demo和解释型视频。 |
| [**Real-ESRGAN**](https://github.com/xinntao/Real-ESRGAN) | ⭐ **37.5k** | Python | xinntao | 图像超分辨率修复经典工具。 |
| [**Diffusers**](https://github.com/huggingface/diffusers) | ⭐ **34.9k** | Python | HuggingFace | HuggingFace出品的扩散模型库。 |
| [**ControlNet**](https://github.com/lllyasviel/ControlNet) | ⭐ **34.2k** | Python | lllyasviel | SD可控生成革命性插件。 |
| [**Open-Sora**](https://github.com/hpcaitech/Open-Sora) | ⭐ **29.9k** | Python | hpcaitech | 开源版Sora视频生成。 |
| [**InvokeAI**](https://github.com/invoke-ai/InvokeAI) | ⭐ **29.1k** | Python | invoke-ai | 专业级SD创作工具。 |
| [**Stable Diffusion**](https://github.com/Stability-AI/stablediffusion) | ⭐ **27.2k** | Python | Stability-AI | 扩散模型开源化的里程碑项目。 |
| [**design.md**](https://github.com/google-labs-code/design.md) | ⭐ **28.8k** | Markdown | google-labs-code | 🆕 Google Labs出品的设计规范格式。将YAML设计Token与Markdown说明合并为统一spec文件，AI Agent可读取、验证、对比设计规范并据此生成一致的UI，解决AI生成前端代码的视觉一致性问题。 |
| [**awesome-gpt-image-2**](https://segmentfault.com/a/1190000048222748) | ⭐ **23.6k** | JavaScript | — | 🆕 GPT-Image-2 生态合集（Prompt、案例、工作流）。OpenAI 凭 GPT-Image-2 重夺图像生成王座后，社区侧最热的配套资源仓库。 |
| [**Wan2.1**](https://github.com/Wan-Video/Wan2.1) | ⭐ **17.4k** | Python | Wan-Video | 阿里万相视频生成模型。🆕 **7月持续迭代**：Wan2.1-FLF2V-14B（首尾帧到视频）、Wan2.7（4K、20秒片段、14B架构）。 |
| [**CogVideo**](https://github.com/THUDM/CogVideo) | ⭐ **13.2k** | Python | 清华 THUDM | 清华THUDM出品的视频生成模型。 |
| [**HunyuanVideo**](https://github.com/Tencent/HunyuanVideo) | ⭐ **12.8k** | Python | Tencent | 腾讯混元开源的视频生成模型。 |
| [**AnimateDiff**](https://github.com/guoyww/AnimateDiff) | ⭐ **12.3k** | Python | guoyww | 将静态图像模型转化为视频生成器的创新方案。 |
| [**InstantID**](https://github.com/InstantID/InstantID) | ⭐ **12k** | Python | InstantID | 零样本身份保持图像生成。 |
| [**PhotoMaker**](https://github.com/TencentARC/PhotoMaker) | ⭐ **10.1k** | Python | TencentARC | 腾讯ARC出品，个性化图像生成。 |
| [**LongCat-Video**](https://segmentfault.com/a/1190000048333142) | ⭐ **9.0k** | Python | — | 🆕 **2026年10月初热榜**。LongCat 系视频生成模型开源项目，国产视频生成新力量，与 Wan/HunyuanVideo/CogVideo 同场竞技。 |
| [**FLUX.2**](https://github.com/black-forest-labs/flux2) | ⭐ **2.9k** | Python | black-forest-labs | 🆕 Black Forest Labs新一代文生图模型。**FLUX.2 [dev]（2025年11月）**320亿参数文生图+图像编辑，Apache 2.0。**FLUX.2 [klein]（2026年1月）**40亿参数，消费级硬件1024×1024生成不到0.5秒。 |
| [**open-higgsfield**](https://github.com/wide-trace/open-higgsfield) | ⭐ **5.8k** | TypeScript | wide-trace | 🆕 **2026年8月26日开源**。图像和视频生成工作室——一条Prompt栏，每个模型独立设置，所有成品统一画廊管理。将分散的生成模型统一到一个工作台界面。 |
| [**Concat**](https://github.com/jub0t/Concat) | ⭐ **17.2k** | Rust | jub0t | 🆕 **2026年8月25日开源**，AGPL-3.0。又一个开源CapCut替代，Rust渲染内核。与OpenCut形成开源视频编辑双雄格局。 |

### 九、🎤 语音 / 音频

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**Whisper**](https://github.com/openai/whisper) | ⭐ **113k** | Python | OpenAI | OpenAI出品的语音识别标杆模型，支持99种语言。 |
| [**VoiceStudio**](https://blog.csdn.net/weixin_45635831/article/details/167177296) | ⭐ **96.8k** | Python | — | 🆕 **2026年10月初热榜（9月3日仅1.47万→一个月内近5倍蹿升）**。本地优先语音创作平台——TTS/ASR/语音克隆一体，全部在自己的机器上跑。与Voicebox正面竞争"开源语音工作室"定位，是10月语音赛道最大黑马。 |
| [**GPT-SoVITS**](https://github.com/RVC-Boss/GPT-SoVITS) | ⭐ **64.9k** | Python | RVC-Boss | 少样本语音克隆与合成。 |
| [**Voicebox**](https://github.com/jamiepine/voicebox) | ⭐ **60.5k** | TypeScript | jamiepine | 🆕 开源AI语音工作室。"Clone, dictate, create"——包含语音克隆、转录、音频编辑、本地模型等能力，在自己的机器上运行。适合产品Demo配音、播客制作和Agent语音输出。 |
| [**TTS (Coqui)**](https://github.com/coqui-ai/TTS) | ⭐ **46.2k** | Python | coqui-ai | 深度学习语音合成全能库。 |
| [**ChatTTS**](https://github.com/2noise/ChatTTS) | ⭐ **40k** | Python | 2noise | 专为对话场景优化的TTS模型。 |
| [**Bark**](https://github.com/suno-ai/bark) | ⭐ **39.4k** | Python | suno-ai | Suno AI出品的多语种TTS。 |
| [**OpenVoice**](https://github.com/myshell-ai/OpenVoice) | ⭐ **38.2k** | Python | myshell-ai | MyShell出品的即时声音克隆技术。 |
| [**MockingBird**](https://github.com/babysor/MockingBird) | ⭐ **36.9k** | Python | babysor | 5秒克隆声音的语音合成工具。 |
| [**Fish Speech**](https://github.com/fishaudio/fish-speech) | ⭐ **33.7k** | Python | fishaudio | 多语种零样本TTS。 |
| [**CosyVoice**](https://github.com/FunAudioLLM/CosyVoice) | ⭐ **24.4k** | Python | FunAudioLLM | 阿里通义实验室出品的语音合成模型。 |
| [**F5-TTS**](https://github.com/SWivid/F5-TTS) | ⭐ **15.6k** | Python | SWivid | 基于Flow Matching的零样本TTS。 |
| [**Spark-TTS**](https://github.com/SparkAudio/Spark-TTS) | ⭐ **11k** | Python | SparkAudio | 新兴高质量TTS模型。 |

### 十、👁️ 计算机视觉

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**OpenCV**](https://github.com/opencv/opencv) | ⭐ **91.6k** | C++ | opencv | 计算机视觉标准库，2500+算法覆盖全场景。 |
| [**Ultralytics**](https://github.com/ultralytics/ultralytics) | ⭐ **63.3k** | Python | ultralytics | YOLO系列统一框架。 |
| [**Segment Anything**](https://github.com/facebookresearch/segment-anything) | ⭐ **55.1k** | Python | Meta | Meta出品的"分割一切"模型。 |
| [**SAM 2**](https://github.com/facebookresearch/sam2) | ⭐ **20.1k** | Python | Meta | Meta SAM二代，从图像分割扩展到视频分割。 |
| [**GroundingDINO**](https://github.com/IDEA-Research/GroundingDINO) | ⭐ **10.7k** | Python | IDEA-Research | 开放词汇目标检测。 |
| [**Unlimited-OCR**](https://huggingface.co/baidu/Unlimited-OCR) | ⭐ **1.2k+** | Python | baidu | 🆕 百度出品的开源权重视觉语言模型，专为OCR场景优化。支持PDF高亮——不仅能识别文字，还能标注文字在页面上的位置。可在单张消费级GPU上运行，MIT许可。 |
| [**Mistral OCR 4**](https://huggingface.co/mistralai/mistral-ocr) | ⭐ **N/A** | Python | mistralai | 🆕 Mistral AI出品（2026年6月23日），支持170语言的文档模型。返回带边界框、块类型和逐词置信度的结构化页面，是OCR领域的强劲新选手。 |

### 十一、🗄️ 向量数据库

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**Milvus**](https://github.com/milvus-io/milvus) | ⭐ **46.6k** | Go | milvus-io | 云原生向量数据库，支持万亿级向量的分布式存储和检索。 |
| [**Qdrant**](https://github.com/qdrant/qdrant) | ⭐ **35.5k** | Rust | qdrant | Rust编写的高性能向量搜索引擎。 |
| [**Chroma**](https://github.com/chroma-core/chroma) | ⭐ **29.7k** | Rust | chroma-core | AI搜索基础设施，为LLM应用提供轻量级向量存储。 |
| [**pgvector**](https://github.com/pgvector/pgvector) | ⭐ **23.7k** | C | pgvector | PostgreSQL的向量搜索扩展。 |
| [**Weaviate**](https://github.com/weaviate/weaviate) | ⭐ **16.9k** | Go | weaviate | 混合向量/对象数据库。 |
| [**LanceDB**](https://github.com/lancedb/lancedb) | ⭐ **11.9k** | Rust | lancedb | 嵌入式向量数据库，无需服务器直接嵌入应用。 |

### 十二、🔢 嵌入 / 检索

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**Jina**](https://github.com/jina-ai/jina) | ⭐ **21.8k** | Python | jina-ai | 多模态AI云原生服务框架。 |
| [**FlagEmbedding**](https://github.com/FlagOpen/FlagEmbedding) | ⭐ **12.3k** | Python | FlagOpen | 智源研究院出品的嵌入模型和检索框架。 |
| [**WeMM-Embedding**](https://github.com/Tencent/WeMM-Embedding) | ⭐ **1.8k** | Python | Tencent | 🆕 **2026年8月25日开源**。腾讯微信视觉团队出品的通用多模态嵌入模型族，支持多模态理解和检索。填补了国产多模态嵌入模型的开源空白。 |

### 十三、🔌 协议 / 标准化

> 📊 **MCP生态8月数据**：GitHub上MCP仓库超17,000个，官方Registry登记Server突破11,000个，SDK月下载破1亿次。财富500强中31%已部署MCP服务器。**2026年5月21日MCP发布最大修订**：无状态核心、MCP Apps（服务端渲染UI）、Tasks扩展、OAuth/OpenID Connect对齐。**2026年8月初MCP 1.0 规范草案发布**，进一步明确了Registry与协议标准。

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers) | ⭐ **97.7k** | TypeScript | punkpeye | 🆕 MCP服务器合集，冲进GitHub总榜前300。收录数千个MCP Server实现，是MCP生态的入口级项目。 |
| [**Agent-Reach**](https://github.com/Panniantong/Agent-Reach) | ⭐ **111k** | Python | Panniantong | "让AI Agent看见整个互联网，零API费用"。一键赋予任何AI Agent读取15+主流平台公开内容的能力（Twitter/X、Reddit、B站、小红书、GitHub、YouTube等）。每平台一个Python模块，内置多后端自动路由。**10月初已达9.19万星**，稳居热榜前十。 |
| [**MCP Servers**](https://github.com/modelcontextprotocol/servers) | ⭐ **92k** | TypeScript | modelcontextprotocol | MCP协议参考实现集合，包含文件系统、数据库、API等数十种标准MCP Server。 |
| [**chrome-devtools-mcp**](https://github.com/ChromeDevTools/chrome-devtools-mcp) | ⭐ **55.2k** | TypeScript | ChromeDevTools | 🆕 Chrome开发者工具MCP Server，让AI Agent直接操控Chrome DevTools进行网页调试和自动化。**10月初突破5万星**。 |
| [**playwright-mcp**](https://github.com/microsoft/playwright-mcp) | ⭐ **39.6k** | TypeScript | Microsoft | 🆕 微软出品的浏览器自动化MCP Server，基于Playwright实现Agent驱动的浏览器操作。 |
| [**github-mcp-server**](https://github.com/github/github-mcp-server) | ⭐ **34.4k** | Go | github | 🆕 GitHub官方MCP Server，让AI Agent直接操作GitHub仓库、Issues、PR和工作流。 |
| [**code-review-graph**](https://github.com/tirth8205/code-review-graph) | ⭐ **32.7k** | Python | tirth8205 | 🆕 将代码库解析为知识图谱的MCP工具。用Tree-sitter构建AST，以节点（函数/类/导入）和边（调用/继承/测试覆盖）存储为图，审查时查询计算AI助手所需的最小文件集。解决AI编码助手每次重读整个代码库导致的Token浪费问题，专为Claude Code/Cursor等AI编码助手设计。 |
| [**fastmcp**](https://github.com/PrefectHQ/fastmcp) | ⭐ **28.4k** | Python | PrefectHQ | 🆕 PrefectHQ出品的Pythonic MCP服务端/客户端快速构建框架。让用Python构建MCP Server像写FastAPI一样简单。 |
| [**A2A**](https://github.com/google/A2A) | ⭐ **26.5k** | Python | Google | Google提出的Agent-to-Agent通信协议。已有150+组织参与，**2026年6月捐赠给Linux基金会**，与MCP形成AI协议双雄格局。 |
| [**MCP Python SDK**](https://github.com/modelcontextprotocol/python-sdk) | ⭐ **24.8k** | Python | modelcontextprotocol | Anthropic提出的Model Context Protocol Python实现。 |
| [**MCP TypeScript SDK**](https://github.com/modelcontextprotocol/typescript-sdk) | ⭐ **13.8k** | TypeScript | modelcontextprotocol | MCP协议的TypeScript/JavaScript实现。 |
| [**wigolo**](https://github.com/KnockOutEZ/wigolo) | ⭐ **5.5k** | TypeScript | KnockOutEZ | 🆕 **本地优先的AI Agent网络智能层**MCP服务器。搜索、抓取、爬取、提取、缓存、找相似、研究、自主收集，全程零API Key、零云依赖、零按次计费。18个搜索引擎适配器+ML重排序+设备端嵌入模型，所有数据存于 `~/.wigolo/`。支持Claude Code/Cursor/Codex/Gemini CLI等，7月GitHub Trending持续升温。AGPL-3.0。 |
| [**claude-plugins-community**](https://github.com/anthropics/claude-plugins-community) | ⭐ **4.9k** | Python | anthropics | 🆕 **2026年9月开源（Anthropic官方）**。Claude 社区插件镜像/分发仓库——官方下场做插件生态治理，与 DSH"万物皆插件"形成正面呼应，插件分发标准之争开启。 |
| [**commerce-agents**](https://github.com/anthropics/commerce-agents) | ⭐ **3.5k** | Python | anthropics | 🆕 **2026年9月1日开源**，Apache 2.0。**Anthropic官方商业Agent参考蓝图**——覆盖零售、电商、电信、娱乐场景的购物和商户Agent示例。标志着Agent从"开发者工具"走向"商业化落地"，由模型厂商亲自下场提供生产级参考实现。 |
| [**x64dbg-mcp-server**](https://github.com/duty1g/x64dbg-mcp-server) | ⭐ **2.8k** | Zig | duty1g | 🆕 **2026年8月22日开源**，MIT许可。**MCP渗透到逆向工程领域**——Zig编写，零依赖单二进制，为x64dbg调试器暴露完整MCP接口。AI Agent可设断点、单步执行、读内存、dump寄存器，将MCP从"Web工具"扩展到"二进制安全"。 |

### 十四、🖥️ UI 平台

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**Open WebUI**](https://github.com/open-webui/open-webui) | ⭐ **159k** | Python | open-webui | 🆕 **9月初已增长至151k**。Ollama最佳搭档，功能最全的开源AI聊天界面。支持多模型对话、知识库、插件和工作流。GitHub AI排行榜第10名。 |
| [**NextChat**](https://github.com/ChatGPTNextWeb/NextChat) | ⭐ **89k** | TypeScript | ChatGPTNextWeb | 一键部署的ChatGPT Web界面。 |
| [**LobeChat**](https://github.com/lobehub/lobe-chat) | ⭐ **85.2k** | TypeScript | lobehub | 现代化多模型聊天平台。🆕 中国团队开发，支持30+语言，设计最佳的开源Chat UI，AGPL-3.0许可。 |
| [**LibreChat**](https://github.com/danny-avila/LibreChat) | ⭐ **47.1k** | TypeScript | danny-avila | 多模型ChatGPT克隆。 |
| [**ChatBox**](https://github.com/Bin-Huang/chatbox) | ⭐ **42.3k** | TypeScript | Bin-Huang | 轻量级AI桌面客户端。 |

### 十五、🔄 工作流自动化 / 低代码平台

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**n8n**](https://github.com/n8n-io/n8n) | ⭐ **210k** | TypeScript | n8n-io | 🆕 **9月初已增长至203k+**。n8n 2.0（2026年1月）默认启用任务运行器，AI Agent节点支持OpenAI/Anthropic/Ollama等，新增Chat Hub把工作流秒变GPTs，AI Assistant可自动规划/构建/测试工作流。30天96次发布事件。 |
| [**Dify**](https://github.com/langgenius/dify) | ⭐ **161k** | TypeScript | langgenius | 生产级AI应用开发平台。超过100万部署应用、18万开发者；RAG+工作流+API+监控一体化。**9月初增长至154k+**。 |
| [**Langflow**](https://github.com/langflow-ai/langflow) | ⭐ **157k** | Python/JS | langflow-ai | 🆕 **8月初突破102k星**。可视化LangChain，完整组件访问，可导出Python代码，LangSmith集成。 |
| [**Flowise**](https://github.com/FlowiseAI/Flowise) | ⭐ **55.6k** | TypeScript | FlowiseAI | 拖拽式LLM流程构建工具。🆕 2025年被Workday收购，轻量单容器部署，100+ LLM集成。 |
| [**Apache Airflow**](https://github.com/apache/airflow) | ⭐ **47.5k** | Python | apache | 工作流编排的行业标准，Apache基金会顶级项目。 |
| [**Activepieces**](https://github.com/activepieces/activepieces) | ⭐ **25.5k** | TypeScript | activepieces | AI原生工作流自动化平台。 |
| [**Prefect**](https://github.com/PrefectHQ/prefect) | ⭐ **24.2k** | Python | PrefectHQ | 现代Python工作流引擎。 |
| [**Windmill**](https://github.com/windmill-labs/windmill) | ⭐ **18.6k** | TypeScript | windmill-labs | 脚本转工作流平台。 |

### 十六、📈 监控 / 评估

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**LangFuse**](https://github.com/langfuse/langfuse) | ⭐ **37.4k** | TypeScript | langfuse | 开源LLM可观测性平台。 |
| [**MLflow**](https://github.com/mlflow/mlflow) | ⭐ **28.8k** | Python | mlflow | AI工程全生命周期管理平台。 |
| [**DeepEval**](https://github.com/confident-ai/deepeval) | ⭐ **19.5k** | Python | confident-ai | LLM测试评估框架。 |
| [**RAGAS**](https://github.com/explodinggradients/ragas) | ⭐ **16.3k** | Python | explodinggradients | RAG系统专项评估框架。 |
| [**Phoenix**](https://github.com/Arize-ai/phoenix) | ⭐ **12.3k** | Python | Arize-ai | Arize AI出品的AI可观测性平台。 |

### 十七、🛡️ AI 安全与防护（事前扫描 → 事中拦截 → 事后审计，三层已齐）

> 当 Agent 拥有终端控制权、文件读写权限甚至能执行 `git push`，安全不再是「锦上添花」，而是「底线」。
>
> **10 月的形态变化在于「治理主体换了」**：9 月是社区工具竞赛（SkillSpector 扫技能、agent-firewall 拦调用），10 月变成**监管与审计入场**——
>
> - **FTC 据报向 OpenAI 与 Anthropic 发出传票**（10-15 报道）：要求提交安全事故记录、隐私政策与营销材料，并拟强制高管作证；
> - **G7 拟推演 AI 网络攻击银行**（10-16 路透）：日本财务大臣确认开展桌面推演，防范前沿模型「超级充电」式黑客行为；
> - **Anthropic 开放 METR 员工级审计权限**（10-15）：独立评估机构可以接近内部员工的权限检视系统，「调速」从承诺变成可验证机制；
> - **OpenAI 与 Anthropic 在英听证会上主动「请监管我们」**；
> - **Anthropic 划拨 5% 股份入公共福利基金**（10-18），随估值增长。
>
> 再叠加 9 月 24 日澳总理证实「OpenAI 智能体擅自闯入政府系统」、10 月 4 日 MaxKB 沙箱绕过（CVE-2026-77521，间接 Prompt Injection）、10 月 8 日 Mem0 未鉴权删记忆（CVE-2026-31241）、Pwn2Own 首日 32 个 0-day、ClawHavoc 投放 44 个恶意 Skill——**「失控 Agent 的事故成本」第一次被外部定价**。

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**strix**](https://github.com/usestrix/strix) | ⭐ **75.2k** | Python | usestrix | 开源 AI 渗透测试工具，自动发现并修复 Web 应用漏洞。扫描 OWASP Top 10（SQL 注入、XSS、CSRF 等）并给出修复建议。月增 1.8 万星，在 AI 代码生成浪潮中为安全装上「刹车」。 |
| [**system_prompts_leaks**](https://github.com/asgeirtj/system_prompts_leaks) | ⭐ **71.3k** | Markdown | asgeirtj | 各大 AI 系统提示词泄露合集（Anthropic / OpenAI / Google / xAI）。从 Claude、ChatGPT、Gemini、Grok 等逆向出的系统级 Prompt，帮助开发者写出更好的应用层 Prompt——**也是理解「厂商怎么防注入」的第一手材料**。 |
| [**iFixAi**](https://github.com/iFixAi/iFixAi) | ⭐ **41.4k** | TypeScript | iFixAi | 🆕 **120 秒给 Agent 打分 A—F**。设计上有个巧思：故意要求配置**两家不同厂商的 API Key 做交叉审计**，避免 Agent 自评。8 天 +5.8k，是 10 月增速最快的安全项目之一。 |
| [**Cybersecurity Skills**](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | ⭐ **36k** | Shell | mukul975 | 817 个结构化网络安全 Skills，映射到 MITRE ATT&CK、NIST CSF 2.0、MITRE ATLAS、D3FEND、NIST AI RMF 等六大框架。配合 Claude Code / Codex / Cursor / Gemini CLI 等 20+ 平台使用。 |
| [**SkillSpector**](https://github.com/NVIDIA/SkillSpector) | ⭐ **25.7k** | Python | NVIDIA | **AI Agent Skills 安全扫描器**。检测 16 个类别、65 种漏洞模式，包括 Prompt Injection、数据外泄、权限提升、供应链风险。规则：任何第三方 skill 安装前先跑一遍。Apache 2.0。 |
| [**NVIDIA OpenShell**](https://github.com/NVIDIA/OpenShell) | ⭐ **21.5k** | Rust | NVIDIA | 🆕 **Open Agent Safety Platform 的核心件**，100+ 签署方。Rust 沙箱，把 Agent 的每一次执行装进可审计的隔离环境。 |
| [**jailbreaks**](https://github.com/togg53192-cmd/jailbreaks) | ⭐ **16.7k** | Markdown | togg53192-cmd | 🆕 收集 31 组针对 25+ 模型的系统提示、角色定义与政策规范，用于研究提示层级与模型对注入的抵抗力。**红队资料的「公开教科书」**，也是理解厂商防御边界的入口。 |
| [**agent-firewall**](https://github.com/agent-firewall/agent-firewall) | ⭐ **8.2k** | Rust | agent-firewall | **AI Agent 运行时防火墙**。在 Agent 与工具 / MCP 之间架一道实时拦截层，基于策略引擎阻断越权工具调用、敏感数据外泄（如把密钥写入公开 Gist）和危险命令。Rust 实现、低延迟、可热更新规则。相比 SkillSpector 的「事前扫描」，它做「事中拦截」。 |
| [**destructive_command_guard**](https://github.com/Dicklesworthstone/destructive_command_guard) | ⭐ **6.3k** | Rust | Dicklesworthstone | 拦截 AI Agent 可能执行的毁灭性命令：`rm -rf /`、`git push --force` 到 main、`DROP TABLE`、`chmod -R 777`、Fork 炸弹等。Rust 实现，小而美。 |
| [**ARTEX**](https://github.com/mhtsec/ARTEX) | ⭐ **4.1k** | Go | mhtsec | 🆕 **10-15 日榜项目**。Go 后端 + Next.js 前端的 **AI 自主渗透测试系统**：资产同步、任务管理、LLM 集成、Agent 调度与审批流程，获百度「agent+」攻防挑战赛冠军。同日还出现一个近乎同名的复刻版 ARTEXX（1,202⭐）——**自主渗透的门槛已经低到一个周末就能复刻**。 |
| [**stop-that-shit**](https://github.com/lennney/stop-that-shit) | ⭐ **3.9k** | JavaScript | lennney | 面向 Codex / GPT 场景的多平台 Hook + Skill Guard，拦截编码 Agent 的「无需求哈希/校验和生成」和任务范围膨胀。从「安全拦截」扩展到「**行为质量拦截**」——不仅防危险操作，更防无意义操作。 |
| [**oss-scanner**](https://github.com/anthropics/oss-scanner) | ⭐ **1.8k** | Dockerfile | Anthropic | 🆕 **10-15 日榜，厂商亲自下场做审计**。在隔离 VM 中构建并分析开源项目，自动生成漏洞报告与修复建议。面向开源维护者与安全团队——把「供应链安全」做成可一键跑的流水线。 |
| [**reverify**](https://github.com/2akouwu/reverify) | ⭐ **1.3k** | Python | 2akouwu | AI 幻觉防护层——AI 提出声明，确定性工具裁决，每条声明对照 ground truth 验证并附带证据。MCP Server + CLI 形态，补齐「Agent 可能说谎」的最后一环。 |
| [**agent-safe-pipeline**](https://github.com/decionis/agent-safe-pipeline) | ⭐ **671** | TypeScript | Decionis | **参考架构级** Agent 安全方案：Agent 提议动作但不可授权——不可变意图捕获、独立策略裁决（ALLOW / ESCALATE / BLOCK）、人工审批、单次意图绑定令牌的 SafeExecutor。从架构层面保证 Agent 永远不可越权，是「零信任 Agent」的落地。 |

> 🧭 **三层防御怎么配（10 月版）**
>
> | 阶段 | 要解决的问题 | 推荐组合 | 失效后果 | 落地成本 |
> | :--- | :--- | :--- | :--- | :--- |
> | **事前** | 这个 Skill / MCP 能不能装 | SkillSpector（65 种漏洞模式）+ oss-scanner（供应链审计） | 恶意 Skill 直接进流水线 | 低：装一次，接进 CI |
> | **事中** | 这个调用能不能放行 | agent-firewall（策略拦截）+ OpenShell（沙箱）+ destructive_command_guard | 越权调用与密钥外泄 | 中：要写策略 |
> | **事后** | 这次执行到底干了什么 | iFixAi（交叉审计打分）+ 第三方审计 + 完整会话留痕 | 出了事无法归因 | 中高：要留痕基建 |
>
> **一句提醒**：`ClawHavoc` 那 44 个恶意 Skill 不是靠「用户小心」防住的，是靠「默认不信任第三方技能」防住的。**先把默认值改掉，再谈工具。**

### 十八、💰 AI 金融 / 量化交易（🆕 2026年7月新兴赛道）

> AI正在把量化交易的门槛拉到地板——从机构专属变成人人可用。

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**TradingAgents**](https://github.com/TauricResearch/TradingAgents) | ⭐ **122k** | Python | Tauric Research | 🆕 多Agent LLM金融交易框架，模拟真实交易公司运作。分析师团队（基本面/情绪/新闻/技术分析）→研究员团队（多空辩论）→交易员Agent→风控与组合经理，Agent间动态讨论确定最优策略。基于LangGraph构建，支持10+LLM提供商，覆盖美股/A股/港股/加密货币等多市场。**v0.3.1（7月5日）**，决策日志持久化+断点续跑，Apache 2.0，AAAI 2025论文。**9月初突破10万⭐**。 |
| [**ai-hedge-fund**](https://github.com/virattt/ai-hedge-fund) | ⭐ **64.7k** | Python | virattt | 🆕 模拟完整AI对冲基金团队，13个Agent分别扮演巴菲特（价值投资）、芒格（逆向思维）、木头姐（成长投资）、索罗斯（宏观对冲）等"基金经理"。每个分析师Agent独立出信号→风控Agent审核→组合经理配置。教育/研究属性大于实战，872次提交维护活跃。 |
| [**Kronos**](https://segmentfault.com/a/1190000048333142) | ⭐ **40.0k** | Python | Kronos 团队 | 🆕 **2026年10月初热榜，达4万星**。"金融市场语言基础模型"（Financial Foundation Model）——把K线/量价数据当作一种语言进行预训练的时序基础模型，开源量化从"用LLM做交易"升级到"为市场训练专用基础模型"。 |
| [**financial-services**](https://blog.csdn.net/u130130/article/details/166899588) | ⭐ **38.2k** | Python | 未确认（参考实现系） | 🆕 **2026年9月月榜项目**。金融服务工作流的**参考Agent与数据连接器合集**——与Anthropic commerce-agents同一思路（厂商/机构下场给行业级蓝图），把合规、研报、风控等金融工作流做成可直接复用的Agent模板。 |
| [**Vibe-Trading**](https://github.com/HKUDS/Vibe-Trading) | ⭐ **38.1k** | Python | HKUDS | 🆕 港大数据科学实验室出品，"用聊天的方式做量化"。自然语言描述交易想法→Agent自动完成Route（识别市场）→Ground（拉取数据）→Test（编写策略+回测）→Deliver（输出报告含K线图、热力图、风险指标）。多Agent协作+MCP协议，支持真实券商连接，MIT协议。 |

### 十九、🏢 Agent 办公自动化（🆕 2026年7月新兴赛道）

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**orca**](https://github.com/stablyai/orca) | ⭐ **124k** | TypeScript | stablyai | 🆕 **管理并行编码Agent集群的桌面/移动端工具**。当团队有5个Claude Code、3个Codex、2个Cursor同时在跑时，orca提供统一Agent编排界面，支持Worktree隔离、并行任务对比、跨Agent结果合并。桌面+移动+VPS三种部署。 |
| [**ai-job-search**](https://github.com/MadsLorentzen/ai-job-search) | ⭐ **71.5k** | TypeScript | MadsLorentzen | 🆕 AI求职框架：评估岗位、定制简历、写求职信、准备面试，全跑在本地。基于Claude Code构建，完全本地运行，MIT协议。单周+13k星。 |
| [**meetily**](https://github.com/Zackriya-Solutions/meetily) | ⭐ **32.7k** | Swift | Zackriya-Solutions | 🆕 100%本地AI会议助手，4x Whisper转录，无需云端。隐私优先，所有会议数据在本地处理。 |
| [**OfficeCLI**](https://github.com/iOfficeAI/OfficeCLI) | ⭐ **33.2k** | Python | iOfficeAI | 🆕 **首个面向AI Agent的Office套件**，无需安装Office。把Word/Excel/PowerPoint操作封装为CLI命令，AI Agent可直接读写.docx/.xlsx/.pptx文件。支持数据读取、图表生成、PPT模板填充，是Agent+办公自动化的关键拼图。 |
| [**headcount**](https://github.com/cbrock84/headcount) | ⭐ **2.6k** | Markdown | cbrock84 | 🆕 **2026年8月28日开源**，MIT许可。将Claude Code组织成一家"公司"——15+部门、125+技能，每个技能独立安装。CEO/工程/QA/设计等Agent角色分工明确，是Agent Skills"组织化"趋势的代表项目。 |

### 二十、🧠 大模型（开源权重）

> 📊 **2026 年 10 月的开源节奏已经变成「周更」**：6—7 月 30 天内 10 款旗舰落地；9 月「六家齐发开放权重」；10 月中旬到下旬，Meta、NVIDIA、Black Forest Labs、DeepSeek 又各发了一轮。
>
> 但真正值得注意的不是数量，是**叙事的分裂**：一边是 **GLM-5.2 在 SWE-Bench Pro 上击败 GPT-5 与 Claude**，开源在 agentic coding 上首次领先闭源；另一边是 **Reflection Beam 承诺 Apache 2.0 却只有 API、Mistral Large 4 只有等待列表**，HuggingFace CEO 公开质疑「权重没到就自称最强开权重模型」。
>
> **战场已经从「开源能不能追上闭源」变成「Open Source 与 Open Weight 的控制权之争」**——许可证条款、训练数据透明度、可商用范围，成了新的主战场。

| 模型 | Stars | 出品方 | 发布 · 参数 | 简介 |
| :--- | :---: | :--- | :--- | :--- |
| [**DeepSeek-V3/V4**](https://github.com/deepseek-ai/DeepSeek-V3) | ⭐ **105k** | DeepSeek | 2026-04-24 · V4-Pro 1.6T（49B 激活） | 国产最强开源 LLM。V4-Pro 1.6T 参数对标顶级闭源模型；V4-Flash 284B/13B MoE，MIT 许可，百万上下文，价格最低（$0.14/$0.28）。 |
| [**DeepSeek-R1/R3**](https://github.com/deepseek-ai/DeepSeek-R1) | ⭐ **92k** | DeepSeek | 2026-07-05 · R3 685B-A37B MoE | R3 于 7 月 5 日发布，AIME 2025 达 95%，**开源模型数学推理最强**。1M 上下文，MIT 许可。 |
| [**Llama 5**](https://github.com/meta-llama/llama) | ⭐ **59.6k** | Meta | 2026-07-06 · 405B 稠密 | 7 月 6 日发布，MMLU 91%，**开源模型学术知识最强**。256K 上下文，原生多模态。Llama 5 License。**Meta 已转向「部分闭源 + 选择性开放」策略**，Llama 5 是最后一个「全家桶式」开源。 |
| [**Qwen 3.8-Max**](https://github.com/QwenLM/Qwen3) | ⭐ **27.7k** | 阿里通义 | 2026-08-04 · 2.4T MoE | 8 月 4 日开源。2.4 万亿参数 MoE，SWE-Verified 83%，原生 1M 上下文，Apache 2.0。与 Qwen 4.1 形成「双旗舰」格局。 |
| [**Qwen3 / Qwen 4.1**](https://github.com/QwenLM/Qwen3) | ⭐ **27.7k** | 阿里通义 | 2026-07-02 · 4.1: 32B-A3B MoE | Qwen 4.1 于 7 月 2 日发布，SWE-Verified 80%，Mac 可运行模型新冠军。1M 原生上下文，Apache 2.0。 |
| [**Kimi K2 / K3**](https://github.com/MoonshotAI/Kimi-K2) | ⭐ **11.1k** | 月之暗面 | 2026-07-16 · K3 ~2.8T | K3 于 7 月 16 日发 API，权重于 7 月 27 日如期开源。2.8 万亿参数，**史上最大开源权重模型**，开源两周冲上 42k⭐ 登顶 GitHub Trending。2M 上下文，SWE-Bench Pro 66%。MIT 许可。 |
| [**Mistral**](https://github.com/mistralai/mistral-inference) | ⭐ **10.8k** | Mistral AI | 2026-07-04 · Medium 4 41B-A13B MoE | Mistral Medium 4 于 7 月 4 日发布，SWE-Verified 70%，32GB Mac 上 ~48 tok/s，速度/编码质量比最优。Apache 2.0。**Mistral Large 4（1.05 万亿参数「Le Chonk」）10-06 发布时只有 API，10-29 才正式放出权重**——两周的「承诺与交付」时间差，本身就是 10 月的行业议题。 |
| [**Yi**](https://github.com/01-ai/Yi) | ⭐ **7.8k** | 01.AI | — | 李开复创办的零一万物出品，中英文双语大模型。 |
| [**InternLM**](https://github.com/InternLM/InternLM) | ⭐ **7.3k** | 上海 AI Lab | — | 书生系列大模型，学术界影响力最高的开源 LLM 之一。 |
| [**GLM-5.2**](https://github.com/zai-org/GLM-5) | ⭐ **7.5k** | 智谱 AI | 2026-07-08 · 744B-A40B MoE | 7 月最重要开源事件：SWE-Bench Pro 68.5%，**首个在 agentic coding 上击败 GPT-5 和 Claude 的开源模型**。1M 原生上下文，IndexShare 架构使每 token FLOPs 降低 2.9×。另有 GLM-5.2 Air（106B-A12B，Mac ~30 tok/s）。MIT 许可。 |
| [**Gemma 4.5**](https://github.com/google-deepmind/gemma) | ⭐ **5.8k** | Google | 2026-07-03 · 27B 稠密 | Gemma 4.5 于 7 月 3 日发布，1M 原生上下文，MMLU 86%，M5 Max 上 ~42 tok/s。 |
| [**DeepSeek-V4.1-Flash-1017**](https://www.qbitai.com/2026/10/504067.html) | ⭐ — | DeepSeek | 2026-10-17 · Flash 级 | 🆕 **本轮最重要的模型发布**。命名即快照日期（10 月 17 日）。核心卖点是**「性能—费用帕累托改进」**：各项基准整齐抬头的同时，任务运行时间与输出长度被一起压下来。针对 **DeepSeek Harness 专项优化**（需 DSH ≥ 0.2.1-rc.1），腾讯 CodeBuddy / WorkBuddy 同步受益。新能力「**许愿式编程**」——一句话直出可交互 3D 场景（官方 Demo 是「Vibe 修故宫」、Godot 版《传送门 2》），底层是**基于自反馈的强化学习**：写完第一版先自查，发现不对回头修。同步开放自研 **Search / Fetch API**（每千次成功请求 5 元，失败/无结果/超时不计费，**11 月 1 日前免费**）。 |
| [**Muse Spark Open**](https://venturebeat.com/technology/meta-unveils-muse-spark-open-the-new-top-u-s-open-weights-model-and-it-runs-on-two-paired-mac-desktops) | ⭐ — | Meta | 2026-10 中旬 · 未公布 | 🆕 **美版顶级开放权重模型**，可在**两台互联的 Mac 桌面**上本地运行——「旗舰级开放权重能在消费硬件跑」第一次成为官方宣传点。同批发布的 Muse Wonder 在 3D 建模上出现短板，引发内部辩护，说明「多模态开放权重」仍在爬坡。 |
| [**GLM-5.3**](https://baike.baidu.com/item/GLM-5.3/68244961) | ⭐ — | 智谱 AI | 2026-08 中旬 · 未公布 | 8 月 17—18 日发布，GLM-5.2 的增强后续，与 Qwen3.8-Max 并称国产旗舰双雄。持续霸榜 SWE-Bench 系 agentic 编码基准。 |
| [**Step 5 Preview**](https://www.stepfun.com/) | ⭐ — | 阶跃星辰 | 2026-10-15 · 600B（27B 激活）稀疏 MoE | 🆕 **10 月「真放权重」的代表**。600B 总参 / 27B 激活，1M 上下文，原生图文，BF16 + FP8，HuggingFace 与 ModelScope 同步。OpenRouter 日榜与周榜 token 用量全球第二。**它与 Beam / Mistral Large 4 的对比，构成了 10 月「发布 ≠ 开源」的完整案例。** |
| [**Nemotron 3.5 Super VL**](https://venturebeat.com/technology/nvidias-new-open-nemotron-3-5-super-vl-with-post-training-beats-claude-opus-5-gpt-6-1-sol-on-specialized-task-benchmarks) | ⭐ — | NVIDIA | 2026-10 中旬 · 未公布 | 🆕 **后训练开放多模态模型**，在专项基准上超越 Claude Opus 5 与 GPT-6.1 Sol。NVIDIA 的路线很清楚：不追通用榜首，专打「特定任务 + 可商用 + 训练配方公开」。 |
| [**MiMo-V2.6-Flash**](https://blog.csdn.net/debug_fan/article/details/167175851) | ⭐ — | 小米 | 2026-09/10 报道 · 309B-A15B MoE | 小米开源系模型：**309B 总参、15B 激活、1M 上下文**，主打「低激活高能力」的服务性价比路线。 |
| [**Beam**](https://blog.csdn.net/debug_fan/article/details/167175851) | ⭐ — | Reflection AI | 2026-10 报道 · 501B | Reflection 的开放权重新作，**以低算力配置对标中国开源旗舰**。⚠️ 10 月 5 日承诺 Apache 2.0，到 10 月 14 日仍只有 API 与等待列表——**「承诺开源」与「真的开源」之间的时间差，本身就是 10 月的行业议题。** |
| [**Ternary-Bonsai-2**](https://blog.csdn.net/debug_fan/article/details/167175851) | ⭐ — | Thinking Machines | 2026-09/10 报道 · 三值量化 | **三值（Ternary）量化开源模型**——极限压缩换取自托管成本断崖式下降，与 Decider 2B 同推「自托管性价比战线」。 |
| [**Strands Decider 2B**](https://blog.csdn.net/debug_fan/article/details/167175851) | ⭐ — | AWS Strands 团队 | 2026-09/10 报道 · 2B | 2B 参数性价比小模型，面向 Agent 工作流中的路由/裁决类轻任务，对抗集中式高价大模型。 |
| [**Inkling**](https://huggingface.co/thinking-machines) | ⭐ — | Thinking Machines | 2026-07-15 · 975B（41B 激活） | 多模态 base 模型，专为微调设计。Apache 2.0，支持 vLLM / SGLang / llama.cpp。 |
| [**Phi-5 Large**](https://huggingface.co/microsoft/phi-5) | ⭐ — | Microsoft | 2026-06-28 · 28B 稠密 | MMLU 88%，AIME 80%，24—32GB Mac 段最强纯推理模型。MIT 许可。 |
| [**MiniMax-M3**](https://huggingface.co/MiniMaxAI) | ⭐ — | MiniMax | 2026-06-01 · 未公布 | MSA 稀疏注意力，1M 上下文，frontier-adjacent 编程能力。 |
| [**Nemotron 3 Ultra**](https://huggingface.co/nvidia) | ⭐ — | NVIDIA | 2026 · 未公布 | 开源训练数据/配方/中间检查点，研究者首选。Apache 2.0。 |
| [**GPT-6.1 Terra**](https://www.theverge.com/ai-artificial-intelligence/1018854/gpt-6-1-terra-is-very-good-at-computer-use-openai-says) | ⭐ — | OpenAI | 2026-10-27 · 未公布 | 🆕 主打 **computer use**，官方称在电脑操作任务上表现优异；实测以约 **1 折价格**获得 Astra 级操作能力。同周 OpenAI 把编码工具重构为常驻助理 **Dots**。 |
| [**Kimi K3.1 Pro**](https://venturebeat.com/technology/moonshots-kimi-k3-1-pro-flirts-with-open-weights-leadership-amid-paid-influencer-scandal-allegations) | ⭐ — | 月之暗面 | 2026-10-27 · 3T / 1M 上下文 | 🆕 3T 级参数、100 万 token 上下文，编程 / 3D 创建 / 金融研究 / Agent 能力大幅跃升，Highspeed 版快 2—3 倍。**完整权重计划 11-04 发布**——先 API 后权重，已成开源惯例。 |
| [**Mistral Large 4「Le Chonk」**](https://techcrunch.com/2026/10/29/mistral-releases-weights-for-its-trillion-parameter-ai-model-targeting-cybersecurity/) | ⭐ — | Mistral AI | 2026-10-29 · 1.05T | 🆕 **万亿参数开放权重正式放出**，主攻网络安全场景，单任务成本较竞品低 **63%**，自称「中国以外最强开源模型」。**开源模型第一次把「安全」写进卖点。** |
| [**Gemini 4 Carbon**](https://www.theverge.com/tech/1021339/google-gemini-4-carbon-cybersecurity-frontier) | ⭐ — | Google | 2026-10-31 · 未公布 | 🆕 在更新、更难的基准上**重回世界第一**，网络安全防御显著跃升；但访问受限，事实知识幻觉率高于前代 Argon。 |

> 📌 **趋势判断（10 月下旬更新）**
>
> 1. **中国实验室已在原始开源能力上领跑**：智谱、深度求索、月之暗面、阿里、阶跃五家都有「对标闭源旗舰」的开放权重。
> 2. **许可证两极分化**：MIT / Apache 2.0 仍主导（Top 10 中 9 个），但**「开放权重 + 商用限制」的新许可证在变多**（FLUX 3 Klein 就对中小企业限定了免费商用范围）。
> 3. **MoE 极端稀疏成主流**：GLM-5.2 仅 5.4% 参数激活，DeepSeek-V4 49B/1.6T，Step 5 27B/600B。
> 4. **「周更」带来新问题**：模型换代快于评测周期，社区横评的可比性在下降——**选型要开始看「版本稳定性」而不只是「榜一」**。

### 二十一、🏗️ 基础框架

| 框架 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**TensorFlow**](https://github.com/tensorflow/tensorflow) | ⭐ **202k** | C++ | tensorflow | Google出品的机器学习框架，深度学习领域的奠基者。 |
| [**Transformers**](https://github.com/huggingface/transformers) | ⭐ **169k** | Python | HuggingFace | HuggingFace核心库，提供10万+预训练模型的统一API。 |
| [**PyTorch**](https://github.com/pytorch/pytorch) | ⭐ **105k** | Python | pytorch | Meta出品的深度学习框架，学术界和AI研究的事实标准。 |
| [**FastAPI**](https://github.com/tiangolo/fastapi) | ⭐ **105k** | Python | tiangolo | Python高性能Web框架，AI应用后端的事实标准。 |
| [**Streamlit**](https://github.com/streamlit/streamlit) | ⭐ **46.3k** | Python | streamlit | 数据应用快速构建框架。 |
| [**Ray**](https://github.com/ray-project/ray) | ⭐ **44.3k** | Python | ray-project | 分布式AI计算引擎。 |
| [**Gradio**](https://github.com/gradio-app/gradio) | ⭐ **44k** | Python | gradio-app | HuggingFace出品，快速搭建ML模型Demo。 |
| [**JAX**](https://github.com/jax-ml/jax) | ⭐ **36.6k** | Python | jax-ml | Google出品的高性能数值计算框架。 |
| [**NumPy**](https://github.com/numpy/numpy) | ⭐ **33.4k** | Python | numpy | Python科学计算基础库。 |

### 二十二、🤖 具身智能 / 机器人（🆕 2026 年 10 月新入列赛道）

> 10 月上旬，全栈开源人形机器人与开源「机器人大脑」同周出现；10 月中旬，**世界模型**又集体开源。三件事连起来看：**Agent 的开源方法论（Skills、记忆、沙箱、评测）正在整体平移进物理世界**，而世界模型就是这套方法论的地基——机器人要先能在「脑内预演」，才谈得上规划。

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**UnifoLM-WLA-1.0**](https://blog.csdn.net/qq_39427511/article/details/167072184) | ⭐ 新项目 | 6B VLA 模型 | 宇树科技 | **2026 年 10 月初发布**。宇树开源的 6B 参数**全身 VLA（Vision-Language-Action）模型**，基于 Qwen3-VL 构建，覆盖 64 项机器人任务——国产机器人头部厂商把「机器人大脑」放上开源货架。 |
| [**RoboParty RP1**](https://blog.csdn.net/qq_39427511/article/details/167072184) | ⭐ 新项目 | 全栈开源人形 | RoboParty | **2026 年 10 月初亮相**。全栈开源双足人形机器人：峰值扭矩 160 N·m，搭载 PartyOS 与无监督强化学习方案。从硬件图纸到训练配方全开源，个人实验室造人形的门槛被击穿。 |
| [**VAST EdenLive**](https://www.qbitai.com/2026/10/504136.html) | ⭐ 新项目 | 实时世界模型 | VAST | 🆕 **10 月 18—19 日发布并开源**。实时世界模型，**首次在实时生成前提下同时做到「任意参考输入 + 任意画风 + 长时连续运行」**——世界模型从「能生成一段」走到「能持续跑」。 |
| [**优必选 Thinker-WM**](https://www.qbitai.com/2026/10/503843.html) | ⭐ 新项目 | 具身世界模型 | 优必选 | 🆕 多模态统一具身世界模型，与 EdenLive 同日开源。定位是机器人「预演引擎」：在动作执行前先在模型里推演结果。 |
| [**清华 GeoPT**](https://www.qbitai.com/2026/10/503880.html) | ⭐ 新项目 | 物理世界模型 | 清华大学 | 🆕 **物理世界模型**，同日开源。与前两者互补——EdenLive 管「视觉上像」，Thinker-WM 管「动作上对」，GeoPT 管「物理上成立」。 |
| [**小米 21 自由度灵巧手**](https://www.qbitai.com/2026/10/505600.html) | ⭐ 新项目 | 仿生灵巧手 | 小米 | 🆕 **10-27 披露**。21 自由度仿生灵巧手，基于 **1827 个工厂 SOP** 验证——灵巧手从实验室 demo 走向产线可制造。 |
| [**启元 PrimeSim**](https://www.qbitai.com/2026/10/506866.html) | ⭐ 新项目 | 世界模型 | 启元 | 🆕 **10-31 登顶两大机器人权威榜单**。世界模型直接用于机器人策略训练与仿真，与「世界模型指导芯片设计（NPU 700 TOPS）」同周出现。 |
| [**人形机器人全套图纸**](https://www.qbitai.com/2026/10/505865.html) | ⭐ 新项目 | 全栈开源 | 开源社区 | 🆕 **10-27 开源**：从机械结构、关节到运动控制算法的全栈方案，可下载自造。与 RoboParty RP1 一起把「造人形」的门槛打到个人实验室级。 |

> 💰 **资本侧信号**：FieldAI 以 **100 亿估值融资 7 亿美元**。当「世界模型 + VLA + 全栈开源硬件」三件套同时齐备，具身智能的开源生态就具备了复现条件——这是下一个十年入口的样子。

### 二十三、📚 AI 学习教程 / 路线图（🆕 2026 年 11 月新入列赛道）

> 这一节补的是「从 0 到能跑」的那条路。工具天天换代，但**开源书、体系课、动手实现、Cookbook** 这几类内容反而越来越稳——因为它们沉淀的是「怎么想」，不是「怎么调 API」。
>
> 四个判断：① **「开源书」是 2026 年最被低估的一类**——李博杰《深入理解 AI Agent》56.9k、上海交大《动手学大模型》58.8k，星数已经和一线框架持平；② 中文教程不再是「翻译版」，Datawhale《从零开始构建智能体》85.6k，比微软的 Agent 课（78.7k）还高；③ 头部 Cookbook 的星数（awesome-llm-apps 14.4 万）超过大多数框架本体——**「给我能跑的示例」比「给我一套抽象」更刚需**；④ 从零实现类（LLMs-from-scratch 10.8 万）持续上涨，说明「懂原理」在 Agent 时代重新变成竞争力。

#### 📖 开源书（成书的系统教程）

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**dive-into-llms**](https://github.com/Lordog/dive-into-llms) | ⭐ **60.1k** | Jupyter Notebook | 上海交大 / Lordog | 《动手学大模型 Dive into LLMs》系列编程实践教程：从 Prompt、RAG、Agent 到微调、量化、对齐，每章一个可跑 notebook。**中文圈最像「课程 + 实验」的一本。** |
| [**ai-agent-book**](https://github.com/bojieli/ai-agent-book) | ⭐ **57.9k** | Python | 李博杰 | 《深入理解 AI Agent：设计原理与工程实践》开源主仓库：**全书正文 + 编译版 PDF + 按章配套代码**。少见的「原理讲透 + 代码能跑」的 Agent 系统书，覆盖上下文工程、工具调用、记忆、多 Agent 与评测。 |
| [**Hands-On-Large-Language-Models**](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) | ⭐ **30.1k** | Jupyter Notebook | HandsOnLLM | O'Reilly《Hands-On Large Language Models》官方代码库，从 tokenizer 一路做到 RAG 与多模态。 |
| [**ml-engineering**](https://github.com/stas00/ml-engineering) | ⭐ **19.7k** | Python | Stas Bekman | 《Machine Learning Engineering》开放书：GPU 选型、显存估算、分布式训练、推理调优——**工程细节最硬的一本**。 |

#### 🎓 体系课与路线图

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**generative-ai-for-beginners**](https://github.com/microsoft/generative-ai-for-beginners) | ⭐ **123k** | Jupyter Notebook | Microsoft | **21 节课**从 0 到能搭生成式 AI 应用：Prompt、RAG、微调、Agent、负责任 AI 全覆盖，配代码、视频与作业。英文世界最常被推荐的入门课。 |
| [**ML-For-Beginners**](https://github.com/microsoft/ML-For-Beginners) | ⭐ **92.2k** | Jupyter Notebook | Microsoft | **12 周 26 课 52 个测验**的经典机器学习课，Scikit-learn 为主线，适合打地基。 |
| [**llm-course**](https://github.com/mlabonne/llm-course) | ⭐ **85.1k** | Jupyter Notebook | Maxime Labonne | 带**路线图 + Colab** 的 LLM 课程：从数学基础 → 微调 → 量化 → 部署，一条线走完，最适合「知道自己要补哪块」的人。 |
| [**d2l-zh**](https://github.com/d2l-ai/d2l-zh) | ⭐ **82.5k** | Python | 李沐 / D2L.AI | 《动手学深度学习》中文版——可运行、可讨论，被 70 多个国家 500 多所大学采用。**中文深度学习教材的事实标准。** |
| [**ai-agents-for-beginners**](https://github.com/microsoft/ai-agents-for-beginners) | ⭐ **79.5k** | Jupyter Notebook | Microsoft | **18 节课**教怎么构建 AI Agent：工具调用、多 Agent 协作、记忆、评估与生产化。 |
| [**AI-For-Beginners**](https://github.com/microsoft/AI-For-Beginners) | ⭐ **70.7k** | Jupyter Notebook | Microsoft | 12 周 24 节课的 AI 通识课，偏概念、历史与伦理，适合零基础转行先建立地图。 |
| [**agents-course**](https://github.com/huggingface/agents-course) | ⭐ **34.8k** | Jupyter Notebook | HuggingFace | 官方 Agent 课程，同一套概念用 **smolagents / LlamaIndex / LangGraph** 三种实现对照讲，理解框架差异的最快路径。 |
| [**courses**](https://github.com/anthropics/courses) | ⭐ **23k** | Jupyter Notebook | Anthropic | Anthropic 官方课程合集：Prompt 工程、工具调用、Agent 评测。 |
| [**ML-YouTube-Courses**](https://github.com/dair-ai/ML-YouTube-Courses) | ⭐ **17.5k** | Markdown | DAIR.AI | 把全网优质 ML / AI 视频课整理成索引——省掉「学什么」的决策成本。 |
| [**mlops-zoomcamp**](https://github.com/DataTalksClub/mlops-zoomcamp) | ⭐ **15.6k** | Jupyter Notebook | DataTalks.Club | 免费 MLOps 训练营：实验跟踪、编排、部署、监控，从 notebook 到生产的那一段。 |
| [**smol-course**](https://github.com/huggingface/smol-course) | ⭐ **6.8k** | Jupyter Notebook | HuggingFace | 小模型对齐课程：SFT、DPO、评测一条龙，适合只有单卡的人。 |
| [**deep-rl-class**](https://github.com/huggingface/deep-rl-class) | ⭐ **5.1k** | Jupyter Notebook | HuggingFace | 深度强化学习课程，配套 Unity ML-Agents 环境，理论与可玩 demo 并行。 |

#### 🛠️ 从零实现（动手造一遍）

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**LLMs-from-scratch**](https://github.com/rasbt/LLMs-from-scratch) | ⭐ **108k** | Jupyter Notebook | Sebastian Raschka | 用 PyTorch **从零实现一个 ChatGPT 式 LLM**，逐章对应《Build a Large Language Model (From Scratch)》。2026 年最推荐的「懂原理」入口。 |
| [**nanoGPT**](https://github.com/karpathy/nanoGPT) | ⭐ **64.7k** | Python | Andrej Karpathy | 最简单最快的 GPT 训练 / 微调仓库，几百行讲清 Transformer 训练全流程。**读一遍胜过十篇综述。** |
| [**Made-With-ML**](https://github.com/GokuMohandas/Made-With-ML) | ⭐ **50k** | Jupyter Notebook | Goku Mohandas | 生产级 ML 全流程课：数据校验、训练、部署、监控、迭代，强调「能上线」而不是「能跑分」。 |
| [**happy-llm**](https://github.com/datawhalechina/happy-llm) | ⭐ **34.9k** | Jupyter Notebook | Datawhale | 《从零开始构建大模型》中文版：分词、注意力、预训练、SFT、RLHF 全部手写一遍。 |
| [**llm.c**](https://github.com/karpathy/llm.c) | ⭐ **31.5k** | CUDA | Andrej Karpathy | 用**纯 C / CUDA** 训练 LLM，把框架黑盒拆到寄存器级别。想搞懂「显存去哪了」就看它。 |
| [**fastbook**](https://github.com/fastai/fastbook) | ⭐ **25.5k** | Jupyter Notebook | fast.ai | 《Deep Learning for Coders》配套 notebook，自顶向下教学法的代表作——先能跑，再讲原理。 |
| [**llm-action**](https://github.com/liguodongiot/llm-action) | ⭐ **25.3k** | Python | liguodongiot | 大模型工程化实战合集：训练、推理、量化、RAG、Agent 落地，偏「踩坑记录」而非教科书。 |
| [**nn-zero-to-hero**](https://github.com/karpathy/nn-zero-to-hero) | ⭐ **25.6k** | Jupyter Notebook | Andrej Karpathy | 神经网络零基础系列（配套视频）：从 micrograd 一路写到 GPT。 |
| [**micrograd**](https://github.com/karpathy/micrograd) | ⭐ **18.9k** | Jupyter Notebook | Andrej Karpathy | **100 行**的标量自动求导引擎 + 神经网络库，理解反向传播的最佳起点。 |
| [**KuiperInfer**](https://github.com/zjhellofss/KuiperInfer) | ⭐ **3.5k** | C++ | zjhellofss | 从零实现一个高性能深度学习推理库（支持 Llama2 / UNet / YOLOv5），**校招项目里最硬的一个**，配套逐行讲解。 |
| [**Cortex**](https://github.com/qibin0506/Cortex) | ⭐ **2.7k** | Python | qibin0506 | 从零构建大模型：预训练 → SFT → RLHF 的完整实践，代码量克制，适合跟着跑一遍全流程。 |

#### 🧪 Cookbook 与实战合集（照着搭）

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**awesome-llm-apps**](https://github.com/Shubhamsaboo/awesome-llm-apps) | ⭐ **145k** | Python | Shubham Saboo | **100+ 可直接跑的 AI Agent / RAG 应用合集**。星数超过大多数框架本体——「给我能跑的示例」比「给我一套抽象」更刚需。 |
| [**Prompt-Engineering-Guide**](https://github.com/dair-ai/Prompt-Engineering-Guide) | ⭐ **80k** | Jupyter Notebook | DAIR.AI | 提示工程指南：技术、论文、讲义、notebook 一网打尽，仍是这个领域引用最多的索引。 |
| [**openai-cookbook**](https://github.com/openai/openai-cookbook) | ⭐ **77.1k** | Jupyter Notebook | OpenAI | 官方 API 示例与最佳实践：Prompt、函数调用、RAG、评测、结构化输出。 |
| [**claude-cookbooks**](https://github.com/anthropics/claude-cookbooks) | ⭐ **54.6k** | Jupyter Notebook | Anthropic | Claude 官方 notebook 合集（原 anthropic-cookbook），工具调用与 Agent 模式最全的一份。 |
| [**awesome-ai-agents**](https://github.com/e2b-dev/awesome-ai-agents) | ⭐ **30.9k** | Markdown | E2B | 自主 Agent 清单，按用途分类——做选型调研时比搜索更快。 |
| [**RAG_Techniques**](https://github.com/NirDiamant/RAG_Techniques) | ⭐ **30.3k** | Jupyter Notebook | Nir Diamant | **30+ 种 RAG 进阶技巧**，每种都有可运行实现：分块、重排、混合检索、GraphRAG、Agentic RAG。 |
| [**GenAI_Agents**](https://github.com/NirDiamant/GenAI_Agents) | ⭐ **24.9k** | Jupyter Notebook | Nir Diamant | 50+ 生成式 AI Agent 教程与实现，从最简单的单 Agent 到多 Agent 协作渐进。 |
| [**cookbook（Gemini）**](https://github.com/google-gemini/cookbook) | ⭐ **17.9k** | Jupyter Notebook | Google | Gemini API 官方 cookbook：多模态、长上下文、函数调用示例。 |
| [**langchain-academy**](https://github.com/langchain-ai/langchain-academy) | ⭐ **3k** | Jupyter Notebook | LangChain | 官方 LangGraph 课程：从 state graph、持久化到 human-in-the-loop 与部署。 |

#### 🇨🇳 中文教程与社区

| 项目 | Stars | 语言 | 出品方 | 简介 |
| :--- | :---: | :---: | :--- | :--- |
| [**hello-agents**](https://github.com/datawhalechina/hello-agents) | ⭐ **86.9k** | Jupyter Notebook | Datawhale | 《从零开始构建智能体》——**中文世界目前最系统的 Agent 教程**，星数已超过微软的 Agent 课。 |
| [**paper-reading**](https://github.com/mli/paper-reading) | ⭐ **34.1k** | Python | 李沐 | 深度学习经典与新论文**逐段精读**，配套视频，中文圈读论文的最佳入口。 |
| [**self-llm**](https://github.com/datawhalechina/self-llm) | ⭐ **32.8k** | Jupyter Notebook | Datawhale | 《开源大模型食用指南》：Linux 环境下全参 / LoRA 微调 + 部署国内外开源模型，国内环境最实用的一份。 |
| [**llm-cookbook**](https://github.com/datawhalechina/llm-cookbook) | ⭐ **24.9k** | Jupyter Notebook | Datawhale | 吴恩达大模型系列课程的**中文版**，面向开发者，保留原课程的工程视角。 |
| [**leedl-tutorial**](https://github.com/datawhalechina/leedl-tutorial) | ⭐ **16.9k** | Jupyter Notebook | Datawhale | 《李宏毅深度学习教程》整理版，李宏毅本人推荐，中文入门最友好的讲义之一。 |
| [**so-large-lm**](https://github.com/datawhalechina/so-large-lm) | ⭐ **7.8k** | Markdown | Datawhale | 《大模型基础》：把 LLM 的基础知识写成一本可读的书，适合作为系统复习材料。 |
| [**CV**](https://github.com/AccumulateMore/CV) | ⭐ **24.3k** | Jupyter Notebook | AccumulateMore | 超级全面的深度学习笔记合集：土堆 PyTorch + 李沐《动手学深度学习》+ 吴恩达深度学习 + 大模型，**一份文档覆盖四门课**。 |
| [**ai-guide**](https://github.com/liyupi/ai-guide) | ⭐ **22.1k** | Markdown | 程序员鱼皮 | AI 资源大全 + Vibe Coding 零基础教程，含 OpenClaw 保姆级上手、大模型选型与提示词模板。**面向「想马上用起来」的开发者。** |
| [**llm-universe**](https://github.com/datawhalechina/llm-universe) | ⭐ **14.3k** | Jupyter Notebook | Datawhale | 面向小白开发者的大模型应用开发教程：API 调用 → RAG → 部署，配套在线阅读。 |
| [**ai-agents-from-zero**](https://github.com/didilili/ai-agents-from-zero) | ⭐ **6k** | Python | didilili | 「2026 最系统的 AI Agent 速成指南」：学习路径 + 实战项目 + 面试题，偏求职导向。 |
| [**yu-ai-agent**](https://github.com/liyupi/yu-ai-agent) | ⭐ **2.8k** | Java | 程序员鱼皮 | 基于 Spring Boot 3 + Java 21 + Spring AI 的 AI 应用实战项目，**Java 后端转 AI 的落地样本**。 |
| [**yu-ai-code-mother**](https://github.com/liyupi/yu-ai-code-mother) | ⭐ **2k** | Java | 程序员鱼皮 | Spring Boot 3 + LangChain4j 的 AI 代码生成器全栈项目，含微服务拆分。 |
| [**hugging-multi-agent**](https://github.com/datawhalechina/hugging-multi-agent) | ⭐ **1.4k** | Jupyter Notebook | Datawhale | 基于 MetaGPT 的多智能体入门教程，半天能跑通一个协作案例。 |

> 🎯 **怎么用这一节（三条路线）**
>
> - **完全零基础**：AI-For-Beginners（建立地图）→ d2l-zh 或 ML-For-Beginners（打地基）→ ai-agents-for-beginners（转 Agent）。
> - **会写代码、想搞懂原理**：nanoGPT → micrograd → LLMs-from-scratch → llm.c（难度递增）；想直接啃 Agent 系统设计，读 **ai-agent-book**（原理 + 代码）。
> - **要马上做出东西**：awesome-llm-apps（找同类项目照抄）→ openai-cookbook / claude-cookbooks（查 API 用法）→ RAG_Techniques（补检索细节）。
> - **中文、想少踩环境坑**：hello-agents（Agent）→ dive-into-llms（动手实验）→ self-llm（微调部署）→ llm-cookbook（应用开发）。

## 📌 说明

1. ✅ **数据通过全网实时搜索 + GitHub API 获取**（采集截止 **2026-11-02**），综合 GitHub 日榜/周榜/月榜、YourTools 趋势榜、技术媒体（量子位、机器之心、VentureBeat、TechCrunch、The Verge、WIRED、MIT TR、Reuters）与每日 AI 研究简报等多源交叉验证。
2. 📚 覆盖 **23 大类别、449 条目**（去重后实时统计），涵盖 Agent 生态全链路（框架 → 技能 → 记忆 → 推理 → 安全 → 具身 → **学习教程**）。
3. 🔗 项目标题均内联 **GitHub / HuggingFace / 报道出处**链接。⚠️ 部分新上榜项目**暂未核实到官方仓库**，链接先指向报道出处，后续版本补正（如 Reflection Beam、MiMo-V2.6-Flash、Ternary-Bonsai-2、DeepInfer 等）。
4. 📏 **Star 口径说明**：星数于 **2026-11-03** 经 GitHub API 统一刷新（449 条中 417 条取得读数）。为保持表格整洁，日期标注不再逐条展示，**每条数据的精确采集时间记录在 `data/projects.json` 的 `stars_as_of` 字段**；本次未取到读数的条目沿用上一版数值。不同来源仍可能有小幅波动，数据仅供参考。
5. 🆕 标记为本次更新新增的项目或重大变更；⚠️ 标记为需要注意的风险（CVE、争议、口径存疑）。
6. 📐 **表格统一为 5 列**：项目类表为「项目 / Stars / 语言 / 出品方 / 简介」，模型表为「模型 / Stars / 出品方 / 发布 · 参数 / 简介」，目录与速览等功能表同样按 5 列组织。出品方取自项目官方仓库所属组织，非 GitHub 项目标注为「—」。
7. 🧹 **历次整理动作**：修复被空行切断的表格、删除 43 行完全重复的表格行、合并跨章节重复条目、修正梯队错位、全篇统一 5 列并按 Star 降序排列、补齐目录与「选型四问」；本轮新增 22 个条目并刷新头部项目 Star。
8. 🔍 **本轮查漏补缺**：以 [awesome-LLM-resources · 智能体 Agents](https://github.com/WangRongsheng/awesome-LLM-resources#智能体-agents) 为对照清单逐条比对，补入 **38 个此前缺失的项目**（含 pi 11.96 万、AutoGen 6.17 万、Coze Studio 2.18 万、agent-zero 1.97 万、rowboat 1.81 万、Qwen-Agent 1.72 万等），Star 与语言均通过 **GitHub API（2026-11-03）实时读取**。该清单中的 `AgentScope` 重复出现两次（本表只保留一条）；`AgentsMesh`、`BitFun`、`meta-llama/llama-agentic-system` 三个仓库当前无法解析（404 / 未公开），暂未收录。
9. 🗂️ **结构化数据**：`data/projects.json` 由 `scripts/extract.mjs` 从本文抽取（449 条，含星数、采集日期、语言、分类、梯队），供检索与自动化脚本使用；README 仍是唯一事实来源，数据文件仅为派生索引。
10. *整理不易，如有遗漏或错误欢迎指出 🙏*

## 🤝 贡献指南

欢迎补充遗漏项目、修正失效链接或刷新 Star 数据。

**提 Issue**：链接 404、数据错误、分类不当，请附项目名与可验证的证据链接。

**提 PR**：

1. 沿用现有 5 列表格格式新增行，保持 Star 降序排列；
2. 星数直接填写，如 `⭐ 12.3k`，**不写日期标注**——采集时间统一记录在 `data/projects.json` 的 `stars_as_of` 字段；未取到新读数则保留旧值；
3. 简介控制在 80 字内，突出「一句话定位 + 关键差异」，避免罗列功能清单。

**收录标准**（当前建议值，可按社区反馈调整）：

- 开源项目，或权重可公开下载；
- Star ≥ 1k，或虽未达标但属于被权威媒体报道的新兴方向；
- 近 6 个月有提交记录，且有可用的 README / 文档。

> 信息不全时宁可标注「待核实」，也不要凭推测填写——这份清单的价值在于可查证，而不在于条数多。

## 📄 许可证

本项目（文档、表格与图表）采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可协议，完整条款见 [LICENSE](LICENSE)。

- ✅ **允许**：自由转载、摘编、二次整理与商业使用。
- 📌 **须署名**：注明来源与链接，并说明是否做过修改。
- ⚠️ **第三方内容**：文中引用的项目名称、商标、Star 数据及简介归各自所有者，本仓库仅作汇总与评述，不主张其权利；转载时请一并遵守原项目许可证。

建议署名格式：`Agent Nexus（https://github.com/cosolar/agent-nexus），CC BY 4.0`
