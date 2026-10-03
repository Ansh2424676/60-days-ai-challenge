# Engineering Decisions

| Decision | Alternative Considered | Why I Chose This |
|---|---|---|
| FastAPI backend | Flask | FastAPI provides typed request/response models and is well suited to API-first AI services. |
| FAISS for vector retrieval | Hosted vector database | FAISS kept the retrieval layer lightweight and locally controllable during experimentation. |
| Dedicated evaluation suite | Manual testing only | Automated evaluation makes regressions measurable and repeatable. |
| Redis caching | No caching | Repeated AI/retrieval operations can increase latency and cost, so caching improves efficiency. |
| Circuit-breaker/reliability controls | Direct external API calls | External model APIs can fail or become unavailable, so failure handling prevents one dependency from taking down the complete workflow. |
