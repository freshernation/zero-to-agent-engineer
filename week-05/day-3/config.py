"""Configuration and secrets.

    get_api_key()   value of COURSE_API_KEY, or raises RuntimeError naming it
    get_base_url()  API_BASE_URL, defaulting to http://127.0.0.1:8765
    load_config()   a dict with "api_key" and "base_url"

import os
from dotenv import load_dotenv
"""
