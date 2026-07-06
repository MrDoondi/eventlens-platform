from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import SubscriptionPlan
from app.models.base import BaseModel


class Organization(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )

    logo_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        Enum(
            SubscriptionPlan,
            values_callable=lambda enum: [e.value for e in enum],
            name="subscription_plan",
        ),
        default=SubscriptionPlan.FREE,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )