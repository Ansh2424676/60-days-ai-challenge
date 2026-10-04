# Day 42 — Design Your AI Product System Architecture

## ResearchMate AI

ResearchMate AI is an evidence-grounded technical research assistant
designed to help users research technical topics using retrieval,
external sources, LLM synthesis and citation validation.

---

## Day 42 Objective

The goal of Day 42 was to design the complete system architecture
before continuing implementation.

The architecture defines:

- System components
- Data flow
- External dependencies
- Storage layers
- API contracts
- Technology decisions
- Architecture trade-offs
- Component dependencies
- Future implementation order

---

# System Architecture

```text
User
  ↓
Next.js Frontend
  ↓
FastAPI API
  ↓
Research Workflow
  ↓
Query Planning
  ↓
Query Decomposition
  ↓
Retrieval
  ├── FAISS Knowledge Base
  └── External Sources
  ↓
Evidence Filtering
  ↓
OpenAI LLM
  ↓
Citation & Grounding Validation
  ↓
Research Report
  ↓
Next.js UI