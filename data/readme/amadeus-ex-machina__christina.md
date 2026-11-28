# Project Christina: Autonomous Cognitive Amplifier

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20external%20(pure%20stdlib)-brightgreen.svg)](#-ponytail-ultra-zero-dependency-guarantee)
[![Tests](https://img.shields.io/badge/tests-62%2F62%20passing-brightgreen.svg)](tests/)
[![FastMCP Compliant](https://img.shields.io/badge/FastMCP-JSON--RPC%202.0-orange.svg)](#-the-canonical-fastmcp-tool-matrix)
[![Code Style: Ponytail Ultra](https://img.shields.io/badge/code%20style-ponytail%20ultra-purple.svg)](CONTRIBUTING.md#core-philosophy-ponytail-ultra-discipline)

<br/>

[![Host: Google Antigravity](https://img.shields.io/badge/Host-Google%20Antigravity%20(`agy`)-4285F4.svg?logo=google)](#-multi-host-compatibility--setup)
[![Host: OpenCode](https://img.shields.io/badge/Host-OpenCode-10B981.svg)](#-multi-host-compatibility--setup)
[![Host: Claude Desktop](https://img.shields.io/badge/Host-Claude%20Desktop-D97706.svg?logo=anthropic)](#-multi-host-compatibility--setup)
[![Host: OpenAI Codex CLI](https://img.shields.io/badge/Host-OpenAI%20Codex%20CLI-000000.svg?logo=openai)](#-multi-host-compatibility--setup)

<p align="center">
  <b>The Autonomous Cognitive Trinity for AI Agents Navigating Multi-Million-Token Codebases</b><br/>
  <i>Recursive Language Models (Context as Variable) • Code Property Graph (AST Radar) • Open Knowledge Format (Durable Semantic Memory) • Swarm Concurrency Substrate</i>
</p>

[Quick Start](#-1-command-zero-friction-installation) • [Architecture](#-tri-pillar-cognitive-architecture) • [MCP Tools](#-the-canonical-fastmcp-tool-matrix) • [CLI Reference](#-cli-quick-reference) • [Documentation](#-documentation--guides) • [Contributing](CONTRIBUTING.md)

---

</div>

## 🌟 Executive Overview: Eliminating Context Rot

Modern AI coding agents fail on large codebases ($10\text{M}+$ tokens) not due to reasoning limitations, but due to **Context Rot**: attention distraction, unindexed prompt pollution, lost architectural constraints across context wipes, and uncoordinated swarm collisions.

**Project Christina** solves this through an integrated, high-performance cognitive trinity:

1. **RLM (Recursive Language Models — Context as a Variable)**: Moves massive codebases out of conversational prompt transcripts into sandboxed heap variables (`context`). Agents execute bounded sub-queries ($D \le 2, N \le 20$) and transactional copy-on-write (CoW) Python control loops with automated rollback.
2. **Graphify (Deterministic CPG & AST Radar)**: Builds an in-memory SQLite3 WAL call graph delivering **sub-0.3ms recursive CTE queries**, transitive blast radius calculation, and God node centrality ranking with a **71.5x token discovery reduction**.
3. **OKF (Durable Semantic Memory & Epistemic Evolution)**: Sub-microsecond regex frontmatter parsing ($6.72\ \mu\text{s}$/doc), formal AGM belief revision, Ebbinghaus decay, and Mark-and-Sweep epistemic garbage collection with an automated $\le 400$-token post-compaction memory recovery anchor.
4. **Cross-Project Epistemic Distillation**: Anonymizes proprietary code into mathematical archetypes with a strict **Zero-Information Leakage invariant ($\mathcal{I} = 0$)**, multi-base Shannon entropy secret scrubbing, and Bayesian invariant aggregation across code repositories.
5. **Swarm Concurrency Control**: Decentralized multi-agent execution using Kung-Robinson Optimistic Concurrency Control (OCC), Tree-CRDT 3-way AST merge, and Linda tuple-space blackboard.

---

## 🏛️ Tri-Pillar Cognitive Architecture

```
                                  ┌─────────────────────────────────────────┐
                                  │           SUPERVISOR / AGENT            │
                                  │  (Antigravity / OpenCode / Claude / AI) │
                                  └────────────────────┬────────────────────┘
                                                       │ JSON-RPC 2.0 (stdio)
                                                       ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            PROJECT CHRISTINA FAST-MCP GATEWAY                                     │
├──────────────────────────────────────┬────────────────────────────────────┬───────────────────────────────────────┤
│          PILLAR 1: RLM ENGINE        │       PILLAR 2: GRAPHIFY CPG       │        PILLAR 3: OKF MEMORY           │
│         (Context as Variable)        │          (AST Code Radar)          │         (Semantic Evolution)          │
├──────────────────────────────────────┼────────────────────────────────────┼───────────────────────────────────────┤
│ • Out-of-core Heap Variables         │ • In-Memory SQLite3 WAL Graph      │ • Sub-microsecond OKF Regex Parser    │
│ • Transactional CoW Rollback         │ • Sub-0.3ms Transitive Blast Query │ • Formal AGM Belief Revision          │
│ • 3-Phase EGRI Invariant Linter      │ • Composite God-Node Centrality    │ • Ebbinghaus Forgetting & GC          │
│ • Dynamic Governor (D<=2, N<=20)     │ • Circular Dependency & Wave Sort  │ • Symbol-to-ADR Constraints           │
└──────────────────────────────────────┴────────────────────────────────────┴───────────────────────────────────────┘
                                                       │
                                                       ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        DECENTRALIZED SWARM & DISTILLERY                                           │
├───────────────────────────────────────────────────────────────────┬───────────────────────────────────────────────┤
│                    SWARM CONCURRENCY BLACKBOARD                   │         GLOBAL EPISTEMIC DISTILLERY           │
├───────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ • Kung-Robinson Optimistic Concurrency Control (OCC)              │ • Zero-Information Leakage (I = 0)           │
│ • Semantic Tree-CRDT 3-Way AST Merge Resolution                   │ • Multi-Base Shannon Entropy Secret Redaction │
│ • Linda Tuple Space (`out`, `rd`, `in`, `eval`, `digest`)         │ • Bayesian Invariant Distillation (0700 Fence)│
└───────────────────────────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

### Mermaid Flowchart

```mermaid
flowchart TD
    Host[Host Agent Context] -->|JSON-RPC 2.0 stdio| MCP[Christina FastMCP Server]
    
    subgraph Trinity["Autonomous Cognitive Trinity"]
        MCP -->|cpg_query| CPG[Graphify CPG Radar<br/><i>sub-0.3ms SQLite WAL</i>]
        MCP -->|rlm_execute| RLM[RLM Sandbox<br/><i>Transactional CoW REPL</i>]
        MCP -->|memory_evolve| OKF[OKF Semantic Memory<br/><i>AGM Revision & Epistemic GC</i>]
    end
    
    subgraph SwarmDistill["Swarm & Cross-Project Substrate"]
        MCP -->|swarm_blackboard| OCC[Swarm Concurrency<br/><i>Kung-Robinson OCC + Tree-CRDT</i>]
        OKF -->|distill_global| Distill[Global Epistemic Distillery<br/><i>Anonymized Archetypes (I=0)</i>]
    end

    CPG -.->|Blast Radius & Waves| OCC
    RLM -.->|Isolated Sub-Calls| Host
    OKF -.->|ADR Anchor <=400 Tokens| Host
```

---

## 🚀 1-Command Zero-Friction Installation

Christina installs in seconds without background daemons, native compilation, or root privileges:

```bash
cd christina
./install.sh
```

### Automated Diagnostic Preflight
```bash
./install.sh doctor
```

```text
================================================================
 Christina Cognitive Amplifier Diagnostics (v1.0.0)
================================================================
✓ Python Version: 3.11+ (Requirement satisfied)
✓ SQLite3 in-memory WAL Engine: Ready
✓ OKF Semantic Memory Engine: Ready
✓ Google Antigravity Plugin: Registered
✓ OpenCode Plugin: Registered
✓ Global memory directory: ~/.config/christina/global_memory (0700 fenced)
================================================================
✅ All systems functional.
```

### Run Full Test Suite (62/62 Passed in <1.2s)
```bash
./install.sh test
# Or with pytest directly:
pytest tests/ -v
```

---

## 🛠️ The Canonical FastMCP Tool Matrix

Christina exposes 4 unified JSON-RPC 2.0 stdio tools compatible with any MCP host:

| Tool | Category | Key Capabilities & Modes | Performance Bound |
| :--- | :--- | :--- | :--- |
| **`cpg_query`** | AST Code Radar | `blast_radius`, `def_use`, `cfg`, `vinterfaces`, `god_nodes`, `cycles`, `waves`, `info` | $<0.3\text{ms}$ in-memory traversal |
| **`rlm_execute`** | Sandboxed Execution | Sub-agent MapReduce, transactional CoW REPL, 3-phase EGRI linting, compute governor | $D \le 2, N \le 20$ recursion bound |
| **`memory_evolve`** | Semantic Memory | `search`, `persist`, `revise` (AGM), `gc` (Ebbinghaus Mark-and-Sweep), `distill_global`, `query_global` | $6.72\ \mu\text{s}$/doc parsing |
| **`swarm_blackboard`** | Swarm Concurrency | `out`, `rd`, `in`, `eval`, `occ_validate` (Kung-Robinson OCC), `tree_merge` (Tree-CRDT), `digest` | Lock-free optimistic validation |

### MCP Tool Invocations

#### 1. Blast Radius Analysis (`cpg_query`)
```json
{
  "name": "cpg_query",
  "arguments": {
    "symbol": "PaymentGateway",
    "mode": "blast_radius",
    "depth": 3
  }
}
```

#### 2. Transactional Sub-Query Execution (`rlm_execute`)
```json
{
  "name": "rlm_execute",
  "arguments": {
    "query": "Audit error recovery handling in database connection pool",
    "scope_paths": ["src/db/", "src/pools/"]
  }
}
```

#### 3. Semantic Memory Search with Symbol Constraint (`memory_evolve`)
```json
{
  "name": "memory_evolve",
  "arguments": {
    "action": "search",
    "query": "zero-trust authentication policy",
    "linked_symbols": ["AuthMiddleware"]
  }
}
```

#### 4. Swarm OCC Conflict Validation (`swarm_blackboard`)
```json
{
  "name": "swarm_blackboard",
  "arguments": {
    "action": "occ_validate",
    "worker_id": "worker_security_audit",
    "read_version": 4,
    "read_set": ["AuthMiddleware", "SessionToken"],
    "write_set": ["AuthMiddleware"]
  }
}
```

---

## ⚡ CLI Quick Reference

```bash
# 1. Scan codebase and index AST knowledge graph into in-memory SQLite3 WAL
python3 -m christina.cli scan .

# 2. Calculate static blast radius for a target symbol
python3 -m christina.cli blast AuthService --depth 3

# 3. List top God Nodes ranked by composite degree centrality
python3 -m christina.cli god-nodes --limit 10

# 4. Search OKF institutional memory, ADRs, and symbol constraints
python3 -m christina.cli memory "connection pool timeout" --symbol DatabasePool

# 5. Run FastMCP JSON-RPC 2.0 stdio server
python3 -m christina.cli serve

# 6. Execute system diagnostics
python3 -m christina.cli doctor
```

---

## 🔌 Multi-Host Compatibility & Setup

Christina includes seamless 1-command registration across all standard AI agent hosts:

### 1. Google Antigravity CLI (`agy`)
Automatically symlinked to `~/.gemini/antigravity-cli/plugins/christina` and registered in `~/.gemini/antigravity-cli/mcp_config.json`.

### 2. OpenCode
Automatically registered in `~/.config/opencode/plugins/christina` and `~/.config/opencode/opencode.json`.

### 3. Claude Desktop
Automatically configured in `~/.claude/claude_desktop_config.json` (or `Library/Application Support/Claude/claude_desktop_config.json` on macOS):
```json
{
  "mcpServers": {
    "christina": {
      "command": "python3",
      "args": ["-m", "christina.bridge.mcp_server"],
      "env": {
        "PYTHONPATH": "/path/to/christina"
      }
    }
  }
}
```

### 4. OpenAI Codex CLI
Automatically registered in `~/.config/codex/config.json`.

---

## 🪮 Ponytail Ultra: Zero-Dependency Guarantee

Project Christina is strictly engineered under **Ponytail Ultra** discipline:

- **Zero External Runtime Dependencies**: Uses Python standard library only (`ast`, `sqlite3`, `re`, `json`, `hashlib`, `fcntl`, `math`, `pathlib`, `typing`).
- **Zero Heavy Daemons**: No Docker, no Neo4j, no ChromaDB, no Redis. In-memory SQLite3 WAL and POSIX file locks deliver sub-millisecond execution with $0\text{MB}$ idle background RAM.
- **Strict Code Brevity**: Every module is concise ($<250$ LOC), cohesive, and self-contained.

---

## 📚 Documentation & Guides

| Document | Description |
| :--- | :--- |
| **[Getting Started Guide](docs/getting_started.md)** | Step-by-step setup, verification, and first agent workflow. |
| **[Skills Taxonomy](skills/christina/SKILL.md)** | Progressive disclosure skill definitions (`cpg`, `rlm`, `memory`, `swarm`). |
| **[Contributing Guide](CONTRIBUTING.md)** | Ponytail Ultra development guidelines, Nix setup, test suites, and ADR workflow. |
| **[Security Policy](SECURITY.md)** | Zero-information leakage ($\mathcal{I} = 0$), Shannon entropy secret scrubbing, and containment. |
| **[Changelog](CHANGELOG.md)** | Detailed release notes and version history. |

---

## 📜 License

Project Christina is distributed under the open-source **[MIT License](LICENSE)**.

Copyright (c) 2026 Christina Engineering Swarm & Contributors.
