# dsh-plugin-zen-useragent

> A DeepSeek Harness (DSH) plugin that lets provider-configured request headers
> (e.g. `User-Agent`) reach the `pi-ai` API requests and fixes the OpenCode ZEN
> free model errors — `429 FreeUsageLimitError`, `400 MissingSessionID`,
> `401 api_key_expired` (reported by DSH as "API key invalid/expired") and
> `403 Generation.FreeTierError` (reported by DSH as "API key invalid") — by
> identifying requests as the opencode client instead of `deepseek-harness`,
> carrying a **real, account-known session ID** read from your local opencode
> client database (v1.5.0+: the patched request headers re-resolve the session
> at runtime every 60s, so new conversations / session invalidation / account
> switches are picked up **without restarting DSH**), and (v1.6.0+)
> authenticating with the opencode client's **OAuth access token** (`st_…`)
> instead of the Zen API key — which **expires** and is what actually produced
> `401 api_key_expired` for DSH.

修复 DSH 中 OpenCode ZEN 免费模型 `429 FreeUsageLimitError: Rate limit exceeded`
、`400 MissingSessionID`、`401 api_key_expired`（DSH 误报为「API 密钥失效 /
无效」）与 `403 Generation.FreeTierError / FreeTierError`（DSH 误报为「API 密钥
无效」）等问题的插件。会话（v1.5.0+）与认证（v1.6.0+）都在运行时自动跟随本机
opencode 客户端，均无需重启 DSH。

> ⚠️ **已知限制（首次安装 / DSH 升级后务必重启一次）**：DSH 的 loader 并行导入
> 各入口模块，全新安装后的**第一次启动**（或 DSH 升级把补丁文件还原后的第一次
> 启动），若原生 `llm-pi-ai` 恰好先于本插件读到未补丁的文件，该次启动仍按原生
> 行为运行；补丁当次落盘，**重启 DSH 后生效**。此后每次启动日志显示
> `already patched`，零额外开销。判断标准：启动日志出现 `patched:` /
> `upgraded:` 时建议再重启一次确认生效；出现 `already patched` 即为生效状态。

## 原理

原生 `@deepseek-ai/dsh-llm-pi-ai` 的 `requestHeaders()` 会把与 attribution headers
冲突的自定义请求头（如 `User-Agent`）**过滤掉**，实际发给 API 的 always 是
`user-agent: deepseek-harness/0.1.0-rc.6 (+https://github.com/deepseek-ai/deepseek-harness)`。

OpenCode ZEN（`https://opencode.ai/zen/v1`）按客户端标识限流/鉴权。

本插件对两处做补丁：

1. **请求头**（`@deepseek-ai/dsh-llm-pi-ai/lib/index.js` 的 `requestHeaders`）：
   允许 provider 配置的 headers 覆盖 attribution，对指向 opencode 的请求自动补全
   opencode 身份头，并用本机 opencode 客户端的 OAuth 令牌覆盖 provider 那把会
   过期的 `sk-` key；
2. **请求体**（`@earendil-works/pi-ai/api/openai-completions` 的
   `buildParams`）：向 OpenCode Zen 网关的请求 `body.tools` 里在缺失时补一个名为
   `read` 的**空壳工具**（网关判定必需）。

### ZEN 免费档的判定条件（v1.6.0 逐一消融实测）

对真实网关（`https://opencode.ai/zen/v1/chat/completions`）做全量消融实验，
免费档判定**只看三件事**：

1. **`User-Agent` 以 `opencode/` 开头**（任意版本都行，如 `opencode/1.18.32`；
   `axios/…` 或缺失 → 403）；
2. **`x-opencode-session` 是账号已知会话**（真实客户端创建过的会话 ID；
   随机/自造 id → 403）；
3. **`body.tools` 含一个名为 `read` 的函数工具**（`tools:[<read>]` → 200；
   `[]` / `[foo]` / `[bash]` / `[shell]` / `[edit]` / `[glob]` / `[grep]` /
   `[write]` / `[pwsh]` 等一律 403；数量 / 描述 / JSON Schema 都不校验）。

其余一概**不参与**判定：`x-opencode-project`、`x-opencode-org-id`、
`x-opencode-client`、`x-opencode-request-id`、`b3`、`traceparent` 有没有都不影响。

