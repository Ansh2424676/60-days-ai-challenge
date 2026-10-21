# Day 57 — STAR Behavioural Interview Answers

## 1. Technical decision made under uncertainty

**Situation:** During my AI engineering challenge, I was developing a RAG-based AI application and needed to connect user questions with relevant information from a knowledge base.

**Task:** I needed to choose an approach that could retrieve useful context while keeping the system maintainable and easier to evaluate.

**Action:** I used the RAG architecture as my design approach. I considered document processing, chunking, embeddings, retrieval, and language-model generation. I focused on evaluating retrieval relevance and response quality rather than assuming fluent answers were necessarily correct.

**Result:** This gave me a clearer, modular approach to building and evaluating the application. It also helped me understand trade-offs involving retrieval quality, latency, model cost, and answer reliability.

## 2. Failure diagnosed

**Situation:** During a technical review of my AI challenge repository, I ran the test suite and encountered test collection problems.

**Task:** I needed to determine whether the failures came from application logic, missing dependencies, import paths, or test configuration.

**Action:** I reviewed the test output and separated the failures into categories, including missing modules, dependency issues, and a test-file naming conflict. The run reported 21 passing tests and seven collection errors. I identified the areas requiring investigation instead of assuming every error represented a code defect.

**Result:** I established a debugging plan and identified specific issues to investigate. This is a diagnosis, not a verified fix. I will update this result after applying the changes and rerunning the affected tests successfully.

## 3. Improvement driven by data

**Situation:** While developing AI applications, I recognized that a response that sounds convincing is not necessarily correct, relevant, or efficient.

**Task:** I wanted a systematic way to assess quality and identify meaningful improvements.

**Action:** I focused on measurable evaluation methods, including retrieval quality, response correctness, latency, and error tracking. My approach was to establish a baseline, identify a specific weakness, test a targeted change, and compare results instead of relying on intuition.

**Result:** This established a more evidence-based improvement process for my AI engineering work. Any numerical improvement will be reported only after verification using comparable evaluation results.
