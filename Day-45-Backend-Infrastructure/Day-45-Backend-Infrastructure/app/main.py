from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.db.database import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database when the application starts
    initialize_database()

    yield


app = FastAPI(
    title="ResearchMate AI API",
    description="Backend infrastructure for ResearchMate AI",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(router)