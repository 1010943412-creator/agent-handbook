# 《AGENT 七层手册》目录

> 72 节正文 + 6 实战案例 + 4 附录 + 79 题自测题库
> **累计 ~11.77 万字 / 85 个 .md / 95+ 图 / 90+ S/A 引用**
> 作者：晴暖

## 🟢 L1 · 基础理论层（8 节）

- 1.1 LLM 速通：Transformer 推理路径与 KV Cache
- 1.2 Token 经济：成本 / 延迟 / 上下文的三角约束
- 1.3 Prompt 三件套：System / Few-shot / CoT
- 1.4 ReAct 论文精读：Reasoning + Acting 的循环
- 1.5 ReWOO：把推理与观察解耦，省 token
- 1.6 Plan-and-Execute：先规划后执行
- 1.7 Self-Reflection：自我批评的边界
- 1.8 LLM 能力雷达：哪类任务交给 LLM，哪类不要

## 🟢 L2 · 上下文工程层（10 节）

- 2.1 上下文窗口的物理上限
- 2.2 RAG 三件套：检索 / 重排 / 注入
- 2.3 Embedding 模型选型矩阵
- 2.4 向量库选型：pgvector / Milvus / Qdrant / Chroma
- 2.5 高级 RAG：HyDE / Self-RAG / GraphRAG
- 2.6 短期记忆：会话内 Context 管理
- 2.7 长期记忆：Letta / MemGPT 的存储分层
- 2.8 Token 压缩：LLMLingua / Selective Context
- 2.9 缓存策略：Prompt Cache / Semantic Cache
- 2.10 上下文注入反模式与避坑清单

## 🟢🟡 L3 · 协议与接口层（10 节）

- 3.1 Function Calling：OpenAI 协议与 Anthropic Tool Use 的差异
- 3.2 JSON Schema 在工具描述中的关键细节
- 3.3 MCP 协议精读：Resources / Prompts / Tools / Sampling
- 3.4 MCP Server 实战：让 Agent 接入 IDE / DB / GitHub
- 3.5 A2A 协议：Agent-to-Agent 通信模型
- 3.6 OpenAI Assistants API 与 Threads 模型
- 3.7 Anthropic Prompt Caching 的协议级实现
- 3.8 Streaming / SSE：长任务的实时反馈
- 3.9 协议演进时间线（Function Call → MCP → A2A）
- 3.10 协议选型决策树

## 🟡 L4 · 框架与运行时层（12 节）

- 4.1 框架全景：LangChain / LlamaIndex / AutoGen / CrewAI / LangGraph / OpenAI Agents SDK / Claude Agent SDK
- 4.2 LangChain 1.x：Runnable 与 LCEL
- 4.3 LangGraph：状态机 + 持久化 + Human-in-the-Loop
- 4.4 LlamaIndex：RAG 优先的范式
- 4.5 AutoGen：对话式多 Agent
- 4.6 CrewAI：角色化协作
- 4.7 OpenAI Agents SDK：轻量官方参考实现
- 4.8 Claude Agent SDK：长任务与工具深度集成
- 4.9 Agent 协议适配器：跨框架的中间层
- 4.10 框架选型决策矩阵
- 4.11 自研 vs 用框架：何时值得自己写
- 4.12 Agent 框架演进时间线

## 🟢🟡 L5 · 设计模式层（12 节）

- 5.1 ReAct 模式
- 5.2 Reflection 模式
- 5.3 Plan-and-Execute 模式
- 5.4 Tool Use 模式
- 5.5 Routing 模式（Supervisor + 子 Agent）
- 5.6 Parallelization 模式（Sectioning / Voting）
- 5.7 Orchestrator-Workers 模式
- 5.8 Evaluator-Optimizer 模式
- 5.9 Memory 模式（短期 / 长期 / 共享）
- 5.10 Human-in-the-Loop 模式
- 5.11 Multi-Agent 协作的反模式与踩坑
- 5.12 模式组合实战：从单 Agent 到多 Agent 的演化路径

## 🟡 L6 · 可观测与评估层（10 节）

- 6.1 Tracing 基础：Span / Trace / Context Propagation
- 6.2 OpenTelemetry 在 Agent 中的落地
- 6.3 Langfuse / LangSmith / Arize Phoenix 选型
- 6.4 Eval 三件套：单元 / 集成 / 端到端
- 6.5 LLM-as-Judge：评估的元层
- 6.6 Agent 评测基准：SWE-bench / GAIA / AgentBench
- 6.7 成本监控：Token 用量 × 工具调用 × 缓存命中率
- 6.8 延迟分析：TTFT / TPOT / 端到端 P95
- 6.9 A/B 与灰度：Agent 系统的实验设计
- 6.10 可观测性反模式：日志打全 vs 有效信号

## 🔴 L7 · 生产化与安全层（10 节 / 1.40 万字）

- 7.1 Guardrails：输入/输出/工具三层防护
- 7.2 Prompt Injection 攻防
- 7.3 工具权限：最小化原则与沙箱
- 7.4 代码执行沙箱：E2B / Docker / Firecracker
- 7.5 鉴权与会话：用户态 / 工具态分离
- 7.6 部署形态：Serverless / Container / Long-running Worker
- 7.7 容量评估：QPS / 并发 / 限流设计
- 7.8 故障注入与混沌工程
- 7.9 SLA 与降级策略
- 7.10 合规与审计：日志保留 / 数据脱敏 / 区域合规

## ✅ L8 · 实战案例层（6 案例 / 0.78 万字 / 12 图 / 24 引用）

- 8.1 企业知识库 RAG Agent
- 8.2 生产级 Coding Agent
- 8.3 数据库 Agent（Text2SQL）—— 晴暖独家深度
- 8.4 浏览器自动化 Agent
- 8.5 小红书爆款笔记生成 Agent（引流爆款）
- 8.6 电商智能客服 Agent（引流爆款）

## 附录

- **附录 A**：ReAct Agent 模板（Python 主版 150 行 + TypeScript 辅助 50 行）
- **附录 B**：多 Agent 协作骨架（LangGraph Supervisor 80 行）
- **附录 C**：AGENT 框架选型矩阵（9 框架 × 8 维度 + 4 场景决策）
- **附录 D**：术语表（L1-L8 关键术语 100 词条）

## 自测题库（79 题）

- **quiz-l1-l3.md**：28 题（L1 × 8 + L2 × 10 + L3 × 10）
- **quiz-l4-l5.md**：24 题（L4 × 12 + L5 × 12）
- **quiz-l6-l8.md**：27 题（L6 × 11 + L7 × 10 + L8 × 6）
- 题型分布：选择 64 + 判断 15 = **79 题**，每题含答案 + 解析
