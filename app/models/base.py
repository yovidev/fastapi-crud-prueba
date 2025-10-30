from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from ..utils.timestamps import TimestampsMixin
from ..utils.soft_delete import SoftDeleteMixin

Base = declarative_base()

class BaseModel(Base, TimestampsMixin, SoftDeleteMixin):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)

