# ResearchMate AI — Technology Stack & Architecture Rationale

## 1. Product

ResearchMate AI is an evidence-grounded technical research assistant
that retrieves relevant information, validates evidence and generates
structured research reports.

---

# 2. Frontend

## Next.js

### Purpose

Interactive web interface for submitting research questions,
displaying research results, citations and collecting feedback.

### Why Next.js?

Next.js provides a structured React application with production-ready
routing and deployment support.

It fits this product because the frontend mainly requires:

- Interactive research forms
- Loading states
- Structured report rendering
- Citation display
- Feedback controls
- API integration

The frontend does not need a separate custom web server.

---

## Vercel

### Purpose

Frontend hosting and deployment.

### Why Vercel?

Vercel provides straightforward deployment for Next.js applications
and automatically handles production builds and frontend delivery.

This reduces infrastructure management for the frontend.

---

# 3. Backend

## FastAPI

### Purpose

REST API and research workflow orchestration.

### Why FastAPI?

FastAPI is suitable because ResearchMate AI is API-driven and requires:

- Typed request validation
- JSON APIs
- Async support
- Automatic OpenAPI documentation
- Low-overhead HTTP handling
- Clear endpoint contracts

FastAPI also integrates naturally with Python-based AI and retrieval
libraries used by the product.

---

## Railway

### Purpose

Backend hosting.

### Why Railway?

Railway provides a simple deployment environment for containerized
Python applications.

It allows the FastAPI service to be deployed without maintaining
complex cloud infrastructure.

---

# 4. Programming Language

## Python

### Purpose

Backend, AI workflow, retrieval, evaluation and testing.

### Why Python?

The AI ecosystem required by the product is primarily Python-based.

Python provides direct access to:

- LLM APIs
- FAISS
- NumPy
- Pandas
- Pytest
- AI evaluation tooling
- RAG libraries

Using Python across the backend and AI pipeline reduces integration
complexity.

---

# 5. LLM

## OpenAI API

### Purpose

Research synthesis and structured answer generation.

### Why OpenAI?

ResearchMate AI requires an LLM capable of:

- Understanding retrieved context
- Synthesizing multiple sources
- Producing structured responses
- Following grounding instructions
- Generating explanations

The LLM is accessed only through the backend so that API credentials
are never exposed to the browser.

---

# 6. Vector Search

## FAISS

### Purpose

Semantic retrieval from the internal knowledge base.

### Why FAISS?

The current knowledge base is small enough to operate without a
managed vector database.

FAISS provides:

- Fast similarity search
- Local vector indexing
- Low infrastructure overhead
- No hosted vector database cost

This makes it appropriate for the current portfolio-scale system.

The architecture can migrate to a managed vector database if the
knowledge base grows significantly.

---

# 7. Embeddings

## Sentence Transformers

### Purpose

Convert documents and research queries into numerical vectors.

### Why Sentence Transformers?

The retrieval pipeline needs semantic representations rather than
simple keyword matching.

Sentence-transformer embeddings allow semantically similar content
to be retrieved even when exact words differ.

---

# 8. Cache

## Redis

### Purpose

High-speed temporary storage and caching.

### Uses

- Embedding cache
- Semantic response cache
- Frequently requested results
- Short-lived workflow state

### Why Redis?

LLM calls and embedding generation can introduce latency and cost.

Redis allows frequently repeated operations to be served from memory,
reducing unnecessary external calls.

Redis is treated as a cache rather than the permanent source of truth.

---

# 9. Database

## SQLite

### Purpose

Store lightweight application data.

### Uses

- User feedback
- Feedback summaries
- Lightweight application records
- Evaluation metadata

### Why SQLite?

The current product is a portfolio-scale application with moderate
data volume.

SQLite provides:

- Zero database server management
- Simple local development
- SQL support
- Low operational cost

A managed PostgreSQL database can replace SQLite if concurrent
production traffic grows substantially.

---

# 10. Observability

## LangSmith

### Purpose

LLM and AI workflow tracing.

### Why LangSmith?

Traditional application logs cannot easily explain why an AI answer
was poor.

LangSmith allows tracing of:

- Prompts
- LLM calls
- Retrieval steps
- Intermediate outputs
- Latency
- Failures

This makes debugging AI-specific failures easier.

---

# 11. Testing

## Pytest

### Purpose

Automated testing.

### Test Areas

- API endpoints
- Retrieval
- Data validation
- Research workflow
- Failure handling
- Regression tests

### Why Pytest?

The backend is Python-based, so Pytest provides a simple and mature
testing framework that integrates directly with the application.

---

# 12. Evaluation

## Custom Python Evaluation Pipeline

### Purpose

Measure research quality.

### Metrics

- Answer quality
- Retrieval quality
- Citation coverage
- Grounding quality
- Latency
- Regression performance

### Why?

Traditional unit tests cannot determine whether an AI-generated
research answer is actually useful.

A dedicated evaluation layer allows AI quality to be measured
separately from code correctness.

---

# 13. Containerization

## Docker

### Purpose

Package the backend and its dependencies into a reproducible
environment.

### Why Docker?

AI applications often depend on multiple Python packages and system
dependencies.

Docker ensures that the same application environment can be used
during development and deployment.

---

# 14. Version Control

## Git

### Purpose

Track source-code and architecture changes.

### Why Git?

Architecture decisions and implementation changes need to remain
traceable during the multi-day development process.

---

## GitHub

### Purpose

Remote repository, collaboration and portfolio presentation.

### Why GitHub?

The challenge requires documenting the engineering process publicly,
while GitHub provides version history and a central location for
source code and architecture documentation.

---

# 15. Frontend ↔ Backend Communication

## REST + JSON

### Why?

The research workflow is naturally represented through HTTP API
requests and structured JSON responses.

Example:

Frontend
→ POST /research
→ FastAPI
→ Research Workflow
→ JSON Research Report
→ Frontend

This keeps frontend and backend responsibilities clearly separated.

---

# 16. External Dependencies

ResearchMate AI depends on external services for:

1. LLM generation
2. External research sources
3. Cloud deployment
4. Observability

These dependencies are isolated behind backend services so that
provider-specific implementation does not leak into the frontend.

---

# 17. Technology Decision Summary

| Layer | Technology | Main Reason |
|---|---|---|
| Frontend | Next.js | Structured interactive UI |
| Frontend Hosting | Vercel | Simple Next.js deployment |
| Backend | FastAPI | Typed, API-first Python backend |
| Language | Python | Strong AI/RAG ecosystem |
| LLM | OpenAI API | Research synthesis |
| Embeddings | Sentence Transformers | Semantic representation |
| Vector Search | FAISS | Fast local retrieval |
| Cache | Redis | Low-latency caching |
| Database | SQLite | Simple lightweight persistence |
| Observability | LangSmith | AI workflow tracing |
| Testing | Pytest | Python-native testing |
| Evaluation | Python | Custom AI quality measurement |
| Containerization | Docker | Reproducible deployment |
| Version Control | Git/GitHub | Versioning and portfolio |

---

# 18. Architecture Principle

The technology stack intentionally favors:

- Low operational complexity
- Low infrastructure cost
- Python-native AI tooling
- Observable AI workflows
- Replaceable infrastructure components
- Clear separation between frontend and backend

The architecture avoids introducing infrastructure that the current
product scale does not require.