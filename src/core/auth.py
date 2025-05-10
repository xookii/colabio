from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from src.config import JWT_SECRET, JWT_ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(email: str):
    payload = {
        "email": email
    }
    token = jwt.encode(
        payload, JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )
    return token
