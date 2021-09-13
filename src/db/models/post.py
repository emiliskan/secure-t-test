from sqlalchemy import Column, String, ForeignKey
from db.models.base import AbstractModel


class Post(AbstractModel):
    __tablename__ = "posts"

    text = Column(String)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
