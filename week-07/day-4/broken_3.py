# Should print:  Results: ['4', '2']
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from fake_model import FakeClient, Message, ToolUseBlock, assistant_turn, text_reply
from toolkit import all_schemas, run_tool, tool_uses

client = FakeClient([
    Message(
        [
            ToolUseBlock("calculate", {"expression": "2+2"}, "t1"),
            ToolUseBlock("word_count", {"text": "a b"}, "t2"),
        ],
        stop_reason="tool_use",
    ),
    text_reply("Both done."),
])

messages = [{"role": "user", "content": "two things"}]

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    tools=all_schemas(),
    messages=messages,
)

messages.append(assistant_turn(response))

results = []
for block in tool_uses(response):
    results.append({
        "type": "tool_result",
        "tool_use_id": "t1",
        "content": run_tool(block.name, block.input),
    })

messages.append({"role": "user", "content": results})

client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    tools=all_schemas(),
    messages=messages,
)

print("Results:", [block["content"] for block in results])
