# Should print 5.0, then "Cannot divide by zero" instead of crashing.

def divide(a, b):
    try:
        return a / b
    except ValueError:
        return "Cannot divide by zero"


print(divide(10, 2))
print(divide(10, 0))
