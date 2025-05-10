from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.user import UserModel

async def get_user_by_email(email: EmailStr, db: AsyncSession):
    query = await db.execute(select(UserModel).where(UserModel.email == email))
    return query.scalar_one_or_none()
        