# 04 前端设计

## 设计定位

**数据仪表盘美学**：深色高级感 + 精致排版 + 微动效。参考 Vercel / Linear / Raycast 的仪表盘质感，配色基于 GitHub Primer 深色系但做了提亮和渐变。

核心记忆点：**前三名领奖台卡片 + 每行内嵌 Star 迷你曲线**——曲线数据来自快照序列，成本为零但视觉收益极大。

## 技术选型

**无构建纯静态**：原生 HTML + CSS + JavaScript（ES2020），不引入框架和打包工具。

- 数据全部是预生成 JSON，前端只做渲染和切换
- 零构建 = CI 最快、依赖最少、Pages 部署最简单
- 字体用系统栈（`-apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei"`），不引外部字体，保证加载速度

## 页面结构

```
site/                        # GitHub Pages 根目录（或 /docs）
  index.html                 # 榜单主页（单页）
  assets/
    style.css                # 全部样式（含动效）
    app.js                   # 路由 + 渲染 + 数据加载 + sparkline 绘制
  data/                      # rank.py 生成（见 03-ranking.md）
    index.json
    days/*.json
    months/*.json
    years/*.json
```

## 视觉系统

### 色板

```
背景:     #0a0e14 → #0d1117（顶部径向微光 #1a2332）
卡片:     rgba(255,255,255,0.03) + border rgba(255,255,255,0.07)
主文字:   #e6edf3    次文字: #8b949e    弱文字: #7d8590
品牌色:   纯色蓝 #58a6ff（不用蓝紫渐变——刻意的去"AI 味"处理；sparkline
          描边允许 #58a6ff→#79c0ff 同色系渐变，不构成渐变字/渐变块）
上涨绿:   #3fb950    下跌红: #f85149
奖牌色:   #f0c040(金) #c0c0c0(银) #cd7f32(铜)
```

### 组件规范

- **卡片**：`border-radius: 12px`，`backdrop-filter: blur(8px)`，hover 时 `translateY(-2px)` + 边框提亮，过渡 200ms ease
- **数字**：Star/增长量用 `font-variant-numeric: tabular-nums` 对齐；增长量 ≥1000 显示 `12.3k`
- **徽标**：语言彩色圆点 + 名称；增速% 用 pill 徽标（≥50% 绿色高亮，≥100% 加粗光晕）
- **动效**：数据加载 `fadeSlideIn`（opacity + translateY 8px，stagger 30ms）；`prefers-reduced-motion` 时全部降级为静态

## 页面布局

```
┌──────────────────────────────────────────────────────────────┐
│ ◉ Trending Rank Radar      数据更新于3小时前 [中/EN][☀][GitHub↗]│
│   GitHub 开源项目趋势榜单 · 每日双快照                          │
├──────────────────────────────────────────────────────────────┤
│  ┌── HERO ────────────────────────────────────────────────┐  │
│  │ 独立采集·开源数据      │  ▁▂▅▆▅▇▆▇█▇▅▆▅▃▅▂▁（Top1 仓库      │  │
│  │ 独立追踪 GitHub 星标   │   近30日 Star 曲线大图 + 说明行） │  │
│  │ 的每一次脉动           │                                  │  │
│  └───────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────┤
│  榜单 [新星榜][日飙升榜][日增速榜][周飙升榜]…（全名，非缩写）    │
│  时间 [日|月|年]  [2026-11-08 ▾]  Star范围 [1]k-[500]k       │
├──────────────────────────────────────────────────────────────┤
│  ┌── PODIUM ────────────────────────────────────────────┐    │
│  │  🥇        🥈        🥉                                 │    │
│  │ avatar   avatar    avatar                               │    │
│  │ owner/repo …（卡片：名称/简介/Star/增长/+sparkline）       │    │
│  └──────────────────────────────────────────────────────┘    │
│  ┌── LIST ──────────────────────────────────────────────┐    │
│  │ 4 avatar  owner/ repo↗   Py ★12.3k ⑂678 👁 ⑃ ◔ 🏷 ~spark~│  │
│  │           简介按内容自适应（≤2行）          ▲ +523 [+9%] │  │
│  │ [加载更多]                                              │  │
│  └──────────────────────────────────────────────────────┘    │
├──────────────────────────────────────────────────────────────┤
│ 跟踪 1,320 仓库 · N 快照日 · 覆盖 MM-DD~MM-DD · 最近Top1 +NNN │
│ 数据来源: GitHub API · 快照差值计算 · 仅供参考                 │
└──────────────────────────────────────────────────────────────┘
```

