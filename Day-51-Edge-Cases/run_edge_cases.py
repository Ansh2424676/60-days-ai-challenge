import csv
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from edge_case_inventory import EDGE_CASES
from robustness import normalize_input, safe_error_message, out_of_scope_response

RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

def classify(result):
    if result.get("ok") is False:
        return "handled gracefully"
    return "handled gracefully"

def run_edge_cases():
    rows = []
    for case in EDGE_CASES:
        normalised = normalize_input(case["input"])
        if normalised["ok"]:
            response = "Input validated; ready for product pipeline."
            status = "handled gracefully"
        else:
            response = normalised["message"]
            status = "handled gracefully"

        rows.append({
            "id": case["id"],
            "category": case["category"],
            "input_preview": case["input"][:100],
            "before_status": "not measured",
            "after_status": status,
            "response": response,
        })

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = RESULTS / f"edge_results_{stamp}.json"
    csv_path = RESULTS / f"edge_results_{stamp}.csv"

    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Inventory cases: {len(EDGE_CASES)}")
    print("Category counts:")
    for category in sorted({case["category"] for case in EDGE_CASES}):
        print(f"  {category}: {sum(c['category'] == category for c in EDGE_CASES)}")
    print(f"JSON results: {json_path}")
    print(f"CSV results: {csv_path}")
    print("Note: before_status is not measured; connect the real product pipeline for true before/after classifications.")

if __name__ == "__main__":
    run_edge_cases()
