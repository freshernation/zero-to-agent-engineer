"""Reading status codes.

    status_of(base_url, path)   the status code as an int
    is_ok(base_url, path)       True for ANY 2xx, False otherwise
    fetch_json(base_url, path)  the parsed body for a 2xx, None for anything else

path looks like "/users" or "/error".
"""
