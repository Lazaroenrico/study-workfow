# My AI Engineering Path
<!-- Managed by /nivelamento and /curriculo. Placement note: Aulas/Nivelamento 2026-10-05.md -->

## Mission
"o conjunto de todos os 4, a qual eu passaria para um próximo nível ao tê-los" — construir agentes em produção, construir produtos com LLM, entender os modelos por dentro e conseguir vaga de AI engineer · Route: agentic-ai-engineer + applied-ai-engineer + ai-evaluation-reliability-engineer — Agent Systems Engineering, LLM Product Engineering, AI Evaluation and Reliability · Scope: rota + mecanismo

## Placement
- Date: 2026-10-06 (iniciado 2026-10-05)
- Method: adaptive, 60 questions across 15 strands
- Pace: ~6 h/week
- Estimated: ~130 h for the study queue (~22 semanas): 101 h do nivelamento + 3 aulas novas + ~24 h de mentoria S02–S07

## Strands
| Strand | Result | Entry lesson | Mechanism | Practice |
|--------|--------|--------------|-----------|----------|
| algebra-linear | Vocabulário sem mecanismo | [0] 01/01-linear-algebra-intuition | falhou em [1] (produto escalar ↔ ângulo) | — |
| calculo-otimizacao | Borda em [0] | [0] 01/04-calculus-for-ml | nada passou | — |
| probabilidade | Borda em [1] | [1] 01/07-bayes-theorem | ok em [0] | — |
| ml-classico | Borda em [1] | [1] 02/02-linear-regression | ok em [0] | só leu/ouviu |
| redes-neurais | Borda em [0] | [0] 03/01-the-perceptron | nada passou | só leu/ouviu |
| representacao-texto | Borda em [4] | [4] 10/01-tokenizers | ok em [1],[3],[5],[6]; cosseno sem geometria | exercício/mentoria |
| atencao-transformers | Borda em [1] | [1] 05/10-attention-mechanism | ok em [0] | só leu/ouviu |
| treino-llms | Borda em [8] | [8] 10/10-evaluation | ok em [2],[6],[7] | só leu/ouviu |
| prompting | Borda em [5] (quase dominada) | [5] 05/20-structured-outputs-constrained-decoding | ok em [1]–[4],[6] | exercício/mentoria |
| rag | Borda em [0] (prática à frente da base) | [0] 05/14-information-retrieval-search | ok em [2]–[4] | só leu/ouviu |
| tools-mcp | Borda em [0] (concepção errada) | [0] 13/01-the-tool-interface | errou quem executa a tool | — |
| agentes | Borda em [0] (prática à frente da base) | [0] 14/01-the-agent-loop | ok em [2],[5],[6]; errou [0],[8] | exercício/mentoria |
| avaliacao | Borda em [1] (prática à frente da base) | [1] 11/10-evaluation | ok em [2],[4]; errou estatística | só leu/ouviu |
| producao | Borda em [10] | [10] 17/04-vllm-serving-internals | ok em [5],[8],[9] | só leu/ouviu |
| seguranca | Borda em [1] | [1] 14/27-prompt-injection-defense | ok em [0]; errou ponto de controle | só leu/ouviu |

## Study queue
<!-- /curriculo takes the first unchecked item. "confirmar" = post-quiz / mechanism check only. -->
<!-- Roteiro integrado (2026-10-08): mentoria na ordem das semanas + as aulas do currículo que dão o mecanismo de cada semana, e 1–2 aulas de base por etapa (ritmo 2:1, escolha do aprendiz). Itens "mentoria:" são feitos com /mentoria (triagem = Step 4; blocos = Steps 5–6). Semana nova da mentoria = etapa nova antes de "Depois": puxa de "Depois" as aulas relacionadas e as 1–2 próximas aulas de base. -->

