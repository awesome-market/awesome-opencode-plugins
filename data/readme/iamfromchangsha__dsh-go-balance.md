# dsh-go-balance

[![Awesome DSH Plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com/)

给 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（DSH）Web 界面加一个 **OpenCode Go 订阅余额**小部件：在输入框工具行右侧（发送按钮旁）显示滚动 / 每周 / 每月三个配额窗口的**剩余百分比**，数据直接来自 OpenCode Zen 用量接口（Go 订阅仪表页同源），不是估算值。

[English](./README.en.md)

## 功能

- **真实余额，非估算** — 用您的 Go API 密钥轮询 `https://opencode.ai/zen/go/v1/usage`，渲染与 Go 仪表页完全一致的数字。
- **紧凑胶囊** — `Go 96% · 94% · 97%`（滚动 / 每周 / 每月剩余），位于发送按钮右侧。
- **悬停明细** — 已用百分比、各窗口重置时间、数据更新时间。
- **警示配色** — 任一窗口剩余低于 30% 变黄、低于 15% 变红。
- **容错** — 刷新失败保留上次快照并淡化标记；未配置凭据或尚无数据时不渲染。
- **凭据安全** — API 密钥运行时经 DSH 凭据服务解析（`OPENCODE_ZERO_API_KEY`），只留在 host 进程内；本仓库不含任何密钥，也不会下发到浏览器。

## 截图

![输入框工具行右侧的余额胶囊](docs/screenshot-composer.png)

![悬停明细](docs/screenshot-tooltip.png)

![低余额警示配色](docs/screenshot-warn.png)

## 安装

```sh
dsh plugin --profile web add dsh-go-balance
```

然后重启 DSH（`dsh web`）。插件会自动加入 profile 的 bundle 层，无需其他配置。

也可以直接从 GitHub 仓库安装（例如镜像源尚未同步时）：

```sh
dsh plugin --profile web add github:iamfromchangsha/dsh-go-balance
```

本地开发目录安装：

```sh
# 在插件仓库目录下执行（相对路径锚定到当前目录）
dsh plugin --profile web add file:./
```

## 凭据

插件通过 DSH 凭据服务读取 **`OPENCODE_ZERO_API_KEY`**（`$DSH_HOME/.credentials.yaml` 或进程环境变量，即您 Go 订阅的 API 密钥），每次刷新时在 host 进程内解析。

## 配置

bundle 行暴露一个可选键：

| 键 | 默认值 | 含义 |
|---|---|---|
| `intervalMs` | `60000` | host 轮询 OpenCode Zen 用量接口的间隔（毫秒）。 |

在 profile 补丁层（`$DSH_HOME/profiles/web/cordis.patch.yml`）覆盖：

```yaml
- id: go-balance
  config:
    intervalMs: 120000
```

## 原理

一个 npm 包承载插件的两个半边：

- **节点半边**（`lib/index.js`）— `goUsage` 服务：经 `ctx.credentials` 解析 `OPENCODE_ZERO_API_KEY`，定时轮询 Zen 用量接口（请求发现缓存超过 30 秒也会顺手刷新），校验响应结构后在 `GET /go-usage` 提供快照。
- **浏览器半边**（`lib/client.js`）— 注册进 `conversation.input.right` 插槽（输入框工具行右端），每 60 秒以及标签页重新可见时拉取 `/go-usage`。

### 安全与健壮性

- **并发去重** — 刷新调用共享同一个在途 Promise，定时器与懒刷新永远不会并发打到上游 API。
- **错误脱敏与密钥安全** — 返回浏览器的错误只含 `code`（和可选的 HTTP `status`）；DNS 失败等内部细节仅写入 host 日志，且日志中的密钥串一律替换为 `[REDACTED]`。密钥只经 `Authorization: Bearer` 发给 opencode.ai，仅存在于 host 进程内存，不落盘、不进日志、不过 `/go-usage`。
- **路由防护** — DSH webServer 本身不强制鉴权（"No TLS, auth, or origin policy"），默认只绑定回环地址即为边界；`/go-usage` 另拒绝非回环 `Origin` 的浏览器跨站读取（403），并带每地址 120 次/分钟的内存级速率限制（429）。快照只含配额百分比与重置时间，绝不含密钥或身份信息。
- **范围校验** — `percent` 必须是 `[0, 100]` 内的有限数字，上游返回畸形值会丢弃整份快照并保留上次有效数据。

## 开发

```sh
node --check lib/index.js && node --check lib/client.js
```

`lib/client.js` 随仓库提交并随包发布，安装时无需构建。

## 已知限制

- 需要有效的 OpenCode Go 订阅，且 DSH host 上配置了 `OPENCODE_ZERO_API_KEY` 凭据。
- 仅支持 Web 界面（渲染的插槽属于 DSH Web UI）。
- 快照是面向用户的账户额度参考，不是计费记录。

## License

[MIT](./LICENSE)
