# job-hunt · 远程求职投递 Skill

把「找工作」变成一条可复用、可审计的流程：**发现岗位 → 按规则筛选 → 批次预览 → 你确认 → 投递/沟通 → 结果核实 → 本地记账**。

不绑定平台账号，不依赖特定操作系统，任何能控制浏览器的 agent 都能用。你只负责登录和拍板，剩下的搜索、筛选、逐条投递、结果核对和记录由 agent 完成。

---

## 它能做什么

| 能力 | 说明 |
|---|---|
| 多平台找岗位 | BOSS 直聘、智联招聘、RemoteCN、远程.work、公司官网/V2EX 邮箱 |
| 按规则筛岗位 | 岗位类型、远程真实性、薪资门槛、公司风险四道闸 |
| 识别假远程 | 自动排除「远程面试」「远程面」这类面试方式远程、不是工作远程的岗位 |
| 公司主体核查 | 导入牛企查导出 CSV，或接白牛商查 API，把「招聘主体待核实」变成可追溯证据 |
| 批次预览 | 投之前给你一张表：公司、岗位、渠道、薪资、简历版本、将发送的内容 |
| 逐条投递/沟通 | 智联点「立即投递」，BOSS 点「立即沟通」，每条都核实页面状态 |
| 结果核实 | 只认页面证据（成功弹窗、按钮变「继续沟通」、消息「已发送」），点击不算成功 |
| 本地记账 | 追加式 JSONL 账本，支持查状态、统计、生成 HTML 报告 |
| 断点续跑 | 账本只追加不改写，中断、重启、换电脑都不丢历史 |

## 它不做什么

- **不替你登录**：扫码、短信验证码、密码都由你本人完成；agent 不读取、不保存任何凭证
- **不绕过平台风控**：遇到验证码、滑块、登录失效就暂停并告诉你，不换 IP、不硬绕
- **不伪造简历**：只用你提供的材料和确认过的表述，不编造经历、不夸大业绩
- **不代答笔试、不自动接受 offer、不承诺薪资和入职时间**
- **不群发骚扰**：一封邮件只投一个岗位，一句招呼只发一次

---

## 需要准备什么

### 1. 一个支持 Skill 的 agent

任何能加载 `SKILL.md` 的 agent 都可以，例如：

- **ZCode**：把本仓库放到 `~/.agents/skills/job-hunt/`（或项目内 `.agents/skills/job-hunt/`）
- **Claude Code**：放到 `~/.claude/skills/job-hunt/`
- 其他 agent：只要能读 `SKILL.md`、执行 shell、控制浏览器，按它的 skill 目录约定放置即可

### 2. 浏览器控制能力

agent 需要能打开网页、读取页面结构、点击按钮。ZCode 自带内置浏览器；其他 agent 可用 Playwright / CDP / 浏览器扩展任一方式。

> 没有浏览器能力时，skill 仍能做筛选和记账，但无法执行投递。

### 3. 招聘平台账号（按需）

| 渠道 | 要准备什么 | 备注 |
|---|---|---|
| BOSS 直聘 | 账号 + 手机（扫码登录） | 建议每天新沟通不超过 15-20 条 |
| 智联招聘 | 账号 + 完善在线简历 | 投递走在线简历，不是本地 PDF |
| 邮箱投递 | 已配置好的邮件客户端或 SMTP | 没配置就记「需用户处理」，不伪造发送 |
| RemoteCN / 远程.work | 部分岗位需要平台账号 | 按岗位提示操作 |
| 牛企查（可选） | SVIP 账号，用于导出企业核查 CSV | 会员权益不等于 API 授权 |
| 白牛商查（可选） | API Key，放在环境变量 `BAINIU_API_KEY` | 按次消耗额度，调用前会告知 |

**登录永远由你本人完成。** agent 只负责打开登录页、切到扫码模式，然后停下来等你。

### 4. Python 3（可选）

账本脚本只用了标准库，**没有第三方依赖**。

- 有 Python 3.8+：用 `scripts/jobhunt.py` 记账、统计、生成报告
- 没有 Python：按 `references/data-format.md` 直接写 JSONL，流程完全一样

---

## 安装

```bash
git clone https://github.com/a1271981054/job-hunt-skill.git ~/.agents/skills/job-hunt
```

或者手动复制整个目录到 agent 的 skill 目录。

项目内使用（只对当前项目生效）：

```bash
git clone https://github.com/a1271981054/job-hunt-skill.git .agents/skills/job-hunt
```

---

## 5 分钟上手

### 第 1 步：初始化账本

```bash
cd ~/.agents/skills/job-hunt
python3 scripts/jobhunt.py init
```

