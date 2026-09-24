from backend.profiler import PipelineProfiler


def test_profiler_records_timing():
    profiler = PipelineProfiler()

    with profiler.measure("embedding"):
        sum(range(10000))

    assert len(profiler.timings) == 1
    assert profiler.timings[0].name == "embedding"
    assert profiler.timings[0].duration >= 0


def test_profiler_breakdown():
    profiler = PipelineProfiler()

    with profiler.measure("embedding"):
        sum(range(10000))

    with profiler.measure("faiss_search"):
        sum(range(10000))

    breakdown = profiler.breakdown()

    assert len(breakdown) == 2
    assert abs(sum(item["percentage"] for item in breakdown) - 100) < 0.01