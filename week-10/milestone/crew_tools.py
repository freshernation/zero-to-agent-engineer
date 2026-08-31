"""The same tools again, in CrewAI's shape."""

from crewai.tools import tool

CITIES = {
    "Lisbon": {"country": "Portugal", "population": 545000},
    "Lagos": {"country": "Nigeria", "population": 15400000},
    "Bogota": {"country": "Colombia", "population": 7900000},
    "Mumbai": {"country": "India", "population": 12500000},
}

SAFE_CHARACTERS = set("0123456789+-*/(). ")


@tool("calculate")
def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as '2 + 2 * 3'.

    Use this whenever a number needs working out rather than guessing at it.
    Only + - * / and parentheses are supported.
    """
    if not expression or not set(expression) <= SAFE_CHARACTERS:
        return "Unsafe expression"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except (SyntaxError, ZeroDivisionError, TypeError, NameError):
        return "Unsafe expression"


@tool("city_info")
def city_info(city: str) -> str:
    """Look up the country and population of a named city.

    Use this for facts about a specific city rather than recalling them.
    """
    facts = CITIES.get(city)
    if facts is None:
        return f"I don't know about {city}."
    return f"{city} is in {facts['country']}, population {facts['population']}."


@tool("word_count")
def word_count(text: str) -> str:
    """Count the words in a piece of text.

    Use this when asked how long something is rather than estimating it.
    """
    return str(len(text.split()))
