import pytest

from app.circuit_breaker import CircuitBreaker


def failing_function():
    raise RuntimeError("OpenAI API failed")


def successful_function():
    return "success"


def test_circuit_opens_after_three_failures():

    breaker = CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=60,
    )

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.call(failing_function)

    assert breaker.state == "OPEN"
    assert breaker.failure_count == 3


def test_open_circuit_blocks_request():

    breaker = CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=60,
    )

    for _ in range(3):
        with pytest.raises(RuntimeError):
            breaker.call(failing_function)

    with pytest.raises(RuntimeError, match="Service temporarily unavailable"):
        breaker.call(successful_function)


def test_success_resets_failure_count():

    breaker = CircuitBreaker(
        failure_threshold=3,
        recovery_timeout=60,
    )

    with pytest.raises(RuntimeError):
        breaker.call(failing_function)

    assert breaker.failure_count == 1

    result = breaker.call(successful_function)

    assert result == "success"
    assert breaker.failure_count == 0
    assert breaker.state == "CLOSED"