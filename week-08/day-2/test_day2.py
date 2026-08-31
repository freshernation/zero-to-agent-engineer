"""Week 8, Day 2 - graphs.

Run me:  pytest week-08/day-2 -v

No model today. Plain numbers, so the graph is the only thing you are thinking
about.
"""

import pytest
from langgraph.graph import END


class TestNodes:
    def test_increment(self, load):
        update = load("state.py").increment({"count": 3, "limit": 5, "log": []})
        assert update["count"] == 4
        assert update["log"] == ["incremented"], (
            "A node returns a PARTIAL update. Return just the new log entry - "
            "the reducer adds it to what is already there."
        )

    def test_double(self, load):
        update = load("state.py").double({"count": 3, "limit": 5, "log": []})
        assert update["count"] == 6
        assert update["log"] == ["doubled"]

    def test_nodes_do_not_mutate_the_state(self, load):
        mod = load("state.py")
        state = {"count": 3, "limit": 5, "log": ["old"]}
        mod.increment(state)
        assert state == {"count": 3, "limit": 5, "log": ["old"]}, (
            "The node changed the state it was given. Return an update and let "
            "the graph merge it - the same rule as week 3's add_expense."
        )

    @pytest.mark.parametrize("count,even", [(0, True), (2, True), (3, False)])
    def test_is_even(self, load, count, even):
        assert load("state.py").is_even({"count": count, "limit": 5, "log": []}) is even


class TestRouting:
    def test_route_by_parity_even(self, load):
        assert load("state.py").route_by_parity(
            {"count": 4, "limit": 5, "log": []}
        ) == "double"

    def test_route_by_parity_odd(self, load):
        assert load("state.py").route_by_parity(
            {"count": 3, "limit": 5, "log": []}
        ) == END

    def test_route_until_limit_keeps_going(self, load):
        assert load("state.py").route_until_limit(
            {"count": 1, "limit": 3, "log": []}
        ) == "increment", (
            "A routing function returns the NAME of the next node. Returning the "
            "node you just came from is how a graph loops."
        )

    def test_route_until_limit_stops(self, load):
        assert load("state.py").route_until_limit(
            {"count": 3, "limit": 3, "log": []}
        ) == END


class TestLinearGraph:
    def test_runs_both_nodes(self, load):
        mod = load("graphs.py")
        result = mod.build_linear().invoke(mod.initial(count=3, limit=5))
        assert result["count"] == 8, "increment then double: (3+1)*2"

    def test_the_log_accumulates(self, load):
        mod = load("graphs.py")
        result = mod.build_linear().invoke(mod.initial(count=0, limit=5))
        assert result["log"] == ["incremented", "doubled"], (
            f"Got {result['log']}. Without a reducer each node's log update "
            "overwrites the last. Annotated[list, operator.add] merges them."
        )


class TestBranchingGraph:
    def test_takes_the_double_branch(self, load):
        mod = load("graphs.py")
        result = mod.build_branching().invoke(mod.initial(count=1, limit=9))
        assert result["count"] == 4, "1 -> 2 (even) -> doubled -> 4"
        assert result["log"] == ["incremented", "doubled"]

    def test_skips_the_double_branch(self, load):
        mod = load("graphs.py")
        result = mod.build_branching().invoke(mod.initial(count=2, limit=9))
        assert result["count"] == 3, "2 -> 3 (odd) -> straight to END"
        assert result["log"] == ["incremented"]


class TestLoopGraph:
    def test_loops_until_the_limit(self, load):
        mod = load("graphs.py")
        result = mod.build_loop().invoke(mod.initial(count=0, limit=3))
        assert result["count"] == 3
        assert result["log"] == ["incremented"] * 3, (
            f"Got {result['log']}. Three passes, three entries."
        )

    def test_does_not_run_at_all_past_the_limit(self, load):
        mod = load("graphs.py")
        result = mod.build_loop().invoke(mod.initial(count=5, limit=3))
        assert result["count"] == 6, (
            "The first increment always happens - START goes straight to it. "
            "The condition is checked afterwards."
        )
        assert len(result["log"]) == 1

    def test_a_longer_loop(self, load):
        mod = load("graphs.py")
        result = mod.build_loop().invoke(mod.initial(count=0, limit=7))
        assert result["count"] == 7
        assert len(result["log"]) == 7


class TestCompiled:
    @pytest.mark.parametrize("builder", ["build_linear", "build_branching", "build_loop"])
    def test_returns_something_invokable(self, load, builder):
        graph = getattr(load("graphs.py"), builder)()
        assert hasattr(graph, "invoke"), (
            f"{builder}() should return a COMPILED graph - call .compile() on it "
            "before handing it back."
        )
