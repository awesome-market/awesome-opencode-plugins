# opcode-pg-memory v4.0

**OpenCode 长期记忆插件** — PostgreSQL + pgvector 跨平台记忆持久化 + 多策略检索

![TypeScript strict](https://img.shields.io/badge/strict-true-brightgreen)
![tests](https://img.shields.io/badge/tests-100%20passing-brightgreen)

---

## 架构

`
src/
├── index.ts                  # 插件入口 — 注册钩子
│   ├── event                 # session 生命周期事件
│   ├── experimental.chat.system.transform  # 记忆注入 system prompt
│   └── tool.execute.after    # 工具调用记录 observation
│
├── config/index.ts           # 配置加载
├── db/index.ts               # 数据库层（连接池 + Schema）
├── plugin/                   # 插件逻辑
│   ├── recorder.ts           # observation 写入
│   ├── injector.ts           # system prompt 注入
│   └── events.ts             # session 事件处理
├── retrieve/                 # 检索层（单一入口）
│   ├── index.ts              # 编排器
│   ├── scope.ts              # session 范围解析
│   ├── fusion.ts             # RRF 融合
│   └── strategies/
│       ├── keyword.ts        # ILIKE 搜索
│       ├── bm25.ts           # pg_trgm 搜索
│       ├── semantic.ts       # pgvector 搜索
│       └── graph.ts          # 图遍历
└── mcp/
    ├── server.ts             # MCP 服务器
    ├── recall-memory.ts      # 记忆检索
    ├── hindsight-reflect.ts  # 反思归纳
    ├── get-memory.ts         # 单条记忆
    ├── timeline.ts           # 时间线
    └── delete-memory.ts      # 删除记忆
`

### 数据流

`
LLM 调用前
  → experimental.chat.system.transform
  → plugin/injector.ts → retrieve/index.ts → 注入相关记忆

工具调用后
  → tool.execute.after
  → plugin/recorder.ts → INSERT INTO observations

检索请求
  → MCP recall_memory
  → retrieve/index.ts
    → scope.ts（范围解析）
    → parallel strategies (keyword + bm25 + semantic + graph)
    → fusion.ts（RRF 融合）
  → 返回排序结果
`

---

## 快速开始

详见 REFERENCE.md。

### 环境变量

`ash
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=PGOMO
PG_PASSWORD=your_password
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=qwen3-embedding:0.6b
`

---

## 检索策略

| 策略 | 后端 | 需要 embedding |
|------|------|---------------|
| keyword | ILIKE + 正则 | ❌ |
| bm25 | pg_trgm similarity | ❌ |
| semantic | pgvector <=> | ✅ Ollama |
| graph | 实体关系图 | ❌ |

---

## 开发

`ash
npm run typecheck
npm run test
npm run build
`

## License

GPL-3.0
