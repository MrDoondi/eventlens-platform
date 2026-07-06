from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.account.schemas import AccountResponse


class RegisterRequest(BaseModel):
    organization_slug: str = Field(
        min_length=3,
        max_length=150,
    )

    full_name: str = Field(
        min_length=2,
        max_length=150,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    account: AccountResponse

class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    account: AccountResponse