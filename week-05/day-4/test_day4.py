"""Week 5, Day 4 - combining endpoints.

Run me:  pytest week-05/day-4 -v
"""

import pytest

PLACEHOLDER = "(your answer)"


class TestMerge:
    def test_get_orders(self, load, base_url):
        orders = load("merge.py").get_orders(base_url, 1)
        assert len(orders) == 2
        assert {o["id"] for o in orders} == {100, 101}

    def test_get_orders_for_someone_with_none(self, load, base_url):
        assert load("merge.py").get_orders(base_url, 3) == []

    def test_enrich_orders(self, load, base_url):
        rows = load("merge.py").enrich_orders(base_url, 1)
        assert len(rows) == 2
        first = rows[0]
        assert first["product"] == "Widget"
        assert first["quantity"] == 2
        assert first["price"] == 4.5
        assert first["line_total"] == 9.0

    def test_enrich_orders_bigger_line(self, load, base_url):
        rows = load("merge.py").enrich_orders(base_url, 2)
        assert rows[0]["product"] == "Thingummy"
        assert rows[0]["line_total"] == 267.0

    def test_enrich_fetches_products_once(self, load, base_url, monkeypatch):
        """Four orders must not mean four product lookups."""
        import requests

        calls = {"products": 0}
        real_get = requests.get

        def counting_get(url, *args, **kwargs):
            if "/products" in str(url):
                calls["products"] += 1
            return real_get(url, *args, **kwargs)

        monkeypatch.setattr(requests, "get", counting_get)
        load("merge.py").enrich_orders(base_url, 1)
        assert calls["products"] <= 1, (
            f"The product list was fetched {calls['products']} times for two "
            "orders. Fetch it once, build a lookup dict, then loop over local "
            "data - this is the N+1 problem and it has a name for a reason."
        )

    def test_user_summary(self, load, base_url):
        summary = load("merge.py").user_summary(base_url, 1)
        assert summary["name"] == "Ana Silva"
        assert summary["city"] == "Lisbon"
        assert summary["order_count"] == 2
        assert summary["total_spent"] == 12.25

    def test_user_summary_with_no_orders(self, load, base_url):
        summary = load("merge.py").user_summary(base_url, 3)
        assert summary["name"] == "Cara Diaz"
        assert summary["order_count"] == 0
        assert summary["total_spent"] == 0

    def test_ranked_customers(self, load, base_url):
        ranked = load("merge.py").ranked_customers(base_url)
        assert len(ranked) == 4
        assert [r["name"] for r in ranked] == [
            "Ben Okafor", "Ana Silva", "Dev Patel", "Cara Diaz",
        ]
        assert ranked[0]["total_spent"] == 267.0


class TestFixes:
    def test_broken_1_checks_the_status(self, run, source):
        run("broken_1.py").expect("Missing user: none found")
        code = source("broken_1.py", code_only=True)
        assert "status_code" in code, (
            "Check response.status_code before you trust the body. A 404 still "
            "has a body - it just contains an error message, not your data."
        )

    def test_broken_2_stops_after_one(self, run, source):
        run("broken_2.py").expect("Attempts: 1")
        code = source("broken_2.py", code_only=True)
        assert "range(3)" in code.replace(" ", ""), (
            "Keep the retry loop - the fix is to stop retrying something that "
            "cannot succeed, not to delete the retries."
        )

    def test_broken_3_narrows_the_except(self, run, source):
        run("broken_3.py").expect("City: Lisbon")
        code = source("broken_3.py", code_only=True)
        for bad in ("except Exception", "except:"):
            assert bad not in code, (
                f"`{bad}` is still there. It caught the KeyError from a "
                "misspelt field and turned a bug into a plausible-looking "
                "answer. Catch what you actually expect."
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
