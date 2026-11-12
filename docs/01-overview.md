# 01 项目概述

## 目标

做一个独立运行的 GitHub 项目趋势榜单站，覆盖主流 GitHub 榜单站的核心能力：

- **十一种榜单**：新榜 + 首登榜（首次进入任一榜单）+ 日/周/月 × 飙升榜（增长绝对值）+ 增速榜（相对增长率）+ Fork/Watch 日增榜 + 总榜（累计 Star），口径经同类榜单站公开数据实测校准
- **历史回看**：按日 / 月 / 年查看任意历史时点的榜单数据；另有按语言重排的静态页（`/langs/<slug>.html`）
- **完全自托管**：数据自己爬，不依赖第三方榜单 API
- **低运维**：GitHub Actions 定时跑，产物是纯静态文件，Cloudflare Pages 主托管（gh-pages 分支冷备）；用户态（登录/评论/点赞）由独立 `zhuikan-api` 服务承载，与本静态数据管道解耦

## 对标分析（2026-11 调研）

| 项目 | Stars | 相似点 | 差距 |
|---|---|---|---|
| josebergo/github-pulse | 0 | 日/周/月榜 + 快照差值算法 + 历史回放 | Go 后端 + SQLite + React SPA，必须跑服务，无法上 Pages |
| hanishrao/trending-collection | 13 | Trending 日/周/月数据归档至 2015，静态 JSON API | 只有官方 Trending 原始榜，无 Star 增长计算、无新/总榜、无 UI |
| larsbijl/trending_archive | 408 | Trending 每日归档 | 纯 markdown 数据，无网站 |
| sivagao/github-serendipity.github.io | 534 | 唯一同类静态站（Pages 托管） | 无 Star 增长榜、无历史数据 |
| EvanLi/Github-Ranking | 12.9k | 仓库按 Star 排名 | 只按总 Star 排，无增长榜、无历史 |
| OpenGithubs/github-*-rank 等数据归档仓库 | ~4.6k 合计 | 榜单快照数据归档 | 仅 markdown 数据，无站点代码 |

## 差异化定位

```
别人做的：  Trending 页面抓取  →  存原始榜  →  发 markdown
我们做的：  自建 Star 快照库   →  差值算增长  →  八榜 + 历史回看  →  静态网站
```

核心壁垒是**自有快照数据**：Star 增长榜的本质是"同一仓库不同时点的 Star 差值"，必须自己每天存快照才能算出来，无法靠一次性爬取获得。

## 关键约束（先说清楚）

- **冷启动**：Star 历史无法从 GitHub API 回溯，增长量按窗口回退规则用可用快照计算（见 03-ranking.md）——上线第 2 天日榜即可出，周/月榜以"近 N 天"口径先行展示，约 8 / 31 个有效快照日后分别补满 7 / 30 天完整窗口。
- **GitHub API 限额**：Search API 30 req/min（认证），GraphQL 5000 points/hr。日更场景下足够，详见 [02-data-pipeline.md](02-data-pipeline.md)。
- **数据规模**：跟踪仓库 ~6000 个，每次快照（每日 2 次）约 600–800 KB 原始 JSON，年增原始 ~400–500 MB；git 对重复性 JSON 压缩比高，仓库体积年增 ~80–100 MB。`site/` 生成产物（~300MB、每日全量重写）不入版本库，由 rank.py 现场重建后发布。

## 架构决策：为什么不用数据库

静态托管只能放静态文件，无服务端运行时。本项目采用 JAMstack 模式规避：

- **写**：GitHub Actions 是榜单数据的唯一写入者——`collect.py` 爬数据、`rank.py` 算榜、git commit 回仓库。`data/snapshots/` 本身就是数据库（追加式 JSON 档案）。VPS 救援机作为 CI 外补数通道，同样只写 `data/`。
- **读**：浏览器直接 fetch `site/data/*.json` 预计算文件，零后端零查询。
- **用户态**：登录 / 评论 / 点赞 / 收藏走独立部署的 `zhuikan-api` 服务（SQLite + FastAPI），与榜单数据完全解耦——榜单站挂掉不影响用户态，反之亦然。

该模式适配本项目"定时批处理 + 读多写少"的特征。

## 非目标

- 商业推广/榜单投稿机制
- 更多语言 UI（中/英双语已上线，暂不加第三语言）
- 语言页的历史回看（语言榜只有最新日视图）
