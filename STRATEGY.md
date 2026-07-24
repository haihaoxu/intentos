# Intent OS — 战略与逻辑

> **不是"我们做一个 Agent 监控工具"。是"AI Agent 正在从工具变成执行主体，但整个世界还没有为它们建立身份、记录、责任和协作标准。Intent OS 正在构建这一层基础设施。"**

**2026-07-24**

---

## 一、我们观察到了什么

### 一个正在发生的、不可逆的结构性变化

AI 正在从一个*回答问题*的系统，变成一个*自主执行任务*的系统。

```
过去：人 → 写代码 → 运行 → 结果
现在：人 → 给目标 → Agent 自主规划 → 调用工具 → 修改环境 → 产生结果
```

这个变化的核心不是"AI 变强了"。是**权力转移**——Agent 从"建议者"变成了"执行者"。执行权一旦转移，人类需要的就不再只是更好的模型，而是**一个能约束、记录、证明和追责这个执行过程的系统**。

### 四个已经发生、但不被广泛承认的事实

1. **Agent 没有身份。** 今天的所有 Agent 都是 API Key。它们没有 ID、没有归属、没有权限边界。想象一个公司有 100 个 Agent——没有人能回答"谁干的"。

2. **Agent 执行不可见。** Agent 跑 30 分钟，调用几十次模型，修改十几个文件，然后说"完成了"。没有轨迹，没有证据。

3. **Agent 被锁定在 Runtime 里。** 你在 Claude 上花三个月打造的 Agent，不能搬到 OpenAI。你的能力不属于你——它属于你选择的平台。

4. **每一次 Agent 执行都是一次性消耗。** 执行完就消失了。最有价值的资产——Agent 如何做决策的数据——全部丢弃。

---

## 二、这四个事实指向同一个缺口

**AI Agent 缺少一个跨 Runtime 的可移植执行契约（Portable Execution Contract）。**

这不是一个功能缺口。是基础设施缺口。

历史上每一个重大计算生态，都有一个中间层使能力可移植：

| 时代 | 能力 | 被锁在 | 中间层 |
|------|------|--------|--------|
| 软件 | 代码 | 硬件 | 操作系统 |
| Web | 服务 | 网络协议 | HTTP |
| 云 | 应用 | 基础设施 | Container / K8s |
| **AI Agent** | **Agent 能力** | **Runtime** | **← 不存在** |

Intent OS 存在的理由就是补上这一层。

---

## 三、我们的解决方案

**一个可移植的 Agent 执行契约——由六个条款组成。**

当任何一个 Agent 要在任何 Runtime 上运行，它必须回答六个问题：

```
1. Identity      → "Who is this agent, and who does it represent?"
2. Capability    → "What can this agent do?"
3. Context       → "What environment does this agent need?"
4. Execution     → "What did this agent actually do?"
5. Verification  → "Can we prove its claims are true?"
6. Governance    → "Was it allowed to do that?"
```

这六个条款合在一起，就是**Agent Execution Contract**。它是 Agent 的身份证、简历、操作日志、证据链和权限文件的总和。

```
                    Agent Capability
                          │
                          │  "I am this Agent.
                          │   I can do these things.
                    ┌─────▼──────┐   I need this context.
                    │  Execution  │   Here is what I did.
                    │  Contract   │   Here is the evidence.
                    └─────┬──────┘   These are my boundaries."
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    Claude RT       OpenAI RT        Ollama RT
```

---

## 四、我们的路径

### 你不能一上来就宣布标准

1995 年有人说"我要制定 Web 标准"——没人理。但他说"我做一个浏览器"——大家用了。20 年后，那个浏览器定义的格式就是 Web 标准。

**标准不是靠宣布建立的。是靠"先用起来"建立的。**

### 四阶段路径

