import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.health import HealthChecker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Production Hardened AI Assistant",
    version="1.0.0"
)


# Temporary FAISS index for health-check testing.
# Later we will replace this with your real Day 14/20/30 FAISS index.
import faiss

TEST_DIMENSION = 384

faiss_index = faiss.IndexFlatL2(TEST_DIMENSION)

# Add one test vector so the index is queryable.
import numpy as np

test_vector = np.zeros(
    (1, TEST_DIMENSION),
    dtype="float32"
)

faiss_index.add(test_vector)


health_checker = HealthChecker(
    faiss_index=faiss_index
)


@app.get("/")
def root():
    return {
        "message": "Production Hardened AI Assistant is running"
    }


@app.get("/health")
def health():
    result = health_checker.run_all_checks()

    status_code = (
        200
        if result["status"] == "healthy"
        else 503
    )

    return JSONResponse(
        status_code=status_code,
        content=result
    )