会创建：

```
~/.job-hunt/
├── config.json      # 筛选门槛、授权模式、简历设置
└── ledger.jsonl     # 空账本
```

### 第 2 步：改配置

打开 `~/.job-hunt/config.json`，至少确认这三项：

```json
{
  "salary_floor_fulltime_cny_month": 10000,
  "salary_floor_parttime_cny_month": 5000,
  "approval": "batch"
}
```

- `salary_floor_fulltime_cny_month`：全职月薪下限，低于它直接排除
- `salary_floor_parttime_cny_month`：兼职月薪下限
- `approval`：`batch`＝每批等你确认（默认，推荐）；`auto`＝按规则自动执行

### 第 3 步：在对话里发起

对 agent 说：

> 帮我找远程 AI Agent 的工作，先给我看一批，别直接投

或者直接点名 skill：

```
/skill job-hunt 帮我找远程全栈岗位
```

agent 会：

1. 打开 BOSS / 智联，按关键词搜索
2. 去重、按四道闸筛选
3. 给你一张预览表
4. 等你确认后再逐条投递
5. 每条核实页面状态并记账

### 第 4 步：看进度

```bash
python3 scripts/jobhunt.py list      # 岗位列表
python3 scripts/jobhunt.py stats     # 状态统计
python3 scripts/jobhunt.py report    # 生成 HTML 报告
```

报告默认写到 `~/.job-hunt/report.html`，浏览器直接打开即可。

---

## 命令参考

```bash
# 初始化
python3 scripts/jobhunt.py init

# 追加岗位（stdin 传 JSON）
echo '{"channel":"boss","source_job_id":"abc123","title":"AI Agent 工程师","company":"某某科技","url":"https://...","salary_text":"20-35K","remote":"remote","employment":"fulltime"}' \
  | python3 scripts/jobhunt.py add-job

# 记录动作结果
echo '{"job_id":"8019714073b5","action":"greet","status":"confirmed","evidence":"消息显示已发送，按钮变为继续沟通"}' \
  | python3 scripts/jobhunt.py record

# 公司主体核查：导入牛企查导出 CSV
python3 scripts/jobhunt.py import-nqc ~/Downloads/牛企查导出.csv --dry-run
python3 scripts/jobhunt.py import-nqc ~/Downloads/牛企查导出.csv

# 公司主体核查：写入单条结果（白牛 API 或人工核对）
echo '{"job_id":"8019714073b5","provider":"bainiu","company":"某某科技有限公司","source":"白牛商查 企业照面","fields":{"登记状态":"存续","成立日期":"2020-05-12"}}' \
  | python3 scripts/jobhunt.py verify

# 查状态
python3 scripts/jobhunt.py list
python3 scripts/jobhunt.py list --json

# 统计
python3 scripts/jobhunt.py stats

# 生成报告
python3 scripts/jobhunt.py report --out ~/Desktop/report.html
```

`record` 的 `status` 只能是：

| status | 含义 |
|---|---|
| `running` | 开始执行 |
| `confirmed` | 页面证据确认成功 |
| `failed` | 明确失败（岗位下线、无投递入口、平台报错） |
| `unknown` | 结果不明，需要人工核对，**不要重发** |

---

## 筛选规则

四条闸，顺序固定：

1. **岗位类型**：排除销售、运营、标注、客服、产品经理、设计、实习等
2. **远程真实性**：排除「远程面试」「远程面」「不支持远程面试」
3. **薪资门槛**：全职上限低于门槛直接排除；兼职低于兼职门槛排除
4. **公司风险**：成立不足一年、0-20 人、法人即招聘人、代招/劳务，标记风险

结论只有三档：**可继续 / 待核实 / 建议排除**，每条都带理由。

细节见 [`references/screening.md`](references/screening.md)。

---

## 公司主体核查（牛企查 / 白牛）

筛选会把「招聘主体待核实」列进待核实项。这条要消掉，必须有可追溯的证据。

### 方式一：牛企查导出 CSV（推荐）

1. 在牛企查网页端按企业名称查询目标公司
2. 用导出功能导出 CSV
3. 交给 agent，或自己执行：

```bash
python3 scripts/jobhunt.py import-nqc ~/Downloads/牛企查导出.csv --dry-run
python3 scripts/jobhunt.py import-nqc ~/Downloads/牛企查导出.csv
```

脚本按**企业名称归一化后精确匹配**（去空格、全角括号转半角），一个公司对应多个岗位时全部写入。匹配不上的公司会列在 `unmatched` 里。

