# Day 60 — AI Engineer Graduation

## Engineering Retrospective

### What I Built
During the 60-day AI engineering challenge, I worked on RAG pipelines, semantic search, embeddings, FastAPI services, automated testing, evaluation, caching, reliability, and deployment.

Key projects included:
- AI Research Assistant
- RAG-based Knowledge Assistant
- HireLens — AI Job Match and Resume Analyzer
- Domain-specific evaluation and testing tools

### Five Technical Lessons
1. AI quality depends on the complete system, not only the language model.
2. Retrieval quality strongly affects grounded answer quality.
3. Evaluation and regression tests should guide development.
4. Deployment requires logging, error handling, security, and monitoring.
5. Performance improvements must be measured against quality and cost.

### Three Engineering Challenges
1. Import and dependency issues across separate project folders.
   Lesson: isolate environments and run tests from the correct project root.
2. Integration complexity between backend, frontend, and retrieval components.
   Lesson: define API contracts and test component boundaries.
3. Optimisation and evaluation complexity.
   Lesson: establish a baseline before changing the system.

These are engineering challenge categories; replace them with verified incidents from the challenge log where appropriate.

### What I Would Do Differently
- Define measurable success criteria on Day 1.
- Create a small end-to-end prototype early.
- Establish a representative evaluation dataset immediately.
- Add automated regression tests from the beginning.
- Record architecture decisions, failures, latency, and costs continuously.
- Gather genuine user feedback before expanding features.

### Final Evaluation
- Evaluation dataset size: Not yet verified
- Final quality score: Not yet verified
- Test results: Root-level pytest collection reported 7 errors
- Latency and cost: Not yet verified
- Production URL: Verify before publishing

Never report unverified scores or claim that all tests pass.
