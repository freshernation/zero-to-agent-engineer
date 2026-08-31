"""Week 11, Day 2 - configuration, health, deployment.

Run me:  pytest week-11/day-2 -v
"""

import pytest


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


GOOD_ENV = {"ANTHROPIC_API_KEY": "sk-ant-abc123xyz"}


class TestSettings:
    def test_defaults(self, load):
        settings = load("config.py").load_settings(GOOD_ENV)
        assert settings.api_key == "sk-ant-abc123xyz"
        assert settings.model == "claude-sonnet-4-5"
        assert settings.environment == "development"
        assert settings.max_question_length == 500
        assert settings.request_timeout == 30

    def test_overrides(self, load):
        settings = load("config.py").load_settings({
            **GOOD_ENV,
            "MODEL": "claude-opus-4-5",
            "ENVIRONMENT": "production",
            "MAX_QUESTION_LENGTH": "200",
            "REQUEST_TIMEOUT": "10",
        })
        assert settings.model == "claude-opus-4-5"
        assert settings.environment == "production"
        assert settings.max_question_length == 200
        assert settings.request_timeout == 10

    @pytest.mark.parametrize("env", [{}, {"ANTHROPIC_API_KEY": ""}])
    def test_missing_key_names_the_variable(self, load, env):
        with pytest.raises(RuntimeError) as caught:
            load("config.py").load_settings(env)
        assert "ANTHROPIC_API_KEY" in str(caught.value), (
            f"The message was '{caught.value}'. Name the variable - a service "
            "that fails at startup should say exactly what to set."
        )

    def test_rejects_an_unknown_environment(self, load):
        with pytest.raises(Exception):
            load("config.py").load_settings({**GOOD_ENV, "ENVIRONMENT": "prod"})

    @pytest.mark.parametrize("value", ["0", "99999"])
    def test_rejects_a_silly_question_length(self, load, value):
        with pytest.raises(Exception):
            load("config.py").load_settings(
                {**GOOD_ENV, "MAX_QUESTION_LENGTH": value}
            )

    def test_reads_the_real_environment_by_default(self, load, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-from-the-environment")
        assert load("config.py").load_settings().api_key == "sk-from-the-environment"


class TestMasking:
    def test_masks_the_middle(self, load):
        assert load("config.py").mask("sk-ant-abc123xyz") == "sk-a...3xyz"

    @pytest.mark.parametrize("secret", ["", "short", "1234567"])
    def test_short_secrets_show_nothing(self, load, secret):
        assert load("config.py").mask(secret) == "****", (
            "A short secret cannot be partly shown without giving most of it "
            "away."
        )

    def test_redacted_hides_the_key(self, load):
        mod = load("config.py")
        settings = mod.load_settings(GOOD_ENV)
        shown = mod.redacted(settings)
        assert "sk-ant-abc123xyz" not in str(shown), (
            "The key is still in the output. This dict gets logged at startup "
            "and ends up in a log service your whole company can read."
        )
        assert shown["model"] == "claude-sonnet-4-5", (
            "Everything except the key should still be there - that is what "
            "makes logging it useful."
        )

    def test_is_production(self, load):
        mod = load("config.py")
        assert mod.is_production(mod.load_settings(GOOD_ENV)) is False
        assert mod.is_production(
            mod.load_settings({**GOOD_ENV, "ENVIRONMENT": "production"})
        ) is True


class TestHealth:
    def test_uptime(self, load):
        assert load("health.py").uptime_seconds(1000.0, 1042.7) == 42

    def test_uptime_at_the_start(self, load):
        assert load("health.py").uptime_seconds(1000.0, 1000.0) == 0

    def test_health_payload(self, load):
        payload = load("health.py").health_payload(1000.0, 1060.0, "1.2.3")
        assert payload["status"] == "ok"
        assert payload["version"] == "1.2.3"
        assert payload["uptime_seconds"] == 60


class TestReadiness:
    def test_all_passing(self, load):
        result = load("health.py").readiness({
            "corpus": lambda: True, "key": lambda: True,
        })
        assert result["ready"] is True
        assert result["failing"] == []

    def test_one_failing(self, load):
        result = load("health.py").readiness({
            "corpus": lambda: True, "key": lambda: False,
        })
        assert result["ready"] is False
        assert result["failing"] == ["key"]
        assert result["checks"]["corpus"] is True

    def test_a_check_that_raises_counts_as_failing(self, load):
        def explodes():
            raise RuntimeError("no")

        result = load("health.py").readiness({"corpus": lambda: True, "db": explodes})
        assert result["ready"] is False
        assert "db" in result["failing"], (
            "A readiness probe that throws tells the platform nothing. Catch it "
            "and report the check as failing."
        )

    def test_no_checks_is_ready(self, load):
        assert load("health.py").readiness({})["ready"] is True


class TestDockerfile:
    @pytest.fixture
    def dockerfile(self, source):
        return _instructions_removed(source("Dockerfile"), "Dockerfile")

    def test_starts_from_python(self, dockerfile):
        assert "FROM python" in dockerfile

    def test_installs_requirements_before_copying_the_code(self, dockerfile):
        lines = [ln.strip() for ln in dockerfile.splitlines() if ln.strip()]
        install = next(
            (i for i, ln in enumerate(lines) if "pip install" in ln), None
        )
        copy_all = next(
            (i for i, ln in enumerate(lines) if ln.startswith("COPY . ")), None
        )
        assert install is not None, "Nothing installs the requirements."
        assert copy_all is not None, "Nothing copies the code in."
        assert install < copy_all, (
            "The code is copied before the install, so every code change "
            "reinstalls every dependency. Copy requirements.txt first - it "
            "turns a two-minute build into a five-second one."
        )

    def test_binds_all_interfaces(self, dockerfile):
        assert "0.0.0.0" in dockerfile, (
            "Bind 0.0.0.0, not 127.0.0.1. In a container the request comes from "
            "outside it - this is the most common reason a deploy 'works "
            "locally' and returns nothing in production."
        )

    def test_takes_the_port_from_the_environment(self, dockerfile):
        assert "PORT" in dockerfile


class TestEnvExample:
    @pytest.fixture
    def example(self, source):
        return _instructions_removed(source(".env.example"), ".env.example")

    def test_names_every_variable(self, example):
        for name in ("ANTHROPIC_API_KEY", "MODEL", "ENVIRONMENT"):
            assert name in example, f"{name} is not mentioned."

    def test_has_no_real_key(self, example):
        for line in example.splitlines():
            if line.strip().startswith("ANTHROPIC_API_KEY"):
                value = line.split("=", 1)[1].strip() if "=" in line else ""
                assert not value.startswith("sk-"), (
                    "There is a real-looking key in .env.example. This file is "
                    "committed - it carries the names, never the values."
                )
