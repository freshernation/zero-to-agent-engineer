"""Timeouts and auth.

    fetch_with_timeout(base_url, path, timeout)
        the parsed body, or the string "timed out" if it took too long

    get_secret(base_url, api_key)
        the parsed body, or None if the key is rejected

The API key is course-key-123 and the header is:  Authorization: Bearer <key>
"""
