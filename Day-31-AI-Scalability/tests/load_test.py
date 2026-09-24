import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


API_URL = "http://127.0.0.1:8000"

TOTAL_REQUESTS = 10
TIMEOUT = 30


def send_request(index: int) -> dict:
    """
    Send one research request.
    """

    start = time.perf_counter()

    try:
        response = requests.post(
            f"{API_URL}/research",
            json={
                "topic": "Artificial Intelligence in Healthcare"
            },
            timeout=TIMEOUT,
        )

        elapsed = time.perf_counter() - start

        return {
            "request": index,
            "status_code": response.status_code,
            "success": response.ok,
            "latency": elapsed,
            "response": response.json(),
        }

    except Exception as exc:

        elapsed = time.perf_counter() - start

        return {
            "request": index,
            "status_code": None,
            "success": False,
            "latency": elapsed,
            "error": str(exc),
        }


def main():

    print("=" * 60)
    print("DAY 31 CONCURRENT LOAD TEST")
    print("=" * 60)

    start = time.perf_counter()

    results = []

    with ThreadPoolExecutor(
        max_workers=TOTAL_REQUESTS
    ) as executor:

        futures = [
            executor.submit(
                send_request,
                i + 1
            )
            for i in range(TOTAL_REQUESTS)
        ]

        for future in as_completed(futures):

            result = future.result()

            results.append(result)

            print(
                f"Request {result['request']}: "
                f"{'SUCCESS' if result['success'] else 'FAILED'} "
                f"| {result['latency']:.3f}s"
            )

    total_time = time.perf_counter() - start

    successful = sum(
        1 for result in results
        if result["success"]
    )

    failed = TOTAL_REQUESTS - successful

    latencies = [
        result["latency"]
        for result in results
    ]

    average_latency = (
        sum(latencies) / len(latencies)
        if latencies
        else 0
    )

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    print(f"Total requests:      {TOTAL_REQUESTS}")
    print(f"Successful:          {successful}")
    print(f"Failed:              {failed}")
    print(f"Total test time:     {total_time:.3f}s")
    print(f"Average latency:     {average_latency:.3f}s")


if __name__ == "__main__":
    main()