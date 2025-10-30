from datetime import datetime
from pydantic import BaseModel, constr, ConfigDict
from typing import List

class TagBase(BaseModel):
    name: constr(min_length=1, max_length=50)

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class TagWithPosts(Tag):
    posts: List['Post'] = []

from .post import Post
TagWithPosts.update_forward_refs()