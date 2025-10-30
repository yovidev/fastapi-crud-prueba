from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.hashing import get_password_hash
from ..models.entities import User
from ..schemas.user import UserCreate, UserUpdate
from ..utils.soft_delete import get_non_deleted

async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email, User.is_deleted == False)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: UserCreate):
    hashed_password = get_password_hash(user_in.password)
    current_time = datetime.utcnow()
    db_user = User(
        **user_in.dict(exclude={"password"}),
        hashed_password=hashed_password,
        created_at=current_time,
        updated_at=current_time
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    await db.refresh(db_user, attribute_names=['id', 'email', 'name', 'hashed_password', 'created_at', 'updated_at',
                                               'is_deleted', 'deleted_at'])
    return db_user

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    users = await get_non_deleted(db, User)
    return users[skip : skip + limit]

async def get_user(db: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id, User.is_deleted == False)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    values = user_update.dict(exclude_unset=True)
    if values:
        values['updated_at'] = datetime.utcnow()
        stmt = update(User).where(User.id == user_id, User.is_deleted == False).values(**values).returning(User)
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()
    return await get_user(db, user_id)

async def soft_delete_user(db: AsyncSession, user_id: int):
    current_time = datetime.utcnow()
    stmt = update(User).where(User.id == user_id).values(
        is_deleted=True,
        deleted_at=current_time,
        updated_at=current_time
    )
    await db.execute(stmt)
    await db.commit()
    return user_id