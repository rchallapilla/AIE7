## 📊 Production RAG with Cashing + Guardrails Pipeline

This diagram shows how a user query flows through retrieval, caching, generation, and safety checks in this project.
- **Embedding cache**: persisted under `./cache/embeddings`.
- **LLM cache**: configurable in memory or SQLite via `setup_llm_cache(...)`.
- **Guardrails**: post-generation validation before returning a response.



## 📊 Production RAG + Guardrails Pipeline (Implemented Flow)

```mermaid
graph TD
    %% User Input
    A["👤 User Query"] --> B["🧠 LangGraph Agent"]

    %% Embedding + RAG Flow
    B --> C["🔡 Generate Query Embeddings"]
    C --> D["💾 Embedding Cache<br/>(LocalFileStore: ./cache/embeddings)"]
    D --> E["📚 Vector Search<br/>(Qdrant In-Memory)"]
    E --> F["🧩 Combine Context + Query"]

    %% LLM Call + Guardrails
    F --> G["🤖 OpenAI LLM Call<br/>(LangGraph Tools)"]
    G --> H["🛡️ Guardrails Check"]

    %% Guardrails Decision
    H --> I{"✅ Passed All Checks?"}
    I -->|Yes| J["📤 Return Final Response"]
    I -->|No| K["⚠️ Return Guard Alert / Sanitized Output"]

    %% Styling
    style A fill:#2e7d32,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style B fill:#1e88e5,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style C fill:#6a1b9a,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style D fill:#6a1b9a,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style E fill:#6a1b9a,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style F fill:#6a1b9a,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style G fill:#3949ab,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style H fill:#e65100,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style I fill:#e65100,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style J fill:#2e7d32,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style K fill:#c62828,stroke:#ffffff,stroke-width:3px,color:#ffffff


```

### Implementation notes

- **Embedding caching**: `langgraph_agent_lib/caching.py` → `CacheBackedEmbeddings` uses `LocalFileStore` under `./cache/embeddings` and namespaces by model hash.
- **LLM caching**: `langgraph_agent_lib/caching.py` → `setup_llm_cache("memory"|"sqlite", cache_path)`; SQLite default is `./cache/llm_cache.db`.
- **Model config**: `langgraph_agent_lib/models.py` → `get_openai_model(...)` (defaults to `gpt-4.1-mini`).
- **Performance tests**: `cache_performance_test.py` and `activity1_cache_testing_notebook.py` measure speedup and hit rates for embeddings, LLM, and end-to-end RAG.