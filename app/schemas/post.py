from datetime import datetime

from pydantic import BaseModel, constr
from typing import Optional, List
from ..schemas.user import User
from ..schemas.tag import Tag

class PostBase(BaseModel):
    title: constr(min_length=5, max_length=200)
    content: constr(min_length=10, max_length=1000)

class PostCreate(PostBase):
    tag_ids: Optional[List[int]] = None

class PostUpdate(BaseModel):
    title: Optional[constr(min_length=5, max_length=200)] = None
    content: Optional[constr(min_length=10, max_length=1000)] = None
    tag_ids: Optional[List[int]] = None

class Post(PostBase):
    id: int
    owner_id: int
    owner: User
    tags: List[Tag] = []
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True