from uuid import UUID

from app.account.models import Account
from app.account.repository import AccountRepository
from app.account.schemas import AccountCreate


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def create(self, data: AccountCreate) -> Account:
        return self.repository.create(data)

    def get_by_email(self, email: str) -> Account | None:
        return self.repository.get_by_email(email)

    def get_by_id(self, account_id: UUID) -> Account | None:
        return self.repository.get_by_id(account_id)

    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[Account]:
        return self.repository.list_by_organization(
            organization_id,
        )
    
    def update(
        self,
        account: Account,
    ) -> Account:
        return self.repository.update(account)