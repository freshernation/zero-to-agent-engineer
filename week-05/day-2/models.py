"""Pydantic models for the practice API.

    User     id: int, name: str (>= 1 char), email: str (must contain @), city: str
    Product  id: int, name: str, price: float (> 0), category: str,
             in_stock: bool = True
    Order    id: int, user_id: int, product_id: int, quantity: int (>= 1)

from pydantic import BaseModel, Field, field_validator
"""
