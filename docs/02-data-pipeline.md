# 02 数据采集与快照

## 数据源

| 源 | 用途 | 成本 | 方式 |
|---|---|---|---|
| `github.com/trending` | 发现当日热门仓库（各语言） | 无 API 成本 | 抓 HTML，解析仓库名/描述/语言/今日 Star |
| GitHub Search API | 发现新晋候选（按创建时间 + Star 数过滤） | 30 req/min（认证） | REST `search/repositories` |
| GitHub GraphQL API | 批量读取 watchlist 仓库的 Star/Fork/推送时间 | 5000 points/hr | `nodes()` / `repository()` 批量别名查询 |

原则：**Trending 负责"发现"，GraphQL 负责"计量"**。Search API 只用于补充新仓库候选。

## 候选仓库发现（每日 Discovery）

每次运行抓取并合并以下来源，去重后得到候选集：

1. **Trending 页面**：抓 `https://github.com/trending`（必要时按 `?since=daily` 及几个主要语言页），取每仓库的 `owner/name`、简介、语言、今日 Star 增长。
2. **新仓库搜索**：Search API 查询 `created:>{90天前} stars:>20 sort=stars`（对齐新榜口径），取前 1–2 页，补充新榜候选。
3. **老仓库活跃搜索**（`search_surge`）：Search API 按 star 分段查询 `created:<{90天前} stars:{lo}..{hi} pushed:>{7天前}`（20–300 / 300–1000 / 1000–5000 三段，各取 1 页 ≈ 300 候选/次）。近似"trending 缺位时的老仓库爆量"发现——召回靠 `pushed` 活跃度过滤，是否真在涨由每日快照 delta 判定，误报由 14 天零增长驱逐清理。
4. **存量 watchlist**：上一轮快照中所有在榜/接近在榜的仓库继续跟踪。

候选集与 watchlist 合并后，**按规则裁剪到上限 10000 个**（`MAX_WATCH`，`--max-repos` 可调）。**淘汰规则**（超限时按此顺序剔除）：本轮非 Trending 命中且近 14 天 Star 零/负增长的仓库按 Star 升序优先出局；仍超限则剔除 Star 最低者。

### Watchlist 冷启动（首次运行）

`watchlist.json` 不存在或为空时，collect 进入初始化模式，额外执行：

- Search API `sort=stars` 多页拉取高 Star 仓库（如 `stars:>2000`，每页 100，取前 ~1000 条）——保证总榜/存量榜有足够的高基数样本；
- Search API `created:>{90天前} stars:>20 sort=stars` 拉取新仓库候选（对齐新榜口径）；
- Trending 页面全量候选。

初始化后 watchlist 一次性填充至上限（按 Star 降序截断），此后走常规增量更新。注意 **Search API 单查询最多返回 1000 条**（10 页 × 100），故"90 天新仓库"候选实际只能覆盖其中 Star 最高的 ~1000 个——新榜口径是"跟踪集内"排名，README 需注明。

## 快照（Snapshot）

**分级刷新**：每 run 只对"热集"调 API——本轮候选（trending/search 命中）+ 从未拉取 + `last_fetch` 距今 ≥ `TRR_COLD_DAYS`（默认 3 天，env 可调）的长尾仓。其余冷仓**整行复用上份快照**（stars..prs_merged 全部 15 字段带回），快照行数保持全集稳定。GraphQL ~1pt/仓 → 10k 跟踪 ≈ ~3k pts/run，单 token 预算放得下；冷仓元数据文件不被带回行覆写（`pushed_at`/`description` 缺失则跳过）。每次运行生成一个带 UTC 时间戳的快照文件。

### 存储格式

```
data/
  snapshots/
    2026-11-08T02.json    # UTC 02:00 那次运行（≈北京时间 10:00）
    2026-11-08T14.json    # UTC 14:00 那次运行（≈北京时间 22:00，当日"收盘"）
    ...
  watchlist.json        # 当前跟踪列表（含首次发现日期、历史最佳排名等元数据）
```

文件名 `YYYY-MM-DDTHH.json` 按 **UTC 小时**命名；一天可有多份（每日 2 次运行）。`rank.py` 按**北京时间（Asia/Shanghai）自然日**分组，每天取当天最后一次快照作为该日"收盘值"——日/周/月窗口一律基于收盘值差分，与快照频率解耦。

