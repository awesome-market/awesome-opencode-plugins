<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="全平台退费助手 — 年费、自动续费、课程、预付卡，不管在哪买 — 先判四要素（支付主体 / 付费形态 / 消耗程度 / 条款提示），再按渠道顺序处理，给出可复制话术与人工申请模板。">
</p>

# lhg-refund · 全平台退费助手

年费、自动续费、课程、预付卡、虚拟商品，不管在哪个平台想退费，先判四要素再选路径，附 12 平台专属话术与人工申请模板。

（SKILL.md v2.1.1）

## 它是什么

- 四要素先判：支付主体 / 付费形态 / 消耗程度 / 条款提示。
- 再按渠道顺序升级：客服 → 支付争议 → 12315 → 诉讼。
- 12 个平台专属话术（见 `references/platforms/INDEX.md`），照抄就能发。
- 7 份人工申请模板：自动续费、课程、数字商品、预付卡、正式函件、12315 投诉、线下预付。
- 扣子（coze.cn）为已实测自动化模块；iOS 内购、苹果渠道、预付卡等走对应专项模块；未覆盖平台走指导版。

## 先试一句

| 你说 | 它给你 |
|---|---|
| 想退掉 X 平台的年费 | 先判四要素，再选路径，给可复制话术 |
| 自动续费扣了钱能退吗 | 按渠道顺序升级，模板照抄就能发 |
| iOS 内购想退款 | 走苹果渠道专项模块，不找平台客服 |

## 安装

```bash
npx skills add lhg-skills/lhg-refund
```

<details>
<summary>发给 Agent 的安装话术（推荐：小白用户直接复制整段发给你的 Agent）</summary>

> 请帮我安装 Skill「lhg-refund」：先从 Gitee 上 lhg-skills 组织下的 lhg-refund 仓库下载；如果 Gitee 无法访问或下载失败，改从 GitHub 上 lhg-skills 组织下的同名仓库下载。按当前 Agent 的规范安装其中的 Skill，优先全局安装，保留完整目录和依赖。请直接执行，完成后验证是否安装成功，告诉我实际使用的来源、安装的版本号以及如何调用；遇到访问或安装限制请说明具体原因。需要输入管理员密码或确认风险时停下来等我。

**怎么算装好了**：Agent 能在已安装的 Skill 里看到 `lhg-refund`，并报出版本号（与仓库 `SKILL.md` 的 `version` 一致）。只是打开了仓库网页不算安装。

</details>


## 它怎么做

1. 判四要素
2. 选四条路径
3. 按渠道顺序升级
4. 可复制话术
5. 人工申请模板

自动化优先级见 [references/automation-roadmap.md](references/automation-roadmap.md)：12 个平台里只有 3 个值得做自动化。

## 什么时候用 / 不用

**用它，当你：**

- 年费、自动续费、课程、预付卡、虚拟商品想退费
- 不知道找谁、说什么、按什么顺序升级
- 要照抄就能发的话术与模板

**别用它，当你：**

- 开口就说「你们诈骗」——对方直接转法务
- iOS 内购去找平台客服——钱在苹果账上，平台无权退
- 只打一个渠道就放弃——在线客服拒绝就升级渠道

## 目录结构

```
SKILL.md            skill 全文
references/
  decision.md         四要素判定
  channels.md         渠道升级顺序
  platform-scripts.md 12 个平台专属话术
  platforms/          12 个平台专属文档
  automation-roadmap.md 自动化优先级
templates/          7 份人工申请模板
automation/         已实测自动化模块（扣子）
scripts/            发布脚本
LICENSE             MIT
manifest.yaml
```

## 自检与反馈

本仓库没有脚本冒烟测试；自检方法是按 SKILL.md 走一遍「判四要素 → 选路径 → 话术」：四要素缺一项就停下，话术必须与 `references/platforms/INDEX.md` 里的 12 个平台对应得上。

发现问题请提 issue：[提一个 issue](https://github.com/lhg-skills/lhg-refund/issues/new)（标题以 `[QC] ` 开头，写清你让它做了什么、它实际给了什么）。

---

## 出品：刘洪光

本 skill 由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 抖音：搜「刘老师讲AI实战」
- 微信：lhgsmsw

觉得有用，欢迎点 ⭐ Star。
