from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.user import User
from schemas.user import UserSchema, LoginSchema, TokenSchema
from werkzeug.security import check_password_hash, generate_password_hash

from services.exceptions import AuthFailed
from utils.tokens import generate_tokens


class UsersService:

    def __init__(self, db: Session):
        self.db = db

    async def create(self, user: UserSchema) -> TokenSchema:
        db_user = User(**user.dict())
        db_user.password = generate_password_hash(user.password)
        self.db.add(db_user)
        await self.db.commit()
        return generate_tokens(db_user.id)

    async def login(self, login_data: LoginSchema) -> TokenSchema:

        users_result = await self.db.execute(
            select(
                User.id,
                User.password
            ).where(
                User.username == login_data.username
            )
        )
        users_result = users_result.all()
        if not users_result:
            raise AuthFailed

        db_user = users_result[0]
        if not check_password_hash( db_user.password, login_data.password):
            raise AuthFailed

        return generate_tokens(db_user.id)


@lru_cache(maxsize=128)
def get_user_service(db: Session = Depends(get_db)) -> UsersService:
    return UsersService(db)
