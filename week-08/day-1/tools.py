# Four @tool functions with REAL docstrings - the docstring is the prompt now.
#
#   calculate(expression)   arithmetic; ValueError("Unsafe expression") otherwise
#   word_count(text)        how many words
#   city_info(city)         "Lisbon is in Portugal, population 545000."
#                           "I don't know about Narnia."
#   reverse_text(text)      the text backwards
#
#   all_tools()             the list of all four
#   tool_by_name(name)      one tool, or None
#   describe_tools()        "calculate: Evaluate a basic..." per line
#
# from langchain_core.tools import tool

CITIES = {
    "Lisbon": {"country": "Portugal", "population": 545000},
    "Lagos": {"country": "Nigeria", "population": 15400000},
    "Bogota": {"country": "Colombia", "population": 7900000},
    "Mumbai": {"country": "India", "population": 12500000},
}
