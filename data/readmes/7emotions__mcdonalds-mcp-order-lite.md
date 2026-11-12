<p align="center">
  <img src="https://www.mcdonalds.com.cn/favicon.ico" width="80" alt="McDonald's" />
</p>

<h1 align="center">麦当劳 MCP 点餐助手</h1>

<p align="center">
  基于麦当劳官方 MCP 接口的 OpenCode Skill，用自然语言完成点餐。
  <br />
  <a href="#安装"><strong>安装 &raquo;</strong></a>
  ·
  <a href="#使用示例"><strong>使用示例 &raquo;</strong></a>
  ·
  <a href="#工具参考"><strong>工具参考 &raquo;</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.2.0-blue" alt="version" />
  <img src="https://img.shields.io/badge/platform-OpenCode-green" alt="platform" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="license" />
</p>

---

## 目录

- [功能](#功能)
- [快速开始](#快速开始)
- [安装](#安装)
  - [面向人类](#面向人类)
  - [面向 LLM Agent](#面向-llm-agent)
- [使用示例](#使用示例)
- [点餐场景](#点餐场景)
- [工具参考](#工具参考)
- [配置](#配置)
- [错误处理](#错误处理)
- [文件结构](#文件结构)
- [贡献](#贡献)
- [许可](#许可)

## 功能

| 场景 | 说明 |
|---|---|
| 麦乐送到家 | 查配送地址 → 选门店 → 浏览菜单 → 算价 → 下单 → 查进度 |
| 到店自取 | 搜附近门店 → 菜单浏览 → 下单取餐 |
| 得来速 | 车道取餐全流程 |
| 企业团餐 | 助餐服务、预算管理、多人配餐 |

**附加能力：**

- 优惠券查询、自动领券、券包管理
- 积分查询与商城兑换
- 餐品营养成分查询（热量、蛋白质、脂肪等）
- 当月营销活动日历

## 快速开始

对 LLM Agent 说 **我要吃麦麦**（触发词还可说麦当劳 / 点餐 / 领券），Agent 会自动加载 skill，引导你完成选地址 → 选门店 → 选餐 → 下单的完整流程。

![订单](./imgs/order.png)

然后大喊**我要吃麦麦**触发~~ATM~~猫猫芋头的付款功能

![ATM](./imgs/pay.jpg)

如果你在编排文档中落盘了你的喜好，一顿麦麦只需要喊两次「我要吃麦麦」，是不是很方便呢？

## 安装

### 面向人类

将下面这段话复制给你的 LLM Agent：

```markdown
参考 [INSTALL.md](https://raw.githubusercontent.com/7emotions/mcdonalds-mcp-order-lite/main/INSTALL.md) 安装麦当劳 Skill。
```

### 面向 LLM Agent

当人类用户将本文档链接发给你时，按以下步骤执行安装。

### 1. 克隆仓库

```bash
git clone <repo-url> ~/.agents/skills/mcdonalds-mcp-order-lite
```

### 2. 替换 Token

打开 `~/.agents/skills/mcdonalds-mcp-order-lite/SKILL.md`，找到前页中的 `Authorization` 头：

```yaml
headers:
  Authorization: Bearer <placeholder>
```

如果 token 是占位符，告诉用户去 [open.mcd.cn/mcp](https://open.mcd.cn/mcp) 登录麦当劳账号获取 Bearer token，拿到后替换进去。

### 3. 验证

```bash
ls ~/.agents/skills/mcdonalds-mcp-order-lite/SKILL.md
```

文件存在即安装成功。告诉用户「装好了，说『我要吃麦麦』就能点餐」。
## 使用示例

### 麦乐送到家

```
用户: 想吃麦当劳，送到家
助手: 好的！先看看你的配送地址。
      → 找到 1 个地址：南京理工大学学生宿舍南区26舍
      → 附近有 3 家门店可配送，选哪家？

用户: 第一家
助手: [展示菜单分类] 想吃什么？

用户: 随心配1+1
助手: [列出红区主食 + 白区小食] 怎么搭配？

用户: 汉堡包 + 中薯条
助手: 价格明细：
      汉堡包 ¥15.00
      中薯条 ¥15.50
      配送费 ¥6.00
      打包费 ¥1.90
      合计 ¥38.40
      确认下单？

用户: 下单
助手: 订单已创建！[支付链接] 请在 15 分钟内完成支付。
```


### 到店自取

```
用户: 附近有什么麦当劳
助手: 到店还是得来速？哪个城市？

用户: 到店，南京玄武区
助手: [列出附近门店]
```

### 优惠券

```
用户: 帮我领券
助手: [自动领取麦麦省可用券] 已领取 X 张优惠券！
```

## 点餐场景

| 场景 | `beType` | `orderType` | 备注 |
|---|---|---|---|
| 到店自取 | 1 | 1 | 不传 `beCode` |
| 麦乐送到家 | 2 | 2 | 需配送地址 |
| 得来速 | 5 | 1 | 必传 `beCode` |
| 企业团餐 | 6 | 2 | 需助餐服务 |

## 工具参考

### 核心流程

| 工具 | 说明 |
|---|---|
| `delivery-query-addresses` | 查配送地址列表 |
| `delivery-create-address` | 新建配送地址 |
| `delivery-query-stores` | 按地址查可配送门店 |
| `query-nearby-stores` | 到店场景搜附近门店 |
| `query-meals` | 查门店菜单 |
| `query-meal-detail` | 查餐品详情与特调选项 |
| `calculate-price` | 计算订单总价 |
| `create-order` | 创建订单 |
| `query-order` | 查订单状态与进度 |

### 优惠券与积分

| 工具 | 说明 |
|---|---|
| `query-store-coupons` | 查门店可用券 |
| `available-coupons` | 可领取的券列表 |
| `auto-bind-coupons` | 一键领取麦麦省券 |
| `query-my-coupons` | 我的券包 |
| `query-my-account` | 积分余额 |
| `mall-points-products` | 积分兑换商品列表 |
| `mall-product-detail` | 兑换商品详情 |
| `mall-create-order` | 积分兑换下单 |
| `mall-order-list` | 商城订单列表 |
| `mall-order-detail` | 商城订单详情 |

### 辅助

| 工具 | 说明 |
|---|---|
| `campaign-calendar` | 当月营销活动 |
| `list-nutrition-foods` | 餐品营养成分 |
| `now-time-info` | 当前时间 |

## 配置

MCP 服务器连接信息全部内嵌在 `SKILL.md` 前页的 `mcp:` 块中，无需额外配置文件。

**Token 轮换：** 如遇 401 错误，前往 [open.mcd.cn/mcp](https://open.mcd.cn/mcp) 重新获取 token，更新前页 `Authorization` 头。

## 错误处理

| 错误码 | 含义 | 处理方式 |
|---|---|---|
| 401 | Token 过期 | 前往 open.mcd.cn/mcp 重新获取 |
| 429 | 请求超频 | 等待 30 秒后重试 |
| 门店不支持配送 | 当前地址不可达 | 建议更换地址或选到店自取 |
| 菜品售罄 | 单品不可售 | 告知用户，推荐替代品 |

## 文件结构

```
.
├── SKILL.md     # Skill 定义、内嵌 MCP 配置、完整工作流
├── README.md    # 本文件
└── INSTALL.md   # 安装指南（详细版）
```

## 贡献

欢迎提交 Issue 和 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feat/amazing`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feat/amazing`)
5. 发起 Pull Request

## 许可

MIT
