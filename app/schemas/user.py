from pydantic import BaseModel, EmailStr, constr, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: constr(min_length=2, max_length=100)

class UserCreate(UserBase):
    password: constr(min_length=8, max_length=100)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[constr(min_length=2, max_length=100)] = None

class User(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    posts: List['Post'] = []

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)