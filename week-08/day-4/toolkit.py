"""Monday's tools, given to you complete.

Today the graph is the only thing you are building.
"""

from langchain_core.tools import tool

CITIES = {
    "Lisbon": {"country": "Portugal", "population": 545000},
    "Lagos": {"country": "Nigeria", "population": 15400000},
    "Bogota": {"country": "Colombia", "population": 7900000},
    "Mumbai": {"country": "India", "population": 12500000},
}

SAFE_CHARACTERS = set("0123456789+-*/(). ")


@tool
def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as '2 + 2 * 3'.

    Use this whenever a number needs working out rather than guessing at it.
    Only + - * / and parentheses are supported.
    """
    if not expression or not set(expression) <= SAFE_CHARACTERS:
        raise ValueError("Unsafe expression")
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except (SyntaxError, ZeroDivisionError, TypeError, NameError):
        raise ValueError("Unsafe expression")


@tool
def word_count(text: str) -> str:
    """Count the words in a piece of text.

    Use this when asked how long something is, rather than estimating.
    """
    return str(len(text.split()))


@tool
def city_info(city: str) -> str:
    """Look up the country and population of a named city.

    Use this for facts about a specific city, not for weather or directions.
    """
    facts = CITIES.get(city)
    if facts is None:
        return f"I don't know about {city}."
    return f"{city} is in {facts['country']}, population {facts['population']}."


@tool
def reverse_text(text: str) -> str:
    """Return a piece of text with its characters in reverse order.

    Use this for word puzzles and for checking palindromes.
    """
    return text[::-1]


def all_tools():
    """Return every tool."""
    return [calculate, word_count, city_info, reverse_text]


def tool_by_name(name):
    """Return one tool by name, or None."""
    for tool_function in all_tools():
        if tool_function.name == name:
            return tool_function
    return None


def describe_tools():
    """Return one line per tool: its name and the first line of its description."""
    return "\n".join(
        f"{t.name}: {t.description.splitlines()[0]}" for t in all_tools()
    )