### Etapa 1 — Agentes e tools · S02
- [ ] 13-tools-and-protocols/01-the-tool-interface — The Tool Interface — Why Agents Need Structured I/O · tools-mcp · fazer
- [ ] 13-tools-and-protocols/02-function-calling-deep-dive — Function Calling Deep Dive — OpenAI, Anthropic, Gemini · tools-mcp · fazer
- [ ] mentoria: S02 LangChain e LangGraph — triagem dos 10 blocos · mentoria · triagem
- [ ] mentoria: S02 LangChain e LangGraph — blocos 1–4: framework, primitivas, mensagens e tool call, Runnable · mentoria · blocos 1–4
- [ ] 01-math-foundations/01-linear-algebra-intuition — Linear Algebra Intuition · algebra-linear · fazer
- [ ] 14-agent-engineering/01-the-agent-loop — The Agent Loop: Observe, Think, Act · agentes · fazer
- [ ] 14-agent-engineering/06-tool-use-and-function-calling — Tool Use and Function Calling · agentes · fazer
- [ ] 11-llm-engineering/09-function-calling — Function Calling & Tool Use · tools-mcp · confirmar
- [ ] mentoria: S02 LangChain e LangGraph — blocos 5–6: stream e async, ReAct e create_agent · mentoria · blocos 5–6
- [ ] 01-math-foundations/02-vectors-matrices-operations — Vectors, Matrices & Operations · algebra-linear · fazer
- [ ] 11-llm-engineering/16-langgraph-state-machines — Agent State Machines — Graphs, Nodes, Checkpoints · agentes · fazer
- [ ] mentoria: S02 LangChain e LangGraph — blocos 7–10: LangGraph como runtime, grafo ReAct na mão, stream modes, reducers · mentoria · blocos 7–10
- [ ] 14-agent-engineering/26-failure-modes-agentic — Failure Modes: Why Agents Break · agentes · fazer
- [ ] 14-agent-engineering/27-prompt-injection-defense — Prompt Injection and the PVE Defense · seguranca · fazer

### Etapa 2 — Structured output · S03
- [ ] mentoria: S03 Structured Output — triagem dos 8 blocos + blocos 1–2: schema como contrato, não é tool nem agent · mentoria · triagem + blocos 1–2
- [ ] 05-nlp-foundations-to-advanced/20-structured-outputs-constrained-decoding — Structured Outputs & Constrained Decoding · prompting · fazer
- [ ] mentoria: S03 Structured Output — blocos 3–8: pedir × obrigar, Pydantic, Literal, Field e retries, nested, fail early · mentoria · blocos 3–8
- [ ] 13-tools-and-protocols/05-tool-schema-design — Tool Schema Design — Naming, Descriptions, Parameter Constraints · tools-mcp · confirmar
- [ ] 01-math-foundations/03-matrix-transformations — Matrix Transformations · algebra-linear · fazer

### Etapa 3 — Memória de curto prazo · S04
- [ ] 11-llm-engineering/05-context-engineering — Context Engineering: Windows, Budgets, Memory, and Retrieval · agentes · fazer
- [ ] mentoria: S04 Memória de curto prazo — triagem dos 10 blocos + blocos 1–4: recorte do request, thread ID, sessão × thread, janela e compactação · mentoria · triagem + blocos 1–4
- [ ] 01-math-foundations/12-tensor-operations — Tensor Operations · algebra-linear · fazer
- [ ] 14-agent-engineering/13-langgraph-stateful-graphs — Stateful Graph Orchestration — Durable Execution and Checkpoints · agentes · confirmar
- [ ] mentoria: S04 Memória de curto prazo — blocos 5–10: checkpointer, reducer × checkpointer, persistência, AG-UI, fork/rewind, backend · mentoria · blocos 5–10
- [ ] 01-math-foundations/10-dimensionality-reduction — Dimensionality Reduction · algebra-linear · fazer

### Etapa 4 — Memória de longo prazo · S05
- [ ] mentoria: S05 Memória de longo prazo — triagem dos 9 blocos + blocos 1–5: checkpointer × longo prazo, modelo de dados, tipos de memória, case, fora do caminho crítico · mentoria · triagem + blocos 1–5
- [ ] 01-math-foundations/11-singular-value-decomposition — Singular Value Decomposition · algebra-linear · fazer
- [ ] 14-agent-engineering/07-memory-virtual-context-memgpt — Agent Memory — Virtual Context and Memory Paging · agentes · confirmar
- [ ] mentoria: S05 Memória de longo prazo — blocos 6–9: contexto reconstruído, transcript store, observabilidade, memória evolutiva e segurança · mentoria · blocos 6–9
- [ ] 14-agent-engineering/24-agent-observability-platforms — Agent Observability: Langfuse, Phoenix, Opik · producao · fazer
- [ ] 01-math-foundations/04-calculus-for-ml — Calculus for Machine Learning · calculo-otimizacao · fazer

