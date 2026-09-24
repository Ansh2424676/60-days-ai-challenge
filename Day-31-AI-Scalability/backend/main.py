import asyncio
import uuid
from datetime import datetime, timezone

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from workflow import run_workflow
from cache_service import get_cached_response, save_response_to_cache


app = FastAPI(
    title="AI Research Assistant - Day 31",
    description="Scalable AI backend with Redis caching and background jobs",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Temporary in-memory job store
jobs: dict[str, dict] = {}


class ResearchRequest(BaseModel):
    topic: str


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "AI Research Assistant - Day 31",
    }


async def run_research_job(job_id: str, topic: str):
    jobs[job_id]["status"] = "running"
    jobs[job_id]["started_at"] = datetime.now(timezone.utc).isoformat()

    try:
        # --------------------------------
        # 1. Embedding Cache
        # --------------------------------
        embedding, cached = await asyncio.to_thread(
            get_cached_response,
            topic,
        )

        # --------------------------------
        # 2. Semantic Response Cache HIT
        # --------------------------------
        if cached:
            jobs[job_id].update(
                {
                    "status": "completed",
                    "cache_hit": True,
                    "similarity": cached["similarity"],
                    "cached_query": cached["query"],
                    "report": cached["response"],
                    "completed_steps": [
                        "embedding_cache",
                        "semantic_response_cache",
                    ],
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                }
            )

            return

        # --------------------------------
        # 3. Run AI Research Workflow
        # --------------------------------
        result = await asyncio.to_thread(
            run_workflow,
            topic=topic,
            resume=False,
        )

        if result.error:
            jobs[job_id].update(
                {
                    "status": "failed",
                    "cache_hit": False,
                    "error": result.error,
                }
            )
            return

        # --------------------------------
        # 4. Save Generated Response
        # --------------------------------
        await asyncio.to_thread(
            save_response_to_cache,
            topic,
            embedding,
            result.final_report,
        )

        jobs[job_id].update(
            {
                "status": "completed",
                "cache_hit": False,
                "completed_steps": result.completed_steps,
                "report": result.final_report,
                "cached_for_future_requests": True,
                "completed_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    except Exception as exc:
        jobs[job_id].update(
            {
                "status": "failed",
                "error": str(exc),
            }
        )


@app.post("/research")
async def research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks,
):
    topic = request.topic.strip()

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="Research topic cannot be empty.",
        )

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "job_id": job_id,
        "topic": topic,
        "status": "queued",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    background_tasks.add_task(
        run_research_job,
        job_id,
        topic,
    )

    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Research job started.",
    }


@app.get("/research/status/{job_id}")
async def research_status(job_id: str):
    job = jobs.get(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Research job not found.",
        )

    return job