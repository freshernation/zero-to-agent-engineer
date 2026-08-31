"""Week 10, Day 2 - pausing for a human, and subgraphs.

Run me:  pytest week-10/day-2 -v
"""

import pytest
from langgraph.checkpoint.memory import MemorySaver


@pytest.fixture
def approval(load):
    mod = load("approval.py")
    return mod, mod.build(MemorySaver())


class TestPausing:
    def test_stops_before_spending(self, approval):
        mod, app = approval
        state = mod.start(app, "t1", 500)
        assert "prepared 500" in state["log"]
        assert not any("spent" in entry for entry in state["log"]), (
            "It spent the money without stopping. interrupt_before means the "
            "graph returns before that node runs."
        )

    def test_reports_what_it_is_waiting_on(self, approval):
        mod, app = approval
        mod.start(app, "t1", 500)
        assert mod.pending(app, "t1") == "spend"

    def test_not_finished_while_paused(self, approval):
        mod, app = approval
        mod.start(app, "t1", 500)
        assert mod.is_finished(app, "t1") is False


class TestApproving:
    def test_resuming_spends(self, approval):
        mod, app = approval
        mod.start(app, "t1", 500)
        state = mod.approve(app, "t1")
        assert "spent 500" in state["log"]

    def test_finished_afterwards(self, approval):
        mod, app = approval
        mod.start(app, "t1", 500)
        mod.approve(app, "t1")
        assert mod.is_finished(app, "t1") is True
        assert mod.pending(app, "t1") is None


class TestRejecting:
    def test_rejecting_does_not_spend(self, approval):
        mod, app = approval
        mod.start(app, "t1", 500)
        state = mod.reject(app, "t1")
        assert "rejected" in state["log"]
        assert not any("spent" in entry for entry in state["log"]), (
            "Resuming always runs the node - refusing means changing the state "
            "first so the node can see it. What 'no' means is yours to define."
        )

    def test_finished_after_rejecting(self, approval):
        mod, app = approval
        mod.start(app, "t1", 500)
        mod.reject(app, "t1")
        assert mod.is_finished(app, "t1") is True


class TestThreadsStaySeparate:
    def test_two_pending_approvals(self, approval):
        mod, app = approval
        mod.start(app, "alice", 500)
        mod.start(app, "bob", 900)
        mod.approve(app, "alice")
        assert mod.is_finished(app, "alice") is True
        assert mod.pending(app, "bob") == "spend", (
            "Approving one thread completed another. That is what thread ids "
            "are for."
        )
        state = mod.reject(app, "bob")
        assert "rejected" in state["log"]
        assert "prepared 900" in state["log"]


class TestSubgraphs:
    def test_child_works_alone(self, load):
        """The reason to make it a subgraph at all - it can be tested by itself."""
        child = load("nested.py").build_child()
        assert child.invoke({"value": 4, "log": []})["value"] == 8

    def test_parent_runs_the_child(self, load):
        assert load("nested.py").run_parent(3)["value"] == 8, (
            "3 + 1 = 4, doubled = 8. If you got 7 the child never ran; if you "
            "got 6 the order is wrong."
        )

    @pytest.mark.parametrize("value,expected", [(0, 2), (1, 4), (10, 22)])
    def test_several_values(self, load, value, expected):
        assert load("nested.py").run_parent(value)["value"] == expected

    def test_the_child_is_a_node(self, load, source):
        load("nested.py").build_parent()
        code = source("nested.py", code_only=True)
        assert "add_node" in code and "build_child" in code, (
            "Use the compiled child graph as a node in the parent - that is the "
            "whole feature."
        )