支持的列名会自动识别：企业名称、统一社会信用代码、登记状态、成立日期、法定代表人、注册资本、参保人数、注册地址、所属行业。导出是 xlsx 的，先在表格软件里另存为 CSV。

### 方式二：白牛商查 API（可选）

需要 API Key，按次消耗额度：

```bash
export BAINIU_API_KEY="你的 key"
```

拿到结果后用 `verify` 入账：

```bash
echo '{"job_id":"abc123","provider":"bainiu","company":"某某科技有限公司","source":"白牛商查 企业照面","fields":{"公司状态":"存续","成立日期":"2020-05-12","参保人数":"未返回"}}' \
  | python3 scripts/jobhunt.py verify
```

### 方式三：人工核对

用户自己查到的信息也可以入账，但必须写清来源：

```bash
echo '{"job_id":"abc123","provider":"manual","company":"某某科技有限公司","source":"国家企业信用信息公示系统（用户核对）","fields":{"登记状态":"存续"}}' \
  | python3 scripts/jobhunt.py verify
```

### 三条纪律

- **会员资格 ≠ API 授权**：牛企查 SVIP 是网页权益，能不能调 API 取决于账号实际授权；没有授权就走导出文件
- **名称相似不算核实**：品牌名、母公司名、简称都不等于招聘主体一致
- **参保人数未返回年份时不能推断当前参保情况**，只能记「未返回」

核查完成后，`list` 和报告里会显示「已核实」，「招聘主体待核实」的理由自动消失。细则见 [`references/company-verification.md`](references/company-verification.md)。

---

## 目录结构

```
job-hunt-skill/
├── SKILL.md                  # 主流程与硬性边界
├── references/
│   ├── discovery.md          # 搜岗位、关键词、假远程识别
│   ├── screening.md          # 四道闸、薪资解析、风险公司
│   ├── company-verification.md # 牛企查导入、白牛 API、核查证据
│   ├── boss.md               # BOSS 直聘操作手册
│   ├── zhaopin.md            # 智联招聘操作手册
│   ├── email.md              # 官网/邮箱投递
│   ├── data-format.md        # 账本 schema、状态机
│   └── portability.md        # 跨平台与无 Python 降级
└── scripts/
    └── jobhunt.py            # 本地账本（纯标准库）
```

---

## 常见问题

**Q：会不会把我账号封了？**
A：skill 明确要求不绕过验证、控制频率（单渠道每天 15-20 条）、遇验证码即停。但自动化操作本身仍有平台风控风险，建议先用小批量试。

**Q：投出去的是哪份简历？**
A：智联和 BOSS 走的是**平台在线简历**，不是你本地的 PDF。附件简历需要你在平台里单独上传和选择。skill 不会替你上传文件。

**Q：为什么某条显示「结果不明」？**
A：点击后页面没有出现成功提示，可能被拦截、超时或岗位状态变化。这种情况必须人工核对，**不要直接重投**。

**Q：换电脑后历史还在吗？**
A：账本在 `~/.job-hunt/ledger.jsonl`，和 skill 目录分开。把这两处一起拷走即可延续；只拷 skill 目录则从空账本开始。

**Q：没有 Python 能用吗？**
A：能。按 [`references/data-format.md`](references/data-format.md) 的格式直接追加 JSONL，agent 用文件工具就能维护。

**Q：牛企查会员能直接调 API 吗？**
A：不一定。SVIP 是网页端权益，API 授权和额度要单独确认。没有 API 权限时用导出 CSV 的方式，效果一样，也不需要额外付费。

**Q：为什么公司核查显示「已核实」但来源是 manual？**
A：那是用户自己核对后写入的，证据强度弱于导出文件或 API。报告里保留了 `provider` 字段，可以区分来源。

**Q：支持 Windows 吗？**
A：脚本用 `pathlib` 处理路径、只用标准库。Windows 下把 `python3` 换成 `python` 或 `py -3`；中文编码问题见 [`references/portability.md`](references/portability.md)。

---

## 隐私与安全

- skill 和仓库里**没有任何个人信息**：不含姓名、手机号、邮箱、简历正文
- 登录凭证不读取、不写入、不上传
- 账本和报告只存在本地，不自动上传任何服务
- 报告里不出现手机号、邮箱、简历正文
- 公司核查只查企业主体信息，不查询个人；导出文件由用户合法取得

---

## 平台与合规

- 只操作用户**本人**的账号
- 不绕过验证码、不规避频控、不伪造请求
- 遇到平台限制立即暂停，保留进度并告知用户
- 自动化投递可能违反部分平台的服务条款，使用前请自行确认；因使用产生的账号限制由使用者承担

---

## License

MIT
