# Day 39 — Product Iteration Based on Evidence

## Prioritised Failure List

| Priority | Failure | Evidence | Impact |
|---|---|---|---|
| 1 | Conversational context can be lost in longer conversations | Day 24 memory testing + Day 38 feedback review | High |
| 2 | Low-confidence retrieval can produce uncertain answers without warning | RAG retrieval behaviour + Day 29 evaluation | High |
| 3 | Users need clearer feedback mechanisms | Day 38 feedback system | Medium |

## Fix 1 — Seven-Turn Conversation Memory

File:
`Day-39-Product-Iteration/test_memory_7_turns.py`

Change:
Conversation memory window increased from 5 turns to 7 turns.

Root-cause hypothesis:
Longer conversations can lose earlier context when the memory window is too small. Increasing the window should preserve more context for follow-up questions and pronoun references.

Expected impact:
Better multi-turn context retention without changing the underlying model.

Validation:
7-turn memory test confirms that earlier conversation context remains available.

## Fix 2 — Low-Confidence Retrieval Feedback

File:
`Day-39-Product-Iteration/confidence_feedback.py`

Function:
`add_helpfulness_prompt()`

Change:
When the highest retrieval score is below 0.4, append:

"Is this answer helpful? Yes or No"

Root-cause hypothesis:
Users may not know when the retrieval system has weak evidence. An inline prompt makes low-confidence interactions explicit and creates an additional feedback signal.

Expected impact:
Better user awareness of uncertain answers and easier identification of retrieval failures.

Validation:
Low-confidence test adds the prompt.
High-confidence test leaves the response unchanged.

## Evaluation

Memory test:
PASS — seven-turn context retained.

Low-confidence test:
PASS — prompt added below 0.4.

High-confidence regression test:
PASS — prompt not added above the threshold.

## Deployment

Target:
Railway — FastAPI backend
Vercel — Next.js frontend

Production verification:
Pending deployment verification.

## Feedback

Five new production feedback ratings should be collected after deployment to compare user experience against Day 38.
