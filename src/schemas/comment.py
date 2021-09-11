from schemas.base import AbstractModel


class CommentSchema(AbstractModel):

    post: int
    comment: int = None
    text: str

    class Config:
        orm_mode = True
