from sqlalchemy import Column, String
from schemas.base import AbstractModel


class Post(AbstractModel):
    __tablename__ = "posts"

    text = Column(String)
