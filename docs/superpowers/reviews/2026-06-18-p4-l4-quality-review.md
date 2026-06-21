# P4 L4 内容质量审查报告

> 审查对象：L4 · 框架与运行时层（12 节 + README，13 个 markdown 文件）
> 审查日期：2026-06-18
> head SHA：a576ac4
> 审查范围：API 编造、版本/日期失真、数据失真、代码块格式、引用准确性

---

## 优点（本批次做得好的地方）

1. **SDK API 引用真实可靠**——本批次最容易翻车的两个 SDK（OpenAI Agents SDK 0.17.5、Claude Agent SDK 0.2.104）核心 API 全部验证存在：`Agent` / `Runner` / `function_tool` / `MCPServerStdio` / `GuardrailFunctionOutput` / `input_guardrail`（4.7）；`query` / `ClaudeSDKClient` / `@tool` / `create_sdk_mcp_server` / `HookMatcher` / `betas: list[SdkBeta]` 含 `context-1m-2025-08-07`（4.8）。**没有出现 P3 类似的 a2a-sdk 整段编造问题**。

2. **AutoGen v0.4 维护模式描述准确**——4.5 反复强调"AutoGen README 标注 Maintenance Mode"与官方推荐迁移到 Microsoft Agent Framework，与 `microsoft/autogen` 当前 README 一致（curl 验证 ✓）。这种"事实标注"是 L4 难得的硬功夫。

3. **LangGraph `interrupt()` API 描述准确**——4.3 第 99-106 行代码使用 `interrupt({...})` 函数式调用 + `Command(resume=...)` 恢复，对应 LangGraph 0.4+ 推荐的新写法；README 也确认 `interrupt` 是 LangGraph 公共导出。

4. **`MemorySaver` 别名描述准确**——4.3 第 12 行说"InMemorySaver 是 2025 重命名后的默认；早期文档中的 MemorySaver 仍是常见别名"，源码确认 `MemorySaver = InMemorySaver  # Kept for backwards compatibility`，与描述一致。

5. **每个章节末尾提供 S/A 级引用清单**——这是 L4 的工程化亮点，让读者能反查一手资料。12 节都包含引用块（除 4.8 略厚外，其余基本标准）。

---

## 关键问题（K 级，必须修复）

### K1: 4.12 时间线多个关键日期严重失真

**文件**：`handbook/l4-framework/4.12-framework-timeline.md`
**位置**：第 39-54 行（mermaid Gantt 图）+ 第 100-134 行（milestones 列表）

curl 验证数据：

| 事件 | 4.12 写法 | 实际日期 | 偏差 | 来源 |
|---|---|---|---|---|
| AutoGen v0.4 actor-model 重构 | 2024-08 | **2025-01-09** | **+5 个月** | PyPI `autogen-agentchat==0.4.0` |
| CrewAI 1.0 GA | 2025-05 | **2025-10-20** | **+5 个月** | PyPI `crewai==1.0.0` |
| Claude Agent SDK 公开 | 2025-09 | **2025-10-11** | +1 个月 | GitHub `v0.1.3` |
| A2A 协议 v0.1 | 2025-04 | **2025-06-09** | +2 个月 | GitHub `a2aproject/A2A v0.1.0` |
| LangChain 1.0 alpha | 2024-12 | **2025-08-27** | **+8 个月** | PyPI `langchain==1.0.0a1` |
| LangGraph 0.1 状态机框架 | 2024-01 | **2024-01-09 (0.0.10)** | 偏差小 | PyPI 首个 0.0.x 实际是 2024-01-09 |
| OpenAI Agents SDK 首发 | 2025-03 | 2025-03-13 | 准确 ✓ | GitHub `v0.0.4` |
| LangChain 0.1 早期包 | 2022-10 | 2022-10-25 (0.0.1) | 准确 ✓ | PyPI |

**严重程度**：K（关键）。这是 L4 收尾节，"框架从何而来"的时间线是 P4 的工程化根基。5 处偏差中有 2 处偏差 5 个月以上，会让按时间线选型的读者做出错误推断（例如把已存在半年的 Stable 当成"刚发布"）。

**修复方向**：
1. AutoGen v0.4 → 改为 `2025-01`（实际是 2025-01-09）
2. CrewAI 1.0 → 改为 `2025-10`（1.0.0 final 在 2025-10-20）
3. A2A v0.1 → 改为 `2025-06`（v0.1.0 在 2025-06-09）
4. Claude Agent SDK → 改为 `2025-10`（首个公开 release v0.1.3 在 2025-10-11）
5. LangChain 1.0 alpha → 改为 `2025-08`（1.0.0a1 在 2025-08-27）；GA `2025-10-17` 是准确的
6. Gantt 图日期同步更新

