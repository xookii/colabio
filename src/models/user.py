from sqlalchemy.orm import Mapped, mapped_column

from src.database import Model

class UserModel(Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str]
    password_hash: Mapped[str]