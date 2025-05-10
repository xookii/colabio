from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas.auth import SignUpSchema, SignInSchema
from src.services.auth import new_user, new_session

from src.dependencies import get_current_user

router = APIRouter(
    prefix="/auth", 
    tags=["auth"]
)

@router.post("/signup")
async def signup(
    credentials: SignUpSchema, 
    db: AsyncSession = Depends(get_db)
):
    return await new_user(credentials, db)

@router.post("/signin")
async def signin(
    credentials: SignInSchema,
    db: AsyncSession = Depends(get_db)
):
    return await new_session(credentials, db)
