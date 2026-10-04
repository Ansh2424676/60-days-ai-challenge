# ResearchMate AI — API Contract

## API Base

Production:

https://<railway-backend-url>

All API requests and responses use JSON unless otherwise specified.

---

# 1. POST /research

## Purpose

Submit a technical research question and generate an
evidence-grounded research report.

## HTTP Method

POST

## Path

/research

## Request Headers

Content-Type: application/json

## Request Body

```json
{
  "topic": "How does Retrieval Augmented Generation work?"
}