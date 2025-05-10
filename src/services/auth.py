from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.schemas.auth import SignUpSchema, SignInSchema
from src.models.user import UserModel
from src.core.auth import create_access_token, hash_password, verify_password

async def new_user(
    credentials: SignUpSchema, 
    db: AsyncSession
):
    password_hash = hash_password(credentials.password)
    user = UserModel(
        email=credentials.email,
        username=credentials.username,
        password_hash=password_hash
    )
    try:
        db.add(user)
        await db.commit()
        return user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email is already in use"
        )

async def new_session(
    credentials: SignInSchema,
    db: AsyncSession
):
    query = await db.execute(select(UserModel).where(UserModel.email == credentials.email))
    user = query.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )
    
    token = create_access_token(user.email)
    return {"access_token": token}