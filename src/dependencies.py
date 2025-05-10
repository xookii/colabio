from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import PyJWTError # Все ошибки jwt наследуются от PyJWTError
from sqlalchemy import select
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt

from src.config import JWT_SECRET, JWT_ALGORITHM
from src.models.user import UserModel
from src.database import get_db

token_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials= Depends(token_scheme), 
    db: AsyncSession = Depends(get_db)
) -> UserModel:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
    except PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    email = payload.get("email")
    query = await db.execute(select(UserModel).where(UserModel.email == email))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    return user