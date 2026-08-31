"""One object that knows the base URL, the key, the timeout and the retries.

    class ApiError(Exception): pass

    ApiClient(base_url, api_key=None, timeout=5, retries=3)
        get(path, params=None)          parsed body; raises ApiError on 4xx or
                                        an exhausted retry
        get_or_none(path, params=None)  same, but returns None instead
        users()                         list of users
        user(user_id)                   one user, or None
        products(category=None)         the products

Use a requests.Session. Send Authorization when a key was given. Retry 5xx.
"""