### K2: 4.5 / 4.1 / 4.10 AutoGen 版本号 "v0.7" 误导

**文件**：
- `handbook/l4-framework/4.1-framework-landscape.md` 第 38 行：`AG[AutoGen v0.7<br/>维护模式]`
- `handbook/l4-framework/4.5-autogen-conversational-multiagent.md` 多处出现 `v0.4+`
- `handbook/l4-framework/4.10-framework-decision-matrix.md` 第 42 行：`F4[AutoGen v0.7]`

**问题**：4.1 和 4.10 mermaid 图写 `AutoGen v0.7`，但 4.5 正文说"v0.4 actor-model 重构"且全文以 v0.4 为基线。读者会困惑："v0.7 还是 v0.4？"。

curl 验证：AutoGen 当前最新版本 `python-v0.7.5` 发布于 2025-09-30，确实是 v0.7。但 4.5 正文代码示例仍是 v0.4 风格 API（`AssistantAgent` + `model_client` + `McpWorkbench`），没有标注 v0.5/v0.6/v0.7 的破坏性变更。

**严重程度**：K（关键）。读者会按图索骥去查"AutoGen v0.7"，但 4.5 给的是 v0.4 API。即使 API 在 0.4-0.7 之间相对稳定，**版本号不一致 = 信息失真**。

**修复方向**：
1. 4.1 / 4.10 mermaid 图统一改为 `AutoGen v0.4+` 或 `AutoGen v0.7` 并保持全文一致
2. 4.5 在"维护模式与迁移"小节顶部加一句："本文以 v0.4 API 为基线写就；当前 PyPI 最新版为 v0.7.5（2025-09-30），0.5-0.7 主要增加新 teams（`MagenticOneGroupChat`）与 OpenAI 客户端能力，主体 API 兼容"

### K3: 4.7 OpenAI Agents SDK Sandbox Agents 描述与时间错位

**文件**：`handbook/l4-framework/4.7-openai-agents-sdk.md`
**位置**：第 14 行（正文）、第 238-240 行（实战片段）

**问题**：
- 第 14 行："2025-09 后新增 Sandbox Agents：在 v0.14.0 引入"
- curl 验证：`openai-agents==0.14.0` 实际发布于 **2026-04-15**（不是 2025-09）

OpenAI Agents SDK 当前版本 `0.17.5`（2026-06-11）。Sandbox Agents 是 2026-Q2 才加入的能力，**不是 2025-09**。

**严重程度**：K（关键）。把一个 2026 年初才出现的能力归到"2025-09"会让读者误以为"Agent SDK 一发布就支持 Sandbox"——这是事实性错误。

**修复方向**：第 14 行改为"**2026-Q2 新增 Sandbox Agents**：在 v0.14.0（2026-04-15）引入"，并把第 50 行依赖 `openai-agents>=0.10` 改为 `>=0.14`。

### K4: 4.8 Claude Agent SDK 发布日期与首发版本错位

**文件**：`handbook/l4-framework/4.8-claude-agent-sdk.md`
**位置**：第 9 行（"2025 年开源"）、第 55 行（依赖 `claude-agent-sdk>=0.1`）

**问题**：
- 第 9 行：说"Anthropic 在 2025 年开源的 Python SDK"
- 4.12 时间线第 52 行：`Claude Agent SDK 公开 :ca1, 2025-09, 12M`
- curl 验证：首个公开 release `v0.1.3` 在 **2025-10-11**（不是 2025-09）；早期 v0.1.0/v0.1.1/v0.1.2 应该是 internal/alpha

**严重程度**：K（关键）。时间偏差 1 个月看似不大，但 4.8 描述的 SDK 实际首发是 2025-10，而 4.12 把它放在 2025-09，会让读者误以为"9 月已 GA"。

**修复方向**：4.8 第 9 行改"2025-10 开源"；4.12 Gantt 图 `2025-09` → `2025-10`；同时核实 Claude Code CLI bundling 的具体细节——README 已确认 "The Claude Code CLI is automatically bundled"，与 4.8 描述一致 ✓。

---

## 重要问题（I 级，建议修改）

### I1: 4.12 mermaid Gantt 图日期与里程碑表日期自相矛盾

**文件**：`handbook/l4-framework/4.12-framework-timeline.md`
**位置**：第 36-54 行 vs 第 100-134 行

