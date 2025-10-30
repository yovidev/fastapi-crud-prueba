from .user import User, UserCreate, UserUpdate
from .post import Post, PostCreate, PostUpdate
from .tag import Tag, TagCreate

User.model_rebuild()
Post.model_rebuild()
Tag.model_rebuild()