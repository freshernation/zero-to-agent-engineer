# Should print:  Answer: Stopped after 3 steps without finishing.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from fake_model import FakeClient, assistant_turn, tool_reply
from toolkit import all_schemas, extract_text, run_tool, tool_uses


def run(client, question, max_iterations=3):
    messages = [{"role": "user", "content": question}]

    for step in range(max_iterations):
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            tools=all_schemas(),
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            return extract_text(response)

        messages.append(assistant_turn(response))
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": run_tool(block.name, block.input),
                }
                for block in tool_uses(response)
            ],
        })


client = FakeClient(tool_reply("calculate", {"expression": "1+1"}, id="t1"))
print("Answer:", run(client, "go forever"))
