from pydantic import BaseModel, EmailStr, Field, validator


class AuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length = 8,
        max_length = 50
    )


class SignUpSchema(AuthSchema):
    username: str = Field(
        min_length = 4,
        max_length = 50
    )

    @validator("username", pre=True)
    def strip_username(cls, v):
        return v.strip().lower()


class SignInSchema(AuthSchema):
    pass