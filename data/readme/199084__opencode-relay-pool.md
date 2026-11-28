# opencode-relay-pool

[![npm version](https://img.shields.io/npm/v/opencode-relay-pool.svg?color=blue)](https://www.npmjs.com/package/opencode-relay-pool)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenCode Version](https://img.shields.io/badge/OpenCode-%3E%3D1.4.0-blueviolet.svg)](https://opencode.ai)

面向 [OpenCode](https://opencode.ai) 的企业级 OpenAI 兼容中转站集成插件。集成了 **动态模型自动发现** 与 **多 Key 故障转移（Failover）账号池**，解决自建网关或第三方中转站模型频繁变动、多 Key 手工配置繁琐、限流（429）无缝切换等痛点。

---

## 架构特性

```
┌─────────────────────────────────────────────────────────────┐
│                       OpenCode Client                       │
└──────────────────────────────┬──────────────────────────────┘
                               │ Fetch Request
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    opencode-relay-pool                      │
│  ┌───────────────────────┐       ┌────────────────────────┐ │
│  │   Dynamic Discovery   │       │   Failover Pool Mgmt   │ │
│  │  - GET /v1/models     │       │  - Weighted RR Policy  │ │
│  │  - Context Window Ext │       │  - Auto Quarantine     │ │
│  │  - Reasoning Support  │       │  - Exponential Backoff │ │
│  └───────────────────────┘       └────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────┘
                               │ Round-Robin with Fallback
                               ▼
            [ Key 1 ]      [ Key 2 (429冷却) ]      [ Key 3 ]
```

- **全协议兼容**：无缝对接 One-API、New-API、LiteLLM 以及任何标准 OpenAI 兼容（`/v1`）网关。
- **启动即发现**：启动时自动拉取中转站 `/v1/models`，自动解析模型上下文上限与 Reasoning 特性，自动注入 OpenCode 模型选择器。
- **多 Key 账号池**：单个 Provider 支持挂载多个 API Key，采用加权轮询（Weighted Round-Robin）调度分发。
- **智能错误识别与自动隔离**：
  - **HTTP 429 / 配额超限**：自动进入临时隔离冷却（默认 60 秒），自动切换至健康 Key。
  - **HTTP 401 / 403 鉴权失败**：自动永久隔离失效 Key，避免无意义重试。
  - **网络抖动（5xx / ETIMEDOUT）**：触发即时重试，无感切换可用节点。
- **实时管理工具**：向 Agent 注入 `relay_pool_status` 与 `relay_pool_reset` 工具，可在对话中实时查看 Key 状态与请求统计。

---

## 安装说明

在 OpenCode 项目根目录或全局插件目录中安装：

```bash
npm install opencode-relay-pool
```

在 `opencode.json` 中注册插件：

```json
{
  "plugin": [
    "opencode-relay-pool"
  ]
}
```

---

## 配置示例

在 `opencode.json` 中配置中转站 Provider：

```json
{
  "provider": {
    "my-relay": {
      "npm": "opencode-relay-pool",
      "options": {
        "baseURL": "https://api.your-relay.com/v1",
        "keys": [
          { "key": "sk-key-01", "weight": 5 },
          { "key": "sk-key-02", "weight": 2 },
          { "key": "sk-key-03", "weight": 1 }
        ],
        "discovery": {
          "enabled": true,
          "refreshIntervalMs": 3600000,
          "filter": ["deepseek-*", "claude-*", "gpt-4*"]
        },
        "pool": {
          "cooldownMs": 60000,
          "maxRetries": 3
        }
      }
    }
  }
}
```

---

## 配置参数详解

### `options` 根配置

| 字段 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `baseURL` | `string` | 是 | - | 中转站 API 基础地址（需包含 `/v1`） |
| `keys` | `Array<string \| KeyConfig>` | 是 | - | API Key 列表，支持纯字符串或带权重配置 |
| `discovery` | `DiscoveryConfig` | 否 | `{ enabled: true }` | 动态模型发现相关配置 |
| `pool` | `PoolConfig` | 否 | - | 账号池调度与隔离策略 |

### `DiscoveryConfig` 模型发现配置

| 字段 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `enabled` | `boolean` | `true` | 是否启用启动时动态模型探测 |
| `refreshIntervalMs`| `number` | `0`（不轮询） | 后台定时刷新模型列表周期（毫秒） |
| `filter` | `string[]` | `["*"]` | 模型白名单过滤规则（支持 通配符） |

### `PoolConfig` 账号池配置

| 字段 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `cooldownMs` | `number` | `60000` | 触发 429 后的临时冷却隔离时间（毫秒） |
| `maxRetries` | `number` | `3` | 单次请求在 Key 池中的最大故障转移尝试次数 |

---

## 进阶管理工具

插件自动为 Agent 提供以下系统级排障工具：

- **`relay_pool_status`**：查看当前 Provider 的 Key 池存活状态、健康度、隔离倒计时以及调用统计。
- **`relay_pool_reset`**：手动重置指定 Provider 的 Key 隔离状态，立即恢复所有节点的调度。

---

## 开源协议

本项目基于 [MIT 协议](LICENSE) 开源。
