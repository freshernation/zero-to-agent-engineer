"""Shapes. This file is CORRECT and you must not change it.

Your job today is to write test_shapes.py to test it.
"""

PI = 3.14159


class Circle:
    def __init__(self, radius):
        if radius <= 0:
            raise ValueError("Radius must be positive")
        self.radius = radius

    def __repr__(self):
        return f"Circle({self.radius})"

    def area(self):
        """Return the area, rounded to 2 decimal places."""
        return round(PI * self.radius * self.radius, 2)

    def circumference(self):
        """Return the distance around the edge, rounded to 2 decimal places."""
        return round(2 * PI * self.radius, 2)


class Square:
    def __init__(self, side):
        if side <= 0:
            raise ValueError("Side must be positive")
        self.side = side

    def __repr__(self):
        return f"Square({self.side})"

    def area(self):
        """Return the area."""
        return self.side * self.side

    def perimeter(self):
        """Return the distance around the outside."""
        return 4 * self.side


def total_area(shapes):
    """Return the combined area of every shape, rounded to 2 decimal places."""
    return round(sum(shape.area() for shape in shapes), 2)


def largest(shapes):
    """Return the shape with the biggest area, or None if there are none."""
    if not shapes:
        return None
    return max(shapes, key=lambda shape: shape.area())
