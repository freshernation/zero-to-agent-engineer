"""A small web API that runs on your own machine.

    python3 week-05/server.py

Then open http://127.0.0.1:8765/users in a browser, or point your code at it.
The tests start their own copy automatically, so you only need to run this when
you want to poke at it by hand.

It behaves like a real API, including the parts of real APIs that ruin your day:
one endpoint is slow, one fails intermittently, one returns broken JSON, and one
is simply on fire.

You never need to change this file. You do need to read the endpoint list.
"""

import json
import re
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

PORT = 8765

USERS = [
    {"id": 1, "name": "Ana Silva", "email": "ana@example.com", "city": "Lisbon"},
    {"id": 2, "name": "Ben Okafor", "email": "ben@example.com", "city": "Lagos"},
    {"id": 3, "name": "Cara Diaz", "email": "cara@example.com", "city": "Bogota"},
    {"id": 4, "name": "Dev Patel", "email": "dev@example.com", "city": "Mumbai"},
]

PRODUCTS = [
    {"id": 10, "name": "Widget", "price": 4.50, "category": "tools", "in_stock": True},
    {"id": 11, "name": "Gadget", "price": 12.00, "category": "tools", "in_stock": False},
    {"id": 12, "name": "Doohickey", "price": 3.25, "category": "toys", "in_stock": True},
    {"id": 13, "name": "Thingummy", "price": 89.00, "category": "toys", "in_stock": True},
]

ORDERS = [
    {"id": 100, "user_id": 1, "product_id": 10, "quantity": 2},
    {"id": 101, "user_id": 1, "product_id": 12, "quantity": 1},
    {"id": 102, "user_id": 2, "product_id": 13, "quantity": 3},
    {"id": 103, "user_id": 4, "product_id": 11, "quantity": 1},
]

API_KEY = "course-key-123"

_flaky_calls = {"count": 0}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # keep the test output readable

    def _send(self, status, payload, raw=False):
        body = payload if raw else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/users":
            return self._send(200, USERS)

        match = re.fullmatch(r"/users/(\d+)", path)
        if match:
            for user in USERS:
                if user["id"] == int(match.group(1)):
                    return self._send(200, user)
            return self._send(404, {"error": "User not found"})

        if path == "/products":
            category = query.get("category", [None])[0]
            if category is None:
                return self._send(200, PRODUCTS)
            return self._send(
                200, [p for p in PRODUCTS if p["category"] == category]
            )

        if path == "/orders":
            user_id = query.get("user_id", [None])[0]
            if user_id is None:
                return self._send(200, ORDERS)
            return self._send(
                200, [o for o in ORDERS if str(o["user_id"]) == user_id]
            )

        if path == "/secret":
            if self.headers.get("Authorization") != f"Bearer {API_KEY}":
                return self._send(401, {"error": "Unauthorized"})
            return self._send(200, {"message": "You found the secret"})

        if path == "/slow":
            time.sleep(3)
            return self._send(200, {"message": "Sorry I took so long"})

        if path == "/flaky":
            _flaky_calls["count"] += 1
            if _flaky_calls["count"] % 3 != 0:
                return self._send(503, {"error": "Try again"})
            return self._send(200, {"message": "Worth the wait", "attempts": 3})

        if path == "/reset-flaky":
            _flaky_calls["count"] = 0
            return self._send(200, {"ok": True})

        if path == "/broken":
            return self._send(200, b'{"this": "is not valid json"', raw=True)

        if path == "/error":
            return self._send(500, {"error": "Something went wrong"})

        return self._send(404, {"error": "No such endpoint"})


def serve_in_background():
    """Start the server on a daemon thread and return it. Used by the tests."""
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


if __name__ == "__main__":
    print(f"Serving on http://127.0.0.1:{PORT}")
    print("Endpoints: /users  /users/<id>  /products  /orders  /secret")
    print("           /slow  /flaky  /broken  /error")
    print("Ctrl-C to stop.")
    try:
        HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
