# Three CrewAI tools with real docstrings.
#
#   calculate(expression)   arithmetic; returns "Unsafe expression" for anything
#                           else - RETURNS the message, does not raise
#   city_info(city)         "Lisbon is in Portugal, population 545000."
#                           "I don't know about Narnia."
#   word_count(text)        how many words
#
# from crewai.tools import tool
#
# CrewAI tools return strings and should not raise - an exception inside a crew
# is much harder to see than one in your own loop.

CITIES = {
    "Lisbon": {"country": "Portugal", "population": 545000},
    "Lagos": {"country": "Nigeria", "population": 15400000},
    "Bogota": {"country": "Colombia", "population": 7900000},
    "Mumbai": {"country": "India", "population": 12500000},
}
