\# AI Engineering Resume Bullets



Use the bullets that accurately reflect your implemented work. Add measured numbers only after verifying them.



\- Developed a Retrieval-Augmented Generation (RAG) pipeline using vector search, metadata filtering, and retrieval improvements to support context-aware AI responses.

\- Built a FastAPI-based AI assistant API with chat and conversation-history endpoints.

\- Created automated evaluation and regression-testing components to assess AI response quality and identify failures.

\- Implemented a domain-specific evaluation dataset and failure-analysis workflow to compare system behaviour across test cases.

\- Explored caching and retrieval optimisation to reduce unnecessary processing and improve response performance.

\- Used Python, FastAPI, SQLite, vector databases, and automated tests across AI application development projects.



\## Quantification Checklist

Before adding metrics to the resume, verify:

\- Number of evaluation questions actually run

\- Actual evaluation score and scoring rubric

\- Test count and passing results

\- Measured response latency before and after optimisation

\- Measured cost per query, if available

\- Verified production deployment URL



\# Five Technical Interview Talking Points



\## 1. Vector Search vs Keyword Search

\*\*Decision:\*\* Use semantic retrieval when meaning matters, and consider keyword search for exact terms.

\*\*Alternative:\*\* Keyword-only retrieval.

\*\*Trade-off:\*\* Semantic search can find related concepts but may miss exact identifiers.



\## 2. Metadata Filtering

\*\*Decision:\*\* Narrow candidate documents using relevant metadata.

\*\*Alternative:\*\* Search the entire index.

\*\*Trade-off:\*\* Filtering can improve relevance but incorrect metadata can hide useful documents.



\## 3. Automated Evaluation

\*\*Decision:\*\* Reuse a fixed evaluation dataset during development.

\*\*Alternative:\*\* Judge quality only through occasional manual checks.

\*\*Trade-off:\*\* Automated evaluation is repeatable but depends on dataset quality and scoring reliability.



\## 4. API Separation

\*\*Decision:\*\* Keep API routes separate from retrieval and evaluation logic.

\*\*Alternative:\*\* Put all logic in one large route handler.

\*\*Trade-off:\*\* Separation improves maintainability but introduces additional modules.



\## 5. Regression Tests

\*\*Decision:\*\* Rerun tests after changes to prompts, retrieval, or processing.

\*\*Alternative:\*\* Test only the newly changed feature.

\*\*Trade-off:\*\* Regression testing catches unintended changes but requires a maintained test suite.

