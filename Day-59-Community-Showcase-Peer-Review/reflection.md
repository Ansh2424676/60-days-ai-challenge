# Day 59 — Engineering Journey Reflection

If I started this challenge today with my current knowledge, I would approach the project with a stronger focus on measurement, architecture, and feedback from the beginning.

## Week 1: Define the Problem and Establish a Baseline

During the first week, I would spend more time defining the user problem and deciding how success should be measured. Before building a complex AI pipeline, I would create a small working prototype and a fixed set of representative questions. I would record a baseline for answer correctness, retrieval relevance, latency, and cost. This would give me evidence to guide future engineering decisions instead of relying mainly on whether a response sounds convincing.

I would also document the system architecture early, identify the most important risks, and keep configuration and secrets out of source control. A small, testable foundation would make later changes easier to understand.

## Week 2: Build Modularly and Test Continuously

In the second week, I would separate ingestion, retrieval, generation, API handling, and evaluation into clearly defined components. I would add automated tests for normal requests, empty results, malformed input, API failures, and difficult queries. I would compare retrieval strategies using the same evaluation dataset rather than changing several variables at once.

I would also collect structured logs and track latency and token usage. These measurements would help identify whether a problem comes from retrieval, generation, or infrastructure. Peer feedback would become part of the development process earlier, not just a final activity.

## Final Phase: Validate the Whole Product

In the final phase, I would prioritize production readiness alongside new features. I would verify deployment health, test the frontend on desktop and mobile, check API error handling, and run regression evaluations before release. I would prepare a reproducible demo and ensure that all public claims match measured results.

I would also schedule time for peer reviews, real user feedback, and follow-up fixes. Rather than treating launch as the finish line, I would use it to start a measurable improvement cycle.

Overall, this challenge has reinforced that AI engineering requires more than connecting a model to an API. Reliable products need thoughtful architecture, honest evaluation, maintainable code, clear communication, and continuous learning from other engineers and real users.
