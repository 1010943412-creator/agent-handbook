# 自测题库 L4-L5（24 题）

> **目标**:验证 L4 框架 / L5 模式 的关键概念掌握度
> **受众**:🟡 进阶 + 🔴 专家
> **前置知识**:L4-L5 全部

---

## 使用说明

- **题型**:选择(20) + 判断(4) = 24 题
- **建议**:每节先看正文,再做对应题目
- **评分**:答对 60% 算"基本掌握",80% 算"熟练"

---

## L4 框架(12 题)

### L4.1-1 (选择)
**题目**:L4.1 把 2025 年主流 Agent 框架划分为 4 个集群,最准确的一组是?
**选项**:
- A. 通用工具链 / 数据检索 / 对话驱动 / 厂商官方
- B. 单 Agent / 多 Agent / 长任务 / 通用工具
- C. 开源 / 闭源 / 商业 / 实验
- D. 轻量 / 中量 / 重型 / 企业级
**答案**:A
**解析**:4.1 按通用工具链型(LangChain/LangGraph)+ 数据检索中心型(LlamaIndex)+ 对话驱动多 Agent(AutoGen/CrewAI)+ 官方轻量 SDK(OpenAI/Claude)四类划分。

### L4.2-2 (选择)
**题目**:LangChain 1.x 的 Runnable 与 LCEL,下列说法正确的是?
**选项**:
- A. LCEL 的 `|` 只是语法糖,和 Python 函数组合等价
- B. `Runnable` 统一接口 invoke/stream/batch,`|` 操作符返回 RunnableSequence
- C. LangChain 1.x 移除了所有异步接口
- D. `LLMChain` 是 1.x 推荐主类
**答案**:B
**解析**:4.2 强调 `|` 调用 `Runnable.__or__` 返回 `RunnableSequence`,自动获得 streaming/async/batch/retry/tracing;是协议级抽象而非语法糖。

### L4.3-3 (选择)
**题目**:LangGraph 的核心差异化能力,描述最准确的是?
**选项**:
- A. 提供比 LangChain 更简单的 Chain API
- B. 基于 Pregel 启发的图计算引擎,支持持久化与可恢复执行
- C. 主要靠 callback 函数实现 HITL
- D. 不能与 LangChain 组件混用
**答案**:B
**解析**:4.3 定位 LangGraph 为 Pregel 启发的图计算引擎,杀手锏是持久化 + 可恢复执行(durable execution),而非画流程图。

### L4.4-4 (判断)
**题目**:LlamaIndex 等同于 LangChain 的 RAG 模块,二者可无缝互换。
**选项**:
- 对
- 错
**答案**:错
**解析**:4.4 明确这是误区。LlamaIndex 有独立 Agent 抽象(4.4);Workflows 走事件而非状态 dict,API 与 LangGraph 不同。

### L4.5-5 (选择)
**题目**:关于 AutoGen 4.5 的现状,下列说法最准确的是?
**选项**:
- A. AutoGen 已停止维护,仓库不再更新
- B. AutoGen 进入维护模式,官方推荐新项目用 Microsoft Agent Framework
- C. AutoGen v0.4 是全新框架,与历史无关
- D. AutoGen 只能在 Azure 上运行
**答案**:B
**解析**:4.5 指出 AutoGen README 自 2025-Q3 起标注 Maintenance Mode,官方推荐新项目用 MAF;v0.4 是 actor-model 重构,API 不兼容 v0.2 但概念延续。

### L4.6-6 (选择)
**题目**:CrewAI 的核心抽象与执行模式,组合正确的是?
**选项**:
- A. Agent + Task + Crew;执行模式 sequential / hierarchical
- B. StateGraph + Node + Edge;执行模式 sync / async
- C. Runnable + Pipe + Parser;执行模式 stream / batch
- D. AssistantAgent + GroupChat;执行模式 initiate / reply
**答案**:A
**解析**:4.6 明确 CrewAI 三件套 Agent(role/goal/backstory) + Task + Crew;process 取 Process.sequential 或 Process.hierarchical。

### L4.7-7 (选择)
**题目**:OpenAI Agents SDK 的核心三件套不包括下列哪一项?
**选项**:
- A. tools
- B. handoffs
- C. guardrails
- D. checkpoints
**答案**:D
**解析**:4.7 明确核心三件套是 tools、handoffs(整段对话上下文交接)、guardrails;checkpoints 是 LangGraph 概念,不属于 Agents SDK。

### L4.8-8 (选择)
**题目**:Claude Agent SDK 与 Anthropic Python API 的关系,下列说法最准确的是?
**选项**:
- A. 两者完全等价,只是命名不同
- B. Claude Agent SDK 是应用层 SDK,自带 Claude Code CLI、工具集、子 Agent 框架
- C. Claude Agent SDK 只能通过 Web 界面调用
- D. Anthropic Python API 包含完整工具集
**答案**:B
**解析**:4.8 明确 Anthropic Python API 是薄协议封装;Claude Agent SDK 是应用层 SDK,自带 Claude Code CLI 与工具集,定位长任务。

