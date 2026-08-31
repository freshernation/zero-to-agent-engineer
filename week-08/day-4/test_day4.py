"""Week 8, Day 4 - inspecting and debugging graphs.

Run me:  pytest week-08/day-4 -v
"""

import operator
from typing import Annotated, TypedDict

import pytest
from langgraph.graph import END, START, StateGraph

PLACEHOLDER = "(your answer)"


class DemoState(TypedDict):
    count: int
    limit: int
    log: Annotated[list, operator.add]


def _bump(state):
    return {"count": state["count"] + 1, "log": ["bumped"]}


def _route(state):
    return "bump" if state["count"] < state["limit"] else END


@pytest.fixture
def loop_app():
    graph = StateGraph(DemoState)
    graph.add_node("bump", _bump)
    graph.add_edge(START, "bump")
    graph.add_conditional_edges("bump", _route, ["bump", END])
    return graph.compile()


@pytest.fixture
def start():
    return {"count": 0, "limit": 3, "log": []}


class TestInspect:
    def test_node_updates(self, load, loop_app, start):
        updates = load("inspect_graph.py").node_updates(loop_app, start)
        assert len(updates) == 3
        name, update = updates[0]
        assert name == "bump", (
            "Each streamed item is {node_name: update}. The key is the name of "
            "the node that just finished."
        )
        assert update["count"] == 1

    def test_node_sequence(self, load, loop_app, start):
        assert load("inspect_graph.py").node_sequence(loop_app, start) == [
            "bump", "bump", "bump",
        ]

    def test_count_visits(self, load, loop_app, start):
        mod = load("inspect_graph.py")
        assert mod.count_visits(loop_app, start, "bump") == 3
        assert mod.count_visits(loop_app, start, "nothing") == 0

    def test_final_state(self, load, loop_app, start):
        final = load("inspect_graph.py").final_state(loop_app, start)
        assert final["count"] == 3

    def test_a_two_node_graph(self, load):
        graph = StateGraph(DemoState)
        graph.add_node("bump", _bump)
        graph.add_node("bump_again", _bump)
        graph.add_edge(START, "bump")
        graph.add_edge("bump", "bump_again")
        graph.add_edge("bump_again", END)
        app = graph.compile()
        assert load("inspect_graph.py").node_sequence(
            app, {"count": 0, "limit": 9, "log": []}
        ) == ["bump", "bump_again"]


class TestFixes:
    def test_broken_1_needs_a_reducer(self, run, source):
        run("broken_1.py").expect("Log: ['a', 'b']")
        code = source("broken_1.py", code_only=True)
        assert "Annotated" in code, (
            "A key with no reducer is last-write-wins, so the second node's "
            "update replaced the first. Declare how the two should merge."
        )

    def test_broken_2_off_by_one(self, run):
        r = run("broken_2.py")
        r.expect("Visits: 3")
        assert "Visits: 4" not in r.stdout

    def test_broken_3_missing_edge(self, run, source):
        run("broken_3.py").expect("Answer: It is 391.")
        code = source("broken_3.py", code_only=True).replace(" ", "")
        assert '"tools","model"' in code.replace("'", '"'), (
            "The tools node still goes straight to END, so the result never "
            "reaches the model. That one edge is the whole cycle - it is your "
            "week-7 'go round again'."
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
