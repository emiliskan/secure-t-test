from schemas.base import AbstractModel


class CommentSchema(AbstractModel):

    post: int
    comment: int = None
    text: str
    user_id: int = 0

    class Config:
        orm_mode = True
