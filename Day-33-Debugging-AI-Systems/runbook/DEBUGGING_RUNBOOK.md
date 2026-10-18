# AI System Debugging Runbook

## 1. Identify the Failure

First determine whether the problem is related to:

- Retrieval
- Generation
- Configuration
- Data
- Application logic

Record the failing query and expected result.

---

## 2. Select Failed Cases

Use the failure-selection utility to isolate failed evaluation cases.

```python
failures = select_failures(results)