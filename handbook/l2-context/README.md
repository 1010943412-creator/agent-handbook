# L2 · 上下文工程层

> 10 节正文 | 10+ 张原创图 | 47+ 条 S/A 级引用 | 30+ 道自测题
> 作者：晴暖 | 协议：CC BY-NC-SA 4.0

## L2 总览

L2 是从 L1"理论地基"到 L3"协议接口"的**工程桥梁**——这一层不写 LLM 推理机制，而是写"怎么把 LLM 喂饱、喂对、喂便宜"。L1 解决了"LLM 能做什么"的问题，L2 解决"怎么用最少的 Context 拿到最好的结果"。

这 10 节是一条**递进的工程链**：2.1 先搞清上下文窗口的物理上限（Lost in the Middle、U 形曲线），2.2-2.5 进入 RAG 四件套（检索/重排/Embedding/向量库 + 高级 RAG 范式），2.6-2.7 处理记忆问题（短期滑动窗口 + 长期 MemGPT 分层），2.8-2.9 解决成本和延迟（LLMLingua 压缩 + Prompt/Semantic Cache），2.10 收尾——10 大反模式避坑清单，把 L2 全部踩过的坑汇总成可勾选 Checklist。

读完 L2，你应该能：
1. 解释清楚 Lost in the Middle 的 U 形曲线为什么决定 RAG 检索结果的注入顺序；
2. 在 4 种 RAG 范式（朴素 / HyDE / Self-RAG / GraphRAG）之间做选型；
3. 根据数据规模、查询模式、运维预算在 pgvector / Milvus / Qdrant / Chroma 之间选型；
4. 设计短期记忆（滑动窗口 + 关键事件 + 摘要）和长期记忆（MemGPT 分层）；
5. 用 LLMLingua 压缩 2-5x + 双层缓存把 LLM 调用成本降到 1/10。

## 10 节导览

| 节 | 标题 | 一句话钩子 | 难度 |
|---|---|---|---|
| 2.1 | [上下文窗口的物理上限](./2.1-context-window-limits.md) | 上下文从 4k 扩到 1M 是 250 倍提升，但有效利用率 < 50%——Lost in the Middle U 形曲线是工程幻觉 | 🟢 |
| 2.2 | [RAG 三件套：检索 / 重排 / 注入](./2.2-rag-three-pieces.md) | 纯向量检索不是 RAG 全部——BM25 在技术文档上常反超向量检索 10-20 个百分点 | 🟢 |
| 2.3 | [Embedding 模型选型矩阵](./2.3-embedding-selection.md) | MTEB 榜一不一定是你的最优——垂直领域"小模型 + 微调"反超通用大模型 | 🟡 |
| 2.4 | [向量库选型：pgvector / Milvus / Qdrant / Chroma](./2.4-vector-db-selection.md) | 80% 业务用 pgvector 就够了——盲目上 Milvus 带来 2-3 倍运维成本，收益只 5% | 🟡 |
| 2.5 | [高级 RAG：HyDE / Self-RAG / GraphRAG](./2.5-advanced-rag.md) | GraphRAG 不是银弹——关系稀疏时（< 10% 实体关系率）反而负优化 5-10% | 🔴 |
| 2.6 | [短期记忆：会话内 Context 管理](./2.6-short-term-memory.md) | 保留全量历史 ≠ 越聪明——混合策略（滑动 + 关键事件 + 摘要）比全量便宜 50%+ | 🟢 |
| 2.7 | [长期记忆：Letta / MemGPT 的存储分层](./2.7-long-term-memory.md) | 长期记忆 = 操作系统分层——Core 2k 永远在 prompt + Archival 无限历史按需召回 | 🔴 |
| 2.8 | [Token 压缩：LLMLingua / Selective Context](./2.8-prompt-compression.md) | 压缩 50% token 准确率反升 2-3%——去噪 + 反 Lost in the Middle 双机制 | 🟡 |
| 2.9 | [缓存策略：Prompt Cache / Semantic Cache](./2.9-cache-strategies.md) | 缓存真正的价值是降延迟（11s → 1.6s）而不是省钱——10 倍延迟差决定用户留不留 | 🟡 |
| 2.10 | [上下文注入反模式与避坑清单](./2.10-anti-patterns.md) | 90% 上下文问题出在这 5 个反模式——System Prompt 塞太多 / 历史无脑塞 / RAG 不重排等 | 🟢 |

## 学习路径建议

**首次通读（4-6 小时）**：按 2.1 → 2.10 顺序读。2.1 是物理上限必读，2.2-2.5 是 RAG 主线，2.6-2.9 是优化手段，2.10 是避坑收尾。

**RAG 视角优先（2-3 小时）**：专注 2.1-2.5——5 节覆盖"上下文窗口 → 检索 → 重排 → 向量库 → 高级范式"的完整 RAG 流水线。可直接读 2.10 的 RAG 相关反模式。

**记忆系统视角（2 小时）**：2.6-2.7 配套读——2.6 解决"会话内 Context 管理"，2.7 解决"跨 session 长期记忆"。短期 + 长期配合看是工业级 Agent 的标配。

**性能优化视角（2 小时）**：2.8-2.9 配套读——压缩（省 token）+ 缓存（省 API + 降延迟）。这两节是降低 LLM 成本的"双引擎"。

**自测驱动（2 小时）**：每节 3-5 题自测，覆盖概念辨析 / 场景判断 / 代码补全 / 反直觉思考。建议读完每节立刻做题，错题回去看正文相应段落。

## 与 L1 / L3 的衔接

- **L1 → L2**：L1 的 1.2（Token 经济）解释了"为什么 LLM 调用贵"，L2 的 2.8（压缩）和 2.9（缓存）给出"怎么降本"的具体方案；L1 的 1.8（能力雷达）告诉你"哪些任务该走 RAG"，L2 的 2.2-2.5 教你"怎么搭 RAG 流水线"。
- **L2 → L3**：L2 的"上下文管理"是 L3"协议层"的基础——3.x 协议层讲的是 Agent 之间怎么通信，通信内容就是 L2 准备好的 Context。L2 的 2.10 反模式里的"Prompt Injection"会在 L3 协议层 + L7 安全层深入展开。

## 下一步

- **L3 · 协议与接口层（10 节）**：在 L2 准备好的 Context 基础上，定义 Agent 之间、Agent 与工具之间的标准通信协议——Function Calling、Tool Use、JSON Schema、Anthropic MCP、OpenAI Function Calling 等。
- **L4 · 框架与运行时层（12 节）**：把 L3 的协议落到 LangChain / LangGraph / LlamaIndex / AutoGen 等具体框架上。
- **附录 D · 术语表**：中英对照 + 缩写速查（KV Cache、RAG、HyDE、MTEB、CoT 等）。
