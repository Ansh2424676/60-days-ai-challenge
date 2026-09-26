import json
from pathlib import Path

from attacks.attack_payloads import ATTACK_PAYLOADS
from attacks.run_attacks import classify_response
from app.secure_assistant import ask_assistant


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "results" / "after_defence_results.json"


def main():
    results = []

    for payload in ATTACK_PAYLOADS:
        print("=" * 70)
        print(f"ATTACK: {payload['id']}")

        try:
            result = ask_assistant(payload["payload"])

            if result["blocked"]:
                classification = "successfully_blocked"
            else:
                classification = classify_response(result["response"])

            record = {
                "id": payload["id"],
                "category": payload["category"],
                "payload": payload["payload"],
                "classification": classification,
                "blocked": result["blocked"],
                "blocked_by": result["blocked_by"],
                "raw_response": result["response"],
            }

            print(f"CLASSIFICATION: {classification}")
            print(f"BLOCKED_BY: {result['blocked_by']}")
            print("RAW RESPONSE:")
            print(result["response"])

            results.append(record)

        except Exception as exc:
            print(f"ERROR: {exc}")

            results.append({
                "id": payload["id"],
                "category": payload["category"],
                "payload": payload["payload"],
                "classification": "error",
                "blocked": False,
                "blocked_by": None,
                "raw_response": "",
                "error": str(exc),
            })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nAfter-defence testing complete.")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()