> ⚠️ **修正（v1.6.0）**：v1.4.2 曾误判为「必须有 `read` + `bash`/`shell`
> 组合」，因此注入的是 `bash` 空壳 —— 实测 `[bash]` 单独**并不通过**（403），
> 关键是 `read`。DSH 默认工具集本就含 `read`，所以当时那个补丁实际未改变判定
> 结果（无害但无效）。v1.6.0 已把它修正为**缺失 `read` 时才补一个 `read` 空壳**。
> 补丁只影响 provider 名为 `opencodezen` 或 baseUrl 含 `opencode` 的请求，
> 非 opencode 网关完全不变。

### 认证：401 api_key_expired 的真因（v1.6.0 新增修复）

免费档**并不要求认证**：不带 `Authorization` 的请求同样 200。但如果你带了
**已过期的**凭证，网关会返回
`401 {"error":{"code":"api_key_expired","message":"This API key has expired…"}}`
——DSH 把它显示成「API 密钥失效 / 无效」，这就是「过一段时间 DSH 又开始报错」的
真因：**Zen 免费档 API key（`sk-…`）会过期**，官方 opencode 客户端早已改用
**OAuth 访问令牌（`st_…`）**，而你 profile 里配的 `OPENCODEZEN*_API_KEY`
（`sk-…`）早晚会过期。

因此 v1.6.0 起，插件在运行时从本机 opencode 客户端数据库读取 OAuth 令牌并覆盖
它：

- **令牌有效** → `Authorization: Bearer st_…`（账号归属、配额正确）；
- **令牌过期 / 缺失 / DB 不可读** → `Authorization` 被**显式置空**
  （`null`，openai SDK 会把该头整个丢掉）→ 走免费档匿名路径，仍然 200，
  **绝不 401**。

OAuth 令牌存放位置（插件自动读取，无需你处理）：`~/.local/share/opencode/
opencode.db` 的 `credential` 表里 `active=1` 的
`{"type":"oauth","access":"st_…","refresh":"rt_…","expires":…}`；令牌过期时
**运行一次 opencode 客户端**即会自动刷新。

### 补丁后的行为（v1.6.0）

**请求头补丁**（`requestHeaders`）：

1. 允许 provider 配置的 headers 覆盖 attribution（解决 429）；
2. 当合并后的 `User-Agent` 含 `opencode`（即该 provider 指向 opencode Zen/Go
   网关）时，**自动补全**缺失的 opencode 身份头（解决 400/403），并据此把请求
   伪装成真正的 `opencode` 深度求索（DeepSeek-Harness）客户端：
   - `x-opencode-client: cli`
   - `x-opencode-session: ses_<…>` —— **真实会话，运行时自愈（v6）**：补丁体内置
     一个运行时会话解析器（60s TTL 缓存），按
     `session_v2 → session` 表读取本机 opencode 客户端数据库
     （`~/.local/share/opencode/opencode.db`；node:sqlite 不可用/损坏时回退为
     8MB 分块二进制扫描，适配超过 512MB 的大 DB）里最近更新的「账号已知」会话
     ID。因此**用户在 opencode 里新开对话 / 会话被服务端作废 / 换账号，无需
     重启 DSH**，下一个请求自动采用最新会话（保留 last-known-good：解析暂时
     失败时不降级回旧值或丢掉会话）。启动时解析出的会话烘焙为字面量**兜底值**，
     仅在运行时 DB 完全不可读时使用；再退化为进程内随机生成。结构为 `ses_` +
     12 位小写 hex + 14 位字母数字（`ses_[0-9a-f]{12}[0-9A-Za-z]{14}`）。
     网关校验该会话是否属于账号已知会话（具体启用日期无官方公告；按实际使用
     记录推断约在 2026-10 月中旬前后生效 —— 在此之前 DSH 用自造会话仍可用）。
     **自造/全新会话一律 `403 FreeTierError`**（DSH 误报「API 密钥无效」）——
     这是 v1.4.2 修复的核心，v1.5.0 只是把这个真实会话的来源从「启动时定死」
     升级为「运行时自动跟随」。
   - `x-opencode-request-id: msg_<…>` —— 每次请求随机，结构为 `msg_` + 12 位
     小写 hex + 14 位字母数字（`msg_[0-9a-f]{12}[0-9A-Za-z]{14}`）
   - `Authorization`（v7）—— 用本机 opencode 客户端的 **OAuth 令牌**覆盖 provider
     配置的那把（会过期的）`sk-` key：令牌有效 → `Bearer st_…`；令牌无效/缺失 →
     **显式置 `null`**（SDK 省略该头）。因此绝不会再发出过期的 `sk-`，401
     `api_key_expired` 从根上消除；令牌每 60s 自动重读、过期后运行一次 opencode
     即刷新，无需改配置或重启。
