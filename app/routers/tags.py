from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..core.database import get_db
from ..core.security import get_current_active_user
from ..crud.tag import create_tag, get_tags, get_tag, update_tag, soft_delete_tag
from ..schemas.tag import TagCreate, Tag

router = APIRouter()

@router.post("/", response_model=Tag)
async def create_tag_endpoint(tag_in: TagCreate, db=Depends(get_db), current_user=Depends(get_current_active_user)):
    return await create_tag(db, tag_in)

@router.get("/", response_model=List[Tag])
async def read_tags(skip: int = 0, limit: int = 100, db=Depends(get_db), current_user=Depends(get_current_active_user)):
    return await get_tags(db, skip, limit)

@router.get("/{tag_id}", response_model=Tag)
async def read_tag(tag_id: int, db=Depends(get_db), current_user=Depends(get_current_active_user)):
    tag = await get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.put("/{tag_id}", response_model=Tag)
async def update_tag_endpoint(tag_id: int, tag_in: TagCreate, db=Depends(get_db), current_user=Depends(get_current_active_user)):
    tag = await update_tag(db, tag_id, tag_in)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.delete("/{tag_id}")
async def delete_tag_endpoint(tag_id: int, db=Depends(get_db), current_user=Depends(get_current_active_user)):
    await soft_delete_tag(db, tag_id)
    return {"detail": "Tag soft deleted"}