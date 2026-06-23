# 附录 C:AGENT 框架选型矩阵(纯表格快查)

> **目标**:9 个 Agent 框架的集中对比速查表,一眼扫完知道"该选谁"
> **受众**:🟡 进阶 + 🔴 专家
> **前置知识**:必读 L4.1 框架全景 + L4.10 框架选型决策矩阵

---

## C.0 使用说明

本附录聚焦**速查**,不做版本号、依赖、迁移成本等细节(详见 L4.10)。读者通常处于以下两种场景之一:

1. **新项目立项**:不知道选哪个框架,先扫本附录确定候选(2-3 个),再读 L4.10 做最终决策。
2. **旧项目重构**:已经在用某个框架,想评估"要不要换",用本附录横向对比。

⚠️ **数据更新提示**:GitHub Stars 与维护状态随时间变化,本附录对这两个字段统一标 `TBD` 占位。读者用前请 `curl https://api.github.com/repos/<owner>/<repo>` 获取实时数据。**绝不**编造具体数字。

---

## C.1 框架清单(9 个)

按"通用性 / 专业性"维度排序:

1. **LangChain** —— 通用 LLM 编排框架,生态最广
2. **LangGraph** —— 状态机驱动的 LangChain 扩展,长任务首选
3. **LlamaIndex** —— RAG 优先的编排框架
4. **AutoGen**(Microsoft) —— 对话式多 Agent
5. **CrewAI** —— 角色化多 Agent 框架,上手快
6. **OpenAI Agents SDK** —— OpenAI 官方轻量 SDK(2025+)
7. **Claude Agent SDK**(Anthropic) —— 官方长任务 SDK(2025+)
8. **Semantic Kernel**(Microsoft) —— 企业 .NET 生态 Agent 框架
9. **Haystack**(deepset) —— NLP Pipeline 框架,RAG 传统强项

---

## C.2 基础对比表(9 框架 × 8 维度)

| 框架 | 类型 | GitHub Stars | 维护状态 | 学习曲线 | 生产就绪 | 性能 | 文档质量 | 适用场景 |
|---|---|---|---|---|---|---|---|---|
| LangChain | 通用编排 | TBD | 活跃 | 中 | 高 | 中 | 优 | 通用 RAG/Agent |
| LangGraph | 状态机 | TBD | 活跃 | 中高 | 高 | 高 | 优 | 多 Agent / 长任务 |
| LlamaIndex | RAG 优先 | TBD | 活跃 | 低中 | 中高 | 中 | 良 | RAG 场景 |
| AutoGen | 多 Agent 对话 | TBD | 活跃(0.4+) | 中高 | 中 | 中 | 良 | 多 Agent 协作 |
| CrewAI | 角色化多 Agent | TBD | 活跃 | 低 | 中 | 中 | 良 | 快速多 Agent 原型 |
| OpenAI Agents SDK | 轻量官方 | TBD | 活跃(2025+) | 低 | 高 | 高 | 优 | OpenAI 生态快速原型 |
| Claude Agent SDK | 长任务官方 | TBD | 活跃(2025+) | 中 | 高 | 高 | 优 | Anthropic 长任务 / 工具深度 |
| Semantic Kernel | 企业 .NET | TBD | 活跃 | 中 | 高 | 中 | 良 | 企业 .NET 生态集成 |
| Haystack | NLP Pipeline | TBD | 活跃 | 中 | 高 | 高 | 良 | NLP / RAG 传统场景 |

**维度解释**:
- **类型**:框架定位,决定它擅长什么
- **Stars**:社区热度参考(避免编造,标 TBD)
- **维护状态**:近 6 个月是否有 commit / release
- **学习曲线**:1 周内能否上手做 demo(低 / 中 / 高)
- **生产就绪**:是否有大型项目案例、监控、调试工具
- **性能**:框架本身 overhead(高 = overhead 低,贴近原生)
- **文档质量**:examples/tutorials 完善度
- **适用场景**:框架的甜蜜点

---

## C.3 场景决策表(4 场景 × 9 框架)