### L4.9-9 (选择)
**题目**:关于跨框架协议适配器(4.9),下列说法最准确的是?
**选项**:
- A. 每个框架必须重写一遍工具定义,无法统一
- B. 通过 UnifiedTool + 适配器层把内部工具统一转换为 MCP/Function Calling/A2A
- C. 适配器层会让运行时性能显著下降
- D. 只有 Anthropic 支持 MCP
**答案**:B
**解析**:4.9 提出 UnifiedTool + 4 个适配器,把跨框架迁移成本从重写工具降到改配置;适配只发生在初始化阶段,运行时无性能损耗。

### L4.10-10 (选择)
**题目**:4.10 框架选型决策矩阵最关键的 3 个维度是?
**选项**:
- A. stars 数 / 文档量 / 性能基准
- B. 团队熟悉度 + 工具生态兼容 + 长期维护状态
- C. 编程语言 / 协议 / 是否开源
- D. 发布年份 / 公司背景 / 贡献者数量
**答案**:B
**解析**:4.10 明确 stars/文档量/性能都不是最重要的;真正决定成败的是团队熟悉度 + 工具生态兼容 + 长期维护状态。

### L4.11-11 (判断)
**题目**:4.11 主张换框架能解决生产环境 80% 的业务问题,所以项目遇到性能瓶颈时应优先更换框架。
**选项**:
- 对
- 错
**答案**:错
**解析**:4.11 明确这是误区。生产 Agent 80% 时间花在自研 prompt/可观测性/工具适配,框架只解决 20%;性能瓶颈通常在 prompt/retrieval/cache。

### L4.12-12 (选择)
**题目**:4.12 框架演进时间线中,抽象跃迁对应正确的是?
**选项**:
- A. 2022-10:Agent → Chain 范式跃迁
- B. 2023-01:Chain → Agent;2024-06:Agent → 状态机
- C. 2025-03:状态机 → 流程图跃迁
- D. 2026-01:所有第三方框架被官方 SDK 替代
**答案**:B
**解析**:4.12 给出三个跃迁:2023-01 Chain → Agent(ReAct 落地)、2024-06 Agent → 状态机(LangGraph 0.1.1)、2025-03 第三方 → 官方 SDK。

---

## L5 模式(12 题)

### L5.1-1 (选择)
**题目**:ReAct 模式(5.1)的 Thought-Action-Observation 循环,描述最准确的是?
**选项**:
- A. LLM 先思考一次,再连续执行所有工具
- B. 每步都包含思考 + 工具调用 + 结果回灌三段,每步都可能修正上一步的计划
- C. 工具越多越好,超过 50 个仍可保持高准确率
- D. ReAct 适合步骤数 > 20 的超长任务
**答案**:B
**解析**:5.1 定义每 cycle 包含 Thought + Action + Observation 三步,每步都可能修正上一步的计划;超过 20 个工具选工具准确率显著下降。

### L5.2-2 (选择)
**题目**:关于 Reflection 模式(5.2)的关键机制,下列说法正确的是?
**选项**:
- A. 再问一次同样的问题就能显著提质量
- B. 评审 prompt 必须结构化,迭代 4+ 次质量持续提升
- C. 结构化批评可将质量从 60% 提到 85%;Self-Refine 显示 2-3 次后边际收益骤降
- D. Reflection 适合所有任务包括实时聊天和客观题
**答案**:C
**解析**:5.2 明确结构化批评能让质量从 60 分提到 85+ 分;2-3 次后边际收益骤降,4+ 次成本超过质量提升。

### L5.3-3 (判断)
**题目**:Plan-and-Execute 模式是 ReAct 的优化版,任何场景下都优先选择 Plan-and-Execute。
**选项**:
- 对
- 错
**答案**:错
**解析**:5.3 明确定义 Plan-and-Execute 是 ReAct 的互补模式而非进化版;浏览器交互等边走边调场景应改用 ReAct。

### L5.4-4 (选择)
**题目**:关于 Tool Use 模式(5.4)的协议分层,下列说法最准确的是?
**选项**:
- A. LLM 直接调用外部 API 完成工具执行
- B. LLM 只生成结构化 JSON 工具调用指令,运行时负责实际执行 + 错误处理 + 重试
- C. Tool Use 等同于 Function Calling,二者完全等价
- D. 工具描述写得简单不会影响选工具准确率
**答案**:B
**解析**:5.4 强调 Tool Use 是协议层:LLM 输出 tool_call JSON,Runtime 解析执行回灌;Anthropic 基准好 description 可让准确率从 70% 提到 95%。

### L5.5-5 (选择)
**题目**:Routing(5.5)与 Orchestrator-Workers(5.7)的根本区别是?
**选项**:
- A. Routing 用 if-else 硬编码,Orchestrator-Workers 用 LLM 决策
- B. Routing 的子任务结构已知(订单/账单),Orchestrator-Workers 的子任务动态生成
- C. Routing 只能串行执行,Orchestrator-Workers 只能并行
- D. 二者本质完全相同
**答案**:B
**解析**:5.5 明确 Routing 子 Agent 列表静态已知;5.7 Orchestrator-Workers 子任务动态生成。Routing ≠ if-else 硬编码,Supervisor 由 LLM 决策。

