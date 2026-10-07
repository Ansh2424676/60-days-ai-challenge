# ResearchMate AI — API Design

## Overview

ResearchMate AI is an evidence-grounded technical research assistant.

The Day 45 backend provides session management, authentication,
rate limiting, request logging, feedback collection and health monitoring.

---

# Authentication

Protected endpoints require the following HTTP header:

```text
x-api-key: researchmate-day45-secret-key