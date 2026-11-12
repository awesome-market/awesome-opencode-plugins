# trending-rank-radar 文档索引

> GitHub 开源项目趋势榜单站：独立采集仓库 Star 数据，产出日 / 周 / 月增长榜、新榜、总榜，支持按日 / 月 / 年回看历史，纯静态站部署 GitHub Pages，由 GitHub Actions 定时更新。

## 文档目录

| 文档 | 内容 |
|---|---|
| [01-overview.md](01-overview.md) | 项目概述、目标、竞品调研结论、差异化定位 |
| [02-data-pipeline.md](02-data-pipeline.md) | 数据源选型、候选仓库发现、快照存储格式、限流策略 |
| [03-ranking.md](03-ranking.md) | 八种榜单的计算口径、过滤规则、日 / 月 / 年历史回看语义 |
| [04-frontend.md](04-frontend.md) | 前端技术选型、页面结构、交互设计、数据文件约定 |
| [05-automation.md](05-automation.md) | 仓库目录结构、GitHub Actions 工作流、Pages 部署配置 |
| [06-roadmap.md](06-roadmap.md) | 分阶段实施计划与验收标准 |
| [07-rescue.md](07-rescue.md) | 离线救援通道：CI 抓 trending 失败时 issue 驱动的服务器补采 |

## 一句话架构

```
GitHub Trending / Search API / GraphQL API
        │  每日 2 次定时抓取
        ▼
data/snapshots/YYYY-MM-DDTHH.json   （每日 2 次 Star 快照，按北京时间归日）
        │  本地计算
        ▼
site/  （纯静态 HTML + JSON 数据，GitHub Pages 托管）
```