**问题**：Gantt 图写 `LangGraph 0.1 状态机 :lg1, 2024-01, 18M`，但里程碑表写 `2024-01 LangGraph: 0.1 状态机框架发布`——这两个"2024-01"对应 LangGraph 首个 0.0.10 版本（2024-01-09），不是真正的"0.1 状态机框架"。实际 LangGraph 0.1.x 系列首版 `0.1.1` 在 2024-06-22。**两处互相"自洽"但与实际都不符**。

**严重程度**：I（重要）。Gantt 图是 L4 最常被引用的视觉资产，日期偏差会让读者在画自己的演进路线时被误导。

**修复方向**：Gantt 图 `lg1, 2024-01` 改为 `lg1, 2024-06`（对应 0.1.1）；同时里程碑表 `2024-01` 改为 `2024-06`。

### I2: 4.4 LlamaIndex `FunctionCallingAgent` 已重构为 `FunctionAgent` + Workflows

**文件**：`handbook/l4-framework/4.4-llamaindex-rag-paradigm.md`
**位置**：第 161 行、第 205 行

**问题**：4.4 实战片段代码用 `from llama_index.core.agent import FunctionCallingAgent` 和 `FunctionCallingAgent.from_tools(tools, llm=Settings.llm)`。

curl 验证：当前 `llama-index==0.14.22` 已重构为 `from llama_index.core.agent.workflow.function_agent import FunctionAgent`，继承 `BaseWorkflowAgent`。原 `FunctionCallingAgent` 是早期 API。

**严重程度**：I（重要）。新读者照搬 4.4 代码会运行失败。

**修复方向**：第 161 行改为 `from llama_index.core.agent.workflow import FunctionAgent`，第 205 行 `FunctionCallingAgent.from_tools(...)` 改为 `FunctionAgent(name="...", tools=tools, llm=Settings.llm)`。同时检查 README 中的 agent 用法：`from llama_index.core.workflow import Workflow` 已存在，Workflows API 仍然可用 ✓。

### I3: 4.5 AutoGen v0.4+ → v0.7 API 演进未交代

**文件**：`handbook/l4-framework/4.5-autogen-conversational-multiagent.md`
**位置**：整个文件以 v0.4 为基线

**问题**：curl 验证显示 AutoGen 已经历 v0.4 → v0.5 (2025-04) → v0.6 (2025-06) → v0.7 (2025-07)。4.5 仅在第 219 行轻描淡写"AutoGen v0.4+ 与 Microsoft Agent Framework (MAF) 概念对齐"，没有交代 0.5-0.7 的具体变化（如新增 `MagenticOneGroupChat`、`AgentTool` 优化）。

**严重程度**：I（重要）。当读者点开 PyPI 安装 `autogen-agentchat>=0.4`，会发现装到 0.7.x，但 4.5 给的代码示例未必在 0.7 全部兼容。

**修复方向**：在 4.5 顶部加"本文 API 以 v0.4 为基线写就；当前 PyPI 最新版为 v0.7.5（2025-09-30），建议 `pip install "autogen-agentchat>=0.4,<0.8"` 以锁定兼容范围"。如发现破坏性变更，标注具体受影响 API。

### I4: 4.12 阶段 3 milestone `2025-04 A2A 协议 v0.1` 写作不准

**文件**：`handbook/l4-framework/4.12-framework-timeline.md`
**位置**：第 128 行（阶段 3 milestones）、第 52 行（Gantt 图 `A2A 协议 v0.1 :a2a, 2025-04`）

**问题**：A2A v0.1.0 实际在 **2025-06-09** 发布，不是 2025-04。这是 K1 的衍生 I 级条目（Gantt 与 milestone 表同一日期偏差）。

**严重程度**：I（重要，与 K1 部分重叠）。如果 K1 修复时改了日期，此条自动消解。

**修复方向**：第 128 行 `2025-04` → `2025-06`；第 52 行 Gantt `2025-04` → `2025-06`。

### I5: 4.1 / 4.10 引用 CrewAI "1.14" 但版本号是 PyPI stable 不一致

**文件**：
- `handbook/l4-framework/4.1-framework-landscape.md` 第 39 行：`CR[CrewAI 1.14<br/>角色协作]`
- `handbook/l4-framework/4.10-framework-decision-matrix.md` 第 43 行：`F5[CrewAI 1.14]`

**问题**：PyPI `crewai==1.14.7`（2026-05 之前）是 1.14 系列。1.0 系列在 2025-10 GA。4.6 写 `crewai>=1.0` 是兼容的。但 4.1/4.10 mermaid 图写"1.14"会让读者以为有"1.14 这个稳定版本"——而 1.14 是 2026-Q2 才出现的版本。

