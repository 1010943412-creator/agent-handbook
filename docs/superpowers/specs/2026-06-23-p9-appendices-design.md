# P9 自测题库 + 4 附录 实施规格

> 笔名：晴暖
> 文档语言：中文（简体）
> 创建日期：2026-06-23
> 状态：v1.0 设计定稿
> 协议：CC BY-NC-SA 4.0
> 父级规格：`docs/superpowers/specs/2026-06-18-agent-dev-handbook-design.md`

---

## 0. 项目背景

P0-P8 已完成（项目骨架 + L1-L7 共 72 节 / ~9.5 万字 + L8 6 案例 / ~0.78 万字 = 累计 ~10.3 万字 + 93 图 + 78 S/A 引用）。P9 启动"**配套学习资源包**"——**4 附录 + 自测题库**，作为七层手册的**配套资源层**。

**P9 的核心价值**：从"**读完**"到"**会用、能考**"。读者拿到手册后，能通过附录快速查模板（附录 A/B/C/D）和刷题验证掌握度（题库 79 题），形成"学-查-练-考"的完整闭环。

**P8 → P9 衔接**：附录 A ReAct 模板对照 L1.4 ReAct 论文 + L5.1 ReAct 模式，附录 B Supervisor 对照 L5.7 + L8.5，附录 C 选型矩阵对照 L4.10，附录 D 术语表对照 L1-L8 全部关键词，题库覆盖 L1-L8 全部节。

---

## 1. P9 在手册中的定位

```
L1-L7 主体 72 节 + L8 案例 6 + ★P9 附录 4 + 题库 79 题★
                                ↑
                "配套资源 · 学-查-练-考 完整闭环"
```

| 维度 | L1-L7 主体 | L8 案例 | P9 附录 + 题库 |
|---|---|---|---|
| 视角 | "是什么 + 为什么" | "真业务怎么落地" | "速查 + 练习" |
| 抽象度 | 理论 + 模式 + 代码 | 业务 + 决策 + 实战 | 模板 + 题 + 术语 |
| 字数预算 | ~9.5 万（已交付） | ~0.78 万（已交付） | ~1.5 万 |
| 受众 | 全员 | 🟢🟡🔴 | 🟢 入门 + 🟡 进阶 |
| 交付形式 | 72 节 .md | 6 案例 .md | 4 附录 .md + 1 题库 .md |

---

## 2. 受众与门槛

| 圈层 | 受众 | 读完附录+题库能做 | 占比 |
|---|---|---|---|
| 🟢 入门圈 | 自学 Agent 的开发者 | 复制 ReAct 模板跑通，答对 60% 选择题 | ~40% |
| 🟡 进阶圈 | 准备面试/上线的工程师 | 借多 Agent 骨架改造项目，答对 80% | ~50% |
| 🔴 专家圈 | 架构师 / 技术布道者 | 用选型矩阵做内部决策 | ~10% |

**前置知识**：必读 L1-L8 全部（P0-P8 已交付）。

---

## 3. P9 详细大纲

### 3.1 附录 A：ReAct Agent 模板（Py 主 + TS 辅）

**目标**：给读者一份**可复制粘贴即可跑**的 ReAct Agent 完整模板，覆盖 Python（主力）+ TypeScript（辅助）。

**核心组件**：
- LLM 客户端封装（OpenAI / Anthropic）
- Tool 定义 + JSON Schema
- ReAct 循环（Thought → Action → Observation）
- 错误处理 + 超时
- 完整 prompt 模板

**Python 版 150 行**（主，~80% 字数）：
```python
# 完整 150 行 ReAct Agent
# - 支持多 tool 并行调用
# - 错误回灌 + 重试
# - 流式输出
```

**TypeScript 版 50 行**（辅，~20% 字数）：
```typescript
// 精简 50 行 ReAct Agent
// - 基于 Vercel AI SDK
// - 核心循环演示
```

**字数**：~3000 字（Py ~2400 + TS ~600）
**图**：1 张（ReAct 循环流程图）
**代码**：Py 150 行 + TS 50 行
**引用**：≥3 条 S/A 级

### 3.2 附录 B：多 Agent 协作骨架（LangGraph Supervisor）

**目标**：给读者一份**可扩展**的多 Agent 骨架，基于 LangGraph Supervisor 模式。

**核心组件**：
- Supervisor 节点（决策下一个 sub-agent）
- 2-3 个 sub-agent（researcher / writer / reviewer）
- 共享 State
- 条件边（conditional edges）
- Human-in-the-Loop 接入点

