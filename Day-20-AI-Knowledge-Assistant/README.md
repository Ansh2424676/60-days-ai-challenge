# Day 20 — Working AI Knowledge Assistant

An end-to-end RAG product built for the ABTalks AI Engineering Challenge.

## What this project combines

- **Day 12:** LangChain `RecursiveCharacterTextSplitter` chunking
- **Day 14:** FAISS semantic retrieval using normalized embeddings + cosine similarity
- **Day 17:** metadata filtering
- **Day 19:** grounded RAG system prompt
- **Day 20:** FastAPI `/ask` endpoint, source citations, confidence indicator, 15-query evaluation

## Architecture

```text
knowledge_base.json
       |
       v
LangChain chunking
       |
       v
SentenceTransformer embeddings
       |
       v
FAISS cosine-similarity index
       |
       v
Metadata filtering (optional)
       |
       v
Top-k context
       |
       v
OpenAI grounded generation
       |
       v
FastAPI POST /ask
       |
       +--> answer + source citations
       +--> sources[]
       +--> confidence
       +--> low-confidence warning
```

## 1. Create the environment

Windows PowerShell:

```powershell
cd Day-20-AI-Knowledge-Assistant

python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## 2. Configure the API key

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

`OPENAI_MODEL` should be a model available to your OpenAI API account. The example uses the model name used in the earlier challenge work.

## 3. Start the API

```powershell
uvicorn app:app --reload
```

Expected server:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 4. Verify health

```powershell
curl.exe http://127.0.0.1:8000/health
```

Expected:

```json
{"status":"ok"}
```

## 5. Test POST /ask

PowerShell:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/ask" `
  -H "Content-Type: application/json" `
  -d "{\"query\":\"Who led the NovaMind project?\"}"
```

A successful response contains:

- `answer`
- `sources`
- `confidence`
- `low_confidence`

The answer itself includes source citations such as:

```text
Sources: [doc-005] NovaMind Project Leadership
```

## 6. Test metadata filtering

For example, restrict retrieval to training documents:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/ask" `
  -H "Content-Type: application/json" `
  -d "{\"query\":\"How long does AI Launchpad last?\",\"filters\":{\"category\":\"training\"}}"
```

Another example:

```json
{
  "query": "What is NovaMind?",
  "filters": {
    "department": "Artificial Intelligence"
  }
}
```

## 7. Confidence indicator

The application uses:

```text
LOW_CONFIDENCE_THRESHOLD=0.3
```

If the highest retrieved cosine similarity is below `0.3`, the response appends:

```text
⚠️ Low confidence: the retrieved evidence may not strongly support this answer.
```

This makes weak retrieval visible instead of silently presenting an unsupported answer.

## 8. Run the 15-query evaluation

Make sure the API key is configured, then run:

```powershell
python evaluate.py
```

The script covers:

- 5 easy questions
- 5 medium questions
- 5 hard questions

It scores retrieval quality separately from answer quality and writes:

```text
results/evaluation_results.json
```

### Retrieval score

The evaluation is ranking-aware:

- 5/5 — all expected documents retrieved and an expected document is ranked first
- 4/5 — all expected documents retrieved
- 3/5 — at least half retrieved
- 2/5 — one expected document retrieved
- 1/5 — no expected document retrieved

### Answer score

The script also provides a transparent local fallback answer-quality score based on overlap with the reference answer. This is useful when you want a reproducible local score without paying for a separate judge model.

## 9. Git

From the parent `60-days-of-ai` repository:

```powershell
git add Day-20-AI-Knowledge-Assistant
git commit -m "Complete Day 20 AI Knowledge Assistant"
git push
```

Check the commit:

```powershell
git log -1 --oneline
```

## Submission checklist

- [x] End-to-end RAG module
- [x] FastAPI `POST /ask`
- [x] JSON request with `query`
- [x] `answer` field
- [x] `sources` list
- [x] Source IDs/titles included in answers
- [x] Metadata filtering
- [x] Confidence indicator
- [x] 15-query evaluation
- [x] Separate retrieval and answer quality scores
- [x] README
- [x] Working curl example
- [ ] Start server locally and capture proof screenshot
- [ ] Run evaluation and capture result screenshot
- [ ] Push Git commit
- [ ] Submit GitHub URL + LinkedIn URL to ABTalks
