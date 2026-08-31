"""Week 5, Day 2 - pydantic.

Run me:  pytest week-05/day-2 -v
"""

import pytest
from pydantic import ValidationError

GOOD_USER = {"id": 1, "name": "Ana Silva", "email": "ana@example.com", "city": "Lisbon"}
GOOD_PRODUCT = {
    "id": 10, "name": "Widget", "price": 4.50, "category": "tools", "in_stock": True,
}


class TestUser:
    def test_accepts_a_good_record(self, load):
        user = load("models.py").User(**GOOD_USER)
        assert user.name == "Ana Silva"
        assert user.id == 1

    def test_converts_a_numeric_string(self, load):
        user = load("models.py").User(**{**GOOD_USER, "id": "7"})
        assert user.id == 7 and isinstance(user.id, int)

    @pytest.mark.parametrize("field,bad", [
        ("id", "seven"),
        ("name", ""),
        ("email", "no-at-sign"),
    ])
    def test_rejects_bad_values(self, load, field, bad):
        User = load("models.py").User
        with pytest.raises(ValidationError):
            User(**{**GOOD_USER, field: bad})

    def test_email_rule_is_yours(self, load):
        """'no-at-sign' is a perfectly good str - only your validator objects."""
        User = load("models.py").User
        with pytest.raises(ValidationError) as caught:
            User(**{**GOOD_USER, "email": "nope"})
        assert "@" in str(caught.value) or "email" in str(caught.value)

    def test_missing_field_is_rejected(self, load):
        User = load("models.py").User
        with pytest.raises(ValidationError):
            User(id=1, name="Ana", email="a@b.com")


class TestProduct:
    def test_accepts_a_good_record(self, load):
        p = load("models.py").Product(**GOOD_PRODUCT)
        assert p.price == 4.5 and p.in_stock is True

    def test_in_stock_defaults_to_true(self, load):
        raw = {k: v for k, v in GOOD_PRODUCT.items() if k != "in_stock"}
        assert load("models.py").Product(**raw).in_stock is True

    @pytest.mark.parametrize("price", [0, -1, -0.01])
    def test_rejects_a_non_positive_price(self, load, price):
        Product = load("models.py").Product
        with pytest.raises(ValidationError):
            Product(**{**GOOD_PRODUCT, "price": price})


class TestOrder:
    def test_accepts_a_good_record(self, load):
        o = load("models.py").Order(id=100, user_id=1, product_id=10, quantity=2)
        assert o.quantity == 2

    @pytest.mark.parametrize("quantity", [0, -1])
    def test_rejects_a_non_positive_quantity(self, load, quantity):
        Order = load("models.py").Order
        with pytest.raises(ValidationError):
            Order(id=1, user_id=1, product_id=1, quantity=quantity)


class TestParse:
    def test_parse_user(self, load):
        assert load("parse.py").parse_user(GOOD_USER).name == "Ana Silva"

    def test_parse_user_raises_on_rubbish(self, load):
        with pytest.raises(ValidationError):
            load("parse.py").parse_user({"id": "x"})

    def test_parse_users_keeps_the_good_ones(self, load):
        raw = [GOOD_USER, {"id": "bad"}, {**GOOD_USER, "id": 2, "name": "Ben"}]
        users = load("parse.py").parse_users(raw)
        assert len(users) == 2, (
            "parse_users skips records that fail rather than giving up. "
            "Three good users beat none."
        )
        assert [u.name for u in users] == ["Ana Silva", "Ben"]

    def test_parse_users_of_nothing(self, load):
        assert load("parse.py").parse_users([]) == []

    def test_parse_users_all_bad(self, load):
        assert load("parse.py").parse_users([{"id": "x"}, {}]) == []

    def test_parse_products(self, load):
        raw = [GOOD_PRODUCT, {**GOOD_PRODUCT, "price": -5}]
        assert len(load("parse.py").parse_products(raw)) == 1

    def test_count_bad(self, load):
        mod = load("parse.py")
        User = load("models.py").User
        raw = [GOOD_USER, {"id": "x"}, {}, {**GOOD_USER, "email": "nope"}]
        assert mod.count_bad(raw, User) == 3


class TestPipeline:
    def test_fetch_users_returns_models(self, load, base_url):
        users = load("pipeline.py").fetch_users(base_url)
        assert len(users) == 4
        assert users[0].name == "Ana Silva", (
            "Return validated model objects, not dicts - a dict has no shape, "
            "which is the whole thing we are fixing today."
        )
        assert not isinstance(users[0], dict)

    def test_fetch_products(self, load, base_url):
        products = load("pipeline.py").fetch_products(base_url)
        assert len(products) == 4
        assert all(p.price > 0 for p in products)

    def test_fetch_products_filtered(self, load, base_url):
        products = load("pipeline.py").fetch_products(base_url, "toys")
        assert len(products) == 2
        assert all(p.category == "toys" for p in products)

    def test_total_stock_value_ignores_out_of_stock(self, load, base_url):
        """Gadget at 12.00 is out of stock. 4.50 + 3.25 + 89.00 = 96.75."""
        assert load("pipeline.py").total_stock_value(base_url) == 96.75