| 场景 | 推荐 | 备选 | 不推荐 | 理由 |
|---|---|---|---|---|
| **长任务执行** | LangGraph | Claude Agent SDK | AutoGen | LangGraph 状态机 + checkpoint 最成熟;Claude SDK 长任务工具深度集成;AutoGen 对话式调试困难 |
| **RAG 优先** | LlamaIndex | LangChain | Haystack | LlamaIndex RAG 范式最成熟,索引/检索/re-rank 一站式;LangChain 通用性强但 RAG 不如 LlamaIndex 专注;Haystack 偏 NLP 工程师 |
| **多 Agent 对话** | AutoGen | CrewAI | LangChain | AutoGen 对话式多 Agent 最深,sub-agent 可自由通信;CrewAI 角色化入门更友好;LangChain 多 Agent 需自己组装 |
| **快速原型** | OpenAI Agents SDK | LangChain | AutoGen | OpenAI SDK 极简,几行代码即可跑通;LangChain 通用但概念多;AutoGen 上手成本高 |

---

## C.4 阅读建议

**初次选型**:先看 C.3 场景表,定位你的场景属于哪一类,锁定"推荐"列的框架(1-2 个候选),然后:

1. 读 L4.1 框架全景理解框架定位
2. 读 L4.10 决策矩阵看版本/依赖/迁移成本
3. 跑官方 quickstart demo 验证"上手体感"
4. 选 1 个框架 PoC 1-2 周,再决定是否投入

**已经选型**:用 C.2 基础表横向扫一遍,如果你当前用的框架在"适用场景"列与你的实际场景不匹配,考虑迁移或搭配使用(例如:主用 LangGraph 状态机,某些 RAG 步骤调用 LlamaIndex)。

**生态选型**:9 个框架部分可组合使用:
- LangGraph + LlamaIndex(状态机 + RAG 检索)
- LangChain + CrewAI(通用编排 + 多 Agent 角色)
- OpenAI Agents SDK + LangGraph 工具(快速原型 + 状态机)

**避免的选型**:
- ❌ AutoGen 跑生产长任务(调试困难,Decision Log 不可见)
- ❌ LlamaIndex 做多 Agent 协作(它不擅长 sub-agent 通信)
- ❌ LangChain 单跑多 Agent(不如 AutoGen/CrewAI 直接)
- ❌ Semantic Kernel 跨 .NET 边界(若团队不是 .NET 栈)

---

## C.5 与 L4.10 关系

| 维度 | L4.10 决策矩阵 | 附录 C 速查表 |
|---|---|---|
| 内容 | 详细决策树 + 版本依赖 + 迁移成本 | 8 维度横向对比 + 4 场景推荐 |
| 篇幅 | 长文 ~3000 字 | 纯表格 + 短说明 ~2000 字 |
| 适用 | 立项最终决策 | 立项初筛 + 日常速查 |
| 数据 | 实时数据 + 引用 | TBD 占位,避免编造 |

**配合使用**:附录 C 做"快筛"(知道候选),L4.10 做"深选"(确定最终)。

---

## C.6 配套资源

- **L4.1 框架全景** —— 9 框架的定位与生态
- **L4.10 框架选型决策矩阵** —— 详细决策树与迁移成本
- **L5.11 Multi-Agent 反模式** —— 多 Agent 选型时的常见踩坑
- **9 框架官方 GitHub README** —— 实时数据与最新 release

> 📚 本附录参考
>
> - [https://github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain) —— LangChain README,生态/版本/特性
> - [https://github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) —— LangGraph README,状态机设计
> - [https://github.com/run-llama/llama_index](https://github.com/run-llama/llama_index) —— LlamaIndex README,RAG 范式
> - [https://github.com/microsoft/autogen](https://github.com/microsoft/autogen) —— AutoGen README,对话式多 Agent
> - [https://github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) —— CrewAI README,角色化多 Agent
> - [https://github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python) —— OpenAI Agents SDK
> - [https://github.com/anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) —— Claude Agent SDK
> - [https://github.com/microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) —— Semantic Kernel README
> - [https://github.com/deepset-ai/haystack](https://github.com/deepset-ai/haystack) —— Haystack README
