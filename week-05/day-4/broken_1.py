# Should print:  Missing user: none found
import requests

response = requests.get("http://127.0.0.1:8765/users/99", timeout=5)
user = response.json()
print("Missing user:", user["name"])
