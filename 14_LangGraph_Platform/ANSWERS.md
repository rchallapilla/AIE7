## Short Answers

### 1) chunk_overlap in RecursiveCharacterTextSplitter
- Purpose: Preserve cross-chunk context by duplicating a tail of tokens from the previous chunk into the next.
- Trade-offs:
  - Higher overlap: better recall/semantic continuity; more tokens, slower ingestion and higher embedding/storage cost; may increase redundancy and reduce precision if too high.
  - Lower overlap: faster/cheaper; risk of splitting facts across chunks and missing context, potentially hurting recall and answer coherence.

### 2) Retriever search k and RAGAS metrics
- Increasing k generally increases Context Recall (more chances the gold evidence is retrieved) but can reduce Context Precision (more irrelevant text). Decreasing k often improves precision while risking recall drop. The best k balances sufficient recall with minimal distractors for the generator.

### 3) agent vs agent_helpful graphs
- Location of helpfulness evaluator: a dedicated `helpfulness` node that runs when the model does not request tool calls.
- Routing condition:
  - If the agent’s last message has tool_calls → go to `action` (ToolNode) and loop back to `agent`.
  - If no tool_calls → run `helpfulness`; return to `agent` only if not helpful (`N`), terminate if helpful (`Y`) or if loop-limit is reached.


