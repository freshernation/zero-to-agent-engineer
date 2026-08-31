"""The same four tools in week-7 shape - plain functions plus hand-written schemas.

Given to you, so the hand-written agent has something to call that does not
depend on LangChain. Compare it with toolkit.py, which is the same four tools
with @tool doing the schema work.

That comparison is one row of Friday's table, already written for you.
"""

CITIES = {
    "Lisbon": {"country": "Portugal", "population": 545000},
    "Lagos": {"country": "Nigeria", "population": 15400000},
    "Bogota": {"country": "Colombia", "population": 7900000},
    "Mumbai": {"country": "India", "population": 12500000},
}

SAFE_CHARACTERS = set("0123456789+-*/(). ")


def calculate(expression):
    if not expression or not set(expression) <= SAFE_CHARACTERS:
        raise ValueError("Unsafe expression")
    try:
        return eval(expression, {"__builtins__": {}}, {})
    except (SyntaxError, ZeroDivisionError, TypeError, NameError):
        raise ValueError("Unsafe expression")


def word_count(text):
    return len(text.split())


def city_info(city):
    facts = CITIES.get(city)
    if facts is None:
        return f"I don't know about {city}."
    return f"{city} is in {facts['country']}, population {facts['population']}."


def reverse_text(text):
    return text[::-1]


TOOLS = {
    "calculate": calculate,
    "word_count": word_count,
    "city_info": city_info,
    "reverse_text": reverse_text,
}


def _param(description):
    return {"type": "string", "description": description}


def _schema(name, description, properties, required):
    return {
        "name": name,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }


def all_schemas():
    return [
        _schema(
            "calculate",
            "Evaluate a basic arithmetic expression such as '2 + 2 * 3'. Use this "
            "whenever a number needs working out rather than guessing at it.",
            {"expression": _param("The arithmetic to evaluate.")},
            ["expression"],
        ),
        _schema(
            "word_count",
            "Count the words in a piece of text. Use this when asked how long "
            "something is rather than estimating.",
            {"text": _param("The text to count the words in.")},
            ["text"],
        ),
        _schema(
            "city_info",
            "Look up the country and population of a named city. Use this for "
            "facts about a specific city, not for weather.",
            {"city": _param("The name of the city, correctly capitalised.")},
            ["city"],
        ),
        _schema(
            "reverse_text",
            "Return a piece of text with its characters in reverse order. Use "
            "this for word puzzles and palindromes.",
            {"text": _param("The text to reverse.")},
            ["text"],
        ),
    ]


def run_tool(name, arguments):
    function = TOOLS.get(name)
    if function is None:
        return f"Unknown tool: {name}"
    try:
        return str(function(**arguments))
    except Exception as error:
        return f"Tool failed: {error}"
