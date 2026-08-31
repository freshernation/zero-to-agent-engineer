"""Week 12, Day 2 - the drills.

Run me:  pytest week-12/day-2 -v
Or one:  pytest week-12/day-2 -k two_sum -v

The edge cases are half the marks. They are half the marks in a real screen too.
"""

import pytest


class TestTwoSum:
    def test_finds_a_pair(self, load):
        assert load("drills.py").two_sum([2, 7, 11, 15], 9) == (0, 1)

    def test_a_later_pair(self, load):
        assert load("drills.py").two_sum([3, 2, 4], 6) == (1, 2)

    def test_no_pair(self, load):
        two_sum = load("drills.py").two_sum
        assert two_sum([2, 7, 11, 15], 9) == (0, 1)  # must work at all first
        assert two_sum([1, 2, 3], 99) is None

    def test_empty(self, load):
        two_sum = load("drills.py").two_sum
        assert two_sum([2, 7, 11, 15], 9) == (0, 1)  # must work at all first
        assert two_sum([], 5) is None

    def test_does_not_reuse_one_number(self, load):
        two_sum = load("drills.py").two_sum
        assert two_sum([3, 3], 6) == (0, 1)  # two 3s is fine
        assert two_sum([3, 5], 6) is None, (
            "3 + 3 = 6, but there is only one 3. Each number is used once."
        )

    def test_duplicates_are_fine(self, load):
        assert load("drills.py").two_sum([3, 3], 6) == (0, 1)

    def test_negatives(self, load):
        assert load("drills.py").two_sum([-2, 5, 3], 1) == (0, 2)


class TestMostCommonWord:
    def test_finds_it(self, load):
        assert load("drills.py").most_common_word("the cat the dog") == "the"

    def test_lowercases(self, load):
        assert load("drills.py").most_common_word("The the THE cat") == "the"

    def test_tie_goes_alphabetically_first(self, load):
        assert load("drills.py").most_common_word("zebra apple") == "apple", (
            "A tie is the case people forget. Say out loud what you will do "
            "about it before you write the code."
        )

    def test_empty(self, load):
        most_common_word = load("drills.py").most_common_word
        assert most_common_word("a a b") == "a"  # must work at all first
        assert most_common_word("") is None

    def test_one_word(self, load):
        assert load("drills.py").most_common_word("hello") == "hello"


class TestGroupBy:
    def test_groups(self, load):
        records = [{"a": 1, "n": "x"}, {"a": 2, "n": "y"}, {"a": 1, "n": "z"}]
        grouped = load("drills.py").group_by(records, "a")
        assert set(grouped) == {1, 2}
        assert [r["n"] for r in grouped[1]] == ["x", "z"]

    def test_keeps_order(self, load):
        records = [{"k": "b"}, {"k": "a"}, {"k": "b"}]
        assert len(load("drills.py").group_by(records, "k")["b"]) == 2

    def test_skips_records_missing_the_key(self, load):
        records = [{"a": 1}, {"b": 2}]
        assert set(load("drills.py").group_by(records, "a")) == {1}

    def test_empty(self, load):
        assert load("drills.py").group_by([], "a") == {}


class TestTopNBy:
    def test_sorts_descending(self, load):
        records = [{"v": 3}, {"v": 9}, {"v": 5}]
        assert [r["v"] for r in load("drills.py").top_n_by(records, "v", 2)] == [9, 5]

    def test_n_larger_than_the_list(self, load):
        assert len(load("drills.py").top_n_by([{"v": 1}], "v", 10)) == 1

    def test_n_of_zero(self, load):
        assert load("drills.py").top_n_by([{"v": 1}], "v", 0) == []

    def test_empty(self, load):
        assert load("drills.py").top_n_by([], "v", 3) == []


