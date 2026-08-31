"""Week 11, Day 1 - behind an API.

Run me:  pytest week-11/day-1 -v

TestClient runs the app in-process. No server, no port, no network.
"""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError


def fake_answerer(question, k):
    return {
        "answer": f"answered {question} with k={k}",
        "sources": ["expenses.md"],
        "refused": False,
    }


def refusing_answerer(question, k):
    return {"answer": "I don't know.", "sources": [], "refused": True}


@pytest.fixture
def client(load):
    return TestClient(load("service.py").create_app(fake_answerer))


class TestModels:
    def test_ask_request_defaults(self, load):
        request = load("models.py").AskRequest(question="hi")
        assert request.k == 3

    @pytest.mark.parametrize("kwargs", [
        {"question": ""},
        {"question": "x" * 501},
        {"question": "hi", "k": 0},
        {"question": "hi", "k": 11},
    ])
    def test_ask_request_rejects(self, load, kwargs):
        with pytest.raises(ValidationError):
            load("models.py").AskRequest(**kwargs)

    def test_ask_response(self, load):
        response = load("models.py").AskResponse(
            answer="a", sources=["x.md"], refused=False
        )
        assert response.sources == ["x.md"]

    def test_health_response(self, load):
        assert load("models.py").HealthResponse(status="ok", documents=6).documents == 6


class TestHealth:
    def test_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_reports_a_document_count(self, client):
        assert isinstance(client.get("/health").json()["documents"], int)


class TestAsk:
    def test_answers(self, client):
        response = client.post("/ask", json={"question": "when are claims due"})
        assert response.status_code == 200
        body = response.json()
        assert "when are claims due" in body["answer"]
        assert body["refused"] is False

    def test_uses_the_k_it_was_given(self, client):
        body = client.post("/ask", json={"question": "hi", "k": 7}).json()
        assert "k=7" in body["answer"]

    def test_default_k(self, client):
        assert "k=3" in client.post("/ask", json={"question": "hi"}).json()["answer"]

    def test_returns_sources(self, client):
        assert client.post("/ask", json={"question": "hi"}).json()["sources"] == [
            "expenses.md"
        ]

    def test_a_refusal_comes_through(self, load):
        client = TestClient(load("service.py").create_app(refusing_answerer))
        body = client.post("/ask", json={"question": "hi"}).json()
        assert body["refused"] is True


class TestValidation:
    @pytest.mark.parametrize("payload", [
        {},
        {"question": ""},
        {"question": "x" * 501},
        {"question": "hi", "k": 0},
        {"question": "hi", "k": 99},
        {"question": 5},
    ])
    def test_bad_input_is_rejected_before_your_code_runs(self, client, payload):
        response = client.post("/ask", json=payload)
        assert response.status_code == 422, (
            f"{payload} got {response.status_code}. FastAPI rejects anything the "
            "model refuses, and you write no code for it - that is the whole "
            "point of declaring the request as a model."
        )

    def test_the_error_names_the_field(self, client):
        detail = client.post("/ask", json={}).json()["detail"]
        assert any("question" in str(item) for item in detail)


class TestSources:
    def test_lists_documents(self, client):
        response = client.get("/sources")
        assert response.status_code == 200
        assert isinstance(response.json(), (list, dict))


class TestInjection:
    def test_the_answerer_is_injected(self, load):
        """Two apps, two answerers, no global state."""
        mod = load("service.py")
        first = TestClient(mod.create_app(fake_answerer))
        second = TestClient(mod.create_app(refusing_answerer))
        assert first.post("/ask", json={"question": "hi"}).json()["refused"] is False
        assert second.post("/ask", json={"question": "hi"}).json()["refused"] is True

    def test_default_answerer_works_alone(self, load):
        """The app has to run with nothing else wired up."""
        client = TestClient(load("service.py").create_app(
            load("service.py").default_answerer
        ))
        assert client.post("/ask", json={"question": "hi"}).status_code == 200