### Etapa 5 — RAG ingestão · S06
- [ ] 01-math-foundations/14-norms-and-distances — Norms and Distances · algebra-linear · fazer
- [ ] 11-llm-engineering/04-embeddings — Embeddings & Vector Representations · representacao-texto · confirmar
- [ ] 05-nlp-foundations-to-advanced/14-information-retrieval-search — Information Retrieval and Search · rag · fazer
- [ ] mentoria: S06 RAG - Ingestão — triagem dos 10 blocos + blocos 1–5: panorama, parsing, chunking, enriquecimento, embeddings · mentoria · triagem + blocos 1–5
- [ ] 05-nlp-foundations-to-advanced/22-embedding-models-deep-dive — Embedding Models — The 2026 Deep Dive · representacao-texto · confirmar
- [ ] mentoria: S06 RAG - Ingestão — blocos 6–10: anatomia do chunk, pipeline e reindexação, GraphRAG, multimodal, Text-to-SQL · mentoria · blocos 6–10
- [ ] 11-llm-engineering/06-rag — RAG (Retrieval-Augmented Generation) · rag · confirmar
- [ ] 01-math-foundations/05-chain-rule-and-autodiff — Chain Rule & Automatic Differentiation · calculo-otimizacao · fazer

### Etapa 6 — RAG retrieval · S07
- [ ] mentoria: S07 RAG - Retrieval — triagem dos 10 blocos + blocos 1–4: busca exata × aproximada, HNSW (inserção, camadas, pgvector), case 64 → 32 · mentoria · triagem + blocos 1–4
- [ ] 11-llm-engineering/07-advanced-rag — Advanced RAG (Chunking, Reranking, Hybrid Search) · rag · fazer
- [ ] mentoria: S07 RAG - Retrieval — blocos 5–7: top-k e threshold, reranking, recall@k · mentoria · blocos 5–7
- [ ] 02-ml-fundamentals/09-model-evaluation — Model Evaluation · ml-classico · fazer
- [ ] mentoria: S07 RAG - Retrieval — blocos 8–10: classificador devo responder, tool × injeção, progressive disclosure · mentoria · blocos 8–10
- [ ] 01-math-foundations/08-optimization — Optimization · calculo-otimizacao · fazer

### Etapa 7 — Eval com estatística (+ a semana de evals da mentoria, quando chegar)
- [ ] 01-math-foundations/07-bayes-theorem — Bayes' Theorem · probabilidade · fazer
- [ ] 01-math-foundations/15-statistics-for-ml — Statistics for Machine Learning · probabilidade · fazer
- [ ] 11-llm-engineering/10-evaluation — Evaluation & Testing LLM Applications · avaliacao · fazer
- [ ] 17-infrastructure-and-production/21-ab-testing-llm-features — A/B Testing LLM Features — GrowthBook, Statsig, and the Vibes Problem · avaliacao · fazer

