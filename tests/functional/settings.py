import os

API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = os.getenv("API_PORT", "8000")

API_SERVICE_URL = f"{API_HOST}:{API_PORT}"
API = "v1"

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
USER_ID = os.getenv("USER_ID", "3")
