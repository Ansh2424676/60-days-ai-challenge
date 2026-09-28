import logging
import os
from typing import Any

import faiss
import numpy as np
import redis
from openai import OpenAI

logger = logging.getLogger(__name__)


class HealthChecker:
    def __init__(self, faiss_index=None):
        self.faiss_index = faiss_index

        self.redis_url = os.getenv(
            "REDIS_URL",
            "redis://localhost:6379"
        )

        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def check_faiss(self) -> dict[str, Any]:
        """Check whether FAISS is loaded and queryable."""

        try:
            if self.faiss_index is None:
                raise RuntimeError("FAISS index is not loaded")

            dimension = self.faiss_index.d

            test_vector = np.zeros(
                (1, dimension),
                dtype="float32"
            )

            self.faiss_index.search(test_vector, 1)

            logger.info("FAISS health check passed")

            return {
                "status": "healthy",
                "message": "FAISS index loaded and queryable"
            }

        except Exception as exc:
            logger.error(
                "FAISS health check failed: %s",
                exc
            )

            return {
                "status": "unhealthy",
                "message": str(exc)
            }

    def check_redis(self) -> dict[str, Any]:
        """Check Redis connectivity."""

        try:
            client = redis.from_url(
                self.redis_url,
                socket_connect_timeout=2,
                socket_timeout=2,
            )

            response = client.ping()

            if not response:
                raise RuntimeError("Redis ping failed")

            logger.info("Redis health check passed")

            return {
                "status": "healthy",
                "message": "Redis ping successful"
            }

        except Exception as exc:
            logger.error(
                "Redis health check failed: %s",
                exc
            )

            return {
                "status": "unhealthy",
                "message": str(exc)
            }

    def check_openai(self) -> dict[str, Any]:
        """Check whether OpenAI responds to a minimal request."""

        try:
            response = self.openai_client.responses.create(
                model="gpt-4o-mini",
                input="Reply with OK.",
                max_output_tokens=5,
            )

            if not response:
                raise RuntimeError(
                    "OpenAI returned an empty response"
                )

            logger.info("OpenAI health check passed")

            return {
                "status": "healthy",
                "message": "OpenAI API responded successfully"
            }

        except Exception as exc:
            logger.error(
                "OpenAI health check failed: %s",
                exc
            )

            return {
                "status": "unhealthy",
                "message": str(exc)
            }

    def run_all_checks(self) -> dict[str, Any]:
        """Run all production health checks."""

        checks = {
            "faiss": self.check_faiss(),
            "redis": self.check_redis(),
            "openai": self.check_openai(),
        }

        overall_status = (
            "healthy"
            if all(
                check["status"] == "healthy"
                for check in checks.values()
            )
            else "unhealthy"
        )

        return {
            "status": overall_status,
            "checks": checks,
        }