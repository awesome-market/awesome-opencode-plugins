# 大学导师数据库 · university-advisor-database

> 把散落在几百个院系页面里的教职人员信息，变成**可核验、可追溯、可续跑**的结构化数据。

一个给 AI Agent 用的 Skill：从大学官网采集导师信息，按学院 / 院系逐层核验身份、职称、研究方向，产出带证据的 Excel / CSV 与覆盖日志。

**Python 3.10+，零第三方依赖。**

---

## 为什么做这个

留学申请选导师时，最难的不是找到人，是**确认这个人现在还在、还是教授、还带学生**。

这些信息分散在各学院的 directory 页、个人主页、专家库里，分页方式各不相同，几百个系要一个个翻。更麻烦的是，如果直接让 AI 去"整理一下"，它会给出看起来很真、但来源不明、甚至把助理教授写成教授的表格——而这张表会被拿去发邮件。

**所以这个项目的核心不是爬虫，是约束。**

它把「AI 采集」这件容易失控的事，拆成三个必须同时成立的条件：

| 约束 | 做法 |
|---|---|
| **每条数据必须能指回原文** | 姓名、职称、单位、研究方向各自绑定 `{url, excerpt}`，摘录必须是本次实际读取的原文，不能是 Agent 自己的总结 |
| **不确定必须显式标注** | 三态判定：`qualified` / `needs_verification` / `rejected`。访问失败、字段缺失、官网冲突一律进待核验，**unknown 不等于不合格** |
| **进度必须可续跑** | SQLite 台账按院系小批次事务提交，中断不丢、blocked 不计入 completed、抽样不能宣称全量完成 |

一句话：**它不让 AI 自由发挥，而是给 AI 一套必须遵守的记账规则。**

---

## 三个容易被搞混的事实

这个项目里最费劲的部分，是分清几组经常被混为一谈的概念：

- **教职身份**（是不是 Professor） ≠ **终身轨**（tenured / tenure-track，需官方轨制证据） ≠ **博士指导资格**（需 graduate faculty 证据） ≠ **当前招生状态**（需明确说明，且带日期）
- **英国 Lecturer 不是美国 Assistant Professor**，**中国"研究员"不自动等于 Professor**，**Dr 是学位称呼，Chair 是行政职责**——都不构成职级证据
- **目录人数、候选数、合格人数** 是三个不同指标，不能用"每个系必须凑够 8 人"去逼出虚假记录

职称模式三档，显式切换、记录在案：

| 模式 | 收录范围 | 适用 |
|---|---|---|
| `professor-only` | 现任教授 / 副教授，排除助理教授及兼职、访问、名誉、退休、纯教学/纯临床轨 | 默认 |
| `tenure-track` | 含 Assistant / Associate / Full，但必须有官方轨制证据 | 需要确认终身轨时 |
| `research-supervisor` | 宽口径，允许有明确科研方向的 Lecturer / Reader / Research Fellow | 留学检索 |

---

## 用法

```bash
# 1. 初始化台账
python scripts/faculty_store.py init \
  --db run/faculty.sqlite --config run/config.json

# 2. 登记院系队列
python scripts/faculty_store.py unit \
  --db run/faculty.sqlite --input run/units.json

# 3. 分批写入带证据的记录
python scripts/faculty_store.py record \
  --db run/faculty.sqlite --input run/batch.json

# 4. 导出 Excel / CSV
python scripts/faculty_store.py export \
  --db run/faculty.sqlite --out run/exports
```

作为 AI Skill 使用时，直接把 `SKILL.md` 放进 skills 目录（例如 `~/.codex/skills/` 或 `~/.claude/skills/`），Agent 会按其中的流程执行：建队列 → 发现目录 → 逐页核验 → 落盘 → 导出。

---

## 产出

`export` 生成一个多 sheet 的 Excel，每张表回答一个不同的问题：

| Sheet | 作用 |
|---|---|
| `Global_Master` | 主表，固定六列：`Name, Department Name, University, Research Field, Profile URL, School` |
| `Final_Qualified` | 有充分证据、符合当前职称模式的记录 |
| `Needs_Verification` | 访问失败 / 字段不足 / 官网冲突，保留可重试 URL |
| `Rejected_With_Reasons` | 有证据不符合范围，附原因 |
| `School_Run_Log` | 每个院系的处理状态与分页终止依据 |
| `Remaining_Schools_Queue` | 还没做完的部分 |
| `Source_Audit` | 真实职称、身份类别、完整证据 JSON |
| `Reverification_Log` | 合格条目的重新核验失败记录 |

同时输出带 UTF-8 BOM 的真实 CSV（用 CSV writer 转义，不是把表格改名），以及 `summary.json`。

**覆盖评估只针对已核实的范围**：区分"学院入口是否发现完整""已发现单位处理率""研究字段完整率"，未知分母写 `unknown`。已发现单位的处理率不是全校教授覆盖率。

---

## 脚本不做什么

这一点很重要，因为市面上很多"一键爬虫"正是在这里出问题：

- ❌ **不访问网络**。`faculty_store.py` 只操作显式指定的本地文件
- ❌ **不写 Notion**。同步需要单独授权，旧脚本里的 token 和 DB ID 不构成授权
- ❌ **不判断内容真假**。它能校验证据字段存在、URL 域名是否官方、分页是否声明完成，但**不能证明原文真实、姓名属于该人、状态仍然有效**
- ❌ **不自动翻译**。中文视图必须由本次任务补齐译文，缺失值退回原文而不是伪造

网页读取、职称理解、证据判断，仍然由 Agent 完成。**这个脚本是台账，不是爬虫。**

---

## 反爬与稳健性

- 官方域名按 hostname 精确匹配 + 子域边界匹配，重定向后重新校验
- HTTP 200 也可能是登录页、验证码或错误模板 —— 必须校验页面类型
- 瞬时故障有限重试，429 尊重 `Retry-After`，反复失败记为 `blocked` 并转向其他院系
- 去重基于核验后的 canonical profile URL，保留 `id` / `uid` 等身份参数，只剥 `utm_*` / `gclid` / `fbclid`；**不按姓名去重**，不猜测不同 URL 是同一人

---

## 目录

```
.
├── SKILL.md                        # Agent 执行规范（主文件）
├── agents/openai.yaml              # Agent 配置
├── references/
│   ├── schema-and-rules.md         # 字段定义与职称判定矩阵
│   ├── store-protocol.md           # 台账 CLI 与输入输出格式
│   ├── crawler-adaptation.md       # 动态页面、分页、重试的处理方式
│   ├── github-research.md          # 用 GitHub 检索相关项目的思路
│   └── notion-adapter.md           # 可选的 Notion 同步
└── scripts/
    └── faculty_store.py            # 456 行，纯标准库离线台账
```

---

## 声明

仓库内**不含任何真实学校数据、导师姓名、邮箱或个人信息**。所有示例（Example University、Example Person）均为虚构测试数据，不计入任何成果。

Notion 同步为可选项，需单独授权；仓库内无任何凭据、token 或数据库 ID。

---

## License

MIT
