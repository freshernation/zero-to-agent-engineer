"""Project 3 - the deployed assistant.

Run me:  pytest week-11/milestone -v

Everything runs in-process against a scripted model. No key, no network, no cost.
"""

import re

import pytest
from fake_model import FakeClient, text_reply
from fastapi.testclient import TestClient


def _instructions_removed(text, name):
    """Comment lines are the stub's instructions - and they mention the very
    things these tests look for. Check the real content only."""
    body = "\n".join(
        line for line in text.splitlines() if not line.strip().startswith("#")
    )
    assert body.strip(), (
        f"{name} contains only comments so far - write it."
    )
    return body


SETTINGS = {
    "version": "1.0.0",
    "max_question_length": 200,
    "daily_budget": 1.00,
}


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        self.now += 0.01
        return self.now


@pytest.fixture
def assistant(load, corpus_dir):
    return load("pipeline.py").Assistant(corpus_dir).build()


@pytest.fixture
def client_factory(load, assistant):
    def _make(model_client=None, settings=None):
        model_client = model_client or FakeClient(
            text_reply("The fifth. [expenses.md#1]")
        )
        return TestClient(
            load("app.py").create_app(
                assistant, model_client, {**SETTINGS, **(settings or {})}
            )
        )

    return _make


@pytest.fixture
def api(client_factory):
    return client_factory()


class TestAssistant:
    def test_indexes_the_corpus(self, assistant):
        assert assistant.chunk_count > 6
        assert "expenses.md" in assistant.sources

    def test_answers(self, assistant):
        client = FakeClient([text_reply("The fifth. [expenses.md#1]")])
        result = assistant.answer(
            client, "when must expense claims be submitted", "req-1", Clock()
        )
        assert result["refused"] is False
        assert "expenses.md" in result["sources"]
        assert result["request_id"] == "req-1"

    def test_refuses_without_calling_the_model(self, assistant):
        client = FakeClient([text_reply("I would invent something")])
        result = assistant.answer(client, "zzzzqqq wwwwvvv", "req-1", Clock())
        assert result["refused"] is True
        assert client.call_count == 0

    def test_traces_both_stages(self, assistant):
        client = FakeClient([text_reply("ok")])
        result = assistant.answer(
            client, "when must expense claims be submitted", "req-1", Clock()
        )
        names = {span["name"] for span in result["trace"]["spans"]}
        assert {"retrieve", "generate"} <= names, (
            f"Spans were {names}. Trace both stages - 'it is slow' has to become "
            "'generation is 88% of it'."
        )

    def test_reports_a_duration(self, assistant):
        client = FakeClient([text_reply("ok")])
        result = assistant.answer(client, "expense claims", "req-1", Clock())
        assert isinstance(result["duration_ms"], int)

    def test_a_refusal_is_still_traced(self, assistant):
        client = FakeClient([text_reply("x")])
        result = assistant.answer(client, "zzzzqqq wwwwvvv", "req-1", Clock())
        assert result["trace"]["spans"], (
            "A refused request produced no trace at all. Those are exactly the "
            "ones you want to look at later."
        )


class TestHealthAndReady:
    def test_health(self, api):
        response = api.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["version"] == "1.0.0"
        assert isinstance(body["uptime_seconds"], int)

    def test_ready(self, api):
        body = api.get("/ready").json()
        assert body["ready"] is True
        assert body["failing"] == []

    def test_sources(self, api):
        sources = api.get("/sources").json()
        assert "expenses.md" in sources


class TestAsk:
    def test_answers(self, api):
        response = api.post(
            "/ask", json={"question": "when must expense claims be submitted"}
        )
        assert response.status_code == 200
        body = response.json()
        assert body["refused"] is False
        assert body["sources"]

    def test_request_id_in_body_and_header(self, api):
        response = api.post("/ask", json={"question": "expense claims"})
        body = response.json()
        assert re.fullmatch(r"[0-9a-f]{12}", body["request_id"]), (
            f"request_id was {body.get('request_id')!r}."
        )
        assert response.headers.get("X-Request-ID") == body["request_id"], (
            "The id has to be in the header too - that is how somebody with a "
            "failing request tells you which one it was."
        )

    def test_a_different_id_every_time(self, api):
        first = api.post("/ask", json={"question": "expense claims"}).json()
        second = api.post("/ask", json={"question": "expense claims"}).json()
        assert first["request_id"] != second["request_id"]

    def test_refusal_comes_through(self, api):
        body = api.post("/ask", json={"question": "zzzzqqq wwwwvvv"}).json()
        assert body["refused"] is True

    def test_validation_still_applies(self, api):
        assert api.post("/ask", json={}).status_code == 422


