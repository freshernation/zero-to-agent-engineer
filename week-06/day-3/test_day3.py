"""Week 6, Day 3 - structured output.

Run me:  pytest week-06/day-3 -v
"""

import pytest
from fake_model import FakeClient, text_reply
from pydantic import ValidationError

GOOD = '{"name": "Ana Silva", "email": "ana@example.com", "company": null}'
WRAPPED = f"Here's the extracted data:\n\n```json\n{GOOD}\n```\n\nLet me know!"
BAD_JSON = "Here you go: {name: Ana, email}"
WRONG_SHAPE = '{"name": "Ana Silva", "emial": "ana@example.com"}'


class TestExtractJson:
    def test_plain_json(self, load):
        assert load("extract.py").extract_json(GOOD) == GOOD

    def test_json_wrapped_in_prose_and_fences(self, load):
        extracted = load("extract.py").extract_json(WRAPPED)
        assert extracted is not None
        assert extracted.startswith("{") and extracted.endswith("}")

    def test_no_json_at_all(self, load):
        assert load("extract.py").extract_json("I cannot help with that.") is None

    def test_unbalanced(self, load):
        assert load("extract.py").extract_json("} something {") is None

    def test_parse_json_good(self, load):
        assert load("extract.py").parse_json(WRAPPED)["name"] == "Ana Silva"

    def test_parse_json_bad(self, load):
        assert load("extract.py").parse_json(BAD_JSON) is None

    def test_parse_json_nothing(self, load):
        assert load("extract.py").parse_json("no json here") is None

    def test_strip_fences(self, load):
        stripped = load("extract.py").strip_fences("```json\n{\"a\": 1}\n```")
        assert "```" not in stripped
        assert "{" in stripped


class TestModels:
    def test_contact(self, load):
        Contact = load("models.py").Contact
        c = Contact(name="Ana", email="ana@example.com")
        assert c.company is None

    @pytest.mark.parametrize("kwargs", [
        {"name": "", "email": "a@b.com"},
        {"name": "Ana", "email": "nope"},
    ])
    def test_contact_rejects(self, load, kwargs):
        Contact = load("models.py").Contact
        with pytest.raises(ValidationError):
            Contact(**kwargs)

    def test_product(self, load):
        Product = load("models.py").Product
        assert Product(name="Widget", price=4.5, in_stock=True).price == 4.5

    def test_product_rejects_free_things(self, load):
        Product = load("models.py").Product
        with pytest.raises(ValidationError):
            Product(name="Widget", price=0, in_stock=True)

    @pytest.mark.parametrize("rating", [1, 3, 5])
    def test_review_accepts_valid_ratings(self, load, rating):
        Review = load("models.py").Review
        assert Review(rating=rating, summary="ok", sentiment="neutral").rating == rating

    @pytest.mark.parametrize("rating", [0, 6, -1])
    def test_review_rejects_ratings_out_of_range(self, load, rating):
        Review = load("models.py").Review
        with pytest.raises(ValidationError):
            Review(rating=rating, summary="ok", sentiment="neutral")

    def test_review_rejects_an_invented_sentiment(self, load):
        Review = load("models.py").Review
        with pytest.raises(ValidationError):
            Review(rating=3, summary="ok", sentiment="mixed")


class TestExtractionSystem:
    def test_names_every_field(self, load):
        Contact = load("models.py").Contact
        system = load("structured.py").build_extraction_system(Contact)
        for field in ("name", "email", "company"):
            assert field in system, (
                f"The system prompt does not mention '{field}'. "
                "model_class.model_fields gives you the names."
            )

    def test_says_json_only(self, load):
        Contact = load("models.py").Contact
        system = load("structured.py").build_extraction_system(Contact).lower()
        assert "json" in system


class TestExtractOne:
    def test_clean_reply(self, load):
        Contact = load("models.py").Contact
        client = FakeClient([text_reply(GOOD)])
        contact = load("structured.py").extract_one(client, "any text", Contact)
        assert contact.name == "Ana Silva"
        assert contact.company is None

    def test_wrapped_reply(self, load):
        Contact = load("models.py").Contact
        client = FakeClient([text_reply(WRAPPED)])
        contact = load("structured.py").extract_one(client, "any text", Contact)
        assert contact is not None, (
            "The model wrapped the JSON in prose and a code fence, which it does "
            "constantly. First { to last } handles it."
        )
        assert contact.email == "ana@example.com"

    def test_unparseable_reply(self, load):
        Contact = load("models.py").Contact
        client = FakeClient([text_reply(BAD_JSON)])
        assert load("structured.py").extract_one(client, "x", Contact) is None

    def test_valid_json_of_the_wrong_shape(self, load):
        """The dangerous case: it parses, and it is useless."""
        Contact = load("models.py").Contact
        client = FakeClient([text_reply(WRONG_SHAPE)])
        assert load("structured.py").extract_one(client, "x", Contact) is None, (
            "'emial' is valid JSON and the wrong data. json.loads says yes; "
            "only validation says no."
        )

    def test_uses_temperature_zero(self, load):
        Contact = load("models.py").Contact
        client = FakeClient([text_reply(GOOD)])
        load("structured.py").extract_one(client, "x", Contact)
        assert client.last_call.get("temperature") == 0


class TestExtractWithRetry:
    def test_first_try(self, load):
        Contact = load("models.py").Contact
        client = FakeClient([text_reply(GOOD)])
        result = load("structured.py").extract_with_retry(client, "x", Contact)
        assert result.name == "Ana Silva"
        assert client.call_count == 1

    def test_recovers_on_the_second_go(self, load):
        Contact = load("models.py").Contact
        client = FakeClient([text_reply(BAD_JSON), text_reply(GOOD)])
        result = load("structured.py").extract_with_retry(client, "x", Contact)
        assert result is not None and result.name == "Ana Silva"

    def test_gives_up(self, load):
        Contact = load("models.py").Contact
        client = FakeClient([text_reply(BAD_JSON)] * 3)
        assert load("structured.py").extract_with_retry(
            client, "x", Contact, attempts=3
        ) is None

    def test_attempts_taken(self, load):
        Contact = load("models.py").Contact
        client = FakeClient([text_reply(BAD_JSON), text_reply(BAD_JSON),
                             text_reply(GOOD)])
        assert load("structured.py").attempts_taken(client, "x", Contact) == 3

    def test_the_retry_tells_the_model_what_was_wrong(self, load):
        Contact = load("models.py").Contact
        client = FakeClient([text_reply(BAD_JSON), text_reply(GOOD)])
        load("structured.py").extract_with_retry(client, "x", Contact)
        first = str(client.calls[0]["messages"])
        second = str(client.calls[1]["messages"])
        assert first != second, (
            "The second attempt sent exactly the same prompt as the first. "
            "Feed the error back - a model told 'that was not valid JSON' "
            "usually fixes it, and one told nothing usually repeats itself."
        )
