# Job Radar

> 把「每天翻招聘网站」变成一条可复现的流水线：**采集 → 硬过滤 → 逐条核验 → 去重出报**。
> An agent skill that builds a filtered, verified, deduplicated daily job report from Chinese job boards.

[中文](#中文) · [English](#english)

---

## 中文

### 它解决什么问题

中文招聘站（BOSS直聘、智联、猎聘…）对自动化极不友好：一半是 SPA 空壳，一半有 WAF 和登录墙，剩下的关键词匹配还很脏（搜「食品研发」会混进厨师和后厨）。

大多数「AI 找工作」的做法是让模型直接总结搜索页 —— 结果是编造公司、编造薪资、链接打不开。

Job Radar 反过来做：**先用代码把能读的数据读下来，用规则淘汰掉 80%，只对活下来的少数逐条打开详情页核验**，最后输出的每一条都带可点开的原始链接和页面原文 JD。

### 长什么样

```
【深圳麦克韦尔科技（smoore）】深圳·宝安·西乡
岗位：调香助理工程师（MJ005384）
薪资：16-20K·16薪（达标）
企业：已上市｜10000人以上｜智能硬件
JD：协助调香师完成配方小样制作、实验操作及测试；参与感官评测、品吸…
    任职要求：「食品科学与工程、香精香料技术、化学工程等相关专业优先」
投递：https://www.zhipin.com/job_detail/...
```

想看的字段也全在：`weekend`（双休/大小周/单休）、`travel`（出差/驻场/外派）、`shift`（倒班/夜班）——因为这三项是「双休、不出差、不倒班」这类需求的唯一可靠来源。

### 快速开始

```bash
git clone https://github.com/Rsaaaa9/job-radar.git
cp config/profile.example.json config/profile.json
# 改 config/profile.json：城市、关键词、薪资下限、公司规模、加分权重
```

然后在你的 agent 里让它读 `SKILL.md`，说一句：

> 按 job-radar 帮我跑今天的岗位日报

### 数据源实测（2026-11）

| 来源 | 状态 | 说明 |
|---|---|---|
| 智联招聘 | ✅ | 列表页 + 详情页都是 SSR，主力来源 |
| BOSS直聘 | ✅ 有条件 | 需 Edge + OpenCLI 扩展 + 登录态；只读、串行、低频 |
| 腾讯社招 API | ✅ | 公开 JSON，含 JD 全文 |
| 达能中国（TalentBrew） | ✅ | SSR，可读 63 条职位 |
| 猎聘 / 前程无忧 / 应届生网 / 牛客 / 实习僧 | ❌ | WAF、登录墙、纯 JS 空壳 |
| 高校就业网（jysd 等） | ❌ | 多数跳统一认证 |
| 企业官网（玛氏/雀巢/伊利/蒙牛/大疆/影石/华为…） | ❌ | 清一色 SPA ATS（北森/Moka/飞书/Workday/Phenom） |

详细证据与 URL 模板见 [`references/sources.md`](references/sources.md)。

### 设计上的几条硬规矩

1. **没有链接的岗位不许出现在报告里。**
2. **JD 必须是页面原文**，模型只做压缩，不许改写关键条件。
3. **页面没写双休就不许写双休**，标 `⚠️` 让用户自己确认。
4. **通道挂了要写「未覆盖」**，不许假装搜过。
5. **只读**：不自动打招呼、不自动投递。

### 目录

```
SKILL.md                      # 给 agent 的指令（入口）
config/profile.example.json   # 搜索配置模板
scripts/boss-sweep.ps1        # BOSS 批量抓取
scripts/boss-daemon.ps1       # opencli daemon 守护（支持停止文件）
references/sources.md         # 数据源矩阵 + 坑
references/pipeline.md        # 编排骨架（含 8 并发上限的处理）
examples/report.example.md    # 报告样式
```

### License

MIT

---

## English

**Job Radar** is an agent skill that turns "browse job boards every day" into a reproducible pipeline:
collect → hard-filter → verify each shortlisted posting → dedupe → report.

The premise is boring but important: Chinese job boards are hostile to automation (SPA shells, WAFs, login walls) and their keyword matching is noisy. Most "AI job hunting" attempts end with hallucinated companies and dead links. Job Radar instead spends its budget on **opening the few postings that survived code-level filtering**, so every reported job carries a live link and a quote-backed JD.

### What you get

- A daily report where every entry has: company · district · title · salary · company type/size · JD excerpt · link
- Three fields that actually decide job quality: `weekend`, `travel`, `shift` — extracted from the posting text, never assumed
- A dedupe store so the same posting is not pushed twice within 30 days

### Quick start

```bash
git clone https://github.com/Rsaaaa9/job-radar.git
cp config/profile.example.json config/profile.json   # edit it
```

Then ask your agent: *"run the job-radar daily report"*. See `SKILL.md` for the procedure.

### Source support

Zhaopin (SSR, primary) · BOSS Zhipin (via OpenCLI browser bridge, read-only, low frequency) · Tencent careers API · Danone TalentBrew.
Liepin, 51job, Yingjiesheng, Nowcoder, Shixiseng and most corporate ATS are **structurally unscrapeable** — documented with evidence in `references/sources.md` rather than hand-waved.

### Guardrails

Read-only actions only. No auto-greeting, no auto-applying. Missing data is reported as missing, never invented.

### License

MIT