class TestGuards:
    def test_too_long_is_413(self, client_factory):
        api = client_factory(settings={"max_question_length": 50})
        response = api.post("/ask", json={"question": "x" * 60})
        assert response.status_code == 413, (
            f"Got {response.status_code}. A question over the limit is the "
            "caller's problem and 413 says which problem."
        )

    def test_budget_exhausted_is_429(self, client_factory):
        api = client_factory(settings={"daily_budget": 0.0})
        response = api.post("/ask", json={"question": "expense claims"})
        assert response.status_code == 429, (
            f"Got {response.status_code}. When the budget is gone, say so - a "
            "service that silently stops answering is worse than one that "
            "explains."
        )

    def test_no_traceback_ever(self, client_factory):
        exploding = FakeClient([Exception("model on fire")])
        api = client_factory(model_client=exploding)
        response = api.post("/ask", json={"question": "expense claims"})
        assert response.status_code in (200, 500, 503)
        assert "Traceback" not in response.text


class TestEvaluateScript:
    def test_runs_and_reports(self, run):
        result = run("evaluate.py", allow_crash=True)
        assert "hit_rate" in result.stdout
        assert "GATE" in result.stdout

    def test_exits_zero_when_it_passes(self, run):
        result = run("evaluate.py", allow_crash=True)
        if "GATE PASSED" in result.stdout:
            assert result.code == 0
        else:
            assert result.code != 0, (
                "The gate failed and the script exited 0. That exit code is what "
                "a deploy pipeline reads - it has to be non-zero."
            )


class TestDeploymentFiles:
    def test_dockerfile(self, source):
        dockerfile = _instructions_removed(source("Dockerfile"), "Dockerfile")
        assert "FROM python" in dockerfile
        assert "0.0.0.0" in dockerfile
        assert "PORT" in dockerfile
        lines = [ln.strip() for ln in dockerfile.splitlines() if ln.strip()]
        install = next((i for i, ln in enumerate(lines) if "pip install" in ln), None)
        copy_all = next(
            (i for i, ln in enumerate(lines) if ln.startswith("COPY . ")), None
        )
        assert install is not None and copy_all is not None and install < copy_all

    def test_env_example(self, source):
        example = _instructions_removed(source(".env.example"), ".env.example")
        assert "ANTHROPIC_API_KEY" in example
        assert "sk-ant-" not in example


class TestDocuments:
    README_HEADINGS = [
        "What it is", "Try it", "How it works",
        "Running it yourself", "How I know it works", "What I would do next",
    ]
    DEPLOY_HEADINGS = ["Where it runs", "Configuration", "What I would change"]

    @pytest.mark.parametrize("heading", README_HEADINGS)
    def test_readme_section(self, source, heading):
        text = source("PROJECT_README.md")
        assert f"## {heading}" in text, f"No '{heading}' section."
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 20, f"'{heading}' is too short."

    def test_readme_has_a_url(self, source):
        text = source("PROJECT_README.md")
        assert re.search(r"https?://", text), (
            "No URL anywhere. The live link is the whole point of this project - "
            "it is the only one an interviewer can try without cloning anything."
        )

    def test_readme_has_the_eval_numbers(self, source):
        section = source("PROJECT_README.md").split("How I know it works")[-1]
        assert re.search(r"\d", section.split("\n## ")[0]), (
            "The 'How I know it works' section has no numbers in it. That "
            "section is what gets you asked good questions."
        )

    @pytest.mark.parametrize("heading", DEPLOY_HEADINGS)
    def test_deployment_section(self, source, heading):
        text = source("DEPLOYMENT.md")
        assert f"## {heading}" in text
        body = text.split(f"## {heading}", 1)[1].split("\n## ")[0]
        assert len(body.split()) >= 25

    def test_instructions_removed(self, source):
        assert "<!--" not in source("PROJECT_README.md")
        assert "<!--" not in source("DEPLOYMENT.md")
