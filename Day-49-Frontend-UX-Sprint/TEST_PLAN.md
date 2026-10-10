# Day 49 — Frontend Test Plan

## 1. Streaming Response
**Steps**
1. Start the backend and frontend.
2. Submit a research question.
3. Observe the response while it is being generated.

**Expected**
- A skeleton appears before the first token.
- Incoming tokens appear incrementally.
- A typing indicator appears during generation.
- The completed answer and metadata remain visible.

**Result:** Not tested

## 2. Citation Panel
**Steps**
1. Submit a research question that returns sources.
2. Expand the Sources panel.
3. Inspect document names, excerpts, and similarity scores.

**Expected**
- The panel expands and collapses.
- Displayed values match the backend response.

**Result:** Not tested

## 3. API Errors
**Steps**
1. Trigger a controlled API failure in a development environment.
2. Observe the error message.
3. Use the retry action.

**Expected**
- A clear, accessible message appears.
- Retry sends a new request.
- Internal stack traces and secrets are not exposed.

**Result:** Not tested

## 4. Feedback
**Steps**
1. Submit a research question.
2. Select Helpful or Not helpful.
3. Verify the API response or stored feedback record.

**Expected**
- Feedback is sent using the actual backend schema.
- Success and failure states are visible.

**Result:** Not tested

## 5. Usability
**Steps**
1. Observe a non-developer using the app for 15 minutes.
2. Record observed confusion without suggesting solutions during the test.
3. Prioritize and fix the top three friction points.
4. Retest the affected interactions.

**Result:** Not conducted

## Final Sign-off
- [ ] Streaming verified in browser
- [ ] Citation data verified
- [ ] Error recovery verified
- [ ] Feedback endpoint verified
- [ ] Usability observation completed
- [ ] Top three observed friction points fixed
