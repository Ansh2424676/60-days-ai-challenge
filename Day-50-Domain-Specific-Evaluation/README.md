# Day 50 — Domain-Specific Evaluation Suite

## Objective
Evaluate the AI product using 30 domain-focused questions across easy, medium, and hard tiers.

## Dataset
- 10 easy questions
- 10 medium questions
- 10 hard questions
- Includes adversarial questions

## Evaluation dimensions
- Accuracy
- Relevance
- Grounding
- Reasoning

## Required completion checks
1. Connect the real product retrieval and generation pipeline.
2. Integrate the Day 29 LLM judge.
3. Run all 30 questions and calculate scores by tier.
4. Diagnose the five lowest-scoring questions.
5. Implement and verify at least three fixes.
6. Run the regression suite and save timestamped JSON results.

## Current status
Dataset and initial regression-runner scaffold created.
Actual evaluation, verified scores, and fixes remain pending until the real product pipeline and LLM judge are connected.

## Run
```powershell
python .\regression_test_runner.py
```
