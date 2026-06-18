# L4 · 框架与运行时层

> 12 节正文 | 12+ 张原创图 | 50+ 条 S/A 级引用 | 30+ 道自测题
> 作者：晴暖 | 协议：CC BY-NC-SA 4.0

## L4 总览

L4 是从 L3"协议"到 L5"模式"之间的**工程落地层**——这一层不写"Agent 怎么思考"（那是 L1）、也不写"Agent 怎么说话"（那是 L3），而是写"**用什么具体框架把协议落地为可运行系统**"。L1 解决了"LLM 是什么"，L2 解决了"怎么喂 LLM"，L3 解决"Agent 之间怎么说话"，**L4 解决"Agent 应用怎么工程化"**。

这 12 节是一条**框架横评 + 协议落地 + 选型决策**的三线：4.1 用一张对比矩阵把 7 个 2025 年主流 Agent 框架放进统一坐标系；4.2-4.4 讲 LangChain / LangGraph / LlamaIndex 三大**通用 / 数据 / 状态机路线**框架；4.5-4.6 讲 AutoGen / CrewAI 两种**多 Agent 协作范式**；4.7-4.8 讲 OpenAI Agents SDK / Claude Agent SDK 两个**官方 SDK**；4.9 讲跨框架**协议适配器**（MCP / A2A 适配）；4.10-4.11 讲**选型决策**与**自研权衡**；4.12 用一张 2022-2025 Gantt 图**收尾**——把 7 框架放进时间轴，看清"协议演进是层叠、框架演进是分化"的反直觉规律。

读完 L4，你应该能：
1. 说出 LangChain / LangGraph / LlamaIndex / AutoGen / CrewAI / OpenAI Agents SDK / Claude Agent SDK 七个框架的**正交定位**（不是"哪个最好"，而是"哪个匹配你的不匹配"）；
2. 用 LCEL（LangChain Expression Language）写出一个 `prompt | llm | parser` 管道，理解 `Runnable` 接口的协议级意义；
3. 用 LangGraph 的 `StateGraph` + `TypedDict` + `InMemorySaver` 写出一个带持久化和 HITL 的状态机；
4. 区分 LlamaIndex 的"RAG 优先 + Workflows 事件流"路线与 LangGraph 的"通用状态机 + reducer"路线；
5. 理解 AutoGen 的"对话即协作"和 CrewAI 的"角色即协作"两种多 Agent 范式差异，以及 AutoGen 进入维护模式的含义；
6. 用 OpenAI Agents SDK 的 `Agent` + `Runner` 写出一个**轻量多 Agent**，理解它"官方参考实现"的定位；
7. 用 Claude Agent SDK 的 `query()` 异步生成器跑一个**长任务 Coding Agent**，理解它与 Claude Code CLI 的关系；
8. 设计一个**协议适配层**（MCP Server + Function Calling JSON Schema + A2A Agent Card），把跨框架迁移成本降到"改配置"；
9. 用加权决策矩阵（4.10）给自己的项目做**可量化选型**，避免"主观感觉"；
10. 判断项目该用**框架**还是**自研**（4.11 的 80/20 结论：80% 时间花在 prompt/可观测性/工具适配，框架只解决 20% 通用工程问题）；
11. 画出 2022-2025 的 Agent 框架演进时间线，理解"3 年走过 Web 框架 10 年的路"的反直觉规律。

## 12 节导览

| 节 | 标题 | 一句话钩子 | 难度 |
|---|---|---|---|
| 4.1 | [框架全景：7 大 Agent 框架的横向对比](./4.1-framework-landscape.md) | 选框架不是"哪个最好"而是"哪个匹配你的不匹配"——7 个框架覆盖 7 个**正交维度**，**没有任何框架能覆盖所有维度** | 🟢 |
| 4.2 | [LangChain 1.x：Runnable 与 LCEL](./4.2-langchain-runnable-lcel.md) | LCEL 的 `prompt \| llm \| parser` 不是语法糖，是**协议级抽象**——所有节点统一 `Runnable` 接口，框架才能做并行/缓存/持久化的统一调度 | 🟢 |
| 4.3 | [LangGraph：状态机 + 持久化 + Human-in-the-Loop](./4.3-langgraph-state-persistence-hitl.md) | LangGraph 的杀手锏不是"画流程图"，是**持久化 + 可恢复执行**（durable execution）——跑两小时的 agent 崩了从断点精确恢复 | 🟡 |
| 4.4 | [LlamaIndex：RAG 优先的范式](./4.4-llamaindex-rag-paradigm.md) | LlamaIndex 不是 LangChain 的 RAG 模块——2025 年 **Workflows** 事件驱动框架与 LangGraph 殊途同归，但 API 完全不同 | 🟢 |
| 4.5 | [AutoGen：对话式多 Agent（已进入维护模式）](./4.5-autogen-conversational-multiagent.md) | AutoGen 是"对话即协作"的开创者，但 **2025 起 README 标注 Maintenance Mode**——新项目推荐 Microsoft Agent Framework | 🟡 |
| 4.6 | [CrewAI：角色化协作](./4.6-crewai-role-based.md) | CrewAI 是"角色即协作"——给 Agent 起人设（role/goal/backstory），**完全独立于 LangChain 生态**既是优势也是隔离代价 | 🟡 |
| 4.7 | [OpenAI Agents SDK：轻量官方参考实现](./4.7-openai-agents-sdk.md) | OpenAI Agents SDK 不是 LangChain 的"竞品"，而是**官方参考实现**——最小 API（Agent + Runner + tools + handoffs + guardrails）覆盖 80% 场景 | 🟢 |
| 4.8 | [Claude Agent SDK：长任务与工具深度集成](./4.8-claude-agent-sdk.md) | Claude Agent SDK 源自 **Claude Code 内部 SDK**，自动捆绑 CLI，原生长任务（小时级）+ Sub-agents + 内置 Read/Write/Edit/Bash | 🟡 |
| 4.9 | [Agent 协议适配器：跨框架的中间层](./4.9-protocol-adapter.md) | 同时用 4 个框架时最大的痛是"工具定义 4 套写法"——把它们统一到 **MCP / Function Calling JSON Schema / A2A Agent Card**，跨框架迁移从"重写"降到"改配置" | 🟡 |
| 4.10 | [框架选型决策矩阵](./4.10-framework-decision-matrix.md) | 决策矩阵最常用的 3 个维度（stars、文档量、性能）**都不是最重要的**——真正决定项目成败的是团队熟悉度 + 工具生态兼容 + 长期维护状态 | 🟡 |
| 4.11 | [自研 vs 用框架：何时值得自己写](./4.11-build-vs-framework.md) | 生产 Agent **80% 时间花在自研**（prompt/可观测性/工具适配），框架只解决 20% 通用工程问题——这是 L4 最反共识的一节 | 🟡 |
| 4.12 | [Agent 框架演进时间线（2022-2025）](./4.12-framework-timeline.md) | **3 年走过 Web 框架 10 年的路**——协议是层叠、框架是分化，**6+ 框架共存**是常态；2025 是"官方化元年" | 🟢 |

