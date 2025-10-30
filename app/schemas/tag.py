from datetime import datetime

from pydantic import BaseModel, constr
from typing import List
from ..schemas.post import Post

class TagBase(BaseModel):
    name: constr(min_length=1, max_length=50)

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    posts: List[Post] = []
    create_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True