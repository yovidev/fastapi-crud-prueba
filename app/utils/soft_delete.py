from sqlalchemy import Column, Boolean, select, DateTime
from sqlalchemy.ext.asyncio import AsyncSession

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

async def get_non_deleted(session: AsyncSession, model_class):
    stmt = select(model_class).where(model_class.is_deleted == False)
    result = await session.execute(stmt)
    return result.scalars().all()