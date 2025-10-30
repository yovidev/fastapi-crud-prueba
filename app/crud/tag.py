from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.entities import Tag
from ..schemas.tag import TagCreate
from ..utils.soft_delete import get_non_deleted

async def get_tag(db: AsyncSession, tag_id: int):
    stmt = select(Tag).where(Tag.id == tag_id, Tag.is_deleted == False)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_tag(db: AsyncSession, tag_in: TagCreate):
    current_time = datetime.utcnow()
    db_tag = Tag(
        **tag_in.dict(),
        created_at=current_time,
        updated_at=current_time
    )
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

async def get_tags(db: AsyncSession, skip: int = 0, limit: int = 100):
    tags = await get_non_deleted(db, Tag)
    return tags[skip : skip + limit]


async def update_tag(db: AsyncSession, tag_id: int, tag_update: TagCreate):
    current_time = datetime.utcnow()
    stmt = update(Tag).where(Tag.id == tag_id, Tag.is_deleted == False).values(
        **tag_update.dict(),
        updated_at=current_time
    ).returning(Tag)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()

async def soft_delete_tag(db: AsyncSession, tag_id: int):
    current_time = datetime.utcnow()
    stmt = update(Tag).where(Tag.id == tag_id).values(
        is_deleted=True,
        deleted_at=current_time,
        updated_at=current_time
    )
    await db.execute(stmt)
    await db.commit()
    return tag_id