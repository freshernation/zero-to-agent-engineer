"""Week 5 milestone - the customer report.

Run me:  pytest week-05/milestone -v
"""

import pytest

EXPECTED = """CUSTOMER ORDER REPORT
==================================================
Ana Silva            Lisbon
  Widget                2 x $   4.50 = $     9.00
  Doohickey             1 x $   3.25 = $     3.25
  2 orders, $12.25

Ben Okafor           Lagos
  Thingummy             3 x $  89.00 = $   267.00
  1 order, $267.00

Cara Diaz            Bogota
  No orders

Dev Patel            Mumbai
  Gadget                1 x $  12.00 = $    12.00
  1 order, $12.00

==================================================
TOP CUSTOMERS
1. Ben Okafor          $   267.00
2. Ana Silva           $    12.25
3. Dev Patel           $    12.00
Total revenue: $291.25"""

DEAD_URL = "http://127.0.0.1:9999"


@pytest.fixture
def client(load, base_url):
    return load("api.py").ApiClient(base_url)


class TestModels:
    def test_user_rejects_a_bad_email(self, load):
        from pydantic import ValidationError
        User = load("models.py").User
        with pytest.raises(ValidationError):
            User(id=1, name="Ana", email="nope", city="Lisbon")

    def test_product_rejects_a_bad_price(self, load):
        from pydantic import ValidationError
        Product = load("models.py").Product
        with pytest.raises(ValidationError):
            Product(id=1, name="Widget", price=0, category="tools")

    def test_order_rejects_a_bad_quantity(self, load):
        from pydantic import ValidationError
        Order = load("models.py").Order
        with pytest.raises(ValidationError):
            Order(id=1, user_id=1, product_id=1, quantity=0)


class TestApiClient:
    def test_users_are_models(self, client):
        users = client.users()
        assert len(users) == 4
        assert users[0].name == "Ana Silva"
        assert not isinstance(users[0], dict), (
            "users() returns validated models, not raw dicts."
        )

    def test_products(self, client):
        products = client.products()
        assert len(products) == 4
        assert all(p.price > 0 for p in products)

    def test_orders_all(self, client):
        assert len(client.orders()) == 4

    def test_orders_for_one_user(self, client):
        orders = client.orders(user_id=1)
        assert len(orders) == 2
        assert all(o.user_id == 1 for o in orders)

    def test_get_raises_on_4xx(self, load, base_url):
        mod = load("api.py")
        with pytest.raises(mod.ApiError):
            mod.ApiClient(base_url).get("/users/99")

    def test_raises_when_the_server_errors(self, load, base_url):
        mod = load("api.py")
        with pytest.raises(mod.ApiError):
            mod.ApiClient(base_url, retries=2).get("/error")

    def test_retries_a_flaky_endpoint(self, load, base_url, reset_flaky):
        client = load("api.py").ApiClient(base_url, retries=3)
        assert client.get("/flaky")["message"] == "Worth the wait"

    def test_sends_the_api_key(self, load, base_url):
        client = load("api.py").ApiClient(base_url, api_key="course-key-123")
        assert client.get("/secret")["message"] == "You found the secret"

    def test_dead_host_raises_api_error(self, load):
        mod = load("api.py")
        with pytest.raises(mod.ApiError):
            mod.ApiClient(DEAD_URL, timeout=1, retries=1).get("/users")

    def test_one_bad_record_does_not_lose_the_rest(self, load, base_url, monkeypatch):
        """A single malformed product must not cost you the whole report."""
        mod = load("api.py")
        client = mod.ApiClient(base_url)
        real_get = client.get

        def poisoned(path, params=None):
            data = real_get(path, params)
            if path == "/products":
                return data + [{"id": 99, "name": "Broken", "price": -5,
                                "category": "x", "in_stock": True}]
            return data

        monkeypatch.setattr(client, "get", poisoned)
        products = client.products()
        assert len(products) == 4, (
            f"Got {len(products)} products. The malformed one should be skipped "
            "and the other four kept - not an exception, and not five."
        )


