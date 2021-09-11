from schemas.base import AbstractModel


class PostSchema(AbstractModel):

    text: str

    class Config:
        orm_mode = True
