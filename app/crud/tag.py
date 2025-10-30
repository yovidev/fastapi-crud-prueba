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
    db_tag = Tag(**tag_in.dict())
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

async def get_tags(db: AsyncSession, skip: int = 0, limit: int = 100):
    tags = await get_non_deleted(db, Tag)
    return tags[skip : skip + limit]

# Update y soft_delete similares a user