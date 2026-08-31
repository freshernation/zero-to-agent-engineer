"""Week 10, Day 1 - persistence.

Run me:  pytest week-10/day-1 -v
"""

import pytest


@pytest.fixture
def saved(load):
    mod = load("persistence.py")
    return mod, mod.build(mod.make_saver())


class TestWithoutPersistence:
    def test_still_runs(self, load):
        """A graph that cannot run without a checkpointer has made it compulsory."""
        mod = load("persistence.py")
        app = mod.build()
        result = app.invoke({"count": 0, "limit": 3, "log": []})
        assert result["count"] == 3
        assert len(result["log"]) == 3


class TestConfig:
    def test_config_shape(self, load):
        assert load("persistence.py").config_for("abc") == {
            "configurable": {"thread_id": "abc"}
        }


class TestRunning:
    def test_run_reaches_the_limit(self, saved):
        mod, app = saved
        result = mod.run(app, "t1", count=0, limit=3)
        assert result["count"] == 3
        assert len(result["log"]) == 3

    def test_state_survives_the_call(self, saved):
        mod, app = saved
        mod.run(app, "t1", count=0, limit=3)
        assert mod.state_of(app, "t1")["count"] == 3, (
            "The state was not saved. Compile with a checkpointer and pass a "
            "thread id."
        )

    def test_a_thread_that_never_ran(self, saved):
        mod, app = saved
        assert mod.state_of(app, "never-used") is None

    def test_checkpoints_accumulate(self, saved):
        mod, app = saved
        mod.run(app, "t1", count=0, limit=3)
        assert mod.checkpoint_count(app, "t1") > 1, (
            "A checkpoint is written after every node - three passes should "
            "leave several behind."
        )


class TestThreadsAreSeparate:
    def test_two_threads_do_not_mix(self, saved):
        mod, app = saved
        mod.run(app, "alice", count=0, limit=3)
        mod.run(app, "bob", count=0, limit=5)
        assert mod.state_of(app, "alice")["count"] == 3
        assert mod.state_of(app, "bob")["count"] == 5, (
            "One thread's run affected another. Two users, two ids, no "
            "interference - that is what a thread is for."
        )

    def test_an_untouched_thread_stays_empty(self, saved):
        mod, app = saved
        mod.run(app, "alice", count=0, limit=3)
        assert mod.state_of(app, "carol") is None


class TestContinuing:
    def test_running_the_same_thread_again_continues_it(self, saved):
        """The thing everyone gets wrong. It does not start over."""
        mod, app = saved
        mod.run(app, "t1", count=0, limit=3)
        mod.run(app, "t1", count=0, limit=3)
        log = mod.state_of(app, "t1")["log"]
        assert len(log) > 3, (
            f"The log has {len(log)} entries. Invoking the same thread id again "
            "continues that thread - the state you pass is merged into what is "
            "saved, not substituted for it."
        )


class TestEditingState:
    def test_set_state_changes_a_value(self, saved):
        mod, app = saved
        mod.run(app, "t1", count=0, limit=3)
        values = mod.set_state(app, "t1", {"count": 99})
        assert values["count"] == 99

    def test_set_state_honours_the_reducer(self, saved):
        """log accumulates, so an update adds rather than replaces."""
        mod, app = saved
        mod.run(app, "t1", count=0, limit=3)
        before = len(mod.state_of(app, "t1")["log"])
        values = mod.set_state(app, "t1", {"log": ["edited"]})
        assert len(values["log"]) == before + 1, (
            "update_state merges through the reducers, exactly as a node's "
            "return value does."
        )

    def test_set_state_writes_a_checkpoint(self, saved):
        mod, app = saved
        mod.run(app, "t1", count=0, limit=3)
        before = mod.checkpoint_count(app, "t1")
        mod.set_state(app, "t1", {"count": 99})
        assert mod.checkpoint_count(app, "t1") > before
