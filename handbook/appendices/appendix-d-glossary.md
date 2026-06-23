# 附录 D:术语表(L1-L8 关键术语,100 词条)

> **目标**:L1-L8 关键术语的中英对照速查,纯术语不含缩写表/公式
> **受众**:🟢 入门 + 🟡 进阶
> **前置知识**:无(独立查阅)

---

## 使用说明

本附录收录 L1-L8 全部关键术语,按主题分 8 节(每节 10-12 词条,共 100 条)。每条格式:

```
**中文名** (English Name) —— 一句话定义 + 章节定位
```

读者用法:看到陌生术语先查本表,定位章节后再回到正文细读。**章节定位**标注 `L1.4` 即第 1 层第 4 节,以此类推。

---

## D.1 L1 基础理论(10 词条)

- **Transformer** —— 基于自注意力机制的序列模型,是现代 LLM 的基础架构,见 L1.1
- **KV Cache** (Key-Value Cache) —— Transformer decode 阶段缓存历史 token 的 K/V,加速推理,见 L1.2
- **Token** —— LLM 处理文本的最小单位,中文 1 字 ≈ 1-2 token,见 L1.1
- **Prompt** —— 输入给 LLM 的文本(含指令/上下文/问题),见 L1.3
- **CoT** (Chain of Thought) —— 思维链,通过让 LLM 展示推理步骤提升复杂任务表现,见 L1.3
- **Few-shot** —— 少样本学习,在 prompt 中给 2-5 个示例引导 LLM,见 L1.3
- **ReAct** (Reasoning + Acting) —— 推理与行动循环模式,见 L1.4
- **ReWOO** —— Reasoning With Open Observation,把推理与观察解耦的范式,见 L1.5
- **Reflection** —— 自我反思,让 LLM 评估并修正自己的输出,见 L1.6
- **Plan-and-Execute** —— 先规划后执行,把任务拆成步骤再逐步执行,见 L1.6

---

## D.2 L2 上下文工程(12 词条)

- **RAG** (Retrieval-Augmented Generation) —— 检索增强生成,检索外部知识补充 LLM 回答,见 L2.1
- **Embedding** —— 向量化,把文本转为稠密向量用于语义检索,见 L2.2
- **BM25** —— 经典基于词频的检索算法,RAG 中常与向量检索融合,见 L2.3
- **Cross-Encoder** —— 精排模型,query 与 doc 联合打分,精度高但慢,见 L2.4
- **HyDE** (Hypothetical Document Embeddings) —— 用假设答案生成 embedding 提升检索,见 L2.5
- **Self-RAG** —— LLM 自主判断是否需要检索的自适应 RAG,见 L2.6
- **GraphRAG** —— 基于知识图谱的 RAG,擅长关系推理,见 L2.7
- **MemGPT** —— 分层记忆架构,模拟操作系统分页管理长期记忆,见 L2.8
- **Letta** —— 开源长期记忆 Agent 框架(MemGPT 开源版),见 L2.8
- **LLMLingua** —— Prompt 压缩算法,减少 token 数,见 L2.9
- **Prompt Cache** —— Prompt 缓存,OpenAI/Anthropic 提供按前缀匹配的缓存机制,见 L2.10
- **Semantic Cache** —— 语义缓存,基于向量相似度命中已缓存回答,见 L2.11

---

## D.3 L3 协议(12 词条)

- **Function Calling** —— LLM 调用外部函数的标准协议(OpenAI 首发),见 L3.1
- **Tool Use** —— Anthropic 对 Function Calling 的等价命名,见 L3.2
- **JSON Schema** —— 描述工具参数结构的 JSON 规范,见 L3.1
- **MCP** (Model Context Protocol) —— Anthropic 主导的 LLM-工具协议,见 L3.3
- **MCP Resources** —— MCP 协议中 LLM 可读取的资源(文件/API),见 L3.4
- **MCP Prompts** —— MCP 协议中的 prompt 模板,见 L3.5
- **MCP Sampling** —— MCP 协议中让 Server 调用 LLM 的能力,见 L3.6
- **A2A** (Agent-to-Agent) —— Google 主导的 Agent 间通信协议,见 L3.7
- **SSE** (Server-Sent Events) —— 服务端推送事件,流式输出基础,见 L3.8
- **Streaming** —— 流式输出,逐 token 返回 LLM 响应,见 L3.8
- **Assistants API** —— OpenAI 的会话+工具持久化 API(已被 Agents SDK 替代),见 L3.9
- **Threads** —— Assistants API 的会话上下文载体,见 L3.9

