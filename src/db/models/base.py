from sqlalchemy import Column, Integer

from db.database import Base


class AbstractModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

