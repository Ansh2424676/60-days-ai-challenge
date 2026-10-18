# Fix 02 — Generation Failure

## Problem

The generation stage may fail when the retrieved context is empty or insufficient.

## Root Cause

The answer generation step depends on the documents returned by retrieval.

If no relevant documents are available, the system must not create unsupported information.

## Detection

The generation isolation test checks:

- Whether answer generation succeeds
- Whether retrieved context is available
- Number of context documents
- Generated answer

## Fix

The generation component should:

1. Receive retrieved documents from the retrieval stage.
2. Use only the retrieved context.
3. Return a clear fallback response when no documents are available.
4. Avoid generating unsupported information.
5. Keep the generated answer traceable to the retrieved context.

## Validation

Run:

```powershell
pytest tests/test_debugging.py -v