**代码骨架 80 行**：
```python
# StateGraph 定义
# Supervisor 调度 3 sub-agent
# 状态传递 + 条件路由
```

**字数**：~2500 字
**图**：1 张（多 Agent 架构图）
**代码**：LangGraph 80 行
**引用**：≥3 条 S/A 级

### 3.3 附录 C：AGENT 框架选型矩阵（纯表格快查）

**目标**：9 个框架（LangChain / LangGraph / LlamaIndex / AutoGen / CrewAI / OpenAI Agents SDK / Claude Agent SDK / Semantic Kernel / Haystack）的**集中对比速查表**。

**2 张表**：

**表 1：基础对比（9 框架 × 8 维度）**

| 框架 | 类型 | GitHub Stars | 维护状态 | 学习曲线 | 生产就绪 | 性能 | 文档质量 | 适用场景 |
|---|---|---|---|---|---|---|---|---|
| LangChain | 通用 | ... | ... | ... | ... | ... | ... | ... |
| ... |

**表 2：场景决策（4 场景 × 9 框架推荐）**

| 场景 | 推荐 | 备选 | 不推荐 | 理由 |
|---|---|---|---|---|
| 长任务执行 | LangGraph | Claude Agent SDK | AutoGen | ... |
| RAG 优先 | LlamaIndex | LangChain | Haystack | ... |
| 多 Agent 对话 | AutoGen | CrewAI | LangChain | ... |
| 快速原型 | OpenAI Agents SDK | LangChain | AutoGen | ... |

**字数**：~2000 字
**图**：0（纯表格）
**代码**：0
**引用**：≥3 条 S/A 级（框架 GitHub README）

### 3.4 附录 D：术语表（100 词条，纯术语）

**目标**：L1-L8 关键术语的中英对照速查，**纯术语**（不含缩写表/公式）。

**词条分类**：
- L1 基础理论（10 词条）：Transformer / KV Cache / Token / Prompt / CoT / Few-shot / ReAct / ReWOO / Reflection / Plan-and-Execute
- L2 上下文（12 词条）：RAG / Embedding / BM25 / Cross-Encoder / HyDE / Self-RAG / GraphRAG / MemGPT / Letta / LLMLingua / Prompt Cache / Semantic Cache
- L3 协议（12 词条）：Function Calling / Tool Use / JSON Schema / MCP / Resources / Prompts / Sampling / A2A / SSE / Streaming / Assistants API / Threads
- L4 框架（12 词条）：LangChain / LCEL / LangGraph / LlamaIndex / AutoGen / CrewAI / OpenAI Agents SDK / Claude Agent SDK / Semantic Kernel / Haystack / Runnable / AgentExecutor
- L5 模式（12 词条）：ReAct / Reflection / Plan-and-Execute / Tool Use / Routing / Parallelization / Orchestrator-Workers / Evaluator-Optimizer / Memory / Human-in-the-Loop / Multi-Agent / Supervisor
- L6 可观测（10 词条）：Tracing / Span / Trace / OpenTelemetry / Langfuse / LangSmith / Phoenix / LLM-as-Judge / SWE-bench / GAIA
- L7 生产安全（12 词条）：Guardrails / Prompt Injection / RBAC / E2B / Firecracker / Circuit Breaker / SLO / SLI / GDPR / 数据脱敏 / 混沌工程 / 凭据隔离
- L8 案例（10 词条）：RRF / CodeAct / EXPLAIN / sqlparse / Playwright / RAG 引用溯源 / 工单系统 / 多 Agent Supervisor / 升级人工 / 工单降级
- 其他（10 词条）：LLM / Agent / Prompt Engineering / Fine-tuning / RLHF / Embedding Model / Token 压缩 / 多模态 / Function Calling / Vector Database

**词条格式**（每条 ~30 字）：
```
**中文名** (English Name) —— 一句话定义
```

**字数**：~3000 字（100 × 30）
**图**：0
**代码**：0
**引用**：0

### 3.5 自测题库（L1-L8 共 79 题）

**目标**：让读者通过答题验证 L1-L8 关键概念掌握度。

**题型**：
- 选择题（64 题，4 选项单选）
- 判断题（15 题，对/错）
- 答案解析（每题 1-2 句）

