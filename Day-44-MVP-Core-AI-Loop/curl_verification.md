# Day 44 — Curl Verification

## Command

```powershell
curl.exe -X POST "http://127.0.0.1:8000/ask" `
-H "Content-Type: application/json" `
-d '{"question":"What is the difference between RAG and fine-tuning?"}'