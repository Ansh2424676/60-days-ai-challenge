from dataclasses import dataclass

@dataclass
class EvalCase:
    id: str
    tier: str
    question: str
    reference_answer: str
    expected_evidence: tuple
    adversarial_type: str = ""

EVALUATION_DATASET = []

for i in range(1, 11):
    EVALUATION_DATASET.append(EvalCase(
        f"E{i:02}", "easy",
        f"[Replace with single-chunk knowledge question {i}]",
        "[Add verified reference answer]", ("chunk-id",)
    ))

for i in range(1, 11):
    EVALUATION_DATASET.append(EvalCase(
        f"M{i:02}", "medium",
        f"[Replace with multi-chunk synthesis question {i}]",
        "[Add verified synthesis answer]", ("chunk-1", "chunk-2")
    ))

adversarial = {
    1: "misleading phrasing",
    2: "unanswerable",
    3: "hallucination-prone"
}

for i in range(1, 11):
    EVALUATION_DATASET.append(EvalCase(
        f"H{i:02}", "hard",
        f"[Replace with boundary or reasoning question {i}]",
        "[Add verified answer or expected abstention]",
        (),
        adversarial.get(i, "")
    ))

def validate_dataset(dataset=EVALUATION_DATASET):
    counts = {t: sum(q.tier == t for q in dataset)
              for t in ("easy", "medium", "hard")}
    assert counts == {"easy": 10, "medium": 10, "hard": 10}, counts
    assert len({q.id for q in dataset}) == 30
    assert sum(bool(q.adversarial_type) for q in dataset) >= 3
    return counts

if __name__ == "__main__":
    print("Dataset structure:", validate_dataset())