### 头部（Hero）

- 左侧：SVG 雷达图标（扫描动画**只播一次**（3.6s）后定格——既保留"扫描"意象，又满足"循环动画 5s 内停驻"的可访问性要求）+ 标题（纯色蓝字，不用渐变字）+ 副标题
- 右侧：数据新鲜度指示（绿色脉冲圆点 + "数据更新于 X 前"）+ **语言切换按钮**（`EN`/`中`）+ **主题切换按钮**（☀/☾）+ GitHub 仓库链接
- 顶部 40vh 内一层 `radial-gradient` 光晕 + 细网格纹理（CSS `background-image` 线性渐变网格，opacity 3%）

### Hero 视觉区（替代原数据统计条）

左：kicker + 一句主张文案 + 副文案（中英双语）。右：**当日飙升 Top1 仓库的近 30 日 Star 大图曲线**（620×150 SVG 面积图，`preserveAspectRatio="none"` 自适应宽）+ 一行说明（仓库名链接 + 当日增量 + 曲线天数）。无有效曲线时降级为大号雷达徽章。这是"真实产品 UI 片段"而非装饰图——曲线数据本就随榜单生成。

统计信息不占用版面：跟踪仓库数 / 快照天数 / 覆盖跨度 / 最近 Top1 增量合并为**页脚一行**（`#footStats`，双语模板）。

### 控制区（sticky top）

- **榜单 tabs**：8 个 pill tab，**写全名不写缩写**（新星榜 / 日飙升榜 / 日增速榜 / 周飙升榜 / 周增速榜 / 月飙升榜 / 月增速榜 / 总榜；EN：New Repos / Daily Growth / Daily Rate / Weekly Growth / Weekly Rate / Monthly Growth / Monthly Rate / All-Time），月视图追加"月累计榜"；选中态 = 纯色底；≤768px 折行全展示（不做横向半截滚动）
- **时间维度**：`日 | 月 | 年` 三段式 segmented control + 对应日期/月/年选择器（`<select>`，选项来自 `index.json`；月视图进行中的月份标注"进行中"）
- **统计时间显示**：展示榜单实际窗口区间（如 `10-15 ~ 11-08 · 24天`），窗口回退期用户能看懂口径
- **Star 范围**：两个 number 输入（k 为单位，默认 1–500）+ 筛选按钮
- sticky 后带 `backdrop-filter: blur(12px)` + 半透明底 + 底部细分割线

### 榜单内容

**Top 3 领奖台**（仅当榜单 ≥3 条时显示）：

- 三张横排大卡片（移动端纵向），金/银/铜渐变边框 + 轻微不同的纵向偏移（第 2 名低 8px、第 3 名低 16px，经典领奖台错位）
- 卡片内容：大号奖牌 emoji 或 SVG 奖章、头像（`github.com/{owner}.png`）、`owner/name`（链接新窗口）、简介（2 行截断）、主指标超大数字（增长量 `+12.3k` 或 Star 数）、增速 pill、30 天 sparkline
- hover：卡片上浮 + 边框流光（`conic-gradient` 旋转边框，`@property` 注册或伪元素动画）

**4 名及以后·宽版行**（参考主流榜单站的行布局，大气易读）：

```
#4 │ [avatar 48px] │ owner/ name ↗            │ ▁▂▅▇▅▃ │
   │               │ Py ★12.3k ⑂678 👁132 ⑃7 ◔9 🏷3 │ ▲ +523   │
   │               │ 简介按内容自适应（≤2行 clamp）    │ [+9%]    │
```

- 行结构：`rank | avatar | (名称行 / 元信息行 / 自适应简介) | (sparkline + 增长区)`
- 名称行：**作者名 `owner`（灰）+ `/` + 仓库名（加粗）**，整段为 GitHub 新窗口链接，尾挂**常显外链图标**（`↗` 风格 SVG，`title` 提示"在 GitHub 打开"）——作者与"可点击"暗示缺一不可
- 元信息行：语言圆点 + star/fork（始终）+ watchers/PRs/issues/releases（扩展字段非 null 才渲染，≤768px 只留 star/fork）。注：GitHub 无仓库"下载量"口径，releases 数为最接近的发布产物指标
- 简介 `-webkit-line-clamp: 2` **不设 min-height**：一行简介只占一行高度，无简介时整个元素不渲染——行高完全按内容自适应
- 右侧：sparkline（≥900px）+ 大号增长数 `▲ +N`（或总/新榜的大号 star 数）+ 增速 pill（`+N%`，≥100% 加 glow）
- 行 hover：背景提亮 + 左侧 2px 纯色指示条滑入
- sparkline：80×24px 内联 SVG，`polyline` 描边 + 渐变面积填充，窗口内每日 Star 序列归一化
- `approx`/`stale` 条目标 `≈`/`⧗` 角标并 tooltip 说明；新榜条目附"创建于 N 天前"chip（月视图以月末近似日计算）

