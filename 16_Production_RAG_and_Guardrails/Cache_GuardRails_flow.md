### RAG + Guardrails + Caching flow

This diagram shows how a user query flows through retrieval, caching, generation, and safety checks in this project.
- **Embedding cache**: persisted under `./cache/embeddings`.
- **LLM cache**: configurable in memory or SQLite via `setup_llm_cache(...)`.
- **Guardrails**: post-generation validation before returning a response.

```mermaid
flowchart TD
    A[User Query] --> B{Check LLM cache}
    B -- Cache hit --> R1[Return cached LLM response]
    B -- Cache miss --> C[Generate embeddings]

    C --> C1[Embedding cache at ./cache/embeddings]
    C --> D[Retrieve context from Vector DB (Qdrant)]
    D --> E[Combine context + query]
    E --> F[Call LLM/tools (LangGraph Agent)]

    F --> G[Guardrails]
    G --> H{Guardrails check}
    H -- pass --> I[Return final response]
    H -- fail --> J[Return guard alert or sanitized output]

    B --> B1[LLM cache (memory or SQLite)]
```

### Implementation notes

- **Embedding caching**: `langgraph_agent_lib/caching.py` → `CacheBackedEmbeddings` uses `LocalFileStore` under `./cache/embeddings` and namespaces by model hash.
- **LLM caching**: `langgraph_agent_lib/caching.py` → `setup_llm_cache("memory"|"sqlite", cache_path)`; SQLite default is `./cache/llm_cache.db`.
- **Model config**: `langgraph_agent_lib/models.py` → `get_openai_model(...)` (defaults to `gpt-4.1-mini`).
- **Performance tests**: `cache_performance_test.py` and `activity1_cache_testing_notebook.py` measure speedup and hit rates for embeddings, LLM, and end-to-end RAG.