3. 头名与格式都严格对齐真实 opencode CLM 客户端（网关逐位校验）：
   - 请求头名是 `x-opencode-request-id`（不是 `x-opencode-request`）；
   - **不注入** `x-opencode-project`（真实 CLM 客户端不带这个头）。
4. **显式配置永远优先**：你在 provider headers 里手写了同名头（含
   `Authorization`），就按你写的来，自动补全/覆盖不会动它（注意手写的
   `x-opencode-session` 固定值也必须是账号已知会话，否则同样 403）。

**请求体补丁**（`openai-completions` 的 `buildParams`）：

1. 仅对 provider 名为 `opencodezen` 或 baseUrl 含 `opencode` 的请求生效；
2. 同时适配 pi-ai ≥ 0.87（`transcriptTools.requestTools` 结构）与旧版
   （`activeTools` 结构）；
3. tools 里没有 `read` 时，追加一个 `read` 空壳（放在数组末尾，不影响原有工具；
   DSH 默认已有 `read`，故通常不追加）；
4. 幂等 —— `read` 已存在则不重复追加。

## 原理（v1.6.0 实现）

同一把 API Key 在 OpenCode TUI 里正常，在 DSH 里报错，就是这个原因。

本插件的 `cordis.patch.yml` **不改动原生 `llm-pi-ai` 入口**（保持唯一、直接挂载，
因此 DSH 模型页 —— ConfigEditor —— 可以正常增删改 provider；这是 v1.4.0 的核心
修复，旧版「禁用原生行 + 插入同名包装行」会造成两条 `llm-pi-ai` 行，模型页任何
写入都会报 `Configuration for "llm-pi-ai" is overridden by a home patch or command-line overlay`），
而是**额外插入一个独立入口 `zen-useragent`**，该模块每次启动时对磁盘上的
`requestHeaders` 与 pi-ai `openai-completions` 幂等落盘补丁，原生模块加载时读到的
就是已补丁的文件。补丁失败不会中断启动，会回退为原生行为。

时序与生效：见顶部「已知限制」—— 安装/升级后重启一次确认生效；DSH 升级会
自动重新打补丁，修复不会因升级而失效。

## 安装

```bash
# 1. 安装 pnpm（如已有可跳过）
npm install -g pnpm

# 2. 安装插件到 web profile（推荐：从 GitHub 源）
dsh plugin --profile web add github:jiujiezongheti/zen-useragent

#    或从 npm 安装
dsh plugin --profile web add dsh-plugin-zen-useragent
```

**升级 v1/v2/v3/v4/v5 用户**：直接重装/更新插件后重启 DSH 即可。启动时会检测到旧
补丁并自动升级，日志打印 `upgraded: ...` / `patched: ...`，无需手动改动任何文件或
配置：

- v5 → v6：把会话从「启动时烘焙定死」升级为「运行时自愈（60s 跟随 DB）」；
- v6 → v7：新增 OAuth 认证覆盖（修复 `401 api_key_expired`）。

API Key 不再需要（免费档不强制认证，插件会优先用客户端 OAuth 令牌），但保留
profile 里的 `apiKeyEnv` 配置也无妨 —— 插件会在发送前把它换成有效令牌或省略。

## 启用

