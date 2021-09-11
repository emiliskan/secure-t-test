from sqlalchemy import Column, Integer, Float, String

from db.database import Base


class Post(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    x = Column(Float, index=True)
    y = Column(Float, index=True)
