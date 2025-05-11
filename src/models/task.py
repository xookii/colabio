from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from typing import Optional

from src.database import Model

class TaskModel(Model):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    title: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(default="to-do")