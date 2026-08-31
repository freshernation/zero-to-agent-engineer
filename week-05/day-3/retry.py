"""Trying again, sensibly.

    fetch_with_retry(base_url, path, attempts=3, delay=0.05)
        the parsed body, or None if every attempt failed

    attempts_used(base_url, path, attempts=3, delay=0.05)
        how many attempts it actually took

    should_retry(status_code)
        True for 5xx, False for everything else

Retry 5xx, not 4xx. Back off between attempts.
"""
