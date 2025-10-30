from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import BaseModel


post_tags = Table(
    'post_tags',
    BaseModel.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class User (BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    posts = relationship("Post", back_populates="owner",cascade="all, delete-orphan")

class Post (BaseModel):
    __tablename__ = 'posts'
    id=Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(String(1000), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner=relationship("User", back_populates="posts")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

class Tag (BaseModel):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    posts = relationship("Post", secondary=post_tags, back_populates="tags")