# Day 45 — Backend Infrastructure for ResearchMate AI

## ABTalks 60-Day AI Engineering Challenge

ResearchMate AI is an evidence-grounded technical research assistant.

Day 45 focuses on converting the MVP into a structured backend system with
session management, authentication, rate limiting, logging, feedback
collection and API verification.

---

## Features

- FastAPI backend
- UUID-based session management
- Per-session conversation history
- SQLite request/response logging
- 20 requests per session per hour
- HTTP 429 rate-limit protection
- API key authentication using `x-api-key`
- Product-specific feedback collection
- Pydantic request/response validation
- Health check endpoint
- Automated API tests
- cURL verification

---

## Architecture

```text
Client
   |
   v
x-api-key Authentication
   |
   v
Rate Limiter
20 requests/hour/session
   |
   v
Session Manager
   |
   v
ResearchMate AI Core Loop
   |
   +--------> Conversation History
   |
   +--------> SQLite Request Logging
   |
   +--------> Feedback Storage
   |
   v
API Response