**题量分布**（对齐各章节数）：
| 层 | 节数 | 选择 | 判断 | 小计 |
|---|---|---|---|---|
| L1 基础理论 | 8 | 6 | 2 | 8 |
| L2 上下文 | 10 | 8 | 2 | 10 |
| L3 协议 | 10 | 8 | 2 | 10 |
| L4 框架 | 12 | 10 | 2 | 12 |
| L5 模式 | 12 | 10 | 2 | 12 |
| L6 可观测 | 10 | 8 | 2 | 10 |
| L7 生产安全 | 11 | 9 | 2 | 11 |
| L8 案例 | 6 | 5 | 1 | 6 |
| **合计** | **79** | **64** | **15** | **79** |

**题目样例**（选择）：
```markdown
### L1.4-001 (选择)
**题目**：ReAct 论文中, "ReAct" 的两个字母分别代表什么?
**选项**：
- A. Reasoning + Action
- B. Reading + Acting
- C. Retrieval + Action
- D. Reasoning + Activation
**答案**：A
**解析**：ReAct = Reasoning + Acting, 通过推理与行动的循环让 LLM 与外部环境交互。
```

**题目样例**（判断）：
```markdown
### L1.1-002 (判断)
**题目**：Transformer 推理时, KV Cache 主要用于加速 prefill 阶段, 对 decode 阶段影响不大。
**选项**：
- 对
- 错
**答案**：错
**解析**：KV Cache 主要加速 decode 阶段（避免每步重新计算历史 token 的 K/V），对 prefill 阶段影响较小。
```

**字数**：~4500 字（79 题 × ~57 字/题）
**图**：0
**代码**：0
**引用**：0（每题自带解析）

---

## 4. 5 个文件统一结构

每个 .md 文件结构：

```markdown
# [附录/题库名]

> **目标**:[一句话]
> **受众**:[圈层]
> **前置知识**:[必读章节]

[主体内容]

> 📚 本附录参考 (附录 A/B/C 需要,题库和 D 不需要)
> - [<引用名>](<URL>) — <理由>
```

---

## 5. 字数与代码预算

| 交付物 | 字数 | 代码 | 图 | 引用 | 节数 |
|---|---|---|---|---|---|
| 附录 A | ~3000 | Py 150 + TS 50 | 1 | ≥3 | 1 .md |
| 附录 B | ~2500 | 80 行 | 1 | ≥3 | 1 .md |
| 附录 C | ~2000 | 0 | 0 | ≥3 | 1 .md |
| 附录 D | ~3000 | 0 | 0 | 0 | 1 .md |
| 题库 | ~4500 | 0 | 0 | 0 | 1 .md |
| **合计** | **~1.5 万** | **280 行** | **2** | **≥9** | **5 .md** |

---

## 6. 干货来源与引用规范

附录 A/B/C 共需 ≥9 条 S/A 级引用：

**附录 A（≥3 条）**：
- `github.com/langchain-ai/langchain` —— ReAct Agent 实现参考
- ArXiv "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al. 2022)
- `github.com/vercel/ai` —— Vercel AI SDK（TS 版参考）

**附录 B（≥3 条）**：
- `github.com/langchain-ai/langgraph` —— Multi-Agent Supervisor 示例
- ArXiv "Multi-Agent Collaboration Mechanisms" (Han et al. 2024)
- `lilianweng.github.io/posts/2023-12-23-multi-agent-llm/` —— Lilian Weng Multi-Agent

**附录 C（≥3 条）**：
- 9 个框架的 GitHub README（langchain / langgraph / llama-index / autogen / crewAI / openai-agents-python / claude-agent-sdk 等）
- 表格数据**只引用真实开源数据**（不编造 stars / 维护状态），必要时标 "TBD"

⚠️ **不要**引用 `shopify.com` / `xiaohongshu.com` / `aws.amazon.com` 等非白名单。

---

## 7. 验收标准

| 维度 | 门槛 | 校验方法 |
|---|---|---|
| 字数 | 附录 A-D 各 1500-3500；题库 4000-5000 | `scripts/check_word_count.py`（节模式 800-1500 阈值需扩展或附录走 case 模式 1200-2500） |
| 代码 | 附录 A Py 150 + TS 50 行；附录 B 80 行 | 人工核查 + `ast.parse` |
| 引用 | 附录 A/B/C 各 ≥3 条 S/A 级 | `scripts/check_references.py` |
| 图 | 附录 A 1 张 + 附录 B 1 张 | `scripts/check_figures.py` |
| 题量 | 题库 79 题（64 选 + 15 判） | 人工核查 |
| 题库完整 | 每题必有答案 + 解析 | 人工核查 |

