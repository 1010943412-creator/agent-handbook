# L3 · 协议与接口层

> 10 节正文 | 10+ 张原创图 | 42+ 条 S/A 级引用 | 30+ 道自测题
> 作者：晴暖 | 协议：CC BY-NC-SA 4.0

## L3 总览

L3 是从 L2"上下文工程"到 L4"框架与运行时"的**协议桥梁**——这一层不写 LLM 推理机制，也不写上下文管理，而是写"Agent 之间、Agent 与工具之间、Agent 与外部系统之间"的**标准通信协议**。L1 解决了"LLM 是什么"，L2 解决了"怎么喂 LLM"，L3 解决"LLM 应用之间怎么说话"。

这 10 节是一条**协议演进 + 实战落地**的双线：3.1-3.2 讲 Function Calling 与 JSON Schema（**协议基础**），3.3-3.5 讲 MCP / A2A（**新一代开放协议**），3.6-3.7 讲 OpenAI Assistants 与 Anthropic Prompt Caching（**厂商协议级能力**），3.8-3.9 讲 Streaming 与协议演进时间线（**协议工程实践 + 趋势**），3.10 收尾——协议选型决策树，把 L3 全部协议收敛到"按需组合"的方法论。

读完 L3，你应该能：
1. 解释清楚 OpenAI Function Calling 与 Anthropic Tool Use 的协议级差异（schema 字段名、响应结构、错误处理）；
2. 写出符合 JSON Schema 严格规范的 Pydantic 工具描述，避免 80% 的工具调用失败；
3. 部署一个 MCP server 接入 Cursor / Claude Desktop，理解 stdio vs HTTP+SSE 的传输层选型；
4. 理解 A2A 协议的 Agent Card + Task 设计，能在多 Agent 协作场景做协议选型；
5. 区分 OpenAI Assistants 与 Responses API 的差异，避开 2026 年弃用 Assistants 的迁移坑；
6. 监控 Anthropic Prompt Caching 的命中率，理解"命中率 < 19% 反而亏钱"的反直觉结论；
7. 实现 LLM 流式响应（SSE 协议），处理 tool_calls delta 累积；
8. 画出 LLM 协议演进时间线，理解协议层叠而非替代的演进规律；
9. 根据项目特征（工具数 / 跨进程 / 多 Agent / 托管需求）选择协议栈，从简到繁按需升级。

## 10 节导览

| 节 | 标题 | 一句话钩子 | 难度 |
|---|---|---|---|
| 3.1 | [Function Calling：OpenAI 协议与 Anthropic Tool Use 的差异](./3.1-function-calling-diff.md) | 协议差异不是字段名，而是**错误处理哲学**——Anthropic `is_error: true` 结构化错误 vs OpenAI prompt 软约定 | 🟢 |
| 3.2 | [JSON Schema 在工具描述中的关键细节](./3.2-json-schema-tool-description.md) | 工具 schema 里**最影响 LLM 选对工具的不是 type 也不是 enum，而是 description**——信息密度 10 词提到 50 词选对率 60%→92% | 🟢 |
| 3.3 | [MCP 协议精读：Resources / Prompts / Tools / Sampling](./3.3-mcp-protocol.md) | MCP 四大原语不是 Function Calling 升级版——**Resources 是"拉数据"**，**Sampling 是"反向调 LLM"**，Function Calling 完全做不到 | 🟡 |
| 3.4 | [MCP Server 实战：让 Agent 接入 IDE / DB / GitHub](./3.4-mcp-server-practice.md) | 写一个 MCP server 不超过 50 行——但 80% 坑不在协议本身，在**传输层选型**（stdio vs HTTP+SSE）和**安全沙箱** | 🟡 |
| 3.5 | [A2A 协议：Agent-to-Agent 通信模型](./3.5-a2a-protocol.md) | A2A 解决的不是"Agent 怎么调工具"（那是 MCP 的活），而是"Agent **怎么找另一个 Agent 并把任务委托给它**"——Agent Card 是入口 | 🟡 |
| 3.6 | [OpenAI Assistants API 与 Threads 模型](./3.6-openai-assistants.md) | Assistants "省心"的代价是**灵活性大幅下降**——**2026 年底弃用**，新项目用 Responses API + Agents SDK | 🟡 |
| 3.7 | [Anthropic Prompt Caching 的协议级实现](./3.7-anthropic-prompt-caching.md) | 命中率 < 50% 时反而亏钱——`cache_write` 比普通输入贵 25%，**盈亏平衡点 19%**，延迟收益（11s→1.6s）往往比省钱更重要 | 🟡 |
| 3.8 | [Streaming / SSE：长任务的实时反馈](./3.8-streaming-sse.md) | 流式不只省用户等待感，还降低 P95 延迟感知——**首 token 200-400ms vs 非流式 TTFT = 总完成时间**，生产必须开 | 🟢 |
| 3.9 | [协议演进时间线（Function Call → MCP → A2A）](./3.9-protocol-timeline.md) | 协议 18 个月走过 Web 协议 18 年——**协议不是替代是层叠**，Function Calling + MCP + A2A 共存是常态 | 🟢 |
| 3.10 | [协议选型决策树](./3.10-protocol-decision-tree.md) | **80% 场景选 Function Calling 就对了**——盲目追新（MCP / A2A）是协议选型最常见的误区，**从简到繁按需升级** | 🟢 |

