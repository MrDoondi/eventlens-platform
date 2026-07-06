from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.account.models import Account
from app.account.schemas import AccountCreate
from app.common.repository import BaseRepository


class AccountRepository(BaseRepository[Account]):
    def __init__(self, db: Session):
        super().__init__(db, Account)

    def create(
        self,
        data: AccountCreate,
    ) -> Account:
        account = Account(
            **data.model_dump(),
        )

        return super().create(account)

    def get_by_email(
        self,
        email: str,
    ) -> Account | None:
        statement = (
            select(Account)
            .where(Account.email == email)
        )

        return self.db.scalar(statement)

    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[Account]:
        statement = (
            select(Account)
            .where(
                Account.organization_id == organization_id,
            )
            .order_by(Account.created_at.desc())
        )

        return list(self.db.scalars(statement).all())