### Depois — resto da fila do nivelamento, na ordem original
- [ ] 11-llm-engineering/01-prompt-engineering — Prompt Engineering: Techniques & Patterns · prompting · confirmar
- [ ] 13-tools-and-protocols/03-parallel-and-streaming-tool-calls — Parallel Tool Calls and Streaming with Tools · tools-mcp · fazer
- [ ] 13-tools-and-protocols/06-mcp-fundamentals — MCP Fundamentals: Stateless Requests and JSON-RPC · tools-mcp · fazer
- [ ] 01-math-foundations/13-numerical-stability — Numerical Stability · calculo-otimizacao · fazer
- [ ] 01-math-foundations/18-convex-optimization — Convex Optimization · calculo-otimizacao · fazer
- [ ] 13-tools-and-protocols/07-building-an-mcp-server — Building an MCP Server: Stateless Python and TypeScript · tools-mcp · fazer
- [ ] 01-math-foundations/09-information-theory — Information Theory · probabilidade · fazer
- [ ] 01-math-foundations/16-sampling-methods — Sampling Methods · probabilidade · fazer
- [ ] 13-tools-and-protocols/08-building-an-mcp-client — Building an MCP Client: Discovery, Routing, and Dual-Era Fallback · tools-mcp · fazer
- [ ] 02-ml-fundamentals/02-linear-regression — Linear Regression · ml-classico · fazer
- [ ] 02-ml-fundamentals/03-logistic-regression — Logistic Regression · ml-classico · fazer
- [ ] 13-tools-and-protocols/09-mcp-transports — MCP Transports: stdio and Stateless Streamable HTTP · tools-mcp · fazer
- [ ] 02-ml-fundamentals/10-bias-variance — Bias-Variance Tradeoff · ml-classico · fazer
- [ ] 13-tools-and-protocols/10-mcp-resources-and-prompts — MCP Resources and Prompts: Addressable Context for Stateless Servers · tools-mcp · fazer
- [ ] 02-ml-fundamentals/04-decision-trees — Decision Trees and Random Forests · ml-classico · fazer
- [ ] 02-ml-fundamentals/11-ensemble-methods — Ensemble Methods · ml-classico · fazer
- [ ] 13-tools-and-protocols/15-mcp-security-tool-poisoning — MCP Security: Poisoned Metadata, Routing, and MRTR State · tools-mcp · fazer
- [ ] 02-ml-fundamentals/17-imbalanced-data — Handling Imbalanced Data · ml-classico · fazer
- [ ] 02-ml-fundamentals/12-hyperparameter-tuning — Hyperparameter Tuning · ml-classico · fazer
- [ ] 14-agent-engineering/12-anthropic-workflow-patterns — Anthropic's Workflow Patterns: Simple Over Complex · agentes · confirmar
- [ ] 03-deep-learning-core/01-the-perceptron — The Perceptron · redes-neurais · fazer
- [ ] 03-deep-learning-core/02-multi-layer-networks — Multi-Layer Networks and Forward Pass · redes-neurais · fazer
- [ ] 14-agent-engineering/02-rewoo-plan-and-execute — ReWOO and Plan-and-Execute: Decoupled Planning · agentes · fazer
- [ ] 03-deep-learning-core/03-backpropagation — Backpropagation from Scratch · redes-neurais · fazer
- [ ] 03-deep-learning-core/04-activation-functions — Activation Functions · redes-neurais · fazer
- [ ] 14-agent-engineering/03-reflexion-verbal-rl — Reflexion: Verbal Reinforcement Learning · agentes · fazer
- [ ] 03-deep-learning-core/05-loss-functions — Loss Functions · redes-neurais · fazer
- [ ] 03-deep-learning-core/06-optimizers — Optimizers · redes-neurais · fazer
- [ ] 03-deep-learning-core/07-regularization — Regularization · redes-neurais · fazer
- [ ] 03-deep-learning-core/08-weight-initialization — Weight Initialization and Training Stability · redes-neurais · fazer
- [ ] 03-deep-learning-core/09-learning-rate-schedules — Learning Rate Schedules and Warmup · redes-neurais · fazer
- [ ] 03-deep-learning-core/13-debugging-neural-networks — Debugging Neural Networks · redes-neurais · fazer
- [ ] 14-agent-engineering/28-orchestration-patterns — Orchestration Patterns: Supervisor, Swarm, Hierarchical · agentes · fazer
- [ ] 05-nlp-foundations-to-advanced/19-subword-tokenization — Subword Tokenization — BPE, WordPiece, Unigram, SentencePiece · representacao-texto · confirmar
- [ ] 10-llms-from-scratch/01-tokenizers — Tokenizers: BPE, WordPiece, SentencePiece · representacao-texto · fazer
- [ ] 14-agent-engineering/30-eval-driven-agent-development — Eval-Driven Agent Development · agentes · fazer
- [ ] 14-agent-engineering/29-production-runtimes — Production Runtimes: Queue, Event, Cron · agentes · fazer
- [ ] 05-nlp-foundations-to-advanced/10-attention-mechanism — Attention Mechanism — The Breakthrough · atencao-transformers · fazer
- [ ] 07-transformers-deep-dive/01-why-transformers — Why Transformers — The Problems with RNNs · atencao-transformers · fazer
- [ ] 07-transformers-deep-dive/02-self-attention-from-scratch — Self-Attention from Scratch · atencao-transformers · fazer
- [ ] 07-transformers-deep-dive/03-multi-head-attention — Multi-Head Attention · atencao-transformers · fazer
- [ ] 05-nlp-foundations-to-advanced/27-llm-evaluation-frameworks — LLM Evaluation — RAGAS, DeepEval, G-Eval · avaliacao · confirmar
- [ ] 07-transformers-deep-dive/04-positional-encoding — Positional Encoding — Sinusoidal, RoPE, ALiBi · atencao-transformers · fazer
- [ ] 07-transformers-deep-dive/05-full-transformer — The Full Transformer — Encoder + Decoder · atencao-transformers · fazer
- [ ] 14-agent-engineering/19-benchmarks-swebench-gaia — Benchmarks: SWE-bench, GAIA, AgentBench · avaliacao · confirmar
- [ ] 07-transformers-deep-dive/07-gpt-causal-language-modeling — GPT — Causal Language Modeling · atencao-transformers · fazer
- [ ] 07-transformers-deep-dive/06-bert-masked-language-modeling — BERT — Masked Language Modeling · atencao-transformers · fazer
- [ ] 11-llm-engineering/11-caching-cost — Caching, Rate Limiting & Cost Optimization · producao · confirmar
- [ ] 07-transformers-deep-dive/12-kv-cache-flash-attention — KV Cache, Flash Attention & Inference Optimization · atencao-transformers · fazer
- [ ] 07-transformers-deep-dive/11-mixture-of-experts — Mixture of Experts (MoE) · atencao-transformers · fazer
- [ ] 11-llm-engineering/12-guardrails — Guardrails, Safety & Content Filtering · producao · confirmar
- [ ] 07-transformers-deep-dive/13-scaling-laws — Scaling Laws · atencao-transformers · fazer
- [ ] 10-llms-from-scratch/03-data-pipelines — Data Pipelines for Pre-Training · treino-llms · confirmar
- [ ] 11-llm-engineering/13-production-app — Building a Production LLM Application · producao · confirmar
- [ ] 10-llms-from-scratch/04-pre-training-mini-gpt — Pre-Training a Mini GPT (124M Parameters) · treino-llms · confirmar
- [ ] 10-llms-from-scratch/07-rlhf — RLHF: Reward Model + PPO · treino-llms · confirmar
- [ ] 17-infrastructure-and-production/01-managed-llm-platforms — Managed LLM Platforms — Bedrock, Vertex AI, Azure OpenAI · producao · confirmar
- [ ] 10-llms-from-scratch/08-dpo — DPO: Direct Preference Optimization · treino-llms · confirmar
- [ ] 11-llm-engineering/08-fine-tuning-lora — Fine-Tuning with LoRA & QLoRA · treino-llms · confirmar
- [ ] 17-infrastructure-and-production/13-llm-observability — LLM Observability Stack Selection · producao · confirmar
- [ ] 10-llms-from-scratch/10-evaluation — Evaluation: Benchmarks, Evals, LM Harness · treino-llms · fazer
- [ ] 14-agent-engineering/23-otel-genai-conventions — OpenTelemetry GenAI Semantic Conventions · producao · fazer
- [ ] 17-infrastructure-and-production/16-model-routing — Model Routing as a Cost-Reduction Primitive · producao · confirmar
- [ ] 17-infrastructure-and-production/19-ai-gateways — AI Gateways — LiteLLM, Portkey, Kong AI Gateway, Bifrost · producao · confirmar
- [ ] 17-infrastructure-and-production/22-load-testing-llm-apis — Load Testing LLM APIs — Why k6 and Locust Lie · producao · fazer
- [ ] 17-infrastructure-and-production/24-chaos-engineering-llm — Chaos Engineering for LLM Production · producao · fazer
- [ ] 17-infrastructure-and-production/23-sre-for-ai — SRE for AI — Multi-Agent Incident Response, Runbooks, Predictive Detection · producao · fazer
- [ ] 18-ethics-safety-alignment/12-red-teaming-pair-automated-attacks — Red-Teaming: PAIR and Automated Attacks · seguranca · fazer
- [ ] 18-ethics-safety-alignment/02-reward-hacking-goodhart — Reward Hacking and Goodhart's Law · seguranca · fazer
- [ ] 17-infrastructure-and-production/04-vllm-serving-internals — Serving Engine Internals — PagedAttention, Continuous Batching, Chunked Prefill · producao · fazer