### 深/浅色主题 + 中英双语

- **主题**：hero 右侧 ☀/☾ 按钮（SVG 图标随主题显隐），选择存 `localStorage.theme` 并同步 `meta[name=theme-color]`；初始 `localStorage` → `prefers-color-scheme`；`<head>` 内联脚本在 CSS 加载前设置 `documentElement.dataset.theme`，无闪烁；两套调色板均为 CSS 变量，`color-scheme` 同步使原生控件跟随
- **语言**：主题按钮旁的 `EN`/`中` 按钮（label 恒为目标语言），选择存 `localStorage.lang`；初始 `localStorage` → `navigator.language`（zh 前缀判中文，否则英文）；`documentElement.lang` 同步 `zh-CN`/`en`
- **i18n 实现**：`assets/common.js` 内置共享 `I18N` 字典（`{zh, en}` 两棵平行键树，`t(key, params)` 取词 + `{param}` 插值），`app.js`（榜单页）与 `repo.js`（详情页）均在 common.js 之后加载；静态元素用 `data-i18n` / `data-i18n-aria` / `data-i18n-title` 标注，`applyStaticI18n()` 批量刷新；动态文案全部走 `t()`；主题/语言切换由 `bindChrome()` 统一绑定，语言切换回调里重绘页面动态区

**空状态**（冷启动）：居中雷达 SVG 动画 + "快照积累中" + 进度条（`snapshot_days / 31`，月榜完整口径需 31 个有效日；周榜需 8 日）+ 预计可用日期。窗口回退期榜单照常展示，统计时间处标注实际天数。

## 详情页 `repo.html`

每仓库一个详情页，URL `repos/<owner>__<name>`（CF Pages 规范化为无扩展名，`.html` 仍 308 可达）（rank.py 以 `repo.html` 为模板预渲染的独立静态页，全部进 sitemap）：`<title>`/`description`/`canonical`/`og:url` 各自自指，正文 SSR 进 `#repoContent`——爬虫与无 JS 客户端直接读到完整内容；`<body data-repo data-base>` 让 `repo.js` 加载后接管交互（趋势图/分享图/主题语言）。`repo.html?r=` 壳页保留兼容旧链接并标记 `noindex`。数据源 `data/repos/<owner>__<name>.json`。

区块顺序：头部卡（头像/owner/repo/GitHub 外链/简介/topics/语言·许可证·创建·主页）→ 榜单名次 chips（链回 `?board=*`）→ 指标总览卡（stars/forks/watchers/PRs/issues/releases/discussions + stars 日/周/月增量）→ 趋势卡（指标 tab：stars/forks/watchers；范围 tab：近7天/近30天/全部；SVG 折线+网格+悬停点；「生成分享图」Canvas 1200×630 PNG 下载/复制）→ 双列卡片区（热门 Issues / 最新 Discussions / 最新 Release / README 摘要，均无数据时整块不渲染）。

行内仓库名一律进详情页（`repo.html?r=`），↗ 图标单独跳 GitHub；预览行、月榜 top10 chip、hero Top1 同规则。

### 响应式

设计基准为 **≥1440px 桌面屏**（容器 `max-width: 1360px`），向下仍保有可用降级：

- ≥1024px：领奖台三列 + 宽版行，hero 视觉区左右两栏
- 768–1024px：领奖台纵向堆叠，hero 视觉区单列
- <768px：领奖台卡片全宽、榜单 tabs 折行、行元信息只留 star/fork、sparkline 隐藏

## 用户中心 `user.html`

独立静态页 `/user`（`noindex,nofollow`，不进 sitemap，`?tab=` 深链），右上角 auth 下拉即各 tab 的入口链接。四 tab：收藏/点赞（行列表 + 取消按钮，数据源 `GET /me/favorites|likes`）、我的评论（`GET /me/comments`，含审核状态 tag + 自删）、设置（昵称 `POST /auth/display_name`、用户名 `POST /auth/username`、换绑邮箱两步 `POST /auth/email`→`verify`、改密码 `POST /auth/password` 仅 `has_password` 时显示、绑定方只读、退出登录）。未登录态显示登录引导卡而非跳转。所有数据经 api-site + JWT，`user.js` 按 tab 懒加载。

