# 06 实施路线图

> 状态：Phase 1–3 已全部完成并稳定运行；Phase 4 前三项已完成（语言页 2026-11 以静态页形态落地），本文件已按现状勾选。

## Phase 1：数据管道 MVP（先让数据转起来）✅

目标：每天能产出一份有效快照，榜单数据可被离线验证。

- [x] `scripts/collect.py` + `scripts/gh.py`
  - [x] Trending 页面抓取（总榜 + TOP 语言页，`html.parser`；空解析计为失败并触发救援通道）
  - [x] Search API 新仓库候选（`created:>90d stars:>20`，对齐新榜）
  - [x] GraphQL 批量快照 watchlist（16 字段：stars/forks/watchers/issues/prs/releases/created_at/language/is_fork/is_archived + issues/prs 开闭/合并细分）
  - [x] `data/repos/*.json` 低频元数据缓存（description/homepage 等）
  - [x] 写 `data/snapshots/YYYY-MM-DDTHH.json`（自取 UTC 时间戳，原子写）+ 更新 `watchlist.json`（含淘汰规则）
- [x] `scripts/rank.py`（最小版 → 完整版）
  - [x] 读快照（按北京时间分组取每日收盘值）→ 算榜（窗口回退 + `≈`/`stale` 标记）→ 输出 `site/data/index.json` + `days/*.json`（含 `series` sparkline，元数据内联合并）
- [x] 本地手动跑通验证快照累积（现已 60+ 天历史）

## Phase 2：榜单与历史回看 ✅

- [x] `rank.py` 完整版：日/周/月飙升+增速六榜 + 新榜 + 首登榜 + 总榜 + Fork/Watch 日增榜（11 榜）
- [x] 日/月/年三粒度聚合输出（`days/` `months/` `years/`）
- [x] 前端 `index.html` + `app.js` + `style.css`（按 04-frontend.md 视觉规范）
  - [x] Hero 视觉区（Top1 Star 曲线）+ sticky 控制区（榜单 tab / 日月年切换 / k 范围筛选）+ 中英双语 + 深浅主题
  - [x] Top3 领奖台卡片 + 紧凑行列表 + 30 天 sparkline + 空状态
  - [x] 首页/仓库页 SSR 注入（Baidu/无 JS 可读）
- [x] 仓库详情页 `repos/<owner>__<name>`（SSR + 全历史曲线 + 多指标面板 + README + 新闻 + 社交/评论）

## Phase 3：自动化上线 ✅

- [x] 推送到 GitHub 公开仓库
- [x] `.github/workflows/daily-update.yml`（cron ×2 + 周日 news 回填 + workflow_dispatch/deploy_only）
- [x] 上线 `zhuikan.com` —— **主部署为 Cloudflare Pages**（wrangler direct-upload；deploy-pages 的 10 分钟文件同步上限装不下 ~万级文件，`gh-pages` 分支降为冷备镜像，见 05-automation.md）
- [x] 仓库变量 `SITE_BASE`
- [x] README.md
- [x] Trending 抓取失败救援通道（`ci_rescue.py` → rescue issue → VPS `rescue.py` → deploy_only，见 07-rescue.md）
- [x] `tests/` 单测（rank 窗口/榜单/语言页/首登榜语义），CI 采集前运行

## Phase 4：增强（按需迭代）

- [x] 语言维度榜单 —— 以**静态页**落地：`/langs/<slug>.html`（Python/TypeScript/… 共 15 种语言，候选池按语言过滤后重排，日视图），行内语言标签直达
- [x] 指标维度 —— `daily_forks` / `daily_watchers` 两个日榜 tab（快照第 1 天起就有这两列）
- [x] 仓库详情页（见 Phase 2）
- [x] RSS/订阅 —— `feed.xml`（Atom：最新日首登榜 + 日飙升榜 Top）；JSON API 即 `site/data/**` 开放数据（见 `llms.txt`）
- [x] 多语言 UI（en）
- [ ] 语言页历史回看（当前仅最新日；按日历史语言榜数据量大，按需评估）
- [ ] 周/月维度的指标榜（当前只有日维度）

## 已知风险与对策

| 风险 | 影响 | 对策 |
|---|---|---|
| Trending 页面改版导致解析失败 | 当日候选减少 | 空解析计为失败 → `ci_rescue.py` 开 rescue issue → VPS 救援机抓取（07-rescue.md） |
| GitHub API 限额收紧 | 快照不完整 | GraphQL 优先（点数制宽裕）；REST 兜底（有界）；watchlist 规模控制 |
| 仓库被删/改名 | 快照缺字段 | GraphQL `repository()` 返回 null 时标记，次日从 watchlist 移除 |
| git 仓库随数据增长变大 | clone 变慢 | 快照原始 ~150–180MB/年，git 压缩后 ~30–40MB/年；超限再做历史快照归档压缩 |
| Actions cron 延迟/跳过 | 数据断档 | `workflow_dispatch` 手动补跑；快照按时间戳幂等；rescue 通道可在 CI 外补数据 |
| 发布产物不完整 | 半残页面上线 | CF 部署前校验 `index.html` 存在（workflow deploy guard） |
