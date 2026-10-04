# ResearchMate AI — System Architecture

## Product

ResearchMate AI is an evidence-grounded technical research assistant
designed for students, junior developers and early-career
AI/software engineers.

The system accepts a technical research question, retrieves relevant
evidence, filters the evidence, uses an LLM to synthesize findings,
validates citations and returns a structured research report.

---

# 1. Architecture Overview

The system follows this primary flow:

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
↓
Evidence Filtering
↓
LLM Synthesis
↓
Citation & Grounding Validation
↓
Research Report
↓
Next.js UI

---

# 2. System Components

## 2.1 User

The user submits a technical research question through the web
application.

Example:

"What is Retrieval Augmented Generation and how does it work?"

---

## 2.2 Next.js Frontend

### Responsibility

The frontend provides the user-facing interface.

It handles:

- Research question input
- Loading states
- Research report rendering
- Findings display
- Citation display
- Source links
- User feedback

### Deployment

Vercel

### Communication

The frontend communicates with the backend using REST APIs and JSON.

---

## 2.3 FastAPI Backend

### Responsibility

FastAPI acts as the main API gateway and application backend.

It handles:

- Request validation
- API routing
- Research workflow orchestration
- Error handling
- Health checks
- Feedback processing

### Main Endpoints

```text
POST /research
GET  /health
POST /feedback
GET  /feedback/summary