class TestRunningTotal:
    def test_accumulates(self, load):
        assert load("drills.py").running_total([1, 2, 3]) == [1, 3, 6]

    def test_negatives(self, load):
        assert load("drills.py").running_total([5, -2, 1]) == [5, 3, 4]

    def test_empty(self, load):
        assert load("drills.py").running_total([]) == []

    def test_one(self, load):
        assert load("drills.py").running_total([7]) == [7]


class TestChunk:
    def test_even_split(self, load):
        assert load("drills.py").chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_ragged_last_piece(self, load):
        assert load("drills.py").chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_size_bigger_than_the_list(self, load):
        assert load("drills.py").chunk([1, 2], 9) == [[1, 2]]

    def test_empty(self, load):
        assert load("drills.py").chunk([], 3) == []

    @pytest.mark.parametrize("size", [0, -1])
    def test_bad_size_raises(self, load, size):
        with pytest.raises(ValueError) as caught:
            load("drills.py").chunk([1, 2], size)
        assert "Size must be positive" in str(caught.value)


class TestFirstDuplicate:
    def test_finds_it(self, load):
        assert load("drills.py").first_duplicate([1, 2, 3, 2, 1]) == 2

    def test_none(self, load):
        first_duplicate = load("drills.py").first_duplicate
        assert first_duplicate([1, 1]) == 1  # must work at all first
        assert first_duplicate([1, 2, 3]) is None

    def test_empty(self, load):
        first_duplicate = load("drills.py").first_duplicate
        assert first_duplicate([1, 1]) == 1  # must work at all first
        assert first_duplicate([]) is None

    def test_strings(self, load):
        assert load("drills.py").first_duplicate(["a", "b", "a"]) == "a"

    def test_the_first_repeat_wins_not_the_earliest_item(self, load):
        assert load("drills.py").first_duplicate([3, 1, 2, 1, 3]) == 1, (
            "1 repeats before 3 does. It is the first SECOND appearance."
        )


class TestInvert:
    def test_simple(self, load):
        assert load("drills.py").invert({"a": 1, "b": 2}) == {1: ["a"], 2: ["b"]}

    def test_collects_repeats(self, load):
        assert load("drills.py").invert({"a": 1, "b": 2, "c": 1}) == {
            1: ["a", "c"], 2: ["b"],
        }

    def test_empty(self, load):
        assert load("drills.py").invert({}) == {}


class TestIsBalanced:
    @pytest.mark.parametrize("text", ["", "()", "a(b[c]d)e", "{[()]}", "no brackets"])
    def test_balanced(self, load, text):
        assert load("drills.py").is_balanced(text) is True

    @pytest.mark.parametrize("text", ["(", ")", "(]", "a(b]c)", "([)]", "())("])
    def test_not_balanced(self, load, text):
        assert load("drills.py").is_balanced(text) is False

    def test_wrong_order_is_not_balanced(self, load):
        assert load("drills.py").is_balanced(")(") is False, (
            "The counts match and the nesting does not. This is the case a "
            "counter misses and a stack catches."
        )


class TestFlatten:
    def test_one_level(self, load):
        assert load("drills.py").flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

    def test_deeply_nested(self, load):
        assert load("drills.py").flatten([1, [2, [3, [4]]], 5]) == [1, 2, 3, 4, 5]

    def test_empty(self, load):
        assert load("drills.py").flatten([]) == []

    def test_empty_lists_inside(self, load):
        assert load("drills.py").flatten([1, [], [2, []]]) == [1, 2]

    def test_already_flat(self, load):
        assert load("drills.py").flatten([1, 2, 3]) == [1, 2, 3]


class TestDrillLog:
    def test_is_being_kept(self, source):
        rows = [
            line for line in source("DRILL_LOG.md").splitlines()
            if line.strip().startswith("|") and line.count("|") >= 4
        ]
        filled = [
            row for row in rows
            if row.split("|")[1].strip()
            and "Drill" not in row and "---" not in row
        ]
        assert len(filled) >= 5, (
            f"{len(filled)} rows filled in. Log every attempt - by Friday it "
            "tells you exactly which two drills to practise again."
        )
