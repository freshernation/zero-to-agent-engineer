"""Week 11, Day 4 - gating the deploy.

Run me:  pytest week-11/day-4 -v
"""

import pytest
from fake_model import FakeClient, text_reply

GOOD_JUDGEMENT = '{"score": 4, "reason": "Correct but omits the receipt rule."}'


class TestJudge:
    def test_rubric_mentions_the_scale(self, load):
        system = load("judge.py").JUDGE_SYSTEM
        assert "5" in system and "1" in system
        assert "json" in system.lower()

    def test_parses_a_judgement(self, load):
        client = FakeClient([text_reply(GOOD_JUDGEMENT)])
        result = load("judge.py").judge(client, "q", "a", "reference")
        assert result["score"] == 4
        assert "receipt" in result["reason"]

    def test_handles_a_wrapped_judgement(self, load):
        client = FakeClient([text_reply(f"Sure!\n```json\n{GOOD_JUDGEMENT}\n```")])
        assert load("judge.py").judge(client, "q", "a", "r")["score"] == 4

    def test_unparseable_scores_zero(self, load):
        client = FakeClient([text_reply("I think it was pretty good honestly")])
        result = load("judge.py").judge(client, "q", "a", "r")
        assert result["score"] == 0, (
            "A judge that crashes on its own bad output is not a judge. Score "
            "it zero and say why."
        )
        assert result["reason"]

    @pytest.mark.parametrize("bad", ['{"score": 9, "reason": "x"}',
                                     '{"score": 0, "reason": "x"}',
                                     '{"score": "four", "reason": "x"}'])
    def test_out_of_range_scores_zero(self, load, bad):
        client = FakeClient([text_reply(bad)])
        assert load("judge.py").judge(client, "q", "a", "r")["score"] == 0

    def test_uses_temperature_zero(self, load):
        client = FakeClient([text_reply(GOOD_JUDGEMENT)])
        load("judge.py").judge(client, "q", "a", "r")
        assert client.last_call.get("temperature") == 0

    def test_mean_score(self, load):
        judgements = [{"score": 4}, {"score": 5}, {"score": 3}]
        assert load("judge.py").mean_score(judgements) == 4.0

    def test_mean_score_rounds(self, load):
        assert load("judge.py").mean_score([{"score": 4}, {"score": 3}]) == 3.5

    def test_mean_score_of_nothing(self, load):
        assert load("judge.py").mean_score([]) == 0.0


class TestGate:
    def test_thresholds(self, load):
        thresholds = load("gate.py").THRESHOLDS
        assert thresholds["hit_rate"] == 0.80
        assert thresholds["mean_score"] == 3.5
        assert thresholds["refusal_rate"] == 0.20

    def test_a_passing_report(self, load):
        mod = load("gate.py")
        result = mod.check(
            {"hit_rate": 0.85, "mean_score": 4.0, "refusal_rate": 0.10},
            mod.THRESHOLDS,
        )
        assert result["passed"] is True
        assert result["failures"] == []

    def test_exactly_on_the_threshold_passes(self, load):
        mod = load("gate.py")
        result = mod.check(
            {"hit_rate": 0.80, "mean_score": 3.5, "refusal_rate": 0.20},
            mod.THRESHOLDS,
        )
        assert result["passed"] is True

    def test_a_low_hit_rate_fails(self, load):
        mod = load("gate.py")
        result = mod.check(
            {"hit_rate": 0.60, "mean_score": 4.0, "refusal_rate": 0.10},
            mod.THRESHOLDS,
        )
        assert result["passed"] is False
        assert "hit_rate" in result["failures"]

    def test_a_high_refusal_rate_fails(self, load):
        """The direction that trips people up."""
        mod = load("gate.py")
        result = mod.check(
            {"hit_rate": 0.90, "mean_score": 4.0, "refusal_rate": 0.50},
            mod.THRESHOLDS,
        )
        assert result["passed"] is False
        assert "refusal_rate" in result["failures"], (
            "refusal_rate must be at or BELOW its threshold - a system that "
            "always refuses is useless, and a gate that only measures success "
            "misses half of what can go wrong."
        )

    def test_a_low_refusal_rate_is_fine(self, load):
        mod = load("gate.py")
        assert mod.check(
            {"hit_rate": 0.9, "mean_score": 4.0, "refusal_rate": 0.0},
            mod.THRESHOLDS,
        )["passed"] is True

    def test_several_failures(self, load):
        mod = load("gate.py")
        result = mod.check(
            {"hit_rate": 0.1, "mean_score": 1.0, "refusal_rate": 0.9},
            mod.THRESHOLDS,
        )
        assert set(result["failures"]) == {"hit_rate", "mean_score", "refusal_rate"}

    def test_summarise(self, load):
        mod = load("gate.py")
        lines = mod.summarise(
            {"hit_rate": 0.85, "mean_score": 4.0, "refusal_rate": 0.10},
            mod.THRESHOLDS,
        ).splitlines()
        assert len(lines) == 3
        assert any("hit_rate" in line and "PASS" in line for line in lines)

    def test_summarise_marks_failures(self, load):
        mod = load("gate.py")
        summary = mod.summarise(
            {"hit_rate": 0.10, "mean_score": 4.0, "refusal_rate": 0.10},
            mod.THRESHOLDS,
        )
        assert "FAIL" in summary

    def test_exit_code(self, load):
        mod = load("gate.py")
        assert mod.exit_code({"passed": True, "failures": []}) == 0
        assert mod.exit_code({"passed": False, "failures": ["hit_rate"]}) == 1


class TestGuards:
    def test_a_short_question_is_fine(self, load):
        assert load("guards.py").check_question("hello", 500) == (True, "")

    def test_a_long_question_is_refused(self, load):
        ok, message = load("guards.py").check_question("x" * 612, 500)
        assert ok is False
        assert "612" in message and "500" in message, (
            f"The message was {message!r}. Put both numbers in - the person "
            "reading it needs to know how far over they are."
        )

    def test_an_empty_question_is_refused(self, load):
        ok, _ = load("guards.py").check_question("", 500)
        assert ok is False


class TestBudget:
    def test_starts_empty(self, load):
        budget = load("guards.py").Budget(1.00)
        assert budget.spent == 0
        assert budget.remaining == 1.00

    def test_spending(self, load):
        budget = load("guards.py").Budget(1.00)
        budget.spend(0.30)
        assert budget.spent == 0.30
        assert budget.remaining == 0.70

    def test_would_exceed(self, load):
        budget = load("guards.py").Budget(1.00)
        budget.spend(0.90)
        assert budget.would_exceed(0.05) is False
        assert budget.would_exceed(0.20) is True

    def test_going_over_raises(self, load):
        mod = load("guards.py")
        budget = mod.Budget(1.00)
        budget.spend(0.90)
        with pytest.raises(mod.BudgetExceeded):
            budget.spend(0.20)

    def test_a_refused_spend_is_not_recorded(self, load):
        """A budget that goes further over every time it is asked is not a budget."""
        mod = load("guards.py")
        budget = mod.Budget(1.00)
        budget.spend(0.90)
        with pytest.raises(mod.BudgetExceeded):
            budget.spend(0.20)
        assert budget.spent == 0.90, (
            f"spent is {budget.spent}. The refused spend was recorded anyway."
        )

    def test_spending_exactly_the_limit_is_allowed(self, load):
        budget = load("guards.py").Budget(1.00)
        budget.spend(1.00)
        assert budget.remaining == 0

    def test_reset(self, load):
        budget = load("guards.py").Budget(1.00)
        budget.spend(0.50)
        budget.reset()
        assert budget.spent == 0
