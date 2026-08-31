"""Turning raw API data into models.

    parse_user(raw)             a User, or raises ValidationError
    parse_users(raw_list)       list of Users, SKIPPING any that fail
    parse_products(raw_list)    same, for Product
    count_bad(raw_list, model)  how many records fail validation

from models import User, Product
from pydantic import ValidationError
"""