class TestReport:
    def test_build_rows(self, load, client):
        mod = load("report.py")
        user = client.users()[0]
        by_id = {p.id: p for p in client.products()}
        rows = mod.build_rows(client, user, by_id, client.orders(user_id=user.id))
        assert len(rows) == 2
        assert rows[0]["product"] == "Widget"
        assert rows[0]["line_total"] == 9.0

    def test_summarise_is_ranked(self, load, client):
        summaries = load("report.py").summarise(client)
        assert [s["name"] for s in summaries] == [
            "Ben Okafor", "Ana Silva", "Dev Patel", "Cara Diaz",
        ]

    def test_summarise_totals(self, load, client):
        summaries = load("report.py").summarise(client)
        by_name = {s["name"]: s for s in summaries}
        assert by_name["Ana Silva"]["total_spent"] == 12.25
        assert by_name["Ben Okafor"]["total_spent"] == 267.0
        assert by_name["Cara Diaz"]["total_spent"] == 0
        assert by_name["Cara Diaz"]["order_count"] == 0

    def test_render_returns_a_string(self, load, client):
        mod = load("report.py")
        rendered = mod.render(mod.summarise(client))
        assert isinstance(rendered, str), (
            "render() builds and returns the report. Only main() prints - that "
            "is what makes it testable without capturing stdout."
        )

    def test_render_matches_exactly(self, load, client):
        mod = load("report.py")
        actual = mod.render(mod.summarise(client)).rstrip("\n")
        assert actual == EXPECTED, (
            "The report does not match.\n\nExpected:\n"
            + "\n".join(f"  |{ln}" for ln in EXPECTED.splitlines())
            + "\n\nYours:\n"
            + "\n".join(f"  |{ln}" for ln in actual.splitlines())
        )

    def test_singular_order(self, load, client):
        mod = load("report.py")
        rendered = mod.render(mod.summarise(client))
        assert "1 order, $267.00" in rendered
        assert "1 orders" not in rendered

    def test_no_orders_has_no_summary_line(self, load, client):
        mod = load("report.py")
        rendered = mod.render(mod.summarise(client))
        assert "No orders" in rendered
        assert "0 orders" not in rendered, (
            "A customer with nothing gets 'No orders' and nothing else."
        )

    def test_main_prints_the_report(self, run):
        run("report.py").expect("Total revenue: $291.25")

    def test_main_survives_a_dead_api(self, run):
        # A non-zero exit code is correct here - the report genuinely failed.
        # What must not happen is a traceback.
        r = run("report.py", env={"API_BASE_URL": DEAD_URL}, allow_crash=True)
        r.expect(f"Could not reach the API at {DEAD_URL}")
        assert "Traceback" not in r.stderr, (
            "main() produced a traceback. When the API is unreachable it should "
            "say so in one line and stop."
        )


class TestLayering:
    def test_api_and_models_do_not_print(self, load, source):
        for name, attribute in (("api.py", "ApiClient"), ("models.py", "User")):
            getattr(load(name), attribute)  # nothing to check until it exists
            assert "print(" not in source(name, code_only=True), (
                f"{name} contains a print(). Presentation lives in report.py."
            )

    def test_report_does_not_touch_the_network(self, load, source):
        load("report.py").render  # nothing to check until it exists
        code = source("report.py", code_only=True)
        assert "import requests" not in code, (
            "report.py imports requests. Everything that touches the network "
            "goes through ApiClient - that is what makes the report testable."
        )

    def test_every_call_has_a_timeout(self, source):
        code = source("api.py", code_only=True)
        assert "timeout" in code, "No timeout= anywhere in api.py."

    def test_no_key_in_the_source(self, load, source):
        load("api.py").ApiClient  # nothing to check until it exists
        for name in ("api.py", "report.py", "models.py"):
            assert "course-key-123" not in source(name, code_only=True), (
                f"There is a real key in {name}. Keys come from the environment."
            )
