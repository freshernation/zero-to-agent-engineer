"""Week 5, Day 3 - secrets, retries, and a client.

Run me:  pytest week-05/day-3 -v
"""

import pytest


class TestConfig:
    def test_get_api_key(self, load, monkeypatch):
        monkeypatch.setenv("COURSE_API_KEY", "abc123")
        assert load("config.py").get_api_key() == "abc123"

    def test_missing_key_says_which_one(self, load, monkeypatch):
        monkeypatch.delenv("COURSE_API_KEY", raising=False)
        with pytest.raises(RuntimeError) as caught:
            load("config.py").get_api_key()
        assert "COURSE_API_KEY" in str(caught.value), (
            f"The message was '{caught.value}'. Name the variable - whoever "
            "hits this needs to know what to set."
        )

    def test_empty_key_counts_as_missing(self, load, monkeypatch):
        monkeypatch.setenv("COURSE_API_KEY", "")
        with pytest.raises(RuntimeError):
            load("config.py").get_api_key()

    def test_base_url_default(self, load, monkeypatch):
        monkeypatch.delenv("API_BASE_URL", raising=False)
        assert load("config.py").get_base_url() == "http://127.0.0.1:8765"

    def test_base_url_from_env(self, load, monkeypatch):
        monkeypatch.setenv("API_BASE_URL", "https://example.com")
        assert load("config.py").get_base_url() == "https://example.com"

    def test_load_config(self, load, monkeypatch):
        monkeypatch.setenv("COURSE_API_KEY", "abc123")
        monkeypatch.setenv("API_BASE_URL", "https://example.com")
        config = load("config.py").load_config()
        assert config["api_key"] == "abc123"
        assert config["base_url"] == "https://example.com"

    def test_no_key_in_the_source(self, load, source):
        load("config.py").get_base_url  # nothing to check until it exists
        code = source("config.py", code_only=True)
        assert "course-key-123" not in code, (
            "There is a real key in your source. Keys live in the environment - "
            "git keeps history, so a key committed once is committed forever."
        )


class TestShouldRetry:
    @pytest.mark.parametrize("code,retry", [
        (500, True), (502, True), (503, True),
        (200, False), (201, False), (400, False),
        (401, False), (404, False), (429, False),
    ])
    def test_only_5xx(self, load, code, retry):
        assert load("retry.py").should_retry(code) is retry, (
            f"{code}: a 4xx is your problem and will still be a 4xx in a "
            "second. Retrying it wastes your time and their capacity."
        )


class TestRetry:
    def test_succeeds_first_time_on_a_good_endpoint(self, load, base_url):
        result = load("retry.py").fetch_with_retry(base_url, "/users")
        assert isinstance(result, list) and len(result) == 4

    def test_uses_one_attempt_when_it_works(self, load, base_url):
        assert load("retry.py").attempts_used(base_url, "/users") == 1

    def test_gets_there_on_a_flaky_endpoint(self, load, base_url, reset_flaky):
        """/flaky fails twice, then succeeds."""
        result = load("retry.py").fetch_with_retry(base_url, "/flaky", attempts=3)
        assert result is not None, (
            "Three attempts should be enough - /flaky fails twice then works."
        )
        assert result["message"] == "Worth the wait"

    def test_counts_the_attempts(self, load, base_url, reset_flaky):
        assert load("retry.py").attempts_used(base_url, "/flaky", attempts=3) == 3

    def test_gives_up_eventually(self, load, base_url):
        """/error is 500 every single time."""
        assert load("retry.py").fetch_with_retry(base_url, "/error", attempts=2) is None

    def test_does_not_retry_a_404(self, load, base_url):
        assert load("retry.py").attempts_used(base_url, "/users/99", attempts=3) == 1, (
            "A 404 was retried. It will still be a 404 next time."
        )

    def test_backs_off(self, source):
        code = source("retry.py", code_only=True)
        assert "sleep" in code, (
            "No time.sleep anywhere. Retrying instantly is what turns a "
            "struggling service into an outage."
        )


class TestApiClient:
    def test_users(self, load, base_url):
        client = load("client.py").ApiClient(base_url)
        assert len(client.users()) == 4

    def test_user(self, load, base_url):
        client = load("client.py").ApiClient(base_url)
        assert client.user(1)["name"] == "Ana Silva"
        assert client.user(99) is None

    def test_products(self, load, base_url):
        client = load("client.py").ApiClient(base_url)
        assert len(client.products()) == 4
        assert len(client.products("toys")) == 2

    def test_get_raises_on_4xx(self, load, base_url):
        mod = load("client.py")
        client = mod.ApiClient(base_url)
        with pytest.raises(mod.ApiError):
            client.get("/users/99")

    def test_get_or_none_does_not_raise(self, load, base_url):
        client = load("client.py").ApiClient(base_url)
        assert client.get_or_none("/users/99") is None
        assert len(client.get_or_none("/users")) == 4

    def test_raises_after_exhausting_retries(self, load, base_url):
        mod = load("client.py")
        client = mod.ApiClient(base_url, retries=2)
        with pytest.raises(mod.ApiError):
            client.get("/error")

    def test_sends_the_key(self, load, base_url):
        client = load("client.py").ApiClient(base_url, api_key="course-key-123")
        assert client.get("/secret")["message"] == "You found the secret"

    def test_without_a_key_the_secret_is_refused(self, load, base_url):
        mod = load("client.py")
        client = mod.ApiClient(base_url)
        with pytest.raises(mod.ApiError):
            client.get("/secret")

    def test_uses_a_session(self, load, source, base_url):
        load("client.py").ApiClient(base_url)
        code = source("client.py", code_only=True)
        assert "Session" in code, (
            "Use requests.Session - it reuses the connection between calls and "
            "holds your headers so you set them once."
        )

    def test_retries_flaky(self, load, base_url, reset_flaky):
        client = load("client.py").ApiClient(base_url, retries=3)
        assert client.get("/flaky")["message"] == "Worth the wait"
