"""Keep the test files YOU write out of the main test run.

test_shapes.py and test_stats.py are today's exercise, not part of the course's
own suite. They are graded by test_day3.py, which runs them in isolation against
correct and deliberately broken code.

To run your own suites directly and see their output:

    python3 week-04/day-3/check_my_tests.py
"""

collect_ignore = ["test_shapes.py", "test_stats.py"]
