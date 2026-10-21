# Day 57 — AI Engineering Technical Cheat Sheet
## 15 Concepts for Interview Revision

1. **LLM:** A language model that generates responses from learned patterns and the input context.

2. **Prompt Engineering:** Writing clear instructions and supplying relevant context to guide model behavior.

3. **RAG:** Retrieves relevant external information and supplies it to a language model to help ground its answer.

4. **Embeddings:** Numerical representations of text used to compare semantic similarity.

5. **Chunking:** Splitting documents into smaller passages for retrieval. Chunk size and overlap affect relevance and context.

6. **Vector Search:** Finding passages whose embeddings are similar to the query embedding.

7. **FAISS:** A library for efficient similarity search. The application developer manages persistence, deployment, and surrounding infrastructure.

8. **Reranking:** Reordering retrieved passages so the most relevant evidence appears first.

9. **Hallucination:** An unsupported or incorrect model answer. Grounding, validation, and abstention help reduce the risk.

10. **Evaluation:** Testing an AI system against representative examples using defined quality and safety criteria.

11. **Recall@k:** Measures whether relevant items appear among the top-k retrieved results.

12. **FastAPI:** A Python framework for building APIs with request validation and automatic API documentation.

13. **Caching:** Reusing suitable previous results to reduce latency and cost. Cache invalidation and privacy must be considered.

14. **Latency and Throughput:** Latency measures response time; throughput measures how much work a system completes over time.

15. **Monitoring and Guardrails:** Monitoring tracks errors, latency, cost, and quality. Guardrails help enforce validation, safety, and access rules.

## Interview Answer Framework
Problem -> Approach -> Trade-offs -> Evaluation -> Result

Explain the problem, your technical choices, alternatives, how you tested the solution, and the evidence for the result.

Never invent performance metrics or claim features that have not been verified.
