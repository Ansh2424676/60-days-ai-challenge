# Day 49 — Frontend Integration Checklist

## A. Locate the Existing Frontend
- [ ] Find the actual Next.js project directory.
- [ ] Inspect package.json and app/page.tsx.
- [ ] Identify the current API base URL and request payload.
- [ ] Preserve existing working UI before editing.

## B. Verify Backend Contracts
- [ ] Inspect the streaming endpoint and request schema.
- [ ] Confirm whether streaming uses NDJSON, SSE, or another format.
- [ ] Inspect source metadata fields and citation scores.
- [ ] Inspect the feedback endpoint and required payload.
- [ ] Confirm structured error response fields.

## C. Integrate Components
- [ ] Loading skeleton before the first token.
- [ ] Typing indicator while tokens arrive.
- [ ] Completed answer and metadata.
- [ ] Accessible error message with retry action.
- [ ] Expandable source citations.
- [ ] Feedback buttons connected to the real API.

## D. Browser Verification
- [ ] Submit a research question.
- [ ] Observe incremental tokens before completion.
- [ ] Confirm source citations match backend metadata.
- [ ] Submit feedback and verify the server response.
- [ ] Test one recoverable API error.
- [ ] Check desktop and mobile layouts.

## E. Usability Observation
- [ ] Observe a non-developer for 15 minutes.
- [ ] Record actual confusion and friction.
- [ ] Fix the top three observed issues.
- [ ] Retest the changed interactions.

## Completion Rule
Do not mark a checklist item complete without implementation or evidence.
