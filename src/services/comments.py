from functools import lru_cache

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.base import ListQuery
from db.models.comments import Comment
from schemas.comment import CommentSchema
from services.exceptions import NotFound


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
        WITH RECURSIVE temp1 ( id, post, comment, text, path, level ) AS (
                SELECT
                       c.id,
                       c.post,
                       c.comment,
                       c.text,
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
                       c_r.text
                FROM comments AS c_r
                WHERE c_r.comment is NULL
                  AND c_r.id > :offset
                LIMIT :limit
            )
            SELECT id, post, comment, text, level from temp1 ORDER BY PATH
        """)
        params = {
            "post_id": post_id,
            "offset": query.offset,
            "limit": query.limit
        }
        comments = await self.db.execute(sql_text, params)
        return comments.all()

    async def create(self, comment: CommentSchema) -> Comment:
        db_comment = Comment(**comment.dict())
        self.db.add(db_comment)
        await self.db.commit()
        return db_comment

    async def update(self, comment_id: int, comment: CommentSchema) -> Comment:
        db_comment = await self.get(comment_id)
        db_comment.update(**comment.dict(exclude_none=True))

        await self.db.commit()
        return db_comment

    async def delete(self, comment_id: int) -> None:
        db_comment = await self.get(comment_id)
        await self.db.delete(db_comment)
        await self.db.commit()


@lru_cache(maxsize=128)
def get_comments_service(db: Session = Depends(get_db)) -> CommentsService:
    return CommentsService(db)
