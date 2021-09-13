from schemas.base import AbstractModel


class PostSchema(AbstractModel):

    text: str
    user_id: int = 0

    class Config:
        orm_mode = True
