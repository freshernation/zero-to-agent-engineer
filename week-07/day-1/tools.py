# Three real functions. No model involved - these are just Python.
#
#   calculate(expression)   the result as a number
#                           ValueError("Unsafe expression") for anything but
#                           digits, spaces, and  + - * / ( ) .
#   word_count(text)        how many words
#   city_info(city)         "Lisbon is in Portugal, population 545000."
#                           "I don't know about Narnia."
#
# Do NOT eval unfiltered input. Check the characters first.

CITIES = {
    "Lisbon": {"country": "Portugal", "population": 545000},
    "Lagos": {"country": "Nigeria", "population": 15400000},
    "Bogota": {"country": "Colombia", "population": 7900000},
    "Mumbai": {"country": "India", "population": 12500000},
}
