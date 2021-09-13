from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.ext.hybrid import hybrid_property

from db.models.base import AbstractModel


class Comment(AbstractModel):
    __tablename__ = "comments"

    post = Column(Integer, ForeignKey("posts.id"), index=True)
    comment = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    text = Column(String)

    @hybrid_property
    def is_answer(self):
        return self.comment is None
