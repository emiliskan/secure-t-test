from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.ext.hybrid import hybrid_property

from db.models.base import AbstractModel


class Comment(AbstractModel):
    __tablename__ = "comments"

    post = Column(Integer, ForeignKey("posts.id"))
    comment = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    text = Column(String)

    @hybrid_property
    def is_answer(self):
        return self.comment is None
