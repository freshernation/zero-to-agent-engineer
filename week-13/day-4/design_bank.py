"""Gate-5 prompts and what a good answer contains. Given to you.

Junior system design is not capacity planning. Nobody expects you to size a
database. What they are checking is whether you can name the components, say how
data moves between them, and — the part that separates candidates — say what
goes wrong and how you would know.

Answer two of these in DESIGNS.md.
"""

PROMPTS = [
    {
        "id": "support_bot",
        "prompt": (
            "Design a support bot that answers customer questions from our help "
            "centre articles."
        ),
        "must_cover": [
            ("chunk", "split"),
            ("retriev", "search", "embed"),
            ("prompt", "context"),
            ("refus", "don't know", "do not know", "no answer"),
            ("evaluat", "measure", "hit rate", "golden"),
        ],
    },
    {
        "id": "ticket_triage",
        "prompt": (
            "Design a system that reads incoming support tickets and routes each "
            "one to the right team."
        ),
        "must_cover": [
            ("classif", "categor", "label"),
            ("structured", "json", "schema", "validat"),
            ("confiden", "uncertain", "threshold", "unsure"),
            ("human", "escalat", "review"),
            ("evaluat", "measure", "accuracy", "golden"),
        ],
    },
    {
        "id": "doc_summariser",
        "prompt": (
            "Design a service that produces a one-page summary of a long PDF "
            "report."
        ),
        "must_cover": [
            ("chunk", "split", "section"),
            ("context window", "too long", "limit"),
            ("cost", "token", "expensive"),
            ("quality", "judge", "evaluat", "measure"),
            ("fail", "wrong", "hallucin", "error"),
        ],
    },
]


def by_id(prompt_id):
    """Return one prompt, or None."""
    for prompt in PROMPTS:
        if prompt["id"] == prompt_id:
            return prompt
    return None
