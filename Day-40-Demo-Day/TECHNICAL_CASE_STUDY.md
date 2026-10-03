# Technical Case Study — AI Research Assistant

## What I Built

I built an AI Research Assistant that combines a multi-step AI workflow, retrieval, structured tool execution, evaluation, caching, reliability controls, and a production API. The project evolved incrementally through the AI Engineering Challenge rather than being implemented as a single prototype.

The system accepts a research query and processes it through a structured workflow. Backend services expose the research functionality through FastAPI, while the project includes a dedicated evaluation suite for measuring assistant behaviour.

## What Failed and Why

During development, several engineering problems appeared. RAG retrieval could return technically similar but contextually weak documents, making evaluation important instead of relying only on whether the application returned an answer. AI API failures and latency also exposed the limitations of treating external model calls as always available.

The debugging work showed that an AI application can produce a successful HTTP response while still producing an incorrect or low-quality result. This motivated systematic evaluation, tracing, regression checks, caching and reliability controls.

## What Changed

I introduced an evaluation layer with datasets, an evaluator and regression checks. I also added production-oriented improvements such as Redis-based caching, latency optimisation, health checks and a circuit-breaker approach for external API failures.

The project was then extended toward deployment and user feedback collection so that future improvements could be based on observed behaviour rather than assumptions.

## What I Learned

The biggest lesson was that building an AI application is different from building a simple API. Correctness, retrieval quality, latency, external API reliability and evaluation all have to be treated as engineering concerns.

I also learned the value of incremental development. Each stage of the project exposed a new failure mode, and those failures became inputs for the next architectural improvement.

The result is not just a working AI application, but a documented engineering workflow covering experimentation, evaluation, debugging, optimisation, reliability and deployment.