```
Phase 1: Observe    →  用 Flight Recorder 收集执行数据
Phase 2: Standardize → 冻结 Execution Contract（Identity + Manifest + Event + Context + Evidence）
Phase 3: Portable   →  同一个 Agent，任何 Runtime
Phase 4: Economy    →  Agent 成为可发现、可交易、可评级的资产
```

**当前：Phase 1。** `pip install intentos` → `intent-os proxy start` → 每一次 Agent 执行都被记录为 Execution Record。这些数据是冻结标准之前无论如何必须先有的。

---

## 五、我们如何进入市场

### 靠一个今天已经存在的痛

不是"Agent 没有执行契约"。没人在搜这个词。

是四个现在就能感受到的痛：

| 用户类型 | 真正的恐惧 | 我们的入口 |
|----------|-----------|-----------|
| **Vibe coder** | "我害怕给它大任务。改太多文件，我不知道它改了什么。" | `intent-os doctor` |
| **专业开发者** | "花了 30 分钟失败了。没有 stack trace。没有日志。" | `intent-os inspect latest` |
| **小团队** | "API 账单 $300，哪个 agent？哪个任务？不知道。" | `intent-os cost --by agent` |
| **企业** | "AI 出事故谁也解释不了。不敢规模化用。" | `intent-os audit report --format html` |

入口只有一个：**"你敢放手让 Agent 干活吗？"**

### 入口和终局不能混淆

```
入口： Flight Recorder — "我的 Agent 做了什么？"
      ↓ 使用 → 数据积累 → 格式渗透
终局： Execution Contract — "Agent 世界的 HTTP"
```

你不用告诉入口用户什么是 Execution Contract。就像你不用告诉 Git 用户什么是 Merkle DAG。但你自己的每一行代码、每一个 Spec 冻结、每一个模块边界，都必须服务于那个终局。

---

## 六、我们的护城河

### 护城河 1：Execution Data

谁拥有最多的 Agent 执行数据，谁就最有机会定义标准。

Intent OS 的数据引擎已经在运行：721 tests, 26 种 EventType, Agent ID, 6 个 Adapter, SSE 实时捕获。每一个 `pip install intentos` 都是数据引擎的燃料。

### 护城河 2：Frozen Spec

标准的核心资产是 Spec。我们已经有 7 个 Spec，最关键的 4 个已 Frozen v1.0：

- SPEC-0001: Capability Manifest（Frozen）
- SPEC-0002: Workflow Graph（Frozen）
- SPEC-0003: Event Schema（Frozen）
- SPEC-0007: Infrastructure Standard（Frozen）

一个陌生开发者只读 Spec、不读代码，能不能写出兼容实现？这是标准是否真正开放的检验标准。上次审计已确认 SPEC-0001/0003 通过这个检验。

### 护城河 3：Execution Contract 的心智占领

当行业开始讨论"Agent 需要标准"时，Intent OS 已经：
- 定义了六个条款
- 冻结了 Spec
- 有 25 个 CLI 命令
- 有 721 个测试
- 在 PyPI 上，AGPLv3 开源

心智占领不是靠广告。是靠"当别人还在争论要不要做标准的时候，你已经把标准写好了"。

---

## 七、我们不是什么

明确排除，防止叙事稀释：

- ❌ 不是一个 Agent Framework（不是 LangChain、CrewAI 替代品）
- ❌ 不是一个新的大模型
- ❌ 不是一个 AI 应用
- ❌ 不是一个日志工具（长期是 Execution Infrastructure）
- ❌ 不是一个 Monitoring/SaaS 平台

---

## 八、一句话总结

> **Intent OS is building the portable execution contract for AI agents — the missing infrastructure layer between Agent Capabilities and Runtimes.**

不是"做了一个工具"。是在**抢占一个还不存在的品类定义权**。

当 AI Agent 从"助手"变成"执行者"，世界需要一个新的基础设施层来定义 Agent 的身份、能力、执行记录、证据和治理。这个层在今天还没有名字。Intent OS 正在给它命名。