### L5.6-6 (选择)
**题目**:关于 Parallelization 模式(5.6)的两种风格,下列说法正确的是?
**选项**:
- A. Sectioning 切分并行再合并;Voting 多次执行后投票,5 次投票可提准确率 10-15%
- B. 并行 N 个 Agent 速度一定提升 N 倍
- C. 并行越多越好,10+ 次投票仍持续提升
- D. Sectioning 和 Voting 本质相同
**答案**:A
**解析**:5.6 给出两种风格:Sectioning(切分并行)和 Voting(Self-Consistency 5 次投票可提准确率 10-15%);主要价值是质量与覆盖而非速度。

### L5.7-7 (判断)
**题目**:Orchestrator-Workers 模式(5.7)就是主从架构——Orchestrator 发命令,Workers 必须无条件执行。
**选项**:
- 对
- 错
**答案**:错
**解析**:5.7 明确定义 Orchestrator-Workers 不等于主从架构。Workers 有自主权可拒绝/反问/委派回;本质是任务描述而非命令。

### L5.8-8 (选择)
**题目**:Evaluator-Optimizer(5.8)与 Reflection(5.2)的核心差异是?
**选项**:
- A. Reflection 用外部裁判,Evaluator-Optimizer 用自我批评
- B. Reflection 是同 LLM 自我批评,Evaluator-Optimizer 是独立 Agent 外部评估,可基于规则或 LLM-as-Judge
- C. 阈值 9/10 是经验最佳值
- D. 二者本质完全相同
**答案**:B
**解析**:5.8 明确 Reflection 是同 LLM 自我批评,Evaluator-Optimizer 引入外部视角打破自我一致性;Evaluator 含规则、LLM-as-Judge、混合三种类型。

### L5.9-9 (选择)
**题目**:Memory 模式(5.9)的三层架构,划分正确的是?
**选项**:
- A. 缓存 / 索引 / 日志
- B. 短期(当前 Context)/ 长期(外部存储)/ 共享(多 Agent 分布式状态)
- C. 临时 / 永久 / 备份
- D. 输入 / 输出 / 中间
**答案**:B
**解析**:5.9 给出三层:短期 = 当前 Context;长期 = 外部存储按需召回;共享 = 多 Agent 协作的分布式状态(Redis / LangGraph Checkpointer)。

### L5.10-10 (选择)
**题目**:HITL 模式(5.10)的三段式设计包括?
**选项**:
- A. 何时打断 + 打断粒度 + 恢复上下文
- B. 何时启动 + 何时暂停 + 何时停止
- C. 输入校验 + 处理逻辑 + 输出校验
- D. 计划 + 执行 + 反馈
**答案**:A
**解析**:5.10 明确 HITL 三段式:何时打断(按工具名/参数值/步骤数)、打断粒度(计划/单工具/最终结果)、恢复上下文。

### L5.11-11 (选择)
**题目**:5.11 多 Agent 复杂度税中,错误放大的数学原理是?
**选项**:
- A. 多个 Agent 的错误会相互抵消
- B. 单 Agent 错误率 5%,3 Agent 串联后整体错误率升到 1-0.95³≈14.3%
- C. 多 Agent 错误率与单 Agent 完全相同
- D. 错误率随 Agent 数指数下降
**答案**:B
**解析**:5.11 明确错误放大公式:单 Agent 错误 5%,3 Agent 串联后 1-0.95³≈14.3%;多 Agent 在多数任务上比单 Agent 慢 2-5 倍。

### L5.12-12 (选择)
**题目**:5.12 主张的模式叠加演化路径中,阶段 4(生产级)包含哪些模式叠加?
**选项**:
- A. 仅 ReAct 单 Agent
- B. ReAct + Reflection
- C. Routing + 多 Agent
- D. Orchestrator-Workers + HITL + Memory
**答案**:D
**解析**:5.12 明确 4 阶段演化:阶段 1 ReAct → 阶段 2 Plan-and-Execute + Reflection → 阶段 3 Routing + 多 Agent → 阶段 4 Orchestrator-Workers + HITL + Memory。

---

## 📚 题源与参考

> - [LangChain 官方文档 - LangGraph](https://langchain.com/langgraph) (langchain.com)
> - [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) (anthropic.com)
> - [OpenAI - Function Calling Documentation](https://platform.openai.com/docs/guides/function-calling) (platform.openai.com)
> - [Lilian Weng - LLM-powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) (lilianweng.github.io)
> - [LangChain - LangGraph GitHub](https://github.com/langchain-ai/langgraph) (github.com)
> - [OpenAI Agents SDK Repository](https://github.com/openai/openai-agents-python) (github.com)