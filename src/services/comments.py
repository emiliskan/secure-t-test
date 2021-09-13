from functools import lru_cache

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.base import ListQuery
from db.models.comments import Comment
from schemas.comment import CommentSchema
from services.exceptions import NotFound, NotAllowed


class CommentsService:

    def __init__(self, db: Session):
        self.db = db

    async def get(self, comment_id: int) -> Comment:
        item = await self.db.get(Comment, comment_id)
        if not item:
            raise NotFound

        return item

    async def read(self, post_id: int, query: ListQuery) -> list[Comment]:
        sql_text = text("""
        WITH RECURSIVE temp1 ( id, post, comment, text, user_id, path, level ) AS (
                SELECT
                       c.id,
                       c.post,
                       c.comment,
                       c.text,
                       c.user_id,
                       CAST (c.id AS VARCHAR (50)) as PATH,
                       1
                FROM root_comments c
                WHERE c.comment IS NULL and c.post = :post_id
            UNION
                SELECT
                       c2.id,
                       c2.post,
                       c2.comment,
                       c2.text,
                       c2.user_id,
                       CAST ( temp1.path ||'->'|| c2.id AS VARCHAR(50)),
                       level + 1
                FROM comments c2
                INNER JOIN temp1 ON( temp1.id = c2.comment)
            ),
            root_comments AS
            (
                SELECT
                       c_r.id,
                       c_r.post,
                       c_r.comment,
                       c_r.text,
                       c_r.user_id
                FROM comments AS c_r
                WHERE c_r.comment is NULL
                  AND c_r.id > :offset
                LIMIT :limit
            )
            SELECT id, post, comment, user_id, text, level, path from temp1 ORDER BY path
        """)
        params = {
            "post_id": post_id,
            "offset": query.offset,
            "limit": query.limit
        }
        comments = await self.db.execute(sql_text, params)
        return comments.all()

    async def create(self, user_id: int, comment: CommentSchema) -> Comment:
        db_comment = Comment(**comment.dict())
        db_comment.user_id = user_id
        self.db.add(db_comment)
        await self.db.commit()
        return db_comment

    async def update(self, user_id: int, comment_id: int, comment: CommentSchema) -> Comment:
        db_comment = await self.get(comment_id)
        if db_comment.user_id != user_id:
            raise NotAllowed

        comment.user_id = user_id
        db_comment.update(**comment.dict(exclude_none=True))

        await self.db.commit()
        return db_comment

    async def delete(self, user_id: int, comment_id: int) -> None:
        db_comment = await self.get(comment_id)
        if db_comment.user_id != user_id:
            raise NotAllowed

        await self.db.delete(db_comment)
        await self.db.commit()


@lru_cache(maxsize=128)
def get_comments_service(db: Session = Depends(get_db)) -> CommentsService:
    return CommentsService(db)
