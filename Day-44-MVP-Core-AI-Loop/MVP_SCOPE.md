# Day 44 — MVP Scope Decision

## Product

ResearchMate AI — Evidence-Grounded Technical Research Assistant

## Core Value Proposition

ResearchMate AI takes a technical question, retrieves relevant evidence,
and generates a grounded answer with source references.

---

# Single Most Important Function

The single most important function of ResearchMate AI is:

> Take a technical question, retrieve relevant evidence, and generate a
> grounded answer with source references.

This function represents the core value of the product. Without this
function, ResearchMate AI has no meaningful value proposition.

---

# Feature Scope

| # | Feature | Decision | Reason |
|---|---|---|---|
| 1 | Technical question input | MVP | Required for users to interact with the system |
| 2 | Relevant document retrieval | MVP | Provides evidence for the AI response |
| 3 | AI answer generation | MVP | This is the primary product value |
| 4 | Source references | MVP | Allows users to verify the generated answer |
| 5 | RAG-based context injection | MVP | Helps generate evidence-grounded responses |
| 6 | FastAPI POST /ask endpoint | MVP | Exposes the core capability through an API |
| 7 | Pydantic input validation | MVP | Prevents invalid requests |
| 8 | Structured error responses | MVP | Makes API failures predictable |
| 9 | Basic relevance filtering | MVP | Prevents irrelevant context from being used |
| 10 | Evaluation against 10 queries | MVP | Validates whether the core loop works |
| 11 | Conversation memory | Post-MVP | Not required to prove the core research value |
| 12 | Redis caching | Post-MVP | Performance optimization can be added later |
| 13 | User authentication | Post-MVP | Authentication is unnecessary for initial MVP validation |
| 14 | Next.js frontend | Post-MVP | The backend core capability should be validated first |
| 15 | Streaming responses | Post-MVP | Improves UX but is not required for MVP validation |
| 16 | Web search integration | Post-MVP | Existing knowledge-base retrieval is sufficient for initial validation |
| 17 | User feedback system | Post-MVP | Feedback becomes useful after real users test the MVP |
| 18 | Research history | Post-MVP | Historical conversations are not required for the core workflow |
| 19 | Advanced query decomposition | Post-MVP | Adds complexity before basic research queries are validated |
| 20 | Multi-agent research workflow | Post-MVP | The MVP should prove value with a single AI loop |
| 21 | Advanced citation verification | Post-MVP | Basic source references are sufficient initially |
| 22 | Analytics dashboard | Post-MVP | Analytics does not directly provide the core user value |
| 23 | Role-based access control | Post-MVP | Not necessary for initial product validation |
| 24 | Advanced production monitoring | Post-MVP | Reliability infrastructure can be expanded after MVP validation |

---

# MVP Features

The MVP contains only the following capabilities:

1. Accept a technical question.
2. Retrieve relevant evidence.
3. Generate an AI answer using the evidence.
4. Return source references.
5. Expose the capability through `core_ai_loop(user_input)`.
6. Provide a FastAPI `POST /ask` endpoint.
7. Validate input using Pydantic.
8. Return structured errors.
9. Evaluate the system using 10 predefined queries.

---

# Explicitly Excluded From MVP

## 1. Conversation Memory

Conversation memory is excluded because the MVP only needs to prove that
the system can answer an individual research question reliably.

## 2. Redis Caching

Caching improves latency and scalability but does not prove the core
research value.

## 3. User Authentication

Authentication is unnecessary while validating the core product capability.

## 4. Next.js Frontend

The API should prove the core AI interaction before additional UI work.

## 5. Streaming Responses

Streaming can improve perceived latency but is not necessary for the first
working version.

## 6. Web Search

The existing knowledge base provides enough evidence to validate the MVP.

## 7. Feedback System

Feedback collection should be added after the MVP has been tested by users.

## 8. Research History

Persistent history is useful later but is not necessary for answering the
current research question.

## 9. Advanced Query Decomposition

Complex query planning adds engineering complexity before the basic AI loop
has been validated.

## 10. Multi-Agent Architecture

Multiple agents are unnecessary for proving the basic research assistant
value proposition.

## 11. Advanced Citation Verification

The MVP will return available source references without implementing a
separate citation-verification subsystem.

## 12. Analytics Dashboard

Analytics will be added later when there is enough real usage data to
analyze.

---

# MVP Success Criteria

The MVP will be considered successful if:

- `core_ai_loop(user_input)` accepts a technical question.
- Relevant context is retrieved.
- The AI generates a useful and grounded answer.
- Source references are returned.
- All 10 Day 41 example queries can be evaluated.
- The FastAPI `/ask` endpoint returns a valid response.
- Invalid requests return structured errors.
- A curl request successfully demonstrates the working API.

---

# Scope Decision

The MVP deliberately focuses on one question:

> Can ResearchMate AI take a technical question, retrieve useful evidence,
> and produce a reliable answer with source references?

Everything that does not directly help answer this question has been
classified as Post-MVP.

This prevents scope creep and keeps the engineering effort focused on
shipping and validating the core product value.