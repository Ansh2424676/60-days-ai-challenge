import time
from dataclasses import dataclass, field


@dataclass
class StepTiming:
    name: str
    start: float
    end: float

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class PipelineProfiler:
    timings: list[StepTiming] = field(default_factory=list)

    def start(self, step_name: str) -> float:
        start_time = time.perf_counter()
        print(f"[START] {step_name}")
        return start_time

    def end(self, step_name: str, start_time: float) -> float:
        end_time = time.perf_counter()

        timing = StepTiming(
            name=step_name,
            start=start_time,
            end=end_time,
        )

        self.timings.append(timing)

        print(
            f"[END] {step_name}: "
            f"{timing.duration:.4f}s"
        )

        return end_time

    def total_time(self) -> float:
        return sum(
            timing.duration
            for timing in self.timings
        )

    def breakdown(self) -> list[dict]:
        total = self.total_time()

        if total == 0:
            return []

        return [
            {
                "step": timing.name,
                "time_seconds": round(
                    timing.duration, 4
                ),
                "percentage": round(
                    (timing.duration / total) * 100,
                    2,
                ),
            }
            for timing in self.timings
        ]

    def print_report(self) -> None:
        print("\n" + "=" * 60)
        print("PIPELINE LATENCY REPORT")
        print("=" * 60)

        for item in self.breakdown():
            print(
                f"{item['step']:<25}"
                f"{item['time_seconds']:>8.4f}s "
                f"({item['percentage']:>6.2f}%)"
            )

        print("-" * 60)
        print(
            f"Total pipeline time: "
            f"{self.total_time():.4f}s"
        )
        print("=" * 60)