`data/snapshots/YYYY-MM-DDTHH.json` 内容（紧凑数组格式，减少体积）：

```json
{
  "date": "2026-11-08T14",
  "run_at": "2026-11-08T14:03:12Z",
  "repos": [
    ["owner/name", 12345, 678, 901, 34, 56, 7, "2026-01-01T00:00:00Z", "Python", false, false],
    ...
  ],
  "errors": [["owner/gone-repo", "not_found"]]
}
```

字段顺序固定（16 列）：`full_name, stars, forks, watchers, issues_total, prs_total, releases_total, created_at, language, is_fork, is_archived, issues_open, issues_closed, prs_open, prs_closed, prs_merged`。
后 5 列（状态拆分）为追加列——11 列的旧快照按缺失处理（消费端读取时越界即 null）。
`errors` 为可选字段，记录当次拉取失败的仓库及原因。

（watchers/issues/prs/releases 对齐同类榜单站的数据模型，前端元信息行对非 null 字段渲染对应图标计数；扩展字段仅 UTC 14:00 运行填充，其他时刻为 `null`——见下方"拉取方式"。GraphQL 中 issues/pullRequests 分列；REST `open_issues_count` 含两者。）

仓库级低频元数据（description、topics、homepage、pushed_at、updated_at）不逐日重复存储，放 `data/repos/{owner}__{name}.json` 按需缓存，GraphQL 返回值变化时更新；扩展 pass 另写 `detail` 键（avatar、license、discussions 计数、hot issues、最新 discussions、latestRelease、完整 README），非扩展运行沿用文件内已有值。`rank.py` 将 description/homepage 等**内联合并进 `site/data` 条目**，并把 meta+detail+完整历史序列生成 `site/data/repos/{owner}__{name}.json` 供详情页使用。`site/data/**` 整棵树随后由 `pack_data.py` 打成单个 `site-data.db`（KV blob 表）推给 api-site——前端水合改从 `api-site.zhuikan.com/data/<path>` 取，Pages 部署包不再携带 data/（文件数上限约束，见 05-automation）。

序列需保留 **≥35 天**以支持月榜窗口；`rank.py` 从全部快照重建每仓库的日序列。

### 拉取方式

- **GraphQL 批量**（主力，**两档抓取**）：
  - **核心字段**（每次运行）：`stargazerCount / forkCount / isFork / isArchived / createdAt / pushedAt / updatedAt / description / homepageUrl / primaryLanguage`——纯标量+小连接，batch=50 实测 ~2.5s/44 仓库，2000 仓库约 40 请求 ~100s。
  - **扩展字段**（每日一次，UTC 14:00"收盘"运行）：`watchers / repositoryTopics / issues / pullRequests / releases` 的 `totalCount`，以及 issues/PR 的状态拆分计数（`issues OPEN/CLOSED`、`pullRequests OPEN/CLOSED/MERGED` 的 `totalCount`），外加**详情对象**——`owner.avatarUrl`、`licenseInfo`、`discussions` 计数与最新 8 条、最热 open issues 8 条（按评论数）、`latestRelease`、完整 `README.md`（及常见命名的中文版 `README.*zh*|*CN*.md`）——随同一查询抓取，复杂度高故 batch=15。注意 `latestRelease` **跳过 draft 和 pre-release**——全部预发布的仓（如 DiPlay）返回 null，采集时回退取 `releases(first:1, CREATED_AT DESC)` 最新节点并在详情里标 `is_prerelease`（前端显示"预发布"徽标）。非扩展运行这些字段为 `null`，快照写入前用"最近一次含扩展值的快照"向前沿用补齐；详情对象则写入 `data/repos/*.json` 的 `detail` 键（同样向前沿用，见下）。榜单计算不依赖扩展字段，故对排名零影响。
- **REST 兜底**：GraphQL 失败或个别仓库查不到时，用 `GET /repos/{owner}/{repo}` 补漏。注意限额差异：**GITHUB_TOKEN 为 1000 req/hr**，PAT/OAuth 为 5000 req/hr——兜底预算按 1000/hr 设计。
- **重试**：403/429/5xx 指数退避重试，最多 3 次；当日失败仓库在 `snapshot.errors` 中记录，次日补齐。

### Trending 抓取注意

