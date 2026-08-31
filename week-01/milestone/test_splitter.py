"""Week 1 milestone - the bill splitter.

Run me:  pytest week-01/milestone -v

Nine tests. Green means it behaves correctly. It does not mean the code is good,
and Friday's defence is about the code.
"""

import pytest


def split(run, bill, people, service):
    return run("splitter.py", answers=[bill, people, service])


class TestTipRates:
    def test_good_service_is_20_percent(self, run):
        r = split(run, 60, 4, "good")
        r.expect("Tip (20%): $12.00")

    def test_ok_service_is_15_percent(self, run):
        r = split(run, 80, 5, "ok")
        r.expect("Tip (15%): $12.00")

    def test_poor_service_is_10_percent(self, run):
        r = split(run, 45, 2, "poor")
        r.expect("Tip (10%): $4.50")

    def test_unknown_service_is_treated_as_ok(self, run):
        r = split(run, 100, 4, "amazing")
        r.expect("Tip (15%): $15.00")


class TestFullOutput:
    def test_worked_example_from_the_spec(self, run):
        r = split(run, 60, 4, "good")
        r.expect("Tip (20%): $12.00")
        r.expect("Total: $72.00")
        r.expect("Each person pays: $18.00")

    def test_uneven_split(self, run):
        r = split(run, 80, 5, "ok")
        r.expect("Tip (15%): $12.00")
        r.expect("Total: $92.00")
        r.expect("Each person pays: $18.40")

    def test_poor_service_end_to_end(self, run):
        r = split(run, 45, 2, "poor")
        r.expect("Tip (10%): $4.50")
        r.expect("Total: $49.50")
        r.expect("Each person pays: $24.75")

    def test_one_person_pays_the_whole_thing(self, run):
        r = split(run, 20, 1, "good")
        r.expect("Tip (20%): $4.00")
        r.expect("Total: $24.00")
        r.expect("Each person pays: $24.00")


class TestQuality:
    def test_money_always_has_two_decimal_places(self, run):
        r = split(run, 33.33, 3, "good")
        # 33.33 * 0.20 = 6.666 -> 6.67 ; total 39.996 -> 40.00 ; each 13.332 -> 13.33
        r.expect("Tip (20%): $6.67")
        r.expect("Total: $40.00")
        r.expect("Each person pays: $13.33")
