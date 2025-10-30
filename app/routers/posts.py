from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_db
from ..core.security import get_current_active_user
from ..crud.post import create_post, get_posts, get_post, update_post, soft_delete_post
from ..schemas.post import PostCreate, PostUpdate, Post
from ..models.entities import User
from ..crud.tag import create_tag  # Si necesitas tags on fly

router = APIRouter()

@router.post("/", response_model=Post)
async def create_post_endpoint(post_in: PostCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return await create_post(db, post_in, current_user.id)

@router.get("/", response_model=List[Post])
async def read_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await get_posts(db, current_user.id, skip, limit)

@router.get("/{post_id}", response_model=Post)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    post = await get_post(db, post_id)
    if not post or post.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=Post)
async def update_post_endpoint(
    post_id: int, post_update: PostUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    updated = await update_post(db, post_id, post_update, current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated

@router.delete("/{post_id}")
async def delete_post_endpoint(post_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    post = await get_post(db, post_id)
    if not post or post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await soft_delete_post(db, post_id)
    return {"detail": "Post soft deleted"}