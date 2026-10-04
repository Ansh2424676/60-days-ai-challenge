# ResearchMate AI — Architecture Trade-offs

Architecture decisions always involve trade-offs. ResearchMate AI
prioritizes simplicity, cost efficiency, observability and sufficient
performance for its current portfolio-scale workload.

---

# Trade-off 1 — FAISS vs Managed Vector Database

## Decision

Use FAISS as the vector search engine.

## What We Gain

- Simple local development
- No hosted vector database cost
- Fast similarity search
- Easy integration with the existing Python RAG pipeline
- Full control over the vector index

## What We Give Up

We give up:

- Built-in horizontal scaling
- Managed availability
- Distributed vector search
- Easier multi-instance synchronization

## Why This Is Acceptable

The current knowledge base is small enough that FAISS can provide
adequate retrieval performance without introducing the operational
complexity of a managed vector database.

## Future Migration Path

If the knowledge base or traffic grows substantially, FAISS can be
replaced with a managed vector database while keeping the retrieval
interface unchanged.

---

# Trade-off 2 — SQLite vs PostgreSQL

## Decision

Use SQLite for feedback and lightweight application persistence.

## What We Gain

- Zero database-server management
- Very low infrastructure cost
- Simple local development
- Easy backup and portability
- Sufficient for current feedback volume

## What We Give Up

We give up:

- Stronger concurrent write handling
- Horizontal database scaling
- Advanced production database capabilities
- Built-in managed availability

## Why This Is Acceptable

ResearchMate AI is currently a portfolio-scale application with
moderate data volume, so PostgreSQL would add operational complexity
without providing significant value at the current scale.

## Future Migration Path

If concurrent users and persistent data volume increase, the
application can migrate to PostgreSQL while keeping the application
data-access layer separate from the API layer.

---

# Trade-off 3 — Synchronous Research API vs Asynchronous Job Queue

## Decision

Use a synchronous request/response model for the primary
`POST /research` workflow.

## What We Gain

- Simpler API design
- Simpler frontend implementation
- Easier local debugging
- Immediate response to the user
- Fewer infrastructure components

## What We Give Up

We give up:

- Better handling of very long research jobs
- Independent worker scaling
- Natural background processing
- Queue-based retry management

## Why This Is Acceptable

The current product targets research responses that normally complete
within approximately 60 seconds, making a synchronous workflow
acceptable for the current product scope.

## Future Migration Path

If research jobs become significantly longer, the architecture can
move to:

POST /research
       ↓
Job Queue
       ↓
Background Worker
       ↓
Research Pipeline
       ↓
Result Store
       ↓
Frontend Polling / WebSocket

---

# Additional Architectural Principle

These decisions intentionally optimize for:

1. Low infrastructure cost
2. Fast development
3. Easy debugging
4. Sufficient performance
5. Simple deployment

The architecture keeps important interfaces modular so that
individual infrastructure components can be replaced later without
rewriting the complete product.

---

# Decision Summary

| Decision | Chosen | Given Up | Why Acceptable |
|---|---|---|---|
| Vector Search | FAISS | Managed scaling | Current KB is manageable |
| Database | SQLite | High concurrency | Moderate data volume |
| Research Execution | Synchronous API | Background workers | Target response ≤60 sec |