"""Week 7's agent, handed back as one function, with two tools.

Given to you complete. This week is about what happens when there are several
agents, so the loop itself is not the exercise - read it once, then use it.

    result = run_agent(client, system, schemas, tools, task)

    result["text"]            the final answer, or why it stopped
    result["stopped"]         "answered" or "cap"
    result["steps"]           how many times the model was called
    result["input_tokens"]    summed over every call
    result["output_tokens"]   summed over every call
    result["tool_calls"]      [{"name": ..., "input": ..., "result": ...}, ...]
"""

from fake_model import assistant_turn

MODEL = "claude-sonnet-5-5"

CITIES = {
    "Lisbon": 545000,
    "Lagos": 15400000,
    "Bogota": 7900000,
    "Mumbai": 12500000,
}

SAFE_CHARACTERS = set("0123456789+-*/(). ")


def lookup_population(city):
    """Return a city's population as a string of digits."""
    if city not in CITIES:
        raise ValueError(f"No data for {city}")
    return str(CITIES[city])


def calculate(expression):
    """Evaluate basic arithmetic: + - * / and parentheses."""
    if not expression or not set(expression) <= SAFE_CHARACTERS:
        raise ValueError("Unsafe expression")
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except (SyntaxError, ZeroDivisionError, TypeError, NameError):
        raise ValueError("Unsafe expression")


LOOKUP_SCHEMA = {
    "name": "lookup_population",
    "description": (
        "Look up how many people live in a city. Use this for any population "
        "figure rather than recalling one."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "The city, e.g. Lisbon"}
        },
        "required": ["city"],
    },
}

CALCULATE_SCHEMA = {
    "name": "calculate",
    "description": (
        "Evaluate a basic arithmetic expression such as '2 + 2 * 3'. Use this "
        "whenever a number needs working out rather than guessing at it."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "e.g. 545000 + 7900000"}
        },
        "required": ["expression"],
    },
}

TOOLS = {"lookup_population": lookup_population, "calculate": calculate}
SCHEMAS = [LOOKUP_SCHEMA, CALCULATE_SCHEMA]


def _run_tool(tools, name, arguments):
    """Always a string. Success or failure, the model gets an answer."""
    if name not in tools:
        return f"Unknown tool: {name}"
    try:
        return str(tools[name](**arguments))
    except Exception as error:
        return f"Tool failed: {error}"


def run_agent(client, system, schemas, tools, task, max_steps=6, model=MODEL):
    """Run one agent on one task, from an empty conversation, until it stops."""
    messages = [{"role": "user", "content": task}]
    result = {
        "text": "",
        "stopped": "cap",
        "steps": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "tool_calls": [],
    }

    for _ in range(max_steps):
        request = {
            "model": model,
            "max_tokens": 1000,
            "system": system,
            "messages": list(messages),   # a copy: the list grows below
        }
        if schemas:
            request["tools"] = schemas
        response = client.messages.create(**request)

        result["steps"] += 1
        result["input_tokens"] += response.usage.input_tokens
        result["output_tokens"] += response.usage.output_tokens

        if response.stop_reason != "tool_use":
            result["text"] = "".join(
                b.text for b in response.content if b.type == "text"
            )
            result["stopped"] = "answered"
            return result

        messages.append(assistant_turn(response))
        answers = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            outcome = _run_tool(tools, block.name, block.input)
            result["tool_calls"].append(
                {"name": block.name, "input": block.input, "result": outcome}
            )
            answers.append(
                {"type": "tool_result", "tool_use_id": block.id, "content": outcome}
            )
        messages.append({"role": "user", "content": answers})

    result["text"] = f"Stopped after {max_steps} steps without finishing."
    return result
