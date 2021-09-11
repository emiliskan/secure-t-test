from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.post import Post
from schemas.base import ListQuery
from schemas.post import PostSchema
from services.exceptions import NotFound


class UserNotFound(Exception):
    ...


class PostsService:

    def __init__(self, db: Session):
        self.db = db

    async def get(self, post_id: int) -> Post:
        item = await self.db.get(Post, post_id)
        if not item:
            raise NotFound

        return item

    async def read(self, query: ListQuery) -> list[Post]:
        # TODO: offset
        posts = await self.db.execute(
            select(
                Post.id,
                Post.text
            ).limit(query.limit)
        )
        return posts.all()

    async def create(self, post: PostSchema) -> None:
        db_post = Post(**post.dict())
        self.db.add(db_post)
        await self.db.commit()

    async def update(self, post_id: int, post: PostSchema) -> None:
        db_post = await self.get(post_id)
        db_post.update(**post.dict(exclude_none=True))

        await self.db.commit()

    async def delete(self, post_id: int) -> None:
        db_post = await self.get(post_id)
        await self.db.delete(db_post)
        await self.db.commit()


@lru_cache(maxsize=128)
def get_post_service(db: Session = Depends(get_db)) -> PostsService:
    return PostsService(db)
