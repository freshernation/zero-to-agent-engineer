"""Wednesday's logging, given to you complete."""

import json
import uuid

SECRET_KEYS = ("api_key", "authorization", "token")


def new_request_id():
    """One id per request. It is what turns noise into a story."""
    return uuid.uuid4().hex[:12]


def redact(fields, secret_keys=SECRET_KEYS):
    """Replace anything that looks like a secret, at any depth."""
    lowered = {key.lower() for key in secret_keys}
    cleaned = {}

    for key, value in fields.items():
        if key.lower() in lowered:
            cleaned[key] = "****"
        elif isinstance(value, dict):
            cleaned[key] = redact(value, secret_keys)
        else:
            cleaned[key] = value

    return cleaned


def log_line(level, event, **fields):
    """Return one structured log line. Events, not prose."""
    return json.dumps({"level": level, "event": event, **redact(fields)})


def parse(line):
    """Read a log line back."""
    return json.loads(line)