## 学习路径建议

**首次通读（4-5 小时）**：按 3.1 → 3.10 顺序读。3.1-3.2 是协议基础必读，3.3-3.5 是新一代协议主线，3.6-3.7 是厂商能力，3.8-3.9 是工程实践与趋势，3.10 是选型收尾。

**协议基础优先（1-2 小时）**：专注 3.1-3.2——2 节覆盖 Function Calling 协议差异 + JSON Schema 细节。这是写工具、调 API 的基础。

**新一代协议主线（2-3 小时）**：3.3-3.5 配套读——3.3 讲 MCP 协议四大原语，3.4 讲 MCP server 实战（IDE/DB/GitHub），3.5 讲 A2A 协议。**这三节是 2025 年 Agent 工程的核心协议**。

**厂商能力与工程实践（1-2 小时）**：3.6（Assistants API + 2026 弃用迁移）+ 3.7（Prompt Caching 盈亏平衡）+ 3.8（Streaming/SSE）。**这三节是生产 Agent 的性能与成本优化关键**。

**协议选型视角（30 分钟）**：3.9-3.10 配套读——3.9 看完协议演进规律，3.10 直接套用决策树给自己的项目选协议栈。

**自测驱动（2 小时）**：每节 3-5 题自测，覆盖概念辨析 / 场景判断 / 代码补全 / 反直觉思考。建议读完每节立刻做题，错题回去看正文相应段落。

## 与 L1 / L2 / L4 的衔接

- **L1 → L3**：L1 的 1.4（ReAct）讲"模型怎么推理要不要调工具"，L3 的 3.1（Function Calling）把这种推理变成**协议级能力**；L1 的 1.5（ReWoo）讲"工具调用链"，L3 的 3.3-3.5（MCP / A2A）把工具调用链变成**可互操作的协议**。
- **L2 → L3**：L2 的 2.7（长期记忆）讲"MemGPT 怎么管理上下文"，L3 的 3.3（MCP Resources）提供"按需拉数据"的协议级原语；L2 的 2.9（缓存策略）讲应用层 Semantic Cache，L3 的 3.7（Prompt Caching）是**协议层 prefix cache**，两者互补（语义相似 vs 前缀精确）。
- **L3 → L4**：L3 的协议定义"Agent 怎么说话"，L4 给出"用 LangChain / LangGraph / LlamaIndex / AutoGen 等框架怎么落地"。**典型落地**：3.1 Function Calling → LangChain `bind_tools()` → 4.1 LangGraph ReAct Agent。

## 下一步

- **L4 · 框架与运行时层（12 节）**：把 L3 的协议落到 LangChain / LangGraph / LlamaIndex / AutoGen / CrewAI 等具体框架上，理解"协议 → 框架抽象 → 运行时执行"的完整链路。
- **L5 · 设计模式层（12 节）**：在 L4 框架之上抽象常见 Agent 设计模式（Reflection / Planning / Multi-Agent / RAG Fusion 等）。
- **附录 D · 术语表**：中英对照 + 缩写速查（MCP / A2A / SSE / TTFT / Tool Use / Schema 等）。