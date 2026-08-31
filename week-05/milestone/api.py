"""Everything that touches the network. No printing.

    class ApiError(Exception): pass

    ApiClient(base_url, api_key=None, timeout=5, retries=3)
        get(path, params=None)   parsed body, or raises ApiError
        users()                  list[User]
        products()               list[Product]
        orders(user_id=None)     list[Order]

Session, Bearer header when a key is given, retry 5xx with backoff,
ApiError on 4xx or exhausted retries. Skip records that fail validation.
"""