1. 配置 opencodezen provider。DSH 的 provider 配置现在位于 profile 层的
   `cordis.patch.yml`（`$DSH_HOME/profiles/<profile>/cordis.patch.yml`），不再是旧的
   `settings.yaml`。v1.4.0 起插件**不再内置默认 provider**，需要在 profile 层配置
   一个指向 opencode 网关的 provider（headers 必须带 `User-Agent` —— 解决 429
   必需）：

   ```yaml
   - id: llm-pi-ai
     config:
       providers:
         opencodezen:
           displayName: opencode
           apiKeyEnv: OPENCODEZEN_API_KEY
           api: openai-completions
           baseURL: https://opencode.ai/zen/v1
           headers: { User-Agent: opencode/1.18.18, Referer: https://opencode.ai }
           models: [...]
   ```

   对应 API Key 放在 `$DSH_HOME/.credentials.yaml`（web profile 下即
   `C:\Users\...\.dsh\.credentials.yaml`）。

2. `x-opencode-*` 身份头**无需手写**——插件的自动补全会按上面的规则生成。

3. 重启 DSH Web（插件在启动时执行补丁，改配置/装插件后必须重启；全新安装的
   第一次启动若日志显示 `patched` / `upgraded`，建议再重启一次确认生效）。

4. 启动时终端会打印几行确认（会话来源 + 认证 + 两处补丁）：
   ```
   [dsh-plugin-zen-useragent] zen session: ses_00000000000000000000000000 (from opencode client DB)
   [dsh-plugin-zen-useragent] zen auth: OAuth token active (expires 2026-11-17T04:36:02.947Z)
   [dsh-plugin-zen-useragent] upgraded: C:\...\dsh-llm-pi-ai\lib\index.js
   [dsh-plugin-zen-useragent] patched: C:\...\@earendil-works\pi-ai\dist\api\openai-completions.js
   ```
   「zen auth」一行可能是 `OAuth token active` / `stored OAuth token EXPIRED`
   / `no OAuth token found`；后两种情况下请求会**省略 Authorization**（免费档
   匿名路径，同样 200）；想恢复账号归属，运行一次 opencode 客户端刷新令牌即可。
   依次可能出现的状态：`patched`（从原生打补丁）、`upgraded`（旧补丁升级）、
   `already patched`（已是新版）。若输出 `READONLY: ...` 或 `WRITE FAILED: ...`，说明安装目录不可写，
   修复未生效（补丁失败不会中断启动，会回退为原生行为）——修复权限或改用本地安装。
   若缺第二条（`could not locate ... pi-ai`），说明 pi-ai 路径变化，tools 补丁未生效
   （仅请求头补丁生效）。若「zen session」一行是警告（找不到会话），插件会自动尝试用
   官方 opencode CLI 无头创建一个真实会话（首次尝试当天内不再重复）；仍失败的机器，
   请先运行一次官方 opencode 客户端（开任意一个对话）再重启 DSH。
   即使拿到了会话也不必担心它过时：补丁体内的运行时会话解析器每 60s 重新解析
   一次最新会话（v6），平时无需干预。

### 会话 ID 从哪来？

`x-opencode-session` 不再由插件自造，而是按下面的优先级拿一个「账号已知」的
真实会话（网关近期只认账号已知会话，自造必 403 FreeTierError）：

1. **本机 opencode 客户端数据库**（`~/.local/share/opencode/opencode.db` 的
   `session_v2` 表最近更新的一条；历史路径 `~/.opencode/opencode.db` 也支持；
   优先 node:sqlite 精确读取，不可用时回退为 **8MB 分块二进制扫描** —— 真实
   用户的 DB 可能超过 512MB，整文件扫描会字符串超长，分块+重叠保证不丢会话）
   ——这些会话属于你的 opencode 账号，网关认它们。**v6 起不仅有启动时解析，
   补丁体内还内置了同样的运行时解析器（60s TTL）**：opencode 里新开对话、
   会话被服务端作废、换账号，都不需要重启 DSH；
2. **遗留 storage**（`storage/session_diff|message` 等目录里出现过的会话 ID，
   取最近修改的文件）——DB 完全读不到时的再兜底；
3. **自动用官方 CLI 无头创建**：DB 与 storage 都为空（典型场景：装了这个插件但
   **从未运行过 opencode**）时，插件会调用本机已安装的官方 opencode CLI。先试
   轻量命令 `opencode session list --format json`（秒级、不跑模型；DB 读不到但
   CLI 能读时直接拿已有会话），拿不到再 `opencode run ping --model
   opencode/big-pickle` 让真实客户端创建并同步一个会话；且 run 即使因限流返回
   非零，会话往往已创建，插件会先重新解析 DB 再放弃。自动尝试**每天最多一次**
   （临时目录标记），避免反复白跑；
