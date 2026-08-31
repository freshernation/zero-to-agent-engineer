"""Point(x, y)

    .x  .y              attributes
    __repr__            "Point(3, 4)"
    __eq__              equal when both coordinates match;
                        NotImplemented for anything that is not a Point
    distance_to(other)  straight-line distance, rounded to 2dp
    move(dx, dy)        returns nothing - shifts this point

Distance:  ((x2-x1)**2 + (y2-y1)**2) ** 0.5
"""
