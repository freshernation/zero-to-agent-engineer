"""Week 5, Day 1 - HTTP and requests.

Run me:  pytest week-05/day-1 -v

The practice API starts automatically. You do not have to run server.py yourself
for the tests, only when you want to poke at it by hand.
"""

import pytest


class TestFetch:
    def test_get_users(self, load, base_url):
        users = load("fetch.py").get_users(base_url)
        assert isinstance(users, list), (
            f"Expected a list of users, got {type(users).__name__}. "
            "Did you return the response object instead of response.json()?"
        )
        assert len(users) == 4
        assert users[0]["name"] == "Ana Silva"

    def test_get_user(self, load, base_url):
        user = load("fetch.py").get_user(base_url, 2)
        assert user["name"] == "Ben Okafor"
        assert user["city"] == "Lagos"

    def test_get_user_missing_returns_none(self, load, base_url):
        result = load("fetch.py").get_user(base_url, 99)
        assert result is None, (
            f"Got {result!r}. A 404 does not raise - requests hands you a "
            "perfectly good response with status_code 404 and an error body. "
            "Check the status code yourself."
        )

    def test_get_products_all(self, load, base_url):
        products = load("fetch.py").get_products(base_url)
        assert len(products) == 4

    @pytest.mark.parametrize("category,count", [("tools", 2), ("toys", 2), ("nope", 0)])
    def test_get_products_filtered(self, load, base_url, category, count):
        products = load("fetch.py").get_products(base_url, category)
        assert len(products) == count
        assert all(p["category"] == category for p in products)

    def test_uses_params_not_string_building(self, source):
        code = source("fetch.py", code_only=True)
        assert "params" in code, (
            "Use params={...} rather than building the query string with an "
            "f-string. params escapes spaces and symbols that would otherwise "
            "quietly corrupt the URL."
        )

    def test_passes_a_timeout(self, source):
        code = source("fetch.py", code_only=True)
        assert "timeout" in code, (
            "No timeout= anywhere. A request without one waits forever, which "
            "is how a program hangs at 3am with nothing in the logs."
        )


class TestStatus:
    @pytest.mark.parametrize("path,code", [
        ("/users", 200),
        ("/users/1", 200),
        ("/users/99", 404),
        ("/error", 500),
        ("/nothing-here", 404),
    ])
    def test_status_of(self, load, base_url, path, code):
        assert load("status.py").status_of(base_url, path) == code

    @pytest.mark.parametrize("path,ok", [
        ("/users", True),
        ("/users/99", False),
        ("/error", False),
    ])
    def test_is_ok(self, load, base_url, path, ok):
        assert load("status.py").is_ok(base_url, path) is ok

    def test_is_ok_accepts_any_2xx(self, load, source):
        """201 and 204 are successes too."""
        code = source("status.py", code_only=True)
        load("status.py").is_ok
        assert "== 200" not in code.replace(" ", " ") or "< 300" in code or "300" in code, (
            "is_ok checks for exactly 200. A 201 Created and a 204 No Content "
            "are successes too - the rule is 'any 2xx', so compare a range."
        )

    def test_fetch_json_good(self, load, base_url):
        assert len(load("status.py").fetch_json(base_url, "/users")) == 4

    @pytest.mark.parametrize("path", ["/users/99", "/error"])
    def test_fetch_json_bad(self, load, base_url, path):
        assert load("status.py").fetch_json(base_url, path) is None


class TestCareful:
    def test_fetch_with_timeout_fast_enough(self, load, base_url):
        result = load("careful.py").fetch_with_timeout(base_url, "/users", 5)
        assert isinstance(result, list) and len(result) == 4

    def test_fetch_with_timeout_too_slow(self, load, base_url):
        """/slow takes three seconds. One is not enough."""
        result = load("careful.py").fetch_with_timeout(base_url, "/slow", 1)
        assert result == "timed out", (
            f"Got {result!r}. Catch requests.exceptions.Timeout and return "
            '"timed out".'
        )

    def test_get_secret_with_the_right_key(self, load, base_url):
        result = load("careful.py").get_secret(base_url, "course-key-123")
        assert result["message"] == "You found the secret"

    @pytest.mark.parametrize("key", ["wrong", "", "course-key-124"])
    def test_get_secret_with_a_bad_key(self, load, base_url, key):
        assert load("careful.py").get_secret(base_url, key) is None

    def test_sends_a_bearer_header(self, source):
        code = source("careful.py", code_only=True)
        assert "Authorization" in code and "Bearer" in code, (
            "The API wants an Authorization header of 'Bearer <key>'."
        )
