from functools import lru_cache
from math import sqrt
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.post import UserDatabase
from schemas.user import User
from utils.distance import calc_distance


class UserExists(Exception):
    ...


class UserNotFound(Exception):
    ...


class UsersService:

    def __init__(self, db: Session):
        self.db: Session = db

    async def new_user(self, user_data: User) -> UserDatabase:
        db_user = UserDatabase(**user_data.dict())
        self.db.add(db_user)

        try:
            await self.db.commit()
        except IntegrityError:
            raise UserExists
        return db_user

    async def get_user(self, user_id: int) -> UserDatabase:
        users = await self.db.execute(
            select(
                UserDatabase
            ).where(
                UserDatabase.id == user_id
            )
        )
        user = users.scalar()
        if not user:
            raise UserNotFound

        return user

    async def save_user_location(self, user: User) -> UserDatabase:
        db_user = await self.get_user(user.id)
        db_user.x = user.x
        db_user.y = user.y
        await self.db.flush()

        return db_user

    async def get_users_near(self, user_id: int, radius: float, count: int) -> List[UserDatabase]:
        db_user: UserDatabase = await self.get_user(user_id)
        user_x = db_user.x
        user_y = db_user.y

        x_min = max(user_x - radius, 0)
        y_min = max(user_y - radius, 0)

        x_max = user_x + radius
        y_max = user_y + radius

        # get near users
        distance = calc_distance(user_x, UserDatabase.x, user_y, UserDatabase.y)
        users_in_rect = \
            select(
                distance,
                UserDatabase.id,
                UserDatabase.x,
                UserDatabase.y,
                UserDatabase.name
            ).where(
                UserDatabase.x > x_min, UserDatabase.y >= y_min,
                UserDatabase.x <= x_max, UserDatabase.y <= y_max
            ).order_by(distance)
        users_in_radius = \
            select(
                users_in_rect
            ).where(
                users_in_rect.distance < radius
            )

        near_users = await self.db.execute(users_in_radius)
        near_users = near_users.all()

        # calculate and sort by distance
        near_users = list(filter(
            lambda u: u[0] <= radius,
            near_users
        ))

        return near_users[:count]


@lru_cache(maxsize=128)
def get_users_service(db: Session = Depends(get_db)) -> UsersService:
    return UsersService(db)
