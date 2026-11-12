# 05 仓库结构与自动化部署

## 仓库目录结构

```
trending-rank-radar/
├── docs/                  # 本文档目录
├── scripts/               # Python 3 标准库，零第三方依赖
│   ├── gh.py              # GitHub API 客户端（trending/search/graphql/rest + 重试）
│   ├── collect.py         # Discovery + 快照主流程
│   ├── rank.py            # 快照 → 11 榜 + 日/月/年聚合 → site/data/*.json
│   └── build.py           # （可选）HTML 模板渲染；v1 可由 rank.py 直接产出
├── site/                  # 静态站：源码模板+资产入库；data/repos/langs 等产物
│                          #   不入库（.gitignore），rank.py 每轮现场重建再发布
│   ├── index.html
│   ├── assets/
│   └── data/              # 生成物，不手改、不入库
├── data/                  # 采集数据（提交进 git，构成历史档案）
│   ├── snapshots/YYYY-MM-DDTHH.json
│   ├── watchlist.json
│   └── repos/*.json
├── .github/workflows/
│   └── daily-update.yml
└── README.md
```

## GitHub Actions 工作流

### `daily-update.yml`（每日两次 + 周日回填，含部署）

实际 workflow 的关键步骤（以仓库 `.github/workflows/daily-update.yml` 为准，此处为结构摘录）：

```yaml
on:
  schedule:
    - cron: '0 2 * * *'         # UTC 02:00 ≈ 北京 10:00
    - cron: '0 14 * * *'        # UTC 14:00 ≈ 北京 22:00（extended pass：topics/detail/watchers）
    - cron: '0 8 * * 0'         # 周日：news.py --all 全量回填
  workflow_dispatch:            # inputs: at（补录时间戳）/ deploy_only（只发布 site/）/ extended

permissions: { contents: write, issues: write }

jobs:
  plan:                         # collect.py --role=plan：discover + watchlist +
    # pick_fetches → data/collect-plan/plan.json（artifact），输出 16 路分片矩阵
  shard:                        # matrix [0..15]，fail-fast:false，单片 ~5min
    # collect.py --role=shard --shard=K/16：md5(full_name)%16==K 过滤后 fetch_metrics
    # → metrics-K.json（artifact）；14:00 班带 TRR_EXTENDED=1 抓扩展字段
  reduce:                       # needs: shard（等齐 16 片；deploy_only 时前两 job 跳过）
    concurrency: { group: daily-update, cancel-in-progress: false }
    steps:
      - download artifacts      # metrics-*.json + collect-plan
      - Merge + snapshot        # collect.py --role=reduce：合并 → carry-forward
                                #   （缺片标 shard_failed:K 并用旧值补齐）→
                                #   快照/meta/watchlist 落盘
      - Unit tests / news / ci_rescue   # 同前（deploy_only 跳过前两者）
      - Rebuild rankings        # rank.py --site-base $SITE_BASE（deploy_only 也跑：
                                #   site/ 不入库，发布前必须现场重建）
      - Commit data updates     # git add -A → commit → pull --rebase → push（自愈同前）
      - Pack + upload data store# pack_data.py：site/data/** → site-data.db（~9400 行
                                #   KV）→ gzip → POST api-site.zhuikan.com/data-upload
                                #   （Bearer $DATA_UPLOAD_TOKEN，sha256 回执校验，
                                #   失败即中止——数据不上线不发站）
      - Push gh-pages backup    # site/ 全量 → gh-pages 分支（含 data/，冷备镜像）
      - Deploy Cloudflare Pages # rsync 剔除 data/ → wrangler pages deploy
                                #   /tmp/cfp-site（~7k 文件 vs 上限 2 万）
      - Cache-bust              # 产物内 ?v=<sha> 由提交时 sed 写入
```

要点：

- `GITHUB_TOKEN` 在 Actions 内自动可用：**REST core 1000 req/hr、GraphQL 5000 points/hr、Search API 30 req/min**——分片后每 job 一份独立配额（16 片=16 倍预算）。
- 分片架构（2026-11 起）：`plan` 单点发现、`shard` 16 路并行抓数据（md5(full_name)%16 均匀切分，互不重叠）、`reduce` 单点合并落盘——git 只被 reduce 一个 job 写，零竞速；单片失败走 carry-forward 降级不整挂。extended pass（topics/detail）由 UTC 14:00 班或 `extended` input 触发，全量 ~10min（原串行 ~2h）。
- `workflow_dispatch` 输入：`at` 补录历史快照时间戳；`deploy_only` 跳过采集/提交，重建 `site/` 后发布（救援通道与纯 UI 改动用）；`extended` 手动强制扩展采集。
- Collect 后 `ci_rescue.py` 读 `run_status.json`：trending 全败则开 `rescue` issue 交给离线救援通道（[07-rescue.md](07-rescue.md)）；`rescue-report.yml` 是救援服务器回写 issue 的中继工作流（bot 身份）。
- "Commit data updates" 的 `git pull --rebase` 带自愈：生成文件冲突时取远端版本重跑 `rank.py`；干净 rebase 但 `data/` 有上游新快照时同样重建 `site/`。
- **只有 `data/` 提交回 main**（仓库即数据档案）；`site/` 产物由 rank.py 现场重建，不入版本控制——否则 ~5900 个页面每日全量重写会让 .git 无限膨胀。
- 幂等性：同一 CST 日第二次运行生成新时间戳文件，`rank.py` 按"当天最后一次"归日。

