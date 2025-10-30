from .auth import router as auth_router
from .users import router as users_router
from .posts import router as posts_router
from .tags import router as tags_router

__all__ = ["auth_router", "users_router", "posts_router", "tags_router"]