- `github.com/trending` 是 HTML 页面，无官方 API。解析 `h2 a` 仓库链接 + `.f6.text-gray` Star 数等选择器；页面改版导致解析失败时，任务告警但不中断（快照可由 watchlist 独立完成）。
- **Actions 数据中心 IP 对该页限流严重**（匿名 HTML 请求按 IP 信誉调度，实测全部语言页 504）。采集采用 fail-fast：单页 1 次尝试、连续 2 败跳过剩余页，榜单靠 watchlist + Search API 继续运转。全页失败时通过 issue 驱动的离线救援通道补采，见 [07-rescue.md](07-rescue.md)。
- 每天 2 次运行各抓 1 次（共 2 次/日），配合 `GITHUB_TOKEN` 不需要（HTML 页面不需要认证），但加 `User-Agent` 头。
- 语言维度：v1 只抓总榜 trending + `python`/`javascript`/`typescript`/`go`/`rust` 等 TOP10 语言页，控制规模。

### 新闻报道采集（news.py）

- 每仓库 5 路免 key 抓取：Hacker News（Algolia `search` 相关性排序，按 `github.com/owner/repo` URL 精确匹配，带 points/评论数）+ Google News RSS 中文区 + 英文区（`"{name}" github` 查询，链接为 Google 跳转壳，`<source>` 为媒体名）+ Bing News RSS 中文（zh-TW 市场，zh-CN 对境外 IP 封锁）+ 英文区（`"{name}" github` 查询，apiclick 跳转链接的 `url=` 参数可解出原文直链，需浏览器 UA）。
- 落盘 `data/news/{owner}__{repo}.json`（独立目录，与 collect.py 的 repos/ 解耦），无条目不写文件；`items` 按 (直链优先, points, date) 排序、每语言封顶 10 条，`lang` 以标题 CJK 字符为准（纠正聚合器跨区返回），Bing/GN 中指向 github.com 的自引用结果剔除；merge 时旧数据仅被新数据更新、单源失败不清空。
- 频率分级：每日班 `--board`（当日八榜并集 ~400 仓 ×5 路 ≈ 14 分钟）；周日班 `--all`（全量 watchlist ×5 路 ≈ 40 分钟，回填历史报道）。
- rank.py 将 `items` 并入 repo detail JSON 的 `news` 字段，repo 页 SSR 双语块（zh/en 各一，非当前语言 `hidden`，爬虫两版可见）；repo.js 重渲染时按当前界面语言显隐。

## 限流预算（每日两次任务估算）

| 调用 | 每次运行 | 限额占比（GITHUB_TOKEN） |
|---|---|---|
| GraphQL 批量快照（~2000 仓库） | ~50 req / ~300 pts | ≈6% of 5000 pts/hr |
| Search API（新候选） | ~4 req | ≈13% of 30/min |
| Trending HTML | ~6 页 | 无 API 成本 |
| REST 兜底 | <200 req | ≈20% of 1000/hr |

结论：每日 2 次运行完全可行。若未来提高到 6 小时一更（4 次/日），GraphQL 合计 ~1200 pts/日仍远低于限额，REST 兜底需控制在 1000/hr 内，Search API 频率不变。

## 脚本结构（Python 3，仅标准库）

```
scripts/
  gh.py           # GitHub API 客户端：trending 抓取 / search / graphql 批量 / REST 兜底 / 重试
  collect.py      # Discovery + 快照主流程（调用 gh.py）；--role=plan/shard/reduce 三角色分片
  news.py         # 仓库新闻报道抓取：HN Algolia + Google/Bing News RSS（zh/en）→ data/news/
  rank.py         # 读快照 → 计算八榜 + 日/月/年聚合 → site/data/*.json + 静态页
  pack_data.py    # site/data/** → site-data.db（KV blob），CI 推给 api-site
  build.py        # （可选）HTML 模板渲染；v1 可由 rank.py 直接产出
```

- 全部使用标准库：`urllib`（HTTP）+ `html.parser`（Trending 页面解析）+ `json` + `argparse`，CI 零依赖安装。
- Trending HTML 解析用 `html.parser` 写轻量解析器（选类集中在 `gh.py`，页面改版只改一处）；正则解析 HTML 作为兜底。
- 所有外部请求带超时（30s）与重试；任何单点失败不阻塞整批。
