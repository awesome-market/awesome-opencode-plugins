# opencode-ds-websearch

> DeepSeek 自研网页搜索接入 [OpenCode](https://opencode.ai) 的插件：覆盖内置 `websearch` 工具，支持结构化筛选、正文控制、自动重试、低相关度标注与双通道降级。

非 DeepSeek / OpenCode 官方项目，只调用公开的 Search API，不抓取网页、不注入页面脚本。

- 适用：OpenCode v2（插件 API `Plugin.define({ id, setup })`，本插件用等价的默认导出对象）
- 运行依赖：无（只用 Node 内置模块 + 内置 `fetch`）
- 无需构建：`src/index.ts` 直接被宿主加载

## 目录

- [特性](#特性)
- [安装](#安装)
- [配置 API Key](#配置-api-key)
- [工具参数](#工具参数)
- [搜索语法](#搜索语法)
- [使用示例](#使用示例)
- [输出格式](#输出格式)
- [可靠性设计](#可靠性设计)
- [已知限制](#已知限制)
- [开发与测试](#开发与测试)
- [安全与隐私](#安全与隐私)
- [FAQ](#faq)
- [License](#license)

## 特性

| 能力 | 说明 |
| --- | --- |
| 中文召回强 | 使用 DeepSeek 自研搜索引擎，结果自带 `rerank_score`（0–3）与 `authority`（0–4） |
| 结构化筛选 | 用 `site` / `exclude_sites` / `lang` / `after` / `before` / `exclude_terms` 传参，插件自动折叠成 `site:`、`lang:`、`after:` 等语法，已存在的不重复追加 |
| 正文按需返回 | `need_content: true` 才请求网页正文，单条最多 3000 字、单次最多 12000 字，超出明确标注 |
| 质量信号 | `rerank_score >= 1.5` 标 `★优质`；`authority >= 3` 标「高」；低于 0.8 标「（低）」，整批都低时顶部提示换关键词 |
| 稳健请求 | 408 / 429 / 5xx / 网络异常最多重试 3 次，尊重 `Retry-After`；其他 4xx 不重试 |
| 双通道 | DeepSeek 故障或 0 条时自动补查备用通道（TinyFish），并区分「降级」与「补查」 |
| 体积友好 | 标题 160 字、摘要 500 字、片段 240 字上限；URL 去重（忽略 `#fragment`、尾斜杠、主机大小写） |
| Key 免改代码 | 每次调用重新解析 `DEEPSEEK_API_KEY` 或本机 OpenCode 配置，轮换后无需改插件 |

## 安装

### 方式一：单文件放入全局插件目录（最简单，适合分发给同事）

把 `src/index.ts` 复制成：

```
~/.config/opencode/plugins/deepseek-web.ts
```

Windows 即 `C:\Users\<你>\.config\opencode\plugins\deepseek-web.ts`。

该目录下的 `.ts` 会被自动加载，**无需改 `opencode.json`**。改完重启或重载 OpenCode 即可，工具名仍为 `websearch`。

```powershell
# Windows 示例
Copy-Item .\src\index.ts "$env:USERPROFILE\.config\opencode\plugins\deepseek-web.ts" -Force
```

### 方式二：作为本地插件包

克隆到任意固定位置（不要在临时目录，否则清了就失效）：

```bash
git clone https://github.com/2102014/opencode-ds-websearch.git ~/opencode-ds-websearch
```

在 `~/.config/opencode/opencode.json(c)` 中注册：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "/absolute/path/to/opencode-ds-websearch"
  ]
}
```

也可以带 options（当前版本无必填 options，保留给自定义扩展）：

```jsonc
{
  "plugins": [
    { "package": "/absolute/path/to/opencode-ds-websearch" }
  ]
}
```

### 方式三：从 GitHub 安装

```bash
opencode plugin add github:2102014/opencode-ds-websearch
opencode service restart
```

需要跟随分支更新：

```bash
opencode plugin add github:2102014/opencode-ds-websearch#main
```

固定版本（不自动跟随）用 tag 或 commit：

```bash
opencode plugin add github:2102014/opencode-ds-websearch#v1.0.0
```

### 升级 / 卸载

```bash
opencode plugin list          # 查看已安装
opencode plugin update        # 更新所有（含本插件，若配置为跟随分支/范围）
opencode plugin remove github:2102014/opencode-ds-websearch
```

单文件方式直接删除 `plugins/deepseek-web.ts` 即可；删除前建议留一份副本，否则回滚要重新下载。

## 配置 API Key

插件**不内置任何 Key**，每次调用按以下顺序解析，取到第一个有效值：

| 优先级 | 来源 | 说明 |
| --- | --- | --- |
| 1 | 显式传入 `apiKey` | 仅代码/测试调用 `search(req, { apiKey })` 时使用，正常安装用不到 |
| 2 | 环境变量 `DEEPSEEK_API_KEY` | 推荐。团队分发时每人配自己的 Key |
| 3 | 本机 OpenCode 配置 `providers.deepseek.settings.apiKey` | `~/.config/opencode/opencode.json` 或 `opencode.jsonc`，含 JSONC 注释也能解析 |

要点：

- **每次搜索都会重新解析**：改环境变量或改配置后，下一次搜索即生效（环境变量通常需要重启宿主进程才能被重新读取；配置文件是每次调用重读）。
- **分发时只给插件文件/仓库**，不要把 `opencode.json` 一起给，避免把别人的 provider Key 传出去。
- 未找到 Key 不会抛异常打崩会话，而是记录 `未找到 DeepSeek API key…` 并走备用通道。

```powershell
# Windows（当前会话临时生效）
$env:DEEPSEEK_API_KEY = "sk-..."
# 或永久写入用户环境变量（需要重开终端/宿主）
[Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "sk-...", "User")
```

```bash
# macOS / Linux
export DEEPSEEK_API_KEY="sk-..."
```

## 工具参数

工具名：`websearch`（覆盖内置同名工具，参数完全由本插件定义）。

| 参数 | 类型 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| `query` | string | 是 | — | 1–128 字符（**含折叠后的筛选条件**），支持下方全部搜索语法 |
| `count` | integer | 否 | `8` | 1–50，条数不影响计费 |
| `need_content` | boolean | 否 | `false` | 是否返回网页正文；按单条 3000 字、总计 12000 字截断 |
| `ori_question` | string | 否 | — | 触发本次搜索的用户原始问题（≤128 字符），提升意图理解 |
| `site` | string | 否 | — | 只搜这些站点，逗号或空格分隔，如 `github.com,huggingface.co` → `site:a OR site:b` |
| `exclude_sites` | string | 否 | — | 排除站点，多个用逗号/空格分隔 → `-site:x -site:y` |
| `lang` | string | 否 | — | 限定语言，逗号分隔，如 `zh,en` → `lang:zh,en` |
| `after` | string | 否 | — | 只返回该日期之后发布，格式 `2025` / `2025-01` / `2025-01-31` |
| `before` | string | 否 | — | 只返回该日期之前发布，同上格式 |
| `exclude_terms` | string | 否 | — | 排除词，逗号分隔；含空格视为精确短语 → `-词` / `-"短语"` |

参数校验在本地完成，不合法的请求不会发出（省一次计费）：

- 空查询、超过 128 字符、拼接筛选后超 128 字符
- 语言代码不是 `zh` / `en` / `zh-CN` 这类形式
- 日期格式错误或不存在的日期（如 `2025-02-30`）
- 站点不是合法主机名
- `localization`（仅代码/env 可用）不是 IP

## 搜索语法

`query` 原样传给 DeepSeek，以下操作符可直接写在 `query` 里，也可用上表的参数让插件代写：

| 操作符 | 示例 | 说明 |
| --- | --- | --- |
| `site:` | `DeepSeek site:github.com` | 限定站点；多个用 `OR`：`site:a OR site:b` |
| `-site:` | `DeepSeek -site:example.com` | 排除站点 |
| `-` | `DeepSeek -广告` | 排除含该词的网页 |
| `-"..."` | `DeepSeek -"release notes"` | 排除含该短语的网页 |
| `"..."` | `DeepSeek "精确短语"` | 精确匹配短语 |
| `lang:` | `DeepSeek lang:zh,en` | 限定语言，逗号分隔 |
| `after:` | `DeepSeek after:2025-01-01` | 发布时间晚于 |
| `before:` | `DeepSeek before:2026-06` | 发布时间早于 |

## 使用示例

### 自然语言（模型自行决定参数）

```text
帮我查一下 DeepSeek 4 月发布的模型，只看官方文档站，2025 年之后的。
```

模型可能发出：

```json
{
  "query": "DeepSeek 模型 发布",
  "site": "api-docs.deepseek.com",
  "after": "2025",
  "count": 5,
  "ori_question": "DeepSeek 4 月发布的模型"
}
```

实际请求体：

```json
{
  "query": "DeepSeek 模型 发布 site:api-docs.deepseek.com after:2025",
  "count": 5,
  "need_content": false,
  "ori_question": "DeepSeek 4 月发布的模型"
}
```

### 需要读原文

```json
{ "query": "DeepSeek Search API 计费", "count": 3, "need_content": true }
```

### Code Mode / 脚本

```ts
const r = await tools.websearch({
  query: "DeepSeek V4 上下文长度",
  count: 2,
  need_content: true,
  lang: "zh",
})
console.log(r)
```

### 程序化调用（Node / Bun）

```ts
import { search, format } from "./src/index"

const out = await search({ query: "DeepSeek", count: 3 })   // 走 env / 本机配置取 Key
console.log(format(out))
console.log(out.source, out.hits.length, out.errors)
```

## 输出格式

```text
来源：DeepSeek，共 3 条（优质 2 条）

1. DeepSeek-V4 预览版：迈入百万上下文普惠时代
   https://api-docs.deepseek.com/zh-cn/news/news260424/
   DeepSeek · 2026-04-24 · 权威 3/4（高） · 相关 2.35 · ★优质
   摘要：……
   【正文】2258 字
   ……
2. ……
   …inPA · 权威 4/4（高） · 相关 0.41（低）
```

字段含义：

- `来源`：`DeepSeek` / `TinyFish（降级）` / `TinyFish（补查）`
- `优质 N 条`：`rerank_score >= 1.5` 的条数
- `权威 x/4（高）`：`authority >= 3`
- `相关 x.xx（低）`：`rerank_score < 0.8`，仅标注不丢弃
- `⚠️ 结果相关度普遍偏低（最高 x.xx）`：全部命中的最高分都低于 0.8
- `【正文】N 字，已截断至 3000 字`：命中单条上限
- `（另有 N 条正文因总预算 12000 字已用完而未展示。）`

## 可靠性设计

### 超时与重试

| 项目 | 值 |
| --- | --- |
| 单次请求超时 | 15s（`need_content` 时 25s） |
| 重试总次数 | 3 次（含首次） |
| 退避 | 600ms 起，逐次翻倍，单次等待上限 3s |
| `Retry-After` | 优先采用，同样受 3s 上限约束 |
| 会重试 | 408、429、5xx、网络异常/超时 |
| 不重试 | 400、401、402、403、404、413 等确定性错误 |
| 用户取消 | 立即停止，不再重试也不再补查 |

### 降级与补查的区别

| 场景 | `metadata.degraded` | 来源标签 | 顶部提示 |
| --- | --- | --- | --- |
| DeepSeek 正常有结果 | `false` | `DeepSeek` | 无 |
| DeepSeek 故障（401/429/超时…），备用通道有结果 | `true` | `TinyFish（降级）` | `⚠️ DeepSeek 搜索不可用（原因），已自动降级…` |
| DeepSeek 正常返回 0 条，备用通道有结果 | `false` | `TinyFish（补查）` | `ℹ️ DeepSeek 正常返回但无匹配结果…补查结果` |
| 两通道都 0 条 | `false` | — | `没有匹配结果…建议放宽关键词或去掉筛选条件` |
| 两通道都失败 | `true` | — | `❌ 两条搜索通道都失败：…` |

上游脚本判断「主通道是否故障」请看 `degraded`，不要看 `source`。

## 已知限制

- **`query` 上限 128 字符**，且筛选条件会拼进 `query`。站点/排除项过多时可能超限，插件会直接报错并提示缩减，而不是静默截断。
- **`count` 上限 50**；一次请求最多 50 条，条数不影响计费。
- **正文不是全文**：单条 3000 字、单次 12000 字。需要整页请用内置 `webfetch` 或自行调用 `/v1/tools/fetch`（本插件未实现 fetch 工具）。
- **`localization` 不是工具参数**：只接受 env `DEEPSEEK_SEARCH_LOCALIZATION` 或程序化传入的 IP，避免模型瞎猜 IP。
- **计费与限速**（以官方文档为准）：Search 按成功请求计费，约 5 元 / 1000 次；失败、无结果、超时不计费；账号级 QPS 约 100。
- **备用通道是公共端点**：TinyFish keyless MCP，可能被限流、证书异常或不可用；此时只影响降级质量，不影响 DeepSeek 主通道。
- **依赖 OpenCode v2 的 `ctx.tool.transform`**：v1 宿主不适用。
- **覆盖同名 `websearch` 工具**：如果同时安装了其它也覆盖 `websearch` 的插件，后加载者生效；请只保留一个。

## 开发与测试

```
opencode-ds-websearch/
├─ src/index.ts           # 插件入口（Plugin 默认导出）
├─ tests/index.test.ts    # 30 项单测：参数拼接、重试、降级、格式化、注册形状
├─ package.json           # exports "." -> src/index.ts
├─ README.md
└─ LICENSE
```

```bash
bun install     # 无依赖，可跳过
bun test        # 全部桩测试，不发真实网络请求
```

手工验证（会消耗真实额度）：

```bash
DEEPSEEK_API_KEY=sk-... bun -e '
import { search, format } from "./src/index"
console.log(format(await search({ query: "DeepSeek", count: 2 })))
'
```

常改的常量都在 `src/index.ts` 顶部：

| 常量 | 默认 | 作用 |
| --- | --- | --- |
| `COUNT_DEFAULT` / `COUNT_MAX` | 8 / 50 | 默认与最大条数 |
| `QUERY_MAX` | 128 | 查询长度上限 |
| `PER_HIT_CONTENT_CHARS` / `TOTAL_CONTENT_CHARS` | 3000 / 12000 | 正文预算 |
| `SUMMARY_CHARS` / `SNIPPET_CHARS` / `TITLE_CHARS` | 500 / 240 / 160 | 文本截断 |
| `LOW_SCORE` | 0.8 | 低相关度标注阈值 |
| `RETRY_ATTEMPTS` / `RETRY_BASE_MS` / `RETRY_MAX_WAIT_MS` | 3 / 600 / 3000 | 重试策略 |
| `DS_TIMEOUT_MS` / `DS_TIMEOUT_CONTENT_MS` | 15000 / 25000 | 超时 |
| `DS_SEARCH_URL` / `TINYFISH_URL` | 见文件 | 端点，可被测试覆盖 |

## 安全与隐私

- 代码中**不含任何密钥**，输出与日志中也**不会打印 Key**。
- 只向两个域名发请求：
  - `api.deepseek.com`：搜索主通道（携带你的 Key）
  - `agent.tinyfish.ai`：**仅在主通道失败或无结果时**发出查询文本作为补查
- 因此不要在查询里放敏感信息；如果不想让查询离开 DeepSeek，可自行把 `tinyfishSearch` 调用去掉（`src/index.ts` 内 `search()` 的降级分支）。
- Key 只从 env / 本机配置读取，不写盘、不上传。

## FAQ

**Q：为什么老是显示「DeepSeek 搜索不可用」，结果来自 TinyFish？**
A：看顶部原因：`401` 是 Key 无效，`402` 是余额不足，`429` 是限流（等几秒再试），超时/5xx 可重试。Key 与本机配置按上文顺序解析。

**Q：为什么 DeepSeek 返回 0 条？**
A：筛选太窄最常见（站点 + 时间 + 排除词叠加）。先去掉 `site`/`after` 重试；无意义关键词通常不会返回 0 条，而是低分噪声——留意「相关度普遍偏低」提示。

**Q：结果相关度只有 0.4，还能用吗？**
A：能。低于 0.8 只是标注「（低）」。这类结果常见于冷门站点、新发布页面、论坛帖，是否需要由你判断。

**Q：为什么没有 `webfetch` 工具？**
A：DeepSeek 的 Fetch API 是另一个端点（`/v1/tools/fetch`）。本插件只做搜索；读整页用 OpenCode 内置 `webfetch`，或参考 README 的「开发」自行加。

**Q：同事怎么用？要不要把 Key 发给他们？**
A：不要。给他们插件文件或仓库地址，各自设置自己的 `DEEPSEEK_API_KEY`，或各自在 `opencode.json` 填自己的 provider Key。插件代码不含 Key。

**Q：能同时用别的搜索插件吗？**
A：会冲突。多个插件注册同名 `websearch` 时只有最后加载的生效，请只保留一个。

## License

[MIT](./LICENSE) © 2026 2102014

本项目与 DeepSeek、OpenCode 官方无关；接口行为与计费以 [DeepSeek 官方文档](https://api-docs.deepseek.com/zh-cn/guides/search/) 为准。
