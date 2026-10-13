"""Ten interview drills. Target times are in the README.

Talk out loud. Handle the empty case. Start with the obvious version.
"""


def two_sum(numbers, target):
    """Return the indices of the two numbers adding to target, or None.

    two_sum([2, 7, 11, 15], 9) -> (0, 1)
    Each number may be used once. Return the earliest pair.
    """


def most_common_word(text):
    """Return the most common word, lowercased. Ties go to the alphabetically first.

    most_common_word("the cat the dog") -> "the"
    Empty text -> None
    """


def group_by(records, key):
    """Group a list of dicts by one field.

    group_by([{"a": 1}, {"a": 2}, {"a": 1}], "a") -> {1: [...], 2: [...]}
    Records missing the key are skipped.
    """


def top_n_by(records, key, n):
    """Return the n records with the highest value for key, highest first."""


def running_total(numbers):
    """Return the cumulative totals.

    running_total([1, 2, 3]) -> [1, 3, 6]
    """


def chunk(items, size):
    """Split a list into pieces of at most `size`.

    chunk([1, 2, 3, 4, 5], 2) -> [[1, 2], [3, 4], [5]]
    A size of zero or less raises ValueError("Size must be positive").
    """


def first_duplicate(items):
    """Return the first item that appears twice, or None."""


def invert(mapping):
    """Swap keys and values. Values that repeat collect a list of keys.

    invert({"a": 1, "b": 2, "c": 1}) -> {1: ["a", "c"], 2: ["b"]}
    Keys come out in the order they were seen.
    """


def is_balanced(text):
    """Return True if (), [] and {} are balanced and correctly nested.

    is_balanced("a(b[c]d)e") -> True
    is_balanced("a(b]c)") -> False
    Anything that is not a bracket is ignored.
    """


def flatten(nested):
    """Flatten arbitrarily nested lists into one flat list.

    flatten([1, [2, [3, 4]], 5]) -> [1, 2, 3, 4, 5]
    """
