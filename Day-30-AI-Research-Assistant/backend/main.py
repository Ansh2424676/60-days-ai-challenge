from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from workflow import run_workflow


app = FastAPI(
    title="AI Research Assistant",
    description="Day 30 AI Research Assistant API",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ResearchRequest(BaseModel):
    topic: str


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AI Research Assistant",
    }


# ============================================================
# RESEARCH ENDPOINT
# ============================================================

@app.post("/research")
def research(request: ResearchRequest):

    topic = request.topic.strip()

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="Research topic cannot be empty."
        )

    try:

        result = run_workflow(
            topic=topic,
            resume=False
        )

        if result.error:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Research workflow failed.",
                    "error": result.error,
                    "completed_steps": result.completed_steps,
                }
            )

        return {
            "topic": result.topic,
            "status": "completed",
            "completed_steps": result.completed_steps,
            "report": result.final_report,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )