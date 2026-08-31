"""Week 10, Day 4 - judgement, and the bugs these features bring.

Run me:  pytest week-10/day-4 -v
"""

import pytest

PLACEHOLDER = "(your answer)"

NONE_SET = {
    "different_tools": False,
    "different_permissions": False,
    "different_models": False,
    "parallel_subtasks": False,
}


class TestReasons:
    def test_four_of_them(self, load):
        assert len(load("decide.py").REASONS) == 4

    def test_they_are_the_real_ones(self, load):
        joined = " ".join(load("decide.py").REASONS).lower()
        for word in ("tool", "permission", "model", "parallel"):
            assert word in joined


class TestAssess:
    def test_no_reason_means_one_agent(self, load):
        result = load("decide.py").assess(NONE_SET)
        assert result["recommend"] == "single", (
            "With no reason at all, one agent is the answer. It is cheaper, "
            "easier to debug, and there is nowhere for context to get lost."
        )
        assert result["reasons"] == []

    @pytest.mark.parametrize("flag", list(NONE_SET))
    def test_any_one_reason_is_enough(self, load, flag):
        result = load("decide.py").assess({**NONE_SET, flag: True})
        assert result["recommend"] == "multi"
        assert result["reasons"] == [flag]

    def test_several_reasons_are_all_listed(self, load):
        result = load("decide.py").assess({
            **NONE_SET, "different_tools": True, "different_permissions": True,
        })
        assert result["recommend"] == "multi"
        assert set(result["reasons"]) == {"different_tools", "different_permissions"}

    def test_unknown_flags_are_ignored(self, load):
        """'It mirrors how a team works' is not a reason."""
        result = load("decide.py").assess({**NONE_SET, "looks_modular": True})
        assert result["recommend"] == "single"
        assert result["reasons"] == []


class TestEstimates:
    def test_estimate_calls(self, load):
        assert load("decide.py").estimate_calls(1, 1) == 2
        assert load("decide.py").estimate_calls(3, 5) == 8

    def test_compare_designs(self, load):
        designs = {
            "one-agent": {"agent_count": 1, "tools_used": 1},
            "three-agents": {"agent_count": 3, "tools_used": 5},
        }
        assert load("decide.py").compare_designs(designs) == {
            "one-agent": 2, "three-agents": 8,
        }

    def test_cheapest(self, load):
        designs = {
            "one-agent": {"agent_count": 1, "tools_used": 1},
            "three-agents": {"agent_count": 3, "tools_used": 5},
        }
        assert load("decide.py").cheapest(designs) == "one-agent", (
            "Four times the calls for the same answer is the cost you can "
            "estimate before writing anything."
        )


class TestFixes:
    def test_broken_1_needs_a_checkpointer(self, run, source):
        run("broken_1.py").expect("Log: ['prepared', 'spent']")
        code = source("broken_1.py", code_only=True)
        assert "checkpointer" in code, (
            "A pause without persistence is not a pause - it is a run that "
            "stopped and cannot be resumed."
        )

    def test_broken_2_separate_threads(self, run, source):
        run("broken_2.py").expect("Alice: 3 steps  Bob: 2 steps")
        code = source("broken_2.py", code_only=True)
        assert code.count("thread_id") >= 1
        assert '"shared"' not in code.replace("'", '"'), (
            "Both users are still on one thread. Two users, two ids."
        )

    def test_broken_3_no_duplicate(self, run):
        r = run("broken_3.py")
        r.expect("Log: ['added', 'doubled']")
        assert "'added', 'added'" not in r.stdout, (
            "'added' is still in there twice. The child received the parent's "
            "log and returned it, and the reducer added it on again."
        )


class TestNotes:
    @pytest.mark.parametrize("n", [1, 2, 3])
    def test_entry_is_filled_in(self, source, n):
        text = source("NOTES.md")
        parts = text.split(f"## broken_{n}.py")
        assert len(parts) > 1, f"NOTES.md is missing the broken_{n}.py section."
        body = parts[1].split("\n## ")[0]
        assert PLACEHOLDER not in body, (
            f"The broken_{n}.py entry still has '{PLACEHOLDER}' placeholders."
        )
        assert len(body.split()) >= 40, (
            f"The broken_{n}.py entry is too short. Answer all four prompts."
        )