**严重程度**：I（重要）。mermaid 图是节选引用最频繁的地方，版本号 1.14 vs 1.0 容易混淆。

**修复方向**：统一写 `CrewAI 1.x`，或在文中加脚注说明"1.14 = 2026-Q2 的 stable 系列"。

### I6: 4.6 CrewAI "2024 起新增 Flows" 描述含糊

**文件**：`handbook/l4-framework/4.6-crewai-role-based.md`
**位置**：第 9 行、第 14 行

**问题**：第 9 行 "2024 年起新增 `Flows` 提供事件驱动精细控制"。Flows 实际首次稳定发布更晚（具体日期 curl 验证未深入，但 1.0 GA 时是 2025-10）。需要核实具体首发月份。

**严重程度**：I（重要）。Flows 是 CrewAI 的差异化能力，"2024 年起"模糊会让读者误以为 CrewAI 早期就有 Flows。

**修复方向**：核实 Flows 首发日期（curl 应查 `crewai==0.x` 的 `crewai.flow` 模块首次出现的版本），如确属 2024 后期写"2024-Q4 起"。

### I7: 4.7 guardrail API 描述与最新版 SDK 略有偏差

**文件**：`handbook/l4-framework/4.7-openai-agents-sdk.md`
**位置**：第 165-194 行（`input_guardrail` 装饰器 + `GuardrailFunctionOutput`）

**问题**：4.7 给的代码：
```python
from agents import (
    Agent, Runner, function_tool, input_guardrail, output_guardrail,
    GuardrailFunctionOutput, RunContextWrapper, TResponseInputItem,
)
```

curl 验证 `0.17.5` README，core concepts 包括 Guardrails/Human in the loop/Sessions/Realtime Agents——说明 guardrail API 是稳定的。但 `RunContextWrapper` 在新版本可能有所演进。建议核查 `TResponseInputItem` 是否仍存在或已重命名。

**严重程度**：I（重要）。代码示例可能在新版本有 import 报错。

**修复方向**：实测 `from agents import TResponseInputItem` 是否在 0.17.5 仍可导出；如已 deprecated，改用新名称或在脚注中说明。

### I8: 4.8 `betas` 字段示例位置不当

**文件**：`handbook/l4-framework/4.8-claude-agent-sdk.md`
**位置**：第 263 行（实战片段注释 "生产上配 `betas=["context-1m-2025-08-07"]` 启用 1M 上下文窗口"）

**问题**：curl 验证 `betas: list[SdkBeta]` 真实存在，但该字段在 `ClaudeAgentOptions` 中的使用方式应单独写一行示例。当前只是注释提及，读者难以快速复制。

**严重程度**：I（重要）。属于 API 真实但使用方式不显式。

**修复方向**：把 `betas=["context-1m-2025-08-07"]` 显式加进 options 构造示例，让用户能直接复用。

---

## 次要问题（M 级，可酌情修改）

### M1: 4.2 第 9 行 "agent 创建从 `initialize_agent` 改为 `create_react_agent` / LangGraph" 描述

- `initialize_agent` 是 LangChain 0.x 的 high-level API，1.x 已废弃。但 1.x 推荐入口是 `langchain.agents.create_agent`（高阶封装）而非 `create_react_agent`（LangGraph prebuilt）。两者定位不同：前者是 LangChain 1.x 的"统一 agent 创建函数"，后者是 LangGraph 的"ReAct 预构建"。
- 修复方向：明确区分"LangChain 1.x 用 `langchain.agents.create_agent`，需要 ReAct + 状态机用 `langgraph.prebuilt.create_react_agent`"。

### M2: 4.6 第 130 行 `from langchain_openai import ChatOpenAI` 作为 CrewAI manager LLM

- 跨框架引用 LangChain 客户端会让人误以为 CrewAI 依赖 LangChain。实际 CrewAI 完全独立（README 原话），manager_llm 应该用 LiteLLM 或 CrewAI 自带 `LLM` 类。
- 修复方向：改为 `from crewai import LLM; manager_llm = LLM(model="gpt-4.1")`。

### M3: 4.1 第 18 行 "LangChain 139k stars" 数据待验证

- P3 教训中 3.3 MCP stars 严重失真（"5k+" 实际 87k+）。LangChain 实际 stars 应通过 GitHub API 实时核实。
- 修复方向：用 curl `https://api.github.com/repos/langchain-ai/langchain` 拿到当前 stargazers_count；4.1 第 18 行用 "LangChain X 万 stars（截至 2026-06）"。

### M4: 4.7 第 14 行 Sandbox Agents 时间描述与 K3 重叠

- M 级简化版：写"2025-Q3 后"已足够模糊，但若 K3 修复"2025-09"应同时改这里。

