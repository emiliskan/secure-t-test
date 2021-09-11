import os

API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = os.getenv("API_PORT", "8000")

API_SERVICE_URL = f"{API_HOST}:{API_PORT}"
API = "v1"
