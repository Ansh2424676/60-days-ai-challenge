
# Day 21 — AI Product Quality Audit

This project audits the Day 20 AI Knowledge Assistant against:
- Accuracy
- Latency
- Reliability
- Transparency
- Graceful degradation

## Folder placement

Place this folder beside your Day 20 folder:

```text
60-days-of-ai/
├── Day-20-AI-Knowledge-Assistant/
│   ├── rag_pipeline.py
│   ├── knowledge_base.json
│   └── ...
└── Day-21-AI-Product-Quality-Audit/
    ├── audit.py
    ├── README.md
    └── results/
```

## Run

Open PowerShell in the Day 21 folder:

```powershell
cd C:\Users\ansh\OneDrive\Desktop\60-days-of-ai\Day-21-AI-Product-Quality-Audit
python audit.py
```

The script imports the Day 20 `rag_pipeline.py`, runs the structured tests, measures latency, and creates the report.

## Outputs

- `results/quality_test_results.csv`
- `results/latency_results.csv`
- `results/user_style_results.csv`
- `results/DAY21_PRODUCT_QUALITY_REPORT.md`

## Important

Your Day 20 `.env` must contain a valid `OPENAI_API_KEY`.

Do not commit `.env` or any real API key.