**验证脚本适配**：
- 附录字数 1500-3500 高于节模式 800-1500，可复用 case 模式 1200-2500 阈值（但附录超过 2500 需调整）
- 方案：扩展 `check_case_word_count.py` 上限为 3500（仅用于附录），题库独立走 `check_appendix_word_count.py`

**完整验收**：
```bash
# 5 个附录 .md 一起验证
bash scripts/run_all_checks.sh handbook/appendices/

# L1-L8 回归
bash scripts/run_all_checks.sh handbook/l1-theory/
... (其他层)
```

---

## 8. 实施策略（已与用户确认）

**女王大人已确认 P9 实施策略**：
- **方案 C：单 worktree + 题库子并行**
- **题库题型**：选择 + 判断 + 答案解析（不要简答/实操）
- **附录范围**：A Py+TS / B LangGraph / C 纯表格 / D 纯术语

**5 步串行**：
1. 附录 A（Py 主 + TS 辅，单 main agent，因为双版本需一致性）
2. 附录 B（LangGraph Supervisor，单 main agent）
3. 附录 C（选型矩阵，单 main agent）
4. 附录 D（术语表，单 main agent）
5. 自测题库（3 subagent 并行：L1-L3 / L4-L5 / L6-L8）

**Worktree 路径**：
```
C:\Users\caozh\Documents\LangChain\agent-handbook-p9\
```

**流程细节**：
1. 创建 worktree `p9-batch`（单分支）
2. 步骤 1-4 串行 commit（4 个附录各 1 commit）
3. 步骤 5 题库 3 subagent 并行（3 个 commits，可独立分支后 squash merge）
4. 整体跑 `run_all_checks.sh handbook/appendices/` 验证
5. merge worktree 回 master
6. commit 验收报告

**每文件 commit 信息模板**：
```
feat(appendix): 附录名(副标题)

- 主要内容要点 1
- 主要内容要点 2
- 代码: <行数> 行

字数: XXXX 字 | 代码: X 行 | 引用: X 条
```

---

## 9. 风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| **题库题目编造** | 79 题无 L1-L8 真实概念支撑 | 严格基于已交付内容，每题引用节号（如 L1.4-001） |
| **Py/TS 双版本不一致** | 附录 A 两个版本对不上 | Step 1 单 agent 一次完成，强制对照 |
| **术语表覆盖不足** | 100 词条漏关键术语 | 词条清单前置（spec §3.4），逐条 commit |
| **题库跨节一致性** | 3 subagent 风格不统一 | 用同一 prompt 模板，主审统一校验格式 |
| **选型矩阵数据编造** | 9 框架 stars/维护状态造假 | 表格数据标 "TBD" 占位或 curl 验证，**绝不编造数字** |
| **脚本不兼容** | 附录字数超过 2500 | 扩展 `check_case_word_count.py` 上限为 3500 |
| **worktree 合并冲突** | 3 题库 subagent 并行 in-place edit | 3 subagent 各写独立 .md（L1L2L3-quiz.md / L4L5-quiz.md / L6L7L8-quiz.md），先并行后合并 |

---

## 10. 与全局规格的一致性

本规格完全对齐 `docs/superpowers/specs/2026-06-18-agent-dev-handbook-design.md` 第 165-172 行"4 附录 + 题库"主题定义，并在以下 4 处做了**显式微调**：

1. **附录 A 微调**：原"200 行 ReAct 模板（Py/TS 双版本）"→ 现"Py 主 150 行 + TS 辅 50 行"（重点 Python）
2. **附录 B 微调**：原"LangGraph / CrewAI 二选一"→ 现"LangGraph 单选"（与 L8.5 实战一致）
3. **附录 C 微调**：原"框架选型决策矩阵"→ 现"纯表格快查，不含决策树"（避免与 4.10 重复）
4. **附录 D 微调**：原"术语表（中英对照 + 缩写）"→ 现"纯术语 100 词条，不含缩写"（避免与正文重复）

字数与文件数预算在全局预算内（P9 占手册总字数 ~10%）。

---

## 11. 下一步

1. ✅ 已完成：规格文档（本文档）
2. ⏳ 下一步：调用 `writing-plans` skill 写实施计划 `docs/superpowers/plans/2026-06-23-p9-appendices.md`
3. ⏳ 实施：按"单 worktree + 4 附录串行 + 题库 3 subagent 并行"策略启动 P9 写作

---

**本规格经 brainstorming skill 流程产出，请用户审查后再进入 writing-plans 阶段。**