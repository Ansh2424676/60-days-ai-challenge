# ResearchMate AI — Component Dependency Map

## 1. Purpose

This document defines the dependency order of ResearchMate AI
components and establishes the implementation sequence for Days 43–53.

A component should only be tested after all of its required
dependencies are available and working.

---

# 2. Dependency Overview

```text
Project Configuration
        ↓
FastAPI Backend
        ↓
Data Models / Validation
        ↓
Knowledge Base
        ↓
Document Processing
        ↓
Embeddings
        ↓
FAISS Retrieval
        ↓
Query Planning
        ↓
Query Decomposition
        ↓
Evidence Filtering
        ↓
LLM Synthesis
        ↓
Citation / Grounding Validation
        ↓
Research API
        ↓
Frontend Integration
        ↓
Caching / Performance
        ↓
Evaluation
        ↓
Production Validation