4. 以上都失败时（没有 CLI / 未登录 / 网络不通），日志会给出明确指引：
   **运行一次官方 opencode 客户端（开任意一个对话即可），然后重启 DSH**。

要求本机**用 opencode 官方客户端登录过**（只要登录过一次，DB 里就有会话，会一直
有效）。换账号登录 opencode 后，无需重启 DSH —— v6 运行时解析器会在 60s 内自动
采用新账号的会话。

### 想要永久固定会话 ID？不推荐

会话来自你本机 opencode 客户端的真实数据库，随客户端自动更新，无需干预。如果你
确实想在 provider headers 里手写 `x-opencode-session`，注意**任意自造值会被网关
拒绝（403）**，必须写你账号下真实存在（出现过）的会话 ID（启动日志里
`zen session:` 打印的那个）。手写后自动补全会尊重它：

```yaml
headers:
  User-Agent: opencode/1.18.18
  Referer: https://opencode.ai
  x-opencode-session: ses_00000000000000000000000000
  x-opencode-client: cli
  x-opencode-request-id: msg_abcdef012345uvwxyzABCDEFGH
```

## 验证

重启后切到 opencode 免费模型发一条消息，如不再 429 / 400 / 401 / 403 即成功。
终端日志出现 `already patched` 表示此前已被补丁，无需重复操作。
若仍报 `401 api_key_expired`，说明补丁未生效（多半是装/升级后只启动了一次，
按顶部「已知限制」再重启一次即可）。

## 卸载

```bash
dsh plugin --profile web remove dsh-plugin-zen-useragent
```

卸载后需要重启 DSH，且被补丁的文件会保留（无害：只是允许自定义请求头覆盖
attribution、并自动补全 opencode 身份头）。如需彻底还原，可重装最新版 DSH。

## 备注

- **前提**：真实会话 ID 与 OAuth 令牌都来自本机 opencode 客户端数据库，要求这台
  机器用 opencode 官方客户端**登录过一次**（在任何对话界面登入即可）。没有数据库
  时插件降级为随机会话 + 省略认证（仍会注入身份头，但会话自造会被网关 403），且会
  在启动日志打警告。
- 补丁只影响「provider 显式配置了同名请求头」或「请求带 opencode UA」的情况；
  未配置 headers 的 provider 行为与原生完全一致（非 opencode UA 也不会注入身份头、
  不会覆盖 Authorization）。tools 补丁只影响 provider 名为 `opencodezen` 或
  baseUrl 含 `opencode` 的请求。
- 若 DSH 升级后函数结构变化导致"无法识别"，插件会打印
  `SKIPPED: unrecognized requestHeaders shape`（或 pi-ai 的
  `SKIPPED: unrecognized tools shape`）并保持不破坏新代码 —— 此时升级本插件即可。
- 补丁可靠性措施：
  - `requestHeaders` 的定位按**花括号配平**执行（跳过字符串、模板字符串与注释里
    的括号），函数体内出现行首闭合的嵌套对象也不会被截断写坏；
  - pi-ai `openai-completions` 的替换锚点选取 `buildParams` 主分支的唯一文本：
    优先 pi-ai ≥ 0.87 的
    `params.tools = convertTools(transcriptTools.requestTools, compat);`
    （首个唯一出现处），旧版回退 `if (activeTools && activeTools.length > 0) {`
    之后的首个 `params.tools = convertTools(activeTools, compat);`；替换后做
    三重校验（新标记存在、原生结构保留、周边未破坏）；
  - 替换结果写盘前做三重校验（旧特征行已消失、标记已存在、函数唯一），任一不满足
    即拒绝写盘（打印 `SKIPPED:`）;
  - 落盘采用**原子写**（同目录临时文件 + rename，Windows 上 rename 被占用时回退
    直接写），并发启动的进程不会读到写了一半的文件；
  - 目标只读或写入失败时打印 `READONLY:` / `WRITE FAILED:` 并跳过，**不会中断 DSH
    启动**，请求回退为原生行为。
- 补丁算法在 `lib/patch-core.js`（纯函数），单测见 `test/patch-core.test.mjs`，
  运行 `node test/patch-core.test.mjs`。