# Should print:  Attempts: 1
import time

import requests

for attempt in range(3):
    response = requests.get("http://127.0.0.1:8765/users/99", timeout=5)
    if response.status_code == 200:
        break
    time.sleep(0.01)

print("Attempts:", attempt + 1)
