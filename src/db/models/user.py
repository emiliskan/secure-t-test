from sqlalchemy import Column, String
from db.models.base import AbstractModel


class User(AbstractModel):
    __tablename__ = "users"

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
