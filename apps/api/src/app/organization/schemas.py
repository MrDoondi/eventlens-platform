from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import SubscriptionPlan


class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    slug: str = Field(..., min_length=2, max_length=150)
    logo_url: str | None = None
    subscription_plan: SubscriptionPlan = SubscriptionPlan.FREE


class OrganizationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    slug: str | None = Field(default=None, min_length=2, max_length=150)
    logo_url: str | None = None
    subscription_plan: SubscriptionPlan | None = None
    is_active: bool | None = None


class OrganizationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    logo_url: str | None
    subscription_plan: SubscriptionPlan
    is_active: bool


class OrganizationListResponse(BaseModel):
    organizations: list[OrganizationResponse]