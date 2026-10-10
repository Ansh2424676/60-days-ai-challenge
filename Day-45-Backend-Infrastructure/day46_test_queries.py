
"""Day 46: Test cases for advanced retrieval."""

HYDE_QUERIES = [
    "Where would someone go to find the company's internal knowledge?",
    "Who was responsible for that AI project?",
    "How long would a new employee need to complete the training?",
    "Where is the company based, if I wanted to visit?",
    "What happened when that project first became available?",
]

FOLLOW_UP_TESTS = [
    {
        "history": [
            {"role": "user", "content": "Tell me about the NovaMind project."},
            {"role": "assistant", "content": "NovaMind is an internal AI project."},
        ],
        "query": "Who led it?",
        "expected_subject": "NovaMind project leadership",
    },
    {
        "history": [
            {"role": "user", "content": "What is the internal documentation platform?"},
            {"role": "assistant", "content": "The knowledge base uses an internal platform."},
        ],
        "query": "Where can I find more about it?",
        "expected_subject": "internal documentation platform",
    },
    {
        "history": [
            {"role": "user", "content": "Tell me about the AI Launchpad training."},
            {"role": "assistant", "content": "It is a company training program."},
        ],
        "query": "How long does it take?",
        "expected_subject": "AI Launchpad duration",
    },
    {
        "history": [
            {"role": "user", "content": "Where is NovaTech Solutions headquartered?"},
            {"role": "assistant", "content": "Let's check the company information."},
        ],
        "query": "And what about its location?",
        "expected_subject": "NovaTech Solutions headquarters",
    },
    {
        "history": [
            {"role": "user", "content": "When was NovaMind launched?"},
            {"role": "assistant", "content": "I can look that up in the knowledge base."},
        ],
        "query": "What happened around that time?",
        "expected_subject": "NovaMind launch",
    },
]
