"""Yesterday's answer, given to you complete.

Today the loop is the only thing you are building, so the tools are provided.
Read this file - you will need to know exactly what run_tool returns.
"""

CITIES = {
    "Lisbon": {"country": "Portugal", "population": 545000},
    "Lagos": {"country": "Nigeria", "population": 15400000},
    "Bogota": {"country": "Colombia", "population": 7900000},
    "Mumbai": {"country": "India", "population": 12500000},
}

SAFE_CHARACTERS = set("0123456789+-*/(). ")


def calculate(expression):
    """Return the value of a basic arithmetic expression."""
    if not expression or not set(expression) <= SAFE_CHARACTERS:
        raise ValueError("Unsafe expression")
    try:
        return eval(expression, {"__builtins__": {}}, {})
    except (SyntaxError, ZeroDivisionError, TypeError, NameError):
        raise ValueError("Unsafe expression")


def word_count(text):
    """Return how many words are in the text."""
    return len(text.split())


def city_info(city):
    """Return a sentence about a city, or say we do not know it."""
    facts = CITIES.get(city)
    if facts is None:
        return f"I don't know about {city}."
    return f"{city} is in {facts['country']}, population {facts['population']}."


TOOLS = {
    "calculate": calculate,
    "word_count": word_count,
    "city_info": city_info,
}


def text_param(description):
    return {"type": "string", "description": description}


def make_schema(name, description, properties, required):
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
    """Return one schema per tool."""
    return [
        make_schema(
            "calculate",
            "Evaluate a basic arithmetic expression such as '2 + 2 * 3'. "
            "Only + - * / and parentheses are supported.",
            {"expression": text_param("The arithmetic to evaluate.")},
            ["expression"],
        ),
        make_schema(
            "word_count",
            "Count the words in a piece of text.",
            {"text": text_param("The text to count the words in.")},
            ["text"],
        ),
        make_schema(
            "city_info",
            "Look up the country and population of a named city.",
            {"city": text_param("The name of the city, correctly capitalised.")},
            ["city"],
        ),
    ]


def run_tool(name, arguments):
    """Run one tool and return its result as a string. Never raises."""
    function = TOOLS.get(name)
    if function is None:
        return f"Unknown tool: {name}"
    try:
        return str(function(**arguments))
    except Exception as error:
        return f"Tool failed: {error}"


def tool_uses(response):
    """Return only the tool_use blocks from a response."""
    return [block for block in response.content if block.type == "tool_use"]


def extract_text(response):
    """Return every text block joined."""
    return "".join(b.text for b in response.content if b.type == "text")