## Path
| Phase | Name | Status | Est. hours |
|-------|------|--------|------------|
| 00 | Setup & Tooling | Out of scope | — |
| 01 | Math Foundations | Do | 23.2 |
| 02 | ML Fundamentals | Do | 12.2 |
| 03 | Deep Learning Core | Do | 14.0 |
| 04 | Computer Vision | Out of scope | — |
| 05 | NLP Foundations to Advanced | Do | 3.8 |
| 06 | Speech & Audio | Out of scope | — |
| 07 | Transformers Deep Dive | Do | 10.2 |
| 08 | Generative AI | Out of scope | — |
| 09 | Reinforcement Learning | Out of scope | — |
| 10 | LLMs from Scratch | Do | 4.0 |
| 11 | LLM Engineering | Do | 2.8 |
| 12 | Multimodal AI | Out of scope | — |
| 13 | Tools & Protocols | Do | 10.3 |
| 14 | Agent Engineering | Do | 12.0 |
| 15 | Autonomous Systems | Out of scope | — |
| 16 | Multi-Agent & Swarms | Out of scope | — |
| 17 | Infrastructure & Production | Do | 6.5 |
| 18 | Ethics, Safety & Alignment | Do | 2.2 |
| 19 | Capstone Projects | Out of scope | — |

## Progress log
| Date | Lesson | Quiz | Note |
|------|--------|------|------|

## Review queue
