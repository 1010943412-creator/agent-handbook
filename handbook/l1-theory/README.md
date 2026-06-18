# L1 · 基础理论层

> 8 节正文 | 8+ 张原创图 | 32+ 条 S/A 级引用 | 32+ 道自测题
> 作者：晴暖 | 协议：CC BY-NC-SA 4.0

## L1 总览

L1 是整个手册的**地基**——不写代码也能读懂，但读完后能让你对“Agent 为什么这么设计”有物理级理解。

这 8 节不是 8 个独立话题，而是一条**递进的因果链**：1.1 先搞清 LLM 怎么“算出”下一个 token（Transformer 推理 + KV Cache 的工程账），1.2 再看用 LLM 的真实代价（成本 / 延迟 / 上下文三角约束），1.3 学怎么写好 Prompt（System / Few-shot / CoT 三件套），1.4-1.7 进入 Agent 的四种核心范式（ReAct 动态循环、ReWOO 静态规划、Plan-and-Execute 动态规划、Self-Reflection 自我批评），1.8 收尾——LLM 不是万能的，能力雷达决定了“哪些任务交给 LLM、哪些交给工具”。

读完 L1，你应该能：
1. 解释清楚为什么 ReAct 在生产里要卡 `max_steps` 和 `max_tokens`；
2. 根据任务类型在 ReAct / ReWOO / Plan-and-Execute 之间选型；
3. 识别 Self-Reflection 的有效边界（Self-Eval 盲点 → External Critic）；
4. 画出能力雷达，判断一个任务该用 LLM 还是工具。

## 8 节导览

| 节 | 标题 | 一句话钩子 | 难度 |
|---|---|---|---|
| 1.1 | [LLM 速通：Transformer 推理路径与 KV Cache](./1.1-llm-inference.md) | KV Cache 不是“缓存越多越好”——7B 模型 128k 上下文能吃掉 20GB+ 显存 | 🟢 |
| 1.2 | [Token 经济：成本 / 延迟 / 上下文的三角约束](./1.2-token-economics.md) | 输出 token 比输入贵 5 倍——Self-Reflection 多一轮就是 5 倍烧钱 | 🟢 |
| 1.3 | [Prompt 三件套：System / Few-shot / CoT](./1.3-prompt-three-pieces.md) | CoT 对简单任务掉点 5-15%——Prompt 不是越多越好 | 🟢 |
| 1.4 | [ReAct 论文精读：Reasoning + Acting 的循环](./1.4-react-paper.md) | ReAct 让 LLM 第一次能与外部实时交互——所有现代 Agent 的祖师爷 | 🟢 |
| 1.5 | [ReWOO：把推理与观察解耦，省 token](./1.5-rewoo.md) | ReWOO 比 ReAct 省 64% token 但失去动态调整能力 | 🟢 |
| 1.6 | [Plan-and-Execute：先规划后执行](./1.6-plan-and-execute.md) | 显式 Re-Planner 让长任务成功率从 65% 提到 78% | 🟢 |
| 1.7 | [Self-Reflection：自我批评的边界](./1.7-self-reflection.md) | Reflexion 让 HumanEval 从 67% 到 88%，但 Self-Eval 有认知盲点 | 🟢 |
| 1.8 | [LLM 能力雷达：哪类任务交给 LLM，哪类不要](./1.8-llm-radar.md) | 多位数乘法裸 LLM 30% 准确率，写代码调工具 100% | 🟢 |

## 学习路径建议

**首次通读（4-6 小时）**：按 1.1 → 1.8 顺序读，每节 30-45 分钟。1.1-1.3 是“LLM 基础”，不读后面会卡；1.4-1.7 是“Agent 四种范式”，可对比读；1.8 是“全局视角”，放最后收尾。

**工程视角优先（2 小时）**：跳过 1.1 / 1.3 的代码细节，专注 1.2 / 1.4 / 1.5 / 1.8——这 4 节直接对应生产选型决策。

**论文视角优先（3 小时）**：1.4 / 1.5 / 1.6 / 1.7 都给了原始论文精读，配合代码片段可作为组会 paper-reading 素材。

**自测驱动（2 小时）**：每节 3-5 题自测，覆盖概念辨析 / 场景判断 / 代码补全 / 反直觉思考。建议读完每节立刻做题，错题回去看正文相应段落。

## 下一步

- **L2 · 上下文工程层（10 节）**：把 L1 的“能力雷达”落到“上下文管理”具体技术——RAG、Embedding、向量库、记忆系统、Token 压缩、缓存策略。
- **附录 D · 术语表**：中英对照 + 缩写速查（KV Cache、TTFT、TPOT、CoT 等）。