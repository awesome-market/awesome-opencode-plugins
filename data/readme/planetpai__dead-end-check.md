# dead-end-check · 别在死路上装修

An agent **skill** (not a plugin) that asks *"is this path right?"* **before** you spend another
round on it — whether you are stuck in a fix-and-fail loop, or about to hand-roll something that
already has a mature implementation.

> 一个 agent 技能：在**继续投入之前**判断「这条路对不对」。
> 适用于反复修不好的循环，也适用于「还没报错，但越写越重」的技术选型。

---

## 它解决什么问题

大多数工程浪费不是「改错了代码」，而是**在一件根本不可能成立的事情上反复优化**。

死路有两种形态，判断时点完全不同：

| 形态 | 信号 | 危险在哪 |
|---|---|---|
| **已经撞墙** | 反复改都不成立，每次都「找到了新原因」 | 沉没成本让你停不下来 |
| **正在走向墙** | 没报错，但越写越重；自己实现了一件早就有成熟解的事 | **没有任何疼痛信号告诉你该停** |

第二种更隐蔽。代码能编译、能显示，只是慢、只是边界情况无穷——所以你不会去搜「我卡住了」。

---

## 内容结构

```
SKILL.md
├─ 开工之前：这件事该不该由我来做          ← 技术选型 / 自研 vs 采用
│    ├─ 五个判据（差异点 / 规范一致性测试 / 成熟度靠体量 / 维护税 / 退出成本）
│    ├─ 还要对齐「哪一维度最难」
│    ├─ 反向约束：换栈不是免费的
│    ├─ 限时选型探针（同一切片两栈各做一遍）
│    └─ 已开工一半怎么办（沉没成本两问）
├─ 第 0 步：确认自己已经在循环里（5 个自检信号）
├─ 第 1 步：四问定位 —— 我的代码 / 依赖环境 / 上游平台能力 / 需求本身
├─ 第 2 步：能力清单优先（30 分钟内）
├─ 第 3 步：分层判断 —— 这一层能不能合成它
├─ 第 4 步：决策门（强制，防沉没成本）
├─ 第 5 步：让每次验证都物有所值
├─ 第 6 步：结论分级（已验证 / 推断 / 猜测），及时更正
├─ 失效模式自查（9 条）
└─ 一个真实案例（浓缩）
```

**三句话版本：**

> 开工前问「这件难事该不该由我做」，卡住后问「这是谁的错、这一层能不能补」，最后才问「怎么改」。
> 不该自己写的通用能力，写完了也是负债；不能补的能力，改多少遍都补不出来。

---

## 安装

技能就是一个 `SKILL.md` 文件，**不需要插件、不需要 npm、不绑定任何 harness**。

### 方式一：直接 clone 到技能目录（推荐）

```bash
git clone https://github.com/Planetpai/dead-end-check.git ~/.dsh/skills/dead-end-check
```

更新：`git -C ~/.dsh/skills/dead-end-check pull`

### 方式二：手动复制

把 `SKILL.md` 放到 `<skills-dir>/dead-end-check/SKILL.md`。
目录名与 frontmatter 里的 `name` 要一致。

### 方式三：其它 harness

`SKILL.md` 是通用格式（YAML frontmatter + Markdown 正文）。
任何支持「按 description 发现技能」的 harness 都能用，把文件放进它读取技能的目录即可。

---

## 什么时候会被触发

技能只把 `name` + `description` 放进目录给模型挑，`description` 就是触发器。本技能的
description 覆盖这些说法：

- 一个修复反复不生效，每次都「找到了新原因」
- 同一份代码在 A 机器正常、B 机器失败
- 只在某个 OS / 版本 / 运行时 / 架构上崩
- 准备给依赖打补丁、monkey-patch 运行时
- **准备自己实现一个已有成熟方案的东西**（解析器、渲染器、鉴权、图表、同步）
- 写了一半发现越写越重，怀疑选错了技术栈

---

## 出处

这套判据来自一次真实的 20 轮失败：为一个安卓应用在另一套系统的兼容容器里启动引擎，
连续 20 轮探针（二进制补丁、syscall 重定向、fd 继承、全量白名单扫描）全部指向同一结论——
容器被封了 `socket()`，这条路成功率从第 6 轮起就是 0。最终解是一个**同期独立完成的原生移植**，
用的是开始前就已经存在的技术栈。

完整复盘见 [CASE-STUDY.md](./CASE-STUDY.md)。它记录的不是技术细节，而是**为什么一个从未被质疑的前提，
能让人多花 8 小时**。

---

## 反例：它也会告诉你「别换」

这个技能刻意写了反向约束，避免变成「一遇阻力就重写」：

- 剩下的工作量里，不确定的**只是同类工作的堆积** → 做完；
- 你需要一个粗糙版本验证产品、拿反馈、摸清领域 → 做完；
- **能用的粗糙版胜过永不落地的完美架构。**

---

## English

`dead-end-check` is a single-file agent skill that forces a decision *before* more effort is spent.
It covers two failure shapes that feel unrelated but share one root question — *whose problem is
this, and should I be solving it here?*

1. **Already stuck** — a fix that keeps not working. Triage the blame across four owners (your code,
   dependency/environment, upstream/platform capability, the requirement itself), build a capability
   inventory instead of a to-do list, layer the problem by ownership, and install a mandatory decision
   gate every 3 attempts.
2. **Not stuck yet** — no errors, but the work gets heavier. Five criteria decide whether to build or
   adopt (differentiation, conformance suite, maturity-by-volume, maintenance tax, exit cost), plus a
   reverse constraint so "switch stacks" does not become the new default answer.

No plugin, no dependencies, no harness lock-in: it is one `SKILL.md`.

---

## License

MIT
