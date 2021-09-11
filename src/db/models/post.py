from sqlalchemy import Column, String
from db.models.base import AbstractModel


class Post(AbstractModel):
    __tablename__ = "posts"

    text = Column(String)
