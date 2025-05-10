from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class NewProjectSchema(BaseModel):
    name: str = Field(
        min_length = 5,
        max_length = 300
    )
    description: Optional[str] = Field(
        default = None,
        min_length = 8,
        max_length = 500
    )

class NewProjectMemberSchema(BaseModel):
    project_id: int
    email: EmailStr
    role: Optional[str] = None

class GetMemberSchema(BaseModel):
    username: str
    email: EmailStr
    role: str
    