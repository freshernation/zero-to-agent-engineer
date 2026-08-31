# Should print:  Reply: All good
#
# Two things are wrong here.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fake_model import FakeClient, ModelError, text_reply

client = FakeClient([
    ModelError("overloaded"),
    text_reply("All good"),
    text_reply("stale answer from an attempt that should never have happened"),
])

reply = None
for attempt in range(3):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=100,
            messages=[{"role": "user", "content": "hi"}],
        )
        reply = response.content[0].text
    except Exception:
        pass

print("Reply:", reply)