## 学习路径建议

**首次通读（4-5 小时）**：按 4.1 → 4.12 顺序读。4.1 是总览必读，4.2-4.4 是 LangChain 主线（覆盖 60% 生产场景），4.5-4.6 是多 Agent 范式，4.7-4.8 是官方 SDK，4.9 是协议适配器，4.10-4.12 是选型收尾。

**框架横评优先（1-2 小时）**：专注 4.1 + 4.10 + 4.12——3 节覆盖"7 框架对比矩阵 + 选型决策矩阵 + 时间线"，是快速建立全局视角的最小路径。

**LangChain 主线（2-3 小时）**：4.2 → 4.3 → 4.4 顺序读——4.2 讲 LCEL 管道（链式组合），4.3 讲 LangGraph 状态机（持久化 + HITL），4.4 讲 LlamaIndex RAG 优先路线。**这三节覆盖 60% 的 Agent 工程场景**。

**多 Agent 框架（1-2 小时）**：4.5 → 4.6 → 4.8 顺序读——4.5 讲 AutoGen 对话驱动（理解历史范式 + 评估迁移），4.6 讲 CrewAI 角色驱动（学习角色化抽象），4.8 讲 Claude Agent SDK 长任务（理解官方 SDK 与 CLI 的关系）。**跳过 4.7 也行**——OpenAI Agents SDK API 极简，扫一眼 README 即可上手。

**选型视角（30 分钟）**：4.10 → 4.11 → 4.12 配套读——4.10 给加权决策表，4.11 给"自研 vs 框架"的 80/20 反直觉结论，4.12 给历史答案（为什么会有这些框架）。

**协议适配器实战（30 分钟）**：单独读 4.9——当你同时用多个框架时，**这一节能省下 80% 重复造轮子的时间**。

**自测驱动（2 小时）**：每节 3-5 题自测，覆盖概念辨析 / 场景判断 / 代码补全 / 反直觉思考。建议读完每节立刻做题，错题回去看正文相应段落。

## 与 L3 / L5 的衔接

- **L3 → L4**：L3 的协议定义"Agent 怎么说话"，L4 给出"用 LangChain / LangGraph / LlamaIndex / AutoGen / CrewAI 等框架怎么落地"。**典型落地路径**：
  - 3.1 Function Calling → LangChain `bind_tools()` → 4.1 / 4.2 Runnable；
  - 3.3 MCP Resources / Tools → 4.9 协议适配器（MCP Server 接入各种框架）；
  - 3.5 A2A Agent Card → 4.9 A2A 适配层（多框架互操作）；
  - 3.7 Anthropic Prompt Caching → 4.2 LangChain `cache=` + 4.3 LangGraph `InMemorySaver`；
  - 3.8 Streaming SSE → 4.3 LangGraph `graph.stream(stream_mode=...)` 原生支持。
- **L4 → L5**：L4 给"**用什么框架**"，L5 给"**在框架上用什么模式**"——ReAct / Reflection / Plan-Execute / Multi-Agent Collaboration / RAG Fusion 等设计模式。**典型路径**：4.3 LangGraph 状态机 → 5.x 设计模式（如 ReAct Agent、Reflection 循环、Plan-and-Execute 分解）。

## 下一步

- **L5 · 设计模式层（12 节）**：在 L4 框架之上抽象常见 Agent 设计模式（Reflection / Planning / Multi-Agent / RAG Fusion / Self-Consistency 等），让"用框架"升级为"用模式"。
- **L6 · 可观测与评估层（10 节）**：L4 框架跑起来后，**怎么监控 / 调试 / 评估**——Tracing / Logging / Eval / A/B Test / Cost Optimization。
- **L7 · 生产化与安全层（10 节）**：L4-L6 都在"能跑"，L7 给"能稳跑"——部署、灰度、限流、密钥、审计、Prompt Injection 防护、合规。
- **L8 · 案例层（6 个真实案例）**：把 L1-L7 的全部知识串成 6 个端到端项目——RAG 知识库 / Coding Agent / DB Agent / Browser Agent / 小红书运营 / 电商客服。
- **附录 D · 术语表**：中英对照 + 缩写速查（Runnable / LCEL / StateGraph / HITL / Worker / ReAct / A2A / MCP 等）。