### M5: 4.10 决策矩阵 AutoGen "维护状态 = 1" 评分过于主观

- 第 133 行 `Framework("AutoGen v0.7", { ..., "维护状态": 1, })`——"1"对应"完全不满足"过于极端。实际 AutoGen 仍可用、文档完整、PyPI 持续发版（0.7.5 在 2025-09-30）。
- 修复方向：调整为"维护状态 = 2"（"部分支持——仍可用但停止新特性"），并在评分说明中注明评分依据。

### M6: 4.12 Gantt 图 "LangChain 1.0 / LangGraph 1.0 :lg2, 2025-10, 12M" 时长与实际不符

- LangChain 1.0.0 = 2025-10-17；当前最新 1.2.x（2026-04）。Gantt 图说"12M"对应 2026-10，实际产品周期仍在演进。
- 修复方向：Gantt 末尾可用 `till now` 或具体月份。

### M7: 4.8 第 124 行 `elif isinstance(message, ResultMessage := message.__class__):` 海象运算符写在 isinstance 里

- 代码风格问题：`isinstance(message, ResultMessage := message.__class__)` 是非常规写法，简化版反而失真。应直接 `elif isinstance(message, ResultMessage):`。
- 修复方向：简化 isinstance 判断。

### M8: 4.5 第 124 行 `workbench=mcp,` 后接 `model_client_stream=True,` 字段顺序

- `model_client_stream` 字段在最新 0.7.x 仍存在 ✓；但其他字段如 `max_tool_iterations` 顺序在多 Agent 代码中位置合理，可保持。

---

## 评估结论

**结论：有条件通过**

L4 整体质量较高——SDK API 引用全部真实（避免 P3 a2a-sdk 类问题）、LangGraph/AutoGen 维护模式标注准确、Adapter 模式设计合理。**主要扣分项是 4.12 时间线的多日期失真**（K1 包含 5 处偏差），这是 L4 收尾节最关键的硬数据。

**修复优先级**：
- 必须修复（阻塞合并）：K1（4.12 时间线 5 处日期偏差）、K2（AutoGen v0.7 vs v0.4 不一致）、K3（Sandbox Agents 2025-09 误写）、K4（Claude Agent SDK 发布日期）
- 建议修复（质量提升）：I1-I8（共 8 项），尤其是 I2（FunctionCallingAgent 重构）、I3（AutoGen 0.5-0.7 演进未交代）
- 可选修复（细节打磨）：M1-M8（共 8 项）

**修复完成后预计质量**：90+ 分（满分 100）。当前评分约 75 分，扣分主要来自日期失真。

---

## 附录：验证数据汇总

| 框架 | PyPI 最新版 | 发布日期 | 4.12 时间线 | 一致性 |
|---|---|---|---|---|
| langchain | 1.3.9 | 2026-04+ | 1.0 GA = 2025-10-17 | ✓ 准确 |
| langchain-core | 1.4.7 | 2026-06-12 | (未提) | — |
| langgraph | 1.2.5 | 2026-06-12 | 0.1 = 2024-01 | ⚠ 实际 0.0.10 = 2024-01-09，但"状态机"定位是 v0.2 之后 |
| llama-index | 0.14.22 | 2026+ | Workflows 2025-02 | ✓ 准确 |
| autogen-agentchat | 0.7.5 | 2025-09-30 | v0.4 = 2024-08 | ✗ 偏差 5 个月 |
| crewai | 1.14.7 | 2026-05 | 1.0 GA = 2025-05 | ✗ 偏差 5 个月（1.0.0 = 2025-10-20） |
| openai-agents | 0.17.5 | 2026-06-11 | 2025-03 | ✓ 准确 |
| claude-agent-sdk | 0.2.104 | 2026-06-17 | 2025-09 | ⚠ 偏差 1 个月（v0.1.3 = 2025-10-11） |

| A2A 协议 | 首发版本日期 |
|---|---|
| v0.1.0 | **2025-06-09**（非 2025-04） |

| LangChain 历史 | 发布日期 |
|---|---|
| 0.0.1 | 2022-10-25（与"2022-10 LangChain 0.1 早期包"对应 ✓）|
| 0.1.0 | 2024-01-06 |
| 1.0.0a1 | 2025-08-27 |
| 1.0.0 | 2025-10-17 |

| LangGraph 历史 | 发布日期 |
|---|---|
| 0.0.10 | 2024-01-09（首个公开版本） |
| 0.1.1 | 2024-06-22 |
| 0.2.0 | 2024-08-07 |
| 1.2.5 | 2026-06-12 |