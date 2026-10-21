
### Question 2: How would you reduce hallucinations in a medical information assistant?

I would use a safety-first architecture because incorrect medical information can cause serious harm. The goal is to provide evidence-based general information, communicate uncertainty, and direct users to qualified healthcare professionals when necessary.

**1. Trusted sources:** Build the knowledge base from approved medical guidelines and verified healthcare publications. Store source metadata, publication dates, and version information to identify outdated content.

**2. Retrieval-augmented generation:** Retrieve relevant passages from trusted sources and pass them to the model as context. Use appropriate chunking, metadata filters, semantic retrieval, and reranking to improve relevance.

**3. Grounded responses:** Instruct the model to answer only when sufficient evidence is available. Validate important claims against retrieved passages and provide citations where possible.

**4. Uncertainty and safety:** If reliable evidence is missing, the system should abstain rather than guess. It should not replace professional diagnosis or treatment. Urgent warning signs should trigger appropriate emergency guidance.

**5. Human oversight:** Have medical experts review the knowledge base, evaluation dataset, safety policies, and representative outputs. Escalate high-risk questions according to predefined rules.

**6. Privacy:** Minimize collection of personal health information, enforce access controls, protect data in transit and at rest, and avoid exposing sensitive information in logs.

**7. Evaluation:** Measure factual correctness, groundedness, citation accuracy, retrieval recall, unsafe-answer rate, and appropriate abstention using a clinician-reviewed test set.

I would release the system gradually and monitor safety regressions. RAG and guardrails reduce risk but cannot guarantee every answer is correct. The system must communicate its limitations and support, rather than replace, qualified medical care.


### Question 3: Your RAG system returns wrong answers 20% of the time. How would you debug it?

I would avoid changing the model immediately. First, I would reproduce the failures, identify their causes, and measure the impact of each change.

**Step 1 — Establish a baseline:** Build a representative evaluation dataset containing questions, expected answers, trusted source documents, and current responses. Confirm how the 20% error rate was calculated.

**Step 2 — Classify failures:** Separate retrieval failures, ranking failures, generation failures, missing or outdated knowledge-base content, and evaluation errors.

**Step 3 — Inspect retrieval:** Examine the top-k retrieved chunks, similarity scores, metadata filters, and source documents. Use Recall@k to check whether the required evidence was retrieved.

**Step 4 — Check data and indexing:** Investigate document parsing, chunk size, overlap, embeddings, metadata, and index freshness. Compare configurations using the same evaluation dataset.

**Step 5 — Inspect generation:** If the correct evidence was retrieved, examine the prompt, context length, conflicting passages, and model output. Improve grounding instructions, citations, and abstention when evidence is insufficient.

**Step 6 — Run controlled experiments:** Change one variable at a time where practical. Compare against the baseline and measure accuracy, latency, and cost.

**Step 7 — Prevent regressions:** Add failed examples to regression tests, run the evaluation suite, manually review high-risk cases, and deploy improvements gradually.

**Step 8 — Report evidence:** Compare baseline and new error rates, sample size, failure categories, latency, and cost. Claim improvement only when supported by test results.

The key principle is to identify whether the root cause lies in data, retrieval, ranking, generation, or evaluation before choosing a fix.


### Question 4: How would you scale your AI assistant from 100 to 100,000 daily users?

I would scale incrementally, using measured traffic and performance bottlenecks to guide architectural decisions. I would not assume all daily users make requests simultaneously.

**Step 1 — Estimate workload:** Measure requests per user, peak concurrency, token usage, latency, and error rates. Daily active users alone do not determine capacity.

**Step 2 — Scale the API:** Keep FastAPI instances stateless where possible, deploy multiple instances behind a load balancer, and use health checks, timeouts, rate limits, and autoscaling.

**Step 3 — Optimize retrieval:** Profile retrieval latency, embedding generation, indexing, metadata filtering, and top-k selection. Choose managed or self-hosted vector search according to workload and operational needs.

**Step 4 — Control model cost and capacity:** Measure provider rate limits, token throughput, latency, and cost. Optimize context size, use streaming when appropriate, select models by task complexity, and safely cache reusable results.

**Step 5 — Use background workers:** Queue long-running tasks such as document ingestion and re-indexing so they do not block interactive requests.

**Step 6 — Improve reliability:** Use connection pooling, backups, monitoring, recovery procedures, and tenant-level access controls.

**Step 7 — Load-test:** Simulate realistic traffic and monitor p95/p99 latency, throughput, error rate, queue depth, retrieval latency, token usage, and cost per successful task.

**Step 8 — Roll out gradually:** Increase traffic in stages, monitor service-level objectives, and maintain rollback options. Apply fair rate limits and graceful failure handling when capacity is exceeded.

The goal is to scale based on measured bottlenecks while preserving answer quality, security, reliability, and acceptable cost.


### Question 5: What evaluation metrics would you use to measure whether your AI assistant is genuinely improving over time?

I would evaluate answer quality, retrieval performance, user outcomes, safety, and operational efficiency. No single metric is sufficient because improving one area can hide a regression in another.

**1. Answer quality:** Measure correctness, relevance, groundedness, completeness, and citation accuracy using representative questions with human-reviewed reference answers.

**2. Retrieval quality:** Use Recall@k to check whether relevant evidence appears in the top-k results, Precision@k to measure retrieval relevance, and Mean Reciprocal Rank (MRR) to evaluate the position of the first relevant result.

**3. User outcomes:** Track task completion, successful resolution rate, repeat-contact rate, escalation rate, and user satisfaction. Engagement alone does not prove usefulness.

**4. Safety:** Measure unsupported-answer rate, unsafe response rate, privacy incidents, policy violations, and appropriate abstention or escalation.

**5. Operational performance:** Track p50/p95/p99 latency, request error rate, throughput, token usage, and cost per successful task.

**6. Evaluation methodology:** Maintain a representative fixed evaluation set covering common questions, difficult queries, edge cases, and high-risk scenarios. Compare every release against the same baseline and use automated tests plus human review.

**7. Production monitoring:** Monitor privacy-conscious aggregate trends, investigate failure categories, and use controlled A/B tests where appropriate.

**8. Release criteria:** Define quality, safety, latency, and cost thresholds before deployment. Accept an improvement only when evidence shows better outcomes without unacceptable regressions.

My principle is to combine offline evaluation, human review, and production monitoring so that improvements are supported by measurable evidence.

