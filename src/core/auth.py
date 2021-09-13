"""
Auth integration
"""

import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from utils.tokens import get_payload
oauth_schema = HTTPBearer()


async def auth(authorization: HTTPAuthorizationCredentials = Depends(oauth_schema)):
    try:
        payload = get_payload(authorization.credentials)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User id not found.")
        return user_id
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials.",
                            headers={"WWW-Authenticate": "Bearer"})