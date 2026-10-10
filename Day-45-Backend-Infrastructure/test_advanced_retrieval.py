
"""Offline unit tests for Day 46 advanced retrieval."""

import unittest
from unittest.mock import Mock

from advanced_retrieval import AdvancedRetriever


class TestAdvancedRetriever(unittest.TestCase):

    def setUp(self):
        self.client = Mock()
        self.embedding_model = Mock()
        self.index = Mock()

        self.retriever = AdvancedRetriever(
            client=self.client,
            embedding_model=self.embedding_model,
            index=self.index,
            documents=[],
        )

    def test_empty_query_raises_error(self):
        with self.assertRaises(ValueError):
            self.retriever.retrieve("")

    def test_empty_query_rewriting_raises_error(self):
        with self.assertRaises(ValueError):
            self.retriever.rewrite_query("")

    def test_rewriting_without_history_returns_original_query(self):
        query = "Who led the project?"
        result = self.retriever.rewrite_query(query, history=None)
        self.assertEqual(result, query)

    def test_rerank_empty_candidates(self):
        result = self.retriever.rerank(
            "Who led the project?",
            [],
        )
        self.assertEqual(result, [])

    def test_rerank_falls_back_to_first_three_candidates(self):
        candidates = [
            {"chunk_id": f"chunk-{i}", "title": f"Title {i}", "text": f"Text {i}"}
            for i in range(1, 6)
        ]

        self.retriever._ask = Mock(
            side_effect=ValueError("Invalid JSON")
        )

        result = self.retriever.rerank(
            "Who led the project?",
            candidates,
        )

        self.assertEqual(len(result), 3)
        self.assertEqual(
            [item["chunk_id"] for item in result],
            ["chunk-1", "chunk-2", "chunk-3"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
