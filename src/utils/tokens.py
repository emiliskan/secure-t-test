import uuid

import jwt

from core.config import JWT_SECRET, JWT_ALGORITHM
from schemas.user import TokenSchema


def generate_tokens(user_id: int) -> TokenSchema:
    """Generate access and refresh tokens."""

    payload = {"user_id": user_id}
    access_token = jwt.encode(payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)

    token = TokenSchema(access_token=access_token)
    return token


def get_payload(access_token: str) -> dict:
    return jwt.decode(access_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
