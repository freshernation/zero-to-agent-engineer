"""The concept bank. Given to you.

Twelve questions you will be asked in a gate-3 round, each with the ideas an
answer has to contain to be a real answer rather than a definition.

`must_mention` is not a list of magic words - it is the set of things somebody
who understands the idea would inevitably say. Each entry is a tuple of
acceptable ways to say it, so "a list of numbers" counts as much as "vector".
If your answer contains none of them, it is probably a definition you have read
rather than an explanation you own.

Answer every one in ANSWERS.md, out loud first, in about thirty seconds each.
"""

CONCEPTS = [
    {
        "id": "token",
        "question": "What is a token?",
        "must_mention": [("word",), ("cost", "pay", "price"), ("context",)],
    },
    {
        "id": "context_window",
        "question": "What is a context window, and why does a long chat get expensive?",
        "must_mention": [("limit", "maximum"), ("history", "conversation"),
                          ("resend", "send it again", "sent again", "every turn")],
    },
    {
        "id": "rag",
        "question": "What is RAG, and why would you use it instead of fine-tuning?",
        "must_mention": [("retriev", "search", "find"), ("prompt",),
                          ("document", "your own data", "private")],
    },
    {
        "id": "tool_calling",
        "question": "How does tool calling actually work?",
        "must_mention": [("schema", "description of my function"),
                          ("asks", "requests", "emit"),
                          ("my code", "i run", "my loop", "i call")],
    },
    {
        "id": "iteration_cap",
        "question": "Why does an agent loop need a cap?",
        "must_mention": [("forever", "never stop", "runaway"),
                          ("cost", "money", "bill"), ("stop", "cap", "limit")],
    },
    {
        "id": "chunking",
        "question": "What is chunking, and how do you choose a chunk size?",
        "must_mention": [("retriev", "fetch"), ("boundar", "cut", "split"),
                          ("measure", "hit rate", "evaluat")],
    },
    {
        "id": "embedding",
        "question": "What is an embedding?",
        "must_mention": [("vector", "list of numbers", "numbers"),
                          ("meaning", "semantic"), ("similar", "close", "cosine")],
    },
    {
        "id": "rag_eval",
        "question": "How would you know whether your retrieval is any good?",
        "must_mention": [("golden", "test set", "question set"),
                          ("hit rate", "recall", "precision"),
                          ("before", "compare", "baseline")],
    },
    {
        "id": "temperature",
        "question": "What does temperature do, and when do you set it to zero?",
        "must_mention": [("random", "varie", "consistent"), ("zero", "0"),
                          ("pars", "structured", "json", "classif")],
    },
    {
        "id": "structured_output",
        "question": "Why validate a model's JSON rather than just parsing it?",
        "must_mention": [("valid",), ("key", "field", "shape"),
                          ("pydantic", "model", "validat")],
    },
    {
        "id": "prompt_injection",
        "question": "What is prompt injection, and what do you do about it?",
        "must_mention": [("instruction",), ("untrusted", "did not write", "someone else"),
                          ("fence", "delimit", "tag")],
    },
    {
        "id": "multi_agent",
        "question": "When would you use several agents instead of one?",
        "must_mention": [("tool",), ("permission", "security", "access"),
                          ("default", "rarely", "one agent")],
    },
]


def by_id(concept_id):
    """Return one concept, or None."""
    for concept in CONCEPTS:
        if concept["id"] == concept_id:
            return concept
    return None


def questions():
    """Return just the questions, for quizzing yourself."""
    return [concept["question"] for concept in CONCEPTS]
