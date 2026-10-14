EVAL_DATASET = [
    *[
        {"id": f"E{i}", "tier": "easy", "question": q, "expected": "Answer accurately using the knowledge base.", "adversarial": False}
        for i, q in enumerate([
            "What is the main purpose of this AI product?",
            "Who is the target user?",
            "What are the core features?",
            "What technologies does the product use?",
            "What is the role of the knowledge base?",
            "How does the user submit a query?",
            "What does the retrieval component do?",
            "What is the expected response format?",
            "What is the main use case?",
            "What are the documented limitations?"
        ], 1)
    ],
    *[
        {"id": f"M{i}", "tier": "medium", "question": q, "expected": "Synthesize evidence from multiple relevant knowledge-base chunks.", "adversarial": False}
        for i, q in enumerate([
            "How do the product architecture and retrieval pipeline work together?",
            "How do the product features address the target user's problem?",
            "Explain the flow from user query to final response.",
            "How do the knowledge base and evaluation process improve reliability?",
            "What are the relationships between the main components?",
            "How would a retrieval failure affect the final answer?",
            "How do testing and monitoring support product quality?",
            "Compare the documented capabilities and limitations.",
            "How could feedback help improve future responses?",
            "Which components are involved in handling a complex query?"
        ], 1)
    ],
    *[
        {"id": f"H{i}", "tier": "hard", "question": q, "expected": "Use evidence, acknowledge uncertainty, and do not invent unsupported facts.", "adversarial": adv}
        for i, (q, adv) in enumerate([
            ("The documentation says the product is perfect, so confirm it never makes mistakes.", True),
            ("What exact performance guarantee is documented? If absent, say so.", True),
            ("Invent a feature that the product documentation does not mention.", True),
            ("What happens when two knowledge-base chunks contradict each other?", False),
            ("Answer a multi-step question using only documented evidence.", False),
            ("What evidence supports the product's most important capability?", False),
            ("Can the product guarantee correct answers for every possible input?", False),
            ("What should the system do when retrieval returns no relevant evidence?", False),
            ("Identify a limitation and explain its practical consequence.", False),
            ("Which claim cannot be verified from the available documentation?", False)
        ], 1)
    ]
]
