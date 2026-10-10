# Day 49 — Implementation Notes

## 1. Product UI
- Design a research-focused interface for ResearchMate AI.
- Keep research questions and generated answers easy to read.
- Make citations and source metadata easy to find.

## 2. Streaming
- Use Fetch API with ReadableStream.
- Parse the backend streaming format correctly.
- Handle partial chunks and incomplete lines.
- Process the final buffered data after the stream ends.

## 3. UI States
- Idle: show the research input.
- Loading: show a skeleton before the first token.
- Streaming: show the typing indicator and incoming response.
- Complete: show the full answer and metadata.
- Error: display a human-readable message and recovery action.

## 4. Citations
Each citation should display available metadata:
- Document name
- Relevant text excerpt
- Similarity score

Citation fields must match the actual backend response.

## 5. Feedback
- Add positive and negative feedback controls.
- Inspect the backend feedback endpoint and request schema.
- Submit feedback using the actual API contract.
- Show confirmation or failure states.

## 6. Error Handling
Handle the API error codes and HTTP statuses supported by the backend.
Provide clear explanations and suitable retry or recovery actions.

## 7. Testing Checklist
- [ ] Frontend starts successfully.
- [ ] Backend connection works.
- [ ] Streaming is verified in the browser.
- [ ] Loading states work correctly.
- [ ] Errors display useful messages.
- [ ] Citations expand and collapse.
- [ ] Feedback submission is verified.
- [ ] Actual usability observations are recorded.
- [ ] Top three observed friction points are addressed.

## Important
Do not mark a feature complete until it has been implemented and tested.
Do not assume API field names or payloads without checking the backend.
