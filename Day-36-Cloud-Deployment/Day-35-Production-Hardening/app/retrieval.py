import logging
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class ProductionRetriever:
    """
    Production retrieval system.

    Primary:
        FAISS semantic retrieval

    Fallback:
        TF-IDF keyword retrieval
    """

    def __init__(
        self,
        documents: list[str],
        faiss_index=None,
        embedding_function=None,
    ):
        self.documents = documents
        self.faiss_index = faiss_index
        self.embedding_function = embedding_function

        # Day 11 TF-IDF fallback
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english"
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(
            documents
        )

    def search_faiss(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:
        """Perform semantic retrieval using FAISS."""

        if self.faiss_index is None:
            raise RuntimeError("FAISS index is not available")

        if self.embedding_function is None:
            raise RuntimeError(
                "Embedding function is not available"
            )

        query_embedding = self.embedding_function(query)

        query_vector = np.asarray(
            query_embedding,
            dtype="float32"
        )

        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        distances, indices = self.faiss_index.search(
            query_vector,
            top_k
        )

        results = []

        for index in indices[0]:
            if 0 <= index < len(self.documents):
                results.append(self.documents[index])

        logger.info(
            "FAISS retrieval returned %d results",
            len(results)
        )

        return results

    def search_tfidf(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:
        """
        Day 11 TF-IDF keyword retrieval fallback.
        """

        logger.warning(
            "Using TF-IDF fallback retrieval"
        )

        query_vector = self.vectorizer.transform(
            [query]
        )

        similarities = cosine_similarity(
            query_vector,
            self.tfidf_matrix
        ).flatten()

        ranked_indices = np.argsort(
            similarities
        )[::-1][:top_k]

        results = [
            self.documents[index]
            for index in ranked_indices
            if similarities[index] > 0
        ]

        logger.info(
            "TF-IDF fallback returned %d results",
            len(results)
        )

        return results

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> dict[str, Any]:
        """
        Search using FAISS and gracefully fall back
        to TF-IDF when FAISS fails.
        """

        try:
            results = self.search_faiss(
                query=query,
                top_k=top_k
            )

            return {
                "results": results,
                "method": "faiss",
                "fallback": False,
            }

        except Exception as exc:

            logger.error(
                "FAISS retrieval failed: %s",
                exc,
                exc_info=True
            )

            # Graceful degradation
            try:
                results = self.search_tfidf(
                    query=query,
                    top_k=top_k
                )

                return {
                    "results": results,
                    "method": "tfidf",
                    "fallback": True,
                    "error": str(exc),
                }

            except Exception as fallback_exc:

                logger.error(
                    "TF-IDF fallback also failed: %s",
                    fallback_exc,
                    exc_info=True
                )

                raise RuntimeError(
                    "Both FAISS and TF-IDF retrieval failed"
                ) from fallback_exc