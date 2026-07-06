from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.enums import AccountRole


class AccountCreate(BaseModel):
    organization_id: UUID
    full_name: str
    email: EmailStr
    password_hash: str
    role: AccountRole = AccountRole.PHOTOGRAPHER


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID

    full_name: str
    email: EmailStr

    role: AccountRole

    is_active: bool
    is_verified: bool

    created_at: datetime
    updated_at: datetime