# Intent OS — 项目指导手册

> **版本:** v2.0
> **目的:** 确保任何开发者在新的会话中，能够完整理解项目背景、定位、架构、当前状态和开发规范，无缝继续开发。
> **最后更新:** 2026-07-22

---

## 目录

1. [项目身份](#1-项目身份)
2. [核心问题](#2-核心问题)
3. [定位](#3-定位)
4. [核心原则（项目防火墙）](#4-核心原则项目防火墙)
5. [完整方案简述](#5-完整方案简述)
6. [当前实现状态](#6-当前实现状态)
7. [文件结构](#7-文件结构)
8. [关键设计决策（红线）](#8-关键设计决策红线)
9. [Phase 0 实验验证](#9-phase-0-实验验证)
10. [演化路径](#10-演化路径)
11. [开发规范](#11-开发规范)
12. [如何继续](#12-如何继续)
13. [附录：关键洞察清单](#13-附录关键洞察清单)

---

## 1. 项目身份

- **当前名称:** Intent OS (v0.2.0)
- **曾用名:** Agent OS（2026-07-21 前更名）
- **目录位置:** `~/Desktop/intent-os/`
- **GitHub:** https://github.com/X-code-sourse/intentos
- **旧目录:** `~/Desktop/agent-os/`（保留，未删除，可作为备份）
- **项目定位:** AI 能力互操作的开放规范与参考运行时
- **一句话定义:** Intent OS is an open interoperability layer for AI capabilities, workflows, and execution.

### 1.1 名称含义

不叫 "Agent OS" 的原因：项目核心不是管理 Agent，而是管理 **AI 能力（Capability）的描述、组合和执行**。"Intent" 强调用户表达意图，系统负责执行——与"用户只说目标，不说过程"的核心哲学一致。

### 1.2 Repository

```
https://github.com/X-code-sourse/intentos
```

---

## 2. 核心问题

### 2.1 时代矛盾

**AI 能力的增长速度，远远超过了 AI 能力的协作速度。**

过去几年模型越来越强（GPT → Claude → Gemini）、工具越来越多（Browser → Code → Search → API）、Agent 越来越复杂（Coding → Research → Data → Business）。但一个 AI 能力写出来后，**无法在不同平台间自由流动**。

### 2.2 更深层的问题：Execution Semantic Fragmentation

MCP 已经解决了工具移动问题，但移动之后真正的问题暴露了：

> 移动之后，谁负责调用？生命周期是什么？错误怎么办？如何组合？如何记录？

同一个 Workflow（Task A → Task B → Task C），Task B 失败时：

| Runtime | 行为 |
|---|---|
| Runtime A | Retry B，exponential backoff |
| Runtime B | Skip B，继续执行 C |
| Runtime C | Rollback A，整个 Workflow 撤销 |

这三个已经不是同一个 Workflow。**真正的敌人不是 Tool Fragmentation，而是 Execution Semantic Fragmentation。**

### 2.3 五个具体问题

| # | 问题 | 表现 | Intent OS 解决 |
|---|---|---|---|
| 1 | **Capability Fragmentation** | 同一能力适配 N 个平台 | Capability Manifest |
| 2 | **Workflow Lock-in** | 编排逻辑绑定平台，无法迁移 | Workflow Spec（含 Execution Semantics） |
| 3 | **Runtime Lock-in** | 用户被绑定到特定 Agent 平台 | Common Execution Model（Adapter 层） |
| 4 | **Engineering Gap** | Agent 缺日志、Trace、审计 | Event System |
| 5 | **Ecosystem Void** | 没有"AI 能力的 npm" | Registry + Marketplace（Phase 2） |

### 2.4 为什么是现在

三个条件同时出现：
1. **模型能力已足够** — Agent 正在成为软件新形态
2. **Agent 大量出现**（2024-2026）— Claude Code、Codex、Cursor、Devin 等
3. **标准还未形成** — MCP 标准化了连接层（Connection），但**执行层（Execution）是空白**

---

## 3. 定位

### 3.1 是什么

- ✅ Capability 的共同描述语言
- ✅ Workflow 的共同执行模型
- ✅ Agent Runtime 之间的兼容层

### 3.2 不是什么（死边界）

- ❌ **不是新的大模型** — 不是 OpenAI competitor
- ❌ **不是 Agent Framework** — 不是 LangChain replacement
- ❌ **不是 AI 应用** — 不是个人助手或自动化工具
- ❌ **不是封闭平台** — 不要求开发者迁移
- ❌ **不是 Prompt 框架** — 不规定怎么写 Prompt
- ❌ **不是云服务** — 是本地可运行的开放规范

### 3.3 与 MCP 的关系

> **MCP 标准化的是 Connection（AI ↔ Tool）。**
> **Intent OS 标准化的是 Execution（Capability → Workflow → Event）。**
> 两者互补。Intent OS Runtime 可以把 MCP Server 作为 Capability Provider 接入。

### 3.4 历史类比

| 时代 | 基础设施 | 解决的问题 | Intent OS 映射 |
|---|---|---|---|
| 80-90s | **POSIX** | 不同硬件上程序如何运行？ | **Capability Contract** |
| 90-00s | **HTTP + JSON** | 不同机器间信息如何交换？ | **Capability Packaging** |
| 2010s | **OCI + K8s** | 不同环境中应用如何部署？ | **Workflow Execution Model** |
| 2020s | **Intent OS** | 不同平台上 AI 能力如何协作？ | **三者融合的互操作层** |

---

## 4. 核心原则（项目防火墙）

> **Intent OS does not standardize intelligence. It standardizes interaction.**

这条原则划定了所有设计决策的边界。每次有人问"我们要不要加 X"，回到这句话来判断。

### 4.1 延伸出的操作原则

1. **Spec 优先，Runtime 其次** — Runtime 是 Spec 的第一个证明，不是 Spec 的主人
2. **兼容先于替代** — 不替代现有平台，而是提供共同层
3. **不做比做什么更重要** — 严格按边界防守
4. **数据驱动演化** — 没有数据不要设计优化器
5. **Control Plane 不拥有任何状态** — 所有状态通过 Event Bus 写入 Data Plane

---

## 5. 完整方案简述

### 5.1 三份 Spec

| Spec | 职责 | 类比 | 状态 |
|---|---|---|---|
| **SPEC-0001: Capability Manifest** | 定义 AI 能力的统一描述格式 | OpenAPI | 冻结 |
| **SPEC-0002: Workflow Graph** | 定义工作流的拓扑 + 执行语义 | Kubernetes YAML | 冻结 |
| **SPEC-0003: Event Schema** | 定义执行事件格式 | OpenTelemetry | 冻结 |
| **SPEC-0004: Security（未来）** | 权限与安全模型 | — | 占位 |

SPEC-0002 必须拆成两个子 Spec：
- **Workflow Structure Spec** — nodes, edges, dependency, dataflow
- **Execution Semantics Spec** — retry, timeout, failure propagation, compensation, parallel semantics

### 5.2 五 Plane 架构（内部实现视角）

```
┌──────────────────────────────────┐
│ User Plane                       │
│ Goal / Intent                    │
└──────────────┬───────────────────┘
               │ Event Bus
┌──────────────▼───────────────────┐
│ Control Plane                    │
│ Planner / Execution Engine       │
│ Rule Manager / Security          │
│ ⚠️ 红线：不拥有任何状态          │
└──────────────┬───────────────────┘
               │ Event Bus
┌──────────────▼───────────────────┐
│ Metadata Plane                   │
│ Capability / Workflow / Model    │
│ 注册表 + 版本管理                │
└──────────────┬───────────────────┘
┌──────────────▼───────────────────┐
│ Data Plane                       │
│ Event Store / Memory / Knowledge │
└──────────────┬───────────────────┘
┌──────────────▼───────────────────┐
│ Runtime Plane                    │
│ Capability / Model / Tool Pools  │
└──────────────────────────────────┘
```

### 5.3 对外架构

```
            AI Applications
                  ↑
          Workflow 编排层
                  ↑
    ┌──────────────────────────────┐
    │     Intent OS Common Model    │
    │  ┌──────┐┌─────┐┌─────────┐  │
    │  │Capab.││Work.││ Event   │  │
    │  │Spec  ││Spec ││ Spec    │  │
    │  └──────┘└─────┘└─────────┘  │
    │  + Security (future)          │
    │  + Execution Model            │
    └──────────────────────────────┘
                  ↑
        Runtime 实现层（Adapter）
    ┌──────┬──────┬──────┬────────┐
    │OpenAI│Anthrop│GitHub│Ollama │
    │      │ic     │Models│(本地) │
    └──────┴──────┴──────┴────────┘
                  ↑
            Models + Tools
```

### 5.4 核心算法优先级

**第一优先级（已实现）— ★★★★★**

1. **Capability Registry + Manifest 解析** — 能力注册、发现、持久化
2. **Execution Model — Capability Invocation** — Manifest → Runtime 映射
3. **Event System — Execution Record 生成** — 统一执行记录 + 可比较

**第二优先级（已实现）— ★★★★☆**

4. **Workflow Planner** — 模板化规划器（目标匹配 → DAG 生成）
5. **Scheduler + 补偿** — 状态机 + retry + failure propagation + compensation

**第三优先级（Phase 2+）— ★★★☆☆**

6. **Planner 的 Execution Feedback** — 从 Event Store 学习优化
7. **Evolution Loop** — 自动优化调度策略

---

## 6. 当前实现状态

**总测试：560 项（552 pass + 8 skip），全部通过。**

### 6.1 版本演进

| 阶段 | 内容 | 测试 | 状态 |
|---|---|---|---|
| Phase 0 | Manifest 解析 + 跨 Runtime 执行验证（6 Adapter） | 42 | ✅ |
| Phase 0 | CLI 工具链（14 个命令） | 37 | ✅ |
| Phase 1 | Workflow Engine（DAG/Planner/Scheduler/Conditions） | 75 | ✅ |
| Phase 1 | Import/Export（OpenAI/MCP 双向转换） | 26 | ✅ |
| Phase 1 | Event Store + Analytics + Evolution Loop | 49 | ✅ |
| Phase 1 | DevEx（Quickstart + DX 引导 + Ollama 检测） | — | ✅ |
| Phase 1 | 持久化 Registry + 语义搜索 | 62 | ✅ |
| Phase 1 | MCP Server + 测试 | 21 | ✅ |
| Phase 1 | pip install 打包 + entry_points | — | ✅ |
| Phase 2 | Security Manager（SPEC-0004 实现） | 120 | ✅ |
| Phase 2 | Adaptive Execution Graph（条件 DSL） | 36 | ✅ |
| Phase 2 | 跨 Runtime 兼容性自动化测试（L1-L4） | 42 | ✅ |
| Phase 2 | Executor 独立测试 | 41 | ✅ |

### 6.2 已实现功能清单

| 功能模块 | 状态 | 测试文件 |
|---|---|---|
| Capability Manifest 解析 + Schema 验证 | ✅ | `test_workflow.py` |
| 跨 Runtime 执行（6 Adapter） | ✅ | `test_cross_runtime.py` (L1-L4 自动验证) |
| Execution Record 生成 + 跨 Runtime 比较 | ✅ | `test_event_store.py` |
| Workflow DAG 验证（环检测/拓扑排序） | ✅ | `test_workflow.py` |
| Workflow Planner（模板化） | ✅ | `test_workflow.py` |
| Workflow Scheduler（状态机/重试/失败传播/补偿） | ✅ | `test_workflow.py` + `test_workflow_integration.py` |
| Workflow YAML 解析器（正式版） | ✅ | `test_workflow_parser.py` |
| Workflow 端到端集成测试 | ✅ | `test_workflow_integration.py` |
| Adaptive Execution Graph（条件 DSL） | ✅ | `test_conditions.py` + `test_adaptive_workflow.py` |
| Workflow ↔ 真实 Adapter 连接 | ✅ | `test_workflow_adapter_integration.py` |
| Import/Export（OpenAI / MCP 双向） | ✅ | `test_import_export.py` |
| Event Store（SQLite 持久化） | ✅ | `test_event_store.py` |
| Analytics（排名/趋势/失败/Cost Model 导出） | ✅ | `test_event_store.py` |
| Evolution Loop（分析→建议→审批） | ✅ | `test_evolution.py` |
| Security Manager（Policy 评估引擎） | ✅ | `test_security.py` |
| Capability Registry 持久化 + 语义搜索 | ✅ | `test_registry_persistence.py` + `test_search.py` |
| MCP Server（SSE 传输 + tools/list/call） | ✅ | `test_mcp_server.py` |
| 14 个 CLI 子命令 | ✅ | `test_cli_commands.py` |
| Executor 独立测试 | ✅ | `test_executor.py` |
| Adapter 层单元测试（6 Adapter） | ✅ | `test_adapters.py` |
| pip install 打包 | ✅ | 已验证 `pip install -e .` |
| YAML 语义 Round-trip（YAML→Spec→DAG→Scheduler） | ✅ | `test_workflow_integration.py` |

### 6.3 代码统计

```
语言: Python 3.10+
测试: 552 passing (8 skip) in ~17s
文件: 60+ 个 .py 文件，约 13,200 行 Python
      7 个 .md 文件，约 3,000 行文档
      3 个 .yaml 示例文件
      3 个 .json Schema 文件
安装: pip install intent-os 或 pip install -e .
```

---

## 7. 文件结构

```
intent-os/
├── README.md                        # 项目入口
├── POSITIONING.md                   # 战略定位（冻结）
├── CONSTITUTION.md                  # 宪法（冻结）
├── ROADMAP.md                       # 演化路线图
├── GUIDE.md                         # ← 本文件
│
├── docs/
│   └── QUICKSTART.md                # 5 分钟快速入门
│
├── specs/
│   ├── SPEC-0001-capability-manifest.md  # Capability 规范（冻结）
│   ├── SPEC-0002-workflow-graph.md       # Workflow 规范（冻结）
│   └── SPEC-0003-event-schema.md         # Event 规范（冻结）
│
├── examples/
│   ├── hello-world/
│   │   ├── hello_world.yaml
│   │   └── README.md
│   └── research_workflow.yaml       # 4 步骤工作流示例
│
└── reference-runtime/
    ├── cli.py                       # CLI 入口（191 行，调度器）
    ├── mcp_server.py                # MCP Server（SSE 传输）
    ├── pyproject.toml / setup.py    # 打包配置
    │
    ├── commands/                    # CLI 命令（11 个文件）
    │   ├── helpers.py               # 共享工具函数
    │   ├── validate.py / run.py / compare.py / list.py
    │   ├── registry.py / event.py / analytics.py
    │   ├── workflow.py / mcp_server.py
    │   └── import_cmd.py / export.py
    │
    ├── core/                        # 核心引擎（11 个文件）
    │   ├── models.py                # 数据模型
    │   ├── parser.py                # Capability Manifest 解析器
    │   ├── registry.py              # Capability Registry（持久化）
    │   ├── executor.py              # 执行引擎
    │   ├── recorder.py              # Event 记录器
    │   ├── workflow.py              # Workflow 数据模型 + DAG
    │   ├── workflow_parser.py       # Workflow YAML 解析器
    │   ├── workflow_runner.py       # 模拟执行器（集成测试用）
    │   ├── planner.py               # 工作流规划器
    │   ├── scheduler.py             # 执行调度器
    │   ├── event_store.py           # SQLite Event Store
    │   └── analytics.py             # 执行分析引擎
    │
    ├── adapters/                    # Runtime Adapter（6 个）
    │   ├── base.py                  # 抽象接口
    │   ├── openai_adapter.py        # OpenAI Function Calling
    │   ├── anthropic_adapter.py     # Anthropic Tool Use
    │   ├── ollama_adapter.py        # Ollama 原生 API（本地）
    │   ├── openrouter_adapter.py    # OpenRouter 统一 API
    │   └── github_models_adapter.py # GitHub Models（免费）
    │
    ├── tools/                       # Import/Export 工具
    │   ├── importer.py / exporter.py
    │   └── formats/
    │       ├── openai.py            # OpenAI ↔ Manifest 转换
    │       └── mcp.py               # MCP ↔ Manifest 转换
    │
    └── tests/                       # 16 个测试文件，560 项
        ├── test_adapters.py              (45)
        ├── test_cli_commands.py          (37)
        ├── test_executor.py              (41)
        ├── test_event_store.py           (35)
        ├── test_import_export.py         (26)
        ├── test_mcp_server.py            (21)
        ├── test_registry_persistence.py  (29)
        ├── test_search.py                (27)
        ├── test_workflow.py              (39)
        ├── test_workflow_integration.py  (28)
        ├── test_workflow_parser.py       (23)
        ├── test_conditions.py            (25)
        ├── test_adaptive_workflow.py     (11)
        ├── test_workflow_adapter_integration.py (3)
        ├── test_evolution.py             (14)
        ├── test_security.py              (120)
        └── test_cross_runtime.py         (42)
```

---

## 8. 关键设计决策（红线）

以下是 CONSTITUTION.md 中规定的、不可违反的设计决策：

### R1: Control Plane 不拥有任何状态
Control Plane 组件（Planner、Execution Engine、Rule Manager）不能本地存储任何状态。所有状态必须通过 Event Bus 写入 Data Plane 的 Event Store。这是分布式、HA、Replay 的前提。

### R2: 没有直接 Inter-Processor 通信
Processor 之间不能直接调用。所有通信都通过 Scheduler 进行。这保证了可观测性和策略一致性。

### R3: Event Bus 是唯一事实源
所有状态变更——Task 状态转换、Capability 调用、失败、成本——都必须记录为 Event。没有其他权威记录。

### R4: Capability 是无状态的
Capability 实例不能在调用之间维护状态。有状态的上下文由 Context Manager（Data Plane）管理。

### R5: 不可违反的边界
- Phase 0/1 不做 Planner 的自动优化（需要 Execution Record 数据）
- 不标准化智能（不写 Prompt、不选模型、不规定推理方式）
- Spec 开放，不属于任何公司或平台
- 兼容先于替代

---

## 9. Phase 0 实验验证

### 9.1 核心 Thesis（已实验证明为工程事实）

> **同一个 Capability Manifest，在多个不同的 Runtime 上，能够被解析、加载、执行，并产生同一格式的 Execution Record。**

### 9.2 实验数据

| 对比 | 协议差异 | 结果 |
|---|---|---|
| OpenAI（GPT-4o）↔ Ollama（Llama 3.2 1B） | **完全不同**（function calling vs HTTP + prompt） | ✅ COMPATIBLE |
| OpenAI（GPT-4o）↔ OpenRouter（→ Claude Sonnet 4） | 同协议不同提供商 | ✅ COMPATIBLE |
| OpenRouter（Claude）↔ Ollama（Llama 3.2 1B） | **完全不同** | ✅ COMPATIBLE |
| OpenAI ↔ GitHub Models | 同协议不同端点 | ✅ COMPATIBLE |

### 9.3 四层兼容性验证

| 层级 | 检查项 | 状态 |
|---|---|---|
| L1 — Schema Compatibility | 两个 Runtime 解析同一个 Manifest | ✅ |
| L2 — Capability Compatibility | 两个 Runtime 都能执行 | ✅ |
| L3 — Semantic Contract | 输出满足 Manifest 的 Schema | ✅ |
| L4 — Execution Record | 事件序列和指标维度一致 | ✅ |

### 9.4 API Key 说明

| Key 类型 | 用途 | 需要付费 |
|---|---|---|
| `sk-...` (OpenAI) | 调 GPT-4o | 是 |
| `sk-or-...` (OpenRouter) | 统一调多个模型 | 免费额度有限 |
| `ghp_...` (GitHub Token) | GitHub Models（GPT-4o-mini 免费） | 否 |
| 无（Ollama） | 本地推理 | 否 |

**关键发现：** GitHub Models 是 OpenAI 兼容的，所以 OpenAI ↔ GitHub Models 不是真正的跨协议验证。**OpenAI ↔ Ollama** 才是真正的跨协议验证（API 协议完全不同）。

---

## 10. 演化路径

```
Phase 0: AI Interoperability Layer  ← 已验证（188 测试）
    ↓ 产生执行数据
Phase 1: AI Capability Marketplace   ← 当前（CLI + Registry 就绪）
    ↓ 积累足够 Capability
Phase 2: AI Execution Graph / Semantic Search
    ↓ 积累大量 Execution Record
Phase 3: AI Query Engine（Probabilistic Planner）
    ↓ Planner 有数据可优化
Phase 4: Self-optimizing AI Computing Infrastructure

未来演进方向（现有方案的自然延伸）：
  Task → Job + Task（Job 层管理用户完整目标）
  Capability Registry → Capability Knowledge Graph（能力间关系）
  DAG → Adaptive Execution Graph（动态调整执行路径）
  Event → Learning Backbone（数据飞轮）
  Planner → Probabilistic Query Optimizer（带不确定性的 Cost Model）
```

### Phase 0 明细

**验证假设：** 一个 Capability Manifest 可以在不同 Runtime 上执行。

**不做：**
- ❌ Workflow Planner
- ❌ Evolution Loop
- ❌ Capability Marketplace
- ❌ 权限与治理
- ❌ 前端 UI

---

## 11. 开发规范

### 11.1 运行测试

```bash
cd ~/Desktop/intent-os/reference-runtime

# 运行全部测试（推荐）
python -m pytest tests/ -v

# 单文件测试
python -m pytest tests/test_workflow.py -v

# 单条测试
python -m pytest tests/test_workflow.py::TestWorkflowDAGValidation::test_cycle_detection -v

# 快速检查（无详细信息）
python -m pytest tests/ --tb=no -q
```

### 11.2 运行 CLI

```bash
cd ~/Desktop/intent-os/reference-runtime

# 验证 Manifest
python cli.py validate examples/text_summarize.yaml

# 本地执行（Ollama，无需 API Key）
python cli.py run examples/text_summarize.yaml --adapter ollama --input '{"text":"..."}'

# 云端执行（需要 OpenAI API Key）
export OPENAI_API_KEY="sk-..."
python cli.py run examples/text_summarize.yaml --adapter openai --input '{"text":"..."}'

# 跨 Runtime 比较
python cli.py compare examples/text_summarize.yaml --input '{"text":"..."}'

# 工作流规划（本地模拟）
python cli.py workflow plan "research NVIDIA stock"

# 工作流执行
python cli.py workflow run examples/research_workflow.yaml --input '{"company":"NVIDIA"}'

# Registry 管理
python cli.py registry register my_cap.yaml
python cli.py registry list

# Event 管理
python cli.py event list

# Analytics
python cli.py analytics summary

# MCP Server
python cli.py mcp-server status

# Import/Export
python cli.py import openai-function my_tool.json
python cli.py export openai manifest.yaml --as-tool
```

### 11.3 测试命名规范

- 测试类名：`Test` + 组件名（如 `TestWorkflowDAGValidation`）
- 测试方法名：`test_` + 场景描述（如 `test_cycle_detection`）
- 断言风格：`assert` 语句（非 `self.assertEqual`）
- 使用 `setup_method` / `teardown_method`

### 11.4 代码风格

- Python 3.10+
- 类型注解（`from __future__ import annotations`）
- 使用 `dataclass` 而非手写类
- 文件名小写下划线（`workflow_parser.py`）
- 类名 PascalCase，方法名/变量名 snake_case
- 模块 docstring 包含文件名和简要说明
- 所有文件头部 docstring 使用 "Intent OS —" 前缀

### 11.5 新增 Adapter 规范

1. 继承 `adapters/base.py` 中的 `AdapterBase`
2. 实现 `name`、`version`、`default_model` 属性和 `execute()` 方法
3. `execute()` 必须返回包含 `_token_usage` 和 `_cost` 的 dict
4. 在 `commands/helpers.py` 的 `setup_executor()` 中注册

### 11.6 新增 Spec 规范

1. 按 `specs/SPEC-XXXX-name.md` 编号
2. 包含 Purpose、Design Principles、Specification（含 YAML 示例）、Validation Rules
3. 每条规则必须可测试验证

### 11.7 新增 CLI 命令规范

1. 在 `commands/` 下创建 `command_name.py`
2. 函数签名：`def cmd_xxx(args: argparse.Namespace) -> None`
3. 在 `cli.py` 的 `build_parser()` 中注册
4. 注册方式：`xxx_parser.set_defaults(func=CMD_MAP["xxx"])`

---

## 12. 如何继续

### 12.1 第一步：在新会话中恢复环境

```bash
cd ~/Desktop/intent-os

# 先读本文件
# 然后运行测试确认环境正常
cd reference-runtime && python -m pytest tests/ --tb=no -q

# 如果有 Ollama 运行中，可测试本地执行
python cli.py validate examples/text_summarize.yaml

# 如果需要 API Key
export OPENAI_API_KEY="sk-..."
```

### 12.2 当前优先级排序（按价值/风险比）

审查报告建议的 Phase 2 优先级：

| 优先级 | 方向 | 价值 | 风险 | 工作量估计 |
|---|---|---|---|---|
| **P0** | **DX 改进**（新用户引导、错误信息改善、analytics 空状态提示） | 高 | 低 | 1-2 天 |
| **P1** | **Adapter 层单元测试**（6 个 Adapter 缺乏独立测试） | 高 | 低 | 1-2 天 |
| **P2** | **SPEC-0004 Security Model 设计稿**（不实现，只出设计） | 高 | 中 | 2-3 天 |
| **P3** | **Executor 集成测试**（当前只在间接测试） | 中 | 低 | 1 天 |
| **P4** | **Capability Registry 语义搜索**（向量索引） | 中 | 中低 | 3-5 天 |
| P5 | Adaptive Execution Graph | 中高 | 高 | 数周 |
| P6 | Evolution Loop | 高 | 高 | 需要 Execution Record 数据 |

**建议的 Phase 2 起点：DX 改进**

具体包括：
1. `intent-os analytics` 各项在没有数据时显示引导信息，而不是空白
2. `intent-os run` 在 Ollama 未运行时给出更精确的错误提示
3. 首次运行引导（`intent-os quickstart` 或自动检测）
4. Adapter schema 翻译的单元测试

### 12.3 常见问题

**Q: 为什么叫 Intent OS 而不是 Agent OS？**
A: 项目核心不是管理 Agent，而是管理 AI 能力（Capability）的描述、组合和执行。"Intent" 强调用户表达意图，系统负责执行。

**Q: 需要 API Key 才能跑吗？**
A: 不需要。安装 Ollama 后可以用本地模型，完全离线路。只有当你需要 GPT-4 或 Claude 时才需要 API Key。

**Q: 如何理解 Executor 和 Adapter 的关系？**
A: Executor 是编排层，负责选择 Adapter 并协调执行。Adapter 是翻译层，负责将 Manifest 翻译成具体 Runtime 的 API 格式。一个 Executor 可以注册多个 Adapter。

**Q: 为什么用 SQLite？**
A: Phase 1 的目标是最小可用。SQLite 零配置、单文件、Python 内置支持。Phase 2+ 可以换 PostgreSQL。

**Q: 为什么 CLI 叫 `intent-os`？**
A: 保持项目名称的完整性和可读性。

**Q: `cmd_mcp_server` 需要 HTTP 服务器吗？**
A: 不需要跑 HTTP 服务器来测试核心逻辑。`test_mcp_server.py` 直接测试 `_handle_tools_list()` 和 `_handle_tools_call()` 方法，不启动 HTTP。

### 12.4 关键的代码文件入口

| 文件 | 为什么重要 | 新会话应该读 |
|---|---|---|
| `cli.py` | CLI 调度入口，`build_parser()` + `CMD_MAP` | ✅ 必须读 |
| `commands/helpers.py` | 所有命令的共享工具函数 | ✅ 必须读 |
| `core/models.py` | 所有数据模型定义 | ✅ 必须读 |
| `core/workflow.py` | Workflow DAG + Execution Semantics 数据模型 | ✅ 推荐读 |
| `core/scheduler.py` | 工作流调度器，最复杂的组件 | ✅ 推荐读 |
| `core/executor.py` | 执行引擎，Adapter 的调用者 | ✅ 推荐读 |
| `core/workflow_parser.py` | Workflow YAML 正式解析器 | 需要时读 |
| `adapters/base.py` | Adapter 接口定义 | 需要时读 |
| `mcp_server.py` | MCP Server 实现 | 需要时读 |
| `POSITIONING.md` | 战略定位 | ✅ 必须读 |
| `CONSTITUTION.md` | 硬约束 | ✅ 必须读 |
| `GUIDE.md` | 本文件 | ✅ 必须读 |

---

## 13. 附录：关键洞察清单

### 13.1 项目演化路径

```
"AI 艺人公司" → "Agent OS" → "AI 操作系统" → "互操作层" → "Intent OS"
```

### 13.2 关键洞察

| # | 洞察 | 影响 |
|---|---|---|
| 1 | **Execution Semantic Fragmentation** 比 Tool Fragmentation 更深 | 决定了 Workflow Spec 的 Structure + Execution Semantics 拆分 |
| 2 | **Planner = AI Query Optimizer** | Planner 的核心不是"生成计划"而是"选择最优计划" |
| 3 | **不标准化智能，标准化交互** | 项目的防火墙，所有设计决策的试金石 |
| 4 | **Event = 训练数据，不是日志** | Event Store 的战略意义是 Planner 的数据来源 |
| 5 | **Control Plane 不拥有任何状态** | 五 Plane 架构中最关键的设计约束 |
| 6 | **Phase 0 最小验证** | 一个 Manifest，两个 Runtime，同一份 Execution Record |
| 7 | **Spec 可以被复制，生态才是护城河** | 战略重心在 Reference Runtime + Registry 而非 Spec |
| 8 | **Import/Export 桥接** | 不等别人适配，自己先翻译现有格式 |
| 9 | **"Describe once, execute consistently"** | 比 "Write once, run anywhere" 更精确 |
| 10 | **先积累数据再做优化器** | Phase 0 收集 Execution Record，Phase 2+ 才有数据喂给 Planner |

### 13.3 三方方案对比

| 维度 | ChatGPT 对话最终版 | 我的独立设计（第一轮） | 最终采用的方案 |
|---|---|---|---|
| 核心理念 | **开放规范 + 参考实现** | AI OS Kernel | ✅ **融合三者优点** |
| 核心抽象 | Capability / Workflow / Event 三个 Spec | PU（Processing Unit） | ✅ **三 Spec** |
| Execution Semantics | ✅ 独立成 Spec | ❌ 没有 | ✅ **独立成 Spec** |
| 冷启动策略 | Import/Export 桥接 | ❌ 无 | ✅ **桥接** |
| Human/AI 规则治理 | ✅ 分层权限 | ❌ 无 | 待实现 |
| Phase 0 验证 | 一个 Manifest 在两个 Runtime 上跑 | ❌ 无 | ✅ **已验证** |
