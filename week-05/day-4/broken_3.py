# Should print:  City: Lisbon
#
# One bug, hidden by one bad habit. Fix the habit first.
import requests

BASE = "http://127.0.0.1:8765"


def get_city(user_id):
    try:
        response = requests.get(f"{BASE}/users/{user_id}", timeout=5)
        return response.json()["citty"]
    except Exception:
        return "unknown"


print("City:", get_city(1))
