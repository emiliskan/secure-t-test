from schemas.base import AbstractModel


class Post(AbstractModel):

    class Config:
        orm_mode = True
