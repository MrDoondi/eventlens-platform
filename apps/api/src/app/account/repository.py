from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.account.models import Account
from app.account.schemas import AccountCreate


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: AccountCreate) -> Account:
        account = Account(
            organization_id=data.organization_id,
            full_name=data.full_name,
            email=data.email,
            password_hash=data.password_hash,
            role=data.role,
        )

        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)

        return account

    def get_by_email(self, email: str) -> Account | None:
        statement = select(Account).where(
            Account.email == email,
        )

        return self.db.scalar(statement)

    def get_by_id(self, account_id: UUID) -> Account | None:
        statement = select(Account).where(
            Account.id == account_id,
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
            .order_by(Account.created_at)
        )

        return list(self.db.scalars(statement))
    
    def update(
        self,
        account: Account,
    ) -> Account:
        self.db.commit()
        self.db.refresh(account)
        return account