---

## D.4 L4 框架(12 词条)

- **LangChain** —— 通用 LLM 应用编排框架,生态最广,见 L4.1
- **LCEL** (LangChain Expression Language) —— LangChain 的链式声明语法,见 L4.2
- **LangGraph** —— LangChain 的状态机扩展,适合多 Agent/长任务,见 L4.3
- **LlamaIndex** —— RAG 优先的 LLM 框架,见 L4.4
- **AutoGen** —— Microsoft 主导的多 Agent 对话框架(0.4+ 重构),见 L4.5
- **CrewAI** —— 角色化协作多 Agent 框架,低代码,见 L4.6
- **OpenAI Agents SDK** —— OpenAI 官方轻量 Agent 框架(2025+),见 L4.7
- **Claude Agent SDK** —— Anthropic 官方 Agent SDK,长任务与工具深度集成(2025+),见 L4.8
- **Semantic Kernel** —— Microsoft 的企业级 .NET AI 编排框架,见 L4.9
- **Haystack** —— deepset 的 NLP Pipeline 框架,RAG 场景成熟,见 L4.10
- **Runnable** —— LangChain LCEL 的核心接口,所有链式组件实现它,见 L4.2
- **AgentExecutor** —— LangChain Agent 的执行器,负责循环 ReAct,见 L4.2

---

## D.5 L5 模式(12 词条)

- **ReAct Pattern** (Reasoning + Acting) —— 推理与行动循环模式,见 L5.1
- **Reflection Pattern** —— 自我反思模式,LLM 评估并修正自己的输出,见 L5.2
- **Plan-and-Execute Pattern** —— 规划与执行模式,先规划后分步执行,见 L5.3
- **Tool Use Pattern** —— 工具使用模式,Function Calling 的模式层抽象,见 L5.4
- **Routing Pattern** —— 路由模式,Supervisor 根据输入选子 Agent,见 L5.5
- **Parallelization Pattern** —— 并行模式,Sectioning(分块)/Voting(投票)两种子模式,见 L5.6
- **Orchestrator-Workers Pattern** —— 编排者-工作者模式,中心节点一次性分发任务,见 L5.7
- **Evaluator-Optimizer Pattern** —— 评估-优化模式,自动打分并改进输出,见 L5.8
- **Memory Pattern** —— 记忆模式,短期/长期/共享三层记忆架构,见 L5.9
- **Human-in-the-Loop** (HITL) —— 人在回路,关键决策点引入人工审核,见 L5.10
- **Multi-Agent Pattern** —— 多 Agent 协作模式总称,见 L5.11
- **Supervisor Pattern** —— 多 Agent 中的调度者节点,中心化决策,见 L5.11 + 附录 B

---

## D.6 L6 可观测(10 词条)

- **Tracing** —— 全链路追踪,记录每次 LLM 调用的输入/输出/延迟/成本,见 L6.1
- **Span** —— 链路中的一个工作单元(如一次 LLM 调用),见 L6.2
- **Trace** —— 由多个 Span 组成的完整调用链,见 L6.2
- **OpenTelemetry** (OTel) —— 跨语言链路追踪标准,Agent 系统的观测基础,见 L6.3
- **Langfuse** —— 开源 LLM 可观测平台,OpenTelemetry 兼容,见 L6.4
- **LangSmith** —— LangChain 官方的 LLM 调试/追踪平台,见 L6.5
- **Phoenix** —— Arize 开源的 LLM 可观测工具,见 L6.6
- **LLM-as-Judge** —— 用 LLM 评估另一个 LLM 输出的元层评测方法,见 L6.7
- **SWE-bench** —— 评估 LLM 解决真实 GitHub Issue 能力的基准,见 L6.8
- **GAIA** —— 通用 AI 助手基准,测试多步推理与工具使用,见 L6.9

