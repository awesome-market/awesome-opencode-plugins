# 正正公司 AI 多智能体系统

**项目负责人**: 正正  
**当前版本**: v1.0 with Memory System

---

## ⚠️ 重要：给 Sisyphus (CEO) 的指令

**如果你是新会话的 Sisyphus，请立即阅读以下文件：**

1. **`.agent/RULES.md`** - 公司宪法（必读）
2. **`.agent/CEO行为规范.md`** - CEO工作流程（强制执行）

### 核心规则摘要

**召唤员工前必须执行**：
```python
import sys
sys.path.insert(0, '.agent/记忆库系统/核心模块')
from memory_manager import MemoryManager

manager = MemoryManager("员工名")
memory = manager.get_memory_summary()
# 将memory注入到员工的prompt中
```

**用户已明确要求**：自动处理员工记忆，无需用户操心。

---

## 📂 项目结构

```
.agent/
├── RULES.md                    # 公司宪法 v3.1
├── CEO行为规范.md              # CEO工作流程
├── 员工/                       # 员工档案
│   ├── 大河/                   # HR总监（暹罗猫）
│   ├── 海米/                   # 数据分析师（美短猫）
│   └── 困困/                   # 资源搜猎官（博美犬）
└── 记忆库系统/                 # 记忆库核心代码
    ├── 核心模块/memory_manager.py
    ├── 自动化脚本/memory_maintenance.py
    └── README.md               # 使用文档

.opencode/
└── skills/                     # 技能库
    └── 图书馆/百年孤独/
```

---

## 🧑‍💼 核心员工

| 员工 | 角色 | 物种 | 性格 |
|------|------|------|------|
| 大河 | HR总监 | 暹罗猫 | 精力旺盛、话痨、务实 |
| 海米 | 数据分析师 | 美短猫 | 聪明、粘人、擅长PVM模型 |
| 困困 | 资源搜猎官 | 博美犬 | 热情、激动、找书专家 |

**关系**：三人是好友，可互相查看记忆。

---

## 💾 记忆库系统

**状态**: ✅ 已部署并通过测试

**功能**：
- 三档案记忆（工作日志、人际关系、技能经验）
- 自动归档（每月1号）
- 跨员工访问（核心员工互看）
- 格式验证与修复
- 健康检查与备份

**使用文档**: `.agent/记忆库系统/README.md`

---

## 🚀 快速开始

### 召唤员工（带记忆）

```python
# 1. 加载记忆
manager = MemoryManager("大河")
memory = manager.get_memory_summary()

# 2. 召唤
task(
    category="quick",
    prompt=f"""
    [你的记忆库]
    {memory}
    
    [当前任务]
    {用户需求}
    """
)
```

### 维护记忆库

```bash
cd .agent/记忆库系统/自动化脚本

# 健康检查
python memory_maintenance.py --health

# 手动归档
python memory_maintenance.py --archive

# 生成报告
python memory_maintenance.py --report

# 全部维护
python memory_maintenance.py --all
```

---

## 📜 版本历史

### v1.0 (2026-02-13)
- ✅ 初始化三核心员工
- ✅ 部署记忆库系统
- ✅ 完成公司宪法 v3.1
- ✅ 建立技能库结构
