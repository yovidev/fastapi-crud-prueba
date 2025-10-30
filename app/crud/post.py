from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.entities import Post, Tag
from ..schemas.post import PostCreate, PostUpdate
from ..utils.soft_delete import get_non_deleted
from ..crud.tag import get_tag  # Define después

async def create_post(db: AsyncSession, post_in: PostCreate, owner_id: int):
    db_post = Post(**post_in.dict(exclude={"tag_ids"}), owner_id=owner_id)
    if post_in.tag_ids:
        tags = [await get_tag(db, tid) for tid in post_in.tag_ids if await get_tag(db, tid)]
        db_post.tags = tags
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post, ["tags", "owner"])
    return db_post

async def get_posts(db: AsyncSession, owner_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    stmt = select(Post).options(selectinload(Post.tags), selectinload(Post.owner)).where(Post.is_deleted == False)
    if owner_id:
        stmt = stmt.where(Post.owner_id == owner_id)
    result = await db.execute(stmt)
    posts = result.scalars().all()
    return posts[skip : skip + limit]

async def get_post(db: AsyncSession, post_id: int):
    stmt = select(Post).options(selectinload(Post.tags), selectinload(Post.owner)).where(Post.id == post_id, Post.is_deleted == False)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_post(db: AsyncSession, post_id: int, post_update: PostUpdate, current_owner_id: int):
    post = await get_post(db, post_id)
    if post and post.owner_id != current_owner_id:
        raise ValueError("Not authorized")  # Raise HTTP en router
    values = post_update.dict(exclude_unset=True, exclude={"tag_ids"})
    if values:
        for key, value in values.items():
            setattr(post, key, value)
    if post_update.tag_ids is not None:
        post.tags = [await get_tag(db, tid) for tid in post_update.tag_ids if await get_tag(db, tid)]
    await db.commit()
    await db.refresh(post, ["tags", "owner"])
    return post

async def soft_delete_post(db: AsyncSession, post_id: int):
    stmt = update(Post).where(Post.id == post_id).values(is_deleted=True)
    await db.execute(stmt)
    await db.commit()
    return post_id