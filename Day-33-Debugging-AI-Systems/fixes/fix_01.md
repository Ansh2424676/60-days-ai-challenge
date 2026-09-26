# Fix 01 — Retrieval Failure

## Problem

The RAG system may fail when the query does not match any document in the knowledge base.

This can cause the system to generate an answer without relevant retrieved context.

## Root Cause

The retrieval stage returned zero relevant documents.

## Detection

The retrieval isolation test checks:

- Whether retrieval succeeded
- Number of retrieved documents
- Retrieved document details

## Fix

The retrieval component should:

1. Validate the query.
2. Search the available documents.
3. Return only relevant documents.
4. Log the number of candidates and results.
5. Return an empty result when no relevant document exists.

## Validation

Run:

```powershell
pytest tests/test_debugging.py -v