"""Week 2 milestone - the sales report.

Run me:  pytest week-02/milestone -v

Four of these tests swap the SALES block for a different set of sales. That is the
automated version of Friday's mutate phase: anything you typed in by hand instead of
calculating will fail immediately.
"""

REPORT = [
    "SALES REPORT",
    "========================================",
    "Ana           12 x $4.50 = $54.00",
    "Ben            8 x $7.25 = $58.00",
    "Cara          20 x $2.45 = $49.00",
    "Dev            5 x $12.00 = $60.00",
    "Eve           15 x $3.20 = $48.00",
    "Finn           9 x $6.50 = $58.50",
    "Gita          25 x $1.80 = $45.00",
    "Hugo           7 x $9.00 = $63.00",
    "Iris          11 x $5.50 = $60.50",
    "Jon           18 x $2.75 = $49.50",
    "========================================",
    "Total units:   130",
    "Total revenue: $545.50",
    "Average sale:  $54.55",
    "Best seller:   Hugo ($63.00)",
    "",
    "TOP 3 BY REVENUE",
    "1. Hugo         $63.00",
    "2. Iris         $60.50",
    "3. Dev          $60.00",
]

ORIGINAL = """SALES = [
    {"name": "Ana",  "units": 12, "unit_price": 4.50},
    {"name": "Ben",  "units": 8,  "unit_price": 7.25},
    {"name": "Cara", "units": 20, "unit_price": 2.45},
    {"name": "Dev",  "units": 5,  "unit_price": 12.00},
    {"name": "Eve",  "units": 15, "unit_price": 3.20},
    {"name": "Finn", "units": 9,  "unit_price": 6.50},
    {"name": "Gita", "units": 25, "unit_price": 1.80},
    {"name": "Hugo", "units": 7,  "unit_price": 9.00},
    {"name": "Iris", "units": 11, "unit_price": 5.50},
    {"name": "Jon",  "units": 18, "unit_price": 2.75},
]
"""

VARIANT = """SALES = [
    {"name": "Kim", "units": 10, "unit_price": 2.00},
    {"name": "Lee", "units": 4,  "unit_price": 15.00},
    {"name": "Max", "units": 6,  "unit_price": 5.00},
]
"""

SWAP = {ORIGINAL: VARIANT}


class TestRecordLines:
    def test_every_record_line(self, run):
        r = run("report.py")
        for line in REPORT[2:12]:
            r.expect(line)

    def test_revenue_is_calculated(self, run):
        """Revenue is not in the data - units times price has to happen."""
        run("report.py").expect("Gita          25 x $1.80 = $45.00")


class TestSummary:
    def test_total_units(self, run):
        run("report.py").expect("Total units:   130")

    def test_total_revenue(self, run):
        run("report.py").expect("Total revenue: $545.50")

    def test_average_is_per_record_not_per_unit(self, run):
        run("report.py").expect("Average sale:  $54.55")

    def test_best_seller_is_by_revenue_not_units(self, run):
        r = run("report.py")
        r.expect("Best seller:   Hugo ($63.00)")
        assert "Gita" not in r.stdout.split("TOP 3")[0].split("Best seller")[-1], (
            "Gita sold the most units, Hugo made the most money. "
            "Best seller is by revenue."
        )


class TestRanking:
    def test_top_three(self, run):
        r = run("report.py")
        r.expect("TOP 3 BY REVENUE")
        r.expect("1. Hugo         $63.00")
        r.expect("2. Iris         $60.50")
        r.expect("3. Dev          $60.00")

    def test_stops_at_three(self, run):
        r = run("report.py")
        r.expect("TOP 3 BY REVENUE")
        ranking = r.stdout.split("TOP 3 BY REVENUE")[-1]
        assert "4." not in ranking, "Top three only."


class TestShape:
    def test_whole_report_in_order(self, run):
        r = run("report.py")
        actual = [ln.rstrip() for ln in r.stdout.rstrip("\n").split("\n")]
        assert actual == REPORT, (
            "The report does not match line for line. Expected:\n"
            + "\n".join(f"  | {ln}" for ln in REPORT)
            + "\n\nYours:\n"
            + "\n".join(f"  | {ln}" for ln in actual)
        )


class TestDifferentData:
    """The same tests, against sales your program has never seen."""

    def test_record_lines(self, run_variant):
        r = run_variant("report.py", SWAP)
        r.expect("Kim           10 x $2.00 = $20.00")
        r.expect("Lee            4 x $15.00 = $60.00")
        r.expect("Max            6 x $5.00 = $30.00")

    def test_summary(self, run_variant):
        r = run_variant("report.py", SWAP)
        r.expect("Total units:   20")
        r.expect("Total revenue: $110.00")
        r.expect("Average sale:  $36.67")

    def test_best_seller(self, run_variant):
        run_variant("report.py", SWAP).expect("Best seller:   Lee ($60.00)")

    def test_ranking(self, run_variant):
        r = run_variant("report.py", SWAP)
        r.expect("1. Lee          $60.00")
        r.expect("2. Max          $30.00")
        r.expect("3. Kim          $20.00")