## 数据消费约定

前端只读 JSON，不做任何计算。榜单条目需含 sparkline 数据：

```json
{
  "rank": 1,
  "owner": "xxx", "name": "yyy",
  "description": "...", "language": "Python",
  "stars": 12345, "forks": 678,
  "growth": 523, "rate": 9, "approx": false, "stale": false,
  "series": [11800, 11920, ..., 12345]
}
```

`series` = 截至该榜单日期的**最近 30 个有效快照日** Star 序列（与榜单窗口无关，长度统一便于渲染；不足 30 天给已有什么），`rank.py` 输出时附带；`description`/`homepage` 由 `rank.py` 从 `data/repos/*.json` 元数据内联合并。

> **预计算规模**：每榜 Top 200（前端筛选后展示 Top 100），八榜去重后约 300–400 个唯一仓库/日，单日 JSON ~100KB。

`index.json` 示例：

```json
{
  "generated_at": "2026-11-08T14:20:00Z",
  "latest_day": "2026-11-08",
  "snapshot_days": 23,
  "dates": ["2026-10-17", "..."],
  "months": ["2026-10", "2026-11"],
  "years": ["2026"]
}
```

`snapshot_days` = **有效快照天数**（按北京时间归并后有数据的天数，非运行次数——每日 2 次运行不重复计数）。空状态进度条、数据新鲜度均以此为准。

### 关键约束：资源路径必须相对

站点绑定自定义域名 `zhuikan.com`（根路径服务，`site/CNAME` 随 artifact 发布保证绑定不丢），同时保留 `awesome-market.github.io/trending-rank-radar/` 项目子路径镜像。所有资源与数据请求一律使用**相对路径**（`assets/app.js`、`data/index.json`），禁止以 `/` 开头的绝对路径——相对路径在两种部署形态下都成立；`history.pushState` 的 query 参数不受影响。

`sitemap.xml` / OG `og:url` 需要站点绝对地址：`rank.py` 接受 `--site-base` 参数（默认 `https://zhuikan.com`，workflow 可用仓库变量 `SITE_BASE` 覆盖），生成时写入。

## SEO / GEO / 分享

- `history.pushState` 同步 query（`?board=weekly_rate&date=2026-10-15`），可直接分享
- JS 动态更新 `document.title`；`<noscript>` 块保证无 JS 爬虫仍能取到双语站点描述与数据链接
- `<head>`：canonical、robots、author、hreflang（zh/en/x-default）、OG/Twitter 全套、JSON-LD（WebSite + Dataset）、`manifest.webmanifest`
- `robots.txt`（rank.py 生成）：允许全部爬虫，并显式放行 AI/LLM 爬虫（GPTBot、ClaudeBot、PerplexityBot、Google-Extended 等）——开放数据项目主动拥抱 GEO
- `llms.txt`：LLM 友好的站点说明 + 全部 JSON 数据端点 + 字段字典 + 口径说明
- `sitemap.xml`（rank.py 生成）：首页 + 各榜单入口（`?board=*`）
- `site/CNAME` 随 artifact 发布维持自定义域名绑定

## 统计埋点

三套统计并行，互不干扰、各自定位不同：

- **自建 `/stats/view`**（api-site）：`app.js`/`repo.js`/`user.js` 加载时 fire-and-forget，`path=location.pathname` 归属真实页面（曾硬编码 `/` 导致板/tag/语言页全记成首页）；IP+UA 日盐哈希去重不存原始 IP，数据用于行内"浏览数"展示与 admin 统计面板。带登录态的请求另落 `user_views` 浏览历史，仅管理后台用户行「历史」按钮可见。
- **Cloudflare Web Analytics**：CF 边缘对浏览器 UA **自动注入** beacon（curl/探测请求拿不到注入属预期，非故障），免代码免 cookie；面板提供 PV/UV/来源/设备 + Core Web Vitals。
- **百度统计 hm.js**：注入 `index.html`/`repo.html`/`404.html` 模板，构建传播到全部生成页。`common.js` 捕获阶段委托监听把出站点击发 `_trackEvent`（category=`outbound`，action 分 `repo/repo-sub/topic/homepage/other`，label=目标 URL——外链多为 `target=_blank` 本页存活，送达可靠）；`app.js` 在 `pushState` 后补 `_trackPageview`，SPA tab/筛选切换也计 PV。事件在百度后台「事件跟踪」报表查看。
