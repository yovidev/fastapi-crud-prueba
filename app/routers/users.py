from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import get_db
from ..core.security import get_current_active_user
from ..crud.user import create_user, get_users, get_user, update_user, soft_delete_user
from ..schemas.user import UserCreate, UserUpdate, User

router = APIRouter()

@router.post("/", response_model=User)
async def create_user_endpoint(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user_in)

@router.get("/", response_model=List[User])
async def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return await get_users(db, skip, limit)

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user_endpoint(
    user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated = await update_user(db, user_id, user_update)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_active_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await soft_delete_user(db, user_id)
    return {"detail": "User soft deleted"}