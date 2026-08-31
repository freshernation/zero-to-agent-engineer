"""Fetching from the practice API.

    get_users(base_url)                     the list of user dicts
    get_user(base_url, user_id)             one user dict, or None on 404
    get_products(base_url, category=None)   all products, or just that category

get_products must use params=, not an f-string URL.
Always pass timeout=.

import requests
"""