### 部署：Cloudflare Pages 主 + api-site 数据面 + gh-pages 冷备

- **HTML/资产 → Cloudflare Pages**：`wrangler pages deploy /tmp/cfp-site --project-name=zhuikan`——载荷**剔除 `site/data/`**（Pages 免费版单部署上限 2 万文件，全量曾达 ~2.7 万超限失败）。
- **数据面 → api-site blob store**：`site/data/**` 由 `scripts/pack_data.py` 打成单个 `site-data.db`（`data(path PK, blob)` KV 表）→ gzip 后 `POST https://api-site.zhuikan.com/data-upload`（Bearer `DATA_UPLOAD_TOKEN` secret，integrity_check + 原子替换 + sha256 回执）。前端水合统一从 `https://api-site.zhuikan.com/data/<path>` 取（`localhost` 开发时回退相对路径）。同一文件里 pack_data 还建 `search_items`+`search_fts` 两张真表（FTS5+触发器，源自 search-index/search-news.json）——API `db()` ATTACH 后 `/search` 和 `/me/*` 直读 `sd.*`，取代旧 `sync_search.py` cron 同步。
- **冷备**：`site/` 全量（含 `data/`）每轮推 `gh-pages` 分支 → `awesome-market.github.io/trending-rank-radar/` 镜像；该站水合同样指向 api-site，自身 data/ 文件仅作档案。
- 数据不上线不发站：upload 失败→job 失败→CF 不部署；API 不可达时页面仍显示 SSR 快照（水合静默失败），属降级非宕机。
- **Pages 路由层文件**：`site/404.html` 让未匹配路径返回真实 404（此前 SPA fallback 使任意乱拼路径回 200 + 首页 HTML——无限软 404 空间，GSC"已抓取未收录"的主要饲料）；`site/_redirects` 两条规则——`/data/*` → `api-site.zhuikan.com/data/:splat`（301，阴影覆盖 blob 化之前遗留的过期 data 文件：Pages 不回收已删文件，它们仍在服务旧数据）与 `/repo` → `/`（裸 `repo.html` noindex 模板不再直达）。

### 自定义域名

站点绑定 `zhuikan.com`（apex 为规范域），`www.zhuikan.com` 由 DNS 侧 301 到 apex：

- Cloudflare Pages 项目 `zhuikan` 绑定 apex 域；证书由 CF 自动签发。
- **`site/CNAME`** 仍保留 `zhuikan.com`——gh-pages 冷备镜像的 GitHub Pages 绑定需要它（从分支部署时 CNAME 必须存在于发布目录）。
- `sitemap.xml` / OG 绝对 URL 用 `rank.py --site-base`（默认 `https://zhuikan.com`，可用仓库变量 `SITE_BASE` 覆盖）。
- `awesome-market.github.io/trending-rank-radar/` 子路径仍可用作镜像——前端全部相对路径，两种形态兼容。

## 定时策略

**每日 2 次**（UTC 02:00 / 14:00 ≈ 北京 10:00 / 22:00），理由：

1. **冗余**：Actions cron 高负载会延迟甚至跳过，2 次/日至少保证一份完整快照
2. **口径更准**：22:00（北京）快照作为当日"收盘值"，日增接近真实全天涨幅；凌晨单次快照相当于拿"昨天深夜"当"今天"
3. **成本可忽略**：GraphQL ~300 points/次，2 次也远低于限额；公开仓库 Actions 免费
4. 数据文件按运行时刻命名（`YYYY-MM-DDTHH.json`），`rank.py` 按北京时间分组取末次，对榜单逻辑透明；为未来日内趋势图留数据基础

| 任务 | 频率 | 说明 |
|---|---|---|
| 快照 + 榜单重算 | 每日 2 次 | 每次运行都全量重算（幂等，同一天第二次运行会覆盖/补充当日数据） |
| 新闻采集 | 每日 2 次（`--board`） | 榜上仓库相关新闻；失败不阻塞（continue-on-error） |
| 新闻全量回填 | 每周日 1 次（`--all`） | UTC 08:00，补齐长尾仓库新闻 |
| 全量重建 | 每次运行 | rank.py 本就逐日全量重算——无需单独校验任务 |

若日后想降为 1 次/日，删掉一条 cron 即可，数据模型无需改动。

## 失败与告警

- 连续 2 天快照失败 → workflow 失败会体现在 Actions 记录；可选加一个 step 在失败时 commit 一个 `data/health.json` 供前端展示"数据更新于 X 前"。
- 前端 `index.json.generated_at` / `snapshot_days` 已能让用户感知数据新鲜度，v1 不做额外告警渠道。
