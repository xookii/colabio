from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional

from src.database import Model


class ProjectModel(Model):
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]


class ProjectMemberModel(Model):
    __tablename__ = "project_members"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    role: Mapped[str] = mapped_column(default="member")
