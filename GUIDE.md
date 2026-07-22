# Intent OS — 项目指导手册

> **版本:** v1.0
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
13. [附录：从 ChatGPT 对话中沉淀的关键洞察](#13-附录从-chatgpt-对话中沉淀的关键洞察)

---

## 1. 项目身份

- **当前名称:** Intent OS (0.2.0)
- **曾用名:** Agent OS（2026-07-21 前）
- **目录位置:** `~/Desktop/intent-os/`
- **旧目录:** `~/Desktop/agent-os/`（保留，未删除）
- **项目定位:** AI 能力互操作的开放规范与参考运行时
- **一句话定义:** Intent OS is an open interoperability layer for AI capabilities, workflows, and execution.

### 1.1 名称含义

Intent OS 不叫 "Agent OS" 的原因：项目核心不是管理 Agent，而是**管理 AI 能力（Capability）的描述、组合和执行。** "Intent" 强调用户表达意图，系统负责执行——这与我们的核心哲学一致（用户只说目标，不说过程）。

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

这三个已经不是同一个 Workflow。

**所以真正的敌人不是 Tool Fragmentation，而是 Execution Semantic Fragmentation。**

### 2.3 五个具体问题

| # | 问题 | 表现 | Intent OS 解决 |
|---|---|---|---|
| 1 | **Capability Fragmentation** | 同一能力适配 N 个平台 | Capability Manifest |
| 2 | **Workflow Lock-in** | 编排逻辑绑定平台 | Workflow Spec（含执行语义） |
| 3 | **Runtime Lock-in** | 用户被绑定到特定 Agent 平台 | Common Execution Model |
| 4 | **Engineering Gap** | Agent 缺日志、Trace、审计 | Event System |
| 5 | **Ecosystem Void** | 没有"AI 能力的 npm" | Registry + Marketplace |

### 2.4 为什么是现在

三个条件同时出现：
1. **模型能力已足够** — Agent 正在成为软件新形态
2. **Agent 大量出现**（2024-2026）— Claude Code、Codex、Cursor 等
3. **标准还未形成** — MCP 标准化了连接层，但**执行层是空白**

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

| Spec | 职责 | 类比 |
|---|---|---|
| **SPEC-0001: Capability Manifest** | 定义 AI 能力的统一描述格式 | OpenAPI |
| **SPEC-0002: Workflow Graph** | 定义工作流的拓扑 + 执行语义 | Kubernetes YAML |
| **SPEC-0003: Event Schema** | 定义执行事件格式 | OpenTelemetry |

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

**第一优先级（Phase 0 必须）— ★★★★★**

1. **Capability Registry + Manifest 解析** — 能力如何注册和被理解
2. **Execution Model — Capability Invocation** — 将 Manifest 映射到具体 Runtime
3. **Event System — Execution Record 生成** — 统一的执行记录

**第二优先级（Phase 1+）— ★★★★☆**

4. **Workflow Planner** — 从目标到执行计划（需要登记一定量的 Capability）
5. **Evolution Loop** — 从执行历史中学习优化（需要大量 Execution Record）

**核心思想：** 没有数据就不要设计优化器。Phase 0 收集 Execution Record，Phase 2+ 才有数据喂给 Planner。

---

## 6. 当前实现状态

**总测试：159 项，全部通过。**

### 6.1 版本演进

| 阶段 | 内容 | 测试 | 状态 |
|---|---|---|---|
| Phase 0 | 跨 Runtime 执行验证 | — | ✅ 实验通过 |
| Phase 0 | Manifest 解析器 + Adapter 层 | — | ✅ |
| Phase 0 | CLI 工具链（validate/run/compare/list） | — | ✅ |
| Phase 1 | Workflow Engine（DAG/Planner/Scheduler） | 34 | ✅ |
| Phase 1 | Import/Export（OpenAI/MCP 双向转换） | 26 | ✅ |
| Phase 1 | Event Store + Analytics（SQLite） | 35 | ✅ |
| Phase 1 | 项目改名 Intent OS + 打包 | — | ✅ |
| Phase 1 | Workflow 集成测试 + CLI | 20 | ✅ |
| Phase 1 | DevEx（Quickstart + hello-world + Ollama 降级） | — | ✅ |
| Phase 1 | 持久化 Registry + Workflow YAML 解析器 | 44 | ✅ |

### 6.2 已实现文件清单

**文档层（5 个文件）：**
- `README.md` — 项目入口
- `POSITIONING.md` — 战略定位（冻结）
- `CONSTITUTION.md` — 宪法（冻结）
- `ROADMAP.md` — 演化路线图
- `docs/QUICKSTART.md` — 5 分钟快速入门

**Spec 层（3 个文件）：**
- `specs/SPEC-0001-capability-manifest.md`
- `specs/SPEC-0002-workflow-graph.md`
- `specs/SPEC-0003-event-schema.md`

**核心引擎（reference-runtime/core/）：**
- `models.py` — 数据模型（Manifest / Event / ExecutionRecord）
- `parser.py` — Capability YAML 解析 + Schema 验证
- `registry.py` — Capability Registry（内存 + SQLite 持久化）
- `executor.py` — 执行引擎
- `recorder.py` — Event 记录器 + 跨 Runtime 比较算法
- `workflow.py` — Workflow 数据模型 + DAG 验证
- `workflow_parser.py` — Workflow YAML 专用解析器
- `workflow_runner.py` — 模拟执行器（用于集成测试）
- `planner.py` — 模板化工作流规划器
- `scheduler.py` — 执行调度器（完整状态机）
- `event_store.py` — SQLite Event Store
- `analytics.py` — 执行历史分析引擎

**Adapter 层（reference-runtime/adapters/）：**
- `base.py` — 抽象接口
- `openai_adapter.py` — OpenAI Function Calling
- `anthropic_adapter.py` — Anthropic Tool Use
- `ollama_adapter.py` — Ollama 原生 API（本地，无需 Key）
- `github_models_adapter.py` — GitHub Models（免费）
- `openrouter_adapter.py` — OpenRouter（统一 API）

**工具链（reference-runtime/tools/）：**
- `importer.py` — Import 编排
- `exporter.py` — Export 编排
- `formats/openai.py` — OpenAI ↔ Manifest 双向转换
- `formats/mcp.py` — MCP ↔ Manifest 双向转换

**CLI 入口：**
- `cli.py` — 8 个命令：validate / run / compare / list / workflow / import / export

**示例：**
- `examples/text_summarize.yaml` — text_summarize 能力
- `examples/hello-world/hello_world.yaml` — 最小示例
- `examples/research_workflow.yaml` — 4 步骤工作流

---

## 7. 文件结构

```
intent-os/
├── README.md
├── POSITIONING.md
├── CONSTITUTION.md
├── ROADMAP.md
│
├── docs/
│   └── QUICKSTART.md
│
├── specs/
│   ├── SPEC-0001-capability-manifest.md
│   ├── SPEC-0002-workflow-graph.md
│   └── SPEC-0003-event-schema.md
│
├── examples/
│   ├── hello-world/
│   │   ├── hello_world.yaml
│   │   └── README.md
│   ├── text_summarize.yaml
│   └── research_workflow.yaml
│
├── reference-runtime/
│   ├── pyproject.toml
│   ├── setup.py
│   ├── requirements.txt
│   ├── cli.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── parser.py
│   │   ├── registry.py
│   │   ├── executor.py
│   │   ├── recorder.py
│   │   ├── workflow.py
│   │   ├── workflow_parser.py
│   │   ├── workflow_runner.py
│   │   ├── planner.py
│   │   ├── scheduler.py
│   │   ├── event_store.py
│   │   └── analytics.py
│   │
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── openai_adapter.py
│   │   ├── anthropic_adapter.py
│   │   ├── ollama_adapter.py
│   │   ├── github_models_adapter.py
│   │   └── openrouter_adapter.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── importer.py
│   │   ├── exporter.py
│   │   └── formats/
│   │       ├── __init__.py
│   │       ├── openai.py
│   │       └── mcp.py
│   │
│   └── tests/
│       ├── test_workflow.py            (34)
│       ├── test_import_export.py       (26)
│       ├── test_event_store.py         (35)
│       ├── test_workflow_integration.py (20)
│       ├── test_workflow_parser.py     (23)
│       └── test_registry_persistence.py (21)
│
├── schemas/           # (空，待未来扩展)
└── tests/             # (空，待未来扩展)
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
- Phase 0 不做 Planner 和 Evolution Loop（没有数据）
- 不标准化智能（不写 Prompt、不选模型）
- Spec 开放，不属于任何公司
- 兼容先于替代

---

## 9. Phase 0 实验验证

### 9.1 核心 Thesis（已实验证明为工程事实）

> **同一个 Capability Manifest，在两个不同的 Runtime 上，能够被解析、加载、执行，并产生同一格式的 Execution Record。**

### 9.2 实验数据

| 对比 | 协议差异 | 结果 |
|---|---|---|
| OpenAI（GPT-4o）↔ Ollama（Llama 3.2 1B） | 完全不同（function calling vs HTTP + prompt） | ✅ COMPATIBLE |
| OpenAI（GPT-4o）↔ OpenRouter（Claude Sonnet 4） | 同协议不同提供商 | ✅ COMPATIBLE |
| OpenRouter（Claude）↔ Ollama（Llama 3.2 1B） | 完全不同 | ✅ COMPATIBLE |
| OpenAI ↔ GitHub Models | 同协议不同端点 | ✅ COMPATIBLE |

### 9.3 四层兼容性验证（Phase 0 成功标准）

| 层级 | 检查项 | 状态 |
|---|---|---|
| L1 — Schema Compatibility | 两个 Runtime 解析同一个 Manifest | ✅ |
| L2 — Capability Compatibility | 两个 Runtime 都能执行 | ✅ |
| L3 — Semantic Contract | 输出满足 Manifest 的 Schema | ✅ |
| L4 — Execution Record | 事件序列和指标维度一致 | ✅ |

### 9.4 三个 AI 时代的 Key 说明

实验过程中使用了三个 API Key：
- **OpenAI Key** (`sk-...`) — 调 GPT-4o，有付费额度才能运行
- **OpenRouter Key** (`sk-or-...`) — 统一调多个模型，免费额度有限
- **GitHub Token** (`ghp_...`) — 通过 GitHub Models 免费调 GPT-4o-mini

**关键发现：** GitHub Models 是 OpenAI 兼容的，所以 OpenAI ↔ GitHub Models 不是真正的跨协议验证。**OpenAI ↔ Ollama** 才是真正的跨协议验证（API 协议完全不同）。

---

## 10. 演化路径

```
Phase 0: AI Interoperability Layer  ← 当前已验证
    ↓ 产生执行数据
Phase 1: AI Capability Marketplace
    ↓ 积累足够 Capability
Phase 2: AI Execution Graph
    ↓ 积累大量 Execution Record
Phase 3: AI Query Engine
    ↓ Planner 有数据可优化
Phase 4: Self-optimizing AI Computing Infrastructure

未来演进方向（现有方案的自然延伸）：
  Task → Job + Task（Job 层管理用户完整目标）
  Registry → Capability Knowledge Graph（能力间关系）
  DAG → Adaptive Execution Graph（动态调整执行路径）
  Event → Learning Backbone（数据飞轮）
  Planner → Probabilistic Query Optimizer（带不确定性的 Cost Model）
```

### 10.1 Phase 0 明细

**验证假设：** 一个 Capability Manifest 可以在不同 Runtime 上执行。

**范围：**
- ✅ Capability Manifest 格式定义
- ✅ Reference Runtime（最小实现）
- ✅ 第二 Runtime Adapter
- ✅ Execution Record 生成

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

# 运行全部测试
python -m pytest tests/ -v

# 运行单文件测试
python -m pytest tests/test_workflow.py -v

# 运行单条测试
python -m pytest tests/test_workflow.py::TestWorkflowDAGValidation::test_cycle_detection -v

# 使用 unittest（无 pytest 时）
python -m unittest tests.test_workflow -v
```

### 11.2 运行 CLI

```bash
cd ~/Desktop/intent-os/reference-runtime

# 验证 Manifest
python cli.py validate examples/text_summarize.yaml

# 执行（需要 API Key）
export OPENAI_API_KEY="sk-..."
python cli.py run examples/text_summarize.yaml --adapter openai --input '{"text":"..."}'

# 跨 Runtime 比较（需要 API Key）
python cli.py compare examples/text_summarize.yaml --input '{"text":"..."}'

# 工作流规划（本地运行，不需要 Key）
python cli.py workflow plan "research NVIDIA stock"

# 工作流执行（本地模拟，不需要 Key）
python cli.py workflow run examples/research_workflow.yaml --input '{"company":"NVIDIA"}'

# import/export
python cli.py import openai-function my_tool.json
python cli.py export openai manifest.yaml --as-tool
```

### 11.3 测试命名规范

- 测试类名：`Test` + 组件名（如 `TestWorkflowDAGValidation`）
- 测试方法名：`test_` + 场景描述（如 `test_cycle_detection`）
- 断言风格：`assert` 语句（非 `self.assertEqual`）
- 使用 `pytest` 的 fixture 时：用 `setup_method` / `teardown_method`

### 11.4 代码风格

- Python 3.10+
- 类型注解（`from __future__ import annotations`）
- 使用 `dataclass` 而非手写类
- 文件名小写下划线（`workflow_parser.py`）
- 类名 PascalCase
- 方法名 / 变量名 snake_case
- 模块 docstring 包含文件名和简要说明
- 所有文件头部 docstring 使用 "Intent OS —" 前缀

### 11.5 新增 Adapter 规范

1. 继承 `adapters/base.py` 中的 `AdapterBase`
2. 实现 `name`、`version`、`default_model` 属性和 `execute()` 方法
3. 在 `cli.py` 的 `_setup_executor()` 中注册
4. `execute()` 方法必须返回包含 `_token_usage` 和 `_cost` 的 dict

### 11.6 新增 Spec 规范

1. 按 `specs/SPEC-XXXX-name.md` 编号
2. 包含 Purpose、Design Principles、Specification（含 YAML 示例）、Validation Rules
3. 每条规则必须可测试验证

### 11.7 文档规范

- 所有文档使用 Markdown
- 版本号在冻结时标注（`> **Version:** v1.0 (Frozen)`）
- 文件名大写（`POSITIONING.md`、`CONSTITUTION.md`）
- 项目名称统一用 "Intent OS"

---

## 12. 如何继续

### 12.1 第一步

在新会话中打开本文件（`GUIDE.md`），然后：

```bash
cd ~/Desktop/intent-os
# 先跑测试确认环境正常
cd reference-runtime && python -m pytest tests/ -v
```

### 12.2 优先级排序（当前 Phase 1 待完成）

按优先级从高到低：

1. **完善 Adapter 层的错误处理** — 当前错误可能是 `server_error` 字符串格式，需要标准化
2. **Workflow Engine 与真实 Adapter 集成** — 目前 Scheduler 只能用模拟 Runner，需要连接到真实 Adapter
3. **Capability Registry CLI 集成** — 当前 Registry 需在代码中创建，CLI 没有 `registry` 子命令
4. **更多 Runtime Adapter** — Google Gemini、Anthropic 原生（需要 Key）
5. **Workflow Execution Semantics 在 Scheduler 中的完整实现** — 补偿策略还未实现
6. **SPEC-0004: Security / Permission Model** — 设计稿
7. **Evolution Loop 原型** — 基于 Event Store 的分析

### 12.3 常见问题

**Q: 为什么叫 Intent OS 而不是 Agent OS？**
A: 项目核心不是管理 Agent，而是管理 AI 能力（Capability）的描述、组合和执行。"Intent" 强调用户表达意图，系统负责执行。

**Q: 需要 API Key 才能跑吗？**
A: 不需要。安装 Ollama 后可以用本地模型，完全离线路。只有当你需要 GPT-4 或 Claude 时才需要 API Key。

**Q: 为什么 CLI 叫 `intent-os` 而不是 `intentos`？**
A: 保持项目名称的完整性和可读性。

**Q: 如何理解 Executor 和 Adapter 的关系？**
A: Executor 是编排层，负责选择 Adapter 并协调执行。Adapter 是翻译层，负责将 Manifest 翻译成具体 Runtime 的 API 格式。一个 Executor 可以注册多个 Adapter。

**Q: 为什么用 SQLite 而不是更强大的数据库？**
A: Phase 1 的目标是最小可用。SQLite 零配置、单文件、Python 内置支持，足够验证 Event Store 和 Registry 持久化的价值。Phase 2+ 可以换 PostgreSQL。

### 12.4 关键的代码文件入口

| 文件 | 为什么重要 | 新会话应该读 |
|---|---|---|
| `cli.py` | CLI 入口，8 个命令的全部实现 | ✅ 必须读 |
| `core/models.py` | 所有数据模型定义 | ✅ 必须读 |
| `core/executor.py` | 执行引擎，Adapter 的调用者 | ✅ 推荐读 |
| `core/scheduler.py` | 工作流调度器，最复杂的组件 | ✅ 推荐读 |
| `adapters/base.py` | Adapter 接口定义 | ✅ 推荐读 |
| `adapters/openai_adapter.py` | 第一个实现的 Adapter | 需要时读 |
| `core/workflow.py` | Workflow DAG 数据模型 | 需要时读 |
| `core/registry.py` | Capability 注册表（含持久化） | 需要时读 |
| `POSITIONING.md` | 战略定位 | ✅ 必须读 |
| `CONSTITUTION.md` | 硬约束 | ✅ 必须读 |

---

## 13. 附录：从 ChatGPT 对话中沉淀的关键洞察

项目最重要的定位和架构决策，源于一场 70 轮的 ChatGPT 深度对话。以下是从中提取的核心洞察：

### 13.1 项目演化路径

```
"AI 艺人公司" → "Agent OS" → "AI 操作系统" → "互操作层" → "Intent OS"
```

每一轮都在缩小范围、提升精度。

### 13.2 关键洞察清单

| # | 洞察 | 影响 |
|---|---|---|
| 1 | **Execution Semantic Fragmentation** 比 Tool Fragmentation 更深 | 决定了 Workflow Spec 的拆分解构 |
| 2 | **Planner = AI Query Optimizer** | Planner 的核心不是"生成计划"而是"选择最优计划" |
| 3 | **不标准化智能，标准化交互** | 项目的防火墙，所有设计决策的试金石 |
| 4 | **Event = 训练数据，不是日志** | Event Store 的战略意义是 Planner 的数据来源 |
| 5 | **Control Plane 不拥有任何状态** | 五 Plane 架构中最关键的设计约束 |
| 6 | **Phase 0 最小验证** | 一个 Manifest，两个 Runtime，同一份 Execution Record |
| 7 | **Spec 可以被复制，生态才是护城河** | 项目战略重心在 Reference Runtime + Registry 而非 Spec |
| 8 | **Import/Export 桥接** | 不等别人适配，自己先翻译现有格式 |
| 9 | **"Describe once, execute consistently"** | 比 "Write once, run anywhere" 更精确 |

### 13.3 三个版本的方案比较

| 维度 | ChatGPT 对话最终版 | 我的独立设计（第一轮） | Codex 的版本 |
|---|---|---|---|
| 核心理念 | **开放规范 + 参考实现** | AI OS Kernel | 三层架构 + 算法 |
| 核心抽象 | Capability / Workflow / Event 三个 Spec | PU（Processing Unit） | Capability Registry |
| 命名 | Agent OS → Intent OS | Agent OS | Agent OS |
| 最小验证 | 一个 Manifest 在两个 Runtime 上跑 | ❌ 无 | 嘴上说了但架构没体现 |
| Execution Semantics | ✅ 独立成 Spec | ❌ 没有 | ❌ 混在算法里 |
| Cost Model | ✅ Planner = Query Optimizer | 部分 | 部分 |
| 冷启动策略 | Import/Export 桥接 | ❌ 无 | Import/Export |
| Human/AI 规则治理 | ✅ 分层权限 + 审批流 | ❌ 无 | 一句话带过 |
| 最终选用的方案 | ✅ **（融合了三个版本的优点）** | — | — |

---

*本文件应当放置在 `~/Desktop/intent-os/GUIDE.md`。在新会话开始时优先读取此文件。*
