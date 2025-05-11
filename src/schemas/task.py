from pydantic import BaseModel, Field, EmailStr

from typing import Optional

class NewTaskSchema(BaseModel):
    project_id: int
    title: str = Field(
        min_length=5,
        max_length=100
    )
    description: Optional[str] = None
    assignee_email: EmailStr
