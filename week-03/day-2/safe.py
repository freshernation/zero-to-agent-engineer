"""Functions that never crash. Catch the SPECIFIC exception each time.

    to_int(text, default=0)         text as a whole number, or default
    to_float(text, default=0.0)     text as a decimal, or default
    safe_divide(a, b)               a / b, or None if b is zero

    to_int("42")        -> 42
    to_int("abc")       -> 0
    to_int("abc", -1)   -> -1
    safe_divide(10, 0)  -> None

A bare "except:" fails a test. Name the exception you expect.
"""
