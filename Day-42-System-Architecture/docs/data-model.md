# ResearchMate AI — Data Model

## 1. Product Overview

ResearchMate AI is an evidence-grounded technical research assistant.

The system accepts a research question, retrieves relevant evidence,
uses an LLM to synthesize findings, validates citations and returns
a structured research report.

---

# 2. Core Data Entities

## 2.1 Research Request

Represents a research request submitted by a user.

| Field | Type | Required | Description |
|---|---|---|---|
| request_id | UUID/String | Yes | Unique research request ID |
| session_id | String | Yes | User session identifier |
| topic | Text | Yes | Research question |
| status | String | Yes | processing/completed/failed |
| created_at | Datetime | Yes | Request creation time |
| completed_at | Datetime | No | Completion timestamp |
| error_message | Text | No | Failure reason |

### Example

```json
{
  "request_id": "req_001",
  "session_id": "session_123",
  "topic": "How does Retrieval Augmented Generation work?",
  "status": "completed",
  "created_at": "2026-10-04T17:00:00",
  "completed_at": "2026-10-04T17:00:25"
}