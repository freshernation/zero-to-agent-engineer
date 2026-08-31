"""Week 11, Day 3 - seeing inside a request.

Run me:  pytest week-11/day-3 -v

The tracer takes its clock as an argument, so these tests are not flaky.
"""

import json
import re

import pytest


class FakeClock:
    """Advances only when you tell it to."""

    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


@pytest.fixture
def clock():
    return FakeClock()


class TestRequestId:
    def test_shape(self, load):
        request_id = load("logs.py").new_request_id()
        assert re.fullmatch(r"[0-9a-f]{12}", request_id), (
            f"Got {request_id!r}. Twelve lowercase hex characters."
        )

    def test_different_every_time(self, load):
        mod = load("logs.py")
        assert len({mod.new_request_id() for _ in range(50)}) == 50


class TestRedact:
    def test_hides_a_secret(self, load):
        assert load("logs.py").redact({"api_key": "sk-real", "model": "x"}) == {
            "api_key": "****", "model": "x",
        }

    def test_case_insensitive(self, load):
        assert load("logs.py").redact({"API_KEY": "sk-real"})["API_KEY"] == "****"

    def test_nested(self, load):
        result = load("logs.py").redact({"headers": {"Authorization": "Bearer x"}})
        assert result["headers"]["Authorization"] == "****", (
            "A helpful log of the headers puts your key in the log service "
            "forever. Go into nested dicts."
        )

    def test_leaves_everything_else(self, load):
        fields = {"duration_ms": 12, "sources": ["a.md"], "nested": {"k": 1}}
        assert load("logs.py").redact(fields) == fields

    def test_custom_keys(self, load):
        result = load("logs.py").redact({"password": "hunter2"}, ("password",))
        assert result["password"] == "****"


class TestLogLine:
    def test_is_json(self, load):
        mod = load("logs.py")
        parsed = json.loads(mod.log_line("info", "answered", duration_ms=1200))
        assert parsed["level"] == "info"
        assert parsed["event"] == "answered"
        assert parsed["duration_ms"] == 1200

    def test_redacts(self, load):
        mod = load("logs.py")
        line = mod.log_line("debug", "calling", api_key="sk-real-key")
        assert "sk-real-key" not in line
        assert mod.parse(line)["api_key"] == "****"

    def test_round_trip(self, load):
        mod = load("logs.py")
        assert mod.parse(mod.log_line("info", "x", n=1))["n"] == 1


class TestTracer:
    def test_one_span(self, load, clock):
        tracer = load("tracer.py").Tracer("req-1", clock)
        with tracer.span("retrieve"):
            clock.advance(0.140)
        spans = tracer.to_dict()["spans"]
        assert len(spans) == 1
        assert spans[0]["name"] == "retrieve"
        assert spans[0]["duration_ms"] == 140

    def test_request_id_is_carried(self, load, clock):
        tracer = load("tracer.py").Tracer("req-1", clock)
        with tracer.span("x"):
            pass
        assert tracer.to_dict()["request_id"] == "req-1"

    def test_two_top_level_spans(self, load, clock):
        tracer = load("tracer.py").Tracer("req-1", clock)
        with tracer.span("retrieve"):
            clock.advance(0.140)
        with tracer.span("generate"):
            clock.advance(1.090)
        spans = tracer.to_dict()["spans"]
        assert [s["name"] for s in spans] == ["retrieve", "generate"]
        assert [s["duration_ms"] for s in spans] == [140, 1090]

    def test_nesting(self, load, clock):
        tracer = load("tracer.py").Tracer("req-1", clock)
        with tracer.span("retrieve"):
            with tracer.span("embed"):
                clock.advance(0.012)
            with tracer.span("search"):
                clock.advance(0.126)
        spans = tracer.to_dict()["spans"]
        assert len(spans) == 1, "embed and search go INSIDE retrieve."
        children = spans[0]["children"]
        assert [c["name"] for c in children] == ["embed", "search"]
        assert spans[0]["duration_ms"] == 138

    def test_metadata(self, load, clock):
        tracer = load("tracer.py").Tracer("req-1", clock)
        with tracer.span("retrieve", k=3) as span:
            span.set("chunks", 7)
        metadata = tracer.to_dict()["spans"][0]["metadata"]
        assert metadata["k"] == 3
        assert metadata["chunks"] == 7

    def test_total(self, load, clock):
        tracer = load("tracer.py").Tracer("req-1", clock)
        with tracer.span("a"):
            clock.advance(0.1)
        with tracer.span("b"):
            clock.advance(0.2)
        assert tracer.total_ms() == 300

    def test_flatten(self, load, clock):
        tracer = load("tracer.py").Tracer("req-1", clock)
        with tracer.span("request"):
            with tracer.span("retrieve"):
                clock.advance(0.14)
            with tracer.span("generate"):
                clock.advance(1.09)
        assert load("tracer.py") and tracer.flatten() == [
            (0, "request", 1230), (1, "retrieve", 140), (1, "generate", 1090),
        ]

    def test_slowest(self, load, clock):
        tracer = load("tracer.py").Tracer("req-1", clock)
        with tracer.span("retrieve"):
            clock.advance(0.14)
        with tracer.span("generate"):
            clock.advance(1.09)
        assert tracer.slowest() == "generate"

    def test_slowest_of_nothing(self, load, clock):
        assert load("tracer.py").Tracer("req-1", clock).slowest() is None


class TestTracingFailures:
    def test_a_raising_span_is_still_recorded(self, load, clock):
        """The runs you most want to see are the ones that went wrong."""
        tracer = load("tracer.py").Tracer("req-1", clock)
        with pytest.raises(ValueError):
            with tracer.span("generate"):
                clock.advance(0.05)
                raise ValueError("model unavailable")

        spans = tracer.to_dict()["spans"]
        assert len(spans) == 1, (
            "The span vanished when its body raised. A tracer that loses data "
            "on failure is missing exactly the runs you care about."
        )
        assert spans[0]["duration_ms"] == 50
        assert "model unavailable" in spans[0]["metadata"]["error"]

    def test_the_exception_still_propagates(self, load, clock):
        tracer = load("tracer.py").Tracer("req-1", clock)
        with pytest.raises(ValueError):
            with tracer.span("x"):
                raise ValueError("boom")

    def test_nesting_recovers_after_a_failure(self, load, clock):
        tracer = load("tracer.py").Tracer("req-1", clock)
        with tracer.span("request"):
            try:
                with tracer.span("generate"):
                    raise ValueError("boom")
            except ValueError:
                pass
            with tracer.span("fallback"):
                clock.advance(0.01)
        children = tracer.to_dict()["spans"][0]["children"]
        assert [c["name"] for c in children] == ["generate", "fallback"], (
            "After a span failed, the next one was not nested correctly - the "
            "failed span was never popped off the stack."
        )
