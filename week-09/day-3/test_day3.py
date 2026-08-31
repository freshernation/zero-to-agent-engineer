"""Week 9, Day 3 - RAG.

Run me:  pytest week-09/day-3 -v
"""

import pytest
from fake_model import FakeClient, text_reply

REFUSAL = "I don't know based on the documents I have."

RESULTS = [
    {"score": 0.31, "chunk": {
        "source": "expenses.md", "index": 2,
        "text": "Claims are submitted monthly and must be in by the fifth of the "
                "following month."}},
    {"score": 0.09, "chunk": {
        "source": "expenses.md", "index": 0,
        "text": "Expenses under two hundred pounds do not need pre-approval."}},
]


@pytest.fixture
def store(load, corpus_dir):
    loading = load("loading.py")
    chunking = load("chunking.py")
    documents = loading.load_documents(corpus_dir)
    chunks = loading.chunk_documents(
        documents, lambda t: chunking.sentence_chunks(t, 400, 1)
    )
    vector_store = load("store.py").VectorStore()
    vector_store.add(chunks)
    return vector_store


class TestPrompting:
    def test_system_demands_context_only(self, load):
        system = load("prompting.py").RAG_SYSTEM.lower()
        assert "only" in system, (
            "The system prompt has to say the answer must come from the context "
            "alone. A model asked about expenses will otherwise supply a "
            "plausible general answer, which is worse than none."
        )

    def test_system_names_the_refusal(self, load):
        assert REFUSAL in load("prompting.py").RAG_SYSTEM, (
            "Give the exact refusal sentence, so a refusal is recognisable in "
            "code rather than something you have to interpret."
        )

    def test_system_asks_for_citations(self, load):
        system = load("prompting.py").RAG_SYSTEM.lower()
        assert "cite" in system or "[" in system

    def test_citation_for(self, load):
        assert load("prompting.py").citation_for(RESULTS[0]["chunk"]) == (
            "[expenses.md#2]"
        )

    def test_format_context_labels_every_chunk(self, load):
        context = load("prompting.py").format_context(RESULTS)
        assert "[expenses.md#2]" in context
        assert "[expenses.md#0]" in context
        assert "fifth of the following month" in context

    def test_format_context_of_nothing(self, load):
        assert load("prompting.py").format_context([]) == ""

    def test_prompt_contains_the_question_and_the_context(self, load):
        prompt = load("prompting.py").build_rag_prompt("when are claims due", RESULTS)
        assert "when are claims due" in prompt
        assert "fifth of the following month" in prompt

    def test_prompt_fences_the_context(self, load):
        """The context is text you did not write. Fence it."""
        prompt = load("prompting.py").build_rag_prompt("q", RESULTS)
        assert "<context>" in prompt and "</context>" in prompt, (
            "Wrap the retrieved text in tags. It is untrusted input - a document "
            "containing 'ignore the above' should not be read as an instruction."
        )


class TestAnswer:
    def test_returns_the_models_answer(self, load, store):
        client = FakeClient([text_reply("The fifth. [expenses.md#2]")])
        result = load("rag.py").answer(client, store, "when are claims due")
        assert result["answer"] == "The fifth. [expenses.md#2]"

    def test_returns_what_was_retrieved(self, load, store):
        client = FakeClient([text_reply("ok")])
        result = load("rag.py").answer(client, store, "when are claims due", k=3)
        assert len(result["results"]) == 3
        assert "expenses.md" in result["sources"]

    def test_the_context_reached_the_model(self, load, store):
        client = FakeClient([text_reply("ok")])
        load("rag.py").answer(client, store, "when are expense claims due")
        sent = str(client.last_call["messages"])
        assert "fifth of the following month" in sent, (
            "The retrieved text never made it into the prompt. That is the whole "
            "of RAG - search results pasted into a prompt."
        )

    def test_k_controls_how_much_context(self, load, store):
        client = FakeClient([text_reply("ok")])
        result = load("rag.py").answer(client, store, "claims", k=1)
        assert len(result["results"]) == 1


class TestDecline:
    def test_answers_when_there_is_something(self, load, store):
        client = FakeClient([text_reply("The fifth. [expenses.md#2]")])
        result = load("rag.py").answer_or_decline(
            client, store, "when are expense claims due"
        )
        assert result["answer"] == "The fifth. [expenses.md#2]"

    def test_declines_without_calling_the_model(self, load, store):
        """Nothing scores, so there is nothing worth sending."""
        client = FakeClient([text_reply("I will invent something")])
        result = load("rag.py").answer_or_decline(
            client, store, "zzzzqqqq wwwwvvvv", min_score=0.01
        )
        assert result["answer"] == REFUSAL
        assert client.call_count == 0, (
            "The model was called with a context of noise. Check the top score "
            "first - it saves the call, saves the money, and removes the chance "
            "of an answer invented from nothing."
        )

    def test_declining_returns_no_sources(self, load, store):
        client = FakeClient([text_reply("x")])
        result = load("rag.py").answer_or_decline(
            client, store, "zzzzqqqq wwwwvvvv", min_score=0.01
        )
        assert result["sources"] == []


class TestCitations:
    def test_finds_citations(self, load):
        text = "Claims are due on the fifth [expenses.md#2] and need receipts [expenses.md#1]."
        assert load("rag.py").cited_sources(text) == [
            "expenses.md#2", "expenses.md#1",
        ]

    def test_no_repeats(self, load):
        text = "One [a.md#0] two [a.md#0] three [b.md#1]."
        assert load("rag.py").cited_sources(text) == ["a.md#0", "b.md#1"]

    def test_no_citations_at_all(self, load):
        assert load("rag.py").cited_sources("Just an answer.") == []

    def test_is_refusal(self, load):
        mod = load("rag.py")
        assert mod.is_refusal(REFUSAL) is True
        assert mod.is_refusal(f"  {REFUSAL}  ") is True
        assert mod.is_refusal("The fifth of the month.") is False


class TestEndToEnd:
    def test_a_real_question_retrieves_the_right_document(self, load, store):
        client = FakeClient([text_reply("ok")])
        result = load("rag.py").answer(client, store, "when are expense claims due")
        assert result["sources"][0] == "expenses.md"

    def test_another_one(self, load, store):
        client = FakeClient([text_reply("ok")])
        result = load("rag.py").answer(client, store, "how long is the on-call rotation")
        assert result["sources"][0] == "oncall.md"

    def test_and_another(self, load, store):
        client = FakeClient([text_reply("ok")])
        result = load("rag.py").answer(
            client, store, "how many reviewers does billing code need"
        )
        assert result["sources"][0] == "code_review.md"
