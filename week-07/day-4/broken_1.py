# Should print:  Answer: It is 391.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from fake_model import FakeClient, text_reply, tool_reply
from toolkit import all_schemas, extract_text, run_tool, tool_uses

client = FakeClient([
    tool_reply("calculate", {"expression": "17 * 23"}, id="t1"),
    text_reply("It is 391."),
])

messages = [{"role": "user", "content": "What is 17 * 23?"}]

for step in range(3):
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        tools=all_schemas(),
        messages=messages,
    )

    if response.stop_reason != "tool_use":
        print("Answer:", extract_text(response))
        break

    results = []
    for block in tool_uses(response):
        results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": run_tool(block.name, block.input),
        })

    messages.append({"role": "user", "content": results})