---

## D.7 L7 生产安全(12 词条)

- **Guardrails** —— 防护栏,输入/输出/工具三层校验,见 L7.1
- **Prompt Injection** —— 提示注入攻击,通过恶意输入劫持 LLM 行为,见 L7.2
- **RBAC** (Role-Based Access Control) —— 基于角色的访问控制,见 L7.3
- **E2B** —— 云端代码沙箱服务,50ms 冷启动,适合交互场景,见 L7.4
- **Firecracker** —— AWS 开源的 microVM,适合长任务代码隔离,见 L7.5
- **Circuit Breaker** —— 熔断器,故障率超阈值时降级到备用方案,见 L7.6
- **SLO** (Service Level Objective) —— 服务等级目标,可用性的具体数值承诺,见 L7.7
- **SLI** (Service Level Indicator) —— 服务等级指标,实际测量的可用性,见 L7.7
- **GDPR** (General Data Protection Regulation) —— 欧盟数据保护法规,见 L7.8
- **数据脱敏** —— 移除/替换 PII 字段,合规要求,见 L7.8
- **混沌工程** (Chaos Engineering) —— 在生产环境主动注入故障的演练方法,见 L7.9
- **凭据隔离** —— 把账号密码等敏感信息隔离到 Vault,不进代码或 .env,见 L7.10

---

## D.8 L8 案例(10 词条)

- **RRF** (Reciprocal Rank Fusion) —— 多路召回融合算法,见 8.1 RAG 案例
- **CodeAct** —— 用可执行代码作为 Action 的 Agent 范式,见 8.2 编程案例
- **EXPLAIN** —— 数据库查询计划分析,8.3 用于慢查询预检
- **sqlparse** —— Python SQL 解析器,8.3 用于拦截 DELETE/DROP
- **Playwright** —— 微软开源浏览器自动化框架,见 8.4 浏览器案例
- **RAG 引用溯源** —— 把答案标注到具体 chunk 来源,避免幻觉,见 8.1
- **工单系统** —— 客服场景的工单流转系统,见 8.6 客服案例
- **多 Agent Supervisor** —— Supervisor 调度多 Agent 的模式,见 8.5 小红书案例
- **升级人工** —— 客服 Agent 把复杂问题转人工的策略,见 8.6
- **工单降级** —— 工单系统故障时降级到 FAQ 模板,见 8.6 + L7.9

---

## D.9 其他常用术语(10 词条)

- **LLM** (Large Language Model) —— 大语言模型,本手册的核心对象
- **Agent** —— 能自主决策并调用工具完成任务的 LLM 系统,见 L0 引言
- **Prompt Engineering** —— 提示工程,设计与优化 prompt 的方法论
- **Fine-tuning** —— 微调,在特定数据上继续训练 LLM 适配下游任务
- **RLHF** (Reinforcement Learning from Human Feedback) —— 基于人类反馈的强化学习
- **Embedding Model** —— 嵌入模型,把文本转为向量,见 L2.2
- **Token 压缩** —— 用 LLMLingua 等算法减少 prompt token 数
- **多模态** (Multimodal) —— 同时处理文本/图像/音频/视频的模型
- **Vector Database** —— 向量数据库,存储 embedding 并支持相似度检索
- **Function Calling** —— 详见 L3.1(与 D.3 重复出现,提示核心重要性)

---

## 配套资源

- **L0 引言** —— 手册整体定位与读者路径
- **L1-L8 全部章节** —— 词条章节定位的展开内容
- **附录 A ReAct 模板** —— ReAct/Function Calling 等术语的代码示例
- **附录 B 多 Agent 骨架** —— Supervisor / Multi-Agent 的骨架实现
